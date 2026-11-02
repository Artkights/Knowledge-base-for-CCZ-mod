using System.Globalization;
using System.Text.RegularExpressions;
using DataManager.Core.Editing;

namespace DataManager.Core.Scanner;

/// <summary>公式计算过程的一步；Expression 里的 {常量ID} 会替换成当前值。</summary>
public sealed record BattleFormulaStep(int Index, string Title, string Expression, string Note);

/// <summary>战斗公式里的一项常量；有关联常量时可在公式页直接修改。</summary>
public sealed record BattleFormulaConstant(string Name, string Role, string Value64, string Value65,
    string Value66, string? ConstantId, string Location, string Note)
{
    public bool Linked => !string.IsNullOrWhiteSpace(ConstantId);
}

/// <summary>一条战斗公式：三基底的数值表现、通俗说明和证据。</summary>
public sealed record BattleFormulaDefinition(string Id, string Category, string DisplayName,
    string Value64, string Value65, string Value66, string Description, string Detail, string Evidence,
    IReadOnlyList<BattleFormulaConstant> Constants);

public sealed record BattleFormulaConstantValue(BattleFormulaConstant Constant, string CurrentValue,
    bool Editable, string Status, string Range, bool Shared, string Diagnostic);

public sealed record BattleFormulaValue(BattleFormulaDefinition Definition,
    IReadOnlyList<BattleFormulaStep> Steps,
    IReadOnlyList<BattleFormulaConstantValue> Constants)
{
    public int EditableCount => Constants.Count(item => item.Editable);
}

public sealed record BattleFormulaEdit(string ConstantId, int Value);

public enum BattleFormulaIssueSeverity { Error, Warning }

public sealed record BattleFormulaValidationIssue(string ConstantId, string ConstantName,
    string FormulaId, BattleFormulaIssueSeverity Severity, string Message);

public sealed record BattleFormulaCommitResult(bool Success, string Message, string? BackupPath = null,
    int ChangedCount = 0, IReadOnlyList<BattleFormulaValidationIssue>? Issues = null);

/// <summary>三基底战斗公式清单；数值常量与常量页共享同一份读取结果。</summary>
public sealed class EngineBattleFormulaService
{
    private static BattleFormulaConstant Fixed(string name, string role, string value64, string value65,
        string value66, string location, string note = "公式结构值") =>
        new(name, role, value64, value65, value66, null, location, note);

    private static BattleFormulaConstant Link(string name, string role, string constantId,
        string value64, string value65, string value66, string location) =>
        new(name, role, value64, value65, value66, constantId, location, "可在本页直接修改");

    private static readonly BattleFormulaConstant[] HitCurveConstants =
    [
        Fixed("满命中倍率", "攻方 ≥ 守方×2 直接满命中", "2", "2", "2",
            "曲线函数 0x0043B50C / 0x0043B53A 的 shl edx,1", "指令编码，只读"),
        Link("高段基础", "1～2 倍区间的起点", "hit-curve-high-base", "90", "90", "90",
            "6.4 0x0043B53D；6.5/6.6 0x0043B56B"),
        Link("高段系数", "1～2 倍区间每差 1 点加多少", "hit-curve-high-coef", "10", "10", "10",
            "6.4 0x0043B535；6.5/6.6 0x0043B563"),
        Link("中段基础", "1/2～1 倍区间的起点", "hit-curve-mid-base", "60", "60", "60",
            "6.4 0x0043B55E；6.5/6.6 0x0043B58C"),
        Link("中段系数", "1/2～1 倍区间每差 1 点加多少", "hit-curve-mid-coef", "30", "30", "30",
            "6.4 0x0043B556；6.5/6.6 0x0043B584"),
        Link("低段除数", "低于一半时先除以几", "hit-curve-low-divisor", "3", "3", "3",
            "6.4 0x0043B567；6.5/6.6 0x0043B595"),
        Link("低段基础", "低于一半时的起点", "hit-curve-low-base", "30", "30", "30",
            "6.4 0x0043B584；6.5/6.6 0x0043B5B2"),
        Link("低段系数", "低于一半时每差 1 点加多少", "hit-curve-low-coef", "30", "30", "30",
            "6.4 0x0043B57C；6.5/6.6 0x0043B5AA"),
        Link("命中上限", "最高命中率", "hit-curve-cap", "100", "100", "100",
            "6.4 0x0043B51C；6.5/6.6 0x0043B54A"),
        Link("6.6 命中下限", "6.6 判定入口的最低命中率", "hit-curve-floor-66", "—", "—", "25",
            "6.6 0x0043B4E0 cmp、0x0043B4E4 mov，成对写入")
    ];

    private static readonly BattleFormulaConstant[] HitRetryConstants =
    [
        Link("二次判定阈值", "命中率达到多少才允许再判一次", "hit-retry-threshold", "85", "85", "—",
            "6.4 0x0043B4FD；6.5 0x0043B528"),
        Link("二次判定扣减", "再判一次时命中率扣多少", "hit-retry-deduction", "10", "10", "—",
            "6.4 0x0043B503；6.5 0x0043B52E"),
        Link("最多判定次数", "最多判几次", "hit-retry-count", "2", "2", "—",
            "6.4 0x0043B4E9；6.5 0x0043B50A"),
        Link("6.6 命中下限", "6.6 判定入口的最低命中率", "hit-curve-floor-66", "—", "—", "25",
            "6.6 0x0043B4E0 / 0x0043B4E4")
    ];

    private static readonly BattleFormulaConstant[] RateCurveConstants =
    [
        Link("满率倍率", "攻方能力达到守方几倍就必发动", "rate-curve-full-multiplier", "3", "3", "3",
            "0x00405D14 imul ecx,3"),
        Fixed("高段倍率", "高段的守方基准倍数", "2", "2", "2",
            "0x00405D21 shl ecx,1", "指令编码，只读"),
        Link("高段系数", "2～3 倍区间每差 1 点加多少", "rate-curve-high-coef", "80", "80", "80",
            "0x00405D2F imul eax,50h"),
        Link("高段基础", "2～3 倍区间的起点", "rate-curve-high-base", "20", "20", "20",
            "0x00405D37 add eax,14h"),
        Link("低段系数", "1～2 倍区间每差 1 点加多少", "rate-curve-low-coef", "18", "18", "18",
            "0x00405D47 imul eax,12h"),
        Link("低段基础", "1～2 倍区间的起点", "rate-curve-low-base", "2", "2", "2",
            "0x00405D4F add eax,2"),
        Fixed("最低发动率", "攻方低于守方时的基础值", "1", "1", "1",
            "0x00405D52 xor eax,eax; inc eax", "指令编码，只读"),
        Link("发动率上限", "最高发动率", "rate-curve-cap", "100", "100", "100",
            "0x00405D1B mov al,64h")
    ];

    private static readonly BattleFormulaConstant[] PersonalExpConstants =
    [
        Fixed("等级差下限", "守方低于攻方多少级仍按 -1 计算", "-1", "-1", "-1",
            "0x00403846 cmp al,0FFh（立即数 0x00403847）；0x0040384A mov al,0FFh", "指令编码，只读"),
        Fixed("等级差上限", "守方高于攻方多少级后封顶", "47", "47", "47",
            "0x0040384C cmp al,2Fh（立即数 0x0040384D）；0x00403850 mov al,2Fh", "指令编码，只读"),
        Link("基础经验值", "每次攻击的基础经验", "personal-exp-base", "6", "6", "6",
            "0x00403855 lea ecx,[eax+eax+6]"),
        Link("击杀固定加成", "击杀 0x496C96 指定目标时额外加多少", "personal-exp-kill-flat",
            "48", "48", "48", "6.4/6.5 0x00403824；6.6 0x0040381E"),
        Link("击杀经验分子", "普通击杀经验的分子", "personal-exp-kill-ratio-num", "64", "64", "64",
            "6.4/6.5 0x0040383A；6.6 0x00403833"),
        Link("击杀除数偏移", "除数 = max(攻方−守方,0)+本值", "personal-exp-kill-ratio-offset",
            "2", "2", "2", "6.4/6.5 0x00403834；6.6 0x0040382E"),
        Link("经验倍率基础", "倍率 = (第8项能力+本值)/100", "exp-multiplier-base",
            "100", "100", "100", "0x00407FB9 add eax,64h"),
        Fixed("击杀判定来源", "ctx+0x84+索引×4（攻击前HP）与 0x41B500 当前 HP 比较，≥ 视为击杀", "ctx+0x84",
            "ctx+0x84", "ctx+0x84",
            "0x004037EF cmp dword [ctx+edx*4+84h],eax；0x0041B500 mov eax,[ecx+10h]；6.6 额外守卫 0x0040383B cmp dword [ebp-0Ch],0; je 0x0040386A", "公式输入，只读"),
        Fixed("特殊目标来源", "由战场变量装载 0x4122C1 从剧本变量 0x02 写入 0x496C96", "0x496C96",
            "0x496C96", "0x496C96", "0x00406604 movzx eax,word [ecx+3D06]；ecx=0x492F90", "公式输入，只读"),
        Fixed("同行动取最大", "多次攻击只累计最高一次", "取最大值", "取最大值", "取最大值",
            "0x00406043 mov [ctx+428],max", "公式输入，只读"),
        Fixed("道具增加经验", "道具效果 0x26：当前经验 + 道具效果值", "0x0041CD4D", "0x0041CD4D", "0x0041CD4D",
            "0x0041CD30 call 0x004065C7；0x0041CD4D call 0x004088CD", "公式计算，只读"),
        Fixed("道具效果值", "道具记录 +0x15 的 WORD", "item+15", "item+15", "item+15",
            "0x0041DD75 movzx eax,byte [ecx+15h]；0x0041DD7D movzx ecx,word [ecx+15h]", "公式输入，只读")
    ];

    private static readonly BattleFormulaConstant[] WeaponExpConstants =
    [
        Link("武器经验基础值", "造成伤害时每次加多少", "weapon-exp-base", "3", "2", "3",
            "0x004038FA mov cl,本值"),
        Fixed("攻方等级高", "攻方等级高于守方时 -1", "-1", "-1", "-1",
            "0x00403903 dec ecx", "指令编码，只读"),
        Fixed("暴击加成", "暴击时 +1", "+1", "+1", "+1",
            "0x00403910 inc ecx；0x00405F1A 置 ctx+604=1", "指令编码，只读"),
        Link("无伤害值", "未造成 HP/MP 伤害时取本值", "weapon-exp-no-damage", "2", "2", "1",
            "0x00403919 mov byte [ebp-4],本值（实际指令 0x00403916）；判定需 ctx+84h 与 ctx+254h 两项都为 0"),
        Fixed("武器类型门控", "6.4：0x4067CE(武器) 为 0 或 0xA 才计经验；6.5/6.6 该判断被 jmp 短路（任意类型都计）", "0/0xA",
            "0/0xA", "0/0xA",
            "6.4 0x004038D9 je 0x004038DF；6.5/6.6 0x004038D9 jmp 0x004038DF（0x004038DB cmp al,0Ah 成死代码）；前置 0x0041DE1D(id,18h) = (0x43AD29(道具) != 18h)", "公式输入，只读"),
        Link("经验倍率基础", "倍率 = (第8项能力+本值)/100", "exp-multiplier-base",
            "100", "100", "100", "0x00407FB9"),
        Fixed("结算累加", "累加到 ctx+42C", "累加", "累加", "累加",
            "0x00406054 add [ctx+42C],eax", "公式输入，只读")
    ];

    private static readonly BattleFormulaConstant[] ArmorExpConstants =
    [
        Link("防具经验基础值", "每件防具的基础经验", "armor-exp-base", "3", "3", "4",
            "0x00403A8D push 本值"),
        Fixed("攻方等级低", "攻方等级低于守方时 -1", "-1", "-1", "-1",
            "0x00403AF3 dec dword [ebp-4]", "指令编码，只读"),
        Link("无伤害扣减", "未造成 HP/MP 伤害时从基础上扣多少", "armor-exp-no-damage",
            "1", "2", "3", "0x00403AF8 sub dword [ebp-4],本值；判定需 ctx+84h 与 ctx+254h 两项都为 0"),
        Fixed("目标阵营门控", "0x43FF54(守方单位) = (byte[unit+5] != 0)，即只对非我军目标计防具经验", "非我军",
            "非我军", "非我军",
            "0x00403AC8 call 0x0043FF54；0x00403ACF je 0x00403B0E；0x0043FF57 movzx ecx,byte [ecx+5]（neg/sbb/inc 惯用式）", "公式输入，只读"),
        Link("经验倍率基础", "倍率 = (第8项能力+本值)/100", "exp-multiplier-base",
            "100", "100", "100", "0x00407FB9"),
        Fixed("结算写入", "按防具槽写入 ctx+430", "按槽写入", "按槽写入", "按槽写入",
            "0x00406074 mov [ctx+slot*4+430],eax", "公式输入，只读")
    ];

    private static readonly BattleFormulaConstant[] ExpMultiplierConstants =
    [
        Link("倍率基础值", "倍率 = (第8项能力+本值)/100", "exp-multiplier-base",
            "100", "100", "100", "0x00407FB9 add eax,64h"),
        Fixed("倍率来源能力", "角色第 8 项基础能力", "第8项", "第8项", "第8项",
            "0x00407FAD push 8；0x00407FAF call 0x00407C35（6.6 0x00407C29）", "公式输入，只读"),
        Fixed("翻倍条件一", "攻方为我军且 0x501B00[槽位] 非 0", "×2", "×2", "×2",
            "0x00403D60 call 0x0042545F；0x00425470 add edx,0x501B00", "公式输入，只读"),
        Fixed("翻倍条件二", "全局字节 0x500E9A == 1", "×2", "×2", "×2",
            "0x00403D6C cmp byte [0x500E9A],1", "公式输入，只读"),
        Fixed("百分比计算", "经验×百分比÷100", "÷100", "÷100", "÷100",
            "0x00425AD9 imul eax,[ebp+8]; div 100", "公式输入，只读")
    ];

    private static readonly BattleFormulaConstant[] StrategyExpConstants =
    [
        Fixed("策略类型字段", "策略记录 +0x0B：2=固定加成，1=普通档，其他=伤害判定",
            "0/1/2", "0/1/2", "0/1/2", "0x00425AC7 movzx eax,byte [ecx+0Bh]", "公式输入，只读"),
        Fixed("类型2固定经验", "类型 2 直接加多少", "20", "20", "20",
            "6.4/6.5 0x00420F25；6.6 0x00420F19 add 14h", "指令编码，只读"),
        Fixed("击杀档·每级", "攻方低于守方时每级加多少", "8", "8", "8",
            "6.4/6.5 0x00420FB5 lea eax,[eax*8+20h]；6.6 0x00420FA7", "指令编码，只读"),
        Fixed("击杀档·基础", "击杀经验基础值", "32", "32", "32",
            "6.4/6.5 0x00420FB5、0x00420FCA；6.6 0x00420FA7、0x00420FC0", "指令编码，只读"),
        Fixed("击杀档·上限", "击杀经验封顶", "200", "200", "200",
            "6.4/6.5 0x00420FBC；6.6 0x00420FAE", "指令编码，只读"),
        Fixed("击杀档·高等级每级扣", "攻方高于守方时每级扣多少", "4", "4", "4",
            "6.4/6.5 0x00420FCD shl edx,2；6.6 0x00420FBC shl eax,2", "指令编码，只读"),
        Fixed("击杀档·最低", "高等级时最少给多少", "10", "10", "10",
            "6.4/6.5 0x00420FDE；6.6 0x00420FCA", "指令编码，只读"),
        Fixed("普通档·每级", "攻方低于守方时每级加多少", "4", "4", "4",
            "6.4/6.5 0x00421001 lea eax,[eax*4+0Ah]；6.6 0x00421001", "指令编码，只读"),
        Fixed("普通档·基础", "普通经验基础值", "10", "10", "10",
            "6.4/6.5 0x00421001、0x00421024；6.6 0x00421001、0x00421015", "指令编码，只读"),
        Fixed("普通档·上限", "普通经验封顶", "100", "100", "100",
            "6.4/6.5 0x00421012；6.6 0x00421008", "指令编码，只读"),
        Fixed("普通档·高等级每级扣", "攻方高于守方时每级扣一半", "÷2", "÷2", "÷2",
            "6.4/6.5 0x00421021 shr edx,1；6.6 0x00421012 shr eax,1", "指令编码，只读"),
        Fixed("普通档·最低", "高等级时最少给多少", "5", "5", "5",
            "6.4/6.5 0x0042102E；6.6 0x0042101F", "指令编码，只读"),
        Fixed("特殊目标翻倍", "目标 Data 号 = 0x496C96 时经验 ×2", "×2", "×2", "×2",
            "6.4/6.5 0x00420FE8；6.6 0x00420FE8 shl dword [..],1", "指令编码，只读"),
        Link("经验倍率基础", "倍率 = (第8项能力+本值)/100", "exp-multiplier-base",
            "100", "100", "100", "0x00407FB9"),
        Fixed("结算入口", "乘倍率并写入经验缓存", "0x00421053", "0x00421053", "0x0042104F",
            "6.4/6.5 0x00421053；6.6 0x0042104F", "公式输入，只读"),
        Fixed("个人经验缓存", "ctx+0x502：同一策略取最大值", "ctx+0x502", "ctx+0x502", "ctx+0x502",
            "0x0044DE9E 比较后写 [ctx+502]；0x0041A0BC add eax,[edx+502h]", "公式输入，只读"),
        Fixed("武器经验缓存", "ctx+0x506：同一策略取最大值", "ctx+0x506", "ctx+0x506", "ctx+0x506",
            "0x0041A0CB push [edx+506h]；0x0041A0D6 call 0x004082DD（槽 0）", "公式输入，只读"),
        Fixed("防具经验缓存", "ctx+0x50A+策略ID（66 项字节）", "ctx+0x50A", "ctx+0x50A", "ctx+0x50A",
            "0x00422A53 mov al,[eax+edx+50Ah]；0x00422A60 call 0x004082DD（槽 1）；0x004251E1 重置 memset(ctx+50Ah,0,42h)（6.4/6.5 0x004252A9、6.6 0x004252A7）", "公式输入，只读"),
        Fixed("缓存应用", "个人+武器经验统一结算入口", "0x00451085", "0x0041A0AC", "0x0041A0AC",
            "6.4 入口 0x00451085（0x0045109C call 0x004088CD、0x004510AF call 0x004082DD）；6.5/6.6 0x0041A0AC", "公式计算，只读"),
        Fixed("策略武器经验", "0x421363 计算武器经验值", "0x00421363", "0x00421363", "0x00421363",
            "0x0044DEBB call 0x00421363；0x0044DECB 写 [ctx+506]", "公式计算，只读"),
        Fixed("武器经验基础", "使用策略时给武器经验的基础加成", "4", "4", "3",
            "0x00421367 push 4；6.6 0x00421367 push 3", "公式输入，只读"),
        Fixed("武器等级差", "自身等级高于目标时扣 1", "-1", "-1", "-1",
            "0x004213F0 dec [ebp-8]", "公式输入，只读"),
        Fixed("武器门槛", "武器类型为 2 或 0xA 才计入", "2/0xA", "2/0xA", "2/0xA",
            "0x004213A2 cmp al,2；0x004213A6 cmp al,0Ah", "公式输入，只读")
    ];

