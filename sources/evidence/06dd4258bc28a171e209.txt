using System.Diagnostics;
using DataManager.Core.Binary;
using DataManager.Core.Editing;
using DataManager.Core.Models;
using DataManager.Core.Scanner;

namespace DataManager.Tests;

/// <summary>End-to-end allocation transactions on isolated copies of the three supported storage geometries.</summary>
internal static class ThreeBaseAssignmentTests
{
    public static void Run(string repositoryRoot)
    {
        foreach (var sample in new[] { (Name: "洗隋", Rows: 180, Slots: 1),
                     (Name: "加强版6.5未加密版", Rows: 255, Slots: 1),
                     (Name: "复刻版6.6山贼 国庆", Rows: 255, Slots: 2) })
        {
            var source = Path.Combine(repositoryRoot, "基底", sample.Name);
            var sourceHashes = new[] { "Ekd5.exe", "Data.e5", "Star.e5", "Imsg.e5" }
                .ToDictionary(name => name, name => HashService.Sha256(Path.Combine(source, name)));
            var copy = TestSupport.CreateCoreCopy(source, restoreKnown65Snapshot: false);
            try
            {
                var watch = Stopwatch.StartNew();
                var workspace = new ProjectWorkspace();
                workspace.Open(copy);
                var service = new EngineEffectAssignmentService();
                var report = new EngineEffectScanService().Scan(workspace);
                var catalog = service.Read(workspace, report);
                var layout = catalog.JobLayout!;
                Assert(layout is { Verified: true } && layout.RowCount == sample.Rows && layout.SlotCount == sample.Slots,
                    sample.Name + " 未开放实际分配布局。");
                var jobRows = catalog.Effects.Where(effect => effect.JobPoolVisible && effect.PersonalEffectId != null &&
                    effect.PersonalEffectId < layout.RowCount).ToArray();
                Assert(jobRows.Length == layout.RowCount && jobRows.Select(effect => effect.PersonalEffectId!.Value)
                    .Order().SequenceEqual(Enumerable.Range(0, layout.RowCount)), "兵种池未覆盖全部活动表行。");
                Assert(jobRows.All(effect => effect.CanBindJob && effect.JobSlots.Count == layout.SlotCount),
                    "未解析消费者错误阻断已定位兵种槽。");
                Assert(catalog.Effects.Where(effect => effect.PersonalEffectId >= layout.RowCount)
                    .All(effect => !effect.CanBindJob && effect.JobSlots.Count == 0), "名称池尾部越过实际分配表上界。");
                Assert(!workspace.IsDirty, "目录读取产生了数据草稿。");
                Console.WriteLine($"THREE_BASE_SCAN_OK {sample.Name} rows={layout.RowCount} slots={layout.SlotCount} elapsedMs={watch.ElapsedMilliseconds}");

                // With no consumer records at all, every located allocation row remains manageable.
                var noImplementation = service.Read(workspace, CurrentReport(report, []));
                Assert(noImplementation.Effects.Where(effect => effect.JobPoolVisible).Count(effect => effect.CanBindJob) == layout.RowCount,
                    "实现解析状态仍参与真实分配槽权限判断。");
                var noImplementationDraft = service.CreateDraft(noImplementation);
                Assert(service.StageJobBind(noImplementationDraft, $"effect:{layout.RowCount - 1}", 79, 197, 0).Success,
                    "无消费者的末行分配无法暂存。");

                var before = File.ReadAllBytes(report.ExePath);
                var target = jobRows.Single(effect => effect.PersonalEffectId == layout.RowCount - 1);
                var draft = service.CreateDraft(catalog);
                for (var slot = 0; slot < layout.SlotCount; slot++)
                    Assert(service.StageJobUnbind(draft, target.Key, slot).Success, "清空真实槽失败。");
                Assert(service.GetEffects(draft).Single(effect => effect.Key == target.Key).FreeJobSlots == layout.SlotCount,
                    "空槽数量不符。");
                Assert(service.StageJobBind(draft, target.Key, 0, 19).Success, "首空槽分配失败。");
                if (layout.SlotCount == 2)
                    Assert(service.StageJobBind(draft, target.Key, 1, 23).Success, "第二独立槽分配失败。");
                var full = service.StageJobBind(draft, target.Key, 2, 29);
                Assert(!full.Success && full.NeedsReplacement && full.ExistingSlots.Count == layout.SlotCount,
                    "满槽未要求明确替换。");
                Assert(service.StageJobBind(draft, target.Key, 2, 29, layout.SlotCount - 1).Success,
                    "明确选槽替换失败。");
                Assert(service.StageJobValue(draft, target.Key, 0, 37).Success, "真实N暂存失败。");
                Assert(!service.StageJobUnbind(draft, target.Key, layout.SlotCount).Success &&
                    !service.StageJobValue(draft, target.Key, 0, 256).Success &&
                    !service.StageJobBind(draft, target.Key, 80, 17).Success, "槽数或字段值域越界仍被接受。");
                var allowed = new HashSet<long>();
                for (var slot = 0; slot < layout.SlotCount; slot++)
                {
                    allowed.Add(layout.GetJobIdOffset(layout.RowCount - 1, slot));
                    allowed.Add(layout.GetJobValueOffset(layout.RowCount - 1, slot));
                }
                EngineEffectAssignmentEffect? linked = null;
                if (layout.SharedValue)
                {
                    linked = jobRows.First(effect => effect.SharedPersonIds.Count > 0 && effect.Key != target.Key);
                    var newValue = (linked.JobSlots[0].Value + 113) % 256;
                    Assert(service.StageJobValue(draft, linked.Key, 0, newValue).Success, "共用N暂存失败。");
                    allowed.Add(layout.GetJobValueOffset(linked.PersonalEffectId!.Value, 0));
                }
                var preview = service.BuildPreview(workspace, report, draft);
                Assert(preview.CanWrite, "兵种分配预览失败：" + string.Join("；", preview.Errors));
                if (linked != null)
                    Assert(preview.Impact.Any(text => text.Contains("共用N", StringComparison.Ordinal) &&
                        linked.SharedPersonIds.Any(id => text.Contains(id.ToString(), StringComparison.Ordinal))),
                        "共享N预览未列明受影响人物。");
                var candidate = preview.Candidates.Single(change => SamePath(change.FilePath, report.ExePath));
                AssertOnlyOwnedBytes(before, candidate.AfterBytes, allowed);
                AssertPersonIds(before, candidate.AfterBytes, layout);
                Assert(before.AsSpan().SequenceEqual(File.ReadAllBytes(report.ExePath)), "预览提前写盘。");
                var result = service.Commit(workspace, report, draft, preview);
                Assert(result.Success && !draft.HasPendingChanges && !workspace.IsDirty,
                    "兵种分配提交失败：" + result.Message);
                report = result.VerifiedReport ?? CurrentReport(report, report.Effects);
                catalog = service.Read(workspace, report);
                var actual = catalog.Effects.Single(effect => effect.Key == target.Key).JobSlots;
                Assert(actual[0].Value == 37 && actual[0].JobId == (layout.SlotCount == 1 ? 2 : 0), "首槽复读不符。");
                if (layout.SlotCount == 2)
                    Assert(actual[1].JobId == 2 && actual[1].Value == 29, "第二槽N被第一槽联动。");
                var written = File.ReadAllBytes(report.ExePath);
                AssertOnlyOwnedBytes(before, written, allowed);
                AssertPersonIds(before, written, layout);
                Console.WriteLine($"THREE_BASE_BIND_OK {sample.Name} lastRow={layout.RowCount - 1} " +
                    $"sharedN={layout.SharedValue} independentN=PASS personBytes=PASS tableBounds=PASS unparsedWritable=PASS");

                draft = service.CreateDraft(catalog);
                for (var slot = 0; slot < layout.SlotCount; slot++)
                    Assert(service.StageJobUnbind(draft, target.Key, slot).Success, "卸下分配失败。");
                preview = service.BuildPreview(workspace, report, draft);
                Assert(preview.CanWrite, "卸下预览失败：" + string.Join("；", preview.Errors));
                var unbindOffsets = Enumerable.Range(0, layout.SlotCount)
                    .Select(slot => layout.GetJobIdOffset(layout.RowCount - 1, slot)).ToHashSet();
                AssertOnlyOwnedBytes(written, preview.Candidates.Single(change => SamePath(change.FilePath, report.ExePath)).AfterBytes, unbindOffsets);
                result = service.Commit(workspace, report, draft, preview);
                Assert(result.Success, "卸下提交失败：" + result.Message);
                report = result.VerifiedReport ?? CurrentReport(report, report.Effects);
                catalog = service.Read(workspace, report);
                var unloaded = catalog.Effects.Single(effect => effect.Key == target.Key).JobSlots;
                Assert(unloaded.All(slot => slot.JobId == 255) && unloaded.Select(slot => slot.Value).SequenceEqual(actual.Select(slot => slot.Value)),
                    "卸下兵种时修改了共享或独立N。");
                var final = File.ReadAllBytes(report.ExePath);
                AssertOnlyOwnedBytes(written, final, unbindOffsets);
                AssertPersonIds(before, final, layout);
                AssertUnknownLayoutRefusesWrite(workspace, report, catalog, service, final);
                Console.WriteLine($"THREE_BASE_UNBIND_OK {sample.Name} FF=PASS NPreserved=PASS unknownLayoutRejected=PASS elapsedMs={watch.ElapsedMilliseconds}");
            }
            finally
            {
                Directory.Delete(copy, true);
                foreach (var pair in sourceHashes)
                    Assert(HashService.Sha256(Path.Combine(source, pair.Key)) == pair.Value, "测试改动了真实基底 " + pair.Key);
                Console.WriteLine("THREE_BASE_SOURCE_UNCHANGED " + sample.Name);
            }
        }
        Console.WriteLine("THREE_BASE_ASSIGNMENT_TESTS_OK samples=3");
    }

