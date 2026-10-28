using System.Buffers.Binary;

namespace DataManager.Core.Profiles;

/// <summary>
/// Locates embedded tables through their actual x86 consumers. This does not use
/// a 6.5 file offset or the old assigner's INI as evidence for a 6.6 executable.
/// The checked instruction forms and sample hashes are recorded in 验证/本轮逆向.
/// </summary>
public static class EmbeddedEngineLayoutProbe
{
    public sealed record Layout(bool Verified, long Offset, string Evidence);
    public sealed record Assignments(Layout R, Layout S);

    public static Assignments InspectAssignments(byte[] executable)
        => InspectAssignments(executable, requireLegacyIdProof: false);

    /// <summary>
    /// A modified 6.5 executable is accepted only when the complete consumers
    /// also prove runtime person-pointer / 72 and the S person-ID 0..1023 gate.
    /// </summary>
    public static Assignments InspectAssignments65(byte[] executable)
        => InspectAssignments(executable, requireLegacyIdProof: true);

    private static Assignments InspectAssignments(byte[] executable, bool requireLegacyIdProof)
    {
        if (!PeImage.TryRead(executable, out var image))
            return new(Unavailable("R/S 缺少有效 PE32 节映射。"), Unavailable("R/S 缺少有效 PE32 节映射。"));

        // push ebp; mov ebp,esp; push ecx; call PersonId;
        // movzx eax,word ptr[eax*2+R]; pop ecx; pop ebp; ret.
        var rPattern = Pattern("55 8B EC 51 E8 ?? ?? ?? ?? 0F B7 04 45 ?? ?? ?? ?? 59 5D C3");
        var rHits = image.FindCode(rPattern);
        var r = Unavailable("未找到唯一的人物 R 形象 UInt16 消费者。禁止读取继承偏移。");
        if (rHits.Count == 1)
        {
            var hit = rHits[0];
            var va = BinaryPrimitives.ReadUInt32LittleEndian(executable.AsSpan(hit + 13, 4));
            var callTarget = (long)image.ToVa(hit + 9) + BinaryPrimitives.ReadInt32LittleEndian(executable.AsSpan(hit + 5, 4));
            var idProof = !requireLegacyIdProof || VerifyLegacyPersonId(executable, image, callTarget);
            if (callTarget >= 0 && callTarget <= uint.MaxValue && image.TryMap((uint)callTarget, 1, true, false, out _) && idProof &&
                image.TryMap(va, 1024 * 2, false, true, out var offset))
                r = new(true, offset, $"PE 人物 ID 换算消费者（调用 0x{callTarget:X8}，{(requireLegacyIdProof ? "运行时人物指针减去可写基址指针后有符号除以 72 的完整函数已验签" : "运行时记录步长由调用方复核")}）及 VA 0x{image.ToVa(hit + 9):X8} 的 movzx word[eax*2+0x{va:X8}] 已验签；VA 映射到文件 +0x{offset:X}，1024×UInt16 边界已核对。");
            else r = Unavailable("人物 R 消费者的 ID 换算、可写节映射或 1024×UInt16 边界未通过，禁止读取继承偏移。");
        }

        // The actual S consumer doubles the person ID, reads one word, and
        // distinguishes 0 (default), 1..32 (three-stage), and >=33 (single).
        var sPattern = Pattern("8B 55 08 D1 E2 0F B7 82 ?? ?? ?? ?? 85 C0 74 18 83 F8 21 73 0C 48 6B C0 03 83 C0 50 03 45 FC EB 0C 05 8F 00 00 00");
        var sHits = image.FindCode(sPattern);
        var s = Unavailable("未找到唯一的人物 S 形象 UInt16/0/33 分支消费者。禁止读取继承偏移。");
        if (sHits.Count == 1)
        {
            var hit = sHits[0];
            var va = BinaryPrimitives.ReadUInt32LittleEndian(executable.AsSpan(hit + 8, 4));
            var boundedConsumer = !requireLegacyIdProof || VerifyLegacySBounds(executable, hit);
            if (boundedConsumer && image.TryMap(va, 1024 * 2, false, true, out var offset))
                s = new(true, offset, $"PE VA 0x{image.ToVa(hit + 3):X8} 的人物 ID×2、UInt16 读取和 0/33 形象分支已验签{(requireLegacyIdProof ? "；完整函数的人物 ID<1024 前置边界、三转余数和 0xFFFF 返回值已核对" : string.Empty)}；VA 0x{va:X8} 映射到文件 +0x{offset:X}，1024×UInt16 边界已核对。");
            else s = Unavailable("人物 S 消费者的可写节映射或 1024×UInt16 边界未通过，禁止读取继承偏移。");
        }
        if (r.Verified && s.Verified && r.Offset < s.Offset + 2048 && s.Offset < r.Offset + 2048)
            return new(Unavailable("PE R/S 消费者指向的 1024×UInt16 区域互相重叠，布局不可用。"), Unavailable("PE R/S 消费者指向的 1024×UInt16 区域互相重叠，布局不可用。"));
        return new(r, s);
    }

