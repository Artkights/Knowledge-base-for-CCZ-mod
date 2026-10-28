using System.Data;
using DataManager.App;
using DataManager.Core.Binary;
using DataManager.Core.Csv;
using DataManager.Core.Domain;
using DataManager.Core.Editing;
using DataManager.Core.Migration;
using DataManager.Core.Models;
using DataManager.Core.Profiles;
using DataManager.Core.Workbooks;

namespace DataManager.Tests;

/// <summary>Real 6.4 fixtures remain read-only; every edit uses an isolated copy.</summary>
internal static class Ccz64CompatibilityTests
{
    public static void Run(string source64, string source65, string source66)
    {
        var originals = new[] { source64, source65, source66 }.ToDictionary(root => root,
            root => ProfileDetector.CoreFiles.ToDictionary(name => name, name => HashService.Sha256(ProjectFileLocator.Resolve(root, name))));
        ProfileTests.Run();
        var root = TestSupport.CreateCoreCopy(source64, restoreKnown65Snapshot: false);
        try
        {
            var workspace = Open(root);
            TestSupport.Assert(workspace.ProfileMatch?.MatchKind == ProfileMatchKind.Exact, "洗隋原样四核心必须精确识别");
            AssertLayout(workspace);
            RoundTrip(workspace);
            SaveHistory(workspace);
            CompatibleAndDamagedConsumers(root);
            Ui(root);
        }
        finally { Directory.Delete(root, true); }
        foreach (var other in new[] { source65, source66 })
        {
            Migrate(source64, other);
            Migrate(other, source64);
        }
        foreach (var pair in originals)
        foreach (var file in pair.Value)
            TestSupport.Assert(HashService.Sha256(ProjectFileLocator.Resolve(pair.Key, file.Key)) == file.Value, "回归改写了原件：" + pair.Key + "/" + file.Key);
        Console.WriteLine("CCZ64_COMPATIBILITY_TESTS_OK exact compatible consumers save undo redo CSV XLSX UI migration-4-directions originals-unchanged");
    }

    private static ProjectWorkspace Open(string root)
    {
        var workspace = new ProjectWorkspace(); workspace.Open(root); return workspace;
    }

    private static void AssertLayout(ProjectWorkspace workspace)
    {
        TestSupport.Assert(workspace.ActiveProfile.ProfileId == "ccz-6.4" && workspace.ActiveProfile.VariantId == "64-xisui-v1", "6.4 被误判为其他版本");
        var names = workspace.GetDocument("effect-names");
        TestSupport.Assert(names.Definition.DataOffset == 0xD0D60 && names.Data.Rows.Count == 180 && !names.Definition.IsWriteSupported,
            "6.4 名称池必须为180×16只读槽");
        TestSupport.Assert(new EffectNamePoolService().Read(workspace, EffectNameChannel.PersonalJob).Count == 180, "共享引用越过6.4名称池边界");
        foreach (var (key, offset) in new[] { ("person-r-assign", 0xE1000), ("person-s-assign", 0xD2800), ("strategy-terrain-availability", 0x1FECC) })
            TestSupport.Assert(workspace.GetDocument(key).Definition is { Capability: TableCapability.Editable } table && table.DataOffset == offset,
                "6.4 独立消费者未开放正确表：" + key);
        TestSupport.Assert(workspace.GetDocument("person-retreat-quotes").Definition is { DataOffset: 130000, RowCount: 49, RowSize: 200, Capability: TableCapability.Editable }, "6.4撤退台词真实区域未开放");
        TestSupport.Assert(!workspace.Documents.ContainsKey("strategy-extension"), "读取了未验证策略扩展区域");
        TestSupport.Assert(workspace.GetDocument("persons").Definition.Fields.Where(f => f.Offset >= 27).All(f => f.Policy == FieldPolicy.Editable) &&
            workspace.GetDocument("detailed-job-growth").Definition.Fields.Count(f => f.Offset >= 9 && f.Policy == FieldPolicy.Editable) == 26,
            "6.4已验证人物默认装备和兵种装备许可未开放");
        foreach (var category in Enum.GetValues<ExtendDataCategory>())
            TestSupport.Assert(!new ExtendDataService(workspace).GetStatus(category).Available, "洗隋不应自动生成拓展表");
        TestSupport.Assert(LayoutRevisionCompatibility.GetLegacyRevisions(workspace.RootPath, "ccz-6.4", "64-xisui-v1").Count == 1,
            "6.4必须只接受严格冻结的上一版独立修订");
        TestSupport.Assert(!LayoutRevisionCompatibility.IsCompatible(workspace.RootPath, "ccz-6.4", "64-xisui-v1", "DEADBEEF", workspace.ActiveProfile.LayoutRevision),
            "6.4 接受了未知旧修订");
    }

