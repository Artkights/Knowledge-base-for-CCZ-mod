using System.Globalization;
using System.Text.Json;
using System.Text;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;

namespace DataManager.Core.Workbooks;

/// <summary>Streaming package IO keeps large native tables out of an XML DOM.</summary>
internal static class WorkbookPackage
{
    internal const string Schema = "DataManagerWorkbook/1";
    internal const string MetadataName = "_DataManager";
    internal static void Write(string path, WorkbookManifest manifest, IReadOnlyList<WorkbookDataset> datasets)
    {
        using var package = SpreadsheetDocument.Create(path, SpreadsheetDocumentType.Workbook);
        var part = package.AddWorkbookPart(); part.Workbook = new Workbook();
        var styles = part.AddNewPart<WorkbookStylesPart>(); styles.Stylesheet = Styles(); styles.Stylesheet.Save();
        var sheets = part.Workbook.AppendChild(new Sheets());
        var names = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        for (var i = 0; i < datasets.Count; i++)
        {
            var dataset = datasets[i]; var registration = manifest.Datasets[i];
            AddSheet(dataset, registration.SheetId, UniqueName(dataset.Label, names), false);
            AddSheet(dataset, registration.BaselineSheetId, UniqueName($"_baseline{i + 1}", names), true);
        }
        var meta = part.AddNewPart<WorksheetPart>();
        using (var writer = OpenXmlWriter.Create(meta))
        {
            writer.WriteStartElement(new Worksheet()); writer.WriteStartElement(new SheetData());
            var json = JsonSerializer.Serialize(manifest); uint row = 1;
            for (var offset = 0; offset < json.Length; offset += 24000)
            {
                writer.WriteStartElement(new Row { RowIndex = row });
                WriteCell(writer, $"A{row}", json.Substring(offset, Math.Min(24000, json.Length - offset)), false, 0);
                writer.WriteEndElement(); row++;
            }
            writer.WriteEndElement(); writer.WriteEndElement();
        }
        sheets.Append(new Sheet { Id = part.GetIdOfPart(meta), SheetId = (uint)(datasets.Count * 2 + 1), Name = MetadataName, State = SheetStateValues.VeryHidden });
        part.Workbook.Save();

        void AddSheet(WorkbookDataset dataset, uint id, string name, bool baseline)
        {
            if (dataset.Columns.Length > 16384 || dataset.Rows.Length > 1048574) throw new InvalidDataException($"{dataset.Label} 超出 XLSX 行列上限。");
            var columnNames = Enumerable.Range(0, dataset.Columns.Length).Select(ColumnName).ToArray();
            var sheetPart = part.AddNewPart<WorksheetPart>();
            using (var writer = OpenXmlWriter.Create(sheetPart))
            {
                writer.WriteStartElement(new Worksheet());
                if (!baseline)
                {
                    writer.WriteElement(new SheetViews(new SheetView(new Pane { HorizontalSplit = 1, VerticalSplit = 2,
                        TopLeftCell = "B3", ActivePane = PaneValues.BottomRight, State = PaneStateValues.Frozen }) { WorkbookViewId = 0 }));
                    var widths = new Columns();
                    for (var column = 0; column < dataset.Columns.Length; column++)
                        widths.Append(new Column { Min = (uint)column + 1, Max = (uint)column + 1, Width = column == 0 ? 12 : dataset.Columns[column].Numeric ? 15 : 28, CustomWidth = true });
                    writer.WriteElement(widths);
                }
                writer.WriteStartElement(new SheetData());
                WriteRow(1, dataset.Columns.Select(c => c.Key).ToArray(), true);
                WriteRow(2, dataset.Columns.Select(c => c.Label).ToArray(), false);
                for (var row = 0; row < dataset.Rows.Length; row++) WriteRow((uint)row + 3, dataset.Rows[row].Values, false);
                writer.WriteEndElement();
                if (!baseline && dataset.Rows.Length > 0)
                {
                    writer.WriteElement(new AutoFilter { Reference = $"A2:{columnNames[^1]}{dataset.Rows.Length + 2}" });
                    var validations = new DataValidations();
                    for (var column = 1; column < dataset.Columns.Length; column++)
                    {
                        var definition = dataset.Columns[column];
                        if (!definition.Editable || !definition.Numeric) continue;
                        validations.Append(new DataValidation(new Formula1(definition.Minimum.ToString(CultureInfo.InvariantCulture)),
                            new Formula2(definition.Maximum.ToString(CultureInfo.InvariantCulture)))
                        { Type = DataValidationValues.Whole, Operator = DataValidationOperatorValues.Between, AllowBlank = false,
                            ShowErrorMessage = true, ErrorTitle = "输入超出范围", Error = $"请输入 {definition.Minimum} 到 {definition.Maximum} 的整数。",
                            SequenceOfReferences = new ListValue<StringValue> { InnerText = $"{columnNames[column]}3:{columnNames[column]}{dataset.Rows.Length + 2}" } });
                    }
                    if (validations.ChildElements.Count > 0) { validations.Count = (uint)validations.ChildElements.Count; writer.WriteElement(validations); }
                }
                writer.WriteEndElement();

                void WriteRow(uint number, string[] values, bool hidden)
                {
                    writer.WriteStartElement(new Row { RowIndex = number, Hidden = hidden });
                    var rowNumber = number.ToString(CultureInfo.InvariantCulture);
                    for (var column = 0; column < values.Length; column++)
                    {
                        var definition = dataset.Columns[column];
                        WriteCell(writer, columnNames[column] + rowNumber, values[column], number > 2 && definition.Numeric,
                            number <= 2 ? 3U : definition.Editable ? 2U : 1U);
                    }
                    writer.WriteEndElement();
                }
            }
            sheets.Append(new Sheet { Id = part.GetIdOfPart(sheetPart), SheetId = id, Name = name, State = baseline ? SheetStateValues.VeryHidden : SheetStateValues.Visible });
        }
    }
    private static void WriteCell(OpenXmlWriter writer, string reference, string text, bool numeric, uint style)
    {
        if (text.Length > 32767) throw new InvalidDataException($"单元格 {reference} 文本超过 Excel 的 32767 字符容量，未截断导出。");
        var cell = new Cell { CellReference = reference, StyleIndex = style };
        if (numeric && long.TryParse(text, NumberStyles.Integer, CultureInfo.InvariantCulture, out _))
        { cell.DataType = CellValues.Number; cell.CellValue = new CellValue(text); }
        else { cell.DataType = CellValues.InlineString; cell.InlineString = new InlineString(new Text(EncodeSpreadsheetText(text)) { Space = SpaceProcessingModeValues.Preserve }); }
        writer.WriteElement(cell);
    }
    internal static IEnumerable<(uint Index, Dictionary<int, string> Cells)> ReadRows(WorksheetPart part, IReadOnlyList<string> shared)
    {
        using var reader = OpenXmlReader.Create(part);
        uint fallback = 0;
        while (reader.Read())
        {
            if (!reader.IsStartElement || reader.ElementType != typeof(Row)) continue;
            var row = reader.LoadCurrentElement() as Row ?? throw new InvalidDataException("工作表行数据损坏。");
            var index = row.RowIndex?.Value ?? ++fallback; fallback = index;
            var values = new Dictionary<int, string>(); var next = 0;
            foreach (var cell in row.Elements<Cell>())
            {
                if (cell.CellFormula != null) throw new InvalidDataException($"单元格 {cell.CellReference} 含公式，请先粘贴为值再导入。");
                var column = cell.CellReference == null ? next : ColumnIndex(cell.CellReference!); next = column + 1;
                if (column is < 0 or >= 16384 || !values.TryAdd(column, Value(cell, shared)))
                    throw new InvalidDataException($"单元格 {cell.CellReference} 列号无效或重复。");
            }
            yield return (index, values);
        }
    }
    internal static string Value(Cell cell, IReadOnlyList<string> shared)
    {
        var value = cell.CellValue?.Text ?? "";
        if (cell.DataType?.Value == CellValues.InlineString) return DecodeSpreadsheetText(cell.InlineString?.InnerText ?? "");
        if (cell.DataType?.Value == CellValues.SharedString)
        {
            if (!int.TryParse(value, out var index) || index < 0 || index >= shared.Count) throw new InvalidDataException("共享文本索引无效。");
            return DecodeSpreadsheetText(shared[index]);
        }
        if (cell.DataType?.Value == CellValues.Error) throw new InvalidDataException($"单元格 {cell.CellReference} 为 Excel 错误值 {value}。");
        if (cell.DataType?.Value == CellValues.Boolean) return value == "1" ? "1" : "0";
        return cell.DataType?.Value == CellValues.String ? DecodeSpreadsheetText(value) : value;
    }
    // OOXML ST_Xstring escapes retain native control bytes and CR independently of XML newline normalization.
    // Literal escape-looking text must protect its underscore, and decoding must happen exactly once.
    internal static string EncodeSpreadsheetText(string value)
    {
        StringBuilder? output = null;
        for (var i = 0; i < value.Length; i++)
        {
            var c = value[i];
            var literalEscape = IsEscape(value, i);
            var control = c == '\r' || c < 32 && c is not ('\t' or '\n') || c is '\uFFFE' or '\uFFFF';
            if (!literalEscape && !control) { output?.Append(c); continue; }
            // Most game strings need no OOXML escaping. Return their existing string without copying it.
            output ??= new StringBuilder(value.Length + 6).Append(value, 0, i);
            if (literalEscape) output.Append("_x005F_");
            else output.Append("_x").Append(((int)c).ToString("X4", CultureInfo.InvariantCulture)).Append('_');
        }
        return output?.ToString() ?? value;
    }
    internal static string DecodeSpreadsheetText(string value)
    {
        var firstCandidate = value.IndexOf('_');
        if (firstCandidate < 0) return value;
        StringBuilder? output = null;
        for (var i = firstCandidate; i < value.Length; i++)
        {
            if (!IsEscape(value, i)) { output?.Append(value[i]); continue; }
            output ??= new StringBuilder(value.Length).Append(value, 0, i);
            output.Append((char)int.Parse(value.AsSpan(i + 2, 4), NumberStyles.HexNumber, CultureInfo.InvariantCulture));
            i += 6;
        }
        return output?.ToString() ?? value;
    }
    private static bool IsEscape(string value, int index)
        => value[index] == '_' && index + 6 < value.Length && value[index + 1] is 'x' or 'X' && value[index + 6] == '_' &&
            value.AsSpan(index + 2, 4).IndexOfAnyExcept("0123456789abcdefABCDEF") < 0;
    internal static string ColumnName(int index)
    { var result = ""; for (index++; index > 0; index = (index - 1) / 26) result = (char)('A' + (index - 1) % 26) + result; return result; }
    private static int ColumnIndex(string reference)
    { var value = 0; foreach (var c in reference.TakeWhile(char.IsLetter)) value = checked(value * 26 + char.ToUpperInvariant(c) - 'A' + 1); return value - 1; }
    private static string UniqueName(string name, HashSet<string> used)
    {
        name = string.Concat(name.Select(c => "[]:*?/\\".Contains(c) ? '_' : c)).Trim('\'');
        if (name.Length == 0) name = "数据"; name = name[..Math.Min(name.Length, 31)];
        var result = name; var suffix = 1;
        while (!used.Add(result)) { var tail = $"_{++suffix}"; result = name[..Math.Min(name.Length, 31 - tail.Length)] + tail; }
        return result;
    }
    private static Stylesheet Styles() => new(
        new Fonts(new Font(new FontSize { Val = 11 }, new FontName { Val = "Microsoft YaHei" })),
        new Fills(new Fill(new PatternFill { PatternType = PatternValues.None }), new Fill(new PatternFill { PatternType = PatternValues.Gray125 }),
            new Fill(new PatternFill(new ForegroundColor { Rgb = "FFECEFF3" }) { PatternType = PatternValues.Solid }),
            new Fill(new PatternFill(new ForegroundColor { Rgb = "FFDCE9F5" }) { PatternType = PatternValues.Solid })),
        new Borders(new Border()), new CellStyleFormats(new CellFormat()),
        new CellFormats(new CellFormat(), new CellFormat { FontId = 0, FillId = 2, ApplyFill = true }, new CellFormat { FontId = 0 },
            new CellFormat { FontId = 0, FillId = 3, ApplyFill = true }),
        new CellStyles(new CellStyle { Name = "Normal", FormatId = 0, BuiltinId = 0 }));
}