    private static bool VerifyLegacyPersonId(byte[] executable, PeImage image, long target)
    {
        var pattern = Pattern("55 8B EC 8B 45 08 2B 05 ?? ?? ?? ?? 99 33 C9 B1 48 F7 F9 5D C3");
        if (target < 0 || target > uint.MaxValue || !image.TryMap((uint)target, pattern.Length, true, false, out var offset) ||
            !Matches(executable.AsSpan(offset, pattern.Length), pattern)) return false;
        var runtimeBasePointer = BinaryPrimitives.ReadUInt32LittleEndian(executable.AsSpan(offset + 8, 4));
        return image.TryMap(runtimeBasePointer, 4, false, true, out _);
    }

    private static bool VerifyLegacySBounds(byte[] executable, int consumer)
    {
        var prefix = Pattern("55 8B EC 83 EC 08 81 7D 08 00 04 00 00 72 04 33 C9 EB 4D FF 75 08 E8 ?? ?? ?? ?? 89 4D F8 E8 ?? ?? ?? ?? 99 33 C9 B1 03 F7 F9 89 55 FC 8B 4D F8 E8 ?? ?? ?? ?? 89 45 F8");
        var suffix = Pattern("EB 05 B8 FF FF 00 00 8B E5 5D C2 04 00");
        const int consumerLength = 38;
        return consumer >= prefix.Length && consumer + consumerLength <= executable.Length - suffix.Length &&
            Matches(executable.AsSpan(consumer - prefix.Length, prefix.Length), prefix) &&
            Matches(executable.AsSpan(consumer + consumerLength, suffix.Length), suffix);
    }

    public static Layout InspectStrategyTerrain(byte[] executable)
    {
        if (!PeImage.TryRead(executable, out var image)) return Unavailable("策略地形缺少有效 PE32 节映射。");
        // unsigned terrain byte -> table[terrain] -> AND caller's element mask.
        var pattern = Pattern("55 8B EC 0F B6 45 08 8A 80 ?? ?? ?? ?? 23 45 0C 5D C2 08 00");
        var hits = image.FindCode(pattern);
        if (hits.Count != 1) return Unavailable("未找到唯一的策略地形读取/AND 掩码消费者；未提供布局证据，禁止读取继承偏移。");
        var hit = hits[0];
        var va = BinaryPrimitives.ReadUInt32LittleEndian(executable.AsSpan(hit + 9, 4));
        if (!image.TryMap(va, 30, false, false, out var offset))
            return Unavailable("策略地形消费者的 30 字节表 VA 无完整文件映射。");
        if (executable.AsSpan(offset, 30).IndexOfAnyInRange((byte)16, byte.MaxValue) >= 0)
            return Unavailable("策略地形 30 项中出现低四位以外数据；需重新确认该消费者对应的布局。");
        var consumerVa = image.ToVa(hit);
        var calls = image.FindRelativeCalls(consumerVa);
        // Require a real elemental caller: it bounds strategy category by 3,
        // constructs 1 << category, then passes terrain and mask to this function.
        var maskCaller = calls.Any(call =>
        {
            var start = Math.Max(0, call - 48);
            var prefix = executable.AsSpan(start, call - start);
            return Contains(prefix, Pattern("3C 03 77 ??")) && Contains(prefix, Pattern("B0 01 D3 E0")) &&
                prefix.EndsWith(new byte[] { 0xFF, 0x75, 0xE0, 0x50 });
        });
        if (calls.Count < 2 || !maskCaller)
            return Unavailable("策略地形读取函数缺少独立调用者或策略类型 0..3 到 1<<类型的掩码证据。");
        return new(true, offset, $"独立 PE 静态证据：VA 0x{consumerVa:X8} 的完整 UInt8 地形读取/AND 函数已验签，{calls.Count} 个相对调用中含策略类型 0..3→1<<类型；目标 VA 0x{va:X8} 映射文件 +0x{offset:X}，30×UInt8 低四位掩码已核对（非继承 6.5 地址）。");
    }

