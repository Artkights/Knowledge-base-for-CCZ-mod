using System.Data;
using System.Globalization;
using System.Text.RegularExpressions;
using DataManager.Core.Binary;
using DataManager.Core.Csv;
using DataManager.Core.Domain;
using DataManager.Core.Editing;
using DataManager.Core.Models;

namespace DataManager.Core.Workbooks;

/// <summary>The permission boundary belongs to the program, never to an imported manifest.</summary>
internal sealed partial class PageDatasetRegistry(ProjectWorkspace workspace)
{
    internal const string AccessoryKey = "native-accessory-groups";
    private readonly RecordCodecRegistry _codecs = new();
    internal IReadOnlyList<WorkbookDataset> Build(BusinessPageKind kind)
    {
        if (kind == BusinessPageKind.PhysicalTables) throw new InvalidOperationException("物理表使用兼容 CSV；工作簿按业务页交换。");
        var result = new List<WorkbookDataset>();
        foreach (var key in new BusinessDataService(workspace).GetAvailableTableKeys(kind))
        {
            if (!workspace.Documents.TryGetValue(key, out var document)) continue;
            var fields = document.Definition.Fields.Where(f => f.Size > 0 && Allowed(kind, key, f.Name)).ToArray();
            if (fields.Length == 0) continue;
            var columns = new[] { new WorkbookColumn("ID", "编号") }.Concat(fields.Select(field =>
            {
                var editable = field.Policy == FieldPolicy.Editable && document.Definition.Capability == TableCapability.Editable &&
                    document.Data.Columns.Contains(field.Name) && !document.Data.Columns[field.Name]!.ReadOnly;
                if (kind == BusinessPageKind.DetailedJobs && key == "strategies" && !LearningField().IsMatch(field.Name)) editable = false;
                var label = key == "detailed-job-growth" && ItemTypeService.EquipmentColumns.Contains(field.Name)
                    ? new EquipmentTypeCatalogService().GetPermissionDisplayName(workspace, field.Name) : field.ExportName;
                if (key == EquipmentTypeCatalogService.DisplayTableKey && field.Name == "显示值") label = "显示（0=隐藏，1=显示）";
                return new WorkbookColumn(field.Name, label, editable, field.Kind is FieldKind.UInt8 or FieldKind.UInt16 or FieldKind.UInt32,
                    field.Minimum, key == EquipmentTypeCatalogService.DisplayTableKey ? 1 : field.Maximum);
            })).ToArray();
            var rows = document.Data.Rows.Cast<DataRow>().Select((row, rowIndex) =>
            {
                var id = Text(row["ID"]);
                return new WorkbookRow(id, new[] { id }.Concat(fields.Select(field => GetValue(document, rowIndex, field))).ToArray());
            }).ToArray();
            result.Add(new(key, CsvDisplayNameRegistry.GetTableDisplayName(document.Definition), columns, rows));
        }
        if (kind == BusinessPageKind.JobSeries)
        {
            var source = new AccessoryJobGroupService().Read(workspace);
            if (source.Groups.Count > 0 && !source.Diagnostics.Any(d => d.StartsWith("错误：", StringComparison.Ordinal)))
            {
                var groups = AccessoryGroupDraftService.For(workspace).Snapshot();
                result.Add(new(AccessoryKey, "辅助装备分组", [new("ID", "分组编号"), new("Members", "兵种系编号（逗号分隔）", true)],
                    groups.Select((g, i) => new WorkbookRow(Text(i), [Text(i), string.Join(',', g)])).ToArray()));
            }
        }
        return result;
    }

    private static bool Allowed(BusinessPageKind page, string key, string field) => (page, key) switch
    {
        (BusinessPageKind.Items, "detailed-job-growth") => ItemTypeService.EquipmentColumns.Contains(field),
        (BusinessPageKind.DetailedJobs, "strategies") => field is "名称" or "策略名称" || LearningField().IsMatch(field),
        _ => true
    };
    [GeneratedRegex(@"^兵种\d+学习等级$")]
    private static partial Regex LearningField();

    private string GetValue(TableDocument document, int row, TableFieldDefinition field)
    {
        var value = document.Data.Columns.Contains(field.Name) ? document.Data.Rows[row][field.Name] :
            _codecs.Get(document.Definition.RecordCodecKey).Decode(document.OriginalFileBytes.AsSpan(
                checked((int)(document.Definition.DataOffset + (long)row * document.Definition.RowSize)), document.Definition.RowSize), field);
        if (document.Definition.Key == EquipmentTypeCatalogService.DisplayTableKey && field.Name == "显示值")
            return Convert.ToInt32(value, CultureInfo.InvariantCulture) == EquipmentTypeCatalogService.HiddenValue ? "0" : "1";
        return Text(value);
    }
    internal PhysicalLookup CreatePhysicalLookup() => new(workspace);

    // A lookup lives for one preview/apply operation only. Reusing it between operations could hide
    // a changed ID or document after a confirmation dialog or project reload.
    internal sealed class PhysicalLookup(ProjectWorkspace workspace)
    {
        private readonly Dictionary<string, (TableDocument Document, Dictionary<string, int> Rows,
            Dictionary<string, TableFieldDefinition> Fields)> _tables = new(StringComparer.Ordinal);

        internal TableFieldDefinition Resolve(WorkbookProposal proposal, out TableDocument document, out int row)
        {
            if (!_tables.TryGetValue(proposal.Dataset, out var table))
            {
                document = workspace.GetDocument(proposal.Dataset);
                var rows = new Dictionary<string, int>(document.Data.Rows.Count, StringComparer.Ordinal);
                var idColumn = document.Data.Columns["ID"]!;
                for (var index = 0; index < document.Data.Rows.Count; index++)
                    rows.TryAdd(Text(document.Data.Rows[index][idColumn]), index);
                table = (document, rows, document.Definition.Fields.ToDictionary(f => f.Name, StringComparer.Ordinal));
                _tables.Add(proposal.Dataset, table);
            }
            document = table.Document;
            if (!table.Rows.TryGetValue(proposal.Id, out row)) throw new InvalidDataException($"ID={proposal.Id} 不存在。");
            if (!table.Fields.TryGetValue(proposal.Field, out var field)) throw new InvalidDataException($"字段“{proposal.Field}”不存在。");
            return field;
        }
    }

    internal object ConvertPhysical(WorkbookProposal proposal, PhysicalLookup lookup, out TableDocument document, out int row)
    {
        var field = lookup.Resolve(proposal, out document, out row);
        if (proposal.Dataset == EquipmentTypeCatalogService.DisplayTableKey)
        {
            if (proposal.After is not ("0" or "1")) throw new InvalidDataException("显示只能为 0（隐藏）或 1（显示）。");
            return EquipmentTypeCatalogService.DisplayValue(row, proposal.After == "1");
        }
        return field.Kind switch
        {
            FieldKind.UInt8 or FieldKind.UInt16 => int.Parse(proposal.After, NumberStyles.Integer, CultureInfo.InvariantCulture),
            FieldKind.UInt32 => long.Parse(proposal.After, NumberStyles.Integer, CultureInfo.InvariantCulture),
            _ => proposal.After
        };
    }
    internal static string Text(object? value) => Convert.ToString(value, CultureInfo.InvariantCulture) ?? "";
}
