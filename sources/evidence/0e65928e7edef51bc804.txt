using DataManager.Core.Binary;
using DataManager.Core.Editing;
using DataManager.Core.Scanner;

namespace DataManager.Tests;

internal static class EngineBattleFormulaWriteTests
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
            var exe = Path.Combine(copy, "Ekd5.exe");

            WriteAndVerify(workspace, service, exe, version, "hit-curve-high-base", 80);
            WriteAndVerify(workspace, service, exe, version, "hit-curve-high-base", 90);
            WriteAndVerify(workspace, service, exe, version, "physical-damage-base", 30);
            WriteAndVerify(workspace, service, exe, version, "physical-damage-base", 25);
            WriteAndVerify(workspace, service, exe, version, "rate-curve-cap", 90);
            WriteAndVerify(workspace, service, exe, version, "rate-curve-cap", 100);

            foreach (var constantId in new[]
                     {
                         "personal-exp-base", "personal-exp-kill-flat", "personal-exp-kill-ratio-num",
                         "personal-exp-kill-ratio-offset", "exp-multiplier-base", "weapon-exp-base",
                         "weapon-exp-no-damage", "armor-exp-base", "armor-exp-no-damage",
                         "char-exp-max-level", "char-exp-threshold", "char-exp-band-65", "char-exp-step-65",
                         "equip-exp-threshold-special", "equip-exp-threshold-normal",
                         "equip-level-cap-special", "equip-level-cap-normal"
                     })
                ProbeAndRestore(workspace, service, exe, version, constantId);

            if (version == "6.6")
            {
                WriteAndVerify(workspace, service, exe, version, "hit-curve-floor-66", 20);
                var floor = ConstantValue(exe, version, "hit-curve-floor-66");
                TestSupport.Assert(floor.SecondaryFileOffset >= 0 &&
                    File.ReadAllBytes(exe)[checked((int)floor.SecondaryFileOffset)] == 20,
                    "6.6 命中下限次字段没有同步写入。");
                WriteAndVerify(workspace, service, exe, version, "hit-curve-floor-66", 25);
            }
            else
            {
                var pool = ConstantValue(exe, version, "physical-crit-pool");
                var probe = pool.NumericValue == 2 ? 3 : 1;
                WriteAndVerify(workspace, service, exe, version, "physical-crit-pool", probe);
                WriteAndVerify(workspace, service, exe, version, "physical-crit-pool", pool.NumericValue!.Value);
            }

            var beforeInvalid = HashService.Sha256(exe);
            var invalid = new[]
            {
                new BattleFormulaEdit("hit-curve-high-base", 95),
                new BattleFormulaEdit("hit-curve-cap", 90)
            };
            var issues = service.ValidateEdits(workspace, invalid);
            TestSupport.Assert(issues.Any(item => item.Severity == BattleFormulaIssueSeverity.Error),
                "非法曲线组合没有返回错误。");
            var failed = service.Commit(workspace, invalid);
            TestSupport.Assert(!failed.Success, "非法曲线组合仍然写入成功。");
            TestSupport.Assert(HashService.Sha256(exe) == beforeInvalid,
                "非法曲线组合改动了文件。");

            var capOnly = new[] { new BattleFormulaEdit("hit-curve-cap", 90) };
            var capIssues = service.ValidateEdits(workspace, capOnly);
            TestSupport.Assert(capIssues.All(item => item.Severity != BattleFormulaIssueSeverity.Error),
                "只改命中上限被错误拦截。");
            TestSupport.Assert(capIssues.Any(item => item.Severity == BattleFormulaIssueSeverity.Warning),
                "只改命中上限没有给出截断提示。");
            var capCommit = service.Commit(workspace, capOnly);
            TestSupport.Assert(capCommit.Success, "只改命中上限写入失败：" + capCommit.Message);
            TestSupport.Assert(FormulaValue(workspace, service, "hit-curve")
                    .Constants.Single(item => item.Constant.ConstantId == "hit-curve-cap").CurrentValue == "90",
                "命中上限写入后复读不一致。");
            WriteAndVerify(workspace, service, exe, version, "hit-curve-cap", 100);

            TestSupport.Assert(HashService.Sha256(Path.Combine(sourceRoot, "Ekd5.exe")) == sourceHash,
                "战斗公式写入测试改动了基底源文件。");
            Console.WriteLine($"BATTLE_FORMULA_WRITE_OK version={version}");
        }
        finally
        {
            if (Directory.Exists(copy)) Directory.Delete(copy, true);
        }
    }

    private static void WriteAndVerify(ProjectWorkspace workspace, EngineBattleFormulaService service,
        string exe, string version, string constantId, int value)
    {
        var result = service.Commit(workspace, [new BattleFormulaEdit(constantId, value)]);
        TestSupport.Assert(result.Success, $"{constantId} 写入失败：{result.Message}");
        var actual = ConstantValue(exe, version, constantId);
        TestSupport.Assert(actual.NumericValue == value,
            $"{constantId} 复读不符：{actual.NumericValue} != {value}");
        var bytes = File.ReadAllBytes(exe);
        var written = actual.Layout.Length == 1
            ? bytes[checked((int)actual.FileOffset)]
            : BitConverter.ToInt32(bytes, checked((int)actual.FileOffset));
        TestSupport.Assert(written == value, $"{constantId} 文件字节未写到位：{written}");
    }

    private static void ProbeAndRestore(ProjectWorkspace workspace, EngineBattleFormulaService service,
        string exe, string version, string constantId)
    {
        var original = ConstantValue(exe, version, constantId);
        if (!original.SignatureMatches || original.NumericValue is not { } current) return;
        var probe = current <= original.Definition.Minimum ? current + 1 : current - 1;
        if (probe > original.Definition.Maximum) probe = current - 1;
        WriteAndVerify(workspace, service, exe, version, constantId, probe);
        WriteAndVerify(workspace, service, exe, version, constantId, current);
    }

    private static EngineConstantValue ConstantValue(string exe, string version, string constantId)
        => new EngineConstantService().Read(exe, version).Single(item => item.Definition.Id == constantId);

    private static BattleFormulaValue FormulaValue(ProjectWorkspace workspace,
        EngineBattleFormulaService service, string formulaId)
        => service.ReadFormula(workspace, formulaId)
           ?? throw new InvalidDataException("找不到公式：" + formulaId);
}
