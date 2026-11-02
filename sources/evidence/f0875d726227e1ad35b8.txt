using System.Buffers.Binary;
using System.Text;
using System.Text.RegularExpressions;
using DataManager.Core.Binary;

namespace DataManager.Core.Appearance;

internal static class SaveAppearanceFormats
{
    internal const int PeaceLength = 0x40650;
    internal const int BattleLength = 0x43A86;
    private static readonly UTF8Encoding StrictUtf8 = new(false, true);

    internal static int ValidateSave(byte[] bytes, int prefixLength)
    {
        if (prefixLength != 0x30000 || bytes.Length < PeaceLength || bytes[0x30000] != 5 || bytes[0x4062D] != 5)
            throw new InvalidDataException("不是已验证的完整原生存档，或原生段头损坏。");
        var nativeLength = bytes[0x30002] == 3 ? BattleLength : PeaceLength;
        if (bytes.Length < nativeLength) throw new InvalidDataException("原生存档正文已截断。");
        if (bytes.Length == nativeLength) return nativeLength;
        const int footerLength = 168;
        if (bytes.Length < nativeLength + 68 + footerLength || !bytes.AsSpan(bytes.Length - footerLength, 8).SequenceEqual("XASTAT2F"u8))
            throw new InvalidDataException("存在未知、损坏或截断的附加存档尾部，保留原文件。");
        var footer = bytes.AsSpan(bytes.Length - footerLength);
        var payloadLength = checked((int)U64(footer, 24));
        if (U32(footer, 8) != 2 || U32(footer, 12) != footerLength || U64(footer, 16) != (ulong)nativeLength ||
            payloadLength < 68 || payloadLength > 64 * 1024 * 1024 ||
            (long)nativeLength + payloadLength + footerLength != bytes.Length || !footer[160..].SequenceEqual("XASTATEN"u8))
            throw new InvalidDataException("战场统计尾部版本、长度或结束标记无效。");
        var payload = bytes.AsSpan(nativeLength, payloadLength);
        if (!footer.Slice(32, 64).SequenceEqual(Encoding.ASCII.GetBytes(HashService.Sha256(bytes[..nativeLength]))) ||
            !footer.Slice(96, 64).SequenceEqual(Encoding.ASCII.GetBytes(HashService.Sha256(payload.ToArray()))))
            throw new InvalidDataException("原生存档或内嵌战场统计 SHA-256 不匹配。");
        ValidatePayload(payload);
        return nativeLength;
    }

    private static void ValidatePayload(ReadOnlySpan<byte> bytes)
    {
        if (!bytes[..8].SequenceEqual("XASTAT2P"u8) || U32(bytes, 8) != 2 || U32(bytes, 12) != 68 ||
            (U32(bytes, 16) & ~3u) != 0 || U32(bytes, 20) > 250 || U32(bytes, 24) > 65535 ||
            U32(bytes, 28) > 1024 || U32(bytes, 32) > 4096 || I32(bytes, 36) < -1 || I32(bytes, 36) >= 65535 ||
            (U32(bytes, 40) & ~255u) != 0)
            throw new InvalidDataException("内嵌统计人物数量、版本或文本字段无效。");
        var offset = checked(68 + (int)(U32(bytes, 28) + U32(bytes, 32)) * 2);
        ValidateRows(bytes, ref offset, U32(bytes, 20), embedded: true);
        ValidateRows(bytes, ref offset, U32(bytes, 24), embedded: true);
        if (offset != bytes.Length) throw new InvalidDataException("内嵌统计人物数据截断或有未知尾部。");
    }

    internal static byte[] UpdateEmbeddedHash(byte[] candidate, int nativeLength)
    {
        if (candidate.Length > nativeLength)
            Encoding.ASCII.GetBytes(HashService.Sha256(candidate[..nativeLength])).CopyTo(candidate, candidate.Length - 168 + 32);
        return candidate;
    }

    internal static byte[] UpdateSidecar(byte[] before, string beforeSaveHash, string afterSaveHash)
    {
        if (before.Length < 96 || before.Length > 1024 * 1024 || !before.AsSpan(0, 8).SequenceEqual("XA66STAT"u8) ||
            U32(before, 8) != 1 || U32(before, 12) > 1 || U32(before, 16) > 250 || U32(before, 20) > 1024 ||
            !before.AsSpan(32, 64).SequenceEqual(Encoding.ASCII.GetBytes(beforeSaveHash.ToLowerInvariant())))
            throw new InvalidDataException("已有战场统计旁文件损坏、版本未知或与当前存档不匹配。");
        var offset = checked(96 + (int)U32(before, 20) * 2);
        ValidateRows(before, ref offset, U32(before, 16), embedded: false);
        if (offset != before.Length) throw new InvalidDataException("战场统计旁文件人物记录不完整或有未知尾部。");
        var after = (byte[])before.Clone();
        Encoding.ASCII.GetBytes(afterSaveHash.ToLowerInvariant()).CopyTo(after, 32);
        return after;
    }

