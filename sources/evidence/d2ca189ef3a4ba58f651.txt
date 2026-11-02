using DataManager.Core.Domain;
using DataManager.Core.Editing;
using DataManager.Core.Workbooks;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;
using DocumentFormat.OpenXml.Validation;

namespace DataManager.Tests;

internal static class PageWorkbookTests
{
    public static void Run(string source)
    {
        WorkbookTextEncodingTests.Run();
        var root = TestSupport.CreateCoreCopy(source);
        try
        {
            var workspace = new ProjectWorkspace(); workspace.Open(root);
            var service = new PageWorkbookService(workspace);
            var file = Path.Combine(root, "人物.xlsx");
            foreach (var page in Enum.GetValues<BusinessPageKind>().Where(p => p != BusinessPageKind.PhysicalTables))
            {
                if (new BusinessDataService(workspace).GetAvailableTableKeys(page).Count == 0) continue;
                var path = Path.Combine(root, page + ".xlsx"); service.Export(page, path);
                TestSupport.Assert(service.PreviewImport(page, path).ChangedCells == 0 && !workspace.IsDirty,
                    $"{page} 工作簿原样回导应为零修改");
                using var package = SpreadsheetDocument.Open(path, false);
                var errors = new OpenXmlValidator().Validate(package).Take(3).ToArray();
                TestSupport.Assert(errors.Length == 0, $"{page} XLSX schema 无效：" + string.Join(';', errors.Select(e => e.Description)));
                Console.WriteLine($"WORKBOOK_ROUNDTRIP_OK {page} {new FileInfo(path).Length} bytes");
            }
            service.Export(BusinessPageKind.Persons, file);
            var person = workspace.GetDocument("persons"); var old = Convert.ToInt32(person.Data.Rows[0]["武力"]); var next = (old + 1) % 100;
            Edit(file, "persons", "武力", 3, next.ToString());
            var preview = service.PreviewImport(BusinessPageKind.Persons, file);
            TestSupport.Assert(preview.ChangedCells == 1 && preview.Changes[0].Cell.Length > 1 && !workspace.IsDirty, "工作簿预检提前改变了游戏草稿");
            TestSupport.Assert(service.ApplyImport(preview) == 1 && Convert.ToInt32(person.Data.Rows[0]["武力"]) == next, "工作簿没有应用变更");
            workspace.Commands.Undo(); TestSupport.Assert(Convert.ToInt32(person.Data.Rows[0]["武力"]) == old && !workspace.IsDirty, "工作簿不能整次撤回");
            workspace.Commands.Redo(); TestSupport.Assert(Convert.ToInt32(person.Data.Rows[0]["武力"]) == next, "工作簿不能整次重做");
            TestSupport.Assert(service.PreviewImport(BusinessPageKind.Persons, file).ChangedCells == 0, "同一文件重复导入应无修改");
            workspace.Commands.Undo();
            workspace.ApplyCompositeTransaction("并发草稿", [new("persons", 0, "武力", (old + 2) % 100)]);
            Reject(() => service.PreviewImport(BusinessPageKind.Persons, file), "冲突");
            workspace.Commands.Undo();
            preview = service.PreviewImport(BusinessPageKind.Persons, file);
            workspace.ApplyCompositeTransaction("预览后草稿", [new("persons", 0, "武力", (old + 3) % 100)]);
            Reject(() => service.ApplyImport(preview), "预览后"); workspace.Commands.Undo();

            CheckRejected("重复 ID", f => Edit(f, "persons", "ID", 4, "0"));
            CheckRejected("不存在", f => Edit(f, "persons", "ID", 3, "999999"));
            CheckRejected("公式", f => Edit(f, "persons", "武力", 3, "10", formula: "5+5"));
            CheckRejected("实际值", f => Edit(f, "persons", "武力", 3, "999999"));
            CheckRejected("实际值", f => Edit(f, "persons", "名称", 3, new string('长', 100)));
            CheckRejected("缺少", f => MutateSheet(f, "persons", (p, s) => s.Remove()));
            CheckRejected("未知", f => Edit(f, "persons", "武力", 1, "未知字段"));

            var partial = Path.Combine(root, "缺行与重命名.xlsx"); service.Export(BusinessPageKind.Persons, partial);
            MutateSheet(partial, "persons", (p, sheet) =>
            {
                sheet.Name = "自由改名"; var part = (WorksheetPart)p.GetPartById(sheet.Id!);
                part.Worksheet.GetFirstChild<SheetData>()!.Elements<Row>().Single(r => r.RowIndex?.Value == 4).Remove();
                p.Workbook.Sheets!.RemoveChild(sheet); p.Workbook.Sheets!.AppendChild(sheet);
            });
            TestSupport.Assert(service.PreviewImport(BusinessPageKind.Persons, partial).ChangedCells == 0, "重命名/重排页签/缺行被误解释为删除或新增");

            var items = Path.Combine(root, "宝物白名单.xlsx"); service.Export(BusinessPageKind.Items, items);
            AssertFields(items, "detailed-job-growth", f => f == "ID" || ItemTypeService.EquipmentColumns.Contains(f), 27);
            Edit(items, "detailed-job-growth", ItemTypeService.EquipmentColumns[0], 1, "攻击成长");
            Reject(() => service.PreviewImport(BusinessPageKind.Items, items), "未知");
            var jobs = Path.Combine(root, "兵种白名单.xlsx"); service.Export(BusinessPageKind.DetailedJobs, jobs);
            AssertFields(jobs, "strategies", f => f is "ID" or "名称" or "策略名称" || f.Contains("学习等级"), null);
            Edit(jobs, "strategies", "名称", 3, "越界修改");
            Reject(() => service.PreviewImport(BusinessPageKind.DetailedJobs, jobs), "只读");
            Console.WriteLine("PAGE_WORKBOOK_TESTS_OK");

            void CheckRejected(string reason, Action<string> mutate)
            {
                var bad = Path.Combine(root, "错误.xlsx"); service.Export(BusinessPageKind.Persons, bad);
                // A valid edit on an earlier cell must not leak when any later cell fails.
                Edit(bad, "persons", "武力", 3, next.ToString()); mutate(bad);
                Reject(() => service.PreviewImport(BusinessPageKind.Persons, bad), reason);
                TestSupport.Assert(!workspace.IsDirty && Convert.ToInt32(person.Data.Rows[0]["武力"]) == old, "整本预检失败留下部分草稿");
            }
        }
        finally { Directory.Delete(root, true); }
    }
    private static void AssertFields(string path, string table, Func<string, bool> allowed, int? count)
    {
        using var package = SpreadsheetDocument.Open(path, false);
        var part = package.WorkbookPart!; var sheet = Find(part, table);
        var keys = ((WorksheetPart)part.GetPartById(sheet.Id!)).Worksheet.GetFirstChild<SheetData>()!.Elements<Row>().First().Elements<Cell>().Select(c => c.InnerText).ToArray();
        TestSupport.Assert(keys.All(allowed) && (count == null || keys.Length == count), $"{table} 工作表泄露页外字段");
    }
    private static Sheet Find(WorkbookPart part, string key)
    {
        // Resolve the manifest's stable key, independently of user-visible labels.
        var meta = part.Workbook.Sheets!.Elements<Sheet>().Single(s => s.Name == "_DataManager");
        var json = string.Concat(((WorksheetPart)part.GetPartById(meta.Id!)).Worksheet.Descendants<Text>().Select(t => t.Text));
        using var document = System.Text.Json.JsonDocument.Parse(json);
        var id = document.RootElement.GetProperty("Datasets").EnumerateArray().Single(d => d.GetProperty("Key").GetString() == key).GetProperty("SheetId").GetUInt32();
        return part.Workbook.Sheets.Elements<Sheet>().Single(s => s.SheetId?.Value == id);
    }
    private static void Edit(string path, string table, string key, uint row, string value, string? formula = null)
        => MutateSheet(path, table, (part, sheet) =>
        {
            var data = ((WorksheetPart)part.GetPartById(sheet.Id!)).Worksheet.GetFirstChild<SheetData>()!;
            var header = data.Elements<Row>().Single(r => r.RowIndex?.Value == 1).Elements<Cell>().Single(c => c.InnerText == key);
            var letters = new string(header.CellReference!.Value!.TakeWhile(char.IsLetter).ToArray());
            var cell = data.Elements<Row>().Single(r => r.RowIndex?.Value == row).Elements<Cell>().Single(c => c.CellReference == letters + row);
            cell.RemoveAllChildren(); cell.DataType = DocumentFormat.OpenXml.Spreadsheet.CellValues.InlineString;
            cell.InlineString = new InlineString(new Text(value)); if (formula != null) cell.CellFormula = new CellFormula(formula);
        });
    private static void MutateSheet(string path, string key, Action<WorkbookPart, Sheet> action)
    {
        using var package = SpreadsheetDocument.Open(path, true); var part = package.WorkbookPart!; action(part, Find(part, key));
        foreach (var sheet in part.WorksheetParts) sheet.Worksheet.Save(); part.Workbook.Save();
    }
    private static void Reject(Action action, string reason)
    {
        try { action(); }
        catch (InvalidDataException ex) { TestSupport.Assert(ex.Message.Contains(reason, StringComparison.Ordinal), $"错误未明确定位“{reason}”：{ex.Message}"); return; }
        throw new InvalidOperationException("导入应拒绝：" + reason);
    }
}
