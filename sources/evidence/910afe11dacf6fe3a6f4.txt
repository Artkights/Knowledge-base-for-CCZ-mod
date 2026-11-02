using System.Text;
using System.Text.Json;
using DataManager.Core.Domain;
using DataManager.Core.Editing;
using DataManager.Core.Models;
using DataManager.Core.Profiles;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;

namespace DataManager.Core.Workbooks;

public sealed class PageWorkbookService(ProjectWorkspace workspace)
{
    private readonly record struct RowAddresses(string[] Columns, uint Row)
    {
        internal string this[int index] => Columns[index] + Row.ToString(System.Globalization.CultureInfo.InvariantCulture);
    }
    private readonly PageDatasetRegistry _registry = new(workspace);
    private string Identity => $"{Path.GetFullPath(workspace.RootPath)}|{workspace.ActiveProfile.ProfileId}|{workspace.ActiveProfile.VariantId}|{workspace.ActiveProfile.LayoutRevision}";

    public void Export(BusinessPageKind kind, string path)
    {
        var datasets = _registry.Build(kind);
        if (datasets.Count == 0) throw new InvalidDataException("当前业务页没有可导出的数据集。");
        var manifest = new WorkbookManifest(WorkbookPackage.Schema, workspace.ActiveProfile.ProfileId,
            workspace.ActiveProfile.VariantId, workspace.ActiveProfile.LayoutRevision, kind.ToString(),
            datasets.Select((d, i) => new WorkbookSheetRegistration(d.Key, (uint)i * 2 + 1, (uint)i * 2 + 2)).ToArray());
        var fullPath = Path.GetFullPath(path); var temporary = fullPath + "." + Guid.NewGuid().ToString("N") + ".tmp";
        try { WorkbookPackage.Write(temporary, manifest, datasets); File.Move(temporary, fullPath, true); }
        finally { if (File.Exists(temporary)) File.Delete(temporary); }
    }

    public PageWorkbookImportPreview PreviewImport(BusinessPageKind kind, string path)
    {
        try { return ReadPreview(kind, path); }
        catch (Exception ex) when (ex is InvalidDataException or FormatException or OverflowException or ArgumentException or InvalidOperationException or System.Xml.XmlException)
        { throw new InvalidDataException($"文件 {Path.GetFileName(path)}：{ex.Message}", ex); }
    }

