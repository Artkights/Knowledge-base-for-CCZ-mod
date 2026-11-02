using DataManager.Core.Binary;
using DataManager.Core.Editing;
using DataManager.Core.Models;

namespace DataManager.Core.Scanner;

public sealed partial class EngineEffectAssignmentService
{
    public EngineEffectAssignmentPreview BuildPreview(ProjectWorkspace workspace, EngineEffectScanReport report,
        EngineEffectAssignmentDraft draft, bool ensureEquipmentFfGuard = false)
    {
        var errors = new List<string>();
        var impact = new List<string>();
        if (workspace.IsDirty) errors.Add("存在未保存的数据草稿，请先保存或撤销。");
        if (!draft.HasPendingChanges) errors.Add("没有待写入的分配修改。");
        var before = File.ReadAllBytes(report.ExePath);
        if (!HashService.Sha256(before).Equals(draft.Catalog.ExeSha256, StringComparison.OrdinalIgnoreCase) ||
            !report.ExeSha256.Equals(draft.Catalog.ExeSha256, StringComparison.OrdinalIgnoreCase))
            errors.Add("扫描基线已变化，请重新扫描后再分配。");
        var after = (byte[])before.Clone();
        var edits = new List<EngineEffectCallEdit>();
        foreach (var (key, target) in draft.ItemTargets)
        {
            var effect = draft.Catalog.Effects.FirstOrDefault(effect => effect.Key == key);
            if (effect == null || !effect.CanBindItem || target is < 0 or > 255)
            { errors.Add($"特效{key}没有完整的可写绑定点。"); continue; }
            impact.Add($"{effect.Name}：装备号 {string.Join('/', effect.ItemSelectors)} → {(target == 255 ? "255（卸下）" : target)}；" +
                "原归属宝物：" + Owners(draft.Catalog, effect.ItemSelectors) + "；新归属宝物：" + Owners(draft.Catalog, [target], draft.ItemSelectorTargets));
            if (effect.Kind != EngineEffectAssignmentKind.SharedLookup) continue;
            edits.AddRange(effect.BindingPoints.Select(call => new EngineEffectCallEdit
            {
                Identity = call.Identity, CallAddress = call.CallAddress, TableIndex = call.TableIndex, ItemEffectId = target
            }));
        }
        if (edits.Count > 0)
        {
            var callPreview = new EngineEffectWriteService().BuildPreview(workspace, report,
                new EngineEffectWriteRequest { EffectId = -1, CallEdits = edits, DeferEquipmentFfGuard = true });
            errors.AddRange(callPreview.Errors);
            var exe = callPreview.Candidates.FirstOrDefault(candidate =>
                Path.GetFullPath(candidate.FilePath).Equals(Path.GetFullPath(report.ExePath), StringComparison.OrdinalIgnoreCase));
            if (exe != null) after = (byte[])exe.AfterBytes.Clone();
        }
        var layout = ProbeJobLayout(EngineEffectBinaryImage.Read(before));
        foreach (var (key, slots) in draft.JobTargets)
        {
            var effect = draft.Catalog.Effects.FirstOrDefault(effect => effect.Key == key);
            if (!layout.Verified || effect?.PersonalEffectId is not { } effectId || !effect.CanBindJob || slots.Length != layout.SlotCount || effectId >= layout.RowCount)
            { errors.Add($"特效{key}没有经过验证的真实兵种分配槽。"); continue; }
            for (var index = 0; index < layout.SlotCount; index++)
            {
                var slot = slots[index];
                var original = effect.JobSlots[index];
                var expectedOffset = layout.GetJobIdOffset(effectId, index);
                var valueOffset = layout.GetJobValueOffset(effectId, index);
                if (slot.FileOffset != expectedOffset || slot.ValueFileOffset != valueOffset || slot.JobId is < 0 or > 255 || slot.Value is < 0 or > 255 ||
                    slot.JobId != original.JobId && slot.JobId is >= 80 and < 255)
                { errors.Add($"{effect.Name} 槽{index}的地址或值无效。"); continue; }
                if (before[checked((int)expectedOffset)] != original.JobId || before[checked((int)valueOffset)] != original.Value)
                { errors.Add($"{effect.Name} 槽{index}原字节已变化。"); continue; }
                after[checked((int)expectedOffset)] = (byte)slot.JobId;
                after[checked((int)valueOffset)] = (byte)slot.Value;
                if (slot.Value != original.Value && layout.SharedValue)
                    impact.Add($"{effect.Name}：本行人物/兵种共用N {original.Value} → {slot.Value}；人物原始槽：" +
                        string.Join("、", layout.ReadPersonIds(before, effectId)) + "（保留全部人物ID原字节）。");
                if (slot.JobId != original.JobId || slot.Value != original.Value)
                    impact.Add($"{effect.Name} 槽{index}：兵种 {original.JobId}/值{original.Value} → {slot.JobId}/值{slot.Value}；" +
                        $"{slot.MatchScope}；当前影响 {string.Join(',', slot.AffectedJobIds)}；" +
                        $"切换同族模式后可能影响 {string.Join(',', slot.PotentialAffectedJobIds)}。");
            }
        }
        var native = NativeEffectAdapter.Read(after);
        var hp = draft.ItemTargets.TryGetValue("native:hp", out var hpTarget) ? hpTarget : native.HpCurrentSelector;
        var mp = draft.ItemTargets.TryGetValue("native:mp", out var mpTarget) ? mpTarget : native.MpCurrentSelector;
        var nativeChanged = draft.ItemTargets.ContainsKey("native:hp") || draft.ItemTargets.ContainsKey("native:mp");
        var needsFf = ensureEquipmentFfGuard || edits.Any(edit => edit.ItemEffectId == 255);
        if (nativeChanged || needsFf)
        {
            if (!native.IsSupported) errors.Add("本引擎未通过原生适配/FF停用守卫校验，无法提交此次卸下或原生改绑。");
            else
            {
                try { after = NativeEffectAdapter.Build(after, checked((byte)hp), checked((byte)mp), true).After; }
                catch (InvalidDataException ex) { errors.Add("原生适配预览失败：" + ex.Message); }
            }
        }
        var candidates = new List<WorkspaceBinaryCandidate>();
        if (!before.AsSpan().SequenceEqual(after)) candidates.Add(new(report.ExePath, before, after, "特效分配"));
        var changedItems = draft.ItemValues.Keys.Concat(draft.ItemSelectorTargets.Keys).Concat(draft.SpecialItemIds).Distinct();
        foreach (var group in changedItems.GroupBy(id => draft.Catalog.Items.Single(item => item.Id == id).FilePath,
                     StringComparer.OrdinalIgnoreCase))
        {
            var itemBefore = File.ReadAllBytes(group.Key);
            var itemAfter = (byte[])itemBefore.Clone();
            foreach (var id in group)
            {
                var item = draft.Catalog.Items.Single(item => item.Id == id);
                if (draft.ItemValues.TryGetValue(id, out var value))
                {
                    if (item.ValueFileOffset < 0 || item.ValueFileOffset >= itemBefore.Length || item.Value is not { } oldValue ||
                        itemBefore[checked((int)item.ValueFileOffset)] != oldValue || value is < 0 or > 255)
                    { errors.Add($"宝物{id}真实值原字节或地址不符。"); continue; }
                    itemAfter[checked((int)item.ValueFileOffset)] = (byte)value;
                    impact.Add($"宝物 {id}：{item.Name} 的真实共享N {oldValue} → {value}；{item.ValueSource}。");
                }
                if (draft.ItemSelectorTargets.TryGetValue(id, out var selector))
                {
                    // 0x80..FD is allocated for special-type equipment; 26..66 are
                    // static numeric effect codes written directly to the selector.
                    if (item.SelectorFileOffset < 0 || itemBefore[checked((int)item.SelectorFileOffset)] != item.Selector ||
                        selector is < 0 or > 254)
                    { errors.Add($"宝物{id}实际selector字段原字节不符或候选号非法。"); continue; }
                    itemAfter[checked((int)item.SelectorFileOffset)] = (byte)selector;
                    impact.Add($"宝物 {id}：{item.Name} 实际装备号 {item.Selector} → {selector}" +
                        (selector < 0x80 ? "（装备号＝特效号，同号宝物共享）" : "（未占用号）") + "。");
                }
                if (draft.SpecialItemIds.Contains(id))
                {
                    if (!item.NeedsSpecialType || item.TypeFileOffset < 0 || itemBefore[checked((int)item.TypeFileOffset)] != item.TypeValue)
                    { errors.Add($"宝物{id}普通转特殊类型字节未经验证。"); continue; }
                    itemAfter[checked((int)item.TypeFileOffset)] = checked((byte)(item.TypeValue + 1));
                    impact.Add($"宝物 {id}：{item.Name} 普通类型 {item.TypeValue} → 特殊类型 {item.TypeValue + 1}；保持同一装备类型家族。");
                }
            }
            if (!itemBefore.AsSpan().SequenceEqual(itemAfter)) candidates.Add(new(group.Key, itemBefore, itemAfter, "宝物特效值"));
        }
        return new EngineEffectAssignmentPreview
        {
            Candidates = candidates, Errors = errors, Impact = impact,
            Summary = $"特效分配：宝物绑定{draft.ItemTargets.Count}项，兵种分配{draft.JobTargets.Count}项，宝物真实值{draft.ItemValues.Count}项",
            ExpectedItemTargets = new Dictionary<string, int>(draft.ItemTargets),
            ExpectedJobTargets = draft.JobTargets.ToDictionary(pair => pair.Key, pair => pair.Value.ToArray()),
            ExpectedItemValues = new Dictionary<int, int>(draft.ItemValues),
            ExpectedItemSelectors = new Dictionary<int, int>(draft.ItemSelectorTargets),
            ExpectedItemTypes = draft.SpecialItemIds.ToDictionary(id => id,
                id => draft.Catalog.Items.Single(item => item.Id == id).TypeValue + 1)
        };
    }

