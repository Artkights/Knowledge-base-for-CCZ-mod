using System.Text;
using DataManager.Core.Editing;
using DataManager.Core.Models;

namespace DataManager.Core.Scanner;

public enum EngineConstantKind { Byte, Int32, Text }

/// <summary>One signature-guarded location of a constant; different bases may use different code shapes.</summary>
/// <param name="SecondaryFieldVa">Optional second byte that must carry the same value (paired clamp).</param>
/// <param name="Bases">Profiles this layout is valid for; null means every supported base.</param>
/// <param name="Relocate">
/// Allows the signature to be searched when the recorded address no longer matches.
/// Only layouts with a globally unique signature should set this.
/// </param>
/// <param name="Nature">Overrides the definition nature when this layout stores an effect value instead of a code immediate.</param>
/// <param name="RelativePointerVa">
/// Optional VA of a 4-byte pointer to the effect assignment table. When set, the field address is
/// resolved as pointer value + <paramref name="RelativeOffset"/> instead of relying on a fixed table address.
/// </param>
/// <param name="RelativeOffset">Byte offset from the effect assignment table base to this field.</param>
public sealed record EngineConstantLayout(string Label, uint FieldVa, long FieldFileOffset, int Length,
    byte[] Prefix, byte[] Suffix, uint SecondaryFieldVa = 0, long SecondaryFileOffset = -1,
    byte[]? SecondaryPrefix = null, byte[]? SecondarySuffix = null, IReadOnlyList<string>? Bases = null,
    bool Relocate = false, string? Nature = null, uint RelativePointerVa = 0, uint RelativeOffset = 0,
    int SecondaryLength = 0, byte[]? PrefixMask = null, byte[]? SuffixMask = null,
    byte[]? SecondaryPrefixMask = null, byte[]? SecondarySuffixMask = null,
    IReadOnlyList<EngineConstantExtraField>? ExtraFields = null, bool Optional = false)
{
    public bool AppliesTo(string? version) =>
        version == null || Bases == null || Bases.Contains(version, StringComparer.Ordinal);
}

/// <summary>
/// An additional same-valued immediate guarded by its own signature. Used when one balance value is
/// duplicated across more than two sites (for example the six-stat clamp of 夺锐攻击).
/// </summary>
public sealed record EngineConstantExtraField(uint FieldVa, long FieldFileOffset, byte[] Prefix, byte[] Suffix,
    int Length = 0, byte[]? PrefixMask = null, byte[]? SuffixMask = null);

/// <summary>A confirmed engine constant: one immediate byte or one fixed text slot.</summary>
public sealed record EngineConstantDefinition(string Id, string Module, string DisplayName, string Unit,
    string Description, string Evidence, EngineConstantKind Kind, int Minimum, int Maximum,
    IReadOnlyList<EngineConstantLayout> Layouts, IReadOnlyList<string>? ApplicableBases = null)
{
    public string Nature => Kind == EngineConstantKind.Text ? "文本槽" : "代码固定值";
    public string LocationText => string.Join("；", Layouts.Select(layout =>
    {
        var text = layout.RelativePointerVa != 0
            ? $"{layout.Label} 指针 0x{layout.RelativePointerVa:X8}+0x{layout.RelativeOffset:X}（原 0x{layout.FieldVa:X8}）"
            : layout.FieldVa != 0
                ? $"{layout.Label} 0x{layout.FieldVa:X8}（文件 +0x{layout.FieldFileOffset:X}）"
                : $"{layout.Label} 文件 +0x{layout.FieldFileOffset:X}，{layout.Length} 字节";
        if (layout.SecondaryFieldVa != 0)
            text += $"；同步 0x{layout.SecondaryFieldVa:X8}";
        if (layout.ExtraFields is { Count: > 0 } extras)
            text += $"；另同步 {extras.Count} 处（0x{string.Join("、0x", extras.Select(item => $"{item.FieldVa:X8}"))}）";
        return text;
    }));
}

public sealed record EngineConstantValue(EngineConstantDefinition Definition, EngineConstantLayout Layout,
    long FileOffset, int? NumericValue, string TextValue, byte[] OriginalBytes, bool SignatureMatches,
    string Diagnostic, long SecondaryFileOffset = -1, IReadOnlyList<long>? ExtraFileOffsets = null)
{
    public string Nature => Layout.Nature ?? Definition.Nature;
}

public sealed record EngineConstantEdit(string Id, int? NumericValue, string? TextValue);

public sealed record EngineConstantRelocationCheck(string DefinitionId, string Label, bool Applicable,
    bool Relocate, bool ExactMatch, int SignatureHits, IReadOnlyList<uint> HitAddresses, bool Optional = false);

public sealed record EngineConstantContextSuggestion(string DefinitionId, string Label, byte[] Prefix,
    byte[] Suffix, int Hits, uint HitAddress, bool Exact);

public sealed record EngineConstantCommitResult(bool Success, string Message, string? BackupPath = null,
    int ChangedBytes = 0)
{
    public static EngineConstantCommitResult Failed(string message) => new(false, message);
}

