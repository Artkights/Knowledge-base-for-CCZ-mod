using System.Text;
using DataManager.Core.Binary;
using DataManager.Core.Migration;
using DataManager.Core.Models;
using DataManager.Core.Profiles;

namespace DataManager.Tests;

internal static class TextConstraintTests
{
    public static void Run()
    {
        var registry = new ProfileRegistry();
        var codecRegistry = new RecordCodecRegistry();
        foreach (var (profile, variant) in new[] { ("ccz-6.5", "65-standard-v1"), ("ccz-6.6", "66-standard-v1"), ("ccz-6.6", "66-legacy-data-v1") })
        {
            var tables = registry.Resolve(profile, variant).Tables;
            foreach (var (key, budget) in new[] { ("persons", 12), ("strategies", 10), ("items-low", 14), ("items-high", 14),
                ("job-series", 8), ("detailed-jobs", 8), ("person-biography", 200), ("finishing-moves", 10), ("forge", 29) })
            {
                var table = tables.Single(t => t.Key == key);
                var field = table.Fields.First(f => f.Kind == FieldKind.FixedString);
                var constraint = TextFieldConstraints.Get(table, field);
                Assert(constraint.MaxPayloadBytes == budget, $"{variant}/{key} 文本预算错误");
                Assert(constraint.IsConservative == (key is "finishing-moves" or "forge"), $"{key} 消费者证据等级错误");
                var value = new string('汉', budget / 2) + (budget % 2 == 0 ? "" : "A");
                var result = constraint.Evaluate(value);
                Assert(result.CanEncode && result.ByteCount == budget && result.RemainingBytes == 0, $"{key} GBK 满边界计数错误");
                var encoded = codecRegistry.Get(table.RecordCodecKey).EncodeChangedField(new byte[table.RowSize], field, value).Single().Bytes;
                Assert(EncodingService.DecodeFixedString(encoded) == value && encoded.Length == field.Size, $"{key} 满边界不能无损往返");
                Reject(() => codecRegistry.Get(table.RecordCodecKey).EncodeChangedField(new byte[table.RowSize], field, value + "A"), $"{key} 未阻止越界");
                Reject(() => BinaryValueCodec.Encode(value + "A", field), $"{key} 直接字段编码绕过预算");
            }
        }

        var bio = registry.Resolve("ccz-6.5").Tables.Single(t => t.Key == "person-biography").Fields.Single();
        var fullBio = BinaryValueCodec.Encode(new string('列', 100), bio);
        Assert(fullBio.Length == 200 && !fullBio.Contains((byte)0), "列传必须支持满200字节且不占用磁盘终止符");
        var formatting = "测试 \r\n\n\r\t\u0001\u001A\u001B=\v ";
        Assert(EncodingService.DecodeFixedString(BinaryValueCodec.Encode(formatting, bio)) == formatting,
            "尾空格、独立CR/LF或格式控制码被清洗");
        Assert(TextFieldConstraints.Get(bio).Evaluate("汉A\r\n").ByteCount == 5, "换行必须按真实字节计入");
        foreach (var unsupported in new[] { "😀", "𠀀", "A\0B", "\uD800" })
        {
            Assert(!TextFieldConstraints.Get(bio).Evaluate(unsupported).CanEncode, "无法往返的字符通过预检");
            Reject(() => BinaryValueCodec.Encode(unsupported, bio), "无法往返的字符被静默替换/截断");
        }
        Reject(() => EncodingService.DecodeFixedString(new byte[] { 0x81 }), "无效GBK尾字节被静默替换");
        var malformedSlot = new byte[] { (byte)'A', 0xD7, 0 };
        var preserved = EncodingService.DecodeFixedStringPreservingInvalidBytes(malformedSlot);
        Assert(EncodingService.HasPreservedInvalidBytes(preserved), "存量损坏字节被混同真实问号");
        Assert(EncodingService.EncodeFixedStringPreservingTail(preserved, malformedSlot, new(3, 2, true, "测试")).SequenceEqual(malformedSlot),
            "未修改损坏文本未保留原始字节");
        Reject(() => EncodingService.EncodeFixedStringPreservingTail(preserved + "B", malformedSlot, new(3, 2, true, "测试")),
            "编辑损坏文本时静默带入不可编码字符");
        Assert(EncodingService.DecodeFixedString(EncodingService.EncodeFixedStringPreservingTail("AB", malformedSlot, new(3, 2, true, "测试"))) == "AB",
            "用户主动修复损坏文本失败");

        var tailRule = new TextFieldConstraint(8, 7, true, "测试保留尾部");
        byte[] original = [(byte)'A', 0, 0, 0, 0, 0, 0xDE, 0xAD];
        Assert(tailRule.ForOriginalSlot(original).MaxPayloadBytes == 5, "实际文本预算未避开隐藏尾数据及终止符");
        var changed = EncodingService.EncodeFixedStringPreservingTail("BC", original, tailRule);
        Assert(changed[6] == 0xDE && changed[7] == 0xAD && EncodingService.DecodeFixedString(changed) == "BC", "文本编辑破坏NUL后的保留字节");
        Reject(() => EncodingService.EncodeFixedStringPreservingTail("ABCDEFG", original, tailRule), "增长覆盖隐藏非零尾数据");
        var legacyName = EncodingService.GameEncoding.GetBytes("ABCDEFGHIJKLM");
        var nameRule = new TextFieldConstraint(13, 12, true, "姓名12字节");
        Assert(EncodingService.EncodeFixedStringPreservingTail("ABCDEFGHIJKLM", legacyName, nameRule).SequenceEqual(legacyName),
            "未修改存量超预算原值被截断");
        Assert(EncodingService.DecodeFixedString(EncodingService.EncodeFixedStringPreservingTail("ABCDEFGHIJKL", legacyName, nameRule)) == "ABCDEFGHIJKL",
            "主动缩短旧名称不能无损往返");

        MigrationPreviewUsesSameBudgets();
    }

