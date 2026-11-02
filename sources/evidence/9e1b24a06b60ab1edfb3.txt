using System.Buffers.Binary;
using DataManager.Core.Models;

namespace DataManager.Core.Binary;

/// <summary>Annotates text budgets without changing physical geometry or history identity.</summary>
public static class TextConsumerEvidence
{
    private static readonly HashSet<string> VerifiedEngines = new(StringComparer.OrdinalIgnoreCase)
    {
        "3890CC3247163D30CD0A2F3412E06A83E7270AA9324B6E358D84EFAED07DC08C",
        "34B810EE790F4BAA70EBF60AA286AA7BD246A2C17B425B36BD3825B36BA2D6DA",
        "A99DDD6971669D4847444F91B9ED211CD205107E1074528CCEDB86E360FC1282"
    };

    public static bool IsVerifiedEngine(byte[] executable) => VerifiedEngines.Contains(HashService.Sha256(executable));

    public static IReadOnlyList<TableDefinition> Apply(IEnumerable<TableDefinition> tables, byte[] executable)
    {
        var verified = IsVerifiedEngine(executable);
        return tables.Select(table => table with { Fields = table.Fields.Select(field =>
        {
            if (field.Kind != FieldKind.FixedString) return field;
            var constraint = TextFieldConstraints.Get(table, field);
            if (verified && !constraint.IsConservative)
                return field with { TextConstraint = constraint with { Evidence = constraint.Evidence + " 当前 EXE 的 SHA-256 匹配本次反汇编核对样本。" } };
            if (constraint.IsConservative) return field;
            var signature = MatchesConsumer(executable, table.Key, field.Size);
            return field with { TextConstraint = constraint with { IsConservative = true,
                Evidence = constraint.Evidence + (signature
                    ? " 当前 EXE 局部消费者指令特征匹配，但完整引擎指纹不同；其他修改路径未确认，仍按此布局保守限制。"
                    : " 当前 EXE 未匹配已核对指纹/消费者；按此布局保守限制，不代表已确认当前游戏读取行为。") } };
        }).ToArray() }).ToArray();
    }

    private static bool MatchesConsumer(byte[] bytes, string key, int size)
        => key switch
        {
            "persons" => At(bytes, 0x408C39, "807DF00C") && At(bytes, 0x408C59, "83450C0D"),
            "strategies" => At(bytes, 0x40D73C, "6A0AFF7508FF75FCE89742070083C40C8345FC0A8B4DFCC601008345080B"),
            "items-low" or "items-high" or "items-extended" => At(bytes, 0x4010E7, "C6410E00"),
            "job-series" => At(bytes, 0x46C4F6, "8B450848C1E0020570C548008B008038007406FF45F840EBF5"),
            "detailed-jobs" => At(bytes, 0x40111A, "558BEC8B0485A8BE48005DC3"),
            _ when size == 200 => At(bytes, 0x40BF59, "68C8000000FF75088B4D0C69C9C8000000") && At(bytes, 0x40BF78, "C682C800000000"),
            _ => false
        };

    private static bool At(byte[] bytes, uint virtualAddress, string hex)
    {
        var pattern = Convert.FromHexString(hex);
        if (bytes.Length < 0x40 || BinaryPrimitives.ReadUInt16LittleEndian(bytes) != 0x5A4D) return false;
        var pe = BinaryPrimitives.ReadInt32LittleEndian(bytes.AsSpan(0x3C));
        if (pe < 0 || pe > bytes.Length - 24 || BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(pe)) != 0x4550) return false;
        var count = BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(pe + 6));
        var optionalSize = BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(pe + 20));
        var optional = (long)pe + 24;
        if (optionalSize < 32 || optional + optionalSize > bytes.Length || BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan((int)optional)) != 0x10B) return false;
        var imageBase = BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan((int)optional + 28));
        var sectionTable = optional + optionalSize;
        if (sectionTable + count * 40L > bytes.Length) return false;
        for (var i = 0; i < count; i++)
        {
            var section = bytes.AsSpan((int)sectionTable + i * 40, 40);
            if ((BinaryPrimitives.ReadUInt32LittleEndian(section[36..]) & 0x20000000) == 0) continue;
            var rva = BinaryPrimitives.ReadUInt32LittleEndian(section[12..]);
            var rawLength = BinaryPrimitives.ReadUInt32LittleEndian(section[16..]);
            var raw = BinaryPrimitives.ReadUInt32LittleEndian(section[20..]);
            var relative = (long)virtualAddress - imageBase - rva;
            if (relative < 0 || relative + pattern.Length > rawLength || raw + relative + pattern.Length > bytes.Length) continue;
            return bytes.AsSpan(checked((int)(raw + relative)), pattern.Length).SequenceEqual(pattern);
        }
        return false;
    }
}