    private PageWorkbookImportPreview ReadPreview(BusinessPageKind kind, string path)
    {
        using var package = SpreadsheetDocument.Open(path, false);
        var part = package.WorkbookPart ?? throw new InvalidDataException("缺少工作簿。");
        var sheets = part.Workbook.Sheets?.Elements<Sheet>().ToArray() ?? [];
        if (sheets.Any(s => s.SheetId == null) || sheets.GroupBy(s => s.SheetId!.Value).Any(g => g.Count() != 1))
            throw new InvalidDataException("工作表标识缺失或重复。");
        var shared = part.SharedStringTablePart?.SharedStringTable?.Elements<SharedStringItem>().Select(s => s.InnerText).ToArray() ?? [];
        var meta = sheets.SingleOrDefault(s => s.Name == WorkbookPackage.MetadataName) ?? throw new InvalidDataException("缺少隐藏元数据页，不能定位工作簿来源。");
        var json = new StringBuilder();
        foreach (var row in WorkbookPackage.ReadRows(Worksheet(meta), shared))
        {
            if (row.Cells.Any(c => c.Key != 0 && c.Value.Length > 0)) throw new InvalidDataException("工作簿元数据包含未知内容。");
            json.Append(row.Cells.GetValueOrDefault(0, ""));
            if (json.Length > 4_000_000) throw new InvalidDataException("工作簿元数据过大。");
        }
        WorkbookManifest manifest;
        try { manifest = JsonSerializer.Deserialize<WorkbookManifest>(json.ToString()) ?? throw new JsonException(); }
        catch (JsonException ex) { throw new InvalidDataException("工作簿元数据损坏。", ex); }
        if (manifest.Schema != WorkbookPackage.Schema) throw new InvalidDataException($"不支持工作簿 schema：{manifest.Schema}");
        if (manifest.Profile != workspace.ActiveProfile.ProfileId || manifest.Variant != workspace.ActiveProfile.VariantId)
            throw new InvalidDataException("Profile / Variant 与当前项目不符；跨基底请使用一键迁移。");
        if (manifest.Page != kind.ToString()) throw new InvalidDataException("工作簿不属于当前业务页。");
        if (!LayoutRevisionCompatibility.IsCompatible(workspace.RootPath, manifest.Profile, manifest.Variant,
            manifest.Layout, workspace.ActiveProfile.LayoutRevision)) throw new InvalidDataException("布局修订不兼容；请重新导出或使用一键迁移。");
        var current = _registry.Build(kind).ToDictionary(d => d.Key, StringComparer.Ordinal);
        if (manifest.Datasets == null || manifest.Datasets.Any(d => d == null) ||
            manifest.Datasets.GroupBy(d => d.Key).Any(g => g.Count() != 1) ||
            !manifest.Datasets.Select(d => d.Key).ToHashSet(StringComparer.Ordinal).SetEquals(current.Keys))
            throw new InvalidDataException("已登记的数据集缺失、重复或不属于当前业务页。");
        var referenced = manifest.Datasets.SelectMany(d => new[] { d.SheetId, d.BaselineSheetId }).ToArray();
        if (referenced.Distinct().Count() != referenced.Length || referenced.Contains(meta.SheetId!.Value))
            throw new InvalidDataException("工作表与基线的标识重复。");
        var proposals = new List<WorkbookProposal>(); var changes = new List<WorkbookCellChange>();
        var physicalLookup = _registry.CreatePhysicalLookup();
        foreach (var registration in manifest.Datasets)
        {
            var definition = current[registration.Key];
            var sheet = sheets.SingleOrDefault(s => s.SheetId!.Value == registration.SheetId)
                ?? throw new InvalidDataException($"缺少已登记工作表：{definition.Label}。");
            var baselineSheet = sheets.SingleOrDefault(s => s.SheetId!.Value == registration.BaselineSheetId)
                ?? throw new InvalidDataException($"缺少基线：{definition.Label}。");
            var baseline = new Dictionary<string, string[]>(StringComparer.Ordinal);
            var expectedRows = definition.Rows.ToDictionary(r => r.Id, StringComparer.Ordinal);
            ReadDataset(baselineSheet, definition, (id, values, _) =>
            {
                if (!baseline.TryAdd(id, values)) throw new InvalidDataException($"{definition.Label} 基线重复 ID={id}。");
            });
            if (!baseline.Keys.ToHashSet(StringComparer.Ordinal).SetEquals(expectedRows.Keys))
                throw new InvalidDataException($"{definition.Label} 基线 ID 不完整或与当前数据集不符。");
            var seen = new HashSet<string>(StringComparer.Ordinal);
            ReadDataset(sheet, definition, (id, values, addresses) =>
            {
                if (!seen.Add(id)) throw new InvalidDataException($"工作表 {sheet.Name} 单元格 {addresses[0]}：重复 ID={id}。");
                if (!expectedRows.TryGetValue(id, out var currentRow)) throw new InvalidDataException($"工作表 {sheet.Name} 单元格 {addresses[0]}：新增 ID={id} 不存在。");
                var original = baseline[id];
                for (var c = 1; c < definition.Columns.Length; c++)
                {
                    var column = definition.Columns[c];
                    if (Equal(values[c], original[c], column.Numeric)) continue;
                    var context = $"工作表 {sheet.Name} / 单元格 {addresses[c]} / ID={id} / 字段“{column.Label}”";
                    if (!column.Editable) throw new InvalidDataException($"{context}：只读字段被修改（实际值“{values[c]}”）。");
                    if (!Equal(currentRow.Values[c], original[c], column.Numeric) && !Equal(currentRow.Values[c], values[c], column.Numeric))
                        throw new InvalidDataException($"{context}：与当前草稿冲突。导出时“{original[c]}”，当前“{currentRow.Values[c]}”，文件“{values[c]}”。");
                    if (Equal(currentRow.Values[c], values[c], column.Numeric)) continue;
                    var proposal = new WorkbookProposal(definition.Key, id, column.Key, currentRow.Values[c], values[c]);
                    try { ValidatePhysical(proposal, physicalLookup, validateEquipment: false); }
                    catch (Exception ex) when (ex is ArgumentException or InvalidDataException or FormatException or OverflowException or InvalidOperationException)
                    { throw new InvalidDataException($"{context}：实际值“{values[c]}”；{ex.Message}", ex); }
                    proposals.Add(proposal);
                    changes.Add(new(sheet.Name?.Value ?? definition.Label, addresses[c], id, column.Label, currentRow.Values[c], values[c]));
                }
            });
        }
        var pendingPhysical = PhysicalEdits(proposals, physicalLookup);
        for (var index = 0; index < proposals.Count; index++)
        {
            var proposal = proposals[index];
            if (proposal.Dataset != "persons" || !PersonEquipmentService.CategoryForField(proposal.Field).HasValue) continue;
            try { ValidatePhysical(proposal, physicalLookup, pendingPhysical); }
            catch (Exception ex) when (ex is ArgumentException or InvalidDataException or FormatException or OverflowException or InvalidOperationException)
            {
                var change = changes[index];
                throw new InvalidDataException($"工作表 {change.Sheet} / 单元格 {change.Cell} / ID={proposal.Id} / 字段“{proposal.Field}”：实际值“{proposal.After}”；{ex.Message}", ex);
            }
        }
        try { ValidateNative(proposals); }
        catch (Exception ex) when (ex is InvalidDataException or InvalidOperationException or FormatException or ArgumentException or OverflowException)
        {
            var native = changes.Where(c => proposals.Any(p => p.Id == c.Id && p.After == c.NewValue && p.Dataset.StartsWith("native-", StringComparison.Ordinal))).FirstOrDefault();
            throw new InvalidDataException($"{(native == null ? "原生数据集" : $"工作表 {native.Sheet} / 单元格 {native.Cell} / ID={native.Id} / 字段“{native.Field}”")}：{ex.Message}", ex);
        }
        return new() { Changes = changes.AsReadOnly(), ProjectIdentity = Identity, Page = kind, Proposals = proposals.AsReadOnly() };

        WorksheetPart Worksheet(Sheet sheet)
            => sheet.Id != null && part.GetPartById(sheet.Id!) is WorksheetPart worksheet ? worksheet : throw new InvalidDataException($"工作表 {sheet.Name} 数据关系损坏。");
        void ReadDataset(Sheet sheet, WorkbookDataset definition, Action<string, string[], RowAddresses> action)
        {
            Dictionary<int, int>? mapping = null; string[]? addressColumns = null; var headerSeen = false;
            foreach (var row in WorkbookPackage.ReadRows(Worksheet(sheet), shared))
            {
                if (row.Index == 1)
                {
                    if (mapping != null) throw new InvalidDataException($"工作表 {sheet.Name} 稳定字段行重复。");
                    mapping = new(); var seenKeys = new HashSet<string>(StringComparer.Ordinal);
                    foreach (var cell in row.Cells.Where(c => c.Value.Length > 0))
                    {
                        var index = Array.FindIndex(definition.Columns, c => c.Key == cell.Value);
                        if (index < 0 || !seenKeys.Add(cell.Value)) throw new InvalidDataException($"工作表 {sheet.Name} / 单元格 {WorkbookPackage.ColumnName(cell.Key)}1：未知或重复字段“{cell.Value}”。");
                        mapping.Add(cell.Key, index);
                    }
                    if (mapping.Count != definition.Columns.Length) throw new InvalidDataException($"工作表 {sheet.Name} 缺少已登记字段。");
                    addressColumns = new string[definition.Columns.Length];
                    foreach (var map in mapping) addressColumns[map.Value] = WorkbookPackage.ColumnName(map.Key);
                    continue;
                }
                if (row.Index == 2) { if (headerSeen) throw new InvalidDataException($"工作表 {sheet.Name} 标题行重复。"); headerSeen = true; continue; }
                if (row.Index < 3 || row.Cells.All(c => c.Value.Length == 0)) continue;
                if (mapping == null) throw new InvalidDataException($"工作表 {sheet.Name} 缺少稳定字段行。");
                if (row.Cells.Any(c => c.Value.Length > 0 && !mapping.ContainsKey(c.Key)))
                    throw new InvalidDataException($"工作表 {sheet.Name} 第 {row.Index} 行包含未登记列。");
                var values = new string[definition.Columns.Length]; var addresses = new RowAddresses(addressColumns!, row.Index);
                foreach (var map in mapping) values[map.Value] = row.Cells.GetValueOrDefault(map.Key, "");
                if (string.IsNullOrWhiteSpace(values[0])) throw new InvalidDataException($"工作表 {sheet.Name} / 单元格 {addresses[0]}：编号不能为空。");
                action(values[0], values, addresses);
            }
            if (mapping == null || !headerSeen) throw new InvalidDataException($"工作表 {sheet.Name} 表头不完整。");
        }
    }