    private static Layout Unavailable(string evidence) => new(false, 0, evidence);
    private static byte?[] Pattern(string text) => text.Split(' ').Select(part => part == "??" ? (byte?)null : Convert.ToByte(part, 16)).ToArray();
    private static bool Matches(ReadOnlySpan<byte> data, byte?[] pattern)
    {
        if (data.Length < pattern.Length) return false;
        for (var index = 0; index < pattern.Length; index++)
            if (pattern[index] is { } expected && data[index] != expected) return false;
        return true;
    }
    private static bool Contains(ReadOnlySpan<byte> data, byte?[] pattern)
    {
        for (var index = 0; index <= data.Length - pattern.Length; index++)
            if (Matches(data[index..], pattern)) return true;
        return false;
    }

    internal sealed class PeImage(byte[] bytes, uint imageBase, List<Section> sections)
    {
        private const uint Executable = 0x20000000;
        private const uint Writable = 0x80000000;
        public uint ToVa(int offset)
        {
            var section = sections.Single(item => offset >= item.Raw && offset < item.Raw + (long)item.Size);
            return checked(imageBase + section.Rva + (uint)(offset - section.Raw));
        }

        public bool TryMap(uint va, int length, bool code, bool writable, out int offset)
        {
            offset = 0;
            if (va < imageBase || length < 0) return false;
            var rva = (long)va - imageBase;
            var matches = sections.Where(section => rva >= section.Rva && rva + length <= section.Rva + (long)section.Size &&
                (!code || (section.Flags & Executable) != 0) && (!writable || (section.Flags & Writable) != 0)).ToArray();
            if (matches.Length != 1) return false;
            var section = matches[0];
            var result = section.Raw + rva - section.Rva;
            if (result < 0 || result > bytes.LongLength - length) return false;
            offset = (int)result;
            return true;
        }

        public List<int> FindCode(byte?[] pattern)
        {
            var hits = new List<int>();
            foreach (var section in sections.Where(item => (item.Flags & Executable) != 0))
                for (var cursor = (int)section.Raw; cursor <= section.Raw + (long)section.Size - pattern.Length; cursor++)
                    if (Matches(bytes.AsSpan(cursor, pattern.Length), pattern)) hits.Add(cursor);
            return hits;
        }

        public List<int> FindRelativeCalls(uint targetVa)
        {
            var hits = new List<int>();
            foreach (var section in sections.Where(item => (item.Flags & Executable) != 0))
                for (var cursor = (int)section.Raw; cursor <= section.Raw + (long)section.Size - 5; cursor++)
                    if (bytes[cursor] == 0xE8 && (long)ToVa(cursor) + 5 + BinaryPrimitives.ReadInt32LittleEndian(bytes.AsSpan(cursor + 1, 4)) == targetVa)
                        hits.Add(cursor);
            return hits;
        }

        public static bool TryRead(byte[] bytes, out PeImage image)
        {
            image = null!;
            try
            {
                if (bytes.Length < 0x40 || bytes[0] != 'M' || bytes[1] != 'Z') return false;
                var pe = BinaryPrimitives.ReadInt32LittleEndian(bytes.AsSpan(0x3C, 4));
                if (pe < 0 || pe > bytes.Length - 24 || BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(pe, 4)) != 0x4550) return false;
                var count = BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(pe + 6, 2));
                var optionalSize = BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(pe + 20, 2));
                var optional = pe + 24;
                if (optionalSize < 32 || optional > bytes.Length - optionalSize || BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(optional, 2)) != 0x10B) return false;
                var imageBase = BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(optional + 28, 4));
                var sections = new List<Section>();
                for (var index = 0; index < count; index++)
                {
                    var position = optional + optionalSize + index * 40;
                    if (position > bytes.Length - 40) return false;
                    var size = BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(position + 16, 4));
                    var raw = BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(position + 20, 4));
                    if (raw > bytes.Length || size > bytes.Length - raw) return false;
                    sections.Add(new(BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(position + 12, 4)), size, raw,
                        BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(position + 36, 4))));
                }
                // Ambiguous raw/RVA aliases cannot establish a unique mapping.
                if (sections.Any(a => sections.Any(b => a != b && a.Size > 0 && b.Size > 0 &&
                    (a.Raw < b.Raw + (long)b.Size && b.Raw < a.Raw + (long)a.Size ||
                     a.Rva < b.Rva + (long)b.Size && b.Rva < a.Rva + (long)a.Size)))) return false;
                image = new(bytes, imageBase, sections);
                return true;
            }
            catch (Exception ex) when (ex is ArgumentException or OverflowException) { return false; }
        }
    }
    internal sealed record Section(uint Rva, uint Size, uint Raw, uint Flags);
}