    private static void AssertUnknownLayoutRefusesWrite(ProjectWorkspace workspace, EngineEffectScanReport report,
        EngineEffectAssignmentCatalog catalog, EngineEffectAssignmentService service, byte[] original)
    {
        var bad = (byte[])original.Clone();
        // provider entry is in the first executable section with VA/file delta 0x400C00 in these fixtures.
        bad[0x1241E] ^= 1;
        File.WriteAllBytes(report.ExePath, bad);
        try
        {
            var badReport = CurrentReport(report, report.Effects);
            var rejected = service.Read(workspace, badReport);
            Assert(!rejected.JobLayoutVerified && rejected.Effects.All(effect => !effect.CanBindJob), "未知布局仍开放兵种编辑。");
            var clean = service.CreateDraft(rejected);
            Assert(!service.StageJobBind(clean, $"effect:{catalog.JobLayout!.RowCount - 1}", 0, 11).Success,
                "未知布局仍可暂存分配。");
            var stale = service.CreateDraft(catalog with { ExeSha256 = badReport.ExeSha256 });
            var row = catalog.Effects.First(effect => effect.CanBindJob);
            stale.JobTargets[row.Key] = row.JobSlots.Select((slot, index) => index == 0 ? slot with { JobId = 79 } : slot).ToArray();
            var preview = service.BuildPreview(workspace, badReport, stale);
            Assert(!preview.CanWrite && preview.Errors.Any(text => text.Contains("真实兵种", StringComparison.Ordinal)),
                "通过陈旧目录直接提供的槽草稿绕过了当前布局复验。");
        }
        finally { File.WriteAllBytes(report.ExePath, original); }
    }

    private static EngineEffectScanReport CurrentReport(EngineEffectScanReport report, IReadOnlyList<EngineEffectScanRow> rows)
        => new() { ExePath = report.ExePath, ExeSha256 = HashService.Sha256(report.ExePath),
            EngineVersion = report.EngineVersion, Effects = rows };

    private static void AssertOnlyOwnedBytes(byte[] before, byte[] after, IReadOnlySet<long> allowed)
    {
        Assert(before.Length == after.Length, "分配事务修改了文件长度。");
        for (var offset = 0; offset < before.Length; offset++)
            if (before[offset] != after[offset]) Assert(allowed.Contains(offset), $"分配事务修改了非归属字节0x{offset:X}。");
    }

    private static void AssertPersonIds(byte[] before, byte[] after, EffectAssignmentLayout layout)
    {
        for (var row = 0; row < layout.RowCount; row++)
            Assert(layout.ReadPersonIds(before, row).SequenceEqual(layout.ReadPersonIds(after, row)), $"特效{row}的原人物分配被修改。");
    }

    private static bool SamePath(string first, string second)
        => Path.GetFullPath(first).Equals(Path.GetFullPath(second), StringComparison.OrdinalIgnoreCase);

    private static void Assert(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }
}