    private static readonly BattleFormulaConstant[] MeritConstants =
    [
        Fixed("表基址", "功勋表起址", "0x508400", "0x508400", "0x508400",
            "0x00408B6B；0x0041057D movsx word [edx+eax*2+508400h]", "公式输入，只读"),
        Fixed("行宽", "每个角色 14 字节", "14", "14", "14",
            "0x00408B68 imul eax,0Eh；0x00410577", "指令编码，只读"),
        Fixed("字段", "0..4 五维、5 HP、6 MP", "7 项", "7 项", "7 项",
            "0x00408B52 字段索引 [ebp+10h]", "公式输入，只读"),
        Fixed("角色上限", "ID ≥ 102 直接丢弃", "102", "102", "102",
            "0x00408B55、0x00410560 cmp ax,66h", "指令编码，只读"),
        Fixed("读取入口", "叠加到基础能力", "0x0041055D", "0x0041055D", "0x0041055D",
            "0x0041055D movsx eax,word [..]", "公式输入，只读"),
        Fixed("写入入口", "模式 0 设 / 1 加 / 2 减", "0x00408B52", "0x00408B52", "0x00408B52",
            "0x00408B52 模式 [ebp+0Ch]", "公式输入，只读"),
        Fixed("取记录", "返回表内记录", "0x004224A8", "0x004224A8", "0x004224A8",
            "0x004224A8 imul eax,0Eh; add eax,0x508400", "公式输入，只读"),
        Fixed("仅我军叠加", "非我军不参与加成", "char+2A=0", "char+2A=0", "char+2A=0",
            "0x00411DA5 movzx eax,byte [ecx+2Ah]", "公式输入，只读"),
        Fixed("剧本设置命令", "命令 0x11..0x1F 映射字段 0..6，模式 0 设置", "0x11..0x1F",
            "0x11..0x1F", "0x11..0x1F", "0x004203D2 call 0x00408B52；0x004203BD-0x004203C1 映射",
            "公式输入，只读"),
        Fixed("剧本奖励命令", "读 5 个剧本变量后写功勋并同步基础能力", "5 变量", "5 变量", "5 变量",
            "0x00412007；变量表 0x00421492（6.4 0x0042149D）= 02/23/34/04/55；0x004120AD 调用 0x00408B52", "公式输入，只读"),
        Fixed("本场战功表", "0x508000 + ID×10（5 个 2 字节字段）", "0x508000", "0x508000", "0x508000",
            "0x0042ACED imul edx,eax,0Ah；0x0042ACF0 add edx,0x508000", "公式输入，只读"),
        Fixed("本场战功取记录", "战斗事件与道具 0x29 的写入入口", "0x0042ACD2", "0x0042ACD2", "0x0042ACD2",
            "0x0042ACD2 cmp ax,66h；imul edx,eax,Ah", "公式输入，只读"),
        Fixed("战功累加", "add word [记录+字段×2]；可被 ×2", "0x0042AB8E", "0x0042AB8E", "0x0042AB8E",
            "0x0042ABE6/0x0042ABEF add word [edx],cx；0x0042ABD3 imul ecx,ecx,2", "公式输入，只读"),
        Fixed("累加翻倍条件", "0x500E9A==1 且 0x505FDC==0 时增点×2；0x505FDC≠0 且 0x505F5C≠0 时整条放弃累加", "0x500E9A/0x505FDC/0x505F5C",
            "0x500E9A/0x505FDC/0x505F5C", "0x500E9A/0x505FDC/0x505F5C",
            "0x0042ABB6 cmp byte [500E9Ah],1；0x0042ABBF cmp byte [505FDCh],0；0x0042ABC8 cmp byte [505F5Ch],0；0x0042ABD1 jmp 0x0042ABF6（整条放弃）；0x0042ABD3 imul ecx,ecx,2（三基底逐字节相同）",
            "公式输入，只读"),
        Fixed("累加第三路", "0x477ADC 按武将ID找到单位槽且 0x501B00[槽]≠0 时再累加一遍原始增点（非翻倍）", "0x501B00",
            "0x501B00", "0x501B00",
            "0x0042ABE6 cmp byte [eax+501B00h],0；0x0042ABEF add ecx,[ebp+8]；0x00477ADC 扫 0..0xFA 槽（6.4/6.5 在 0x505FDC≠0 时只到 0x3C，6.6 无此限），0x00482715 = word[rec]&0FFFh 与 dword[unit+0] 比较", "公式输入，只读"),
        Fixed("战功全字段派发", "0x42A9C4(增点)：取记录后对字段 0..4 逐条累加", "0x0042A9C4", "0x0042A9C4", "0x0042A9C4",
            "0x0042A9E7 call 0x0042AB8E；调用点 0x0040380B（个人经验击杀）/0x00420FA3（策略经验击杀）/0x0044EC8D（可变增点；循环 0x0044EC60 槽 0..0x22，门控 0x418C90==2 与 0x42AC58=byte[char+2Ah]+1）", "公式计算，只读"),
        Fixed("战功单字段派发", "0x42A9F7：字段 2 固定 +1；6.6 改到伤害链调用", "0x0042A9F7", "0x0042A9F7", "0x0042A9F7",
            "0x0042AA0B push 2；0x0042AA11 call 0x0042AB8E；调用点 6.4/6.5 0x0042309F（行动结算），6.6 0x0043BE08/0x0043BE74", "公式计算，只读"),
        Fixed("战功字段1/3派发", "0x42A96D：每目标字段 1 +1；该目标无任何伤害记录时字段 3 再 +1", "0x0042A96D", "0x0042A96D", "0x0042A96D",
            "0x0040608E call（唯一调用点）；0x0042A98A push 1 字段1；0x0042A99B/0x0042A9A5 检查 ctx+84h/ctx+254h 两项为 0；0x0042A9AF push 3 字段3", "公式计算，只读"),
        Fixed("伤害记录数组", "ctx+84h 与 ctx+254h：按目标槽的 dword 记录；两项都为 0 视为无伤害", "ctx+0x84/0x254",
            "ctx+0x84/0x254", "ctx+0x84/0x254",
            "写：0x004361F7 = 0x407398(...) = max(0x425AD9(输入, byte[0x500E7C+索引]),1)，0x00436217 再取 min 当前HP；0x00418317 min(原+增量,上限)；0x00405FA9 本次应用伤害；0x0040600F 累加。读：0x004037EF/0x0042A99B/0x004038E5/0x00403AD7/0x004059A2", "公式输入，只读"),
        Fixed("战后条件表派发", "0x42AADB：表项 3/4 才累加（加的是表项值本身），其余表项跳过；6.6 表为 05 06 06 → 恒不加", "0x0042AADB", "0x0042AADB", "0x0042AADB",
            "0x0042AAFB mov al,[eax+407826h]；0x0042AB01 cmp al,3 + 0x0042AB05 cmp byte [ctx+608h],1；0x0042AB0E cmp al,4 + 0x0042AB12 cmp byte [ctx+604h],1；0x0042AB24 call 0x0042AB8E", "公式计算，只读"),
        Fixed("成长值→能力写入", "0x43A409(武将记录,字段,flag)：v=成长值+0x408A60(...)；我军只增不减；0x406ECA 写 word[rec+字段*2+0x11]，上限 9999", "9999","9999","9999",
            "0x0043A409 call 0x0040BE7D（ID=(rec-4CEA00h)/48h）；0x0043A41E call 0x0041055D（word[508400h+id*0Eh+字段*2]，仅 2A==0）；0x0043A42A call 0x00408A60；0x0043A440 cmp byte [rec+2Ah],0 + 0x0043A446 cmp ax,[rec+字段*2+11h]；0x0043A451 call 0x00406ECA（0x00406EE7 push 270Fh → 0x0047FA89 min；0x00406EFE mov [edx+字段*2+11h],ax）", "公式计算，只读"),
        Fixed("固定 +1", "0x42A8EE 给字段 0 加 1", "0x0042A8EE", "0x0042A8EE", "0x0042A8EE",
            "0x0042A8F1 mov eax,[ecx+4]；0x0042A8F4 push 0；0x0042A905 call 0x0042AB8E", "公式输入，只读"),
        Fixed("条件表", "战斗事件 +1 字段的条件表；6.6 迁至 0x41A139（内容相同）", "00 03 04 01 03 02", "00 03 04 01 03 02",
            "00 03 04 01 03 02", "6.4/6.5 0x0042AAF8/0x0042AB71 mov al,byte [eax+407826h]；6.6 0x0040DC7C/0x0042AB71 mov al,byte [eax+41A139h]；6.6 的 0x407826 为 05 06 06 06 06 06 但全量扫描无引用（遗留数据）", "公式输入，只读"),
        Fixed("6.6 战后派发入口", "6.6 以 0x40DC5C 按条件表派发字段 0..2", "—", "—", "0x0040DC5C",
            "0x0040DC65 call 0x0042ACD2；0x0040DCA5 call 0x0042AB8E；条件 0x0040DC86 byte [ecx+608h]、0x0040DC93 byte [ecx+604h]", "公式计算，只读"),
        Fixed("战功兑换成长值", "0x423F4B 用本场战功抵扣成长值（开关 0x505FA8、连续 0x501A74）", "0x00423F4B", "0x00423F4B",
            "0x00423F4B", "0x00423F4E cmp byte [505FA8h],0；0x00423F5A mov dl,1 / 0x00423F5C shl dl,cl（逐字段允许位）/ 0x00423F61 and dl,byte [eax+2]；0x00423F75 call 0x0042AC8F（第三参1=只判）；0x00423F7E sub word [edx],ax；0x00423F84 inc byte [eax+ecx+21h]；0x00423F8F call 0x0043A409（武将记录,字段,1；内部 0x40BE7D 取ID、0x41055D 取永久功勋、0x408A60 成长计算、0x406ECA 写能力并 min 9999，我军只增不减）；0x00423F94 cmp byte [501A74h],0（连续兑换）", "公式计算，只读"),
        Fixed("出阵计数表", "战斗后按武将 ID 自增的出阵次数表", "0x507800", "0x508A00", "0x508A00",
            "0x00406080 add eax,507800h（6.4）/ 508A00h（6.5·6.6）；初值 [0]=01（6.4）/ FF（6.5·6.6）", "公式输入，只读"),
        Fixed("本场战功结算", "清零 5 字段并累计到 0x505F40", "0x00408FA0", "0x00423EAD", "0x00423EAD",
            "6.4 只有 0x00408FE0-0x00408FFE xchg/add；6.5/6.6 0x00423EC7 xchg、0x00423EE5 add（0x00423EAD 无 6.4 对应函数）",
            "公式输入，只读"),
        Fixed("本场战功清理", "按 char+2 位图清零本场战功", "0x00408FA0", "0x00408FA0", "0x00408FA0",
            "0x00408FE0 test dl,1；0x00408FEA xchg word [eax+ecx*2],bx；0x0044ECBD 调用", "公式输入，只读"),
        Fixed("道具功勋分派", "效果 0x29 写本场战功；0x2A/0x2B 写永久 HP/MP 功勋", "0x29/0x2A", "0x29/0x2A", "0x29/0x2A",
            "0x004224D8 push 4；0x004224DA call 0x0041D124（取目标）；0x004224EB call 0x004061F9；0x004224F8 cmp cl,29h → 0x0042ACD2（0x508000+ID×10）；0x0042250B → 0x004224A8（0x508400+ID×0Eh）；0x0042258C add word [ecx+edx*2+0Ah],ax", "公式输入，只读"),
        Fixed("本场战功总额", "清零 5 字段并把旧值累计到 0x505F40（开关 0x505F3C 无静态写入，消费入口 0x456CB4 受 0x505FA8 门控）", "0x00423EAD", "0x00423EAD", "0x00423EAD",
            "0x00423EC7 xchg word [edx+eax*2],cx；0x00423ED9 cmp byte [505F3Ch],0；0x00423EE5 add [505F40h],ecx；0x00456CBA cmp byte [505FA8h],0；0x00408FFE add [505F40h],eax", "公式计算，只读"),
        Fixed("战功链总开关", "0x505FA8/0x501A74/0x505FAC 均只有读点，无静态写入", "0x505FA8", "0x505FA8", "0x505FA8",
            "0x0041D15E/0x00423F4E/0x00440D4B/0x00456CBA/0x0047C0C0 cmp byte [505FA8h],0；0x00423F94 cmp byte [501A74h],0；0x0046208A cmp dword [505FACh],0", "公式输入，只读"),        Fixed("道具功勋分派", "效果 0x29 写本场战功；0x2A/0x2B 写永久 HP/MP 功勋", "0x29/0x2A", "0x29/0x2A", "0x29/0x2A",
            "0x004224D8 push 4；0x004224DA call 0x0041D124（取目标）；0x004224EB call 0x004061F9；0x004224F8 cmp cl,29h → 0x0042ACD2（0x508000+ID×10）；0x0042250B → 0x004224A8（0x508400+ID×0Eh）；0x0042258C add word [ecx+edx*2+0Ah],ax", "公式输入，只读"),
        Fixed("本场战功总额", "清零 5 字段并把旧值累计到 0x505F40（开关 0x505F3C 无静态写入，消费入口 0x456CB4 受 0x505FA8 门控）", "0x00423EAD", "0x00423EAD", "0x00423EAD",
            "0x00423EC7 xchg word [edx+eax*2],cx；0x00423ED9 cmp byte [505F3Ch],0；0x00423EE5 add [505F40h],ecx；0x00456CBA cmp byte [505FA8h],0；0x00408FFE add [505F40h],eax", "公式计算，只读"),        Fixed("战功链总开关", "0x505FA8/0x501A74/0x505FAC 均只有读点，无静态写入", "0x505FA8", "0x505FA8", "0x505FA8",
            "0x0041D15E/0x00423F4E/0x00440D4B/0x00456CBA/0x0047C0C0 cmp byte [505FA8h],0；0x00423F94 cmp byte [501A74h],0；0x0046208A cmp dword [505FACh],0", "公式输入，只读"),
        Fixed("道具功勋入口", "道具效果 0x29 获得功勋", "0x004224D4", "0x004224D4", "0x004224D4",
            "0x004224F8 cmp cl,29h；0x004224FF call 0x0042ACD2", "公式输入，只读"),
        Fixed("策略战功", "策略使用 +2；0x2D 类 +4", "2/4", "2/4", "2/4",
            "0x00422A67 cmp byte [ebp-0Ch],2Dh；0x00422A6D mov al,2；0x00422A71 mov al,4", "公式输入，只读"),
        Fixed("策略战功入口", "0x42AA22 把值加到字段 1", "0x0042AA22", "0x0042AA22", "0x0042AA22",
            "0x0042AA27 call 0x0042ACD2；0x0042AA38 call 0x0042AB8E", "公式计算，只读"),
        Fixed("道具HP/MP上升", "效果 0x2A/0x2B 同时加最大 HP/MP 与功勋字段 5/6", "0x0042255C-0x0042258C",
            "0x0042255C-0x0042258C", "0x0042255C-0x0042258C",
            "0x00422565 sub eax,2Ah；0x0047FA89 = min(a+b,c)（0x0047FA90 add ecx,[ebp+8] 后与 [ebp+10h] 比较）；0x0042258C add word [ecx+edx*2+0Ah],ax", "公式输入，只读"),
        Fixed("上升上限", "最大 HP/MP 与功勋字段钳到 65535", "65535", "65535", "65535",
            "0x0042256E push 0FFFFh；0x00422577 call 0x0047FA89", "指令编码，只读"),
        Fixed("上升字段偏移", "功勋字段 5/6 从记录 +0xA 开始", "+0xA", "+0xA", "+0xA",
            "0x0042258C add word [ecx+edx*2+0Ah],ax", "公式输入，只读")
    ];

    private static readonly BattleFormulaConstant[] MeritAllocationConstants =
    [
        Fixed("分配函数", "0x46206C：点数×倍率后按门槛提升五维", "0x0046206C", "0x0046206C", "0x0046206C",
            "0x0046208A cmp [505FACh]；0x00462093 movzx eax,[5083FCh]；0x0046209E imul eax,[ebp+0Ch]", "公式计算，只读"),
        Fixed("点数计数器", "战后累计点；上限 255，并同步到单位 +2", "0x5083FC", "0x5083FC", "0x5083FC",
            "6.4/6.5 0x004719A9 inc byte [5083FCh]（函数 0x00471981，0x0041983F 调用）；6.6 0x0040BB05（函数 0x0040BADD）",
            "公式输入，只读"),
        Fixed("分配开关", "0x505FAC 非 0 才分配", "0x505FAC", "0x505FAC", "0x505FAC",
            "0x0046208A cmp byte [505FACh],0", "公式输入，只读"),
        Fixed("槽位数", "每次分配 5 个槽位", "5", "5", "5",
            "0x004620C1 cmp dl,5；0x004620B0 cmp al,5", "指令编码，只读"),
        Fixed("成长值字段", "槽位当前值 char+0x21+i", "char+0x21", "char+0x21", "char+0x21",
            "0x004620CC movzx eax,byte [ecx+edx+21h]；0x004620BF push [eax+ecx+21h]", "公式输入，只读"),
        Fixed("能力字段", "提升写入 char+0x11+2i", "char+0x11", "char+0x11", "char+0x11",
            "0x004620F9 inc word [ecx+edx*2+11h]；0x004620DD inc word [ecx+eax*2+11h]", "公式输入，只读"),
        Fixed("成长值上限（6.4）", "6.4 槽位值到 100 不再提升", "100", "—", "—",
            "0x004620D1 cmp al,64h", "指令编码，只读"),
        Fixed("成长值上限（6.5/6.6）", "6.5/6.6 槽位值到 110 不再提升", "—", "110", "110",
            "0x0042AC98 cmp al,6Eh", "指令编码，只读"),
        Fixed("门槛基础", "槽位值 <80 时每点消耗 50", "50", "50", "50",
            "0x004620D9 cmp esi,32h；0x0042ACA8 mov al,32h", "公式输入，只读"),
        Fixed("门槛分界", "槽位值达到 80 后改用递增门槛", "80", "80", "80",
            "0x004620D5 cmp al,50h；0x0042ACA4 cmp al,50h", "公式输入，只读"),
        Fixed("门槛系数", "高段每差 1 点增加 10", "10", "10", "10",
            "0x004620E9 imul eax,eax,0Ah；0x0042ACAE imul eax,eax,0Ah", "公式输入，只读"),
        Fixed("门槛偏移", "高段门槛 = (值−79)×10+55", "55", "55", "55",
            "0x004620EC add eax,37h；0x0042ACB1 add eax,37h", "公式输入，只读"),
        Fixed("倍率（0x409639/0x42AD3B）", "对应调用点压栈的第二实参", "1", "25", "50",
            "0x00409639 push 1/19h/32h；0x0042AD3B push 1/19h/32h", "公式输入，只读"),
        Fixed("倍率（0x40C386/0x44CD8D）", "对应调用点压栈的第二实参", "1", "25", "10",
            "0x0040C386 push 1/19h/0Ah；0x0044CD8D push 1/19h/0Ah", "公式输入，只读"),
        Fixed("6.4 内联分配", "6.4 在 0x46206C 内直接循环", "0x004620C1", "—", "—",
            "0x004620CC-0x004620FE", "公式结构，只读"),
        Fixed("门槛函数（6.5/6.6）", "0x42AC8F 查门槛并返回消耗", "—", "0x0042AC8F", "0x0042AC8F",
            "0x004620C7 call 0x0042AC8F；0x0042AC94-0x0042ACCF", "公式结构，只读"),
        Fixed("余额转入", "分配余额写回本场战功", "0x0042ACD2/0x0042AB8E", "0x0042ACD2/0x0042AB8E",
            "0x0042ACD2/0x0042AB8E", "0x004620EA mov eax,[ebp+8]；0x004620EF call 0x0042ACD2", "公式结构，只读")
    ];

    private static readonly BattleFormulaConstant[] CharLevelExpConstants =
    [
        Link("最大等级", "角色经验结算的最高等级", "char-exp-max-level", "80", "60", "99",
            "0x004088D3 mov al,本值"),
        Link("每级经验（6.4/6.6）", "6.4/6.6 每升一级所需经验", "char-exp-threshold",
            "150", "—", "250", "0x004088D6 mov al,本值"),
        Link("等级分段（6.5）", "每多少级提高一档", "char-exp-band-65", "—", "20", "—",
            "0x0040D226 mov ecx,本值"),
        Link("每档增量（6.5）", "阈值 = (min(等级/分段,3)+3)×本值", "char-exp-step-65",
            "—", "50", "—", "0x0040D23D imul eax,本值"),
        Fixed("档位上限（6.5）", "分段最多计 3 档", "—", "3", "—",
            "0x0040D230 cmp eax,3；0x0040D235 mov eax,3", "指令编码，只读"),
        Fixed("等级字段", "角色等级 char+0x2C", "char+2C", "char+2C", "char+2C",
            "0x004065D0 movzx eax,byte [ecx+2Ch]", "公式输入，只读"),
        Fixed("经验字段", "角色经验 char+0x2D", "char+2D", "char+2D", "char+2D",
            "0x004065C7 movzx eax,byte [ecx+2Dh]", "公式输入，只读"),
        Fixed("满级经验", "满级后经验写 255", "255", "255", "255",
            "0x0040891C mov dl,0FFh；0x00408923 mov [ecx+2Dh],dl", "指令编码，只读")
    ];

