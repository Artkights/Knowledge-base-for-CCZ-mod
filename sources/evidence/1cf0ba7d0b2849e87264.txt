using System.Data;
using System.Globalization;
using DataManager.Core.Editing;
using DataManager.Core.Models;

namespace DataManager.Core.Domain;

/// <summary>
/// Read-only cross-file view for one effect id: which persons carry it in Effect.e5
/// and what growth parameters Effectmsg.e5 stores for it. Writing stays in the
/// existing extension-data page so this service never mutates a draft.
/// </summary>
public sealed class EngineEffectReferenceService
{
    public const int NoEffect = 255;
    public const int MaximumSlots = 256;
    public const int MaximumEffectId = 254;
    public const int GrowthRowSize = 8;

    public IReadOnlyDictionary<int, EngineEffectReferenceSummary> Build(ProjectWorkspace workspace)
    {
        ArgumentNullException.ThrowIfNull(workspace);
        var assignments = ReadPersonAssignments(workspace);
        var growth = ReadGrowthSettings(workspace);
        var growthAvailable = workspace.Documents.ContainsKey("effect-messages");
        var result = new Dictionary<int, EngineEffectReferenceSummary>(MaximumEffectId + 1);
        for (var effectId = 0; effectId <= MaximumEffectId; effectId++)
        {
            result[effectId] = new EngineEffectReferenceSummary
            {
                PersonAssignments = assignments.GetValueOrDefault(effectId) ?? [],
                Growth = growth.GetValueOrDefault(effectId) ?? EngineEffectGrowthSettings.Missing(
                    growthAvailable ? "Effectmsg.e5 没有此特效的成长记录" : "当前项目未加载 Effectmsg.e5")
            };
        }
        return result;
    }

    public IReadOnlyDictionary<int, EngineEffectGrowthSettings> ReadGrowthSettings(ProjectWorkspace workspace)
    {
        ArgumentNullException.ThrowIfNull(workspace);
        return ReadGrowthSettingsCore(workspace);
    }

    public IReadOnlyDictionary<int, IReadOnlyList<EngineEffectPersonReference>> ReadPersonAssignments(
        ProjectWorkspace workspace)
    {
        ArgumentNullException.ThrowIfNull(workspace);
        return ReadPersonAssignmentsCore(workspace)
            .ToDictionary(pair => pair.Key, pair => (IReadOnlyList<EngineEffectPersonReference>)pair.Value);
    }

    private static Dictionary<int, EngineEffectGrowthSettings> ReadGrowthSettingsCore(ProjectWorkspace workspace)
    {
        var result = new Dictionary<int, EngineEffectGrowthSettings>();
        if (!workspace.Documents.TryGetValue("effect-messages", out var document)) return result;
        var table = document.Data;
        if (!table.Columns.Contains("ID")) return result;
        var fileName = Path.GetFileName(document.FilePath);
        var writable = document.Definition.IsWriteSupported;
        foreach (DataRow row in table.Rows)
        {
            var id = Convert.ToInt32(row["ID"], CultureInfo.InvariantCulture);
            if (id is < 0 or > MaximumEffectId) continue;
            result[id] = new EngineEffectGrowthSettings(
                true, fileName,
                ReadInt(row, "Enabled") is { } enabled && enabled != 0,
                ReadInt(row, "Param1") ?? 0,
                ReadInt(row, "Param2") ?? 0,
                ReadInt(row, "Param3") ?? 0,
                ReadInt(row, "Param4") ?? 0,
                ReadInt(row, "Param5") ?? 0,
                ReadInt(row, "Param6") ?? 0,
                ReadInt(row, "Param7") ?? 0,
                writable,
                $"{fileName} 行 {id}，+0x{id * GrowthRowSize:X}（{GrowthRowSize} 字节/特效）");
        }
        return result;
    }

    private static Dictionary<int, List<EngineEffectPersonReference>> ReadPersonAssignmentsCore(ProjectWorkspace workspace)
    {
        var result = new Dictionary<int, List<EngineEffectPersonReference>>();
        if (!workspace.Documents.TryGetValue("effect-archive", out var document)) return result;
        var table = document.Data;
        if (!table.Columns.Contains("ID")) return result;
        var names = ReadPersonNames(workspace);
        var effectColumns = new DataColumn?[MaximumSlots];
        var valueColumns = new DataColumn?[MaximumSlots];
        var experienceColumns = new DataColumn?[MaximumSlots];
        var turnColumns = new DataColumn?[MaximumSlots];
        for (var slot = 0; slot < MaximumSlots; slot++)
        {
            var prefix = $"槽{slot.ToString(CultureInfo.InvariantCulture)}";
            effectColumns[slot] = Column(table, prefix + "特效号");
            valueColumns[slot] = Column(table, prefix + "特效值");
            experienceColumns[slot] = Column(table, prefix + "经验");
            turnColumns[slot] = Column(table, prefix + "剩余回合");
        }
        foreach (DataRow row in table.Rows)
        {
            var personId = Convert.ToInt32(row["ID"], CultureInfo.InvariantCulture);
            var personName = names.GetValueOrDefault(personId, $"人物 {personId}");
            for (var slot = 0; slot < MaximumSlots; slot++)
            {
                if (effectColumns[slot] is not { } effectColumn) continue;
                var effectId = ReadInt(row, effectColumn);
                if (effectId is not { } id || id == NoEffect || id > MaximumEffectId) continue;
                if (!result.TryGetValue(id, out var list)) result[id] = list = [];
                list.Add(new EngineEffectPersonReference(personId, personName, slot,
                    ReadInt(row, valueColumns[slot]) ?? 0,
                    ReadInt(row, experienceColumns[slot]) ?? 0,
                    ReadInt(row, turnColumns[slot]) ?? 0));
            }
        }
        foreach (var list in result.Values)
            list.Sort((left, right) => left.PersonId != right.PersonId
                ? left.PersonId.CompareTo(right.PersonId)
                : left.Slot.CompareTo(right.Slot));
        return result;
    }

    private static Dictionary<int, string> ReadPersonNames(ProjectWorkspace workspace)
    {
        var result = new Dictionary<int, string>();
        if (!workspace.Documents.TryGetValue("persons", out var document)) return result;
        var table = document.Data;
        if (!table.Columns.Contains("ID") || !table.Columns.Contains("名称")) return result;
        foreach (DataRow row in table.Rows)
            result.TryAdd(Convert.ToInt32(row["ID"], CultureInfo.InvariantCulture),
                Convert.ToString(row["名称"], CultureInfo.InvariantCulture) ?? string.Empty);
        return result;
    }

    private static DataColumn? Column(DataTable table, string name)
        => table.Columns.Contains(name) ? table.Columns[name] : null;

    private static int? ReadInt(DataRow row, string name)
        => row.Table.Columns.Contains(name) ? ReadInt(row, row.Table.Columns[name]!) : null;

    private static int? ReadInt(DataRow row, DataColumn? column)
    {
        if (column == null || row.RowState == DataRowState.Deleted) return null;
        var value = row[column];
        return value == null || value == DBNull.Value
            ? null
            : Convert.ToInt32(value, CultureInfo.InvariantCulture);
    }
}
