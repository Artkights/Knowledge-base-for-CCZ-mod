using System.Text;
using DataManager.Core.Models;

namespace DataManager.Core.Binary;

public sealed record TextValidationResult(int? ByteCount, int Capacity, bool CanEncode, string? Error = null, string? Warning = null)
{
    public int? RemainingBytes => ByteCount is { } count ? Capacity - count : null;
}

/// <summary>Disk geometry and the independently established text payload budget.</summary>
public sealed record TextFieldConstraint(int StorageBytes, int MaxPayloadBytes, bool RequiresTerminator,
    string Evidence, bool IsConservative = false)
{
    public TextFieldConstraint ForOriginalSlot(ReadOnlySpan<byte> original)
    {
        if (original.Length != StorageBytes) throw new InvalidDataException("文本原始槽位长度与约束不一致。");
        var terminator = original.IndexOf((byte)0);
        if (terminator < 0) return this;
        for (var i = terminator + 1; i < original.Length; i++)
            if (original[i] != 0 && i - 1 < MaxPayloadBytes)
                return this with { MaxPayloadBytes = i - 1,
                    Evidence = Evidence + $" 本槽第 {i + 1} 字节起含非零保留数据，实际文本容量收窄为 {i - 1} 字节。" };
        return this;
    }

    public TextValidationResult Evaluate(string? value)
    {
        value ??= string.Empty;
        int count;
        try { count = EncodingService.GameEncoding.GetByteCount(value); }
        catch (EncoderFallbackException ex)
        {
            return new(null, MaxPayloadBytes, false,
                $"第 {ex.Index + 1} 个 UTF-16 位置含 GBK/CP936 无法表示的字符；请替换该字符，不能以问号代写。");
        }
        if (value.IndexOf('\0') is var nul && nul >= 0)
            return new(count, MaxPayloadBytes, false, $"第 {nul + 1} 个位置是 NUL；游戏会在此截断，不能无损保存。");
        if (count > MaxPayloadBytes)
            return new(count, MaxPayloadBytes, false, $"最多 {MaxPayloadBytes} 个 GBK 字节，当前 {count} 字节，超出 {count - MaxPayloadBytes} 字节。");
        var warnings = new List<string>();
        if (IsConservative) warnings.Add("此容量采用保守保存策略；尚未确认全部目标引擎消费者。");
        if (value.Any(ch => ch < ' ' && ch is not ('\r' or '\n' or '\v' or '\u001B')))
            warnings.Add("含游戏普通文本绘制时会忽略的控制码；仍计入字节并原样保留。");
        if (value.Contains('\u001B') || value.Contains('\v'))
            warnings.Add("含游戏格式/布局控制码；按原始字节保留。");
        return new(count, MaxPayloadBytes, true, Warning: warnings.Count == 0 ? null : string.Join("；", warnings));
    }

    internal byte[] Encode(string? value)
    {
        if (StorageBytes < 0 || MaxPayloadBytes < 0 || MaxPayloadBytes + (RequiresTerminator ? 1 : 0) > StorageBytes)
            throw new InvalidDataException("文本约束超过物理槽位。");
        var result = Evaluate(value);
        if (!result.CanEncode)
        {
            if (result.ByteCount > MaxPayloadBytes)
                throw new ArgumentOutOfRangeException(nameof(value), result.Error);
            throw new ArgumentException(result.Error, nameof(value));
        }
        return EncodingService.GameEncoding.GetBytes(value ?? string.Empty);
    }
}

/// <summary>
/// The named budgets were traced in the local 6.5, 6.6 standard15 and legacy17
/// executables. They are safe defaults for those layouts, not a claim that every
/// modified engine has identical consumers. Unknown consumers remain explicit.
/// </summary>
public static class TextFieldConstraints
{
    public static TextFieldConstraint Get(TableFieldDefinition field)
        => field.TextConstraint ?? new(field.Size, field.Size, false,
            "仅确认物理槽宽；未另行确认该字段的运行时消费者。", true);

    public static TextFieldConstraint Get(TableDefinition table, TableFieldDefinition field)
    {
        if (field.TextConstraint != null) return field.TextConstraint;
        var rule = table.Key switch
        {
            "persons" => (12, true, false, "本地三套引擎姓名加载器只复制 12 字节；物理槽为 13 字节。"),
            "strategies" => (10, true, false, "本地三套引擎策略加载器只复制 10 字节并追加终止符。"),
            "items-low" or "items-high" or "items-extended" => (14, true, false, "本地三套引擎初始化物品数组时将 row[14] 置零；物理槽可能为 15 或 17 字节。"),
            "job-series" or "detailed-jobs" => (8, true, false, "本地三套引擎按 NUL 结尾字符串读取 9 字节槽，须在槽内保留终止符。"),
            "finishing-moves" => (10, true, true, "名称物理槽 11 字节；运行时消费者未确认，暂在槽内保留一个 NUL。"),
            "forge" => (29, true, true, "名称物理槽 30 字节；运行时消费者未确认，暂在槽内保留一个 NUL。"),
            "effect-names" or "item-effect-names-66" => (15, true, false, "16 字节名称槽保留终止符；实际可增长容量还受非零尾部保留字节限制。"),
            _ when field.Size == 200 && table.FileName.Equals("Imsg.e5", StringComparison.OrdinalIgnoreCase)
                => (200, false, false, "本地三套引擎的 Imsg 读取器读取 200 字节后在缓冲区第 201 字节追加 NUL；列传满 200 字节样本已核对。"),
            _ => (field.Size, false, true, "仅确认物理槽宽；未另行确认该字段的运行时消费者。")
        };
        // A custom narrower layout must never gain capacity from a baseline rule.
        var capacity = Math.Min(rule.Item1, Math.Max(0, field.Size - (rule.Item2 ? 1 : 0)));
        return new(field.Size, capacity, rule.Item2, rule.Item4, rule.Item3);
    }

    /// <summary>Use the original complete row to include this slot's preserved tail budget in UI feedback.</summary>
    public static TextFieldConstraint Get(TableDefinition table, TableFieldDefinition field, ReadOnlySpan<byte> originalRow)
        => Get(table, field).ForOriginalSlot(originalRow.Slice(field.Offset, field.Size));

    public static TableDefinition Apply(TableDefinition table)
        => table with { Fields = table.Fields.Select(field => field.Kind == FieldKind.FixedString
            ? field with { TextConstraint = Get(table, field) } : field).ToArray() };
}