    private static void RoundTrip(ProjectWorkspace workspace)
    {
        var directory = Path.Combine(workspace.RootPath, "exchange"); Directory.CreateDirectory(directory);
        foreach (var document in workspace.Documents.Values)
        {
            var file = Path.Combine(directory, document.Definition.Key + ".csv");
            workspace.ExportCsv(document, file);
            var context = CsvService.ReadContext(file);
            TestSupport.Assert(context?.ProfileId == "ccz-6.4" && context.VariantId == "64-xisui-v1", "6.4 CSV身份丢失");
            TestSupport.Assert(workspace.ImportCsv(document, file).ChangedCells == 0 && !workspace.IsDirty, "6.4 CSV 原样回导产生修改：" + document.Definition.Key);
        }
        var workbooks = new PageWorkbookService(workspace);
        foreach (var kind in Enum.GetValues<BusinessPageKind>().Where(k => k != BusinessPageKind.PhysicalTables))
        {
            if (new BusinessDataService(workspace).GetAvailableTableKeys(kind).Count == 0) continue;
            var file = Path.Combine(directory, kind + ".xlsx");
            workbooks.Export(kind, file);
            TestSupport.Assert(workbooks.PreviewImport(kind, file).ChangedCells == 0 && !workspace.IsDirty, "6.4 XLSX 原样回导产生修改：" + kind);
        }
        var badCsv = Path.Combine(directory, "protected.csv");
        File.WriteAllText(badCsv, "ID,保留尾部\n0,00 00 00\n");
        var rejected = false;
        try { workspace.ImportCsv(workspace.GetDocument("persons"), badCsv); } catch (Exception error) when (error is InvalidDataException or InvalidOperationException) { rejected = true; }
        TestSupport.Assert(rejected && !workspace.IsDirty, "CSV允许写入6.4保留尾部");
        Console.WriteLine($"CCZ64_EXCHANGE_OK tables={workspace.Documents.Count} CSV and business XLSX");
    }

    private static void SaveHistory(ProjectWorkspace workspace)
    {
        var before = ProfileDetector.CoreFiles.ToDictionary(name => name, name => File.ReadAllBytes(ProjectFileLocator.Resolve(workspace.RootPath, name)));
        var edits = new List<CompositeCellEdit>();
        foreach (var (key, field) in new[] { ("persons", "武力"), ("person-r-assign", "R形象编号"), ("person-s-assign", "S形象编号"), ("strategy-terrain-availability", "允许掩码") })
        {
            var doc = workspace.GetDocument(key);
            // Keep stable semantic fields while covering first and final physical records.
            var actualField = doc.Definition.Fields.Any(f => f.Name == field) ? field : doc.Definition.Fields.First(f => f.Policy == FieldPolicy.Editable).Name;
            foreach (var row in new[] { 0, doc.Data.Rows.Count - 1 }.Distinct())
                edits.Add(new(key, row, actualField, (Convert.ToInt32(doc.Data.Rows[row][actualField]) + 1) % (key == "strategy-terrain-availability" ? 16 : 200)));
        }
        workspace.ApplyCompositeTransaction("6.4边界回归", edits);
        TestSupport.Assert(workspace.Save().Saved, "6.4跨表保存失败");
        var reopened = Open(workspace.RootPath); AssertLayout(reopened);
        foreach (var edit in edits)
            TestSupport.Assert(Convert.ToInt32(reopened.GetDocument(edit.TableKey).Data.Rows[edit.RowIndex][edit.FieldName]) == Convert.ToInt32(edit.NewValue), "6.4磁盘复读错误");
        var after = ProfileDetector.CoreFiles.ToDictionary(name => name, name => File.ReadAllBytes(ProjectFileLocator.Resolve(workspace.RootPath, name)));
        foreach (var name in before.Keys)
        {
            var allowed = new HashSet<int>();
            foreach (var edit in edits)
            {
                var definition = workspace.GetDocument(edit.TableKey).Definition;
                if (!definition.FileName.Equals(name, StringComparison.OrdinalIgnoreCase)) continue;
                var field = definition.Fields.Single(f => f.Name == edit.FieldName);
                foreach (var index in Enumerable.Range(checked((int)(definition.DataOffset + edit.RowIndex * (long)definition.RowSize + field.Offset)), field.Size)) allowed.Add(index);
            }
            TestSupport.Assert(before[name].Length == after[name].Length && before[name].Zip(after[name]).Select((pair, i) => pair.First == pair.Second || allowed.Contains(i)).All(x => x), "6.4保存越过修改字段：" + name);
        }
        TestSupport.Assert(reopened.UndoSaved().Success, "6.4保存历史无法撤回");
        foreach (var pair in before) TestSupport.Assert(File.ReadAllBytes(ProjectFileLocator.Resolve(workspace.RootPath, pair.Key)).SequenceEqual(pair.Value), "6.4历史撤回未逐字节恢复");
        TestSupport.Assert(reopened.RedoSaved().Success && reopened.UndoSaved().Success, "6.4历史无法重做再撤回");
    }