    private static readonly BattleFormulaConstant[] PerTurnExpConstants =
    [
        Fixed("循环上限", "每回合结算 3 个经验特效", "3", "3", "3",
            "0x0043CEE5 cmp al,3；6.6 0x0043CEE0", "指令编码，只读"),
        Fixed("选择器表", "0x0043CFCD 三字节；装备/道具类型过滤值", "1D 1E 1E", "00 00 00", "1E 1E 1E",
            "6.4/6.5 0x0043CEED；6.6 0x0043CEE8 movzx edx,byte [eax+43CFCDh]；0x00407A17 call 0x0043AD29 比较道具 +0x14，0x00407A1E 比较 +0x11", "公式输入，只读"),
        Fixed("个人/装备 selector", "个人 selector = i+3（经验/武器经验/防具经验）", "3/4/5", "3/4/5", "3/4/5",
            "6.4/6.5 0x0043CEF5；6.6 0x0043CEF0 add eax,3", "公式输入，只读"),
        Fixed("特效查询", "四参数查询：个人/装备/聚合/取值", "0x4101D9", "0x4101D9", "0x4101D9",
            "6.4/6.5 0x0043CEFC；6.6 0x0043CEF7 call 0x004101D9", "公式计算，只读"),
        Fixed("经验倍率", "× (第 8 项能力 + 100) / 100", "0x407FAA/0x425AD9", "0x407FAA/0x425AD9",
            "0x407FAA/0x425AD9",
            "6.4/6.5 0x0043CF0B/0x0043CF18；6.6 0x0043CF06/0x0043CF13", "公式计算，只读"),
        Fixed("个人经验结算", "acc[0] → char 经验 → 升级", "0x4088CD", "0x4088CD", "0x4088CD",
            "0x0043CF9C call 0x004065C7；0x0043CFAA call 0x004088CD", "公式计算，只读"),
        Fixed("武器经验结算", "acc[1] → 装备槽 0", "0x4082DD(0)", "0x4082DD(0)", "0x4082DD(0)",
            "0x0043CFAF push [ebp-10h]；0x0043CFB2 push 0；0x0043CFB7 call 0x004082DD", "公式计算，只读"),
        Fixed("防具经验结算", "acc[2] → 装备槽 1", "0x4082DD(1)", "0x4082DD(1)", "0x4082DD(1)",
            "0x0043CFBC push [ebp-0Ch]；0x0043CFBF push 1；0x0043CFC4 call 0x004082DD", "公式计算，只读"),
        Fixed("当前HP/MP写入", "unit+0x10 / +0x14 = min(新值, 最大HP/MP)；无符号比较、无下限（超大/负值会被钳到上限）",
            "0x0043F6DB/0x0043F715", "0x0043F6DB/0x0043F715", "0x0043F6DB/0x0043F715",
            "0x0043F6DB mov [ecx+10h], 上限 0x407263；0x0043F715 mov [ecx+14h], 上限 0x40728F；三基底 0x43F6DB 起逐字节相同；读取 0x41B500 = dword[unit+10h]",
            "公式输入，只读")
    ];

    private static readonly BattleFormulaConstant[] EquipLevelExpConstants =
    [
        Link("宝物经验阈值", "带宝物标记的装备每级经验", "equip-exp-threshold-special",
            "200", "200", "200", "0x00408319 add dl,本值"),
        Link("普通经验阈值", "普通装备每级经验", "equip-exp-threshold-normal",
            "100", "150", "100", "0x0040831E add dl,本值"),
        Link("宝物等级上限", "宝物装备最高等级", "equip-level-cap-special",
            "9", "9", "15", "0x00408327 mov al,本值"),
        Link("普通等级上限", "普通装备最高等级", "equip-level-cap-normal",
            "5", "5", "9", "0x0040832B mov al,本值"),
        Fixed("满级经验标记", "装备到上限后经验写 0xFF（不再累计）", "0xFF",
            "0xFF", "0xFF",
            "6.4/6.5 0x0040839D push 0FFh；6.6 0x00408393 mov al,0FFh；随后 0x40329B 写回", "指令编码，只读"),
        Fixed("升级后回调", "写等级（0x403286）后调 0x4083C6(charID, slot)；校验 ID<0x400、槽≤1，走脚本派发", "0x004083C6",
            "0x004083C6", "0x004083C6",
            "0x0040838B call 0x004083C6（唯一调用点）；0x004083CC cmp [ebp+8],400h；0x004083D9 cmp byte [ebp+0Ch],1；0x0040842D call 0x0045778F（0x4B5DF0）", "公式输入，只读"),
        Fixed("宝物判定", "道具记录 +0x11 的 bit0", "bit0", "bit0", "bit0",
            "0x0040B4E1；0x0040B4F4 movzx eax,byte [ecx+11h]", "公式输入，只读"),
        Fixed("处理槽位", "只处理武器槽 0 / 防具槽 1", "0/1", "0/1", "0/1",
            "0x004082EA cmp eax,1；0x004082ED jg", "指令编码，只读"),
        Fixed("等级字段", "char+0x2E+槽×3+1", "char+0x2F", "char+0x2F", "char+0x2F",
            "0x004032DF movzx eax,byte [ecx+edx+2Fh]", "公式输入，只读"),
        Fixed("经验字段", "char+0x2E+槽×3+2", "char+0x30", "char+0x30", "char+0x30",
            "0x00409680 movzx eax,byte [eax+ecx+30h]", "公式输入，只读"),
        Fixed("满级经验", "满级后经验写 255", "255", "255", "255",
            "0x0040839D push 0FFh；0x004083A9 call 0x0040329B", "指令编码，只读"),
        Fixed("策略防具经验", "使用策略时给防具经验的基础加成", "3", "3", "4",
            "6.4/6.5 0x00421474 add [ebp-8],3；6.6 0x00421469 add [ebp-8],4", "公式输入，只读"),
        Fixed("防具经验加成条件", "施放类型为 0 且 ctx+0x108+索引×4 非 0 时才加基础值", "type=0", "type=0", "type=0",
            "0x00421450 call 0x00425AC7；0x00421457 test eax,eax；0x0042145F cmp dword [ecx+eax*4+108h],0；0x00421469/0x00421474 add [ebp-8],3（6.6 +4）", "公式输入，只读"),
        Fixed("防具经验加成条件", "施放类型为 0 且 ctx+0x108+索引×4 非 0 时才加基础值", "type=0", "type=0", "type=0",
            "0x00421450 call 0x00425AC7；0x00421457 test eax,eax；0x0042145F cmp dword [ecx+eax*4+108h],0；0x00421469/0x00421474 add [ebp-8],3（6.6 +4）", "公式输入，只读"),
        Fixed("策略等级差", "目标等级更高时扣 1", "-1", "-1", "-1",
            "0x00421480（6.5/6.6 0x00421475）dec [ebp-8]", "公式输入，只读"),
        Fixed("策略禁用查询", "0x450931 扫 0x508C00 的 FF 分隔表；6.6 为 NOP", "0x00450931", "0x00450931", "—",
            "0x00450944 cmp byte [edx],0FFh；0x0045094D je；表 0x508C00 初值 6.4 00 04…、6.5 FF FF、6.6 01 02 03；6.6 同址起为 0x90", "公式输入，只读"),
        Fixed("特技习得查询", "0x41873E 扫 5 条 3 字节表项（技能ID word + 需求等级 byte）", "0x0041873E", "0x0041873E", "0x0041873E",
            "0x00418750 imul eax,eax,3；0x00418759 cmp dx,word [eax]；0x00418764 cmp dl,byte [eax+2]；0x0041876D mov al,0FFh；调用点 0x004225C4", "公式输入，只读"),
        Fixed("特技数据表", "0x41E907(i)=dword[0x500C37]+i×0x10（80 条）；静态为 5 个 {00 04 01}+尾 01 的占位记录", "0x00511800", "0x00511800", "0x00512000",
            "0x0041E907 movzx ecx,al；imul ecx,10h；add ecx,[500C37h]；dword[500C37h] 初值 6.4/6.5 0x00511800、6.6 0x00512000", "公式输入，只读"),
        Fixed("特技习得查询", "0x41873E 扫 5 条 3 字节表项（技能ID word + 需求等级 byte）", "0x0041873E", "0x0041873E", "0x0041873E",
            "0x00418750 imul eax,eax,3；0x00418759 cmp dx,word [eax]；0x00418764 cmp dl,byte [eax+2]；0x0041876D mov al,0FFh；调用点 0x004225C4", "公式输入，只读"),
        Fixed("特技数据表", "0x41E907(i)=dword[0x500C37]+i×0x10（80 条）", "0x00511800", "0x00511800", "0x00512000",
            "0x0041E907 movzx ecx,al；imul ecx,10h；add ecx,[500C37h]；dword[500C37h] 初值 6.4/6.5 0x00511800、6.6 0x00512000；静态内容为 5 个 {00 04 01} + 尾 01 的占位记录", "公式输入，只读"),
        Fixed("策略禁用查询", "0x450931 扫 0x508C00 的 FF 分隔表；6.6 为 NOP", "0x00450931", "0x00450931", "—",
            "0x00450944 cmp byte [edx],0FFh；0x0045094D je；表 0x508C00 初值 6.4 00 04…、6.5 FF FF、6.6 01 02 03；6.6 同址起为 0x90", "公式输入，只读"),
        Fixed("特技习得查询", "0x41873E 扫 5 条 3 字节表项（技能ID word + 需求等级 byte）", "0x0041873E", "0x0041873E", "0x0041873E",
            "0x00418750 imul eax,eax,3；0x00418759 cmp dx,word [eax]；0x00418764 cmp dl,byte [eax+2]；0x0041876D mov al,0FFh；调用点 0x004225C4", "公式输入，只读"),
        Fixed("特技数据表", "0x41E907(i)=dword[0x500C37]+i×0x10（80 条）；静态为 5 个 {00 04 01}+尾 01 的占位记录", "0x00511800", "0x00511800", "0x00512000",
            "0x0041E907 movzx ecx,al；imul ecx,10h；add ecx,[500C37h]；dword[500C37h] 初值 6.4/6.5 0x00511800、6.6 0x00512000", "公式输入，只读"),        Fixed("策略经验入口", "按策略 ID 计算并写入防具经验槽 1", "0x00421409", "0x00421409", "0x00421409",
            "0x0042148F/0x00421492 call 0x00421053；0x00422A53 mov al,[eax+edx+50Ah]；0x00422A60 call 0x004082DD（槽 1）",
            "公式计算，只读")
    ];

    private static readonly BattleFormulaConstant[] AbilityWriteConstants =
    [
        Fixed("能力/HP/MP 增量上限", "0x47FA89(旧,值,cap)=min(旧+值,cap) 的封顶值", "9999", "9999", "9999",
            "0x00406EE7 / 0x00406F18 / 0x00406F36 push 270Fh；0x0047FA89 add ecx,[ebp+8] → cmp ecx,[ebp+10h] → jg 返回 cap", "公式结构值，只读"),
        Fixed("成长值封顶", "字段 10..14 写成长值 byte[rec+字段+0x17] 的上限", "100", "100", "100",
            "0x00406F5B push 64h；0x004070D5 mov dl,64h", "公式结构值，只读"),
        Fixed("最大 HP 直接设置上限", "0x407027 字段 5 写 dword[rec+0x1B] 的封顶", "65535", "65535", "65535",
            "0x00407058 cmp edx,0FFFFh；0x00407065 mov dword [ecx+1Bh],edx", "公式结构值，只读"),
        Fixed("HP/MP 变更模式", "0x505F30：0 扣减(保底1)、1 增加、2 直接设为值", "0/1/2", "0/1/2", "0/1/2",
            "0x0040DA4D mov ecx,dword [505F30h]；0x0040DA57 cmp eax,edx / ja→相减；0x0040DA5B mov eax,1；0x0040DA6B add eax,edx；0x0040DA6F mov eax,edx", "公式结构值，只读")
    ];

    private static readonly BattleFormulaConstant[] TroopTierConstants =
    [
        Fixed("兵种档位长度", "0x408A60 的块长，也是升级阈值单位", "20", "20", "20",
            "0x00408A66 push 14h；0x0041D3E4 push 14h", "公式结构值，只读"),
        Fixed("兵种 ID 上限", "超过 59 的兵种不参与成长计算", "59", "59", "59",
            "0x00408A73 cmp al,3Bh；0x0041D3EB cmp al,3Bh（0x3B=59）", "公式结构值，只读"),
        Fixed("档位除数", "兵种 ID 按 %3 分档", "3", "3", "3",
            "0x0041FBF8 mov cl,3；0x0041D3FF mov ecx,3", "公式结构值，只读"),
        Fixed("前置积分倍数", "0x413FAC 末尾对累加值左移 1 位", "2", "2", "2",
            "0x00413FF9 shl dword [ebp-4],1", "公式结构值，只读")
    ];

    private static readonly BattleFormulaConstant[] TroopUpConstants =
    [
        Fixed("兵种提升增量", "0x41D468 把 byte[rec+0x2B] 设为 troop+1", "1", "1", "1",
            "0x0041D50B call 0x00406610；0x0041D510 inc eax；0x0041D515 call 0x0040E01F；0x0040E025 mov byte [ecx+2Bh],al", "公式结构值，只读"),
        Fixed("提升演出帧数", "兵种提升动画的循环次数", "10", "10", "10",
            "0x0041D5B2 cmp dword [ebp-4],0Ah；0x0041D5AF inc dword [ebp-4]", "公式结构值，只读")
    ];

    private static readonly BattleFormulaConstant[] EquipGrowthConstants =
    [
        Fixed("每级成长字段", "道具记录 +0x17 的字节即每级成长值", "+0x17", "+0x17", "+0x17",
            "0x0041B4F7 movzx eax,byte [ecx+17h]；6.6 0x004202BE 同式", "公式结构值，只读"),
        Fixed("类型门控上界", "0x40B444 映射值 ≤1 才计每级成长", "1", "1", "1",
            "0x0040C464 cmp eax,1；0x0040C467 setle cl；0x0040B447 movzx eax,byte [ecx+11h]", "公式结构值，只读"),
        Fixed("宝物类别例外值", "0x429AD7：类别 0x0A 对索引 0/2 也视为匹配", "0x0A", "0x0A", "0x0A",
            "0x00429AE5 cmp al,0Ah；0x00429AEC/0x00429AF1 je（索引 0/2）", "公式结构值，只读")
    ];

    private static readonly BattleFormulaConstant[] TreasureGrowthConstants =
    [
        Fixed("百分比除数", "0x425AD9 = a×b/100 的除数", "100", "100", "100",
            "0x00425AE5 mov ecx,64h；0x00425AEA div ecx", "公式结构值，只读"),
        Fixed("宝物门控值", "0x46230F[索引]==2 才应用宝物成长", "2", "2", "2",
            "0x00452842 cmp byte [eax+46230Fh],2；6.6 同址基址 4CB6C0h", "公式结构值，只读"),
        Fixed("宝物成长表哨兵", "0x46236F 表值 0xFE 表示不覆盖", "0xFE", "0xFE", "0xFE",
            "0x00420180 cmp al,0FEh", "公式结构值，只读")
    ];

    private static readonly BattleFormulaConstant[] GrowthGapConstants =
    [
        Fixed("缺口索引上限", "索引 ≥5 不走基准补正", "5", "5", "5",
            "0x00436DE9 cmp dword [ebp+8],5；0x00436DED jae 0x436E9F", "公式结构值，只读"),
        Fixed("基准合成除数", "(兵种字节 + 成长档) >> 1 的除数", "2", "2", "2",
            "0x00436E37 pop edx；0x00436E38 add al,dl；0x00436E3A shr eax,1", "公式结构值，只读"),
        Fixed("特效查询参数", "0x42518F(0x3D, 0x5C, 6.4=1/6.5·6.6=2, 0)", "0x3D/0x5C", "0x3D/0x5C", "0x3D/0x5C",
            "0x00436DF7 push 5Ch；0x00436DF9 push 3Dh；0x00436DF5 push 2（6.4 为 push 1）", "公式结构值，只读")
    ];

    private static readonly BattleFormulaConstant[] EffectDispatchConstants =
    [
        Fixed("分派判定值", "0x40B922 = (0x40B913()==3)，为 1 走 0x4101D9", "3", "3", "3",
            "0x0040B922 call 0x40B913；0x0040B92C cmp al,3；0x0040B92E sete cl；0x0040B916 mov ecx,4AC63Ch", "公式结构值，只读"),
        Fixed("查询模式", "0x436DE1 调 0x42518F 的第三参", "1/2", "1/2", "1/2",
            "6.4 0x00436DF5 push 1；6.5/6.6 push 2", "跨基底差异，只读"),
        Fixed("索引/选择子", "0x436DE1 查特效用的索引与选择子", "0x3D/0x5C", "0x3D/0x5C", "0x3D/0x5C",
            "0x00436DF7 push 5Ch；0x00436DF9 push 3Dh", "公式结构值，只读")
    ];

    private static readonly BattleFormulaConstant[] MergeModeConstants =
    [
        Fixed("模式字节地址", "0x4AC63C：初值 0；0x416A78 写 2、0x416A91 自增、0x43C015 写 3", "0x4AC63C", "0x4AC63C", "0x4AC63C",
            "0x00416A78 mov byte [4AC63Ch],2；0x00416A91 inc byte [4AC63Ch]；0x0043C015 mov byte [4AC63Ch],3；0x0040B916 mov ecx,4AC63Ch + 0x0041EDF2 movzx eax,byte [ecx]", "公式结构值，只读"),
        Fixed("分派值", "byte[0x4AC63C]==3 时走 0x4101D9", "3", "3", "3",
            "0x0040B92C cmp al,3；0x0040B92E sete cl", "公式结构值，只读"),
        Fixed("合并模式", "0x40BF2F：0=和、1=取大、3=按位或、其它原值 7 保留否则取大", "0/1/3/7", "0/1/3/7", "0/1/3/7",
            "0x0040BF36 add eax,edx；0x0040BF3F cmp eax,edx；0x0040BF4C or eax,edx；0x0040BF50 cmp al,7", "公式结构值，只读"),
        Fixed("模式置2入口", "进段函数：置 2 → 调用 → 自增到 3", "0x4426E4", "0x416A75", "0x416A75",
            "6.4 0x004426E7 mov byte [4AC63Ch],2；6.5/6.6 0x00416A78 同；6.4 0x00442700 inc；6.5/6.6 0x00416A91 inc", "跨基底差异，只读"),
        Fixed("模式置3位置", "结算前置 3 的写点", "0x43C015", "0x43C015", "0x43C010",
            "0x0043C015 C6 05 3C C6 4A 00 03；6.6 0x0043C010 同码", "跨基底差异，只读")
    ];

