using System.Buffers.Binary;
using System.Text.Json;
using DataManager.Core.Binary;
using DataManager.Core.Domain;
using DataManager.Core.Editing;
using DataManager.Core.Workbooks;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;

namespace DataManager.Tests;

internal static class WorkbookNativeTests
{
    public static void Run(string source)
    {
        var root = TestSupport.CreateCoreCopy(source);
        try
        {
            // Exercise optional native datasets on a profile with actual physical files.
            File.WriteAllBytes(Path.Combine(root, "Effect.e5"), Enumerable.Repeat((byte)255, 3 * 1024).ToArray());
            File.WriteAllBytes(Path.Combine(root, "Effectmsg.e5"), new byte[256 * 8]);
            File.WriteAllBytes(Path.Combine(root, "MeffStudy.e5"), Enumerable.Repeat((byte)255, 3 * 64).ToArray());
            File.WriteAllBytes(Path.Combine(root, "Forge.e5"), new byte[2 * 64]);
            var workspace = new ProjectWorkspace(); workspace.Open(root);
            var workbook = new PageWorkbookService(workspace);
            var path = Path.Combine(root, "原生.xlsx");
            var biography = workspace.GetDocument("person-biography");
            var textField = biography.Definition.Fields.First(f => f.Policy == DataManager.Core.Models.FieldPolicy.Editable).Name;
            workspace.ApplyCompositeTransaction("原生控制符与工作簿文字", [new("person-biography", 0, textField, "甲\r\n乙\n丙\r尾  \u0001\u001A _x0001_ _x0041_")]);
            workbook.Export(BusinessPageKind.Persons, path);
            TestSupport.Assert(workbook.PreviewImport(BusinessPageKind.Persons, path).ChangedCells == 0, "工作簿多行/控制字节/字面转义原样回导不为零");
            workspace.Commands.Undo();
            workbook.Export(BusinessPageKind.ExtendData, path);
            TestSupport.Assert(workbook.PreviewImport(BusinessPageKind.ExtendData, path).ChangedCells == 0, "拓展数据原样回导不为零");
            var growth = workspace.GetDocument("effect-messages");
            var changedField = growth.Definition.Fields.First(f => f.Policy == DataManager.Core.Models.FieldPolicy.Editable).Name;
            Modify(path, "effect-messages", changedField, "1");
            var preview = workbook.PreviewImport(BusinessPageKind.ExtendData, path); workbook.ApplyImport(preview);
            workspace.Commands.Undo(); TestSupport.Assert(!workspace.IsDirty, "拓展工作簿不能整体撤回");

            var groups = AccessoryGroupDraftService.For(workspace); var savedGroups = Signature(groups.Snapshot());
            workbook.Export(BusinessPageKind.JobSeries, path);
            var members = groups.Groups[0].Skip(1).ToArray();
            Modify(path, "native-accessory-groups", "Members", string.Join(',', members));
            var job = workspace.GetDocument("job-series"); var name = Convert.ToString(job.Data.Rows[0]["名称"]);
            Modify(path, "job-series", "名称", "测系");
            preview = workbook.PreviewImport(BusinessPageKind.JobSeries, path);
            TestSupport.Assert(preview.ChangedCells == 2 && !workspace.IsDirty, "原生分组预检产生草稿或漏字段");
            workbook.ApplyImport(preview);
            TestSupport.Assert(groups.HasPendingChanges && Convert.ToString(job.Data.Rows[0]["名称"]) == "测系", "分组与物理表未一并导入");
            workspace.Commands.Undo();
            TestSupport.Assert(Signature(groups.Snapshot()) == savedGroups && Convert.ToString(job.Data.Rows[0]["名称"]) == name && !workspace.IsDirty,
                "原生分组与物理表没有一次撤回");
            workspace.Commands.Redo();
            TestSupport.Assert(groups.HasPendingChanges && Convert.ToString(job.Data.Rows[0]["名称"]) == "测系", "原生分组不能整次重做");
            workspace.Commands.Undo();

            Console.WriteLine("WORKBOOK_NATIVE_TESTS_OK auxiliary+physical/extend/undo/redo");
        }
        finally { Directory.Delete(root, true); }
    }
    private static string Signature(IReadOnlyList<IReadOnlyList<int>> groups) => string.Join(';', groups.Select(g => string.Join(',', g)));
    private static void Modify(string path, string dataset, string field, string value)
    {
        using var file = SpreadsheetDocument.Open(path, true); var part = file.WorkbookPart!;
        var sheets = part.Workbook.Sheets!.Elements<Sheet>().ToArray();
        var meta = sheets.Single(s => s.Name == "_DataManager");
        var json = string.Concat(((WorksheetPart)part.GetPartById(meta.Id!)).Worksheet.Descendants<Text>().Select(t => t.Text));
        using var document = JsonDocument.Parse(json);
        var id = document.RootElement.GetProperty("Datasets").EnumerateArray().Single(d => d.GetProperty("Key").GetString() == dataset).GetProperty("SheetId").GetUInt32();
        var sheet = (WorksheetPart)part.GetPartById(sheets.Single(s => s.SheetId?.Value == id).Id!);
        var rows = sheet.Worksheet.GetFirstChild<SheetData>()!.Elements<Row>().ToArray();
        var cell = rows.Single(r => r.RowIndex?.Value == 1).Elements<Cell>().Single(c => c.InnerText == field);
        var column = new string(cell.CellReference!.Value!.TakeWhile(char.IsLetter).ToArray());
        cell = rows.Single(r => r.RowIndex?.Value == 3).Elements<Cell>().Single(c => c.CellReference == column + "3");
        cell.RemoveAllChildren(); cell.DataType = CellValues.InlineString; cell.InlineString = new InlineString(new Text(value)); sheet.Worksheet.Save();
    }
}
