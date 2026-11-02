using DataManager.Core.Binary;
using DataManager.Core.Editing;
using DataManager.Core.Scanner;

namespace DataManager.Tests;

internal static class EngineBattleFormulaTests
{
    public static void Run(string sourceRoot)
    {
        var sourceHash = HashService.Sha256(Path.Combine(sourceRoot, "Ekd5.exe"));
        var copy = TestSupport.CreateCoreCopy(sourceRoot, restoreKnown65Snapshot: false);
        try
        {
            var version = Path.GetFileName(sourceRoot) == "洗隋" ? "6.4"
                : Path.GetFileName(sourceRoot) == "复刻版6.6山贼" ? "6.6" : "6.5";
            var workspace = new ProjectWorkspace();
            workspace.Open(copy);
            var service = new EngineBattleFormulaService();
            var values = service.Read(workspace);
            TestSupport.Assert(values.Count == EngineBattleFormulaService.Definitions.Count,
                "战斗公式条目数量不符。");
            TestSupport.Assert(values.Count >= 14, "战斗公式条目过少。");
            var constantDefinitions = EngineConstantService.Definitions
                .Select(item => item.Id).ToHashSet(StringComparer.Ordinal);
            var newIds = new[]
            {
                "hit-curve-cap", "hit-curve-high-base", "hit-curve-high-coef", "hit-curve-mid-base",
                "hit-curve-mid-coef", "hit-curve-low-divisor", "hit-curve-low-base", "hit-curve-low-coef",
                "hit-curve-floor-66", "hit-retry-count", "hit-retry-threshold", "hit-retry-deduction",
                "rate-curve-full-multiplier", "rate-curve-cap", "rate-curve-high-coef", "rate-curve-high-base",
                "rate-curve-low-coef", "rate-curve-low-base", "physical-crit-cap", "physical-crit-pool",
                "strategy-crit-cap", "strategy-crit-pool", "combo-pool",
                "personal-exp-base", "personal-exp-kill-flat", "personal-exp-kill-ratio-num",
                "personal-exp-kill-ratio-offset", "exp-multiplier-base", "weapon-exp-base",
                "weapon-exp-no-damage", "armor-exp-base", "armor-exp-no-damage",
                "char-exp-max-level", "char-exp-threshold", "char-exp-band-65", "char-exp-step-65",
                "equip-exp-threshold-special", "equip-exp-threshold-normal",
                "equip-level-cap-special", "equip-level-cap-normal"
            };
            var availableIds = values.SelectMany(value => value.Constants)
                .Where(item => item.Constant.ConstantId != null)
                .Select(item => item.Constant.ConstantId!).ToHashSet(StringComparer.Ordinal);
            foreach (var id in newIds)
                TestSupport.Assert(availableIds.Contains(id), "公式页缺少新增常量：" + id);

            foreach (var value in values)
            {
                var definition = value.Definition;
                TestSupport.Assert(!string.IsNullOrWhiteSpace(definition.Category), "公式缺少分类：" + definition.Id);
                TestSupport.Assert(!string.IsNullOrWhiteSpace(definition.Description), "公式缺少说明：" + definition.Id);
                TestSupport.Assert(!string.IsNullOrWhiteSpace(definition.Detail), "公式缺少详解：" + definition.Id);
                TestSupport.Assert(definition.Evidence.Contains("0x", StringComparison.Ordinal),
                    "公式缺少地址证据：" + definition.Id);
                TestSupport.Assert(value.Constants.Count > 0, "公式没有常量：" + definition.Id);
                TestSupport.Assert(value.Steps.Count >= 3, "公式步骤过少：" + definition.Id);
                foreach (var step in value.Steps)
                    TestSupport.Assert(!string.IsNullOrWhiteSpace(step.Expression) &&
                        !string.IsNullOrWhiteSpace(step.Note), "公式步骤缺少计算式或说明：" + definition.Id);
                foreach (var constant in value.Constants)
                {
                    var item = constant.Constant;
                    TestSupport.Assert(!string.IsNullOrWhiteSpace(item.Name), "常量缺少名称：" + definition.Id);
                    TestSupport.Assert(!string.IsNullOrWhiteSpace(item.Role), "常量缺少作用：" + definition.Id);
                    TestSupport.Assert(item.Location.Contains("0x", StringComparison.Ordinal),
                        $"常量缺少地址证据：{definition.Id}/{item.Name}");
                    if (item.Linked)
                        TestSupport.Assert(constantDefinitions.Contains(item.ConstantId!),
                            $"公式引用了不存在的常量：{definition.Id}/{item.ConstantId}");
                    TestSupport.Assert(constant.CurrentValue.Length > 0, "常量当前值为空：" + item.Name);
                }
            }

            var physical = values.Single(value => value.Definition.Id == "physical-damage");
            var physicalBase = physical.Constants.Single(item => item.Constant.ConstantId == "physical-damage-base");
            TestSupport.Assert(physicalBase.CurrentValue == "25" && physicalBase.Editable,
                $"物理基础伤害不符：{physicalBase.CurrentValue}");
            var strategy = values.Single(value => value.Definition.Id == "strategy-damage");
            var strategyBase = strategy.Constants.Single(item => item.Constant.ConstantId == "strategy-damage-base");
            var strategyDivisor = strategy.Constants.Single(item => item.Constant.ConstantId == "strategy-damage-divisor");
            TestSupport.Assert(strategyBase.CurrentValue == "25" && strategyBase.Editable,
                $"策略基础伤害不符：{strategyBase.CurrentValue}");
            TestSupport.Assert(strategyDivisor.CurrentValue == "3" && strategyDivisor.Editable,
                $"策略能力差除数不符：{strategyDivisor.CurrentValue}");
            var guided = values.Single(value => value.Definition.Id == "guided-attack")
                .Constants.Single(item => item.Constant.ConstantId == "guided-attack-count");
            TestSupport.Assert(guided.CurrentValue == (version == "6.4" ? "4" : "2"),
                $"引导攻击次数不符：{guided.CurrentValue}");
            var counter = values.Single(value => value.Definition.Id == "counter-damage")
                .Constants.Single(item => item.Constant.ConstantId == "counter-damage-share");
            TestSupport.Assert(version == "6.4"
                    ? counter.CurrentValue == "—" && !counter.Editable
                    : counter.CurrentValue == "3" && counter.Editable,
                $"普通反击份数不符：{counter.CurrentValue}");
            var comboDamage = values.Single(value => value.Definition.Id == "combo-damage")
                .Constants.Single(item => item.Constant.ConstantId == "combo-damage-bonus");
            TestSupport.Assert(version == "6.4"
                    ? comboDamage.CurrentValue == "—" && !comboDamage.Editable
                    : comboDamage.CurrentValue == "0" && comboDamage.Editable,
                $"连击固定增伤不符：{comboDamage.CurrentValue}");
            var hitCurve = values.Single(value => value.Definition.Id == "hit-curve");
            var hitCap = Find(hitCurve, "hit-curve-cap");
            TestSupport.Assert(hitCap.CurrentValue == "100" && hitCap.Editable,
                $"命中率上限不符：{hitCap.CurrentValue}");
            var fixedHit = hitCurve.Constants.First(item => item.Constant.Name == "满命中倍率");
            TestSupport.Assert(fixedHit.Range.Length == 0 && fixedHit.Status == "只读（指令编码）",
                $"固定公式值范围/状态不符：{fixedHit.Range}/{fixedHit.Status}");

            foreach (var (id, expected) in new[]
                     {
                         ("hit-curve-high-base", "90"), ("hit-curve-high-coef", "10"),
                         ("hit-curve-mid-base", "60"), ("hit-curve-mid-coef", "30"),
                         ("hit-curve-low-divisor", "3"), ("hit-curve-low-base", "30"),
                         ("hit-curve-low-coef", "30")
                     })
            {
                var item = Find(hitCurve, id);
                TestSupport.Assert(item.CurrentValue == expected && item.Editable,
                    $"{id} 不符：{item.CurrentValue}");
            }

            var rate = values.Single(value => value.Definition.Id == "rate-curve");
            foreach (var (id, expected) in new[]
                     {
                         ("rate-curve-full-multiplier", "3"), ("rate-curve-cap", "100"),
                         ("rate-curve-high-coef", "80"), ("rate-curve-high-base", "20"),
                         ("rate-curve-low-coef", "18"), ("rate-curve-low-base", "2")
                     })
            {
                var item = Find(rate, id);
                TestSupport.Assert(item.CurrentValue == expected && item.Editable,
                    $"{id} 不符：{item.CurrentValue}");
            }

            var physicalCrit = values.Single(value => value.Definition.Id == "physical-crit");
            var strategyCrit = values.Single(value => value.Definition.Id == "strategy-crit");
            var physicalPool = Find(physicalCrit, "physical-crit-pool");
            var strategyPool = Find(strategyCrit, "strategy-crit-pool");
            TestSupport.Assert(Find(physicalCrit, "physical-crit-cap").CurrentValue == "100",
                "物理暴击上限不符。");
            TestSupport.Assert(Find(strategyCrit, "strategy-crit-cap").CurrentValue == "100",
                "策略暴击上限不符。");
            TestSupport.Assert(physicalPool.CurrentValue == (version == "6.4" ? "0" : "2"),
                $"物理暴击池不符：{physicalPool.CurrentValue}");
            TestSupport.Assert(strategyPool.CurrentValue == (version == "6.4" ? "0" : "18"),
                $"策略暴击池不符：{strategyPool.CurrentValue}");
            var comboPool = Find(values.Single(value => value.Definition.Id == "combo-rate"), "combo-pool");
            TestSupport.Assert(comboPool.CurrentValue == "0", $"连击池不符：{comboPool.CurrentValue}");

            foreach (var formulaId in new[] { "physical-hit", "strategy-hit" })
            {
                var hit = values.Single(value => value.Definition.Id == formulaId);
                var count = Find(hit, "hit-retry-count");
                var floor = Find(hit, "hit-curve-floor-66");
                if (version == "6.6")
                {
                    TestSupport.Assert(count.Status == "不适用此基底" && !count.Editable,
                        $"{formulaId} 的二次判定次数不应适用 6.6。");
                }
                else
                {
                    TestSupport.Assert(count.CurrentValue == "2" && count.Editable,
                        $"{formulaId} 的二次判定次数不符：{count.CurrentValue}");
                    TestSupport.Assert(Find(hit, "hit-retry-threshold").CurrentValue == "85",
                        $"{formulaId} 的二次判定阈值不符。");
                    TestSupport.Assert(Find(hit, "hit-retry-deduction").CurrentValue == "10",
                        $"{formulaId} 的二次判定扣减不符。");
                }
                TestSupport.Assert(version == "6.6"
                        ? floor.CurrentValue == "25" && floor.Editable
                        : floor.Status == "不适用此基底" && !floor.Editable,
                    $"{formulaId} 的 6.6 命中下限不符：{floor.CurrentValue}（{version}）");
            }

            var personalExp = values.Single(value => value.Definition.Id == "personal-exp");
            TestSupport.Assert(Find(personalExp, "personal-exp-base").CurrentValue == "6" &&
                Find(personalExp, "personal-exp-base").Editable, "个人经验基础值不符。");
            TestSupport.Assert(Find(personalExp, "personal-exp-kill-flat").CurrentValue == "48" &&
                Find(personalExp, "personal-exp-kill-flat").Editable, "击杀固定加成不符。");
            TestSupport.Assert(Find(personalExp, "personal-exp-kill-ratio-num").CurrentValue == "64",
                $"击杀经验分子不符：{Find(personalExp, "personal-exp-kill-ratio-num").CurrentValue}");
            TestSupport.Assert(Find(personalExp, "personal-exp-kill-ratio-offset").CurrentValue == "2",
                $"击杀除数偏移不符：{Find(personalExp, "personal-exp-kill-ratio-offset").CurrentValue}");

            var weaponExp = values.Single(value => value.Definition.Id == "weapon-exp");
            var weaponBase = Find(weaponExp, "weapon-exp-base");
            TestSupport.Assert(weaponBase.CurrentValue == (version == "6.5" ? "2" : "3") && weaponBase.Editable,
                $"武器经验基础值不符：{weaponBase.CurrentValue}（{version}）");
            var weaponNoDamage = Find(weaponExp, "weapon-exp-no-damage");
            TestSupport.Assert(weaponNoDamage.CurrentValue == (version == "6.6" ? "1" : "2") &&
                weaponNoDamage.Editable, $"武器经验无伤害值不符：{weaponNoDamage.CurrentValue}（{version}）");

            var armorExp = values.Single(value => value.Definition.Id == "armor-exp");
            var armorBase = Find(armorExp, "armor-exp-base");
            TestSupport.Assert(armorBase.CurrentValue == (version == "6.6" ? "4" : "3") && armorBase.Editable,
                $"防具经验基础值不符：{armorBase.CurrentValue}（{version}）");
            var armorNoDamage = Find(armorExp, "armor-exp-no-damage");
            var expectedArmorCut = version == "6.4" ? "1" : version == "6.5" ? "2" : "3";
            TestSupport.Assert(armorNoDamage.CurrentValue == expectedArmorCut && armorNoDamage.Editable,
                $"防具经验无伤害扣减不符：{armorNoDamage.CurrentValue}（{version}）");

            var multiplier = values.Single(value => value.Definition.Id == "exp-multiplier");
            TestSupport.Assert(Find(multiplier, "exp-multiplier-base").CurrentValue == "100" &&
                Find(multiplier, "exp-multiplier-base").Editable, "经验倍率基础值不符。");

            var strategyExp = values.Single(value => value.Definition.Id == "strategy-exp");
            TestSupport.Assert(strategyExp.Steps.Count >= 5, "策略经验步骤过少。");
            TestSupport.Assert(strategyExp.Constants
                    .Where(item => item.Constant.ConstantId == null)
                    .All(item => !item.Editable),
                "策略经验的结构常量应保持只读。");
            TestSupport.Assert(Find(strategyExp, "exp-multiplier-base").CurrentValue == "100",
                "策略经验的倍率基础不符。");
            TestSupport.Assert(strategyExp.Constants.Any(item =>
                    item.Constant.Name == "个人经验缓存" && item.CurrentValue == "ctx+0x502"),
                "策略经验的个人经验缓存不符。");
            TestSupport.Assert(strategyExp.Constants.Any(item =>
                    item.Constant.Name == "防具经验缓存" && item.CurrentValue == "ctx+0x50A"),
                "策略经验的防具经验缓存不符。");
            var strategyWeaponBase = strategyExp.Constants.Single(item => item.Constant.Name == "武器经验基础");
            TestSupport.Assert(strategyWeaponBase.CurrentValue == (version == "6.6" ? "3" : "4"),
                $"策略武器经验基础不符：{strategyWeaponBase.CurrentValue}（{version}）");

            var charLevelExp = values.Single(value => value.Definition.Id == "char-level-exp");
            TestSupport.Assert(Find(charLevelExp, "char-exp-max-level").CurrentValue ==
                    (version == "6.4" ? "80" : version == "6.5" ? "60" : "99") &&
                Find(charLevelExp, "char-exp-max-level").Editable,
                $"角色最大等级不符：{Find(charLevelExp, "char-exp-max-level").CurrentValue}（{version}）");
            TestSupport.Assert(Find(charLevelExp, "char-exp-max-level").Range == "1..255",
                $"角色最大等级的可改范围不是 1..255：{Find(charLevelExp, "char-exp-max-level").Range}（{version}）");
            var charThreshold = Find(charLevelExp, "char-exp-threshold");
            TestSupport.Assert(version == "6.5"
                    ? charThreshold.Status == "不适用此基底" && !charThreshold.Editable
                    : charThreshold.CurrentValue == (version == "6.4" ? "150" : "250") &&
                      charThreshold.Editable,
                $"角色每级经验不符：{charThreshold.CurrentValue}（{version}）");
            var band = Find(charLevelExp, "char-exp-band-65");
            var bandStep = Find(charLevelExp, "char-exp-step-65");
            TestSupport.Assert(version == "6.5"
                    ? band.CurrentValue == "20" && band.Editable &&
                      bandStep.CurrentValue == "50" && bandStep.Editable
                    : band.Status == "不适用此基底" && bandStep.Status == "不适用此基底",
                $"6.5 角色分段经验常量不符：{band.CurrentValue}/{bandStep.CurrentValue}（{version}）");

            var equipLevelExp = values.Single(value => value.Definition.Id == "equip-level-exp");
            TestSupport.Assert(Find(equipLevelExp, "equip-exp-threshold-special").CurrentValue == "200" &&
                Find(equipLevelExp, "equip-exp-threshold-special").Editable, "宝物经验阈值不符。");
            var equipNormalThreshold = Find(equipLevelExp, "equip-exp-threshold-normal");
            TestSupport.Assert(equipNormalThreshold.CurrentValue == (version == "6.5" ? "150" : "100") &&
                equipNormalThreshold.Editable,
                $"普通装备经验阈值不符：{equipNormalThreshold.CurrentValue}（{version}）");
            var equipSpecialCap = Find(equipLevelExp, "equip-level-cap-special");
            TestSupport.Assert(equipSpecialCap.CurrentValue == (version == "6.6" ? "15" : "9") &&
                equipSpecialCap.Editable,
                $"宝物等级上限不符：{equipSpecialCap.CurrentValue}（{version}）");
            var equipNormalCap = Find(equipLevelExp, "equip-level-cap-normal");
            TestSupport.Assert(equipNormalCap.CurrentValue == (version == "6.6" ? "9" : "5") &&
                equipNormalCap.Editable,
                $"普通装备等级上限不符：{equipNormalCap.CurrentValue}（{version}）");
            var strategyEquipExp = equipLevelExp.Constants.Single(item => item.Constant.Name == "策略防具经验");
            TestSupport.Assert(strategyEquipExp.CurrentValue == (version == "6.6" ? "4" : "3") &&
                !strategyEquipExp.Editable,
                $"策略使用装备经验不符：{strategyEquipExp.CurrentValue}（{version}）");

            var merit = values.Single(value => value.Definition.Id == "merit-record");
            TestSupport.Assert(merit.Constants.Any(item =>
                    item.Constant.Name == "表基址" && item.CurrentValue == "0x508400"),
                "功勋表基址不符。");
            TestSupport.Assert(merit.Constants.Any(item =>
                    item.Constant.Name == "本场战功表" && item.CurrentValue == "0x508000"),
                "本场战功表基址不符。");
            TestSupport.Assert(merit.Constants.Any(item =>
                    item.Constant.Name == "战功累加" && item.CurrentValue == "0x0042AB8E"),
                "战功累加函数不符。");
            TestSupport.Assert(merit.Constants.Any(item =>
                    item.Constant.Name == "策略战功" && item.CurrentValue == "2/4"),
                "策略战功值不符。");
            TestSupport.Assert(merit.Constants.Any(item =>
                    item.Constant.Name == "上升上限" && item.CurrentValue == "65535"),
                "道具 HP/MP 上升上限不符。");
            TestSupport.Assert(merit.Steps.Count >= 9, "功勋步骤过少。");
            TestSupport.Assert(merit.Constants.Any(item =>
                    item.Constant.Name == "剧本设置命令" && item.CurrentValue == "0x11..0x1F"),
                "功勋剧本设置命令范围不符。");
            TestSupport.Assert(merit.Constants.Any(item =>
                    item.Constant.Name == "剧本奖励命令" && item.CurrentValue == "5 变量"),
                "功勋剧本奖励命令不符。");
            TestSupport.Assert(merit.Constants.Any(item =>
                    item.Constant.Name == "累加翻倍条件" &&
                    item.CurrentValue == "0x500E9A/0x505FDC/0x505F5C"),
                "战功累加翻倍条件不符。");

            var meritAllocation = values.Single(value => value.Definition.Id == "merit-allocation");
            var multiplierA = meritAllocation.Constants.Single(item =>
                item.Constant.Name == "倍率（0x409639/0x42AD3B）");
            var expectedMultiplierA = version == "6.4" ? "1" : version == "6.5" ? "25" : "50";
            TestSupport.Assert(multiplierA.CurrentValue == expectedMultiplierA,
                $"战功点倍率（A 组）不符：{multiplierA.CurrentValue}（{version}）");
            var multiplierB = meritAllocation.Constants.Single(item =>
                item.Constant.Name == "倍率（0x40C386/0x44CD8D）");
            var expectedMultiplierB = version == "6.4" ? "1" : version == "6.5" ? "25" : "10";
            TestSupport.Assert(multiplierB.CurrentValue == expectedMultiplierB,
                $"战功点倍率（B 组）不符：{multiplierB.CurrentValue}（{version}）");
            var thresholdBase = meritAllocation.Constants.Single(item => item.Constant.Name == "门槛基础");
            TestSupport.Assert(thresholdBase.CurrentValue == "50", "战功点门槛基础不符。");
            var allocationCap = meritAllocation.Constants.Single(item =>
                item.Constant.Name == (version == "6.4" ? "成长值上限（6.4）" : "成长值上限（6.5/6.6）"));
            TestSupport.Assert(allocationCap.CurrentValue == (version == "6.4" ? "100" : "110"),
                $"战功点分配上限不符：{allocationCap.CurrentValue}（{version}）");
            TestSupport.Assert(meritAllocation.Steps.Count >= 8, "战功点分配步骤过少。");

            var perTurnExp = values.Single(value => value.Definition.Id == "per-turn-exp");
            TestSupport.Assert(perTurnExp.Steps.Count >= 5, "每回合经验步骤过少。");
            TestSupport.Assert(perTurnExp.Constants.All(item => !item.Editable),
                "每回合经验的结构常量应保持只读。");
            var selector = perTurnExp.Constants.Single(item => item.Constant.Name == "选择器表");
            TestSupport.Assert(selector.CurrentValue ==
                    (version == "6.4" ? "1D 1E 1E" : version == "6.5" ? "00 00 00" : "1E 1E 1E"),
                $"每回合经验选择器表不符：{selector.CurrentValue}（{version}）");
            TestSupport.Assert(perTurnExp.Constants.Any(item =>
                    item.Constant.Name == "个人经验结算" && item.CurrentValue == "0x4088CD"),
                "每回合经验的个人经验结算不符。");

            var battleVars = values.Single(value => value.Definition.Id == "battle-variable-load");
            TestSupport.Assert(battleVars.Constants.Any(item =>
                    item.Constant.Name == "特殊目标写入" && item.CurrentValue == "0x496C96"),
                "战场变量装载的特殊目标写入不符。");
            TestSupport.Assert(battleVars.Constants.Any(item =>
                    item.Constant.Name == "命令名称" && item.CurrentValue == "未闭环"),
                "剧本变量名称不应被标成已闭环。");
            TestSupport.Assert(battleVars.Steps.Count >= 4, "战场变量装载步骤过少。");

            TestSupport.Assert(values.Sum(value => value.EditableCount) > 0, "当前基底没有可修改的常量。");

            var direct = service.Read(Path.Combine(copy, "Ekd5.exe"), version);
            TestSupport.Assert(direct.Count == values.Count, "直接读取与工作区读取条目数不一致。");
            TestSupport.Assert(direct.Zip(values).All(pair => pair.First.Definition.Id == pair.Second.Definition.Id),
                "直接读取与工作区读取顺序不一致。");
            TestSupport.Assert(HashService.Sha256(Path.Combine(sourceRoot, "Ekd5.exe")) == sourceHash,
                "战斗公式测试改动了基底源文件。");
            Console.WriteLine($"BATTLE_FORMULA_TESTS_OK version={version} formulas={values.Count} " +
                $"constants={values.Sum(value => value.Constants.Count)} " +
                $"editable={values.Sum(value => value.EditableCount)}");
        }
        finally
        {
            if (Directory.Exists(copy)) Directory.Delete(copy, true);
        }
    }

    private static BattleFormulaConstantValue Find(BattleFormulaValue value, string constantId)
        => value.Constants.Single(item => item.Constant.ConstantId == constantId);
}