    public static readonly IReadOnlyList<BattleFormulaDefinition> Definitions =
    [
        new("hit-curve", "命中", "命中率曲线（物理/策略共用）",
            "30..100", "30..100", "25..100",
            "双方能力比值决定命中率：攻方越高越容易打中，最低 30%（6.6 25%）。",
            "把攻方能力与守方能力相比：攻方 ≥ 守方 2 倍直接 100%；1～2 倍是 90%～100%；1/2～1 倍是 60%～90%；低于一半只剩 30%～45%。物理命中比敏捷，策略命中比智力和士气之和。",
            "曲线函数 6.4 0x0043B50C，6.5/6.6 0x0043B53A；三基底同值。6.6 判定入口 0x0043B4DE 把最低值钳到 25。",
            HitCurveConstants),
        new("physical-hit", "命中", "物理命中/闪避",
            "敏捷曲线；85+二判", "敏捷曲线；85+二判", "敏捷曲线；下限25",
            "攻方敏捷对守方敏捷套命中曲线；6.4/6.5 高命中还有一次补判。",
            "物理伤害函数先过命中判定：拿双方敏捷代入命中率曲线。6.4/6.5 命中率 ≥85% 时，第一次没打中会再判一次，命中率扣 10%，最多判 2 次；6.6 用最低命中率 25 的下限钳制。",
            "6.4 判定 0x0043B4BA、命中桩 0x0043B60B；6.5/6.6 判定 0x0043B4B6、命中桩 0x0043B600（同址不同分支）。",
            [Fixed("计算属性", "物理命中看双方敏捷", "敏捷", "敏捷", "敏捷",
                "6.4/6.5/6.6 命中桩内 0x0043B65A 取能力类型 3", "公式输入，只读"),
             ..HitRetryConstants]),
        new("strategy-hit", "命中", "策略命中/闪避",
            "智力+士气曲线；85+二判", "智力+士气曲线；85+二判", "智力+士气曲线；下限25",
            "攻方智力和士气之和对守方同一组能力套命中曲线。",
            "策略伤害函数先过命中判定：攻方（智力+士气）对守方（智力+士气）套命中率曲线。6.4/6.5 同样有 85% 以上的补判；6.6 用最低命中率 25 的下限钳制。",
            "6.4/6.5 命中桩 0x0043B6F3，取能力类型 2 与 4；6.6 命中桩 0x0043B730（同逻辑搬移）。",
            [Fixed("计算属性", "策略命中看双方智力与士气", "智力+士气", "智力+士气", "智力+士气",
                "6.4/6.5 0x0043B7E7、0x0043B800；6.6 0x0043B7FC、0x0043B813", "公式输入，只读"),
             ..HitRetryConstants]),
        new("rate-curve", "暴击", "暴击/连击率曲线（共用）",
            "1..100", "1..100", "1..100",
            "攻方士气或敏捷越高，暴击或连击越容易发动；攻方达到守方 3 倍必发动。",
            "把攻方能力与守方能力相比：攻方 ≥ 守方 3 倍直接 100%；2～3 倍是 20%～100%；1～2 倍是 2%～20%；攻方低于守方时只剩 1%。物理暴击和策略暴击比士气，连击比敏捷。",
            "曲线函数 0x00405D0A（三基底同址同值）；物理暴击入口 0x00405E80，策略暴击入口 0x0040CA68，连击入口 0x004060D2。",
            RateCurveConstants),
        new("physical-crit", "暴击", "物理暴击",
            "士气曲线；池0；伤害×(率+100)/2%", "士气曲线；池2；伤害×(率+100)/2%", "士气曲线；池2；伤害×(率+100)/2%",
            "物理暴击率由双方士气套曲线决定，暴击后额外加“(暴击率+100)÷2%”的伤害。",
            "先用双方士气算暴击率，再按暴击率随机判定。命中暴击后，额外伤害 = 原伤害 × (暴击率+100)/2 / 100；暴击率 0 → +50%，100 → +100%。三基底都进入集气池：6.4 池 0，6.5/6.6 池 2。6.6 再叠加特效 112 的返回值。",
            "物理暴击函数 0x00405E80；暴击率来源 0x0040C7D8（能力类型 4）；伤害追加 6.4/6.5 0x00405F02，6.6 0x0042E4FD（sar / 2）。",
            [Fixed("计算属性", "物理暴击看双方士气", "士气", "士气", "士气",
                "0x0040C7E9-0x0040C7F6 取能力类型 4", "公式输入，只读"),
             Link("暴击率上限", "最高暴击率", "physical-crit-cap", "100", "100", "100",
                "0x00405ED7"),
             Fixed("伤害除数", "暴击率除以几再加伤", "2", "2", "2",
                "6.4/6.5 0x00405F0A sar eax,1；6.6 0x0042E516 sar ecx,1", "指令编码，只读"),
             Link("集气模式", "物理暴击集气池编号", "physical-crit-pool", "0", "2", "2",
                "0x00405EDB push 0/2; call 0x00437896 / 0x004287A8"),
             Fixed("暴击无效特效", "0x412CF4：索引0x70 命中则允许暴击，否则按索引0x30；选择子随基底不同", "0x00/0x41", "0x31/0x41", "0x68/0x00",
                "0x00412CF8 mov ecx,[ecx+0Ch]；0x00412CFB call 0x00422E56（压栈 1,1,选择子,70h：6.4 00、6.5 31h、6.6 68h）；0x00412D07 call 0x00405DCF（压栈 1,1,选择子,30h：6.4/6.5 41h、6.6 00）；名称池 0x4CC600+ID×10：0x70 强化致命一击/暴击增幅、0x31 物理免疫、0x41 步兵防御/增加视野、0x68 劲透攻击/献祭光环；6.4 名称池全 0，改用 0x48BF91 起的紧凑字符串块；其前 0x48BF00 起为 4 字节步长表（0x00500196+9n），目标区为 9 字节记录（首 4 字节 GBK 文本片段，其余 5 字节 0）", "公式输入，只读")]),
        new("strategy-crit", "暴击", "策略暴击",
            "士气曲线；池0；伤害×(率+100)/4%", "士气曲线；池18；伤害×(率+100)/4%", "士气曲线；池18；伤害×(率+100)/4%",
            "策略暴击率同样由双方士气套曲线决定，暴击后额外加“(暴击率+100)÷4%”的伤害。",
            "先用双方士气算暴击率，再按暴击率随机判定。命中暴击后，额外伤害 = 原伤害 × (暴击率+100)/4 / 100；暴击率 0 → +25%，100 → +50%。三基底都进入集气池：6.4 池 0，6.5/6.6 池 18。",
            "策略暴击函数 0x0040CA68；暴击率包装 0x0040CADA；伤害追加 0x0040CAEB（shr eax,2）。",
            [Fixed("计算属性", "策略暴击看双方士气", "士气", "士气", "士气",
                "0x0040CA97-0x0040CAA8 取能力类型 4", "公式输入，只读"),
             Link("暴击率上限", "最高暴击率", "strategy-crit-cap", "100", "100", "100",
                "6.4 0x0040CAD8；6.5/6.6 0x0040CAA5"),
             Fixed("伤害除数", "暴击率除以几再加伤", "4", "4", "4",
                "0x0040CAEE shr eax,2", "指令编码，只读"),
             Link("集气模式", "策略暴击集气池编号", "strategy-crit-pool", "0", "18", "18",
                "6.4 0x0040CADC；6.5/6.6 0x0040CAA9")]),
        new("combo-rate", "连击", "连击率",
            "敏捷曲线；特效52；池0", "敏捷曲线；特效52；池0", "敏捷曲线；特效52；池0",
            "连击率由双方敏捷套曲线决定；有特效 52 时按其发动率判定。",
            "先用双方敏捷算连击率，再随机判定是否追加一击。拥有特效 52 时不再看曲线，直接使用特效 52 的发动率。三基底都会进入集气池，池号默认 0。",
            "连击函数 0x004060D2；连击率来源 0x00405CB9（能力类型 3）；特效 52 桩 6.4 0x00405CF7、6.5/6.6 0x004E411B 与 0x004E4145。",
            [Fixed("计算属性", "连击看双方敏捷", "敏捷", "敏捷", "敏捷",
                "0x00405CCA-0x00405CD5 取能力类型 3", "公式输入，只读"),
             Link("特效52 满率", "有特效 52 时的连击率", "active-combo-chance", "100", "100", "100",
                "6.4 0x00405CF8；6.5/6.6 0x004E411C、0x004E4146"),
             Link("集气模式", "连击集气池编号", "combo-pool", "0", "0", "0",
                "0x0040612E push 0")]),
        new("combo-damage", "连击", "连击伤害",
            "—", "每次 +0%", "每次 +0%",
            "强化连击类特效触发后，连击不再逐次衰减，并额外加固定百分比。",
            "没有强化连击时，连击伤害会逐次衰减；有强化连击/连击上限类特效后，后续连击不再衰减，并在原伤害上再加这个固定百分比。默认 0 表示只不衰减、不加伤。6.4 同址为空，未收录。",
            "函数 0x004E313C；6.5/6.6 指令 0x004E319C 执行 imul eax,[ebp-4]; add eax,本值，再按百分比追加。",
            [Link("连击固定增伤", "每次连击额外加多少", "combo-damage-bonus",
                "—", "0", "0", "0x004E319E")]),
        new("active-combo", "连击", "主动连击发动率",
            "100", "100", "100",
            "拥有主动连击时，追加一击的发动概率。",
            "特效 52 返回的数值直接作为追加一击的概率：100 = 每次都追加，50 = 一半机会。这个值就是主动连击的发动率。",
            "特效 52 桩 6.4 0x00405CF7、6.5/6.6 0x004E411B 与 0x004E4145，字节 B0 64；概率函数 0x00437896 / 0x004287A8 把上限钳到 100 后与 0..99 随机数比较。",
            [Link("主动连击发动率", "追加一击的概率", "active-combo-chance",
                "100", "100", "100", "6.4 0x00405CF8；6.5/6.6 0x004E411C、0x004E4146")]),
        new("guided-attack", "连击", "引导攻击追加次数",
            "4", "2", "2",
            "击杀目标后最多再引导几次。",
            "击杀目标后自动寻找下一个目标继续攻击。总攻击次数 = 这个值 + 1：6.4 默认 4（共五次），6.5/6.6 默认 2（共三次）。",
            "引导循环 0x004212F1：inc 计数后 cmp 本值；6.4/6.5/6.6 指令 0x0042133D，字节 80 7D F8 ?? 73。",
            [Link("引导攻击追加次数", "击杀后再引导几次", "guided-attack-count",
                "4", "2", "2", "0x00421340")]),
        new("furious-attack", "连击", "奋战攻击目标数",
            "8", "8", "8",
            "奋战会依次打几个相邻目标。",
            "奋战会依次攻击一组相邻目标，引导攻击共用这份列表。8 = 周围八格全算，4 = 只算十字四格。",
            "列表构建 6.4/6.5 0x00405BE8、6.6 0x00405BF2；循环 cmp 本值后查方向表；6.4/6.5 指令 0x00405C16、6.6 0x00405C13。",
            [Link("奋战攻击目标数", "一次奋战打几个目标", "furious-attack-targets",
                "8", "8", "8", "6.4/6.5 0x00405C16；6.6 0x00405C13")]),
        new("physical-damage", "伤害", "物理攻击伤害",
            "25", "25", "25",
            "攻方等级加 25，再加武力减统帅的差÷2，保底 1 点。",
            "伤害 = 攻方等级 + 25，再用攻方武力与守方统帅算能力差：攻方高就加“差值÷2”，守方高就减“差值÷2”；最低保底 1 点。之后才结算突破、偷袭、疾风、固定增伤、吸血、猛击、盾反等特效。",
            "物理伤害函数 0x0043BC62：基础经 0x0043BD2F call 0x00412674（0x4065D0 读 char+0x2C 等级）取攻方等级，加 25 在 0x0043BD34；能力对 0/1 来自 0x0043BCF5；能力差 shr 1 在 0x0043BD45/0x0043BD52；保底 inc eax 在 0x0043BD64。",
            [Link("物理攻击基础伤害", "能力差之外先加的固定伤害", "physical-damage-base",
                "25", "25", "25", "0x0043BD36"),
             Fixed("能力差除数", "双方武力/统帅差除以几", "2", "2", "2",
                "0x0043BD45、0x0043BD52 的 shr eax,1", "指令编码，只读"),
             Fixed("保底伤害", "最低打掉多少", "1", "1", "1",
                "0x0043BD64 inc eax", "指令编码，只读"),
             Link("疾风攻击每点增伤", "6.4/6.5 目标能力每低 1 点加 5%；6.6 为特效值 N 的倍率", "swift-attack-bonus",
                "5", "5", "5（兵种76槽）", "6.4/6.5 0x0043BD88；6.6 兵种76槽 +0xE2F5D"),
             Link("疾风攻击补正值（6.6）", "6.6 用 12 − 目标能力，再乘特效值 N", "swift-attack-offset",
                "—", "—", "12", "0x0043BD80 add eax,0Ch（0x0043BD82 为 nop）"),
             Link("突破攻击伤害加成", "突破后伤害加多少百分比", "breakthrough-damage-bonus",
                "40", "40", "40", "0x004110C1"),
             Link("偷袭攻击每档增伤", "侧击/背击每档加多少", "sneak-attack-step",
                "—", "25", "25", "0x004D2767"),
             Link("固定值基础加成", "固定增伤/减伤的基础值", "fixed-damage-basis",
                "—", "10", "15", "0x00448F8B"),
             Link("吸血攻击吸取上限", "最多按伤害的几成回血", "drain-attack-cap",
                "100", "100", "100", "0x00406B9A/0x00406B9E"),
             Link("猛击伤害比例上限", "猛击最多打掉目标当前 HP 的几成", "heavy-strike-cap",
                "100", "100", "100", "0x00422036/0x0042203A（6.4 0x00422039/0x0042203D）"),
             Link("盾反反弹比例上限", "盾反最多反弹攻击者当前 HP 的几成", "shield-counter-cap",
                "100", "100", "100", "0x0042205F/0x00422063（6.4 0x004220B5/0x004220B9）")]),
        new("strategy-damage", "伤害", "策略攻击伤害",
            "25", "25", "25",
            "攻方等级加 25，再加智力差的÷3，保底 1 点。",
            "伤害 = 攻方等级 + 25，再用攻方智力与守方智力算能力差：攻方高就加“差值÷3”，守方高就减“差值÷3”；最低保底 1 点。之后才结算策伤保底/限伤、MP辅助、绝对策略伤害、化险为夷、攻守兼备等特效。",
            "策略伤害函数 6.4/6.5 入口 0x0043C022，6.6 同段；基础经 0x0043C0F6 call 0x00412674（0x4065D0 读 char+0x2C 等级）取攻方等级，加 25 在 0x0043C0FE（6.6 0x0043C10A 起）；能力对 2/2 在 0x0043C0F3；能力差除以 3 在成对 0x0043C126/0x0043C139；保底在 0x0047FA9E。",
            [Link("策略攻击基础伤害", "能力差之外先加的固定伤害", "strategy-damage-base",
                "25", "25", "25", "6.4/6.5 0x0043C101；6.6 0x0043C118"),
             Link("策略伤害能力差除数", "双方智力差除以几", "strategy-damage-divisor",
                "3", "3", "3", "0x0043C126、0x0043C139"),
             Fixed("保底伤害", "最低打掉多少", "1", "1", "1",
                "0x0047FA9E 返回 max(伤害−能力差, 0) 后再保底", "指令编码，只读"),
             Link("策伤保底追加比例", "已高于保底时再加多少", "strategy-floor-bonus",
                "—", "20", "—", "0x0043D3EA、0x0043D43A"),
             Link("MP辅助策略基础加成", "按剩余 MP 加伤时额外加多少", "mp-strategy-bonus",
                "—", "—", "10", "0x00435143"),
             Link("绝对策略伤害追加比例", "已高于下限时再加多少", "absolute-strategy-damage-bonus",
                "—", "—", "15", "0x00434187"),
             Link("限制策略伤害额外减伤", "未超上限时再减多少", "strategy-damage-limit-cut",
                "—", "—", "20", "0x00434243"),
             Link("化险为夷最大伤害比例", "一次伤害最多占最大 HP 的几成", "dodge-damage-cap",
                "—", "—", "10", "0x00449151"),
             Link("金钱防御每点伤害消耗", "每挡 1 点伤害花多少金钱", "money-defense-cost",
                "—", "—", "10", "0x004212C3"),
             Link("攻守兼备增伤触发 HP 线", "一方 HP 不低于几成才增伤", "offense-defense-add-line",
                "—", "—", "40", "0x00441E3A"),
             Link("攻守兼备减伤触发 HP 线", "另一方 HP 不高于几成才减伤", "offense-defense-reduce-line",
                "—", "—", "60", "0x00441E84"),
             Link("孤勇者减伤上限", "周围敌人越少最多减到几成", "lone-brave-reduction-cap",
                "—", "—", "100", "0x0041A982/0x0041A986")]),
        new("counter-damage", "伤害", "普通反击伤害",
            "—", "3/4", "3/4",
            "没有强化反击时，反击伤害按攻击伤害的 3/4 结算。",
            "没有强化反击时，反击伤害 = 原攻击伤害 × 3 / 4。有强化反击时改按已损失 HP 比例加成，不走这份固定份数。6.4 未定位到同一份固定份数。",
            "反击伤害函数 0x004E31B3；6.5/6.6 指令 0x004E3214 执行 imul eax,ecx,3; shr eax,2；6.4 同址为空。",
            [Link("普通反击伤害份数", "反击按攻击伤害的几份结算", "counter-damage-share",
                "—", "3", "3", "0x004E3216")]),
        new("personal-exp", "经验", "个人经验",
            "2×差+6；击杀 +48 或 64/(差+2)",
            "2×差+6；击杀 +48 或 64/(差+2)",
            "2×差+6；击杀 +48 或 64/(差+2)",
            "攻击者每次攻击都会累计个人经验；等级越低打高等级敌人越多，击杀还有额外一笔；道具效果 0x26 也会把道具效果值直接加到当前经验。",
            "设攻方等级 AL、守方等级 DL。基础经验 = 2×clamp(DL−AL,−1,47)+6。若本次伤害 ≥ 目标当前 HP（击杀）：目标 Data 号等于全局 0x496C96 时额外 +48，否则额外 +64/(max(AL−DL,0)+2)。0x496C96 由战场变量装载 0x004122C1 从剧本变量 0x02 写入；最后乘经验倍率；同一行动多次攻击只把最大值写进 ctx+428。",
            "个人经验 0x004037A3（6.4/6.5 同码，6.6 同址重排）；主路径 6.5 0x00406023 调用、0x00406043 写 ctx+428。等级差钳位 0x00403847/0x0040384D，基础 0x00403855；击杀 6.4/6.5 0x00403824/0x0040383A/0x00403834，6.6 0x0040381E/0x00403833/0x0040382E；特殊目标装载 0x004122C1（表 0x004123BE）。",
            PersonalExpConstants),
        new("weapon-exp", "经验", "武器经验",
            "基础3；攻高-1；暴击+1；无伤2",
            "基础2；攻高-1；暴击+1；无伤2",
            "基础3；攻高-1；暴击+1；无伤1",
            "攻击者的武器在每次攻击后获得经验：造成伤害给基础值，等级高、暴击有加减，未造成伤害另有固定值。",
            "经验开关 ctx+600≠0 且武器槽有装备才结算。造成 HP 或 MP 伤害时：经验 = 基础值；攻方等级高于守方 −1；暴击 +1。没有造成任何伤害时直接取“无伤害值”。最后乘经验倍率并累加到 ctx+42C。",
            "武器经验 0x00403870：基础立即数 0x004038FA（6.4/6.6 为 3，6.5 为 2）；等级 −1 在 0x00403903 dec ecx；暴击 +1 在 0x00403910 inc ecx（ctx+604 由 0x00405F1A 置 1）；无伤害立即数 0x00403919（6.4/6.5 为 2，6.6 为 1）。写入 0x00406054 add [ctx+42C],eax。",
            WeaponExpConstants),
        new("armor-exp", "经验", "防具经验",
            "基础3；无伤扣1；攻低-1",
            "基础3；无伤扣2；攻低-1",
            "基础4；无伤扣3；攻低-1",
            "攻击者的每件防具单独累计经验：目标不是我方时才结算，没有造成伤害会扣减。",
            "目标阵营字节 [unit+5] 非 0（不是我方）才结算。基础值按防具槽逐个记；攻方等级低于守方 −1；没有造成 HP/MP 伤害时从基础上扣无伤害值。乘经验倍率后按防具槽写入 ctx+430+槽×4。",
            "防具经验 0x00403A8A：基础立即数 0x00403A8E（3/3/4）；等级 −1 在 0x00403AF3 dec；无伤害扣减立即数 0x00403AFB（1/2/3）；写入 0x00406074。",
            ArmorExpConstants),
        new("strategy-exp", "经验", "策略经验",
            "类型2+20；击杀8×差+32≤200；普通4×差+10≤100",
            "类型2+20；击杀8×差+32≤200；普通4×差+10≤100",
            "类型2+20；击杀8×差+32≤200；普通4×差+10≤100",
            "施法者使用策略后获得的经验：按策略类型、是否击杀和双方等级差分档。",
            "策略记录 +0x0B 的类型为 2 时固定 +20；类型为 1 时走普通档。其余情况若是伤害类策略且造成击杀：攻方低于守方时 8×级差+32（封顶 200），攻方高于守方时 max(32−4×级差,0) 且最低 10；未击杀走普通档：攻方低于守方时 4×级差+10（封顶 100），攻方高于守方时 max(10−级差÷2,0) 且最低 5。目标 Data 号等于 0x496C96 时经验 ×2，最后乘经验倍率。策略经验实际分三路缓存：个人经验取最大值写 ctx+0x502（0x0044DE9E），武器经验取最大值写 ctx+0x506（0x00421363），防具经验按策略 ID 写 ctx+0x50A+ID（0x00421409）；再由 0x0041A0AC 统一结算到 0x004088CD 与 0x004082DD（6.4 入口 0x00451085）。",
            "策略经验 0x00420EFB（6.4/6.5 同码，6.6 重排）；启用开关 ctx+54C；类型读取 0x00425AC7 movzx eax,byte [ecx+0Bh]，策略记录 0x00484002 imul ecx,61h + 0x4A3E77。6.5 立即数：+20 0x00420F25、击杀 0x00420FB5/0x00420FBC/0x00420FCD/0x00420FDE、普通 0x00421001/0x00421008/0x0042102E、翻倍 0x00420FE8。",
            StrategyExpConstants),
        new("per-turn-exp", "经验", "每回合经验（特效 3/4/5）",
            "特效值×(装备第8类成长+100)/100",
            "特效值×(装备第8类成长+100)/100",
            "特效值×(装备第8类成长+100)/100",
            "“每回合获得经验 / 每回合武器经验 / 每回合护具经验”三个特效在单位回合结束时统一结算，按同一经验倍率放大后分别加到角色与装备经验。同一函数还先算回合 HP/MP 增量（按最大 HP/MP 截断）并写回单位：地形恢复由站位坐标查 0x435991/0x412557/0x41E467，地形 0x12→25、0x13/0x14/0x16→20、0x15→15，HP 按最大 HP 的百分比、MP 按定值；经验循环只对我军（0x0043FF54 判定）执行。",
            "每回合结算函数 0x0043CE15 循环 3 次，依次查询第 3/4/5 项（个人经验、武器经验、防具经验）的值，累加后再乘经验倍率 0x00407FAA（装备侧第 8 类成长累计 + 100）；个人经验加进 char 经验并走升级结算 0x004088CD，武器/防具经验分别走 0x004082DD 槽 0 / 槽 1。选择器表 0x0043CFCD 是装备侧的道具类型过滤值：0x0043CEE9-0x0043CEFC 把 i+3 与表值传给 0x004101D9，0x0041301E 再经 0x0043C794 调 0x00407A17 检查装备（槽 0/1 须为宝物且道具 +0x14 == 表值，槽 2 比 +0x11），命中才由 0x00407AF2 累加对应装备值；未命中时装备侧贡献为 0，因此表值本身会改变结果，而不只是标签。6.4/6.6 用 0x1D/0x1E，6.5 用 0。三件特效都为 0 时跳过结算。",
            "结算入口 6.4 0x0043CE15、6.5 0x0043CDF5、6.6 0x0043CDDD（主体从 0x0043CE20 起同址）；特效查询 0x004101D9 → 0x0041301E → 0x0043C794；装备过滤 0x00407A17/0x00407A1E；装备值累加 0x00407AF2 + 0x00407BA6（op=0，求和，上限 255）；倍率 0x00407FAA + 0x00425AD9；个人经验 0x004088CD；装备经验 0x004082DD；selector 表 0x0043CFCD。同函数 HP/MP 结算：0x4210F4（槽 0；选择子 6.4/6.5 0x1A、6.6 0x67）、0x421106（槽 1，选择子 0x1B）、0x42109C/0x42109A（选择子 0x44，6.4/6.5 只走 0x43C794，6.6 走 0x42518F 槽 0x32）；平坦项 0x417B5A（6.6 0x428A25）。",
            PerTurnExpConstants),
        new("exp-multiplier", "经验", "经验倍率与翻倍",
            "×（装备第8类成长+100）/100；两处×2",
            "×（装备第8类成长+100）/100；两处×2",
            "×（装备第8类成长+100）/100；两处×2",
            "所有经验结算都先乘一个以装备侧第 8 类成长为基础的倍率（不是角色五维），再按两个全局条件翻倍。",
            "经验 = 经验 × (0x00407C35 索引 8 的装备侧成长累计 + 100) / 100。之后 0x00403D5A 再判两个条件：攻方为我军且槽位标志 0x501B00 非 0 → ×2；全局字节 0x500E9A == 1 → ×2。个人、武器、防具、策略经验都走这一条，两处翻倍因此同样作用于武器经验与防具经验。0x501B00 的逐槽标志可由 S 剧本命令 0x39/0x3A 置 3（调度表 0x00420C8E 索引 34/35 → 跳转条目 10 = 0x00420BFD：`cmp al,0x14` 后写 `[0x501B00+部队序号]=3`，序号 <20），并由命令 0x0A 的初始化函数 0x00415ACA 清零 0x501B00 起 0x140 个 DWORD；0x500E9A == 1 有静态写入（6.5 `0x41D69B` 置 1、`0x44EA34` 置 0、`0x4516FC` 自增，另有 `0x410594/0x4225F1/0x423377/0x4233EE/0x465FE0` 的 WORD 写点），阶段判定可达；按静态顺序最多 ×4，尚未实机验证。",
            "倍率函数 0x00421053（6.6 入口 0x0042104F）：0x00407FAA = 0x00407C35(索引 8) + 100（立即数 0x00407FB9）；0x00407C35 汇总装备侧第 8 类数值（0x00429AD7 过滤类别、0x0040B3D7 按 (装备等级−1)×道具 +0x17 累加、宝物命中时 0x00452825 对索引≥7 原样返回），因此倍率来源是装备成长而非角色五维；0x00425AD9 做 经验×百分比/100；翻倍函数 0x00403D5A（0x0042545F 读 0x501B00、0x00403D6C 读 0x500E9A）。调用点：个人经验 0x00403865、武器经验 0x00403926、防具经验 0x00403B09、策略经验 0x0042103B（6.6 对应 0x00403926/0x00403B09/0x0042102A 调 0x0042104F）。",
            ExpMultiplierConstants),
        new("merit-record", "功勋", "五维功勋记录",
            "0x508400+ID×14；7 字段",
            "0x508400+ID×14；7 字段",
            "0x508400+ID×14；7 字段",
            "每个角色有 7 个 2 字节功勋字段：五维各一项，再加 HP、MP 两项；读取时叠加到基础能力；战斗事件另记到本场战功表。",
            "永久功勋记录地址 = 0x508400 + 角色ID×14。字段 0..4 分别为五维功勋，字段 5/6 为 HP/MP 功勋。基础能力读取函数 0x00407C35（6.6 0x00407C29）在 0x0041055D 读对应字段并叠加；只有我军（char+2A==0）参与叠加。写入函数 0x00408B52 支持模式 0 设值、1 累加、2 扣减，角色 ID ≥ 102 直接丢弃；0x508400 只有读取与两条剧本命令写入。战斗事件与道具效果 0x29（获得功勋）写入另一张表：0x508000 + ID×10 的 5 个 2 字节字段，累加函数 0x42AB8E 在 0x500E9A==1 且（0x505FDC==0 或 0x505F5C≠0）时把值 ×2；策略使用经 0x42AA22 给字段 1 加 2（0x2D 类 +4）；6.5/6.6 由 0x423EAD 清零 5 字段并累计到 0x505F40，6.4 无 0x423EAD 对应函数，只有 0x408FA0 在战后按 char+2 位图清理并累计。累加前 0x42AB8E 调 0x412A87/0x42518F 查询特效 0x45（6.5 名称“获得功勋”、6.6“功勋卓著”）；总额 0x505F40 由 0x456CB4/0x456DA6 消费（缓冲区 0x4FF3B8/0x4FFF68/0x500B60），静态未发现写入永久功勋 0x508400。战后每个单位另由 0x42A8EE 给本场战功字段 0 +1，并按条件表（6.4/6.5 0x407826、6.6 0x41A139，内容均为 00 03 04）给字段 3（战斗上下文 +608≥1）与字段 4（+604==1）各 +1；6.6 的派发入口搬到 0x40DC5C。0x423F4B 在开关 0x505FA8 与 char+2 允许位下，用本场战功按 0x42AC8F 的递增成本（50/65/75…）抵扣成长值，连续开关 0x501A74；三开关初值 0，默认关闭。",
            "读取 0x0041055D；基础能力叠加 6.4/6.5 0x00407D74、6.6 0x00407D7F；写入 0x00408B52（0x004120AD、0x004203D2）；取永久记录 0x004224A8；本场战功取记录 0x0042ACD2（0x508000+ID×10）；累加 0x0042AB8E；战后派发 0x0042A8EE/0x0042AADB（6.6 0x0040DC5C）；条件表 0x00407826（6.6 0x0041A139）；兑换 0x00423F4B（开关 0x505FA8/0x501A74）；出阵计数 0x00406080 读 0x507800（6.4）/0x508A00（6.5·6.6）；结算 6.5/6.6 0x00423EAD（6.4 无对应函数）；清理/累计 0x00408FA0（0x0044ECBD 调用）；道具入口 0x004224D4。除 0x423EAD 与 6.6 派发入口外三基底同址。",
            MeritConstants),
        new("merit-allocation", "功勋", "战功点分配（五维成长）",
            "×1；门槛 50 或 (v−79)×10+55；上限 100",
            "×25；门槛 50 或 (v−79)×10+55；上限 110",
            "×50 或 ×10；门槛 50 或 (v−79)×10+55；上限 110",
            "战后累计的战功点先按倍率放大，再按当前成长值逐点扣门槛，提升五维成长值与对应能力；不足门槛的余额转回本场战功。",
            "分配函数 0x0046206C：若 0x505FAC 非 0 且 0x5083FC 非 0，则 pool = 0x5083FC × 第二实参。对 5 个槽位 i：v = char[0x21+i]；v 达到上限（6.4 为 100，6.5/6.6 为 110）跳过；v < 80 时门槛 50，否则门槛 = (v−79)×10+55；pool ≥ 门槛时 pool −= 门槛、v+1、word[char+0x11+2i]+1，并在同槽位继续；余额经 0x42ACD2/0x42AB8E 写回本场战功。6.4 在函数内内联循环，6.5/6.6 调用 0x42AC8F（第三实参 1 时只判不扣）。",
            "四调用点第二实参：6.4 恒 1；6.5 恒 25；6.6 0x409639/0x42AD3B 为 50、0x40C386/0x44CD8D 为 10。计数器 6.4/6.5 0x4719A9、6.6 0x40BB05，上限 255；分配函数 0x46206C（0x46208A/0x462093/0x46209E）；门槛 0x4620D1-0x4620FE 与 0x42AC94-0x42ACCF；倍率点 0x409639/0x40C386/0x42AD3B/0x44CD8D。",
            MeritAllocationConstants),
        new("battle-variable-load", "战场", "战场变量装载（特殊目标等）",
            "10 变量 → 0x496C94/96 等",
            "10 变量 → 0x496C94/96 等",
            "10 变量 → 0x496C94/96 等",
            "战斗侧从剧本全局变量装载 10 个参数到战场全局；个人经验的“特殊目标 +48”就取自其中一个值。",
            "装载函数 0x004122C1 按表 0x004123BE 读取 10 个剧本变量（0x004183F7），再写入 0x494FD0、0x496C9F、0x492F90+0x3D0E、0x501BF4、0x496C94/96、0x496C98/9A 等全局。第 6 个读取值（剧本变量 0x02）写入 0x496C96，并在 0x496C94 记录“值 != 0xFFFF”的有效标志；个人经验用它和击杀目标 Data 号比较。变量/命令的剧本名称尚未闭环。",
            "装载 0x004122C1；变量表 0x004123BE = 26 26 04 3E 32 02 32 02 47 22；读取 0x004183F7；写入 0x0041231C-0x0041238C（0x494FD0、0x496C9F、0x492F90+0x3D0E、0x501BF4、0x496C94/96、0x496C98/9A）。三基底同址。",
            [
                Fixed("变量表", "10 个剧本变量索引", "26 26 04 3E 32 02 32 02 47 22",
                    "26 26 04 3E 32 02 32 02 47 22", "26 26 04 3E 32 02 32 02 47 22",
                    "0x004123BE 字节表；0x004122D9 movzx edx,byte [eax+4123BEh]", "公式输入，只读"),
                Fixed("特殊目标写入", "第 6 个读取值写入特殊目标全局", "0x496C96", "0x496C96", "0x496C96",
                    "0x00412366 mov eax,[ebp-1Ch]；0x00412369 mov [0x496C96],ax", "公式输入，只读"),
                Fixed("有效标志", "值 != 0xFFFF 时置 1", "0x496C94", "0x496C94", "0x496C94",
                    "0x00412357 cmp edx,0FFFFh；0x00412360 mov [0x496C94],ax", "指令编码，只读"),
                Fixed("第二目标写入", "第 8 个读取值写入第二目标全局", "0x496C98/9A", "0x496C98/9A", "0x496C98/9A",
                    "0x0041237D mov [0x496C98],ax；0x00412386 mov [0x496C9A],ax", "公式输入，只读"),
                Fixed("战场标志", "第 1 个读取值 !=0 → 0x494FD0", "0x494FD0", "0x494FD0", "0x494FD0",
                    "0x00412316 neg eax；0x0041231C mov [0x494FD0],ax", "公式输入，只读"),
                Fixed("其它写入", "第 2/3/4 个值分别写 0x496C9F、0x492F90+0x3D0E、0x501BF4",
                    "0x496C9F 等", "0x496C9F 等", "0x496C9F 等",
                    "0x00412325/0x00412332/0x0041234D", "公式输入，只读"),
                Fixed("命令名称", "剧本变量 0x02 的命令语义尚未闭环", "未闭环", "未闭环", "未闭环",
                    "0x004183F7 读取剧本变量值", "公式输入，只读")
            ]),
        new("char-level-exp", "经验", "角色升级经验",
            "每级150；上限80",
            "150/200/250/300 分段；上限60",
            "每级250；上限99",
            "战后把角色经验加到 char+0x2D；经验达到阈值就升级，满级后经验固定为 255。",
            "角色经验结算 0x004088CD：读当前经验 char+0x2D、等级 char+0x2C，循环扣减阈值并升级（0x00408D52 做成长），满级后写 255。阈值：6.4 固定 150、上限 80；6.5 每 20 级一档，阈值 = (min(等级/20,3)+3)×50（150/200/250/300），上限 60；6.6 固定 250、上限 99。6.5 的分段阈值在同一次结算中只算一次。",
            "角色经验 0x004088CD；经验 getter 0x004065C7、等级 getter 0x004065D0；升级成长 0x00408D52；6.5 阈值函数 0x0040D21D（分段 20 在 0x0040D225、档位上限 3 在 0x0040D230/0x0040D235、增量 50 在 0x0040D23B）。",
            CharLevelExpConstants),
        new("equip-level-exp", "经验", "装备升级经验",
            "普通100/上限5；宝物200/上限9",
            "普通150/上限5；宝物200/上限9",
            "普通100/上限9；宝物200/上限15",
            "武器与防具各自有等级和经验：战后把战斗经验加到装备上，满阈值就升级并成长。",
            "装备经验结算 0x004082DD：只处理槽位 0（武器）与 1（防具），经验在 char+0x2E+槽×3+2、等级在 +1。阈值按道具记录 +0x11 的 bit0 分宝物/普通；宝物 200、普通 100（6.4/6.6）或 150（6.5）。上限宝物 9/9/15、普通 5/5/9。循环扣减并调用 0x004083C6 做装备成长；满级后经验写 255。使用策略还会按策略 ID 计算一笔装备经验：基础 3（6.6 4），目标等级更高时 −1，乘经验倍率后缓存到 ctx+0x50A+ID，再写入防具槽 1（0x00421409 → 0x004082DD）。",
            "装备经验 0x004082DD；宝物判定 0x0040B4E1（+0x11 bit0）；等级 getter 0x004032DF、经验 getter 0x00409680、等级 setter 0x00403286、经验 setter 0x0040329B；满级标记 0x0040839D；武器槽调用 0x00406C95、防具槽调用 0x00405B05。",
            EquipLevelExpConstants),
        new("ability-write", "功勋", "能力/成长/HP/MP 写入分派",
            "上限 9999；成长 100",
            "上限 9999；成长 100",
            "上限 9999；成长 100",
            "同一个字段号在不同入口里分别代表五维、HP/MP、成长值或状态；分派函数决定“加多少、封顶多少”。",
            "增量入口 0x406ECA：字段 0..4 写五维 word[rec+0x11+i×2]，min(旧+值,9999)；字段 5 写最大 HP（dword +0x1B，会顺带清零 +0x1D/+0x1E）；字段 6 写最大 MP（word +0x1F）；字段 7/8 改当前 HP/MP（走 0x45AA37，模式字节 0x505F30=1 表示增加）；字段 9 无操作；字段 10..14 写成长值 byte[rec+字段+0x17]，封顶 100；字段 15 写 0x501A84 的单位槽字节。直接设置入口 0x407027 用 min(值,0x270F)/min(值,0xFFFF) 覆盖同名字段，字段 7/8 置 0x505F30=2 直设。",
            "0x00406ECA：0x00406ED2 cmp al,0Fh；0x00406EDC cmp dword [ebp+10h],1；0x00406EE7 push 270Fh；0x00406F09 sub eax,5 + 0x00406F0C jmp [eax*4+406FC5h]；表 0x406FC5 三基底同为 13 6F 40/31 6F 40/96 6F 40/96 6F 40/B8 6F 40；0x00406F1E push dword [ecx+1Bh]；0x00406F2C mov dword [ecx+1Bh],eax；0x00406F5B push 64h；0x00406F88 add ecx,501A84h；0x00406F96 mov byte [505F30h],1；0x00407083 mov byte [505F30h],2；0x0040DA4D mov ecx,dword [505F30h]；0x00407027 直接设置（0x00407042 cmp dx,270Fh / 0x00407058 cmp edx,0FFFFh / 0x004070BD mov word [ecx+4],dx + 0x00423E30）；0x0045AA37 索引 7/8 → 0x0041B500/0x0043F6DB、0x00472840/0x0043F715",
            AbilityWriteConstants),
        new("troop-tier", "功勋", "兵种成长档位与前置积分",
            "档长 20；兵种≤59",
            "档长 20；兵种≤59",
            "档长 20；兵种≤59",
            "兵种 ID 按 %3 分三档，每档 20 级；HP/MP 重算还要加上“前一个兵种基础×2”。",
            "兵种 ID 必须 ≤0x3B（59）；0x408A60 以 20 级为块：基础 = v(当前兵种)×max(等级−(兵种%3)×20,0) + v(前兵种)×min(等级,(兵种%3)×20)（%3==2 时先按 40 级比较）。升级条件 0x41D3DC 要求等级 ≥ (兵种%3+1)×20，兵种%3==2 或兵种>59 直接不可升。HP/MP 重算 0x4149CF 额外加 0x413FAC：6.4/6.5 = 2×Σ v(兵种−1..兵种−r)，6.6 = 2×r×v(当前兵种)。",
            "0x00408A66 push 14h（块长）；0x00408A73 cmp al,3Bh；0x00408A8B shl ecx,1（%3==2 时按 40 比较）；0x0041FBF8 mov cl,3 + 0x0041FBFA idiv ecx（兵种%3）；0x0041D3EB cmp al,3Bh；0x0041D406 cmp edx,2；0x0041D42E inc edx + 0x0041D42F imul edx,[ebp-8]；0x00413FF9 shl dword [ebp-4],1；0x00414A3B call 0x00413FAC",
            TroopTierConstants),
        new("troop-up", "功勋", "兵种提升执行",
            "兵种+1；演出10帧",
            "兵种+1；演出10帧",
            "兵种+1；演出10帧",
            "0x41D468 把兵种 +1，并给最大 HP/MP 各补“前兵种基础×2”，随后播放 10 帧提升演出。",
            "流程：编号 0x7F 时先 0x41D124 解析目标；0xFF 直接退出；取 unit/officer 后 0x406610 读兵种、inc 后 0x40E01F 写回 byte[rec+0x2B]（兵种 +1）；接着字段 5/6（最大 HP/MP）各加 0x413FAC(字段, rec, 1) = 2×v(前兵种)；随后 0x401D4E 缓冲拷贝、0x44FA7E/0x44FA1F 取文本、10 帧演出循环，最后 0x42F699(2, “兵种提升”文本 0x48B698, 新兵种) 与 UI 刷新。升级条件不在此函数，见 0x41D3DC。",
            "0x0041D468 三基底前 8 字节 55 8B EC 6A 05 51 6A 01；0x0041D478 编号 7Fh 分支；0x0041D489 mov byte [edx+3],al；0x0041D48E call 0x004061F9；0x0041D50B call 0x00406610；0x0041D510 inc eax；0x0041D515 call 0x0040E01F；0x0041D52C call 0x00413FAC + 0x0041D53A call 0x00406ECA；0x0041D5B2 cmp dword [ebp-4],0Ah；0x0041D653 push 48B698h + 0x0041D65A call 0x0042F699",
            TroopUpConstants),
        new("equip-growth", "经验", "装备成长累计（经验倍率基数）",
            "每级 +0x17；类型≤1",
            "每级 +0x17；类型≤1",
            "每级 +0x17；类型≤1",
            "经验倍率的“装备成长”项 = 各装备 (等级−1)×每级成长 之和，宝物另有按类型的附加。",
            "0x407C35(索引) 对武器/防具两槽逐件累加：先取 0x40B3D7(道具记录, 装备等级) = (等级−1)×byte[道具+0x17]（仅当 0x40B444 映射类型 ≤1），再用 0x429AD7 做类别过滤（类别 0x0A 对索引 0/2 例外），最后对宝物（+0x11 bit0）且类别映射等于索引的装备追加 0x4200F8(道具+0x16, 装备等级) 与 0x452825(单位, 索引)。结果加 100 即经验倍率（0x407FAA）。",
            "0x00407C35 循环 0x00407C49 cmp al,1；0x00407C5A call 0x004032DF；0x00407C6C call 0x0040B3D7；0x00407C7A call 0x00429AD7（6.6 0x00405670）；0x00407C94 add [ebp-0Ch],eax；0x00407CA5 call 0x0040B4E1；0x00407C98 call 0x0040678E；0x00407CA5 call 0x0044661A；0x00407CAD call 0x004200F8（6.6 0x004200F5）；0x00407CB8 call 0x00452825；0x0040B3FB 循环 cmp [ebp-8],al；0x0040B444 movzx eax,byte [ecx+11h] + 0x0040B44B cmp al,14h + 0x0040B453 cmp al,1Ah；0x0040C464 cmp eax,1",
            EquipGrowthConstants),
        new("treasure-growth", "经验", "宝物成长与百分比换算",
            "×成长/100；门控 2",
            "×成长/100；门控 2",
            "×成长/100；门控 2",
            "宝物对能力的加成先按道具类型与装备等级算“成长值”，再换算成能力的百分比。",
            "0x4200F8(道具+0x16, 等级) 按道具 +0x14 类型分支：6.5 下 0x1F → +等级、0x55 → ×(等级+1)、0x2F → ×等级+0x1E、0x33(原值4)→+3、0x32→×2、0x36/0x42/0x46→+1、其它→×3/2；等级≥10 再查表 0x46236F[类型−0x1A]（0xFE 表示不覆盖）。随后 0x452825(索引) 在 索引<7 且 0x46230F[索引]==2 时取该字段当前能力（0..4 word+0x11+i×2、5 dword+0x1B、6 word+0x1F），用 0x425AD9 换算为 能力×成长/100。",
            "0x004200FB movzx edx,dl；0x004200FE movzx ecx,byte [eax]；0x00420101 movzx eax,byte [eax-2]；0x00420131 add cl,dl；0x004200DD imul ecx,edx；0x004200ED add ecx,1Eh；0x00420166 imul ecx,ecx,3 + 0x00420169 shr ecx,1；0x00420177 sub eax,1Ah + 0x0042017A mov al,[eax+46236Fh] + 0x00420180 cmp al,0FEh；0x00452842 cmp byte [eax+46230Fh],2；0x00452865 mov cx,word [edx+eax*2]；0x0045287D call 0x00425AD9；0x00425AE5 mov ecx,64h",
            TreasureGrowthConstants),
        new("growth-gap", "经验", "能力成长缺口与基准补正",
            "缺口≥0；基准×等级",
            "缺口≥0；基准×等级",
            "缺口≥0；基准×等级",
            "0x436DE1 先确定每级基准（特效值或兵种字节+成长档的一半），再算“基准×等级 + 成长值 + 功勋 − 当前能力”的缺口。",
            "流程：索引 ≥5 直接返回传入值；否则 0x42518F(0x3D, 0x5C, 选择子, 0) 查特效（0x40B922 判阵营后走 0x4101D9 或 0x41301E），特效值非 0 时作为每级基准，否则用 (兵种字节 + 成长档) >> 1；随后 基准×等级 + byte[rec+索引+0x21] + 永久功勋，减去当前能力并取下界 0，再加传入成长值；同时返回合成值（edx）供 0x452825 作为宝物成长基数。6.6 入口 0x436E02，基准改走 0x407D48。",
            "0x00436DE9 cmp dword [ebp+8],5 + 0x00436DED jae；0x00436DF3-D [ebp+8] 压栈 0x3D/0x5C/选择子/0；0x00436E17 call 0x00406610；0x00436E1E call 0x0041B782；0x00436E26 call 0x00436CA3；0x00436E32 call 0x0041A534；0x00436E3A shr eax,1；0x00436E42 movzx edx,byte [ecx+2Ch] + 0x00436E46 imul eax,edx；0x00436E52 add eax,edx（+0x21 成长值）；0x00436E68 call 0x0041055D；0x00436E82 movzx edx,word [ecx+edx]；0x00436E8D mov eax,edx + 0x00436E8F sub eax,edx + 0x00436E91 add eax,[ebp-8]",
            GrowthGapConstants),
        new("effect-dispatch", "经验", "特效查询分派（我方/敌方）",
            "模式 6.4=1；6.5/6.6=2",
            "模式 6.4=1；6.5/6.6=2",
            "模式 6.4=1；6.5/6.6=2",
            "同一个特效查询入口会按“当前活动方”自动切到我方或敌方的实现；6.4 与 6.5/6.6 的函数地址不同。",
            "0x42518F(索引, 选择子, 模式, 0) 把 4 参透传给 0x40B922（判定 0x40B913()==3，0x40B913=0x41EDEF(0x4AC63C)），返回 1 走 0x4101D9（按 unit 直查，内部先 0x426A07(0,0,0,0,0) 取默认并与 0x505F78 比较），返回 0 走 0x41301E（0x40BE7D 取 ID → 0x4198BE(0x500C3B, …) → 0x43C794 → 0x413009 → 0x40BF2F）。6.4 的 0x42518F 起 44 字节为 90（函数不存在），等价函数 0x412A87，5 处调用点全部指向它。",
            "0x0042518F push 4 参 + 0x0042519F call 0x0040B922 + 0x004251AB call 0x004101D9 + 0x004251B2 call 0x0041301E + 0x004251BA ret 10h；0x0040B922 cmp al,3 + sete cl；0x0040B913 call 0x41EDEF(0x4AC63Ch)；6.4 0x00412A87 同形；0x004101D9 0x004101E4 call 0x426A07；0x004101F3 cmp ecx,[505F78h]；0x0041301E 0x00413022 call 0x40BE7D + 0x00413037 call 0x4198BE + 0x00413049 call 0x43C794 + 0x00413053 call 0x413009",
            EffectDispatchConstants),
        new("merge-mode", "经验", "模式字节与特效合并规则",
            "模式 0/1/2/3",
            "模式 0/1/2/3",
            "模式 0/1/2/3",
            "全局模式字节 0x4AC63C 决定特效查询走哪条分支；多处合并使用同一套 mode 规则。",
            "0x40B913 直接返回 byte[0x4AC63C]（0x41EDEF 仅是 byte[ecx]），0x40B922 将其与 3 比较；0x4AC63C 的静态写点：0x416A78 置 2、0x416A91 自增到 3、0x43C015 置 3（紧邻策略伤害入口 0x43C022），初值 0。合并函数 0x40BF2F(mode,a,b)：0 求和、1 取大、3 按位或、其它在 a==7 时保留否则取大；0x413009 在 mode==2 且 edx==0 时把 edx 设为 eax 再合并。",
            "0x0040B916 mov ecx,4AC63Ch；0x0040B91B call 0x0041EDEF；0x0041EDF2 movzx eax,byte [ecx]；0x0040B92C cmp al,3 + 0x0040B92E sete cl；0x00416A78 C6 05 3C C6 4A 00 02；0x00416A91 FE 05 3C C6 4A 00；0x0043C015 C6 05 3C C6 4A 00 03；0x0040BF32 test ecx,ecx + 0x0040BF36 add eax,edx + 0x0040BF4C or eax,edx + 0x0040BF50 cmp al,7；0x0041300C cmp ecx,2 + 0x00413015 mov edx,eax + 0x00413017 call 0x0040BF2F",
            MergeModeConstants)






    ];