    public EngineEffectScanReport? Verify(ProjectWorkspace workspace, EngineEffectAssignmentPreview preview)
    {
        foreach (var candidate in preview.Candidates)
        {
            var current = File.ReadAllBytes(candidate.FilePath);
            if (current.Length != candidate.AfterBytes.Length)
                throw new InvalidDataException($"{Path.GetFileName(candidate.FilePath)} 写后文件长度不等于分配候选。");
            // The unified transaction may also contain the effect-management
            // draft. Verify only bytes owned by this candidate so independent
            // edits in the same EXE do not cause a false failure.
            for (var offset = 0; offset < candidate.AfterBytes.Length; offset++)
                if ((offset >= candidate.BeforeBytes.Length || candidate.BeforeBytes[offset] != candidate.AfterBytes[offset]) &&
                    current[offset] != candidate.AfterBytes[offset])
                    throw new InvalidDataException($"{Path.GetFileName(candidate.FilePath)} 偏移 0x{offset:X} 写后字节不等于分配候选。");
        }
        if (preview.ExpectedItemTargets.Count == 0 && preview.ExpectedJobTargets.Count == 0 &&
            preview.ExpectedItemValues.Count == 0 && preview.ExpectedItemSelectors.Count == 0 &&
            preview.ExpectedItemTypes.Count == 0) return null;
        // Verification runs before the transaction refreshes the caller's documents.
        // Open a separate read-only view so item selector/type/N semantics come from
        // the written files rather than the original TableDocument byte cache.
        var writtenWorkspace = new ProjectWorkspace();
        writtenWorkspace.Open(workspace.RootPath);
        var report = new EngineEffectScanService().Scan(writtenWorkspace);
        var catalog = Read(writtenWorkspace, report);
        foreach (var (id, value) in preview.ExpectedItemValues)
            if (catalog.Items.SingleOrDefault(item => item.Id == id)?.Value != value)
                throw new InvalidDataException($"宝物{id}真实特殊效果值写后语义复读不符。");
        foreach (var (id, selector) in preview.ExpectedItemSelectors)
            if (catalog.Items.SingleOrDefault(item => item.Id == id)?.Selector != selector)
                throw new InvalidDataException($"宝物{id}实际装备号写后语义复读不符。");
        foreach (var (id, type) in preview.ExpectedItemTypes)
        {
            var item = catalog.Items.SingleOrDefault(item => item.Id == id);
            if (item?.TypeValue != type || item.NeedsSpecialType)
                throw new InvalidDataException($"宝物{id}普通转特殊类型写后语义复读不符。");
        }
        foreach (var (key, target) in preview.ExpectedItemTargets)
        {
            var effect = catalog.Effects.FirstOrDefault(effect => effect.Key == key);
            if (effect == null || effect.ItemSelectors.Count != 1 || effect.ItemSelectors[0] != target)
                throw new InvalidDataException($"绑定组{key}写后分配字段复读不等于装备号{target}。");
        }
        foreach (var (key, slots) in preview.ExpectedJobTargets)
        {
            var effect = catalog.Effects.FirstOrDefault(effect => effect.Key == key);
            if (!catalog.JobLayoutVerified || effect == null || !effect.JobSlots.Select(slot => (slot.JobId, slot.Value))
                    .SequenceEqual(slots.Select(slot => (slot.JobId, slot.Value))))
                throw new InvalidDataException($"特效{key}真实兵种槽写后复读不符。");
        }
        return report;
    }