    private static void ValidateRows(ReadOnlySpan<byte> bytes, ref int offset, uint count, bool embedded)
    {
        var seen = new HashSet<int>();
        var size = embedded ? 72 : 68;
        for (var i = 0u; i < count; i++)
        {
            if (offset < 0 || offset > bytes.Length - size) throw new InvalidDataException("统计人物记录被截断。");
            var row = bytes.Slice(offset, size);
            var person = I32(row, 0);
            var totals = embedded ? row[4..] : row;
            var slot = I32(totals, 0);
            if (!seen.Add(person) || (embedded ? person < 0 || person >= 65535 || slot < -1 || slot >= 250 : slot < 0 || slot >= 250) ||
                I32(totals, 4) < 0 || U32(totals, 64) > 256)
                throw new InvalidDataException("统计人物 ID、槽位、文本长度或重复记录无效。");
            for (var field = 8; field < 64; field += 8)
                if (BinaryPrimitives.ReadInt64LittleEndian(totals[field..]) < 0)
                    throw new InvalidDataException("统计记录含负计数。");
            offset = checked(offset + size + (int)U32(totals, 64) * 2);
            if (offset > bytes.Length) throw new InvalidDataException("统计人物标签被截断。");
        }
        if (offset > bytes.Length) throw new InvalidDataException("统计文本被截断。");
    }

    internal static byte[] UpdateIni(byte[] before, string beforeSaveHash, string afterSaveHash, bool requireHash = false)
    {
        Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
        Encoding encoding;
        var preamble = 0;
        if (before.AsSpan().StartsWith(new byte[] { 0xFF, 0xFE })) { encoding = new UnicodeEncoding(false, false, true); preamble = 2; }
        else if (before.AsSpan().StartsWith(new byte[] { 0xFE, 0xFF })) { encoding = new UnicodeEncoding(true, false, true); preamble = 2; }
        else if (before.AsSpan().StartsWith(new byte[] { 0xEF, 0xBB, 0xBF })) { encoding = StrictUtf8; preamble = 3; }
        else
        {
            encoding = StrictUtf8;
            try { _ = encoding.GetString(before); }
            catch (DecoderFallbackException) { encoding = Encoding.GetEncoding(936, EncoderFallback.ExceptionFallback, DecoderFallback.ExceptionFallback); }
        }
        var text = encoding.GetString(before, preamble, before.Length - preamble);
        if (!encoding.GetBytes(text).AsSpan().SequenceEqual(before.AsSpan(preamble)))
            throw new InvalidDataException("存档索引编码不能无损往返，保留原文件。");
        var saveSection = false;
        var userSection = false;
        var hasSaveSection = false;
        var userNoteOnly = true;
        var hasUserNote = false;
        int? hashIndex = null;
        foreach (Match line in Regex.Matches(text, @"[^\r\n]+"))
        {
            var trimmed = line.Value.Trim();
            if (trimmed.Length == 0 || trimmed.StartsWith(';') || trimmed.StartsWith('#')) continue;
            if (trimmed.StartsWith('['))
            {
                var end = trimmed.IndexOf(']');
                saveSection = end > 0 && trimmed[1..end].Trim().Equals("Save", StringComparison.OrdinalIgnoreCase);
                userSection = end > 0 && trimmed[1..end].Trim().Equals("User", StringComparison.OrdinalIgnoreCase);
                hasSaveSection |= saveSection;
                if (!userSection) userNoteOnly = false;
                continue;
            }
            if (userSection && Regex.IsMatch(trimmed, @"^Note\s*=", RegexOptions.IgnoreCase)) hasUserNote = true;
            else userNoteOnly = false;
            if (!saveSection) continue;
            var match = Regex.Match(line.Value, @"^\s*Hash\s*=\s*(?<hash>[^;\s]*)(?:\s*(?:;.*)?)$", RegexOptions.IgnoreCase);
            if (!match.Success) continue;
            if (hashIndex is not null) throw new InvalidDataException("存档索引含多个 [Save] Hash，无法唯一同步。");
            var value = match.Groups["hash"];
            if (!value.Value.Equals(beforeSaveHash, StringComparison.OrdinalIgnoreCase))
                throw new InvalidDataException("存档索引 [Save] Hash 与当前存档不匹配。");
            // Keep the absolute string index while preserving every surrounding character.
            hashIndex = line.Index + value.Index;
        }
        if (hashIndex is null)
        {
            // Ordinary save comments are legitimately created with only [User] Note.
            if (!requireHash && !hasSaveSection && userNoteOnly && hasUserNote) return (byte[])before.Clone();
            throw new InvalidDataException("已有存档索引缺少唯一有效的 [Save] Hash。");
        }
        var updated = text[..hashIndex.Value] + afterSaveHash + text[(hashIndex.Value + 64)..];
        var body = encoding.GetBytes(updated);
        var result = new byte[preamble + body.Length];
        before.AsSpan(0, preamble).CopyTo(result); body.CopyTo(result, preamble);
        return result;
    }

    private static uint U32(ReadOnlySpan<byte> bytes, int offset) => BinaryPrimitives.ReadUInt32LittleEndian(bytes[offset..]);
    private static ulong U64(ReadOnlySpan<byte> bytes, int offset) => BinaryPrimitives.ReadUInt64LittleEndian(bytes[offset..]);
    private static int I32(ReadOnlySpan<byte> bytes, int offset) => BinaryPrimitives.ReadInt32LittleEndian(bytes[offset..]);
}