    private static readonly HashSet<string> ExperienceConstantIds = new(StringComparer.Ordinal)
    {
        "personal-exp-base", "personal-exp-kill-flat", "personal-exp-kill-ratio-num",
        "personal-exp-kill-ratio-offset", "exp-multiplier-base", "weapon-exp-base",
        "weapon-exp-no-damage", "armor-exp-base", "armor-exp-no-damage",
        "char-exp-max-level", "char-exp-threshold", "char-exp-band-65", "char-exp-step-65",
        "equip-exp-threshold-special", "equip-exp-threshold-normal",
        "equip-level-cap-special", "equip-level-cap-normal"
    };

    private static readonly IReadOnlyDictionary<string, int> ConstantUsage = Definitions
        .SelectMany(definition => definition.Constants)
        .Where(constant => constant.ConstantId != null)
        .GroupBy(constant => constant.ConstantId!, StringComparer.Ordinal)
        .ToDictionary(group => group.Key, group => group.Count(), StringComparer.Ordinal);

    private static readonly IReadOnlyDictionary<string, BattleFormulaStep[]> StepTemplates =
        new Dictionary<string, BattleFormulaStep[]>(StringComparer.Ordinal)
        {
            ["hit-curve"] =
            [
                new(1, "准备", "A=攻方能力，D=守方能力", "物理命中比敏捷；策略命中比智力+士气。"),
                new(2, "满命中", "A ≥ D×2 → 命中率 = {hit-curve-cap}", "达到两倍直接满命中。"),
                new(3, "高段", "D ≤ A < D×2 → {hit-curve-high-base} + (A−D)×{hit-curve-high-coef}/D", "90～100。"),
                new(4, "中段", "D/2 ≤ A < D → {hit-curve-mid-base} + (A−D/2)×{hit-curve-mid-coef}/(D/2)", "60～90。"),
                new(5, "低段", "A < D/2 → {hit-curve-low-base} + max(A−D/{hit-curve-low-divisor},0)×{hit-curve-low-coef}/(D/{hit-curve-low-divisor})", "30～45。"),
                new(6, "封顶", "命中率 = min(结果, {hit-curve-cap})", "不超过上限。"),
                new(7, "6.6 下限", "命中率 = max(结果, {hit-curve-floor-66})", "仅 6.6 有下限。")
            ],
            ["physical-hit"] =
            [
                new(1, "准备", "A=攻方敏捷，D=守方敏捷", "物理命中看敏捷。"),
                new(2, "套曲线", "命中率 = 命中率曲线(A,D)", "套用命中率曲线。"),
                new(3, "二次判定", "6.4/6.5：未命中且命中率 ≥ {hit-retry-threshold} → 再判一次，命中率 −{hit-retry-deduction}", "最多 {hit-retry-count} 次；6.6 不适用。"),
                new(4, "6.6 下限", "命中率 = max(结果, {hit-curve-floor-66})", "最低 25；6.4/6.5 不适用。"),
                new(5, "结果", "命中 → 进入伤害结算；未命中 → 显示闪避", "最终结果。")
            ],
            ["strategy-hit"] =
            [
                new(1, "准备", "A=攻方智力+士气，D=守方智力+士气", "策略命中看智力与士气。"),
                new(2, "套曲线", "命中率 = 命中率曲线(A,D)", "套用命中率曲线。"),
                new(3, "二次判定", "6.4/6.5：未命中且命中率 ≥ {hit-retry-threshold} → 再判一次，命中率 −{hit-retry-deduction}", "最多 {hit-retry-count} 次；6.6 不适用。"),
                new(4, "6.6 下限", "命中率 = max(结果, {hit-curve-floor-66})", "最低 25；6.4/6.5 不适用。"),
                new(5, "结果", "命中 → 进入策略伤害结算；未命中 → 显示策略闪避", "最终结果。")
            ],
            ["rate-curve"] =
            [
                new(1, "准备", "A=攻方能力，D=守方能力", "暴击比士气；连击比敏捷。"),
                new(2, "满率", "A ≥ D×{rate-curve-full-multiplier} → 发动率 = {rate-curve-cap}", "达到倍数直接满。"),
                new(3, "高段", "D×2 ≤ A < D×3 → {rate-curve-high-base} + (A−D×2)×{rate-curve-high-coef}/D", "20～100。"),
                new(4, "低段", "D ≤ A < D×2 → {rate-curve-low-base} + (A−D)×{rate-curve-low-coef}/D", "2～20。"),
                new(5, "低于守方", "A < D → 1", "低于守方只剩 1%。"),
                new(6, "封顶", "发动率 = min(结果, {rate-curve-cap})", "不超过上限。")
            ],
            ["physical-crit"] =
            [
                new(1, "准备", "A=攻方士气，D=守方士气", "物理暴击看士气。"),
                new(2, "套曲线", "暴击率 = 发动率曲线(A,D)", "套用发动率曲线。"),
                new(3, "封顶", "暴击率 = min(暴击率, {physical-crit-cap})", "不超过上限。"),
                new(4, "随机", "0..99 随机数与暴击率比较", "随机判定。"),
                new(5, "集气", "通过后进入集气池 {physical-crit-pool}", "6.4 池 0；6.5/6.6 池 2。"),
                new(6, "额外伤害", "额外伤害 = 原伤害 × (暴击率+100)/2 / 100", "暴击率 0 → +50%；100 → +100%。"),
                new(7, "特效112", "6.6 再叠加特效 112 的返回值", "仅 6.6。")
            ],
            ["strategy-crit"] =
            [
                new(1, "准备", "A=攻方士气，D=守方士气", "策略暴击看士气。"),
                new(2, "套曲线", "暴击率 = 发动率曲线(A,D)", "套用发动率曲线。"),
                new(3, "封顶", "暴击率 = min(暴击率, {strategy-crit-cap})", "不超过上限。"),
                new(4, "随机", "0..99 随机数与暴击率比较", "随机判定。"),
                new(5, "集气", "通过后进入集气池 {strategy-crit-pool}", "6.4 池 0；6.5/6.6 池 18。"),
                new(6, "额外伤害", "额外伤害 = 原伤害 × (暴击率+100)/4 / 100", "暴击率 0 → +25%；100 → +50%。")
            ],
            ["combo-rate"] =
            [
                new(1, "准备", "A=攻方敏捷，D=守方敏捷", "连击看敏捷。"),
                new(2, "特效52", "有特效 52 → 连击率 = {active-combo-chance}", "默认 100。"),
                new(3, "套曲线", "否则 连击率 = 发动率曲线(A,D)", "套用发动率曲线。"),
                new(4, "集气", "通过后进入集气池 {combo-pool}", "三基底默认 0。"),
                new(5, "结果", "随机判定是否追加一击", "最终结果。")
            ],
            ["combo-damage"] =
            [
                new(1, "连击基数", "第 N 次连击使用连击伤害基数", "N≥2。"),
                new(2, "无强化", "无强化连击：按引擎内部系数逐次衰减", "衰减系数不暴露为常量。"),
                new(3, "有强化", "有强化连击：不再逐次衰减", "强化连击类特效。"),
                new(4, "固定增伤", "追加固定百分比 {combo-damage-bonus}%", "默认 0。")
            ],
            ["active-combo"] =
            [
                new(1, "取发动率", "特效 52 返回 {active-combo-chance}", "默认 100。"),
                new(2, "钳制", "概率函数把上限钳到 100", "0x00437896 / 0x004287A8。"),
                new(3, "随机", "与 0..99 随机数比较", "成功则追加一击。")
            ],
            ["guided-attack"] =
            [
                new(1, "击杀", "击杀目标后寻找下一个目标", "引导链。"),
                new(2, "循环", "已追加次数 < {guided-attack-count} 且找到目标 → 继续攻击", "按次数循环。"),
                new(3, "总次数", "总攻击次数 = {guided-attack-count} + 1", "6.4 默认 4（共 5 次）；6.5/6.6 默认 2（共 3 次）。")
            ],
            ["furious-attack"] =
            [
                new(1, "建列表", "构建相邻目标列表", "方向表 0x004359F5。"),
                new(2, "限制", "列表最多 {furious-attack-targets} 个目标", "8=八格；4=十字。"),
                new(3, "攻击", "依次攻击列表内目标", "0x00417C67。"),
                new(4, "共用", "引导攻击共用这份列表", "0x004212F1。")
            ],
            ["physical-damage"] =
            [
                new(1, "基础", "伤害 = 攻方等级 + {physical-damage-base}", "基础伤害。"),
                new(2, "能力差", "差 = 攻方武力 − 守方统帅", "能力差。"),
                new(3, "攻方更高", "伤害 += 差/2", "除以 2 为指令编码。"),
                new(4, "守方更高", "伤害 −= |差|/2", "除以 2 为指令编码。"),
                new(5, "保底", "伤害 < 1 → 1", "最低 1 点。"),
                new(6, "特效", "之后结算突破、偷袭、疾风、固定增伤、吸血、猛击、盾反", "特效链。")
            ],
            ["strategy-damage"] =
            [
                new(1, "基础", "伤害 = 攻方等级 + {strategy-damage-base}", "基础伤害。"),
                new(2, "能力差", "差 = 攻方智力 − 守方智力", "能力差。"),
                new(3, "除数", "伤害 += 差 / {strategy-damage-divisor}", "除数默认 3。"),
                new(4, "保底", "伤害 < 1 → 1", "最低 1 点。"),
                new(5, "特效", "之后结算策伤保底/限伤、MP辅助、绝对策略伤害、化险为夷、攻守兼备、孤勇者", "特效链。")
            ],
            ["counter-damage"] =
            [
                new(1, "无强化反击", "伤害 = 原伤害 × {counter-damage-share} / 4", "默认 3/4。"),
                new(2, "有强化反击", "按已损失 HP 比例加成", "不走固定份数。"),
                new(3, "6.4", "同址为空，不适用", "显示 —。")
            ],
            ["personal-exp"] =
            [
                new(1, "准备", "AL=攻方等级，DL=守方等级", "等级读取 0x004065D0；攻方 ctx+8，守方 ctx+1。"),
                new(2, "基础", "基础 = 2×clamp(DL−AL,−1,47) + {personal-exp-base}", "等级差限制在 −1..47，全部整数运算。"),
                new(3, "击杀判定", "本次伤害 ≥ 目标当前 HP → 击杀", "目标 HP 由 0x0041B500 读取。"),
                new(4, "特殊目标", "目标 Data 号 = 0x496C96 → 额外 +{personal-exp-kill-flat}", "0x00406604 读 word [0x492F90+0x3D06]。"),
                new(5, "普通击杀", "否则 额外 += {personal-exp-kill-ratio-num} / (max(AL−DL,0)+{personal-exp-kill-ratio-offset})", "整数除法向下取整。"),
                new(6, "倍率", "经验 = 经验 × (第8项能力+{exp-multiplier-base})/100", "倍率函数 0x00421053；0x00403D5A 还会翻倍。"),
                new(7, "写入", "ctx+428 = max(旧值, 本次经验)", "同一行动多次攻击只保留最大值。")
            ],
            ["weapon-exp"] =
            [
                new(1, "条件", "ctx+600≠0 且武器槽有装备", "否则本次武器经验为 0。"),
                new(2, "基础", "经验 = {weapon-exp-base}", "造成 HP 或 MP 伤害时走这一档。"),
                new(3, "等级差", "攻方等级 > 守方等级 → 经验 −1", "0x00403903 dec ecx。"),
                new(4, "暴击", "ctx+604 ≠ 0 → 经验 +1", "ctx+604 由物理暴击 0x00405F1A 置 1。"),
                new(5, "无伤害", "HP/MP 伤害都为 0 → 经验 = {weapon-exp-no-damage}", "直接覆盖，不再走基础值。"),
                new(6, "倍率", "经验 = 经验 × (第8项能力+{exp-multiplier-base})/100", "0x00421053；0x00403D5A 两处翻倍同样生效。"),
                new(7, "写入", "ctx+42C += 经验", "每次攻击累加。")
            ],
            ["armor-exp"] =
            [
                new(1, "条件", "目标阵营字节 [unit+5] ≠ 0 才结算", "0x0043FF54 判定目标不是我方。"),
                new(2, "基础", "经验 = {armor-exp-base}", "每件防具分别结算。"),
                new(3, "等级差", "攻方等级 < 守方等级 → 经验 −1", "0x00403AF3 dec dword [ebp-4]。"),
                new(4, "无伤害", "HP/MP 伤害都为 0 → 经验 −{armor-exp-no-damage}", "结果 = 基础 − 扣减。"),
                new(5, "倍率", "经验 = 经验 × (第8项能力+{exp-multiplier-base})/100", "0x00421053；0x00403D5A 两处翻倍同样生效。"),
                new(6, "写入", "ctx+430+防具槽×4 = 经验", "0x00406074。")
            ],
            ["strategy-exp"] =
            [
                new(1, "条件", "ctx+54C ≠ 0 才结算", "启用开关；否则经验为 0。"),
                new(2, "类型", "策略记录 +0x0B：2 → +20；1 → 普通档；其他 → 伤害判定", "0x00425AC7 读取类型字节。"),
                new(3, "击杀档", "攻方<守方：8×级差+32（≤200）；攻方≥守方：max(32−4×级差,0)，最低 10", "伤害类策略且击杀目标时生效。"),
                new(4, "普通档", "攻方<守方：4×级差+10（≤100）；攻方≥守方：max(10−级差÷2,0)，最低 5", "未击杀或类型 1 走这一档。"),
                new(5, "特殊目标", "目标 Data 号 = 0x496C96 → 经验 ×2", "0x00406604 比较。"),
                new(6, "倍率", "经验 = 经验 × (第8项能力+{exp-multiplier-base})/100", "倍率函数 0x00421053。")
            ],
            ["exp-multiplier"] =
            [
                new(1, "取能力", "P = 角色第 8 项基础能力", "0x00407C35 索引 8；6.6 0x00407C29。"),
                new(2, "倍率", "倍率 = (P + {exp-multiplier-base}) / 100", "百分比计算 0x00425AD9。"),
                new(3, "乘算", "经验 = 经验 × 倍率", "向下取整。"),
                new(4, "翻倍一", "攻方为我军且 0x501B00[部队序号] ≠ 0 → 经验 ×2", "0x0042545F 读取；命令 0x39/0x3A 经 0x00420BFD 置 3，命令 0x0A 经 0x00415ACA 清零。"),
                new(5, "翻倍二", "全局 0x500E9A == 1 → 经验 ×2", "0x00403D6C；6.5 0x41D69B 置 1、0x44EA34 置 0、0x4516FC 自增。"),
                new(6, "适用", "个人、武器、防具、策略经验共用", "各经验函数末尾都调用 0x00421053。")
            ],
            ["merit-record"] =
            [
                new(1, "定位", "记录 = 0x508400 + 角色ID×14", "角色 ID 来自单位首 WORD。"),
                new(2, "字段", "字段 0..4 五维；5 HP；6 MP", "每个字段 2 字节有符号。"),
                new(3, "读取", "基础能力 += 功勋[字段]（仅我军）", "0x0041055D/0x00407D74；char+2A≠0 跳过。"),
                new(4, "写入", "0x00408B52：模式 0 设 / 1 加 / 2 减", "角色 ID ≥ 102 直接丢弃。"),
                new(5, "剧本设置", "命令 0x11..0x1F → 字段 0..6，模式 0 设置", "0x004203D2 调用 0x00408B52。"),
                new(6, "剧本奖励", "5 个剧本变量 → 角色ID/值/模式/字段/操作类型", "0x00412007；变量表 0x00421492。"),
                new(7, "本场战功", "记录 = 0x508000 + 角色ID×10（5 字段）", "0x0042ACD2；道具效果 0x29 走这里。"),
                new(8, "累加", "add word [记录+字段×2]：特效0x45值 + 增点（可×2，或整条放弃）", "0x0042AB8E；0x500E9A==1 且 0x505FDC==0 时增点×2；0x505FDC≠0 且 0x505F5C≠0 时放弃；0x501B00[序号]≠0 再加一遍增点。"),
                new(9, "派发", "0x42A9C4 全字段（击杀/可变增点）；0x42A9F7 字段2+1", "击杀 0x0040380B/0x00420FA3；行动结算 0x0042309F（6.6 改到 0x0043BE08/0x0043BE74）。"),
                new(10, "结算", "清零 5 字段并累计到 0x505F40", "6.5/6.6 0x00423EAD；6.4 由 0x00408FA0 清理并累计。")
            ],
            ["merit-allocation"] =
            [
                new(1, "取点", "pool = 0x5083FC × 第二实参", "计数器战后 +1，上限 255。"),
                new(2, "定位", "i = 0..4；v = char[0x21+i]", "槽位值即当前成长档。"),
                new(3, "上限", "v ≥ 100（6.4）/110（6.5/6.6）跳过", "0x004620D1 / 0x0042AC98。"),
                new(4, "门槛", "v < 80 时 50；否则 (v−79)×10+55", "0x004620D5/0x0042ACA4。"),
                new(5, "扣点", "pool ≥ 门槛 → pool −= 门槛，v++", "0x004620DE/0x0042ACC2。"),
                new(6, "提升", "word[char+0x11+2i]++", "与成长值同步。"),
                new(7, "循环", "同槽位继续，直到不足门槛", "6.4 内联；6.5/6.6 0x0042AC8F。"),
                new(8, "余额", "转回本场战功 0x508000 表", "0x004620EA-0x004620F6。")
            ],
            ["battle-variable-load"] =
            [
                new(1, "入口", "S 剧本命令 0x45：调度 0x00410A38 索引 67", "0x004109E6 `sub eax,2`；6.4/6.5 处理 0x004122C1，6.6 0x004122C3。"),
                new(2, "读表", "按 0x004123BE 的 10 个索引读取剧本变量", "0x004183F7；16 位哨兵 0x8000（索引 2 用 0x80000000）时整条命令返回 5。"),
                new(3, "装载", "写 0x494FD0、0x496C9F、0x492F90+0x3D0E；第 4 值 6.4 写 0x496E23（阈值 80），6.5/6.6 写 0x501BF4（阈值 60）", "0x0041231C-0x0041234D；v>阈值时存 256-(v-阈值)。"),
                new(4, "目标", "第 6/8 个值（均为剧本变量 0x02）写 0x496C96 / 0x496C98+0x496C9A", "0x00412369 / 0x0041237D。"),
                new(5, "有效标志", "值 != 0xFFFF → 0x496C94/0x496C98 = 1；第 9/10 值写 0x496E21/0x496E22", "0x00412357/0x00412374/0x00412398/0x004123A9。"),
                new(6, "保留槽", "第 5/7 个值（剧本变量 0x32）读入后未被消费", "本轮逐字节复核；0x505F64 置 0xFFFF。")
            ],
            ["per-turn-exp"] =
            [
                new(1, "读取", "循环 3 次查询特效 3/4/5 的值", "0x004101D9；槽号 = i+3，表 0x0043CFCD 作为道具类型过滤值。"),
                new(2, "倍率", "× (第 8 项能力 + 100) / 100", "0x00407FAA + 0x00425AD9。"),
                new(3, "个人", "个人经验加进 char 经验 → 0x004088CD 升级", "0x0043CF9C-0x0043CFAA。"),
                new(4, "装备", "武器槽 0 / 防具槽 1 → 0x004082DD", "0x0043CFB7 / 0x0043CFC4。"),
                new(5, "边界", "三件特效值都为 0 时跳过结算", "0x0043CF26-0x0043CF42。")
            ],
            ["char-level-exp"] =
            [
                new(1, "读取", "L=等级 char+0x2C，E=经验 char+0x2D", "0x004065D0 / 0x004065C7。"),
                new(2, "阈值", "6.4：150；6.5：(min(L/20,3)+3)×50；6.6：250", "6.5 由 0x0040D21D 现算。"),
                new(3, "升级", "E ≥ 阈值 且 L < {char-exp-max-level} → E -= 阈值，L++", "升级成长 0x00408D52。"),
                new(4, "写回", "未满级写 E；满级写 255", "char+0x2D。"),
                new(5, "边界", "6.5 的分段阈值在同一次结算中只算一次", "一次结算内不随升级重算。")
            ],
            ["equip-level-exp"] =
            [
                new(1, "读取", "槽位 0/1，等级 char+0x2E+槽×3+1，经验 +2", "0x004032DF / 0x00409680。"),
                new(2, "阈值", "宝物 {equip-exp-threshold-special}；普通 {equip-exp-threshold-normal}", "0x0040B4E1 判道具 +0x11 bit0。"),
                new(3, "升级", "经验 ≥ 阈值 且 等级 < 上限 → 扣减、升级、成长", "装备成长 0x004083C6。"),
                new(4, "上限", "宝物 {equip-level-cap-special}；普通 {equip-level-cap-normal}", "到上限后不再升级。"),
                new(5, "写回", "满级写 255，否则写剩余经验", "0x0040329B。"),
                new(6, "归属", "武器经验进槽 0，防具经验进槽 1", "0x00406C95 / 0x00405B05。")
            ],
            ["ability-write"] =
            [
                new(1, "准备", "字段 0..4 五维、5 最大 HP、6 最大 MP、7/8 当前 HP/MP、10..14 成长值、15 单位槽字节", "0x00406ED2 cmp al,0Fh 后按字段分派。"),
                new(2, "五维/HP/MP 增量", "0x47FA89(旧,值,{ability-write-cap}) = min(旧+值,{ability-write-cap})", "模式 1 时旧值取 0，等价直写。"),
                new(3, "成长值", "byte[rec+字段+0x17] = min(旧+值,{ability-write-growth-cap})", "字段 10..14 对应成长值 0..4。"),
                new(4, "当前 HP/MP", "置 0x505F30={ability-write-mode} → 0x45AA37 按模式改当前值", "0 扣减(保底1)、1 增加、2 直设。"),
                new(5, "直接设置", "0x407027 用 min(值,0x270F) / min(值,0xFFFF) 覆盖", "S 剧本命令模式 0；模式 2 先取基准再相减。")
            ],
            ["troop-tier"] =
            [
                new(1, "准备", "兵种 = byte[rec+0x2B]，等级 = byte[rec+0x2C]，兵种 ≤ 59", "0x00408A73 cmp al,3Bh。"),
                new(2, "分档", "r = 兵种 % 3；块长 20", "0x0041FBF8 mov cl,3；0x00408A66 push 14h。"),
                new(3, "基础", "v(当前兵种)×max(等级−r×块长,0) + v(前兵种)×min(等级,r×块长)", "r==2 时先按 2×块长 比较（0x00408A8B shl ecx,1）。"),
                new(4, "前置积分", "HP/MP 额外 + 2×Σ v(兵种−1..兵种−r)", "0x00413FF9 shl dword [ebp-4],1；6.6 改为 2×r×v(当前兵种)。"),
                new(5, "升级条件", "等级 ≥ (r+1)×块长；r==2 或兵种 > 59 不可升", "0x0041D42E inc edx；0x0041D406 cmp edx,2。")
            ],
            ["troop-up"] =
            [
                new(1, "定位", "编号 0x7F → 0x41D124 解析目标；0xFF 直接退出", "0x0041D478/0x0041D482。"),
                new(2, "取记录", "0x4061F9(槽) 取战场单位，0x40658F 取武将记录", "0x0041D48E/0x0041D496。"),
                new(3, "兵种+1", "byte[rec+0x2B] = troop + 1", "0x0041D510 inc eax；0x0040E025 mov byte [ecx+2Bh],al。"),
                new(4, "补正", "最大 HP/MP 各 += 2×v(前兵种)（0x413FAC(字段,rec,1)）", "0x0041D52C/0x0041D53A，循环字段 5..6。"),
                new(5, "演出与提示", "10 帧循环 + 提示文本 0x48B698", "0x0041D5B2 cmp [ebp-4],0Ah；0x0041D653 push 48B698h。")
            ],
            ["equip-growth"] =
            [
                new(1, "取装备", "槽 0/1：0x4065F0 取道具 ID，0xFF 跳过；0x4837C2 取道具记录", "0x00407C55/0x00407C63。"),
                new(2, "基础成长", "0x40B3D7 = (装备等级−1)×byte[道具+0x17]（门控 0x40B444 ≤ 1）", "0x0040B3FB 循环；0x0040C464 cmp eax,1。"),
                new(3, "类别过滤", "0x429AD7 返回 0 才计入（类别 0x0A 对索引 0/2 例外）", "0x00429AE5 cmp al,0Ah；6.6 该过滤在 0x405670。"),
                new(4, "宝物附加", "宝物且 0x40678E(item)==索引 → 0x4200F8(道具+0x16, 等级) + 0x452825", "0x00407CA5/0x00407CAD/0x00407CB8；6.6 0x004200F5。"),
                new(5, "汇总", "返回值 + 100 = 经验倍率（0x407FAA）", "0x00407FB7 add eax,64h。")
            ],
            ["treasure-growth"] =
            [
                new(1, "取类型与值", "eax=道具+0x16（值），byte[eax-2]=道具+0x14（类型），dl=装备等级", "0x004200FE/0x00420101。"),
                new(2, "类型分支", "0x1F→+等级；0x55→×(等级+1)；0x2F→×等级+30；0x33→+3；0x32→×2；0x36/0x42/0x46→+1；其它→×3/2", "0x00420131/0x004200DD/0x004200ED/0x00420166。"),
                new(3, "高等级查表", "等级≥10 → byte[0x46236F + (类型−0x1A)]，0xFE 时不覆盖", "0x00420177/0x0042017A/0x00420180。"),
                new(4, "门控", "0x452825：索引<7 且 0x46230F[索引]==2 才应用", "0x00452839 cmp al,7；0x00452842 cmp byte [eax+46230Fh],2。"),
                new(5, "换算", "结果 = 0x425AD9(当前能力, 成长值) = 能力×成长/100", "0x0045287D call 0x00425AD9；0x00425AE5 mov ecx,64h。")
            ],
            ["growth-gap"] =
            [
                new(1, "索引门", "索引 ≥5 → 直接返回传入成长值（ecx=0）", "0x00436DE9 cmp dword [ebp+8],5。"),
                new(2, "特效查询", "0x42518F(0x3D, 0x5C, 选择子, 0) → 0x4101D9 / 0x41301E", "0x00436DF3-0x00436DFB；6.4 选择子 1。"),
                new(3, "基准", "特效值非 0 用它；否则 (兵种字节 + 成长档) >> 1", "0x00436E1E/0x00436E26/0x00436E32/0x00436E3A。"),
                new(4, "合成", "基准×等级 + 成长值 byte[rec+索引+0x21] + 永久功勋", "0x00436E46 imul eax,edx；0x00436E68 call 0x0041055D。"),
                new(5, "取差", "max(合成值 − 当前能力, 0) + 传入值；edx=合成值", "0x00436E82/0x00436E8D/0x00436E8F/0x00436E91。")
            ],
            ["effect-dispatch"] =
            [
                new(1, "入口", "0x42518F(索引, 选择子, 模式, 0) 原样透传 4 参；6.4 为 0x412A87", "0x0042518F；6.4 0x00412A87。"),
                new(2, "阵营判定", "0x40B922 = (0x40B913()==3)，0x40B913 = 0x41EDEF(0x4AC63C)", "0x0040B92C cmp al,3；0x0040B916 mov ecx,4AC63Ch。"),
                new(3, "我方", "返回 1 → 0x4101D9：先 0x426A07(0,0,0,0,0)，再与 0x505F78 比较", "0x004101E4/0x004101F3。"),
                new(4, "敌方", "返回 0 → 0x41301E：0x40BE7D → 0x4198BE(0x500C3B) → 0x43C794 → 0x413009 → 0x40BF2F", "0x00413022/0x00413037/0x00413049/0x00413053。"),
                new(5, "参数差异", "模式：6.4 为 1，6.5/6.6 为 2；索引 0x3D、选择子 0x5C 不变", "6.4 0x00436DF5 push 1；6.5 0x00436DF5 push 2。")
            ],
            ["merge-mode"] =
            [
                new(1, "模式字节", "0x40B913() = byte[0x4AC63C]（0x41EDEF 只是 byte[ecx]）", "0x0041EDF2 movzx eax,byte [ecx]；0x0040B916 mov ecx,4AC63Ch。"),
                new(2, "静态写点", "置 2：6.4 0x4426E7 / 6.5·6.6 0x416A78；自增：6.4 0x442700 / 6.5·6.6 0x416A91；置 3：6.4·6.5 0x43C015 / 6.6 0x43C010", "0x004426E7/0x00416A78；0x00442700/0x00416A91；0x0043C015；6.6 0x0043C010。"),
                new(3, "分派", "byte[0x4AC63C]==3 → 0x4101D9，否则 0x41301E", "0x0040B92C cmp al,3；0x0040B92E sete cl。"),
                new(4, "合并规则", "0x40BF2F：0=和、1=取大、3=或、其它 a==7 保留否则取大", "0x0040BF36/0x0040BF3F/0x0040BF4C/0x0040BF50。"),
                new(5, "包装", "0x413009：mode==2 且 edx==0 时 edx=eax，再 0x40BF2F", "0x0041300C/0x00413015/0x00413017。")
            ]
        };