    public EngineEffectWriteResult Commit(ProjectWorkspace workspace, EngineEffectScanReport report,
        EngineEffectAssignmentDraft draft, EngineEffectAssignmentPreview preview)
    {
        if (!preview.CanWrite) return new() { Success = false, Message = string.Join(Environment.NewLine, preview.Errors) };
        EngineEffectScanReport? verified = null;
        var result = new EngineEffectTransactionService().Commit(workspace, preview.Summary, preview.Candidates,
            () => { verified = Verify(workspace, preview); });
        if (result.Success) result.VerifiedReport = verified;
        if (result.Success) draft.Clear();
        return result;
    }

    private static string Owners(EngineEffectAssignmentCatalog catalog, IReadOnlyList<int> selectors,
        IReadOnlyDictionary<int, int>? pendingSelectors = null)
    {
        var owners = catalog.Items.Where(item =>
            {
                var selector = pendingSelectors?.GetValueOrDefault(item.Id, item.Selector) ?? item.Selector;
                var active = item.SelectorFileOffset >= 0 &&
                    (!item.NeedsSpecialType || pendingSelectors?.ContainsKey(item.Id) == true);
                return active && selector != 255 && selectors.Contains(selector);
            })
            .Select(item => $"{item.Id}:{item.Name}").ToArray();
        return owners.Length == 0 ? "无" : string.Join("、", owners);
    }
}