    public int ApplyImport(PageWorkbookImportPreview preview)
    {
        ArgumentNullException.ThrowIfNull(preview);
        if (preview.ProjectIdentity != Identity) throw new InvalidDataException("项目已切换，导入预览已过期。");
        if (preview.ChangedCells == 0) return 0;
        var page = _registry.Build(preview.Page);
        // The preview is a proposal, not a lock. Recheck every edited cell after the confirmation dialog.
        var current = page.ToDictionary(d => d.Key, StringComparer.Ordinal);
        var currentRows = new Dictionary<string, Dictionary<string, WorkbookRow>>(StringComparer.Ordinal);
        var currentColumns = new Dictionary<string, Dictionary<string, int>>(StringComparer.Ordinal);
        var physicalLookup = _registry.CreatePhysicalLookup();
        var physical = PhysicalEdits(preview.Proposals, physicalLookup);
        foreach (var proposal in preview.Proposals)
        {
            if (!current.TryGetValue(proposal.Dataset, out var dataset)) throw new InvalidDataException("预览的数据集已不可用，请重新导入。");
            if (!currentRows.TryGetValue(proposal.Dataset, out var rows))
            {
                currentRows.Add(proposal.Dataset, rows = dataset.Rows.ToDictionary(r => r.Id, StringComparer.Ordinal));
                currentColumns.Add(proposal.Dataset, dataset.Columns.Select((column, index) => (column.Key, index))
                    .ToDictionary(c => c.Key, c => c.index, StringComparer.Ordinal));
            }
            if (!rows.TryGetValue(proposal.Id, out var row) || !currentColumns[proposal.Dataset].TryGetValue(proposal.Field, out var c) ||
                !dataset.Columns[c].Editable || row.Values[c] != proposal.Before)
                throw new InvalidDataException($"ID={proposal.Id} 字段“{proposal.Field}”在预览后已改变，请重新导入。");
            ValidatePhysical(proposal, physicalLookup, physical);
        }
        ValidateNative(preview.Proposals);
        using var group = workspace.Commands.BeginGroup("导入业务页工作簿");
        workspace.ApplyCompositeTransaction("导入工作簿物理字段", physical);
        var groups = GroupChanges(preview.Proposals);
        if (groups != null) AccessoryGroupDraftService.For(workspace).Apply(groups);
        group.Complete();
        return preview.ChangedCells;
    }

