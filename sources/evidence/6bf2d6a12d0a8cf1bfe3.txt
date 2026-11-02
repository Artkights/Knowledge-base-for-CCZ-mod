using System.Buffers.Binary;
using System.Text.Json;
using DataManager.App;
using DataManager.Core.Binary;
using DataManager.Core.Appearance;
using DataManager.Core.Csv;
using DataManager.Core.Domain;
using DataManager.Core.Editing;
using DataManager.Core.Migration;
using DataManager.Core.Workbooks;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;

namespace DataManager.Tests;

internal static class AppearanceSaveIntegrationTests
{
    public static void Run(string path)
    {
        var source = Directory.Exists(Path.Combine(path, "基底")) ? Path.Combine(path, "基底", "加强版6.5未加密版") : path;
        SaveScopeAndHistory(source);
        ExchangeAndTopSave(source);
        LatePrimaryFailure(source);
        MigrationTarget(source);
        RealEngineSaveMatrix(Directory.Exists(Path.Combine(path, "基底")) ? path : TestSupport.RepositoryRootFromBase(path));
        Console.WriteLine("APPEARANCE_SAVE_INTEGRATION_OK (4 suites)");
    }

    private static void RealEngineSaveMatrix(string repository)
    {
        foreach (var (profile, relative) in new[] { ("ccz-6.4", "洗隋"), ("ccz-6.5", "加强版6.5未加密版"),
            ("ccz-6.6", "复刻版6.6山贼"), ("ccz-6.6", "复刻版6.6山贼 国庆"),
            ("ccz-6.6", "曹操传6.6-V10.1 【解压密码：66】/复刻版6.6") })
        {
            var source = Path.Combine(repository, "基底", relative); var root = Path.Combine(Path.GetTempPath(), "AppearanceMatrix_" + Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(Path.Combine(root, "SV"));
            try
            {
                foreach (var save in Directory.EnumerateFiles(Path.Combine(source, "SV"), "*.E5S"))
                    File.Copy(save, Path.Combine(root, "SV", Path.GetFileName(save)));
                var session = SaveAppearanceSyncService.Prepare(root, profile, File.ReadAllBytes(Path.Combine(source, "Ekd5.exe")), [new(0, 777, 778)]);
                if (relative == "复刻版6.6山贼")
                {
                    session.Commit();
                    TestSupport.Assert(session.PreparedGroups.Count == 0 && session.Report.UpdatedSaves == 0 && !session.Report.HasWarnings, "无存档项目应正常保存且无需同步");
                    Console.WriteLine("PASS real-save matrix 复刻版6.6山贼: no actual save slots; no-op");
                    continue;
                }
                TestSupport.Assert(session.PreparedGroups.Count > 0, relative + "没有可同步的原生真实样本");
                var before = session.PreparedGroups.ToDictionary(g => g.SaveRelativePath, g => File.ReadAllBytes(Path.Combine(root, g.SaveRelativePath)));
                session.Commit();
                TestSupport.Assert(session.Report.UpdatedSaves == before.Count, relative + "真实样本提交失败");
                foreach (var pair in before)
                {
                    var after = File.ReadAllBytes(Path.Combine(root, pair.Key)); var expected = (byte[])pair.Value.Clone();
                    BinaryPrimitives.WriteUInt16LittleEndian(expected.AsSpan(0xE800, 2), 777); BinaryPrimitives.WriteUInt16LittleEndian(expected.AsSpan(0, 2), 778);
                    if (expected.AsSpan(expected.Length - 168, 8).SequenceEqual("XASTAT2F"u8))
                    {
                        var nativeLength = checked((int)BinaryPrimitives.ReadUInt64LittleEndian(expected.AsSpan(expected.Length - 168 + 16, 8)));
                        System.Text.Encoding.ASCII.GetBytes(HashService.Sha256(expected[..nativeLength])).CopyTo(expected, expected.Length - 168 + 32);
                    }
                    TestSupport.Assert(after.SequenceEqual(expected), relative + "/" + pair.Key + "出现非目标字节修改");
                }
                session.Rollback();
                TestSupport.Assert(before.All(pair => File.ReadAllBytes(Path.Combine(root, pair.Key)).SequenceEqual(pair.Value)), relative + "整批恢复失败");
                Console.WriteLine($"PASS real-save matrix {relative}: updated={before.Count}, unchanged={session.Report.UnchangedSaves}, skipped={session.Report.SkippedSaves}; bytewise scope + rollback");
            }
            finally { Directory.Delete(root, true); }
        }
    }

    private static void SaveScopeAndHistory(string source) => WithFixture(source, (root, native) =>
    {
        var workspace = Open(root);
        var exe = File.ReadAllBytes(Path.Combine(root, "Ekd5.exe"));
        workspace.ApplyCompositeTransaction("R only", [new("person-r-assign", 0, "R形象ID", 61)]);
        var result = workspace.Save();
        TestSupport.Assert(result.Saved && result.AppearanceSync?.UpdatedSaves == 2 && result.AppearanceSync.SkippedSaves == 1,
            "坏档不应阻断主形象与其余存档：" + string.Join("；", result.Messages));
        AssertScope(native, Read(root), [(0xE800, (ushort)61)]);
        var afterExe = File.ReadAllBytes(Path.Combine(root, "Ekd5.exe")); var afterSave = Read(root);
        TestSupport.Assert(workspace.UndoSaved().Success && File.ReadAllBytes(Path.Combine(root, "Ekd5.exe")).SequenceEqual(exe) && Read(root).SequenceEqual(native), "一次撤回未恢复EXE和所有成功存档");
        TestSupport.Assert(workspace.RedoSaved().Success && File.ReadAllBytes(Path.Combine(root, "Ekd5.exe")).SequenceEqual(afterExe) && Read(root).SequenceEqual(afterSave), "一次重做未恢复EXE和存档");
        workspace.ApplyCompositeTransaction("S compact boundaries", [new("person-s-assign", 0, "S形象ID", 0),
            new("person-s-assign", 1, "S形象ID", 32), new("person-s-assign", 2, "S形象ID", 33),
            new("person-s-assign", 3, "S形象ID", 1023)]);
        result = workspace.Save();
        TestSupport.Assert(result.Saved, "S批量保存失败：" + string.Join("；", result.Messages));
        AssertScope(afterSave, Read(root), [(0, (ushort)0), (2, (ushort)32), (4, (ushort)33), (6, (ushort)1023)]);
        TestSupport.Assert(File.ReadAllBytes(Path.Combine(root, "SV", "SV998.E5S")).SequenceEqual(new byte[37]), "坏档被修改");
        TestSupport.Assert(result.History!.Files.Count == 3, "主文件与两成功存档未进入同一历史");
        Console.WriteLine("PASS assignment R-only/S-only/multi-save/S0/32/33/high-id/history/scope");
    });

    private static void ExchangeAndTopSave(string source) => WithFixture(source, (root, native) =>
    {
        using var form = new MainForm(openDefaultProject: false)
        { StartPosition = FormStartPosition.Manual, Location = new Point(-32000, -32000), ShowInTaskbar = false };
        form.Show(); form.LoadProjectForSmokeTest(root); Application.DoEvents();
        var workspace = form.WorkspaceForSmokeTest;
        var document = workspace.GetDocument("person-r-assign");
        var csv = Path.Combine(root, "R.csv"); workspace.ExportCsv(document, csv);
        var records = CsvService.ReadRecords(csv, document.Data.Columns.Cast<System.Data.DataColumn>().Select(c => c.ColumnName))
            .Select(row => row.ToArray()).ToArray();
        records[2][1] = "62";
        CsvService.WriteRecords(csv, records);
        TestSupport.Assert(workspace.ImportCsv(document, csv).ChangedCells == 1 && Read(root).SequenceEqual(native), "CSV导入应先进入草稿");
        TestSupport.Assert(form.SavePendingForSmokeTest().Saved, "CSV顶部保存失败");
        AssertScope(native, Read(root), [(0xE800, (ushort)62)]);
        var before = Read(root);
        var workbook = new PageWorkbookService(workspace); var xlsx = Path.Combine(root, "人物.xlsx");
        workbook.Export(BusinessPageKind.Persons, xlsx);
        EditWorkbook(xlsx, "person-s-assign", "S形象ID", "34");
        var preview = workbook.PreviewImport(BusinessPageKind.Persons, xlsx);
        TestSupport.Assert(preview.ChangedCells == 1, "工作簿未识别S指定变更");
        workbook.ApplyImport(preview);
        TestSupport.Assert(Read(root).SequenceEqual(before) && form.SavePendingForSmokeTest().Saved, "工作簿草稿/顶部保存边界异常");
        AssertScope(before, Read(root), [(0, (ushort)34)]);
        form.Close();
        Console.WriteLine("PASS CSV + workbook + actual MainForm top-save route");
    });

    private static void LatePrimaryFailure(string source) => WithFixture(source, (root, native) =>
    {
        var workspace = Open(root); var before = File.ReadAllBytes(Path.Combine(root, "Ekd5.exe"));
        workspace.ApplyCompositeTransaction("late failure", [new("person-r-assign", 0, "R形象ID", 64)]);
        workspace.RegisterDraftParticipant(new FailingDraft());
        var result = workspace.Save();
        TestSupport.Assert(!result.Saved && workspace.IsDirty && Read(root).SequenceEqual(native) &&
            File.ReadAllBytes(Path.Combine(root, "Ekd5.exe")).SequenceEqual(before), "全局失败未恢复主文件/成功存档/草稿");
        Console.WriteLine("PASS primary late failure rolls back successful save groups and preserves draft");
    });

    private static void MigrationTarget(string source) => WithFixture(source, (target, native) =>
    {
        var origin = TestSupport.CreateCoreCopy(source);
        try
        {
            Directory.CreateDirectory(Path.Combine(origin, "SV")); File.WriteAllBytes(Path.Combine(origin, "SV", "SV003.E5S"), native);
            var sourceWorkspace = Open(origin);
            sourceWorkspace.ApplyCompositeTransaction("migration source", [new("person-s-assign", 0, "S形象ID", 35)]);
            TestSupport.Assert(sourceWorkspace.Save().Saved, "迁移源指定准备失败");
            var sourceSave = File.ReadAllBytes(Path.Combine(origin, "SV", "SV003.E5S"));
            var sourceExe = File.ReadAllBytes(Path.Combine(origin, "Ekd5.exe"));
            var targetExe = File.ReadAllBytes(Path.Combine(target, "Ekd5.exe"));
            var service = new MigrationService(); var plan = service.Preview(origin, target);
            var choices = plan.Changes.Select((change, index) => (change, index))
                .Where(x => x.change.TableKey == "person-s-assign" && x.change.Id == 0)
                .ToDictionary(x => x.index, _ => MigrationChoice.Overwrite);
            TestSupport.Assert(choices.Count == 1, "迁移计划缺少S指定");
            var result = service.Apply(plan, choices);
            TestSupport.Assert(result.Success && result.AppearanceSync?.UpdatedSaves == 2 && result.AppearanceSync.SkippedSaves == 1,
                "迁移目标同步失败：" + string.Join("；", result.Messages));
            AssertScope(native, Read(target), [(0, (ushort)35)]);
            TestSupport.Assert(!File.Exists(Path.Combine(target, "SV", "SV003.E5S")) &&
                File.ReadAllBytes(Path.Combine(origin, "SV", "SV003.E5S")).SequenceEqual(sourceSave) &&
                File.ReadAllBytes(Path.Combine(origin, "Ekd5.exe")).SequenceEqual(sourceExe), "源档被迁入目标或源文件被修改");
            var workspace = Open(target); var migratedSave = Read(target);
            TestSupport.Assert(workspace.UndoSaved().Success && Read(target).SequenceEqual(native) &&
                File.ReadAllBytes(Path.Combine(target, "Ekd5.exe")).SequenceEqual(targetExe), "迁移撤回未同时恢复指定与存档");
            TestSupport.Assert(workspace.RedoSaved().Success && Read(target).SequenceEqual(migratedSave), "迁移重做未恢复同步存档");
            Console.WriteLine("PASS migration target-only + bad save skip + undo/redo + source unchanged");
        }
        finally { Directory.Delete(origin, true); }
    });

    private static void EditWorkbook(string path, string table, string field, string value)
    {
        using var package = SpreadsheetDocument.Open(path, true); var part = package.WorkbookPart!;
        var sheets = part.Workbook.Sheets!.Elements<Sheet>().ToArray(); var meta = sheets.Single(s => s.Name == "_DataManager");
        var json = string.Concat(((WorksheetPart)part.GetPartById(meta.Id!)).Worksheet.Descendants<Text>().Select(t => t.Text));
        using var manifest = JsonDocument.Parse(json);
        var id = manifest.RootElement.GetProperty("Datasets").EnumerateArray().Single(d => d.GetProperty("Key").GetString() == table).GetProperty("SheetId").GetUInt32();
        var sheet = (WorksheetPart)part.GetPartById(sheets.Single(s => s.SheetId?.Value == id).Id!);
        var rows = sheet.Worksheet.GetFirstChild<SheetData>()!;
        var header = rows.Elements<Row>().First().Elements<Cell>().Single(c => c.InnerText == field);
        var column = new string(header.CellReference!.Value!.TakeWhile(char.IsLetter).ToArray());
        var cell = rows.Elements<Row>().Single(r => r.RowIndex?.Value == 3).Elements<Cell>().Single(c => c.CellReference == column + "3");
        cell.RemoveAllChildren(); cell.DataType = CellValues.InlineString; cell.InlineString = new InlineString(new Text(value));
        sheet.Worksheet.Save();
    }

    private sealed class FailingDraft : IWorkspaceDraftParticipant
    { public bool HasPendingChanges => true; public void AcceptSaved() => throw new IOException("injected late acceptance failure"); public void Discard() { } }
    private static ProjectWorkspace Open(string root) { var workspace = new ProjectWorkspace(); workspace.Open(root); return workspace; }
    private static byte[] Read(string root) => File.ReadAllBytes(Path.Combine(root, "SV", "SV001.E5S"));
    private static void AssertScope(byte[] before, byte[] after, (int Offset, ushort Value)[] changes)
    {
        var expected = (byte[])before.Clone();
        foreach (var (offset, value) in changes) BinaryPrimitives.WriteUInt16LittleEndian(expected.AsSpan(offset, 2), value);
        TestSupport.Assert(after.SequenceEqual(expected), "同步未严格限定到本次目标R/S字段，或人物紧凑编号被错误转换");
    }
    private static void WithFixture(string source, Action<string, byte[]> action)
    {
        var root = TestSupport.CreateCoreCopy(source);
        try
        {
            var native = File.ReadAllBytes(Path.Combine(source, "SV", "SV004.E5S"));
            Directory.CreateDirectory(Path.Combine(root, "SV"));
            File.WriteAllBytes(Path.Combine(root, "SV", "SV001.E5S"), native);
            File.WriteAllBytes(Path.Combine(root, "SV", "SV002.E5S"), native);
            File.WriteAllBytes(Path.Combine(root, "SV", "SV998.E5S"), new byte[37]);
            action(root, native);
        }
        finally { Directory.Delete(root, true); }
    }
}