    private static void CompatibleAndDamagedConsumers(string root)
    {
        var path = Path.Combine(root, "Ekd5.exe"); var original = File.ReadAllBytes(path);
        try
        {
            var customized = original.ToArray();
            Array.Clear(customized, 0xD0D60, 16); EncodingService.GameEncoding.GetBytes("自定义名称").CopyTo(customized, 0xD0D60);
            File.WriteAllBytes(path, customized);
            var workspace = Open(root); AssertLayout(workspace);
            TestSupport.Assert(workspace.ProfileMatch?.MatchKind == ProfileMatchKind.Compatible, "6.4同布局自定义EXE不兼容");
            customized[0x8438] = 0x90; customized[0x5CD9] = 0x90; customized[0x18987] = 0x90; customized[0x1AB07] = 0x90;
            File.WriteAllBytes(path, customized);
            workspace = Open(root);
            foreach (var key in new[] { "person-r-assign", "person-s-assign", "strategy-terrain-availability", "effect-names" })
                TestSupport.Assert(!workspace.Documents.ContainsKey(key), "6.4消费者损坏仍开放继承表：" + key);
            TestSupport.Assert(new EffectNamePoolService().Read(workspace, EffectNameChannel.PersonalJob).Count == 0,
                "6.4名称探测失败后共享引用仍读取猜测偏移");
            TestSupport.Assert(workspace.Documents.ContainsKey("persons"), "辅助消费者缺失阻断普通数据");
        }
        finally { File.WriteAllBytes(path, original); }
    }

    private static void Ui(string root)
    {
        using var form = new MainForm(openDefaultProject: false) { Location = new Point(-32000, -32000), StartPosition = FormStartPosition.Manual };
        form.Show(); form.LoadProjectForSmokeTest(root); Application.DoEvents();
        foreach (var key in new[] { "人物", "兵种系", "兵种", "宝物", "策略", "商店", "拓展数据" })
        {
            form.SelectModuleForSmokeTest(key); Application.DoEvents();
            TestSupport.Assert(!form.StatusForSmokeTest.Contains("详情读取失败", StringComparison.Ordinal), "6.4业务页失败：" + key + " " + form.StatusForSmokeTest);
        }
        TestSupport.Assert(!form.WorkspaceForSmokeTest.IsDirty, "6.4 UI只读浏览产生修改"); form.Close();
        Console.WriteLine("CCZ64_UI_OK seven business pages");
    }