    private CompositeCellEdit[] PhysicalEdits(IReadOnlyList<WorkbookProposal> proposals, PageDatasetRegistry.PhysicalLookup lookup)
        => proposals.Where(proposal => !proposal.Dataset.StartsWith("native-", StringComparison.Ordinal)).Select(proposal =>
        {
            var value = _registry.ConvertPhysical(proposal, lookup, out var document, out var row);
            return new CompositeCellEdit(document.Definition.Key, row, proposal.Field, value);
        }).ToArray();

    private void ValidatePhysical(WorkbookProposal proposal, PageDatasetRegistry.PhysicalLookup lookup,
        IReadOnlyList<CompositeCellEdit>? pendingEdits = null, bool validateEquipment = true)
    {
        if (proposal.Dataset.StartsWith("native-", StringComparison.Ordinal)) return;
        var value = _registry.ConvertPhysical(proposal, lookup, out var document, out var row);
        workspace.ValidateCellValue(document, row, proposal.Field, value, pendingEdits, validateEquipment);
    }
    private void ValidateNative(IReadOnlyList<WorkbookProposal> proposals)
    {
        var groups = GroupChanges(proposals);
        if (groups != null)
        {
            var preview = new AccessoryJobGroupService().Preview(workspace, groups);
            if (!preview.CanWrite) throw new InvalidDataException(string.Join(Environment.NewLine, preview.Diagnostics));
        }
    }
    private IReadOnlyList<IReadOnlyList<int>>? GroupChanges(IReadOnlyList<WorkbookProposal> proposals)
    {
        var changes = proposals.Where(p => p.Dataset == PageDatasetRegistry.AccessoryKey).ToArray();
        if (changes.Length == 0) return null;
        var groups = AccessoryGroupDraftService.For(workspace).Snapshot().Select(g => (IReadOnlyList<int>)g.ToArray()).ToArray();
        foreach (var change in changes)
        {
            var index = int.Parse(change.Id, System.Globalization.CultureInfo.InvariantCulture);
            if (index < 0 || index >= groups.Length) throw new InvalidDataException($"分组 {index} 不存在。");
            groups[index] = string.IsNullOrWhiteSpace(change.After) ? [] : change.After.Split(',').Select(s => int.Parse(s.Trim(), System.Globalization.CultureInfo.InvariantCulture)).ToArray();
        }
        return groups;
    }
    private static bool Equal(string a, string b, bool numeric)
        => a == b || numeric && long.TryParse(a, out var x) && long.TryParse(b, out var y) && x == y;
}
