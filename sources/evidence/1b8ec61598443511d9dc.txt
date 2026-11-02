using System.Buffers.Binary;
using System.Text;

namespace DataManager.Core.Profiles;

/// <summary>Proves the native E5S snapshot through both the engine's writer and loader.</summary>
public static class SaveAppearanceLayoutProbe
{
    public sealed record Layout(bool Verified, int ROffset, int SOffset, int PrefixLength,
        int RExecutableOffset, int SExecutableOffset, string Evidence);

    public static Layout Inspect(byte[] executable, string profileId)
    {
        if (profileId is not ("ccz-6.4" or "ccz-6.5" or "ccz-6.6"))
            return Reject("当前引擎版本没有已验证的原生 E5S 形象同步契约。");
        if (!Pe.TryRead(executable, out var pe)) return Reject("原生存档缺少无重叠的完整 PE32 映射。");
        // The strict probe proves pointer-to-person-ID / 72 and the complete ID<1024 S consumer.
        var assignments = EmbeddedEngineLayoutProbe.InspectAssignments65(executable);
        if (!assignments.R.Verified || !assignments.S.Verified)
            return Reject("人物 ID、R/S UInt16 消费者或 1024 人物边界未通过：" +
                assignments.R.Evidence + "；" + assignments.S.Evidence);
        if (!pe.TryVa(checked((int)assignments.R.Offset), out var rVa) ||
            !pe.TryVa(checked((int)assignments.S.Offset), out var sVa))
            return Reject("人物 R/S 表不能唯一映射到引擎内存。");

        // Four consecutive WriteFile operations: the memory snapshot, persons, script state, and scene.
        var writers = pe.FindCode(Writer);
        var readers = pe.FindCode(Reader);
        if (writers.Count != 1 || readers.Count != 1)
            return Reject("没有唯一的原生四段存档写入链和 seek(0) 快照读取链。");
        var writer = writers[0]; var reader = readers[0];
        var length = ReadU32(executable, writer + 1);
        var snapshot = ReadU32(executable, writer + 6);
        if (length != 0x30000 || ReadU32(executable, reader + 1) != length ||
            ReadU32(executable, reader + 6) != snapshot || !pe.Map(snapshot, (int)length, false, true, out _))
            return Reject("原生写入/读取快照的地址、长度或可写 PE 完整边界不一致。");
        var writeTarget = pe.Call(writer + 13);
        if (writeTarget is null || new[] { 37, 61, 84 }.Any(delta => pe.Call(writer + delta) != writeTarget) ||
            !pe.Code(writeTarget.Value, WriteFileWrapper, out var writeWrapper) ||
            !pe.Import(ReadU32(executable, writeWrapper + 25), "WriteFile"))
            return Reject("四段写入没有调用同一个完整 WriteFile 包装函数。");
        var readTarget = pe.Call(reader + 15);
        if (readTarget is null || !pe.Code(readTarget.Value, SeekReadWrapper, out var seekRead) ||
            pe.Call(seekRead + 12) is not { } seekTarget ||
            !pe.Code(seekTarget, SeekWrapper, out var seek) ||
            !pe.Import(ReadU32(executable, seek + 37), "SetFilePointer") ||
            pe.Call(seekRead + 26) is not { } readFileTarget ||
            !pe.Code(readFileTarget, ReadFileWrapper, out var readFile) ||
            !pe.Import(ReadU32(executable, readFile + 36), "ReadFile"))
            return Reject("读取包装未证明绝对 seek(0)、完整 ReadFile 调用及导入目标。");
        if (!VerifyVersion(pe, executable, writer, reader, readTarget.Value, length))
            return Reject("原生人物段版本 5 的生成与读档检查未通过完整调用链验证。");
        if (!VerifyRecordSegments(pe, writer, reader, readFileTarget))
            return Reject("原生人物/脚本段尺寸或场景头/250 个战场记录的序列化契约未通过。");
        var r = (long)rVa - snapshot; var s = (long)sVa - snapshot;
        if (r < 0 || s < 0 || r + 2048 > length || s + 2048 > length ||
            r < s + 2048 && s < r + 2048)
            return Reject("人物 R/S 表不在被保存和恢复的快照内，或 1024×UInt16 表相互重叠。");
        return new(true, (int)r, (int)s, (int)length, (int)assignments.R.Offset, (int)assignments.S.Offset,
            $"独立 PE 消费者证据：人物指针/72、S 人物 ID<1024、R/S UInt16 和 0/33 分支；" +
            $"原生四段 WriteFile 与 seek(0)/ReadFile 同指向 VA 0x{snapshot:X8}、长 0x{length:X}；" +
            $"人物段版本 5 生成/检查已核对。E5S R=+0x{r:X}、S=+0x{s:X}，各 1024×UInt16；" +
            $"EXE R=+0x{assignments.R.Offset:X}、S=+0x{assignments.S.Offset:X}。");
    }