    public IReadOnlyList<BattleFormulaValue> Read(ProjectWorkspace workspace)
    {
        ArgumentNullException.ThrowIfNull(workspace);
        var exePath = Path.Combine(workspace.RootPath, "Ekd5.exe");
        return Read(exePath, workspace.ActiveProfile.Profile.Version);
    }

    public IReadOnlyList<BattleFormulaValue> Read(string exePath, string? version)
    {
        var constants = new EngineConstantService().Read(exePath, version)
            .ToDictionary(item => item.Definition.Id, StringComparer.Ordinal);
        return Definitions.Select(definition => Build(definition, version, constants)).ToArray();
    }

    public BattleFormulaValue? ReadDefinition(string formulaId, string? version)
    {
        var definition = Definitions.FirstOrDefault(item => item.Id == formulaId);
        return definition == null ? null : BuildStatic(definition, version);
    }

    public BattleFormulaValue? ReadFormula(ProjectWorkspace workspace, string formulaId)
        => Read(workspace).FirstOrDefault(item => item.Definition.Id == formulaId);

    private static BattleFormulaValue Build(BattleFormulaDefinition definition, string? version,
        IReadOnlyDictionary<string, EngineConstantValue> constants)
    {
        var values = definition.Constants.Select(constant => BuildConstant(constant, version, constants)).ToArray();
        return new(definition, BuildSteps(definition, values), values);
    }

