using System.Data;
using System.Globalization;
using DataManager.Core.Binary;
using DataManager.Core.Editing;
using DataManager.Core.Models;

namespace DataManager.Core.Domain;

/// <summary>
/// Semantic access to the four independent extension tables. All changes use the
/// workspace's draft transaction and existing save/history path; reading never writes.
/// </summary>
public sealed class ExtendDataService
{
    private readonly ProjectWorkspace _workspace;
    private readonly RecordCodecRegistry _codecs = new();
    private EffectNamePoolProbeResult? _effectNames;
    private string? _nameSourceIdentity;

    public ExtendDataService(ProjectWorkspace workspace) => _workspace = workspace ?? throw new ArgumentNullException(nameof(workspace));
    public ProjectWorkspace Workspace => _workspace;

    public static string TableKey(ExtendDataCategory category) => category switch
    {
        ExtendDataCategory.Effects => "effect-archive",
        ExtendDataCategory.Growth => "effect-messages",
        ExtendDataCategory.Strategies => "strategy-study-extended",
        ExtendDataCategory.Forge => "forge",
        _ => throw new ArgumentOutOfRangeException(nameof(category))
    };

    public ExtendDataStatus GetStatus(ExtendDataCategory category)
    {
        var key = TableKey(category);
        if (_workspace.Documents.TryGetValue(key, out var document))
        {
            var candidates = ProjectFileLocator.GetCandidates(_workspace.RootPath, document.Definition.FileName);
            var conflict = candidates.Count > 1 ? $"存在多个同名文件，当前使用 {document.FilePath}；其余：{string.Join("、", candidates.Skip(1))}。" : string.Empty;
            return new(category, true, document.Data.Rows.Count, document.FilePath,
                $"{Path.GetFileName(document.FilePath)}：{document.Data.Rows.Count} 条完整记录。" +
                (document.Definition.IsWriteSupported ? string.Empty : "当前布局只读。") + conflict);
        }
        var definition = _workspace.Definitions.FirstOrDefault(table => table.Key == key);
        if (definition == null) return new(category, false, 0, string.Empty, "当前项目配置没有此拓展表。");
        var validation = new BinaryTableReader().Validate(_workspace.RootPath, definition);
        return new(category, false, 0, validation.Path,
            !validation.FileExists ? $"当前项目未提供 {definition.FileName}。" : $"{definition.FileName} 无法读取：{validation.Message}");
    }

    public TableDocument GetDocument(ExtendDataCategory category) => _workspace.GetDocument(TableKey(category));

    public IReadOnlyList<IdNameOption> GetEntityOptions(ExtendDataCategory category)
    {
        if (!GetStatus(category).Available) return [];
        var document = GetDocument(category);
        var effects = category == ExtendDataCategory.Growth ? GetEffectOptions().ToDictionary(option => option.Id, option => option.Name) : null;
        var persons = category is ExtendDataCategory.Effects or ExtendDataCategory.Strategies ? Lookup("persons") : null;
        return document.Data.Rows.Cast<DataRow>().Select(row =>
        {
            var id = Convert.ToInt32(row["ID"], CultureInfo.InvariantCulture);
            var name = category == ExtendDataCategory.Forge ? Convert.ToString(row["名称"], CultureInfo.InvariantCulture) ?? string.Empty
                : category == ExtendDataCategory.Growth ? effects!.GetValueOrDefault(id, "未知特技")
                : persons!.GetValueOrDefault(id, "未命名人物");
            if (category == ExtendDataCategory.Growth && id == 255) name = "空特技 / 保留记录（只读）";
            return new IdNameOption(id, SafeName(name, category == ExtendDataCategory.Forge ? "未命名配方" : "名称不可读取"));
        }).ToArray();
    }

    public EffectNamePoolProbeResult GetEffectNameSource()
    {
        var path = ProjectFileLocator.Resolve(_workspace.RootPath, "Ekd5.exe");
        var info = new FileInfo(path);
        var identity = $"{path}|{(info.Exists ? info.Length : -1)}|{(info.Exists ? info.LastWriteTimeUtc.Ticks : 0)}";
        if (_effectNames == null || identity != _nameSourceIdentity)
        {
            _effectNames = new EffectNamePoolProbe().Inspect(path);
            _nameSourceIdentity = identity;
        }
        return _effectNames;
    }