    private static void Migrate(string sourceOriginal, string targetOriginal)
    {
        var source = TestSupport.CreateCoreCopy(sourceOriginal, restoreKnown65Snapshot: false);
        var target = TestSupport.CreateCoreCopy(targetOriginal, restoreKnown65Snapshot: false);
        try
        {
            SeedMarker(source, 45);
            SeedMarker(target, 46);
            var sourceWorkspace = Open(source); var targetWorkspace = Open(target);
            var targetBefore = ProfileDetector.CoreFiles.ToDictionary(name => name, name => File.ReadAllBytes(ProjectFileLocator.Resolve(target, name)));
            var power = (Convert.ToInt32(targetWorkspace.GetDocument("persons").Data.Rows[0]["武力"]) + 1) % 100;
            var r = (Convert.ToInt32(targetWorkspace.GetDocument("person-r-assign").Data.Rows[0]["R形象ID"]) + 257) % 65536;
            sourceWorkspace.ApplyCompositeTransaction("迁移源准备", [new("persons", 0, "武力", power), new("person-r-assign", 0, "R形象ID", r)]);
            TestSupport.Assert(sourceWorkspace.Save().Saved, "6.4迁移源准备保存失败");
            var sourceHashes = ProfileDetector.CoreFiles.ToDictionary(name => name, name => HashService.Sha256(ProjectFileLocator.Resolve(source, name)));
            var migration = new MigrationService(); var plan = migration.Preview(source, target);
            var choices = plan.Changes.Select((change, index) => (change, index)).Where(pair => pair.change.Kind == MigrationChangeKind.Changed &&
                (pair.change.TableKey == "persons" && pair.change.Id == 0 && pair.change.FieldName == "武力" ||
                 pair.change.TableKey == "person-r-assign" && pair.change.Id == 0 ||
                 pair.change.TableKey == "items-high" && pair.change.Id == 109 && pair.change.FieldName is "宝物类型" or "装备特效号"))
                .ToDictionary(pair => pair.index, _ => MigrationChoice.Overwrite);
            TestSupport.Assert(choices.Count == 3 && !plan.WritableChanges.Any(c => c.TableKey == "persons" && c.FieldName == "保留尾部"), "6.4迁移边界或候选错误");
            var result = migration.Apply(plan, choices);
            TestSupport.Assert(result.Success && result.AppliedChanges == 3, "6.4跨版本迁移失败：" + string.Join("；", result.Messages));
            var reopened = Open(target);
            TestSupport.Assert(reopened.ActiveProfile.ProfileId == targetWorkspace.ActiveProfile.ProfileId && Convert.ToInt32(reopened.GetDocument("persons").Data.Rows[0]["武力"]) == power,
                "跨版本迁移没有保持目标布局和字段值");
            TestSupport.Assert(Convert.ToInt32(reopened.GetDocument("person-r-assign").Data.Rows[0]["R形象ID"]) == r, "迁移截断了16位R编号");
            var itemBytes = File.ReadAllBytes(ProjectFileLocator.Resolve(target, "Star.e5"));
            TestSupport.Assert(itemBytes[5 * 25 + 0x11] == 45 && itemBytes[5 * 25 + 0x12] == 2, "6.4跨版本实际效果/类别发生颠倒");
            var rOffset = targetWorkspace.GetDocument("person-r-assign").Definition.DataOffset;
            foreach (var pair in targetBefore)
            {
                var bytes = File.ReadAllBytes(ProjectFileLocator.Resolve(target, pair.Key));
                TestSupport.Assert(pair.Value.Length == bytes.Length && pair.Value.Zip(bytes).Select((p, i) => p.First == p.Second ||
                    pair.Key == "Data.e5" && i == 396 + 18 || pair.Key == "Star.e5" && i == 5 * 25 + 0x11 ||
                    pair.Key == "Ekd5.exe" && i >= rOffset && i < rOffset + 2).All(x => x), "逻辑迁移改写了其他字节：" + pair.Key);
            }
            var csv = Path.Combine(source, "cross.csv"); sourceWorkspace.ExportCsv(sourceWorkspace.GetDocument("persons"), csv);
            var rejected = false;
            try { reopened.ImportCsv(reopened.GetDocument("persons"), csv); } catch (InvalidDataException) { rejected = true; }
            TestSupport.Assert(rejected && !reopened.IsDirty, "跨Profile CSV未经迁移直接导入");
            var xlsx = Path.Combine(source, "cross.xlsx"); new PageWorkbookService(sourceWorkspace).Export(BusinessPageKind.Persons, xlsx);
            rejected = false;
            try { new PageWorkbookService(reopened).PreviewImport(BusinessPageKind.Persons, xlsx); } catch (InvalidDataException) { rejected = true; }
            TestSupport.Assert(rejected && !reopened.IsDirty, "跨Profile XLSX未经迁移直接导入");
            foreach (var pair in sourceHashes) TestSupport.Assert(HashService.Sha256(ProjectFileLocator.Resolve(source, pair.Key)) == pair.Value, "迁移改写源项目");
            Console.WriteLine($"CCZ64_MIGRATION_OK {sourceWorkspace.ActiveProfile.ProfileId}->{reopened.ActiveProfile.ProfileId} bytes isolated");
        }
        finally { Directory.Delete(source, true); Directory.Delete(target, true); }
    }

    private static void SeedMarker(string root, byte effect)
    {
        var path = ProjectFileLocator.Resolve(root, "Star.e5"); var bytes = File.ReadAllBytes(path);
        bytes[5 * 25 + 0x11] = effect; bytes[5 * 25 + 0x12] = 2; File.WriteAllBytes(path, bytes);
    }
}