    private static BattleFormulaValue BuildStatic(BattleFormulaDefinition definition, string? version)
    {
        var values = definition.Constants.Select(constant => BuildStaticConstant(constant, version)).ToArray();
        return new(definition, BuildSteps(definition, values), values);
    }

    private static BattleFormulaConstantValue BuildConstant(BattleFormulaConstant constant, string? version,
        IReadOnlyDictionary<string, EngineConstantValue> constants)
    {
        if (constant.ConstantId is { } id)
        {
            if (!constants.TryGetValue(id, out var value))
                return new(constant, "—", false, "只读（未找到常量）", string.Empty, false, "常量页没有这个条目。");
            var definition = value.Definition;
            var range = $"{definition.Minimum}..{definition.Maximum}";
            var shared = ConstantUsage.GetValueOrDefault(id, 0) > 1;
            var current = value.SignatureMatches && definition.Kind != EngineConstantKind.Text
                ? value.NumericValue?.ToString(CultureInfo.InvariantCulture) ?? "—"
                : "—";
            if (!value.SignatureMatches)
            {
                var notApplicable = value.Diagnostic.Contains("不适用", StringComparison.Ordinal) ||
                                    value.Diagnostic.Contains("只适用于", StringComparison.Ordinal);
                return new(constant, current, false,
                    notApplicable ? "不适用此基底" : "只读（签名未命中）",
                    range, shared, value.Diagnostic);
            }
            if (definition.Kind == EngineConstantKind.Text)
                return new(constant, "—", false, "只读（文本槽）", range, shared, value.Diagnostic);
            return new(constant, current, true, shared ? "可改（共用）" : "可改", range, shared, value.Diagnostic);
        }

        var staticValue = version switch
        {
            "6.4" => constant.Value64,
            "6.5" => constant.Value65,
            "6.6" => constant.Value66,
            _ => constant.Value65
        };
        var applicable = staticValue != "—";
        var status = constant.Note.Contains("指令编码", StringComparison.Ordinal)
            ? "只读（指令编码）"
            : constant.Note.Contains("公式输入", StringComparison.Ordinal)
                ? "只读（公式输入）"
                : "只读（公式结构）";
        return new(constant, applicable ? staticValue : "—", false,
            applicable ? status : "不适用此基底", string.Empty, false, constant.Note);
    }