    private static void MigrationPreviewUsesSameBudgets()
    {
        var roots = new[] { Path.Combine(Path.GetTempPath(), "DataManagerTextSource_" + Guid.NewGuid().ToString("N")),
            Path.Combine(Path.GetTempPath(), "DataManagerTextTarget_" + Guid.NewGuid().ToString("N")) };
        try
        {
            foreach (var root in roots)
            {
                Directory.CreateDirectory(root);
                foreach (var (file, size) in new[] { ("Data.e5", 61379), ("Star.e5", 6359), ("Ekd5.exe", 1196032), ("Imsg.e5", 450000) })
                    File.WriteAllBytes(Path.Combine(root, file), new byte[size]);
            }
            var definitions = new ProfileRegistry().Resolve("ccz-6.5").Tables;
            foreach (var (key, value) in new[] { ("persons", "ABCDEFGHIJKLM"), ("strategies", "ABCDEFGHIJK"),
                ("items-low", "ABCDEFGHIJKLMNO"), ("job-series", "ABCDEFGHI"), ("person-biography", new string('传', 100)) })
            {
                var definition = definitions.Single(t => t.Key == key);
                var field = definition.Fields.First(f => f.Kind == FieldKind.FixedString);
                var path = Path.Combine(roots[0], definition.FileName);
                var bytes = File.ReadAllBytes(path);
                EncodingService.GameEncoding.GetBytes(value).CopyTo(bytes, checked((int)definition.DataOffset + field.Offset));
                File.WriteAllBytes(path, bytes);
            }
            var plan = new MigrationService().Preview(roots[0], roots[1], "ccz-6.5", "65-standard-v1", "ccz-6.5", "65-standard-v1");
            foreach (var key in new[] { "persons", "strategies", "items-low", "job-series" })
                Assert(plan.Changes.Any(c => c.TableKey == key && c.Id == 0 && c.Kind == MigrationChangeKind.Incompatible),
                    $"迁移预览没有拒绝超预算 {key} 原始文本");
            Assert(plan.WritableChanges.Any(c => c.TableKey == "person-biography" && c.Id == 0), "满200字节列传被迁移预检错误拒绝");
        }
        finally
        {
            foreach (var root in roots) if (Directory.Exists(root)) Directory.Delete(root, true);
        }
    }

    private static void Reject(Action action, string message)
    {
        try { action(); }
        catch (ArgumentException) { return; }
        throw new InvalidOperationException(message);
    }

    private static void Assert(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }
}
