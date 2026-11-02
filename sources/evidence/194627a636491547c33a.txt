using System.Buffers.Binary;
using System.Globalization;
using DataManager.Core.Models;
using DataManager.Core.Profiles;
using DataManager.Core.Editing;

namespace DataManager.Core.Appearance;

public static class AppearanceSyncUpdates
{
    public static IReadOnlyList<PersonAppearanceUpdate> CompareWorkspaces(ProjectWorkspace before, ProjectWorkspace after)
    {
        var updates = new List<PersonAppearanceUpdate>();
        foreach (var key in new[] { "person-r-assign", "person-s-assign" })
        {
            if (!before.Documents.TryGetValue(key, out var oldDocument) || !after.Documents.TryGetValue(key, out var newDocument)) continue;
            var field = key == "person-r-assign" ? "R形象ID" : "S形象ID";
            var oldValues = oldDocument.Data.Rows.Cast<System.Data.DataRow>().ToDictionary(
                row => Convert.ToInt32(row["ID"], CultureInfo.InvariantCulture),
                row => Convert.ToUInt16(row[field], CultureInfo.InvariantCulture));
            foreach (System.Data.DataRow row in newDocument.Data.Rows)
            {
                var id = Convert.ToInt32(row["ID"], CultureInfo.InvariantCulture);
                var value = Convert.ToUInt16(row[field], CultureInfo.InvariantCulture);
                if (oldValues.TryGetValue(id, out var previous) && previous != value)
                    updates.Add(key == "person-r-assign" ? new(id, RId: value) : new(id, SId: value));
            }
        }
        return Merge(updates);
    }

    public static IReadOnlyList<PersonAppearanceUpdate> FromChanges(IEnumerable<TableCellChange> changes)
        => Merge(changes.Where(change => change.Table.Key is "person-r-assign" or "person-s-assign")
            .Select(change => change.Table.Key == "person-r-assign"
                ? new PersonAppearanceUpdate(change.Id, RId: Convert.ToUInt16(change.NewValue, CultureInfo.InvariantCulture))
                : new PersonAppearanceUpdate(change.Id, SId: Convert.ToUInt16(change.NewValue, CultureInfo.InvariantCulture))));

    public static IReadOnlyList<PersonAppearanceUpdate> CompareExecutables(byte[] before, byte[] after, string profileId)
    {
        var oldLayout = SaveAppearanceLayoutProbe.Inspect(before, profileId);
        var newLayout = SaveAppearanceLayoutProbe.Inspect(after, profileId);
        if (!oldLayout.Verified || !newLayout.Verified) return [];
        var updates = new List<PersonAppearanceUpdate>();
        for (var id = 0; id < 1024; id++)
        {
            var oldR = Read(before, oldLayout.RExecutableOffset, id);
            var oldS = Read(before, oldLayout.SExecutableOffset, id);
            var newR = Read(after, newLayout.RExecutableOffset, id);
            var newS = Read(after, newLayout.SExecutableOffset, id);
            if (oldR != newR || oldS != newS)
                updates.Add(new(id, oldR != newR ? newR : null, oldS != newS ? newS : null));
        }
        return updates;
    }

    public static IReadOnlyList<PersonAppearanceUpdate> Merge(IEnumerable<PersonAppearanceUpdate> updates)
    {
        var merged = new Dictionary<int, PersonAppearanceUpdate>();
        foreach (var update in updates)
        {
            if (update.PersonId is < 0 or >= 1024) throw new InvalidDataException("同步人物 ID 必须在 0..1023 内。");
            if (update.RId == null && update.SId == null) continue;
            if (!merged.TryGetValue(update.PersonId, out var previous)) merged[update.PersonId] = update;
            else
            {
                if (previous.RId.HasValue && update.RId.HasValue && previous.RId != update.RId ||
                    previous.SId.HasValue && update.SId.HasValue && previous.SId != update.SId)
                    throw new InvalidDataException($"人物 {update.PersonId} 的形象同步提出了不同的目标值。");
                merged[update.PersonId] = new(update.PersonId, update.RId ?? previous.RId, update.SId ?? previous.SId);
            }
        }
        return merged.Values.OrderBy(update => update.PersonId).ToArray();
    }

    private static ushort Read(byte[] executable, int offset, int id)
        => BinaryPrimitives.ReadUInt16LittleEndian(executable.AsSpan(checked(offset + id * 2), 2));
}