    private static BattleFormulaConstantValue BuildStaticConstant(BattleFormulaConstant constant, string? version)
    {
        var staticValue = version switch
        {
            "6.4" => constant.Value64,
            "6.5" => constant.Value65,
            "6.6" => constant.Value66,
            _ => constant.Value65
        };
        if (constant.ConstantId is { } id)
        {
            var value = version == null ? "—" : staticValue;
            var shared = ConstantUsage.GetValueOrDefault(id, 0) > 1;
            return new(constant, value, false, "只读（尚未打开项目）", string.Empty, shared,
                "尚未打开项目，只显示默认值。");
        }
        var applicable = staticValue != "—";
        var status = constant.Note.Contains("指令编码", StringComparison.Ordinal)
            ? "只读（指令编码）"
            : constant.Note.Contains("公式输入", StringComparison.Ordinal)
                ? "只读（公式输入）"
                : "只读（公式结构）";
        return new(constant, applicable ? staticValue : "—", false,
            applicable ? status : "不适用此基底", string.Empty, false, constant.Note);
    }

    private static IReadOnlyList<BattleFormulaStep> BuildSteps(BattleFormulaDefinition definition,
        IReadOnlyList<BattleFormulaConstantValue> values)
    {
        var current = new Dictionary<string, string>(StringComparer.Ordinal);
        foreach (var value in values.Where(item => item.Constant.ConstantId != null))
            current[value.Constant.ConstantId!] = value.CurrentValue;

        var template = StepTemplates.GetValueOrDefault(definition.Id) ?? [];
        return template.Select(step => step with
        {
            Expression = Regex.Replace(step.Expression, @"\{([a-z0-9-]+)\}",
                match => current.GetValueOrDefault(match.Groups[1].Value, "—"))
        }).ToArray();
    }

    public IReadOnlyList<BattleFormulaValidationIssue> ValidateEdits(ProjectWorkspace workspace,
        IReadOnlyList<BattleFormulaEdit> edits)
    {
        ArgumentNullException.ThrowIfNull(workspace);
        if (edits.Count == 0) return [];
        var values = Read(workspace);
        var issues = new List<BattleFormulaValidationIssue>();
        var seen = new HashSet<string>(StringComparer.Ordinal);
        var definitions = EngineConstantService.Definitions.ToDictionary(item => item.Id, StringComparer.Ordinal);

        var rowsById = values
            .SelectMany(value => value.Constants.Select(constant => new
            {
                FormulaId = value.Definition.Id,
                Value = constant,
                ConstantId = constant.Constant.ConstantId
            }))
            .Where(row => row.ConstantId != null)
            .GroupBy(row => row.ConstantId!, StringComparer.Ordinal)
            .ToDictionary(group => group.Key, group => group.ToArray(), StringComparer.Ordinal);

        void Add(string constantId, string constantName, string formulaId,
            BattleFormulaIssueSeverity severity, string message)
        {
            var key = $"{constantId}|{severity}|{message}";
            if (!seen.Add(key)) return;
            issues.Add(new(constantId, constantName, formulaId, severity, message));
        }

        foreach (var duplicate in edits.GroupBy(item => item.ConstantId, StringComparer.Ordinal))
        {
            var distinct = duplicate.Select(item => item.Value).Distinct().ToArray();
            if (distinct.Length > 1)
                Add(duplicate.Key, duplicate.Key, string.Empty, BattleFormulaIssueSeverity.Error,
                    $"同一常量在本批次出现多个不同值：{string.Join("/", distinct)}。");
        }

        var effective = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (var row in rowsById.Values.SelectMany(items => items))
        {
            if (row.Value.CurrentValue == "—") continue;
            if (int.TryParse(row.Value.CurrentValue, NumberStyles.Integer,
                    CultureInfo.InvariantCulture, out var number))
                effective[row.ConstantId!] = number;
        }

        foreach (var edit in edits.GroupBy(item => item.ConstantId, StringComparer.Ordinal)
                     .Select(group => group.Last()))
        {
            if (!rowsById.TryGetValue(edit.ConstantId, out var rows))
            {
                Add(edit.ConstantId, edit.ConstantId, string.Empty, BattleFormulaIssueSeverity.Error,
                    $"不是公式常量：{edit.ConstantId}。");
                continue;
            }
            var editable = rows.FirstOrDefault(row => row.Value.Editable);
            if (editable == null)
            {
                Add(edit.ConstantId, rows[0].Value.Constant.Name, rows[0].FormulaId,
                    BattleFormulaIssueSeverity.Error,
                    $"{rows[0].Value.Constant.Name}：{rows[0].Value.Status}，当前基底不可写。");
                continue;
            }
            if (!definitions.TryGetValue(edit.ConstantId, out var definition))
            {
                Add(edit.ConstantId, editable.Value.Constant.Name, editable.FormulaId,
                    BattleFormulaIssueSeverity.Error, $"找不到常量定义：{edit.ConstantId}。");
                continue;
            }
            if (edit.Value < definition.Minimum || edit.Value > definition.Maximum)
            {
                Add(edit.ConstantId, definition.DisplayName, editable.FormulaId,
                    BattleFormulaIssueSeverity.Error,
                    $"{definition.DisplayName}：请输入 {definition.Minimum}..{definition.Maximum}。");
                continue;
            }
            effective[edit.ConstantId] = edit.Value;
        }

        var touched = edits.Select(item => item.ConstantId).ToHashSet(StringComparer.Ordinal);
        if (touched.Any(id => id.StartsWith("hit-curve-", StringComparison.Ordinal)))
            ValidateHitCurve(effective, Add);
        if (touched.Any(id => id.StartsWith("rate-curve-", StringComparison.Ordinal)))
            ValidateRateCurve(effective, Add);
        if (touched.Any(id => id.StartsWith("hit-retry-", StringComparison.Ordinal)))
            ValidateRetry(effective, Add);
        if (touched.Any(ExperienceConstantIds.Contains))
            ValidateExperience(effective, touched, Add);
        ValidatePools(workspace.ActiveProfile.Profile.Version, touched, edits, Add);

        return issues;
    }

    private static void ValidateHitCurve(IReadOnlyDictionary<string, int> values,
        Action<string, string, string, BattleFormulaIssueSeverity, string> add)
    {
        var lowBase = Value(values, "hit-curve-low-base");
        var midBase = Value(values, "hit-curve-mid-base");
        var highBase = Value(values, "hit-curve-high-base");
        var cap = Value(values, "hit-curve-cap");
        var lowCoef = Value(values, "hit-curve-low-coef");
        var midCoef = Value(values, "hit-curve-mid-coef");
        var highCoef = Value(values, "hit-curve-high-coef");
        var divisor = Value(values, "hit-curve-low-divisor");
        var floor = Value(values, "hit-curve-floor-66");
        if (lowBase == null || midBase == null || highBase == null || cap == null ||
            lowCoef == null || midCoef == null || highCoef == null || divisor == null) return;

        if (lowBase > midBase)
            add("hit-curve-low-base", "低段基础", "hit-curve", BattleFormulaIssueSeverity.Error,
                $"命中率曲线：低段基础 {lowBase} 大于中段基础 {midBase}。");
        if (midBase > highBase)
            add("hit-curve-mid-base", "中段基础", "hit-curve", BattleFormulaIssueSeverity.Error,
                $"命中率曲线：中段基础 {midBase} 大于高段基础 {highBase}。");
        if (highBase > cap)
            add("hit-curve-high-base", "高段基础", "hit-curve", BattleFormulaIssueSeverity.Error,
                $"命中率曲线：高段基础 {highBase} 超过上限 {cap}。");
        if (divisor < 1 || divisor > 10)
            add("hit-curve-low-divisor", "低段除数", "hit-curve", BattleFormulaIssueSeverity.Error,
                $"命中率曲线：低段除数必须在 1..10，当前 {divisor}。");
        if (floor is { } floorValue && floorValue > lowBase)
            add("hit-curve-floor-66", "6.6 命中下限", "hit-curve", BattleFormulaIssueSeverity.Error,
                $"命中率曲线：6.6 下限 {floorValue} 大于低段基础 {lowBase}，下限会覆盖低段起点。");
        if (highBase + highCoef > cap)
            add("hit-curve-high-base", "高段基础", "hit-curve", BattleFormulaIssueSeverity.Warning,
                $"命中率曲线：高段最高 {highBase + highCoef} 超过上限 {cap}，实际会被截断为 {cap}。");
        if (midBase + midCoef > cap)
            add("hit-curve-mid-base", "中段基础", "hit-curve", BattleFormulaIssueSeverity.Warning,
                $"命中率曲线：中段最高 {midBase + midCoef} 超过上限 {cap}，实际会被截断为 {cap}。");
        if (lowBase + lowCoef / 2 > cap)
            add("hit-curve-low-base", "低段基础", "hit-curve", BattleFormulaIssueSeverity.Warning,
                $"命中率曲线：低段最高 {lowBase + lowCoef / 2} 超过上限 {cap}，实际会被截断为 {cap}。");
    }

    private static void ValidateRateCurve(IReadOnlyDictionary<string, int> values,
        Action<string, string, string, BattleFormulaIssueSeverity, string> add)
    {
        var lowBase = Value(values, "rate-curve-low-base");
        var highBase = Value(values, "rate-curve-high-base");
        var lowCoef = Value(values, "rate-curve-low-coef");
        var highCoef = Value(values, "rate-curve-high-coef");
        var cap = Value(values, "rate-curve-cap");
        var full = Value(values, "rate-curve-full-multiplier");
        if (lowBase == null || highBase == null || lowCoef == null || highCoef == null ||
            cap == null || full == null) return;

        if (lowBase > highBase)
            add("rate-curve-low-base", "低段基础", "rate-curve", BattleFormulaIssueSeverity.Error,
                $"发动率曲线：低段基础 {lowBase} 大于高段基础 {highBase}。");
        if (highBase > cap)
            add("rate-curve-high-base", "高段基础", "rate-curve", BattleFormulaIssueSeverity.Error,
                $"发动率曲线：高段基础 {highBase} 超过上限 {cap}。");
        if (full < 2 || full > 10)
            add("rate-curve-full-multiplier", "满率倍率", "rate-curve", BattleFormulaIssueSeverity.Error,
                $"发动率曲线：满率倍率必须在 2..10，当前 {full}。");
        if (highBase + highCoef > cap)
            add("rate-curve-high-base", "高段基础", "rate-curve", BattleFormulaIssueSeverity.Warning,
                $"发动率曲线：高段最高 {highBase + highCoef} 超过上限 {cap}，实际会被截断为 {cap}。");
        if (lowBase + lowCoef > cap)
            add("rate-curve-low-base", "低段基础", "rate-curve", BattleFormulaIssueSeverity.Warning,
                $"发动率曲线：低段最高 {lowBase + lowCoef} 超过上限 {cap}，实际会被截断为 {cap}。");
    }

    private static void ValidateRetry(IReadOnlyDictionary<string, int> values,
        Action<string, string, string, BattleFormulaIssueSeverity, string> add)
    {
        var threshold = Value(values, "hit-retry-threshold");
        var deduction = Value(values, "hit-retry-deduction");
        if (threshold != null && deduction != null && deduction > threshold)
            add("hit-retry-deduction", "二次判定扣减", "physical-hit", BattleFormulaIssueSeverity.Warning,
                $"二次判定：扣减 {deduction} 大于阈值 {threshold}，补判命中率会变成 0 或负数。");
    }

    private static void ValidateExperience(IReadOnlyDictionary<string, int> values, IReadOnlySet<string> touched,
        Action<string, string, string, BattleFormulaIssueSeverity, string> add)
    {
        if (touched.Contains("exp-multiplier-base") &&
            Value(values, "exp-multiplier-base") is { } multiplier && multiplier < 100)
            add("exp-multiplier-base", "经验倍率基础值", "exp-multiplier", BattleFormulaIssueSeverity.Warning,
                $"经验倍率基础值 {multiplier} 低于 100：所有经验都会按低于 100% 结算。");

        if (touched.Contains("personal-exp-kill-ratio-num") ||
            touched.Contains("personal-exp-kill-ratio-offset"))
        {
            var numerator = Value(values, "personal-exp-kill-ratio-num");
            var offset = Value(values, "personal-exp-kill-ratio-offset");
            if (numerator != null && offset != null && numerator < offset + 2)
                add("personal-exp-kill-ratio-num", "击杀经验分子", "personal-exp",
                    BattleFormulaIssueSeverity.Warning,
                    $"击杀经验分子 {numerator} 小于除数下限 {offset + 1}：普通击杀额外经验最多 1 点。");
        }

        foreach (var (id, name, formulaId) in new[]
                 {
                     ("personal-exp-base", "基础经验值", "personal-exp"),
                     ("weapon-exp-base", "武器经验基础值", "weapon-exp"),
                     ("armor-exp-base", "防具经验基础值", "armor-exp")
                 })
        {
            if (!touched.Contains(id)) continue;
            if (Value(values, id) == 0)
                add(id, name, formulaId, BattleFormulaIssueSeverity.Warning,
                    $"{name} 为 0：正常结算时对应经验会变成 0。");
        }

        if ((touched.Contains("equip-level-cap-special") || touched.Contains("equip-level-cap-normal")) &&
            Value(values, "equip-level-cap-special") is { } specialCap &&
            Value(values, "equip-level-cap-normal") is { } normalCap && specialCap < normalCap)
            add("equip-level-cap-special", "宝物等级上限", "equip-level-exp",
                BattleFormulaIssueSeverity.Warning,
                $"宝物等级上限 {specialCap} 低于普通上限 {normalCap}：宝物装备会更早封顶。");

        if ((touched.Contains("equip-exp-threshold-special") || touched.Contains("equip-exp-threshold-normal")) &&
            Value(values, "equip-exp-threshold-special") is { } specialExp &&
            Value(values, "equip-exp-threshold-normal") is { } normalExp && specialExp < normalExp)
            add("equip-exp-threshold-special", "宝物经验阈值", "equip-level-exp",
                BattleFormulaIssueSeverity.Warning,
                $"宝物经验阈值 {specialExp} 低于普通阈值 {normalExp}：宝物升级反而更快。");
    }

    private static void ValidatePools(string version, IReadOnlySet<string> touched,
        IReadOnlyList<BattleFormulaEdit> edits,
        Action<string, string, string, BattleFormulaIssueSeverity, string> add)
    {
        var defaults = new Dictionary<string, int>(StringComparer.Ordinal)
        {
            ["physical-crit-pool"] = version == "6.4" ? 0 : 2,
            ["strategy-crit-pool"] = version == "6.4" ? 0 : 18,
            ["combo-pool"] = 0
        };
        foreach (var edit in edits)
        {
            if (!defaults.TryGetValue(edit.ConstantId, out var expected) || !touched.Contains(edit.ConstantId))
                continue;
            if (edit.Value == expected) continue;
            var name = edit.ConstantId switch
            {
                "physical-crit-pool" => "物理暴击集气池",
                "strategy-crit-pool" => "策略暴击集气池",
                _ => "连击集气池"
            };
            add(edit.ConstantId, name, string.Empty, BattleFormulaIssueSeverity.Warning,
                $"{name}：当前基底默认 {expected}，新值 {edit.Value} 不是已知默认值，建议实机复核。");
        }
    }

    private static int? Value(IReadOnlyDictionary<string, int> values, string id)
        => values.GetValueOrDefault(id);

    public BattleFormulaCommitResult Commit(ProjectWorkspace workspace, IReadOnlyList<BattleFormulaEdit> edits)
    {
        ArgumentNullException.ThrowIfNull(workspace);
        var issues = ValidateEdits(workspace, edits);
        var errors = issues.Where(item => item.Severity == BattleFormulaIssueSeverity.Error).ToArray();
        if (errors.Length > 0)
            return new(false, string.Join(Environment.NewLine, errors.Select(item => item.Message)), Issues: issues);

        var constantEdits = edits.GroupBy(item => item.ConstantId, StringComparer.Ordinal)
            .Select(group => new EngineConstantEdit(group.Key, group.Last().Value, null))
            .ToArray();
        var result = new EngineConstantService().Commit(workspace, constantEdits);
        if (!result.Success)
            return new(false, result.Message, result.BackupPath, 0, issues);

        var after = Read(workspace);
        foreach (var edit in edits.GroupBy(item => item.ConstantId, StringComparer.Ordinal)
                     .Select(group => group.Last()))
        {
            var value = after.SelectMany(item => item.Constants)
                .FirstOrDefault(item => item.Constant.ConstantId == edit.ConstantId);
            if (value == null || value.CurrentValue != edit.Value.ToString(CultureInfo.InvariantCulture))
                return new(false, $"写入后复读不一致：{edit.ConstantId}。", result.BackupPath, 0, issues);
        }
        return new(true, result.Message, result.BackupPath, result.ChangedBytes, issues);
    }
}