    public IReadOnlyList<IdNameOption> GetEffectOptions()
    {
        var source = GetEffectNameSource();
        return Enumerable.Range(0, 255).Select(id => new IdNameOption(id,
            SafeName(source.Names.GetValueOrDefault(id), source.Success ? "未命名特技" : "名称不可读取")))
            .Append(new IdNameOption(255, "无")).ToArray();
    }

    public IReadOnlyList<IdNameOption> GetStrategyOptions()
    {
        var names = Lookup("strategies");
        return Enumerable.Range(0, 255).Select(id => new IdNameOption(id, SafeName(names.GetValueOrDefault(id), "未命名策略")))
            .Append(new IdNameOption(255, "无")).ToArray();
    }

    public IReadOnlyList<IdNameOption> GetItemOptions()
    {
        var names = Lookup("items-low", "items-high", "items-extended");
        var result = Enumerable.Range(0, 512)
            .Select(id => new IdNameOption(id, id == 255 ? "无（空槽/保留）" :
                SafeName(names.GetValueOrDefault(id), id >= 256 ? "未命名扩展物品" : "未命名装备")))
            .ToList();
        return result;
    }

    public int ReadInt(ExtendDataCategory category, int entityId, string field)
        => checked((int)ReadLong(category, entityId, field));

    public long ReadLong(ExtendDataCategory category, int entityId, string field)
        => Convert.ToInt64(ReadValue(category, entityId, field), CultureInfo.InvariantCulture);

    public object? ReadValue(ExtendDataCategory category, int entityId, string field)
    {
        var (document, row) = Resolve(category, entityId);
        if (document.Data.Columns.Contains(field)) return document.Data.Rows[row][field];
        var definition = document.Definition.Fields.FirstOrDefault(candidate => candidate.Name == field)
            ?? throw new InvalidOperationException($"字段不存在：{field}");
        return BinaryValueCodec.Decode(GetRaw(category, entityId, draft: true), definition);
    }

    public byte[] GetRaw(ExtendDataCategory category, int entityId, bool draft = true)
    {
        var (document, row) = Resolve(category, entityId);
        var offset = checked((int)(document.Definition.DataOffset + (long)row * document.Definition.RowSize));
        var original = document.OriginalFileBytes.AsSpan(offset, document.Definition.RowSize);
        var output = original.ToArray();
        if (!draft) return output;
        var codec = _codecs.Get(document.Definition.RecordCodecKey);
        foreach (var field in document.Definition.Fields.Where(field => field.Policy == FieldPolicy.Editable && document.Data.Columns.Contains(field.Name)))
        {
            var value = document.Data.Rows[row][field.Name];
            if (Same(document.GetOriginal(row, field.Name), value)) continue;
            foreach (var patch in codec.EncodeChangedField(original, field, value)) patch.Bytes.CopyTo(output, patch.Offset);
        }
        return output;
    }

    public CompositeApplyResult ApplyEdits(ExtendDataCategory category, int entityId,
        IReadOnlyDictionary<string, object?> edits, string? description = null)
    {
        ArgumentNullException.ThrowIfNull(edits);
        var (document, row) = Resolve(category, entityId);
        if (category == ExtendDataCategory.Growth && entityId == 255 && edits.Count > 0)
            throw new InvalidOperationException("特技 ID 255 是空特技 / 保留记录，不参与成长，不能编辑。");
        foreach (var (field, value) in edits) _workspace.ValidateCellValue(document, row, field, value);
        if (category == ExtendDataCategory.Forge) ValidateForgeDraft(document, row, edits);
        return _workspace.ApplyCompositeTransaction(description ?? $"编辑拓展数据 {category} ID={entityId}",
            edits.Select(edit => new CompositeCellEdit(document.Definition.Key, row, edit.Key, edit.Value)).ToArray());
    }