/// <summary>Reads and writes the confirmed special-skill constants shown on the 常量 page.</summary>
public sealed class EngineConstantService
{
    static EngineConstantService() => Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);

    private static readonly byte[] CmpByteBpF8Prefix = [0x80, 0x7D, 0xF8];
    private static readonly byte[] CmpByteBpF4Prefix = [0x80, 0x7D, 0xF4];
    private static readonly byte[] CmpByteBpFcPrefix = [0x80, 0x7D, 0xFC];
    private static readonly byte[] CmpAlPrefix = [0x3C];
    private static readonly byte[] MovAlPrefix = [0xB0];
    private static readonly byte[] JaeSuffix = [0x73];
    private static readonly byte[] BreakthroughDamageSuffix = [0x83, 0x7D, 0x08, 0x01, 0x74];

    public static readonly IReadOnlyList<EngineConstantDefinition> Definitions =
    [
        new("guided-attack-count", "连击次数", "引导攻击追加次数", "次",
            "击杀目标后最多再引导几次；总攻击次数 = 这个值 + 1。6.4 默认 4（共五次），6.5/6.6 默认 2（共三次）。部分改版基底写 255 表示基本不限次数。",
            "引导循环 0x004212F1：inc byte [ebp-8] 后 cmp byte [ebp-8], 本值；指令 0x0042133D 字节 80 7D F8 ?? 73。",
            EngineConstantKind.Byte, 0, 255,
            [new("全部基底", 0x00421340, 0x20740, 1, CmpByteBpF8Prefix, [0x73, 0x16],
                Relocate: true)]),
        new("furious-attack-targets", "连击次数", "奋战攻击目标数", "人",
            "奋战会依次打几个相邻目标，引导共用这份列表。8 = 周围八格全算，4 = 只算十字四格。",
            "列表构建 0x00405BE8（6.6 为 0x00405BF2）：循环 cmp 本值后查 0x004359F5 方向表、过滤并写入 0x00500E9D 目标列表；0x00417C67 逐项执行攻击，0x004212F1 负责引导链。",
            EngineConstantKind.Byte, 1, 8,
            [
                new("6.4/6.5", 0x00405C16, 0x5016, 1, [0xFE, 0x45, 0xF4, 0x80, 0x7D, 0xF4],
                    [0x73, 0x3A, 0xFF, 0x75, 0xF4, 0x8D, 0x4D, 0xFC, 0x51],
                    Bases: ["6.4", "6.5"], Relocate: true),
                new("6.6", 0x00405C13, 0x5013, 1, [0x8B, 0x45, 0xF4, 0x3C],
                    [0x73, 0x3D, 0x50, 0x8D, 0x4D, 0xFC, 0x51, 0xE8],
                    Bases: ["6.6"], Relocate: true)
            ]),
        new("active-combo-chance", "连击次数", "主动连击发动率", "%",
            "拥有主动连击时，追加一击的发动概率：100 = 每次都追加，50 = 一半机会。",
            "特效 52 桩：确认特效 52（0x34）后 mov al,本值（6.4 指令 0x00405CF7，6.5/6.6 指令 0x004E411B 与 0x004E4145，字节均为 B0 64）；返回值直接作为概率实参传给 0x00437896，该函数把上限钳到 100 后与 0..99 随机数比较。双枪攻击桩 0x004060D2 与 0x004E3000 也按它判定追加一击。",
            EngineConstantKind.Byte, 0, 100,
            [
                new("6.5/6.6", 0x004E411C, 0xB591C, 1, [0x04, 0xB0], [0xEB, 0x35, 0x8B],
                    SecondaryFieldVa: 0x004E4146, SecondaryFileOffset: 0xB5946,
                    SecondaryPrefix: [0x75, 0x04, 0xB0], SecondarySuffix: [0xEB, 0x0B, 0xFF],
                    Bases: ["6.5", "6.6"], Relocate: true),
                new("6.4", 0x00405CF8, 0x50F8, 1, [0x04, 0xB0], [0xEB, 0x0B, 0xFF],
                    Bases: ["6.4"], Relocate: true)
            ]),
        new("counter-damage-share", "强化反击", "普通反击伤害份数", "份",
            "没有强化反击时，反击伤害按攻击伤害的几份结算：3 = 75%，4 = 全额，2 = 50%。",
            "特效 72 强化反击的伤害函数 0x004E31B3：没有该特效时执行 imul eax,ecx,3; shr eax,2（6.5/6.6 指令 0x004E3214，字节 6B C1 ?? C1 E8 02），即反击伤害 = 攻击伤害的 3/4；有该特效时改走损失 HP 比例加成。6.4 同址为空，不适用。",
            EngineConstantKind.Byte, 0, 8,
            [new("6.5/6.6", 0x004E3216, 0xB4A16, 1,
                [0x0E, 0x8B, 0x4D, 0x08, 0x6B, 0xC1], [0xC1, 0xE8, 0x02, 0x85, 0xC0, 0x75],
                Bases: ["6.5", "6.6"], Relocate: true)],
            ApplicableBases: ["6.5", "6.6"]),
        new("breakthrough-quote", "突破攻击", "突破攻击台词", "文字",
            "突破攻击触发时显示的固定台词，最多 8 个汉字；超出会被截断。",
            "Ekd5.exe 固定 16 字节文本槽，文件偏移 0xD24FF；6.4/6.5/6.6 三个基底的槽内容都能按 GBK 解出完整句子。",
            EngineConstantKind.Text, 0, 0,
            [new("全部基底", 0, 0xD24FF, 16, [], [])]),
        new("breakthrough-damage-bonus", "突破攻击", "突破攻击伤害加成", "%",
            "突破攻击触发时伤害额外增加的百分比：40 = 伤害×1.4，0 = 不加成。伤害增幅走自己的装备值。",
            "伤害函数 0x0043BC62 在 0x0043BE1B 调用 0x00411072：确认特效 97 突破后执行 mov al,本值（指令 0x004110C0），再由 0x00425AD9 按 伤害×百分比/100 追加；三基底同址同值 40。",
            EngineConstantKind.Byte, 0, 200,
            [new("全部基底", 0x004110C1, 0x104C1, 1, MovAlPrefix, BreakthroughDamageSuffix,
                Relocate: true)]),
        new("drain-attack-cap", "吸血攻击", "吸血攻击吸取上限", "%",
            "吸血攻击最多按造成伤害的百分之几回血：100 = 全额回血，50 = 最多回一半。6.6 同名特技为“以战养战”。",
            "函数 0x00406B3C：确认特效 20 后用 cmp al,本值（0x00406B99）和 mov al,本值（0x00406B9D）成对把吸取比例钳到上限，再按 伤害×比例/100 回血；三基底同址同值 100。",
            EngineConstantKind.Byte, 0, 100,
            [new("全部基底", 0x00406B9A, 0x5F9A, 1,
                [0xE8, 0x00, 0x00, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x00, 0x3C],
                [0x76, 0x02, 0xB0, 0x64, 0xFF, 0x35, 0x00, 0x00, 0x00, 0x00, 0x50, 0xE8],
                SecondaryFieldVa: 0x00406B9E, SecondaryFileOffset: 0x5F9E,
                SecondaryPrefix: [0x76, 0x02, 0xB0], SecondarySuffix: [0xFF, 0x35],
                PrefixMask: [0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x00, 0x01],
                SuffixMask: [0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01],
                Relocate: true)]),
        new("iron-chain-directions", "铁索横江", "铁索横江邻接方向数", "方向",
            "铁索横江会检查几个方向的相邻友军：4 = 十字四格，8 = 八方格。改大后斜向相邻的友军也会纳入连锁。6.6 同名特技为“一步剑围”。",
            "函数 0x00412B5F：按方向循环 call 0x0041031C 取邻格、0x00435884 取单位、0x00406710 比阵营并查询特效 96；循环上限 cmp al,本值（6.4/6.5 指令 0x00412B79、6.6 0x00412B7A，字节 3C ?? 73）。三基底同值 4。",
            EngineConstantKind.Byte, 4, 8,
            [
                new("6.4/6.5", 0x00412B7A, 0x11F7A, 1, [0x8B, 0x45, 0xFC, 0x3C],
                    [0x73, 0x40, 0x8D, 0x4D, 0xF0, 0x51],
                    Bases: ["6.4", "6.5"], Relocate: true),
                new("6.6", 0x00412B7B, 0x11F7B, 1, [0x8B, 0x45, 0xFC, 0x3C],
                    [0x73, 0x3F, 0x54, 0x8B, 0x4D, 0x0C, 0xE8],
                    Bases: ["6.6"], Relocate: true)
            ]),
        new("heavy-strike-cap", "猛击", "猛击伤害比例上限", "%",
            "猛击额外造成目标当前 HP 的百分之几伤害；这里限制这个百分比最大能到多少。100 = 最多打掉目标当前 HP 的量。6.6 同名特技为“势不可挡”。",
            "函数 0x00422026：确认特效 114 后用 cmp al,本值 与 mov al,本值 成对钳制，再由 0x004220D3 按 目标当前HP×N/100 追加伤害；6.4 在 0x00422039/0x0042203D，6.5/6.6 在 0x00422036/0x0042203A。",
            EngineConstantKind.Byte, 0, 100,
            [
                new("6.4", 0x00422039, 0x21439, 1,
                    [0x8B, 0x49, 0x00, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x00, 0x3C], [0x76, 0x02],
                    SecondaryFieldVa: 0x0042203D, SecondaryFileOffset: 0x2143D,
                    SecondaryPrefix: [0x76, 0x02, 0xB0], SecondarySuffix: [0x89, 0x45, 0xF4],
                    PrefixMask: [0x01, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01, 0x00, 0x01],
                    Bases: ["6.4"], Relocate: true),
                new("6.5", 0x00422036, 0x21436, 1,
                    [0x55, 0x8B, 0xEC, 0x8B, 0x4D, 0x08, 0xE8, 0x68, 0x9F, 0xFE, 0xFF, 0x85, 0xC0, 0x74, 0x14, 0x3C],
                    [0x76, 0x02], SecondaryFieldVa: 0x0042203A, SecondaryFileOffset: 0x2143A,
                    SecondaryPrefix: [0x02, 0xB0], SecondarySuffix: [0x50, 0x6A, 0x08],
                    Bases: ["6.5"], Relocate: true),
                new("6.6", 0x00422036, 0x21436, 1,
                    [0x55, 0x8B, 0xEC, 0x8B, 0x4D, 0x08, 0xE8, 0x68, 0x9F, 0xFE, 0xFF, 0x85, 0xC0, 0x74, 0x14, 0x3C],
                    [0x76, 0x02], SecondaryFieldVa: 0x0042203A, SecondaryFileOffset: 0x2143A,
                    SecondaryPrefix: [0x02, 0xB0], SecondarySuffix: [0x50, 0x6A, 0x02],
                    Bases: ["6.6"], Relocate: true),
                // 部分 6.6 改版人物仍然是 6.5 式的“cmp al,N; jbe; mov al,N; push eax; push 8”，
                // 用可选布局单独收录，官方 6.6 仍优先走上面的 push 2 布局。
                new("6.6改版（6.5式）", 0x00422036, 0x21436, 1,
                    [0x55, 0x8B, 0xEC, 0x8B, 0x4D, 0x08, 0xE8, 0x68, 0x9F, 0xFE, 0xFF, 0x85, 0xC0, 0x74, 0x14, 0x3C],
                    [0x76, 0x02], SecondaryFieldVa: 0x0042203A, SecondaryFileOffset: 0x2143A,
                    SecondaryPrefix: [0x02, 0xB0], SecondarySuffix: [0x50, 0x6A, 0x08],
                    Bases: ["6.6"], Relocate: true, Optional: true)
            ]),
        new("shield-counter-cap", "盾反", "盾反反弹比例上限", "%",
            "盾反额外反弹攻击者当前 HP 的百分之几伤害；这里限制这个百分比最大能到多少。100 = 最多反弹攻击者当前 HP 的量。6.4 名称“花枪驭敌”，6.6 名称“厄难毒体”。",
            "函数 0x00422026：确认特效 115 后用 cmp al,本值 与 mov al,本值 成对钳制，再由 0x004220D3 按 攻击者当前HP×N/100 反弹；6.4 在 0x004220B5/0x004220B9，6.5/6.6 在 0x0042205F/0x00422063。",
            EngineConstantKind.Byte, 0, 100,
            [
                new("6.4", 0x004220B5, 0x214B5, 1,
                    [0xE8, 0x00, 0x00, 0x00, 0x00, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x85, 0xC0, 0x74, 0x00, 0x3C],
                    [0x76, 0x02],
                    SecondaryFieldVa: 0x004220B9, SecondaryFileOffset: 0x214B9,
                    SecondaryPrefix: [0x76, 0x02, 0xB0], SecondarySuffix: [0x50, 0x6A, 0x02],
                    PrefixMask: [0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00,
                        0x01, 0x01, 0x01, 0x00, 0x01],
                    Bases: ["6.4"], Relocate: true),
                new("6.5", 0x0042205F, 0x2145F, 1,
                    [0xE8, 0x51, 0x9F, 0xFE, 0xFF, 0x85, 0xC0, 0x74, 0x14, 0x3C], [0x76, 0x02],
                    SecondaryFieldVa: 0x00422063, SecondaryFileOffset: 0x21463,
                    SecondaryPrefix: [0x02, 0xB0], SecondarySuffix: [0x50, 0x6A, 0x02],
                    Bases: ["6.5"], Relocate: true),
                new("6.6", 0x0042205F, 0x2145F, 1,
                    [0xE8, 0x51, 0x9F, 0xFE, 0xFF, 0x85, 0xC0, 0x74, 0x14, 0x3C], [0x76, 0x02],
                    SecondaryFieldVa: 0x00422063, SecondaryFileOffset: 0x21463,
                    SecondaryPrefix: [0x02, 0xB0], SecondarySuffix: [0x50, 0x6A, 0x10],
                    Bases: ["6.6"], Relocate: true),
                new("6.6-6.5式", 0x0042205F, 0x2145F, 1,
                    [0xE8, 0x51, 0x9F, 0xFE, 0xFF, 0x85, 0xC0, 0x74, 0x14, 0x3C], [0x76, 0x02],
                    SecondaryFieldVa: 0x00422063, SecondaryFileOffset: 0x21463,
                    SecondaryPrefix: [0x02, 0xB0], SecondarySuffix: [0x50, 0x6A, 0x02],
                    Bases: ["6.6"], Relocate: true, Optional: true)
            ]),
        new("demon-stat-cap", "神魔附体", "神魔附体属性上限", "点",
            "神魔附体提升单项属性时最多算到多少；9999 是原版上限。6.6 同名特技为“洗髓易筋”。",
            "属性写入函数 0x0043C4D3 由 0x0040715A/0x0040718F/0x004071C4/0x004071F9/0x0040722E 五个神魔附体消费者调用；6.5 在 0x0043C516/0x0043C51D 把结果钳到 9999，6.6 在 0x0043C521/0x0043C528。两处同值。",
            EngineConstantKind.Int32, 1, 99999,
            [
                new("6.5", 0x0043C517, 0x3B917, 4, [0x03, 0x45, 0xFC, 0x3D], [0x72, 0x05],
                    SecondaryFieldVa: 0x0043C51E, SecondaryFileOffset: 0x3B91E,
                    SecondaryPrefix: [0x72, 0x05, 0xB8], SecondarySuffix: [0x8B, 0xE5, 0x5D],
                    Bases: ["6.5"], Relocate: true),
                new("6.6", 0x0043C522, 0x3B922, 4, [0x3D], [0x72, 0x05],
                    SecondaryFieldVa: 0x0043C529, SecondaryFileOffset: 0x3B929,
                    SecondaryPrefix: [0x72, 0x05, 0xB8], SecondarySuffix: [0x8B, 0xE5, 0x5D],
                    Bases: ["6.6"], Relocate: true),
                new("6.6-6.5式", 0x0043C517, 0x3B917, 4, [0x03, 0x45, 0xFC, 0x3D], [0x72, 0x05],
                    SecondaryFieldVa: 0x0043C51E, SecondaryFileOffset: 0x3B91E,
                    SecondaryPrefix: [0x72, 0x05, 0xB8], SecondarySuffix: [0x8B, 0xE5, 0x5D],
                    Bases: ["6.6"], Relocate: true, Optional: true)
            ], ApplicableBases: ["6.5", "6.6"]),
        new("swift-attack-bonus", "疾风攻击", "疾风攻击每点增伤", "%",
            "6.4/6.5 是代码里的固定每点增伤（不是特效值）：目标能力每低 1 点 +5%。6.6 的每点比例就是特效值 N；本行改当前兵种对应槽的 N（默认5；官方样本是兵种76槽，信奈/清儿是兵种14槽），人物槽请到特效分配页改。",
            "伤害函数 0x0043BC5A：确认特效 117 后比较目标能力值与效果值，差距取负再 imul ×本值（6.4/6.5 指令 0x0043BD86，字节 6B C0 ?? FF）；6.6 改为 add eax,0Ch; imul eax,edx，N 来自静态分配表 0x00511000 行117 的兵种76槽（文件 +0xE2F5D，当前5）。",
            EngineConstantKind.Byte, 0, 100,
            [
                new("6.4/6.5", 0x0043BD88, 0x3B188, 1, [0xD8, 0x6B, 0xC0], [0xFF, 0x75],
                    Bases: ["6.4", "6.5"], Relocate: true),
                new("6.6 兵种76槽", 0x0051175D, 0xE2F5D, 1, [0x04, 0x00, 0x4C], [0xFF, 0x00],
                    Bases: ["6.6"], Relocate: true, Nature: "特效值槽",
                    RelativePointerVa: 0x00500C3B, RelativeOffset: 0x75D),
                new("6.6 兵种14槽（上限0）", 0x0051175D, 0xE2F5D, 1, [0x0E], [0xFF, 0x00],
                    Bases: ["6.6"], Relocate: true, Optional: true, Nature: "特效值槽",
                    RelativePointerVa: 0x00500C3B, RelativeOffset: 0x75D),
                new("6.6 兵种14槽（上限5）", 0x0051175D, 0xE2F5D, 1, [0x0E], [0xFF, 0x05],
                    Bases: ["6.6"], Relocate: true, Optional: true, Nature: "特效值槽",
                    RelativePointerVa: 0x00500C3B, RelativeOffset: 0x75D),
                new("6.6-6.5式", 0x0043BD88, 0x3B188, 1, [0xD8, 0x6B, 0xC0], [0xFF, 0x75],
                    Bases: ["6.6"], Relocate: true, Optional: true)
            ]),
        new("swift-attack-offset", "疾风攻击", "疾风攻击补正值（6.6）", "点",
            "6.6 公式里的固定补正：能力差先 +12，再乘特效值。12 不是特效值；6.6 当前特效值为 5。",
            "6.6 伤害函数 0x0043BC62 在 0x0043BD80 执行 add eax,本值（字节 83 C0 0C），随后 imul eax,edx；6.4/6.5 用 imul eax,5，不含这一步。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x0043BD82, 0x3B182, 1, [0xD8, 0x83, 0xC0], [0x90, 0x90],
                Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("physical-damage-base", "伤害公式", "物理攻击基础伤害", "点",
            "物理攻击在能力差之外先加的固定伤害；默认25。改大后所有物理攻击都会更疼。",
            "物理伤害函数 0x0043BC62 在 0x0043BD34 执行 add eax,本值（字节 83 C0 19），随后才按双方能力差增减；三基底同址同值25。",
            EngineConstantKind.Byte, 0, 200,
            [new("全部基底", 0x0043BD36, 0x3B136, 1,
                [0x8B, 0x4D, 0xD4, 0xE8, 0x40, 0x69, 0xFD, 0xFF, 0x83, 0xC0],
                [0x89, 0x45, 0xFC, 0x8B, 0x45], Relocate: true)]),
        new("strategy-damage-base", "伤害公式", "策略攻击基础伤害", "点",
            "策略/精神力攻击在能力差之外先加的固定伤害；默认25。改大后所有策略攻击都会更疼。",
            "策略伤害函数在 6.4/6.5 的 0x0043C0FE、6.6 的 0x0043C115 执行 add [ebp-4],本值（字节 83 45 FC 19）；三基底同值25。",
            EngineConstantKind.Byte, 0, 200,
            [
                new("6.4/6.5", 0x0043C101, 0x3B501, 1,
                    [0x01, 0x45, 0xFC, 0x83, 0x45, 0xFC], [0x90, 0x90, 0x90, 0x90],
                    Bases: ["6.4", "6.5"], Relocate: true),
                new("6.6", 0x0043C118, 0x3B518, 1,
                    [0x01, 0x45, 0xFC, 0x83, 0x45, 0xFC], [0x8B, 0x45, 0xEC],
                    Bases: ["6.6"], Relocate: true)
            ]),
        new("strategy-damage-divisor", "伤害公式", "策略伤害能力差除数", "倍",
            "策略伤害里双方能力差除以几；默认3。改大后能力差影响变小，改1影响最大。两处必须同时改。",
            "策略伤害高位/低位两分支都执行 mov ecx,本值; div ecx（指令 0x0043C126 与 0x0043C139，字节 B9 ?? ?? ?? ?? F7 F1）；三基底同址同值3。",
            EngineConstantKind.Byte, 1, 100,
            [new("全部基底", 0x0043C126, 0x3B526, 4, [0x2B, 0x45, 0xE8, 0x99, 0xB9],
                [0xF7, 0xF1, 0x03, 0x45, 0xFC],
                SecondaryFieldVa: 0x0043C139, SecondaryFileOffset: 0x3B539,
                SecondaryPrefix: [0x2B, 0x45, 0xEC, 0x99, 0xB9],
                SecondarySuffix: [0xF7, 0xF1, 0x50, 0xFF, 0x75], Relocate: true)]),
        new("absolute-strategy-damage-bonus", "绝对策略伤害", "绝对策略伤害追加比例", "%",
            "拥有绝对策略伤害时，伤害已经高于下限还会再追加这个百分比；默认15%。改0就是只保底不追加。",
            "函数 0x00434148（特效 214）：先算 最大HP×特效值/100 作为下限；伤害高于下限时执行 push 15 + call 0x00425AD9，把伤害再加 15%；指令 0x00434186 字节 6A 0F。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x00434187, 0x33587, 1, [0xFF, 0x75, 0x08, 0x6A],
                [0xE8, 0x4C, 0x19, 0xFF, 0xFF], Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("strategy-damage-limit-cut", "限制策略伤害", "限制策略伤害额外减伤", "%",
            "拥有限制策略伤害时，伤害没有超过上限会再减这个百分比；默认20%。改0就是只封顶不减伤。",
            "函数 0x00434204（特效 216）：伤害低于上限时执行 push 20 + 伤害×20/100 再扣减；指令 0x00434242 字节 6A 14。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x00434243, 0x33643, 1, [0xFF, 0x75, 0x08, 0x6A],
                [0xE8, 0x90, 0x18, 0xFF, 0xFF], Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("absolute-damage-hp-threshold", "绝对伤害", "绝对伤害触发 HP 线", "%",
            "目标 HP 不高于这个百分比时，绝对伤害把伤害至少提高一个比例；默认 50%。",
            "函数 0x00434199（特效 215）：目标 HP% = 当前HP×100/最大HP（0x004341D9 imul 100、0x004341DE idiv），`cmp eax,本值` 立即数 0x004341E2；不高于本值时走 `push 1Eh; call 0x00425AD9; add` 提高伤害；6.4/6.5 无该查询序列。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x004341E2, 0x335E2, 1,
                [0x6B, 0xC0, 0x64, 0x33, 0xD2, 0xF7, 0xF9, 0x83, 0xF8], [0x77, 0x10, 0x8B, 0x45, 0xFC],
                Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("absolute-damage-bonus", "绝对伤害", "绝对伤害追加比例", "%",
            "绝对伤害触发时伤害至少按这个百分比提高；默认 30%。改 0 就只保底不追加。",
            "同一函数 0x00434199：触发后 `push 本值; call 0x00425AD9` 返回 伤害×本值/100，再加回伤害，最后与传入伤害取较大值；立即数 0x004341EA（字节 6A 1E），后接 call 位移在签名里用掩码忽略。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x004341EA, 0x335EA, 1,
                [0x8B, 0x45, 0xFC, 0x50, 0x6A],
                [0xE8, 0x00, 0x00, 0x00, 0x00, 0x59, 0x03, 0xC1],
                Bases: ["6.6"], Relocate: true,
                SuffixMask: [0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01])],
            ApplicableBases: ["6.6"]),
        new("lone-brave-reduction-cap", "孤勇者", "孤勇者减伤上限", "%",
            "周围敌人越少，孤勇者减伤越高；这里限制最多减到多少。默认100%。改小后封顶更低。",
            "函数 0x0041A92F（特效 210）：算出的减伤比例先 cmp 100，超过就 mov eax,100，再按比例减伤；cmp 立即数 0x0041A982，mov 立即数 0x0041A986（4 字节）。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x0041A982, 0x19D82, 1, [0x0F, 0xAF, 0xC1, 0x83, 0xF8], [0x76, 0x05, 0xB8],
                SecondaryFieldVa: 0x0041A986, SecondaryFileOffset: 0x19D86,
                SecondaryPrefix: [0x76, 0x05, 0xB8], SecondarySuffix: [0x50, 0xFF, 0x75, 0x08, 0xE8],
                SecondaryLength: 4, Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("continuous-attack-reduction-cap", "减轻连续攻击", "连续攻击减伤封顶", "%",
            "连续攻击的累计减伤达到这个比例后，本次伤害只保留 1 点；默认 100%。改小会更早触发保底。",
            "6.6 特效 211 消费者 0x00441E9C：特效值×加成表值后 `cmp eax,本值`（指令 0x00441EC8，立即数 0x00441ECA，文件 +0x412CA）；达到就只返回 1 点伤害；6.4/6.5 同址为 nop/其他代码，签名不匹配。",
            EngineConstantKind.Byte, 1, 100,
            [new("6.6", 0x00441ECA, 0x412CA, 1,
                [0x0F, 0xAF, 0xC1, 0x83, 0xF8], [0x72, 0x05, 0x33, 0xC0, 0x40, 0xEB, 0x0F],
                Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("convert-heal-mp-cost", "化力为疗", "化力为疗每点伤害MP消耗", "点",
            "化力为疗用 MP 抵扣伤害时，每 1 点伤害消耗的 MP；默认 2。改大后同样伤害更耗 MP，改小更省。",
            "6.5 特效 193 消费者 0x0040D057 的 MP 抵伤分支：MP 足够时执行 imul edx,本值（指令 0x0040D0A6，字节 6B D2 ??），随后把伤害与 MP 各扣一次；6.4/6.6 无该序列。",
            EngineConstantKind.Byte, 1, 10,
            [new("6.5", 0x0040D0A8, 0xC4A8, 1,
                [0x2B, 0x48, 0x10, 0x3B, 0xCA, 0x72, 0x0D, 0x6B, 0xD2],
                [0x3E, 0x29, 0x55, 0xB8, 0x3E, 0x29, 0x55, 0xEC, 0xEB, 0x0A],
                Bases: ["6.5"], Relocate: true)],
            ApplicableBases: ["6.5"]),
        new("sharpen-attack-cap", "夺锐攻击", "夺锐攻击能力上限", "点",
            "夺锐攻击把目标六项能力的数值上限压到本值；默认 3。六项能力同值，写入时 12 处同步。仅 6.5 有该处理函数。",
            "6.5 特效 194 消费者 0x0040D057 第一段：确认特效 194 后，对单位 +18h..+1Dh 六项能力逐项 cmp 本值（83 F9 ??）并 mov 本值（36 C6 41 ?? ??）；主 cmp 0x0040D0E1、主 mov 0x0040D0F7，另 10 处分布在 +19h..+1Dh。12 条签名在 6.5 各唯一，6.4/6.6 无该序列。",
            EngineConstantKind.Byte, 1, 100,
            [new("6.5", 0x0040D0E1, 0xC4E1, 1,
                [0x0F, 0xB6, 0x49, 0x18, 0x83, 0xF9], [0x7E, 0x14],
                SecondaryFieldVa: 0x0040D0F7, SecondaryFileOffset: 0xC4F7,
                SecondaryPrefix: [0x8B, 0x4D, 0xE0, 0x36, 0xC6, 0x41, 0x18],
                SecondarySuffix: [0x8B, 0x4D, 0xE0],
                Bases: ["6.5"], Relocate: true,
                ExtraFields:
                [
                    new(0x0040D101, 0xC501, [0x0F, 0xB6, 0x49, 0x19, 0x83, 0xF9], [0x7E, 0x14]),
                    new(0x0040D117, 0xC517, [0x8B, 0x4D, 0xE0, 0x36, 0xC6, 0x41, 0x19], [0x8B, 0x4D, 0xE0]),
                    new(0x0040D121, 0xC521, [0x0F, 0xB6, 0x49, 0x1A, 0x83, 0xF9], [0x7E, 0x14]),
                    new(0x0040D137, 0xC537, [0x8B, 0x4D, 0xE0, 0x36, 0xC6, 0x41, 0x1A], [0x8B, 0x4D, 0xE0]),
                    new(0x0040D141, 0xC541, [0x0F, 0xB6, 0x49, 0x1B, 0x83, 0xF9], [0x7E, 0x14]),
                    new(0x0040D157, 0xC557, [0x8B, 0x4D, 0xE0, 0x36, 0xC6, 0x41, 0x1B], [0x8B, 0x4D, 0xE0]),
                    new(0x0040D161, 0xC561, [0x0F, 0xB6, 0x49, 0x1C, 0x83, 0xF9], [0x7E, 0x14]),
                    new(0x0040D177, 0xC577, [0x8B, 0x4D, 0xE0, 0x36, 0xC6, 0x41, 0x1C], [0x8B, 0x4D, 0xE0]),
                    new(0x0040D181, 0xC581, [0x0F, 0xB6, 0x49, 0x1D, 0x83, 0xF9], [0x7E, 0x14]),
                    new(0x0040D197, 0xC597, [0x8B, 0x4D, 0xE0, 0x36, 0xC6, 0x41, 0x1D], [0x8B, 0x4D, 0xF4])
                ])],
            ApplicableBases: ["6.5"]),
        new("wind-rush-damage-divisor", "风驰电掣", "风驰电掣伤害除数", "点",
            "风驰电掣的加成按百分比算出后还要再除以本值；6.5 默认 11，6.6 默认 10。改大后同特效值增伤变少。",
            "函数 6.5 0x0041A4EC（6.4 同址为 nop）、6.6 0x0041A7BA：原特效值经 0x0043F74F 折算后按 0x00425AD9 追加，再执行 xor edx,edx; mov ecx,本值; div ecx; add [ebp+8],eax；6.5 指令 0x0041A51B（立即数 0x0041A51C，文件 +0x1991C），6.6 0x0041A7EF（立即数 0x0041A7F0，文件 +0x19BF0），均为 4 字节。",
            EngineConstantKind.Int32, 1, 255,
            [
                new("6.5", 0x0041A51C, 0x1991C, 4,
                    [0x0F, 0xAF, 0x45, 0xFC, 0xFF, 0x75, 0x08, 0x50, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x33, 0xD2, 0xB9],
                    [0xF7, 0xF1, 0x01, 0x45, 0x08, 0x8B, 0x45, 0x08],
                    Bases: ["6.5"], Relocate: true,
                    PrefixMask: [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01]),
                new("6.6", 0x0041A7F0, 0x19BF0, 4,
                    [0x0F, 0xAF, 0x45, 0xFC, 0xFF, 0x75, 0x08, 0x50, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x33, 0xD2, 0xB9],
                    [0xF7, 0xF1, 0x01, 0x45, 0x08, 0x8B, 0x45, 0x08],
                    Bases: ["6.6"], Relocate: true,
                    PrefixMask: [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01])
            ], ApplicableBases: ["6.5", "6.6"]),
        new("battle-veteran-damage-divisor", "越战越勇", "越战越勇伤害除数", "点",
            "越战越勇触发时，额外伤害 = 伤害 × 特效值 ÷ 本值；默认67。改大后同特效值增伤变少。",
            "函数 0x0041A865（特效 203）调用 0x0041A84E：0x0041A854 imul eax,[ebp+8]，0x0041A85A mov ecx,67，0x0041A85F div ecx；立即数 0x0041A85B。",
            EngineConstantKind.Int32, 1, 255,
            [new("6.6", 0x0041A85B, 0x19C5B, 4,
                [0x55, 0x8B, 0xEC, 0x8B, 0x45, 0x0C, 0x0F, 0xAF, 0x45, 0x08, 0x33, 0xD2, 0xB9],
                [0xF7, 0xF1, 0x5D, 0xC2, 0x08, 0x00, 0x55, 0x8B, 0xEC, 0x6A, 0x00, 0x6A, 0x01, 0x68, 0x5D, 0x00, 0x00, 0x00, 0x68, 0xCB, 0x00, 0x00, 0x00], Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("strategy-hit-cap", "命中", "策略命中/格挡率上限", "%",
            "策略命中或格挡的最终概率最多到这个数；默认100%。改小后策略更容易被挡住。",
            "函数片段 0x0043B8A0 末尾：概率先由命中曲线 0x0043B53A 算出，再叠加特效 27/28（策略命中）、29（格挡）、39（逆乱阴阳）；0x0043B9E6 cmp al,100，超过就 mov al,100。",
            EngineConstantKind.Byte, 0, 100,
            [
                new("6.4/6.5", 0x0043B9E7, 0x3ADE7, 1,
                    [0x89, 0x45, 0xF0, 0x0F, 0xB6, 0x45, 0xF0, 0x3C], [0x76, 0x02, 0xB0],
                    SecondaryFieldVa: 0x0043B9EB, SecondaryFileOffset: 0x3ADEB,
                    SecondaryPrefix: [0x76, 0x02, 0xB0],
                    SecondarySuffix: [0x5E, 0x8B, 0xE5, 0x5D, 0xC2, 0x0C, 0x00],
                    Bases: ["6.4", "6.5"], Relocate: true),
                new("6.6", 0x0043B9E7, 0x3ADE7, 1,
                    [0x89, 0x45, 0xF0, 0x0F, 0xB6, 0x45, 0xF0, 0x3C], [0x76, 0x02, 0xB0],
                    SecondaryFieldVa: 0x0043B9EB, SecondaryFileOffset: 0x3ADEB,
                    SecondaryPrefix: [0x76, 0x02, 0xB0],
                    SecondarySuffix: [0x90, 0x8B, 0xE5, 0x5D, 0xC2, 0x0C, 0x00],
                    Bases: ["6.6"], Relocate: true)
            ]),
        new("chaos-yin-yang-hit-bonus", "逆乱阴阳", "逆乱阴阳命中加成", "%",
            "拥有逆乱阴阳时，策略命中概率直接加这个百分点，最多到 100%；默认 10。",
            "函数片段 0x0043B8A0：确认特效 39（0x00405DBD）后执行 push 100、push 本值、push 当前概率、call 0x0047FA89（返回 min(100, 概率+本值)）；立即数 0x0043B9D6。",
            EngineConstantKind.Byte, 0, 100,
            [new("全部基底", 0x0043B9D6, 0x3ADD6, 1,
                [0x85, 0xC0, 0x74, 0x0F, 0x6A, 0x64, 0x6A],
                [0xFF, 0x75, 0xF0, 0xE8, 0xAA, 0x40, 0x04, 0x00], Relocate: true)],
            ApplicableBases: ["6.4", "6.5", "6.6"]),
        new("advance-retreat-double-line", "进退有据", "进退有据翻倍触发 HP 线", "%",
            "进退有据：HP 占最大 HP 的百分比达到这个值后，效果值翻倍；默认 50%。",
            "函数 0x0043D3B5（特效 220）：算 HP×100/最大HP 后与 0x32（50）比较（0x0043D3F0 与 0x0043D439 指令 83 F8 32，立即数 0x0043D3F2/0x0043D43B），达到就 imul edx,2，再按特效值×伤害/100 结算。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x0043D3F2, 0x3C7F2, 1,
                [0x6B, 0xC0, 0x64, 0x33, 0xD2, 0xF7, 0xF1, 0x5A, 0x83, 0xF8],
                [0x72, 0x03, 0x6B, 0xD2, 0x02, 0x52, 0xFF, 0x75, 0xE0],
                SecondaryFieldVa: 0x0043D43B, SecondaryFileOffset: 0x3C83B,
                SecondaryPrefix: [0x6B, 0xC0, 0x64, 0x33, 0xD2, 0xF7, 0xF1, 0x5A, 0x83, 0xF8],
                SecondarySuffix: [0x72, 0x03, 0x6B, 0xD2, 0x02, 0x52, 0xFF, 0x75, 0xF0],
                Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("effect-screen-directions", "邻格范围", "特效屏蔽方向数", "方向",
            "屏蔽/邻格类特技枚举几个方向：4 = 十字四格，8 = 八方格。6.4/6.5 默认 4，6.6 默认 8。",
            "指令 0x004253A9 cmp al, 本值；循环经 0x0041031C 取邻格并查询 0x74/0x75 通道。",
            EngineConstantKind.Byte, 4, 8,
            [new("全部基底", 0x004253AA, 0x247AA, 1, [0x8B, 0x45, 0xF4, 0x3C],
                [0x73, 0x42, 0x8D, 0x4D, 0xE8, 0x51, 0x8B, 0x4D, 0xFC, 0xE8],
                Relocate: true)]),
        new("screen-inner-directions", "邻格范围", "特效屏蔽内层方向数", "方向",
            "特效屏蔽内层判定的方向数：4 = 十字。通常要和外层方向数一起放宽，只改这个看不到效果。",
            "谓词 0x0040F1AC：call 0x0041031C 取邻格后循环 cmp al, 本值（指令 0x0040F1E8）。",
            EngineConstantKind.Byte, 4, 8,
            [new("全部基底", 0x0040F1E9, 0xF1E9, 1, [0x8B, 0x45, 0xF4, 0x3C],
                [0x73, 0x51, 0x8D, 0x4D, 0xE8, 0x51, 0x8B, 0x4D, 0xFC],
                Relocate: true)]),
        new("pass-through-directions", "移动特技", "穿越移动判定方向数", "方向",
            "穿越移动检查几个方向的可通行格：4 = 十字四格，8 = 八方格。三基底默认 4。6.6 同名特技为“无人之境”。",
            "函数 0x00437D59：按方向循环 call 0x004359F5 取邻格、0x00435884 查单位、0x0042E2B7 判定通行；循环 cmp 本值（6.4 0x00437DB8、6.5 0x00437D89、6.6 0x00437D9A）。",
            EngineConstantKind.Byte, 4, 8,
            [
                new("6.4", 0x00437DBB, 0x371BB, 1, [0xFE, 0x45, 0xFC, 0x80, 0x7D, 0xFC],
                    [0x73, 0x52, 0xFF, 0x75, 0xFC, 0xFF, 0x75, 0x08, 0xE8],
                    Bases: ["6.4"], Relocate: true),
                new("6.5", 0x00437D8A, 0x3718A, 1, [0x8B, 0x45, 0xF0, 0x3C],
                    [0x73, 0x47, 0x50, 0xFF, 0x75, 0xF4, 0xE8],
                    Bases: ["6.5"], Relocate: true),
                new("6.6", 0x00437D9B, 0x3719B, 1, [0x8B, 0x45, 0xF0, 0x3C],
                    [0x73, 0x47, 0x50, 0xFF, 0x75, 0xF4, 0xE8],
                    Bases: ["6.6"], Relocate: true)
            ]),
        new("aura-range", "邻格范围", "状态强化/周围能力范围", "格",
            "周围能力枚举几格：9 = 自身 + 八方，4 = 自身 + 三方向。6.4/6.5 默认 9，6.6 默认 4。6.6 同名特技为“兼济天下”。",
            "循环 0x0042214A：FF 45 F8（inc [ebp-8]）、8B 45 F8（mov eax,[ebp-8]）、3C 本值（cmp al,imm）、73 相对跳转、85 C0 75 05；索引 0 单独表示当前单位自身，其余索引映射方向表。签名必须包含循环头，只写 cmp 后缀会在异引擎上误匹配到其他循环上界。",
            EngineConstantKind.Byte, 1, 9,
            [
                new("6.4/6.5", 0x00422151, 0x21551, 1, [0xFF, 0x45, 0xF8, 0x8B, 0x45, 0xF8, 0x3C],
                    [0x73, 0x57, 0x85, 0xC0, 0x75, 0x05, 0x8B], SuffixMask: [1, 0, 1, 1, 1, 1, 1],
                    Bases: ["6.4", "6.5"], Relocate: true),
                new("6.6", 0x00422151, 0x21551, 1, [0xFF, 0x45, 0xF8, 0x8B, 0x45, 0xF8, 0x3C],
                    [0x73, 0x3D, 0x85, 0xC0, 0x75, 0x05, 0x8B], SuffixMask: [1, 0, 1, 1, 1, 1, 1],
                    Bases: ["6.6"], Relocate: true)
            ]),
        new("combo-damage-bonus", "连击伤害", "连击固定增伤", "%",
            "强化连击/连击上限类特效触发后，连击伤害不再逐次衰减，并在原伤害上额外加这个固定百分比；0 = 只不衰减，10 = 每次连击多 10%。",
            "函数 0x004E313C（6.4 同址为空）：确认特效后执行 imul eax,[ebp-4]; add eax,本值（6.5/6.6 指令 0x004E319C，字节 0F AF 45 FC 83 C0 ??），再按百分比追加。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.5/6.6", 0x004E319E, 0xB499E, 1,
                [0x0F, 0xAF, 0x45, 0xFC, 0x83, 0xC0], [0xFF, 0x75, 0x08, 0x50, 0xE8],
                Bases: ["6.5", "6.6"], Relocate: true)],
            ApplicableBases: ["6.5", "6.6"]),
        new("adversity-reduction-cap", "逆境减伤", "逆境减伤最大比例", "%",
            "生命越低减伤越高；这里限制最多按已损失生命的多少比例减伤。80 = 最多减 80%。",
            "函数 0x0044904E：确认特效后算 (最大HP-当前HP)×本值/最大HP，再按该比例减少伤害；6.5/6.6 指令 0x00449091 字节 6B C0 50。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.5/6.6", 0x00449093, 0x48493, 1,
                [0x2B, 0x45, 0xFC, 0x6B, 0xC0], [0x33, 0xD2, 0xF7, 0xF9, 0x85, 0xC0],
                Bases: ["6.5", "6.6"], Relocate: true)],
            ApplicableBases: ["6.5", "6.6"]),
        new("sneak-attack-step", "偷袭攻击", "偷袭攻击每档增伤", "%",
            "侧击按 1 档、背击按 2 档，每档增加这个百分比；25 = 侧击 +25%、背击 +50%。",
            "函数 0x004D2700：按方向关系得到 0/1/2 档后 imul eax,本值（6.5/6.6 指令 0x004D2765，字节 6B C0 19），再按百分比追加；6.4 偷袭攻击走另一套按特效值的公式，不适用。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.5/6.6", 0x004D2767, 0xA3F67, 1,
                [0xB0, 0x02, 0x6B, 0xC0], [0x50, 0xFF, 0x75, 0x10, 0xE8, 0x68, 0x33, 0xF5, 0xFF, 0x01],
                Bases: ["6.5", "6.6"], Relocate: true)],
            ApplicableBases: ["6.5", "6.6"]),
        new("fixed-damage-basis", "固定增伤/减伤", "固定值基础加成", "点",
            "特效值为 1 时走固定值模式：加成 = 单位等级÷2 + 本值；增伤和减伤共用。6.5 默认 10，6.6 默认 15。",
            "函数 0x00448F53：确认增伤/减伤特效后，若特效值为 1 则取单位等级（单位+0x2C）÷2 再加本值；6.5 指令 0x00448F89/0x00448FB5 字节 83 C0 0A，6.6 同址 83 C0 0F。",
            EngineConstantKind.Byte, 0, 200,
            [new("6.5/6.6", 0x00448F8B, 0x4838B, 1,
                [0x8B, 0x45, 0xFC, 0xD1, 0xE8, 0x90, 0x83, 0xC0], [0x03, 0x45, 0x08, 0x50, 0x6A, 0x00],
                SecondaryFieldVa: 0x00448FB7, SecondaryFileOffset: 0x483B7,
                SecondaryPrefix: [0x8B, 0x45, 0xFC, 0xD1, 0xE8, 0x90, 0x83, 0xC0],
                SecondarySuffix: [0x8B, 0x4D, 0xF8, 0x2B, 0xC8, 0x83, 0xF9, 0x00],
                Bases: ["6.5", "6.6"], Relocate: true)],
            ApplicableBases: ["6.5", "6.6"]),
        new("strategy-floor-bonus", "策略保底/限伤", "策伤保底追加比例", "%",
            "策略伤害已经高于保底（或低于限伤）时，额外增加/扣减的百分比；默认 20%。",
            "函数 0x0043D3AE：保底分支 0x0043D3E9、限伤分支 0x0043D439 均 push 本值（字节 6A 14），再按 伤害×本值/100 增减；6.4/6.6 同址无这条公式。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.5", 0x0043D3EA, 0x3C7EA, 1,
                [0x39, 0x45, 0x08, 0x72, 0x12, 0x6A], [0xFF, 0x75, 0x08, 0xE8],
                SecondaryFieldVa: 0x0043D43A, SecondaryFileOffset: 0x3C83A,
                SecondaryPrefix: [0x39, 0x45, 0x08, 0x73, 0x10, 0x6A],
                SecondarySuffix: [0xFF, 0x75, 0x08, 0xE8], Bases: ["6.5"], Relocate: true)],
            ApplicableBases: ["6.5"]),
        new("mp-strategy-bonus", "MP辅助策略", "MP辅助策略基础加成", "%",
            "按剩余 MP 提升策略伤害时，在 MP 换算出的比例上再加这个固定百分比；默认 10%。",
            "函数 0x00435110：确认特效 212 后按 特效值×最大MP/100 得到比例，再 add eax,本值（6.6 指令 0x00435141，字节 83 C0 0A），最后乘伤害。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x00435143, 0x34543, 1,
                [0x21, 0xFD, 0xFF, 0x50, 0xE8, 0x98, 0x09, 0xFF, 0xFF, 0x83, 0xC0],
                [0xFF, 0x75, 0x08, 0x50, 0xE8], Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("money-defense-cost", "金钱防御", "金钱防御每点伤害消耗", "金",
            "金钱防御挡住伤害时，每 1 点伤害扣多少金钱；默认 10。钱不够就挡不住。",
            "函数 0x0042128A：确认特效 107 后把伤害值减 1 再 imul ×本值（0x004212C1 字节 6B C0 0A），与全局金钱 0x004B077C 比较后扣除。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x004212C3, 0x206C3, 1,
                [0x8B, 0x45, 0xF8, 0x48, 0x6B, 0xC0], [0xB9, 0x7C, 0x07, 0x4B, 0x00],
                Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("dodge-damage-cap", "化险为夷", "化险为夷最大伤害比例", "%",
            "化险为夷把一次伤害压到最多占最大 HP 的百分之几；默认 10%。",
            "函数 0x00449115：确认特效 206 且满足条件后，用 最大HP×本值/100 作为伤害上限（0x00449150 字节 6A 0A），超过就按上限结算。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x00449151, 0x48551, 1,
                [0x50, 0x6A], [0xE8, 0x82, 0xC9, 0xFD, 0xFF, 0x39, 0x45, 0x08, 0x77, 0x03],
                Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("offense-defense-add-line", "攻守兼备", "攻守兼备增伤触发 HP 线", "%",
            "攻守兼备：一方 HP 不低于这个百分比时，按特效值追加伤害；默认 40%。",
            "函数 0x00441E09：算 HP×100/最大HP 后与 0x28（40）比较（0x00441E38 字节 83 F8 28），达到就按特效值×伤害/100 增伤。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x00441E3A, 0x4123A, 1,
                [0x6B, 0xC0, 0x64, 0x33, 0xD2, 0xF7, 0xF9, 0x59, 0x83, 0xF8], [0x72, 0x0C],
                Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("offense-defense-effect-cap", "攻守兼备", "攻守兼备减伤效果值上限", "%",
            "攻守兼备减伤那一路，特效值超过这个数就按这个数算；默认100%。改小会限制减伤上限。",
            "函数 0x00441E09 第二段：call 0x00449199 取特效值后 cmp eax,100（0x00441E58），超过就 mov eax,100（0x00441E5D）；只作用于减伤那一路。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x00441E5A, 0x4125A, 1,
                [0x85, 0xC0, 0x74, 0x3B, 0x83, 0xF8], [0x76, 0x05, 0xB8],
                SecondaryFieldVa: 0x00441E5E, SecondaryFileOffset: 0x4125E,
                SecondaryPrefix: [0x76, 0x05, 0xB8],
                SecondarySuffix: [0x50, 0x8B, 0x4D, 0x0C, 0xE8, 0x24],
                SecondaryLength: 4, Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("offense-defense-reduce-line", "攻守兼备", "攻守兼备减伤触发 HP 线", "%",
            "攻守兼备：另一方 HP 不高于这个百分比时，按特效值削减伤害；默认 60%。",
            "函数 0x00441E09：算 HP×100/最大HP 后与 0x3C（60）比较（0x00441E82 字节 83 F8 3C），不超过就按特效值×伤害/100 减伤。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.6", 0x00441E84, 0x41284, 1,
                [0x6B, 0xC0, 0x64, 0x33, 0xD2, 0xF7, 0xF9, 0x59, 0x83, 0xF8], [0x77, 0x0C],
                Bases: ["6.6"], Relocate: true)],
            ApplicableBases: ["6.6"]),
        new("exploit-weakness-threshold", "趁虚攻击", "趁虚攻击虚弱阈值", "点",
            "统计 6 项能力中数值低于本阈值的项数，每低一项按特效值追加伤害；默认 3。6.5 同名特技为“落井下石”。",
            "函数 0x0043EA00（6.5 为 0x0043EA12）：循环 6 项能力，`cmp byte [单位+18h+索引],本值`，低于就计数，再 imul 特效值；6.5 立即数 0x0043EA40（文件 +0x3DE40），6.6 0x0043EA31（文件 +0x3DE31）。",
            EngineConstantKind.Byte, 0, 10,
            [
                new("6.5", 0x0043EA40, 0x3DE40, 1,
                    [0x83, 0xFA, 0x06, 0x73, 0x0D, 0x8B, 0x4D, 0x0C, 0x80, 0x7C, 0x11, 0x18],
                    [0x7D, 0x01, 0x40, 0xEB], Bases: ["6.5"], Relocate: true),
                new("6.6", 0x0043EA31, 0x3DE31, 1,
                    [0x83, 0xFA, 0x06, 0x73, 0x0D, 0x8B, 0x4D, 0x0C, 0x80, 0x7C, 0x11, 0x18],
                    [0x7D, 0x01, 0x40, 0xEB], Bases: ["6.6"], Relocate: true)
            ], ApplicableBases: ["6.5", "6.6"]),
        new("money-absorb-multiplier", "吸收金钱", "吸收金钱获得倍率", "倍",
            "吸收金钱结算时，按本次累计伤害 × 本值 计算金钱；6.4 默认 2 倍，6.5/6.6 默认 1 倍。改 0 就不结算金钱。",
            "特效 21 消费者 0x00406B3C：读累计伤害全局 0x0048E8BD 后执行 imul eax,本值（指令 0x00406BFD，字节 6B C0 ??），再按阵营结算全局金钱 0x004B077C（上限 999999）；三基底同址，6.4 立即数 2，6.5/6.6 为 1。",
            EngineConstantKind.Byte, 0, 10,
            [new("全部基底", 0x00406BFF, 0x5FFF, 1,
                [0xA1, 0xBD, 0xE8, 0x48, 0x00, 0x6B, 0xC0], [0xBA, 0x7C, 0x07, 0x4B, 0x00, 0x80, 0xF9, 0x02],
                Relocate: true)],
            ApplicableBases: ["6.4", "6.5", "6.6"]),
        new("fengfeng-floor-bonus", "神锋沥辉", "神锋沥辉保底加成", "%",
            "拥有神锋沥辉（6.5 同名特技为“削铁如泥”）时，按比例追加伤害的保底百分点；6.5 默认 10，6.6 默认 6。改 0 就只按计算值加成。",
            "特效 111 消费者 0x0042423D（6.4 同址为 nop）：读表值后 push 100/20、call 0x0040BAD4 除以 100/20，再 add eax,本值，最后按百分比追加伤害；6.5 字节 83 C0 0A，6.6 为 83 C0 06，前后 call 位移在签名里用掩码忽略。",
            EngineConstantKind.Byte, 0, 100,
            [new("6.5/6.6", 0x0042426A, 0x2366A, 1,
                [0x6A, 0x00, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x83, 0xC0],
                [0x50, 0xE8, 0x00, 0x00, 0x00, 0x00, 0x01, 0x45, 0x08],
                Bases: ["6.5", "6.6"], Relocate: true,
                PrefixMask: [0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01],
                SuffixMask: [0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01])],
            ApplicableBases: ["6.5", "6.6"]),
        new("shop-sell-price-numerator", "商店", "商店卖出价格比例分子", "倍（分母4）",
            "卖出价 = 买入价 × 本值 / 4；默认 3，即卖出价为买入价的 75%。分母固定 4，改本值可整体调整卖出比例。",
            "卖出价函数 0x0040B477：读道具价格字节 +12h 后 imul 100、imul 本值，再执行 cdq/and edx,3/add/sar 2（除以 4）；立即数 0x0040B48D（文件 +0xA88D）。三基底与信奈同址同值；本行只改分子，分母由 0x0040B490 与 0x0040B495 两处固定为 4。",
            EngineConstantKind.Byte, 0, 10,
            [new("全部基底", 0x0040B48D, 0xA88D, 1,
                [0x6B, 0xC0, 0x64, 0x6B, 0xC0],
                [0x99, 0x83, 0xE2, 0x03, 0x03, 0xC2, 0xC1, 0xF8, 0x02],
                Relocate: true)]),
        ..BattleFormulaConstantDefinitions.All
    ];

    public IReadOnlyList<EngineConstantValue> Read(ProjectWorkspace workspace)
    {
        ArgumentNullException.ThrowIfNull(workspace);
        var path = Path.Combine(workspace.RootPath, "Ekd5.exe");
        return Read(path, workspace.ActiveProfile.Profile.Version);
    }

    public IReadOnlyList<EngineConstantValue> Read(string exePath) => Read(exePath, null);

    /// <summary>
    /// Reads constants for one profile. When the address has drifted between engine
    /// variants, the instruction signature is relocated inside the executable section.
    /// </summary>
    public IReadOnlyList<EngineConstantValue> Read(string exePath, string? version)
    {
        var bytes = File.ReadAllBytes(exePath);
        var image = EngineEffectBinaryImage.Read(bytes);
        var result = new List<EngineConstantValue>(Definitions.Count);
        foreach (var definition in Definitions)
        {
            if (definition.Kind is EngineConstantKind.Byte or EngineConstantKind.Int32)
            {
                TryReadNumber(image, bytes, definition, version, out var byteValue);
                result.Add(byteValue!);
                continue;
            }
            var layout = definition.Layouts.FirstOrDefault(item => item.AppliesTo(version));
            if (layout == null)
            {
                result.Add(Unmatched(definition, NotApplicableText(definition)));
                continue;
            }
            if (layout.FieldFileOffset < 0 || layout.FieldFileOffset + layout.Length > bytes.LongLength)
            {
                result.Add(new(definition, layout, -1, null, string.Empty, [], false, "文本槽超出文件范围，只读。"));
                continue;
            }
            var textBytes = bytes.AsSpan(checked((int)layout.FieldFileOffset), layout.Length).ToArray();
            var text = DecodeText(textBytes, out var decodeError) ?? string.Empty;
            result.Add(new(definition, layout, layout.FieldFileOffset, null, text, textBytes, decodeError == null,
                decodeError ?? "固定文本槽，按 GBK 解码。"));
        }
        return result;
    }

    /// <summary>
    /// Diagnostic used by tests and support reports: shows whether each signature is
    /// unique enough to relocate after an engine variant shifts the code.
    /// </summary>
    public IReadOnlyList<EngineConstantRelocationCheck> ProbeRelocations(string exePath, string? version)
    {
        var bytes = File.ReadAllBytes(exePath);
        var image = EngineEffectBinaryImage.Read(bytes);
        var checks = new List<EngineConstantRelocationCheck>();

        void Add(EngineConstantDefinition definition, EngineConstantLayout layout, string label,
            uint fieldVa, byte[] prefix, byte[]? prefixMask, byte[] suffix, byte[]? suffixMask,
            int length, bool relative)
        {
            var applicable = layout.AppliesTo(version);
            if (applicable && relative)
            {
                if (ResolveFieldVa(image, bytes, layout, out _) is not { } resolved)
                {
                    checks.Add(new(definition.Id, label, true, layout.Relocate, false, 0, []));
                    return;
                }
                fieldVa = resolved;
            }
            var exact = applicable && fieldVa != 0 &&
                        MatchesAt(image, bytes, fieldVa, prefix, prefixMask, suffix, suffixMask, length, out _);
            var hits = applicable ? FindSignatureHits(image, prefix, prefixMask, suffix, suffixMask, length) : [];
            checks.Add(new(definition.Id, label, applicable, layout.Relocate, exact, hits.Count, hits, layout.Optional));
        }

        foreach (var definition in Definitions.Where(item => item.Kind is EngineConstantKind.Byte or EngineConstantKind.Int32))
        foreach (var layout in definition.Layouts)
        {
            Add(definition, layout, layout.Label, layout.FieldVa, layout.Prefix, layout.PrefixMask,
                layout.Suffix, layout.SuffixMask, layout.Length, layout.RelativePointerVa != 0);
            if (layout.SecondaryFieldVa != 0 && layout.SecondaryPrefix is { } secondaryPrefix &&
                layout.SecondarySuffix is { } secondarySuffix)
                Add(definition, layout, layout.Label + " 成对", layout.SecondaryFieldVa,
                    secondaryPrefix, layout.SecondaryPrefixMask, secondarySuffix, layout.SecondarySuffixMask,
                    SecondaryLengthOf(layout), false);
            if (layout.ExtraFields is { Count: > 0 } extras)
                foreach (var extra in extras)
                    Add(definition, layout, $"{layout.Label} 附加 0x{extra.FieldVa:X8}", extra.FieldVa,
                        extra.Prefix, extra.PrefixMask, extra.Suffix, extra.SuffixMask,
                        extra.Length > 0 ? extra.Length : layout.Length, false);
        }
        return checks;
    }

    /// <summary>
    /// Grows the bytes immediately before/after each constant until its signature
    /// is unique in the executable section. Used to replace short signatures that
    /// only work at the recorded address with relocatable contexts.
    /// </summary>
    public IReadOnlyList<EngineConstantContextSuggestion> SuggestContexts(string exePath, string? version)
    {
        var bytes = File.ReadAllBytes(exePath);
        var image = EngineEffectBinaryImage.Read(bytes);
        var suggestions = new List<EngineConstantContextSuggestion>();

        void Add(EngineConstantDefinition definition, string label, uint fieldVa,
            byte[] prefix, byte[] suffix, int length)
        {
            if (fieldVa == 0) return;
            if (!MatchesAt(image, bytes, fieldVa, prefix, null, suffix, null, length, out var offset)) return;
            var section = image.SectionOf(fieldVa);
            if (section is not { IsExecutable: true }) return; // 数据段槽位不做代码段上下文扩展。
            var start = Math.Max(0L, section.RawPointer);
            var end = Math.Min(bytes.LongLength, section.RawPointer + section.RawSize);
            var leftLimit = checked((int)Math.Min(32L, offset - start));
            var rightLimit = checked((int)Math.Min(32L, Math.Min(end, bytes.LongLength) - offset - length));
            var bestHits = FindSignatureHits(image, prefix, null, suffix, null, length).Count;
            var bestPrefix = prefix;
            var bestSuffix = suffix;
            var bestAddress = fieldVa;
            for (var extra = 0; extra <= leftLimit + rightLimit; extra++)
            {
                var left = Math.Min(leftLimit, prefix.Length + extra / 2);
                var right = Math.Min(rightLimit, suffix.Length + extra - left + prefix.Length);
                if (left < prefix.Length || right < suffix.Length) continue;
                var candidatePrefix = bytes.AsSpan(checked((int)offset) - left, left).ToArray();
                var candidateSuffix = bytes.AsSpan(checked((int)offset) + length, right).ToArray();
                var hits = FindSignatureHits(image, candidatePrefix, null, candidateSuffix, null, length);
                if (hits.Count != 1) continue;
                bestHits = 1;
                bestPrefix = candidatePrefix;
                bestSuffix = candidateSuffix;
                bestAddress = hits[0];
                break;
            }
            suggestions.Add(new(definition.Id, label, bestPrefix, bestSuffix, bestHits,
                bestAddress, bestHits == 1));
        }

        foreach (var definition in Definitions.Where(item => item.Kind is EngineConstantKind.Byte or EngineConstantKind.Int32))
        foreach (var layout in definition.Layouts.Where(item => item.AppliesTo(version)))
        {
            Add(definition, layout.Label, layout.FieldVa, layout.Prefix, layout.Suffix, layout.Length);
            if (layout.SecondaryFieldVa != 0 && layout.SecondaryPrefix is { } secondaryPrefix &&
                layout.SecondarySuffix is { } secondarySuffix)
                Add(definition, layout.Label + " 成对", layout.SecondaryFieldVa,
                    secondaryPrefix, secondarySuffix, SecondaryLengthOf(layout));
        }
        return suggestions;
    }

    private static bool TryReadNumber(EngineEffectBinaryImage image, byte[] bytes,
        EngineConstantDefinition definition, string? version, out EngineConstantValue? value)
    {
        value = null;
        var applicable = definition.Layouts.Where(layout => layout.AppliesTo(version)).ToArray();
        if (applicable.Length == 0)
        {
            value = Unmatched(definition, NotApplicableText(definition));
            return false;
        }
        var failures = new List<string>();
        // Pass 1: exact address + signature. This prevents a short signature in
        // the wrong base layout from being mistaken for a relocated constant.
        foreach (var layout in applicable)
        {
            if (!TryMatchLayout(image, bytes, definition, layout, relocate: false, out var match, out var diagnostic))
            {
                if (diagnostic != null) failures.Add(diagnostic);
                continue;
            }
            value = match!;
            return true;
        }
        // Pass 2: only layouts that declare a unique signature may be relocated.
        foreach (var layout in applicable.Where(item => item.Relocate))
        {
            if (!TryMatchLayout(image, bytes, definition, layout, relocate: true, out var match, out var diagnostic))
            {
                if (diagnostic != null) failures.Add(diagnostic);
                continue;
            }
            value = match!;
            return true;
        }
        value = Unmatched(definition, failures.Count > 0
            ? string.Join("；", failures.Distinct(StringComparer.Ordinal))
            : "指令签名不匹配，保持只读。");
        return false;
    }

    private static bool TryMatchLayout(EngineEffectBinaryImage image, byte[] bytes,
        EngineConstantDefinition definition, EngineConstantLayout layout, bool relocate,
        out EngineConstantValue? value, out string? diagnostic)
    {
        value = null;
        uint fieldVa;
        if (ResolveFieldVa(image, bytes, layout, out var relativeDiagnostic) is { } resolved)
            fieldVa = resolved;
        else if (relocate)
            fieldVa = layout.FieldVa; // 指针槽本身搬家时，退回记录地址再按唯一签名找回。
        else
        {
            diagnostic = relativeDiagnostic;
            return false;
        }
        if (!TryResolveField(image, bytes, fieldVa, layout.Prefix, layout.PrefixMask, layout.Suffix, layout.SuffixMask,
                layout.Length, relocate, out var offset, out string? signatureDiagnostic))
        {
            diagnostic = relativeDiagnostic ?? signatureDiagnostic;
            return false;
        }
        diagnostic = signatureDiagnostic ?? relativeDiagnostic;
        var original = bytes.AsSpan(checked((int)offset), layout.Length).ToArray();
        var number = layout.Length == 1 ? original[0] : BitConverter.ToInt32(original, 0);
        if (signatureDiagnostic != null && (number < definition.Minimum || number > definition.Maximum))
        {
            diagnostic = $"重定位值 {number} 超出范围 {definition.Minimum}..{definition.Maximum}，保持只读。";
            return false;
        }
        long secondaryOffset = -1;
        if (layout.SecondaryFieldVa != 0)
        {
            if (layout.SecondaryPrefix is not { } secondaryPrefix || layout.SecondarySuffix is not { } secondarySuffix)
                return false;
            var secondaryLength = SecondaryLengthOf(layout);
            // 成对字段必须和主字段在同一段代码里：主字段搬家后按相对位移取成对地址，
            // 不再各自搜索签名，避免把另一个函数里数值恰好相同的字段配成一对。
            if (image.FileOffsetToVirtualAddress(offset) is not { } primaryVa)
            {
                diagnostic = "成对字段无法换算代码地址，保持只读。";
                return false;
            }
            var target = (long)primaryVa + (long)layout.SecondaryFieldVa - layout.FieldVa;
            if (target <= 0 || target > uint.MaxValue)
            {
                diagnostic = "成对字段地址超出范围，保持只读。";
                return false;
            }
            if (!TryResolveField(image, bytes, (uint)target, secondaryPrefix,
                    layout.SecondaryPrefixMask, secondarySuffix, layout.SecondarySuffixMask, secondaryLength,
                    relocate: false, out var secondary, out var secondaryDiagnostic))
            {
                diagnostic = secondaryDiagnostic ?? "成对字段签名不匹配，保持只读。";
                return false;
            }
            var secondaryBytes = bytes.AsSpan(checked((int)secondary), secondaryLength).ToArray();
            var secondaryNumber = secondaryLength == 1 ? secondaryBytes[0] : BitConverter.ToInt32(secondaryBytes, 0);
            if (number != secondaryNumber)
            {
                diagnostic = "成对地址的值不一致，保持只读。";
                return false;
            }
            secondaryOffset = secondary;
        }
        List<long>? extraOffsets = null;
        if (layout.ExtraFields is { Count: > 0 } extras)
        {
            extraOffsets = new List<long>(extras.Count);
            foreach (var extra in extras)
            {
                var extraLength = extra.Length > 0 ? extra.Length : layout.Length;
                // 附加同值字段同样按主字段的相对位移定位，防止在别的函数里误配。
                if (image.FileOffsetToVirtualAddress(offset) is not { } extraBaseVa)
                {
                    diagnostic = "附加同步字段无法换算代码地址，保持只读。";
                    return false;
                }
                var extraTarget = (long)extraBaseVa + (long)extra.FieldVa - layout.FieldVa;
                if (extraTarget <= 0 || extraTarget > uint.MaxValue)
                {
                    diagnostic = "附加同步字段地址超出范围，保持只读。";
                    return false;
                }
                if (!TryResolveField(image, bytes, (uint)extraTarget, extra.Prefix, extra.PrefixMask, extra.Suffix,
                        extra.SuffixMask, extraLength, relocate: false, out var extraOffset, out var extraDiagnostic))
                {
                    diagnostic = extraDiagnostic ?? "附加同步字段签名不匹配，保持只读。";
                    return false;
                }
                var extraBytes = bytes.AsSpan(checked((int)extraOffset), extraLength).ToArray();
                var extraNumber = extraLength == 1 ? extraBytes[0] : BitConverter.ToInt32(extraBytes, 0);
                if (extraNumber != number)
                {
                    diagnostic = "附加同步字段的值不一致，保持只读。";
                    return false;
                }
                extraOffsets.Add(extraOffset);
            }
        }
        value = new(definition, layout, offset, number, number.ToString(), original, true,
            diagnostic ?? relativeDiagnostic ?? "指令签名匹配（" + layout.Label + "）。", secondaryOffset,
            extraOffsets);
        return true;
    }

    private static int SecondaryLengthOf(EngineConstantLayout layout)
        => layout.SecondaryLength > 0 ? layout.SecondaryLength : layout.Length;

    private static byte[] EncodeNumber(int numeric, int length)
        => length == 1 ? [(byte)numeric] : BitConverter.GetBytes(numeric);

    private static uint? ResolveFieldVa(EngineEffectBinaryImage image, byte[] bytes,
        EngineConstantLayout layout, out string? diagnostic)
    {
        diagnostic = null;
        if (layout.RelativePointerVa == 0) return layout.FieldVa;
        if (image.VirtualAddressToFileOffset(layout.RelativePointerVa) is not { } pointerOffset ||
            pointerOffset < 0 || pointerOffset + 4 > bytes.LongLength)
        {
            diagnostic = "特效表指针槽超出文件范围，保持只读。";
            return null;
        }
        var tableBase = BitConverter.ToUInt32(bytes, checked((int)pointerOffset));
        if (image.SectionOf(tableBase) == null)
        {
            diagnostic = $"特效表指针值 0x{tableBase:X8} 不在文件节内，保持只读。";
            return null;
        }
        diagnostic = $"按特效表指针 0x{layout.RelativePointerVa:X8}→0x{tableBase:X8} 相对定位（行偏移 +0x{layout.RelativeOffset:X}）。";
        return tableBase + layout.RelativeOffset;
    }

    private static bool TryResolveField(EngineEffectBinaryImage image, byte[] bytes, uint expectedVa,
        byte[] prefix, byte[]? prefixMask, byte[] suffix, byte[]? suffixMask, int length, bool relocate,
        out long offset, out string? diagnostic)
    {
        offset = -1;
        diagnostic = null;
        if (expectedVa != 0 && MatchesAt(image, bytes, expectedVa, prefix, prefixMask, suffix, suffixMask,
                length, out offset))
        {
            diagnostic = null;
            return true;
        }
        if (!relocate) return false;
        var hits = FindSignatureHits(image, prefix, prefixMask, suffix, suffixMask, length);
        if (hits.Count != 1)
        {
            diagnostic = hits.Count > 1
                ? $"指令签名不唯一（{hits.Count} 处），保持只读。"
                : "指令签名不匹配，保持只读。";
            return false;
        }
        if (image.VirtualAddressToFileOffset(hits[0]) is not { } relocated) return false;
        offset = relocated;
        diagnostic = $"原地址 0x{expectedVa:X8} 已偏移，按指令签名定位到 0x{hits[0]:X8}。";
        return true;
    }

    private static bool MatchesAt(EngineEffectBinaryImage image, byte[] bytes, uint virtualAddress,
        byte[] prefix, byte[]? prefixMask, byte[] suffix, byte[]? suffixMask, int length, out long offset)
    {
        offset = -1;
        if (image.VirtualAddressToFileOffset(virtualAddress) is not { } fileOffset ||
            fileOffset < prefix.Length ||
            fileOffset + length + suffix.Length > bytes.LongLength) return false;
        var index = checked((int)fileOffset);
        if (!SignatureBytesMatch(bytes.AsSpan(index - prefix.Length, prefix.Length), prefix, prefixMask) ||
            !SignatureBytesMatch(bytes.AsSpan(index + length, suffix.Length), suffix, suffixMask)) return false;
        offset = fileOffset;
        return true;
    }

    /// <summary>Mask byte 0 means wildcard; any other value requires an exact match.</summary>
    private static bool SignatureBytesMatch(ReadOnlySpan<byte> actual, byte[] pattern, byte[]? mask)
    {
        if (mask is { } && mask.Length != pattern.Length) return false;
        for (var index = 0; index < pattern.Length; index++)
            if ((mask is null || mask[index] != 0) && actual[index] != pattern[index]) return false;
        return true;
    }

    /// <summary>
    /// Scans executable sections for prefix + wildcard immediate + suffix. The hit is
    /// the immediate VA, so a layout stays valid when an engine variant moves the code.
    /// </summary>
    private static IReadOnlyList<uint> FindSignatureHits(EngineEffectBinaryImage image,
        byte[] prefix, byte[]? prefixMask, byte[] suffix, byte[]? suffixMask, int length)
    {
        if (prefix.Length == 0 && suffix.Length == 0) return [];
        var total = prefix.Length + length + suffix.Length;
        var hits = new List<uint>();
        foreach (var section in image.ExecutableSections)
        {
            var size = (int)Math.Min(section.RawSize, int.MaxValue);
            var blob = image.ReadBytes(section.RawPointer, size);
            if (blob == null || blob.Length < total) continue;
            for (var index = 0; index + total <= blob.Length; index++)
            {
                if (!SignatureBytesMatch(blob.AsSpan(index, prefix.Length), prefix, prefixMask) ||
                    !SignatureBytesMatch(blob.AsSpan(index + prefix.Length + length, suffix.Length), suffix,
                        suffixMask)) continue;
                var address = section.VirtualAddress + (uint)index + (uint)prefix.Length;
                if (!hits.Contains(address)) hits.Add(address);
            }
        }
        return hits;
    }

    private static string NotApplicableText(EngineConstantDefinition definition)
    {
        if (definition.ApplicableBases is { } declared)
            return $"此常量只适用于 {string.Join("/", declared)}，当前基底不适用。";
        var bases = definition.Layouts.SelectMany(layout => layout.Bases ?? []).Distinct(StringComparer.Ordinal).ToArray();
        return bases.Length > 0
            ? $"此常量只适用于 {string.Join("/", bases)}，当前基底不适用。"
            : "指令签名不匹配，保持只读。";
    }

    private static EngineConstantValue Unmatched(EngineConstantDefinition definition, string diagnostic)
        => new(definition, definition.Layouts[0], -1, null, string.Empty, [], false, diagnostic);

    public EngineConstantCommitResult Commit(ProjectWorkspace workspace, IReadOnlyList<EngineConstantEdit> edits)
    {
        ArgumentNullException.ThrowIfNull(workspace);
        if (edits.Count == 0) return EngineConstantCommitResult.Failed("没有修改。");
        var path = Path.Combine(workspace.RootPath, "Ekd5.exe");
        if (!File.Exists(path)) return EngineConstantCommitResult.Failed("找不到 Ekd5.exe。");
        var before = File.ReadAllBytes(path);
        var after = (byte[])before.Clone();
        var version = workspace.ActiveProfile.Profile.Version;
        var current = Read(path, version).ToDictionary(value => value.Definition.Id, StringComparer.Ordinal);
        var changes = new List<string>();
        var expected = new List<(EngineConstantDefinition Definition, int? Numeric, string? Text)>();
        foreach (var edit in edits)
        {
            if (!current.TryGetValue(edit.Id, out var value))
                return EngineConstantCommitResult.Failed($"未知常量：{edit.Id}");
            if (!value.SignatureMatches)
                return EngineConstantCommitResult.Failed($"{value.Definition.DisplayName}：{value.Diagnostic}");
            var definition = value.Definition;
            if (definition.Kind is EngineConstantKind.Byte or EngineConstantKind.Int32)
            {
                if (edit.NumericValue is not { } numeric || numeric < definition.Minimum || numeric > definition.Maximum)
                    return EngineConstantCommitResult.Failed(
                        $"{definition.DisplayName}：请输入 {definition.Minimum}..{definition.Maximum}。");
                if (value.NumericValue == numeric) continue;
                var encoded = EncodeNumber(numeric, value.Layout.Length);
                encoded.CopyTo(after, checked((int)value.FileOffset));
                if (value.SecondaryFileOffset >= 0)
                    EncodeNumber(numeric, SecondaryLengthOf(value.Layout))
                        .CopyTo(after, checked((int)value.SecondaryFileOffset));
                if (value.ExtraFileOffsets is { Count: > 0 } extraOffsets)
                {
                    var extraEncoded = EncodeNumber(numeric, value.Layout.Length);
                    foreach (var extraOffset in extraOffsets)
                        extraEncoded.CopyTo(after, checked((int)extraOffset));
                }
                changes.Add($"{definition.DisplayName} {value.NumericValue} → {numeric}");
                expected.Add((definition, numeric, null));
            }
            else
            {
                var text = (edit.TextValue ?? string.Empty).Trim();
                var encoded = EncodeText(text, value.Layout.Length);
                if (encoded == null)
                    return EngineConstantCommitResult.Failed(
                        $"{definition.DisplayName}：最多 {value.Layout.Length} 字节 GBK（约 8 个汉字）。");
                var slot = new byte[value.Layout.Length];
                encoded.CopyTo(slot, 0);
                if (after.AsSpan(checked((int)value.FileOffset), value.Layout.Length).SequenceEqual(slot)) continue;
                slot.CopyTo(after, checked((int)value.FileOffset));
                changes.Add($"{definition.DisplayName} \"{value.TextValue}\" → \"{text}\"");
                expected.Add((definition, null, text));
            }
        }
        if (changes.Count == 0) return new(true, "没有需要写入的常量。");
        var candidate = new WorkspaceBinaryCandidate(path, before, after, "引擎常量");
        var result = new EngineEffectTransactionService().Commit(workspace,
            "写入引擎常量：" + string.Join("、", changes), [candidate], () =>
        {
            var verify = Read(path, version).ToDictionary(item => item.Definition.Id, StringComparer.Ordinal);
            foreach (var (definition, numeric, text) in expected)
            {
                if (!verify.TryGetValue(definition.Id, out var actual))
                    throw new InvalidDataException($"{definition.DisplayName} 复读不到。");
                if (numeric is { } number && actual.NumericValue != number)
                    throw new InvalidDataException($"{definition.DisplayName} 复读值 {actual.NumericValue} 与写入 {number} 不符。");
                if (text != null && !actual.TextValue.Equals(text, StringComparison.Ordinal))
                    throw new InvalidDataException($"{definition.DisplayName} 复读文本与写入不符。");
            }
        });
        return new(result.Success, result.Message, result.BackupPath, changes.Count);
    }

    private static string? DecodeText(ReadOnlySpan<byte> bytes, out string? error)
    {
        try
        {
            var strict = Encoding.GetEncoding(936, EncoderFallback.ExceptionFallback, DecoderFallback.ExceptionFallback);
            error = null;
            return strict.GetString(bytes).TrimEnd('\0');
        }
        catch (DecoderFallbackException)
        {
            error = "文本槽不是有效 GBK，保持只读。";
            return null;
        }
        catch (ArgumentException)
        {
            error = "当前系统缺少 GBK 代码页。";
            return null;
        }
    }

    private static byte[]? EncodeText(string text, int length)
    {
        try
        {
            var strict = Encoding.GetEncoding(936, EncoderFallback.ExceptionFallback, DecoderFallback.ExceptionFallback);
            var bytes = strict.GetBytes(text);
            return bytes.Length <= length ? bytes : null;
        }
        catch (EncoderFallbackException) { return null; }
        catch (ArgumentException) { return null; }
    }
}
