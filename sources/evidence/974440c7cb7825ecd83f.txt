using System.Buffers.Binary;
using System.Security.Cryptography;
using DataManager.Core.Models;
using DataManager.Core.Scanner;

namespace DataManager.Tests;

/// <summary>Uses real EXE bytes read-only; every damaged or relocated fixture lives only in memory.</summary>
internal static class EffectAssignmentLayoutTests
{
    public static void Run(string repositoryRoot)
    {
        var samples = new[]
        {
            (Name: "洗隋", Rows: 180, Width: 8, Slots: 1, Address: 0x508998u, Offset: 0xDA198L),
            (Name: "加强版6.5未加密版", Rows: 255, Width: 8, Slots: 1, Address: 0x507800u, Offset: 0xD9000L),
            (Name: "复刻版6.6山贼", Rows: 255, Width: 16, Slots: 2, Address: 0x511000u, Offset: 0xE2800L),
            (Name: "复刻版6.6山贼 国庆", Rows: 255, Width: 16, Slots: 2, Address: 0x511000u, Offset: 0xE2800L)
        };
        foreach (var sample in samples)
        {
            var path = Path.Combine(repositoryRoot, "基底", sample.Name, "Ekd5.exe");
            var bytes = File.ReadAllBytes(path);
            var hash = SHA256.HashData(bytes);
            var layout = EngineEffectAssignmentService.ProbeJobLayout(bytes);
            Assert(layout.Verified, sample.Name + "：" + layout.Evidence);
            Assert(layout.RowCount == sample.Rows && layout.RowSize == sample.Width && layout.SlotCount == sample.Slots &&
                layout.TableAddress == sample.Address && layout.TableOffset == sample.Offset && layout.PointerAddress == 0x500C3B,
                sample.Name + " 的当前布局与静态基线不符。");
            Assert(layout.SharedValue == (sample.Width == 8) && layout.PersonIdOffsets.Count == (sample.Width == 8 ? 3 : 4),
                "个人槽数或共享N判定错误。");
            Assert(layout.JobIdOffsets.SequenceEqual(sample.Width == 8 ? [6] : new[] { 12, 14 }) &&
                layout.JobValueOffsets.SequenceEqual(sample.Width == 8 ? [7] : new[] { 13, 15 }), "兵种ID/N字段错位。");
            for (var row = 0; row < layout.RowCount; row++)
            {
                Assert(layout.GetRowOffset(row) == sample.Offset + (long)row * sample.Width, "分配行地址错位。");
                var people = layout.ReadPersonIds(bytes, row);
                for (var slot = 0; slot < people.Count; slot++)
                {
                    var expected = BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(
                        checked((int)layout.GetPersonIdOffset(row, slot)), 2));
                    Assert(people[slot] == expected, "原始人物UInt16值未保留。");
                    if (layout.SharedValue)
                        Assert(layout.GetPersonValueOffset(row, slot) == layout.GetJobValueOffset(row, 0), "共享N地址被拆分。");
                }
            }
            ThrowsRange(() => layout.GetRowOffset(sample.Rows));
            ThrowsRange(() => layout.GetRowOffset(-1));
            ThrowsRange(() => layout.GetJobIdOffset(0, sample.Slots));
            RejectMutation(bytes, 0x41301E, "provider入口");
            RejectMutation(bytes, sample.Width == 8 ? 0x4198C4u : 0x4198C6u, "读取行宽");
            RejectMutation(bytes, sample.Width == 8 ? 0x40883Eu : 0x408829u, "写入上界");
            RejectMutation(bytes, sample.Width == 8 ? 0x40118Cu : 0x401193u, "初始化上界");
            RejectMutation(bytes, sample.Width == 8 ? 0x408846u : 0x408831u, "写入指针不一致");
            RejectMutation(bytes, sample.Width == 16 ? 0x42F9D8u : sample.Rows == 180 ? 0x422DEEu : 0x422DE8u, "匹配器清栈");
            RejectMutation(bytes, sample.Width == 8 ? 0x408869u : 0x40886Cu, "写入器清栈");

            var virtualTail = (byte[])bytes.Clone();
            BinaryPrimitives.WriteUInt32LittleEndian(virtualTail.AsSpan(Offset(virtualTail, layout.PointerAddress), 4), 0x4B0000);
            Assert(!EngineEffectAssignmentService.ProbeJobLayout(virtualTail).Verified, "没有原始文件映射的虚拟尾部仍开放编辑。");
            var relocated = (byte[])bytes.Clone();
            var targetAddress = layout.TableAddress + 0x4000;
            var targetOffset = Offset(relocated, targetAddress);
            bytes.AsSpan(checked((int)layout.TableOffset), layout.RowCount * layout.RowSize)
                .CopyTo(relocated.AsSpan(targetOffset));
            BinaryPrimitives.WriteUInt32LittleEndian(relocated.AsSpan(Offset(relocated, layout.PointerAddress), 4), targetAddress);
            var moved = EngineEffectAssignmentService.ProbeJobLayout(relocated);
            Assert(moved.Verified && moved.TableAddress == targetAddress && moved.TableOffset == targetOffset,
                "有效表指针迁移后仍使用固定文件偏移。");

            var opaque = (byte[])bytes.Clone();
            BinaryPrimitives.WriteUInt16LittleEndian(opaque.AsSpan(checked((int)layout.GetPersonIdOffset(0, 0)), 2), 0xFEDC);
            opaque[checked((int)layout.GetJobIdOffset(0, 0))] = 79;
            opaque[checked((int)layout.GetJobValueOffset(0, 0))] = 231;
            var changedFields = EngineEffectAssignmentService.ProbeJobLayout(opaque);
            Assert(changedFields.Verified && changedFields.ReadPersonIds(opaque, 0)[0] == 0xFEDC,
                "分配存储被业务值/未解析消费者不必要地锁定，或不透明人物ID被改写。");
            Assert(hash.SequenceEqual(SHA256.HashData(bytes)) && hash.SequenceEqual(SHA256.HashData(File.ReadAllBytes(path))),
                "只读布局测试改动了来源文件。");
            Console.WriteLine($"LAYOUT_OK {sample.Name} rows={layout.RowCount} width={layout.RowSize} slots={layout.SlotCount} " +
                $"sharedN={layout.SharedValue} pointer=0x{layout.PointerAddress:X8} table=0x{layout.TableAddress:X8} file=0x{layout.TableOffset:X} " +
                "allRows=PASS boundary=PASS mutations=7/7 relocation=PASS opaqueIds=PASS sourceUnchanged=PASS");
        }
        Console.WriteLine("EFFECT_ASSIGNMENT_LAYOUT_TESTS_OK samples=4");
    }

    private static void RejectMutation(byte[] original, uint address, string label)
    {
        var changed = (byte[])original.Clone();
        changed[Offset(changed, address)] ^= 1;
        Assert(!EngineEffectAssignmentService.ProbeJobLayout(changed).Verified, "损坏的" + label + "仍通过存储探测。");
    }

    private static int Offset(byte[] image, uint address)
    {
        var pe = BinaryPrimitives.ReadInt32LittleEndian(image.AsSpan(0x3C, 4));
        var optional = pe + 24;
        var imageBase = BinaryPrimitives.ReadUInt32LittleEndian(image.AsSpan(optional + 28, 4));
        var sectionCount = BinaryPrimitives.ReadUInt16LittleEndian(image.AsSpan(pe + 6, 2));
        var sectionTable = optional + BinaryPrimitives.ReadUInt16LittleEndian(image.AsSpan(pe + 20, 2));
        for (var index = 0; index < sectionCount; index++)
        {
            var header = sectionTable + index * 40;
            var rva = BinaryPrimitives.ReadUInt32LittleEndian(image.AsSpan(header + 12, 4));
            var length = BinaryPrimitives.ReadUInt32LittleEndian(image.AsSpan(header + 16, 4));
            if (address < imageBase + rva || (ulong)address >= (ulong)imageBase + rva + length) continue;
            return checked((int)(BinaryPrimitives.ReadUInt32LittleEndian(image.AsSpan(header + 20, 4)) + address - imageBase - rva));
        }
        throw new InvalidDataException($"测试VA 0x{address:X8}没有磁盘映射。");
    }

    private static void ThrowsRange(Action action)
    {
        try { action(); }
        catch (ArgumentOutOfRangeException) { return; }
        throw new InvalidOperationException("分配表末行或槽位上界未生效。");
    }

    private static void Assert(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }
}