    public CompositeApplyResult SetEffect(int entityId, int slot, int effectId, int value,
        int? experience = null, int? remainingTurns = null)
    {
        CheckSlot(slot, 256);
        var prefix = $"槽{slot}";
        var wasEmpty = ReadInt(ExtendDataCategory.Effects, entityId, prefix + "特效号") == 255;
        var edits = new Dictionary<string, object?> { [prefix + "特效号"] = effectId, [prefix + "特效值"] = effectId == 255 ? 0 : value };
        if (effectId == 255 || wasEmpty || experience.HasValue) edits[prefix + "经验"] = effectId == 255 ? 0 : experience ?? 0;
        if (effectId == 255 || wasEmpty || remainingTurns.HasValue) edits[prefix + "剩余回合"] = effectId == 255 ? 255 : remainingTurns ?? 255;
        return ApplyEdits(ExtendDataCategory.Effects, entityId, edits);
    }

    public CompositeApplyResult ClearEffect(int entityId, int slot) => SetEffect(entityId, slot, 255, 0);

    public CompositeApplyResult SetStrategy(int entityId, int slot, int strategyId, int? useCount = null)
    {
        CheckSlot(slot, 32);
        var prefix = $"策略{slot}";
        var wasEmpty = ReadInt(ExtendDataCategory.Strategies, entityId, prefix + "ID") == 255;
        var edits = new Dictionary<string, object?> { [prefix + "ID"] = strategyId };
        if (strategyId == 255 || wasEmpty || useCount.HasValue) edits[prefix + "次数"] = strategyId == 255 ? 0 : useCount ?? 255;
        return ApplyEdits(ExtendDataCategory.Strategies, entityId, edits);
    }

    public CompositeApplyResult ClearStrategy(int entityId, int slot) => SetStrategy(entityId, slot, 255);

    public IReadOnlyList<ExtendEffectSlot> GetEffects(int entityId)
    {
        var raw = GetRaw(ExtendDataCategory.Effects, entityId);
        return Enumerable.Range(0, 256).Select(slot => new ExtendEffectSlot(slot,
            raw[slot * 4], raw[slot * 4 + 1], raw[slot * 4 + 2], raw[slot * 4 + 3])).ToArray();
    }

    public IReadOnlyList<ExtendStrategySlot> GetStrategies(int entityId)
    {
        var raw = GetRaw(ExtendDataCategory.Strategies, entityId);
        return Enumerable.Range(0, 32).Select(slot => new ExtendStrategySlot(slot, raw[slot * 2], raw[slot * 2 + 1])).ToArray();
    }

    public IReadOnlyList<ExtendForgeSlot> GetForgeSlots(int entityId)
    {
        var raw = GetRaw(ExtendDataCategory.Forge, entityId);
        return Enumerable.Range(0, 8).Select(slot => new ExtendForgeSlot(slot,
            System.Buffers.Binary.BinaryPrimitives.ReadUInt16LittleEndian(raw.AsSpan(30 + slot * 3, 2)), raw[32 + slot * 3], slot < raw[58])).ToArray();
    }

    public ExtendGrowthPreview GetGrowth(int effectId)
    {
        var raw = GetRaw(ExtendDataCategory.Growth, effectId);
        return new(raw[0] != 0, raw[1], raw[2], raw[3], raw[4], raw[5], raw[6], raw[7]);
    }

    public CompositeApplyResult Compact(ExtendDataCategory category, int entityId)
    {
        var edits = new Dictionary<string, object?>();
        if (category == ExtendDataCategory.Effects)
        {
            var active = GetEffects(entityId).Where(slot => !slot.IsEmpty).ToArray();
            for (var slot = 0; slot < 256; slot++)
            {
                var value = slot < active.Length ? active[slot] : new ExtendEffectSlot(slot, 255, 0, 0, 255);
                edits[$"槽{slot}特效号"] = value.EffectId; edits[$"槽{slot}特效值"] = value.Value;
                edits[$"槽{slot}经验"] = value.Experience; edits[$"槽{slot}剩余回合"] = value.RemainingTurns;
            }
        }
        else if (category == ExtendDataCategory.Strategies)
        {
            var active = GetStrategies(entityId).Where(slot => !slot.IsEmpty).ToArray();
            for (var slot = 0; slot < 32; slot++)
            {
                var value = slot < active.Length ? active[slot] : new ExtendStrategySlot(slot, 255, 0);
                edits[$"策略{slot}ID"] = value.StrategyId; edits[$"策略{slot}次数"] = value.UseCount;
            }
        }
        else throw new InvalidOperationException("只有人物特技和策略学习支持整理槽位。");
        return ApplyEdits(category, entityId, edits, $"整理拓展数据 {category} ID={entityId} 的全部槽位");
    }