    private static bool VerifyVersion(Pe pe, byte[] bytes, int writer, int reader, uint readTarget, uint length)
    {
        if (pe.Call(writer + 27) is not { } builder || !pe.Code(builder,
            Pattern("55 8B EC 51 68 ?? ?? ?? ?? 6A 00 6A 00 C6 01 05 E8 ?? ?? ?? ??"), out _)) return false;
        // The old compiler loads/compares AL; 6.6 compares the pointed byte directly.
        foreach (var (distance, marker) in new[] { (57, LegacyMarker), (55, ModernMarker) })
        {
            var start = reader - distance;
            if (start < 0 || !pe.At(start, marker) || ReadU32(bytes, start + 6) != length ||
                pe.Call(start + 13) != readTarget) continue;
            return true;
        }
        return false;
    }

    private static bool VerifyRecordSegments(Pe pe, int writer, int reader, uint readFileTarget)
    {
        // The rest of the native loader must consume the proved D4F0 and 313D segments.
        var records = reader + 20;
        if (!pe.At(records, RecordReader)) records += 3; // legacy add [ebp-4],eax
        if (!pe.At(records, RecordReader) || pe.Call(records + 18) != readFileTarget ||
            pe.Call(records + 57) != readFileTarget || pe.Call(writer + 74) is not { } sceneTarget) return false;
        // Both compiler forms create a 0x23 header; only battle mode adds the
        // 0x4F2 scene state, 250 x 0x2A unit rows and the final 0x640 block.
        var modern = false;
        if (!pe.Code(sceneTarget, LegacySceneWriter, out var scene))
        {
            if (!pe.Code(sceneTarget, ModernSceneWriter, out scene)) return false;
            modern = true;
        }
        if (pe.Call(scene + 83) is not { } battle || !pe.Code(battle,
            Pattern("55 8B EC E8 ?? ?? ?? ?? 33 C9 3C 03 0F 94 C1 8B C1 5D C3"), out _) ||
            pe.Call(scene + 98) is not { } sceneHeader || !pe.Code(sceneHeader, SceneHeaderWriter, out _) ||
            pe.Call(scene + (modern ? 122 : 127)) is not { } unit || !pe.Code(unit, UnitWriter, out _)) return false;
        return true;
    }