    public IReadOnlyList<string> GetDiagnostics()
        => Enum.GetValues<ExtendDataCategory>().Select(category => GetStatus(category).Message)
            .Append(GetEffectNameSource().Message).ToArray();

    public IReadOnlyList<string> GetDiagnostics(ExtendDataCategory category, int entityId)
    {
        var result = new List<string>();
        if (!GetStatus(category).Available) return [GetStatus(category).Message];
        if (category == ExtendDataCategory.Effects)
        {
            var slots = GetEffects(entityId);
            var firstEmpty = slots.FirstOrDefault(slot => slot.IsEmpty);
            result.Add(firstEmpty == null ? "全部 256 个特技槽已满，没有 ID 255 结束槽。" :
                $"第一个空特技槽位于第 {firstEmpty.Slot + 1} 槽（槽号 {firstEmpty.Slot}）；引擎在这里停止读取特技。");
            var gap = false;
            foreach (var slot in slots)
            {
                if (slot.IsEmpty) { gap = true; continue; }
                if (gap) { result.Add("空特技槽后仍有记录；引擎遇 ID 255 停止读取，后续特技不生效。可使用整理槽位保持顺序并前移。"); gap = false; }
                if (slot.RemainingTurns == 0) result.Add($"槽 {slot.Slot} 剩余回合为 0；引擎递减后会下溢为 255，不会直接删除。原值已保留。");
            }
        }
        else if (category == ExtendDataCategory.Strategies)
        {
            var slots = GetStrategies(entityId);
            var firstEmpty = slots.FirstOrDefault(slot => slot.IsEmpty);
            result.Add(firstEmpty == null ? "全部 32 个策略槽已满，没有 ID 255 空槽。" :
                $"第一个空策略槽位于第 {firstEmpty.Slot + 1} 槽（槽号 {firstEmpty.Slot}）；扣次与关末清理会在这里停止，查询仍可能扫描后续槽。");
            var empty = false;
            foreach (var slot in slots)
            {
                if (slot.IsEmpty) empty = true;
                else if (empty) { result.Add("空槽后的策略可能被查询到，但使用扣次与关末清理会跳过；可使用整理槽位保持顺序并前移。"); break; }
            }
        }
        else if (category == ExtendDataCategory.Growth)
        {
            if (entityId == 255) result.Add("ID 255 是空特技 / 保留记录，不参与成长，保持只读。");
            var enabled = ReadInt(category, entityId, "Enabled");
            if (enabled > 1) result.Add($"启用字节 {enabled} 在引擎中为启用；未主动切换前保留原值。");
        }
        else
        {
            var count = ReadInt(category, entityId, "材料项数");
            if (count > 8) result.Add($"材料项数 {count} 超出 0..8；原值保留，修改该项时必须修正。");
            foreach (var slot in GetForgeSlots(entityId))
            {
                if (!slot.IsEmpty && !slot.IsEquipment && !slot.IsConsumable) result.Add($"槽 {slot.Slot + 1} 的物品 ID {slot.ItemId} 未知；保留完整 UInt16 原值。");
                if (slot.IsMaterial && slot.IsConsumable && slot.RawAmount >= 128) result.Add($"材料槽 {slot.Slot + 1} 的消耗品数量含高位标记，上游可能越界；原值保留，新编辑数量须为 0..127。");
            }
        }
        return result.Distinct().ToArray();
    }