    private static Layout Reject(string reason) => new(false, 0, 0, 0, 0, 0, reason);
    private static uint ReadU32(byte[] bytes, int offset) => BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(offset, 4));
    private static byte?[] Pattern(string text) => text.Split(' ').Select(part => part == "??" ? (byte?)null : Convert.ToByte(part, 16)).ToArray();
    private static bool Matches(ReadOnlySpan<byte> data, byte?[] pattern)
    {
        if (data.Length < pattern.Length) return false;
        for (var i = 0; i < pattern.Length; i++) if (pattern[i] is { } value && data[i] != value) return false;
        return true;
    }

    private static readonly byte?[] Writer = Pattern("68 ?? ?? ?? ?? 68 ?? ?? ?? ?? 8D 4D F8 E8 ?? ?? ?? ?? 01 45 FC 8B 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 50 51 8D 4D F8 E8 ?? ?? ?? ?? 01 45 FC 8B 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 50 51 8D 4D F8 E8 ?? ?? ?? ?? 01 45 FC B9 ?? ?? ?? ?? E8 ?? ?? ?? ?? 50 51 8D 4D F8 E8 ?? ?? ?? ?? 01 45 FC 8D 4D F8 E8 ?? ?? ?? ?? 8B E5 5D C2 04 00");
    private static readonly byte?[] Reader = Pattern("68 ?? ?? ?? ?? 68 ?? ?? ?? ?? 6A 00 8D 4D F8 E8 ?? ?? ?? ??");
    private static readonly byte?[] WriteFileWrapper = Pattern("55 8B EC 51 8B 01 85 C0 74 1A 6A 00 8D 4D FC 51 FF 75 0C FF 75 08 50 FF 15 ?? ?? ?? ?? 85 C0 74 03 8B 45 FC 8B E5 5D C2 08 00");
    private static readonly byte?[] SeekReadWrapper = Pattern("55 8B EC 51 6A 00 FF 75 08 8B 4D FC E8 ?? ?? ?? ?? FF 75 10 FF 75 0C 8B 4D FC E8 ?? ?? ?? ?? 8B E5 5D C2 0C 00");
    private static readonly byte?[] SeekWrapper = Pattern("55 8B EC 6A 00 51 8B 45 0C 83 F8 03 73 03 89 45 FC 8B 4D F8 8B 01 85 C0 74 0F FF 75 FC 6A 00 FF 75 08 50 FF 15 ?? ?? ?? ?? 8B E5 5D C2 08 00");
    private static readonly byte?[] ReadFileWrapper = Pattern("55 8B EC 51 51 6A 00 83 39 00 74 26 EB 03 FF 45 F4 6A 00 8D 55 FC 52 FF 75 0C FF 75 08 8B 55 F8 FF 32 FF 15 ?? ?? ?? ?? 85 C0 75 0A 83 7D F4 05 7E DC 33 C0 EB 03 8B 45 FC 8B E5 5D C2 08 00");
    private static readonly byte?[] LegacyMarker = Pattern("6A 01 FF 75 F4 68 ?? ?? ?? ?? 8D 4D F8 E8 ?? ?? ?? ?? 8B 45 F4 0F B6 00 3C 05 74 0F 8D 4D F8 E8 ?? ?? ?? ?? 33 C0 E9 ?? ?? ?? ?? 6A 00 E8 ?? ?? ?? ?? C6 05 ?? ?? ?? ?? 01");
    private static readonly byte?[] ModernMarker = Pattern("6A 01 FF 75 F4 68 ?? ?? ?? ?? 8D 4D F8 E8 ?? ?? ?? ?? 8B 45 F4 80 38 05 74 0F 8D 4D F8 E8 ?? ?? ?? ?? 33 C0 E9 ?? ?? ?? ?? 6A 00 E8 ?? ?? ?? ?? C6 05 ?? ?? ?? ?? 01");
    private static readonly byte?[] RecordReader = Pattern("6A 01 E8 ?? ?? ?? ?? 68 F0 D4 00 00 FF 75 F4 8D 4D F8 E8 ?? ?? ?? ?? E8 ?? ?? ?? ?? 8B 4D F4 E8 ?? ?? ?? ?? 6A 0E E8 ?? ?? ?? ?? 83 C4 04 68 3D 31 00 00 FF 75 F4 8D 4D F8 E8 ?? ?? ?? ?? 8B 4D F4 E8 ?? ?? ?? ??");
    private const string ScenePrefix = "55 8B EC 6A 00 51 6A 0E E8 ?? ?? ?? ?? 83 C4 04 E8 ?? ?? ?? ?? 50 C6 00 05 8B 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 8B 4D F4 88 41 01 8B 55 F8 8A 42 02 FE C0 88 41 02 83 C1 05 51 B8 ?? ?? ?? ?? 05 10 3D 00 00 50 FF 75 F0 E8 ?? ?? ?? ?? 83 C4 08 83 45 F0 1E E8 ?? ?? ?? ?? 85 C0 ";
    private static readonly byte?[] LegacySceneWriter = Pattern(ScenePrefix + "74 4D FF 75 F0 8B 4D F8 E8 ?? ?? ?? ?? 89 45 F0 EB 03 FF 45 FC 8B 4D FC 80 F9 FA 73 12 E8 ?? ?? ?? ?? FF 75 F0 E8 ?? ?? ?? ?? 89 45 F0 EB E3 C7 45 FC 40 06 00 00 B8 80 0C 00 00 E8 ?? ?? ?? ?? FF 75 FC FF 75 F0 50 E8 ?? ?? ?? ?? 83 C4 0C 8B 4D FC 01 4D F0 8B 45 F0 8B 4D F4 2B C1 8B E5 5D C3");
    private static readonly byte?[] ModernSceneWriter = Pattern(ScenePrefix + "74 4B FF 75 F0 8B 4D F8 E8 ?? ?? ?? ?? 89 45 F0 8B 4D FC 80 F9 FA 73 15 E8 ?? ?? ?? ?? FF 75 F0 E8 ?? ?? ?? ?? 89 45 F0 FF 45 FC EB E3 C7 45 FC 40 06 00 00 B8 80 0C 00 00 E8 ?? ?? ?? ?? FF 75 FC FF 75 F0 50 E8 ?? ?? ?? ?? 83 C4 0C 8B 45 F0 03 45 FC 8B 4D F4 2B C1 8B E5 5D C3");
    private static readonly byte?[] SceneHeaderWriter = Pattern("55 8B EC 6A 00 51 8B 45 08 8B 11 89 10 83 C0 04 8A 51 08 88 10 40 8B 51 0C 89 10 83 C0 04 8A 51 11 88 10 40 8B 51 04 66 89 10 83 C0 02 8A 91 00 05 00 00 88 10 40 8A 91 04 05 00 00 88 10 40 8B 91 FC 04 00 00 66 89 10 83 C0 02 EB 03 FF 45 FC 8B 55 FC 81 FA FA 00 00 00 73 1B 6B D2 05 8B 4D F8 8B 4C 11 19 89 08 83 C0 04 8B 4D F8 8A 4C 11 1D 88 08 40 EB D7 8B E5 5D C2 04 00");
    private static readonly byte?[] UnitWriter = Pattern("55 8B EC 51 8B 45 08 8B 11 89 10 8B 51 10 89 50 02 8B 51 14 89 50 04 83 C1 04 83 C0 06 6A 0C 51 50 E8 ?? ?? ?? ?? 83 C4 0C 59 83 C1 18 8B 45 08 83 C0 12 6A 18 51 50 E8 ?? ?? ?? ?? 83 C4 0C 8B 45 08 83 C0 2A 5D C2 04 00");

    private sealed record Section(uint Rva, uint Raw, uint Size, uint VirtualSize, uint Flags);
    private sealed class Pe(byte[] bytes, uint imageBase, List<Section> sections, uint importsRva, uint importsSize)
    {
        public bool TryVa(int offset, out uint va)
        {
            va = 0;
            var matches = sections.Where(s => offset >= s.Raw && offset < s.Raw + (long)s.Size).ToArray();
            if (matches.Length != 1) return false;
            var value = imageBase + (long)matches[0].Rva + offset - matches[0].Raw;
            if (value > uint.MaxValue) return false;
            va = (uint)value; return true;
        }
        public bool Map(uint va, int length, bool code, bool writable, out int offset)
        {
            offset = 0;
            if (va < imageBase || length < 0) return false;
            var rva = (long)va - imageBase;
            var matches = sections.Where(s => rva >= s.Rva && rva + length <= s.Rva + (long)s.Size &&
                (!code || (s.Flags & 0x20000000) != 0) && (!writable || (s.Flags & 0x80000000) != 0)).ToArray();
            if (matches.Length != 1) return false;
            var mapped = matches[0].Raw + rva - matches[0].Rva;
            if (mapped < 0 || mapped > bytes.Length - (long)length) return false;
            offset = (int)mapped; return true;
        }
        public uint? Call(int offset)
        {
            if (offset < 0 || offset > bytes.Length - 5 || bytes[offset] != 0xE8 || !TryVa(offset, out var va)) return null;
            var target = (long)va + 5 + BinaryPrimitives.ReadInt32LittleEndian(bytes.AsSpan(offset + 1, 4));
            return target is >= 0 and <= uint.MaxValue ? (uint)target : null;
        }
        public bool Code(uint va, byte?[] pattern, out int offset) => Map(va, pattern.Length, true, false, out offset) && At(offset, pattern);
        public bool At(int offset, byte?[] pattern) => offset >= 0 && offset <= bytes.Length - pattern.Length &&
            TryVa(offset, out var va) && Map(va, pattern.Length, true, false, out var mapped) && mapped == offset && Matches(bytes.AsSpan(offset), pattern);
        public List<int> FindCode(byte?[] pattern)
        {
            var hits = new List<int>();
            foreach (var section in sections.Where(s => (s.Flags & 0x20000000) != 0))
                for (var i = (int)section.Raw; i <= section.Raw + (long)section.Size - pattern.Length; i++)
                    if (Matches(bytes.AsSpan(i), pattern)) hits.Add(i);
            return hits;
        }
        public bool Import(uint iatVa, string name)
        {
            if (importsSize < 20 || importsSize > 0x100000 || importsRva > uint.MaxValue - imageBase ||
                !Map(imageBase + importsRva, (int)importsSize, false, false, out var directory)) return false;
            for (var pos = directory; pos <= directory + (long)importsSize - 20; pos += 20)
            {
                var thunk = ReadU32(bytes, pos); var first = ReadU32(bytes, pos + 16);
                if (thunk == 0 && first == 0) return false;
                if (first > uint.MaxValue - imageBase || iatVa < imageBase + first || ((iatVa - imageBase - first) & 3) != 0) continue;
                var index = (iatVa - imageBase - first) / 4;
                if (index > 0x10000) continue;
                var lookup = (long)(thunk == 0 ? first : thunk) + index * 4;
                if (lookup > uint.MaxValue - imageBase || !Map(imageBase + (uint)lookup, 4, false, false, out var entry)) continue;
                var symbol = ReadU32(bytes, entry);
                if ((symbol & 0x80000000) != 0 || symbol > uint.MaxValue - imageBase - 2 ||
                    !Map(imageBase + symbol + 2, name.Length + 1, false, false, out var text)) continue;
                if (bytes[text + name.Length] == 0 && bytes.AsSpan(text, name.Length).SequenceEqual(Encoding.ASCII.GetBytes(name))) return true;
            }
            return false;
        }
        public static bool TryRead(byte[] bytes, out Pe image)
        {
            image = null!;
            try
            {
                if (bytes.Length < 64 || bytes[0] != 'M' || bytes[1] != 'Z') return false;
                var header = BinaryPrimitives.ReadInt32LittleEndian(bytes.AsSpan(0x3C, 4));
                if (header < 0 || header > bytes.Length - 24 || ReadU32(bytes, header) != 0x4550 ||
                    BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(header + 4, 2)) != 0x14C) return false;
                var count = BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(header + 6, 2));
                var optionalSize = BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(header + 20, 2));
                var optional = header + 24;
                if (count is 0 or > 96 || optionalSize < 112 || optional > bytes.Length - optionalSize ||
                    BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(optional, 2)) != 0x10B || ReadU32(bytes, optional + 92) < 2) return false;
                var sectionHeader = optional + optionalSize;
                if (sectionHeader > bytes.Length - count * 40) return false;
                var sections = new List<Section>();
                for (var i = 0; i < count; i++)
                {
                    var pos = sectionHeader + i * 40;
                    var size = ReadU32(bytes, pos + 16); var raw = ReadU32(bytes, pos + 20);
                    var rva = ReadU32(bytes, pos + 12); var virtualSize = ReadU32(bytes, pos + 8);
                    if (raw > bytes.Length || size > bytes.Length - raw || rva + (long)Math.Max(size, virtualSize) > uint.MaxValue) return false;
                    sections.Add(new(rva, raw, size, virtualSize, ReadU32(bytes, pos + 36)));
                }
                for (var a = 0; a < sections.Count; a++)
                    for (var b = a + 1; b < sections.Count; b++)
                    {
                        var x = sections[a]; var y = sections[b];
                        if (x.Size > 0 && y.Size > 0 && x.Raw < y.Raw + (long)y.Size && y.Raw < x.Raw + (long)x.Size ||
                            Math.Max(x.Size, x.VirtualSize) > 0 && Math.Max(y.Size, y.VirtualSize) > 0 &&
                            x.Rva < y.Rva + (long)Math.Max(y.Size, y.VirtualSize) && y.Rva < x.Rva + (long)Math.Max(x.Size, x.VirtualSize)) return false;
                    }
                image = new(bytes, ReadU32(bytes, optional + 28), sections, ReadU32(bytes, optional + 104), ReadU32(bytes, optional + 108));
                return true;
            }
            catch (Exception ex) when (ex is ArgumentException or OverflowException) { return false; }
        }
    }
}