    /// <summary>
    /// Shared semantic guard for business edits, CSV and physical-table saves.
    /// Existing unusual bytes remain valid until a related value is changed.
    /// Pending values override the current draft without mutating it.
    /// </summary>
    public static void ValidateForgeDraft(TableDocument document, int rowIndex, IReadOnlyDictionary<string, object?>? edits = null)
    {
        if (document.Definition.Key != "forge") throw new ArgumentException("文档不是锻造表。", nameof(document));
        if (rowIndex < 0 || rowIndex >= document.Data.Rows.Count) throw new ArgumentOutOfRangeException(nameof(rowIndex));
        var offset = checked((int)(document.Definition.DataOffset + (long)rowIndex * document.Definition.RowSize));
        var original = document.OriginalFileBytes.AsSpan(offset, document.Definition.RowSize).ToArray();
        int Value(string field, int fallback)
        {
            var value = edits != null && edits.TryGetValue(field, out var pending) ? pending :
                document.Data.Columns.Contains(field) ? document.Data.Rows[rowIndex][field] : fallback;
            return checked((int)BinaryValueCodec.ParseInteger64(Convert.ToString(value, CultureInfo.InvariantCulture) ?? string.Empty, 0, ushort.MaxValue, field));
        }
        var count = Value("材料项数", original[58]);
        var countChanged = count != original[58];
        if (countChanged && count > 8) throw new InvalidDataException("材料项数必须在 0..8 范围内。");
        for (var slot = 0; slot < Math.Min(count, 8); slot++)
        {
            var idField = $"材料{slot + 1}ID"; var amountField = $"材料{slot + 1}数量";
            var oldId = System.Buffers.Binary.BinaryPrimitives.ReadUInt16LittleEndian(original.AsSpan(30 + slot * 3, 2));
            var oldAmount = original[32 + slot * 3];
            var id = Value(idField, oldId); var amount = Value(amountField, oldAmount);
            if (id is >= 256 and <= 510 && amount >= 128 &&
                (id != oldId || amount != oldAmount || countChanged && slot >= original[58]))
                throw new InvalidDataException($"材料槽 {slot + 1} 为消耗品；数量必须为 0..127，精确等级标记仅适用于装备材料。");
        }
    }

    private (TableDocument Document, int Row) Resolve(ExtendDataCategory category, int entityId)
    {
        var document = GetDocument(category);
        var row = entityId - document.Definition.BeginId;
        if (row < 0 || row >= document.Data.Rows.Count || Convert.ToInt32(document.Data.Rows[row]["ID"], CultureInfo.InvariantCulture) != entityId)
            throw new ArgumentOutOfRangeException(nameof(entityId), entityId, $"{document.Definition.DisplayName} 没有此 ID 的完整记录。");
        return (document, row);
    }

    private Dictionary<int, string> Lookup(params string[] keys)
    {
        var result = new Dictionary<int, string>();
        foreach (var key in keys)
        {
            if (!_workspace.Documents.TryGetValue(key, out var document)) continue;
            var column = document.Data.Columns.Contains("名称") ? "名称" : null;
            if (column == null) continue;
            foreach (DataRow row in document.Data.Rows)
                result.TryAdd(Convert.ToInt32(row["ID"], CultureInfo.InvariantCulture), Convert.ToString(row[column], CultureInfo.InvariantCulture) ?? string.Empty);
        }
        return result;
    }

    private static string SafeName(string? name, string fallback)
        => string.IsNullOrWhiteSpace(name) || EncodingService.HasPreservedInvalidBytes(name) || name.Any(char.IsControl) ? fallback : name;

    private static bool Same(object? left, object? right)
        => Convert.ToString(left == DBNull.Value ? null : left, CultureInfo.InvariantCulture) == Convert.ToString(right == DBNull.Value ? null : right, CultureInfo.InvariantCulture);

    private static void CheckSlot(int slot, int count)
    {
        if (slot < 0 || slot >= count) throw new ArgumentOutOfRangeException(nameof(slot), slot, $"槽位必须在 0..{count - 1} 范围内。");
    }
}
