using System.Drawing;
using System.Reflection.PortableExecutable;

namespace ImageManager.Core;

/// <summary>Pairs Mmap scene images with native Pmap cells and builds ordinary atomic history transactions.</summary>
public sealed class SceneTerrainService
{
    public const int OuterSceneCount = 40;
    private const string PairProtocol = "v1";

    public SceneTerrainDocument Load(ProjectProfile project, int mmapPhysicalNumber, CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        var mmapPath = RequireResource(project, "Mmap.e5");
        var pmapPath = project.TryGetResource("Pmap.e5");
        var snapshots = CaptureDependencies(project, mmapPath, pmapPath);
        var mmap = E5Archive.OpenFresh(mmapPath);
        var background = BmpPayloadService.Decode(mmap.ReadDecoded(mmapPhysicalNumber));
        try
        {
            var reasons = new List<string>(); PmapTerrainData? terrain = null;
            if (mmapPhysicalNumber <= OuterSceneCount) reasons.Add("前 40 个为外场景，没有配对的内场景地形。");
            else if (pmapPath == null || !File.Exists(pmapPath)) reasons.Add("缺少 Pmap.e5，无法读取对应地形。");
            else
            {
                var pmap = E5Archive.OpenFresh(pmapPath);
                var number = mmapPhysicalNumber - OuterSceneCount;
                if (number > pmap.Entries.Count) reasons.Add($"缺少 Pmap 第 {number} 条，对应地形不完整。");
                else
                {
                    try { terrain = PmapTerrainCodec.Decode(pmap.ReadDecoded(number)); }
                    catch (Exception ex) when (ex is InvalidDataException or OverflowException) { reasons.Add(ex.Message); }
                    if (terrain != null && !terrain.CanEdit) reasons.Add(terrain.Diagnostic);
                }
            }
            if (background.Width != 640 || background.Height is not (399 or 400)) reasons.Add("该场景图片尺寸尚未验证，地形仅可查看；已支持 640×399 和 640×400。");
            if (project.IsReadOnly) reasons.Add("当前项目只读。");
            var engineReason = EngineDiagnostic(project);
            if (engineReason != null) reasons.Add(engineReason);
            VerifyDependencies(snapshots);
            cancellationToken.ThrowIfCancellationRequested();
            return new SceneTerrainDocument(background, mmapPath, pmapPath, mmapPhysicalNumber, terrain,
                reasons.Count == 0 && terrain != null, string.Join(Environment.NewLine, reasons), snapshots);
        }
        catch { background.Dispose(); throw; }
    }

    public MutationPlan PlanEdit(ProjectProfile project, SceneTerrainDocument document)
    {
        EnsureWritable(project);
        if (!document.CanEdit || document.PmapPath == null) throw new InvalidOperationException(document.Diagnostic);
        RequireDocumentProject(project, document); document.EndStroke();
        if (!document.IsDirty) throw new InvalidOperationException("地形没有更改，无需保存。");
        VerifyDependencies(document.SourceSnapshots);
        var archive = E5Archive.OpenFresh(document.PmapPath);
        var payload = document.BuildPayload();
        if (!PmapTerrainCodec.IsVerifiedPayload(payload)) throw new InvalidDataException("待保存的地形结构或格值未经验证。");
        var candidate = archive.Rebuild(replacementDecoded: new Dictionary<int, byte[]> { [document.PmapImageNumber] = payload });
        var decodedCandidate = E5Archive.Parse(document.PmapPath, candidate);
        if (decodedCandidate.Entries.Count != archive.Entries.Count ||
            !decodedCandidate.ReadDecoded(document.PmapImageNumber).AsSpan().SequenceEqual(payload) ||
            !payload.AsSpan(0, PmapTerrainCodec.HeaderLength).SequenceEqual(archive.ReadDecoded(document.PmapImageNumber).AsSpan(0, PmapTerrainCodec.HeaderLength)))
            throw new InvalidDataException("地形候选复读后的头部、编号或单元与编辑内容不一致。");
        for (var number = 1; number <= archive.Entries.Count; number++)
            if (number != document.PmapImageNumber) RequireStoredEqual(archive, number, decodedCandidate, number);
        var file = new MutationFile(document.PmapPath, candidate, $"保存 Mmap #{document.MmapImageNumber} 的 Pmap #{document.PmapImageNumber} 地形")
        { ExpectedSource = document.SourceSnapshots[Path.GetFullPath(document.PmapPath)] };
        VerifyDependencies(document.SourceSnapshots);
        return new MutationPlan(Guid.NewGuid().ToString("N"), MutationKind.TerrainEdit,
            $"保存场景 {document.MmapImageNumber} 的地形", [file], [], false,
            new Dictionary<string, string> { ["SceneMmapNumber"] = document.MmapImageNumber.ToString(), ["ScenePmapNumber"] = document.PmapImageNumber.ToString() }, document.SourceSnapshots);
    }

    public void AcceptSaved(ProjectProfile project, SceneTerrainDocument document)
    {
        RequireDocumentProject(project, document);
        if (document.PmapPath == null) throw new InvalidOperationException("缺少地形文件。");
        foreach (var pair in document.SourceSnapshots)
            if (!SamePath(pair.Key, document.PmapPath)) pair.Value.Verify(pair.Key);
        var snapshots = CaptureDependencies(project, document.MmapPath, document.PmapPath);
        var actual = E5Archive.OpenFresh(document.PmapPath).ReadDecoded(document.PmapImageNumber);
        if (!actual.AsSpan().SequenceEqual(document.BuildPayload())) throw new IOException("地形保存后复读不一致，请重新读取。");
        VerifyDependencies(snapshots); document.MarkSaved(snapshots);
    }

    public MutationPlan AugmentAppend(ProjectProfile project, MutationPlan existingMmapPlan, int? copySourceMmapNumber = null)
    {
        EnsureWritable(project);
        var mmapPath = RequireResource(project, "Mmap.e5"); var pmapPath = RequireResource(project, "Pmap.e5");
        VerifyPlanSnapshots(existingMmapPlan);
        return MutationPlanningSnapshot.Build(DependencyPaths(project, mmapPath, pmapPath), () =>
        {
            var file = SingleFile(existingMmapPlan, mmapPath);
            if (existingMmapPlan.Files.Any(item => SamePath(item.TargetPath, pmapPath))) throw new InvalidOperationException("新增候选已包含 Pmap，不能重复配对。");
            var oldMmap = E5Archive.OpenFresh(mmapPath); var nextMmap = E5Archive.Parse(mmapPath, file.CandidateBytes);
            var added = nextMmap.Entries.Count - oldMmap.Entries.Count;
            if (added <= 0 || oldMmap.Entries.Count < OuterSceneCount) throw new InvalidDataException("Mmap 新增候选必须在完整的 40 个外场景后末尾追加。");
            for (var i = 1; i <= oldMmap.Entries.Count; i++) RequireStoredEqual(oldMmap, i, nextMmap, i);
            var pmap = E5Archive.OpenFresh(pmapPath); var insertionNumber = oldMmap.Entries.Count - OuterSceneCount + 1;
            if (pmap.Entries.Count < insertionNumber - 1) throw new InvalidDataException("现有内场景缺少对应 Pmap，无法安全追加；请先修复缺口。");
            var payload = PmapTerrainCodec.CreateDefault();
            if (copySourceMmapNumber is > OuterSceneCount)
            {
                if (copySourceMmapNumber > oldMmap.Entries.Count || copySourceMmapNumber - OuterSceneCount > pmap.Entries.Count)
                    throw new InvalidDataException("复制来源缺少配对地形。");
                payload = pmap.ReadDecoded(copySourceMmapNumber.Value - OuterSceneCount);
                if (!PmapTerrainCodec.IsVerifiedPayload(payload)) throw new InvalidDataException("复制来源的地形结构或格值未经验证。");
            }
            var additions = Enumerable.Range(0, added).Select(_ => (byte[])payload.Clone()).ToArray();
            var pmapBytes = insertionNumber <= pmap.Entries.Count
                ? pmap.Rebuild(insertBeforeDecoded: new Dictionary<int, IReadOnlyList<byte[]>> { [insertionNumber] = additions })
                : pmap.Rebuild(appendDecoded: additions);
            var metadata = CopyMetadata(existingMmapPlan);
            metadata["ScenePairProtocol"] = PairProtocol; metadata["ScenePairAction"] = "Append";
            metadata["SceneMmapNumbers"] = string.Join(",", Enumerable.Range(oldMmap.Entries.Count + 1, added));
            metadata["ScenePmapTailCountBefore"] = (pmap.Entries.Count - (insertionNumber - 1)).ToString();
            metadata["ScenePmapTailCountAfter"] = metadata["ScenePmapTailCountBefore"];
            var result = existingMmapPlan with
            {
                Files = existingMmapPlan.Files.Append(new MutationFile(pmapPath, pmapBytes, "同步插入内场景地形，保留 Pmap 尾部余项")).ToArray(),
                Metadata = metadata,
                Warnings = existingMmapPlan.Warnings.Append(copySourceMmapNumber is > OuterSceneCount
                    ? "新增内场景已复制来源的地形。" : "新增内场景地形默认全部可通行，请在地形编辑中标记障碍。").ToArray()
            };
            ValidateMmapPlan(project, result); return result;
        });
    }

    public MutationPlan PlanDelete(ProjectProfile project, IReadOnlyList<LogicalImageAsset> assets)
    {
        EnsureWritable(project);
        if (assets.Count == 0 || assets.Any(asset => !asset.ResourceKey.Equals("Mmap.e5", StringComparison.OrdinalIgnoreCase)))
            throw new InvalidOperationException("场景配对删除只能处理选中的 Mmap 场景。");
        var mmapPath = RequireResource(project, "Mmap.e5"); var pmapPath = RequireResource(project, "Pmap.e5");
        return MutationPlanningSnapshot.Build(DependencyPaths(project, mmapPath, pmapPath), () =>
        {
            EnsureWritable(project);
            var mmap = E5Archive.OpenFresh(mmapPath); var pmap = E5Archive.OpenFresh(pmapPath);
            var numbers = assets.Select(asset => asset.Frames.Single().ImageNumber).Distinct().Order().ToArray();
            if (numbers.Any(number => number <= 0 || number > mmap.Entries.Count) ||
                assets.Any(asset => !SamePath(asset.Frames.Single().SourcePath, mmapPath))) throw new InvalidOperationException("场景不属于当前项目或编号越界。");
            var outer = numbers.Where(number => number <= OuterSceneCount).ToArray();
            var inner = numbers.Where(number => number > OuterSceneCount).ToArray();
            var pairNumbers = inner.Select(number => number - OuterSceneCount).ToArray();
            if (inner.Length > 0 && pmap.Entries.Count < mmap.Entries.Count - OuterSceneCount)
                throw new InvalidDataException("现有内场景缺少对应 Pmap，无法安全删除并重排；请先修复缺口。");
            if (pairNumbers.Any(number => number > pmap.Entries.Count)) throw new InvalidDataException("待删除内场景缺少对应 Pmap，已拒绝修改。");
            var replacements = outer.ToDictionary(number => number, number => BlackPlaceholder(mmap.ReadDecoded(number)));
            var files = new List<MutationFile>
            { new(mmapPath, mmap.Rebuild(replacementDecoded: replacements, deleteImageNumbers: inner), "外场景保留槽位清空，内场景移除对应图片") };
            var emptyTail = inner.Length > 0 && pairNumbers.Length == pmap.Entries.Count;
            if (inner.Length > 0)
            {
                // Neither the native reader nor E5Archive has an established zero-entry
                // representation. When deleting the last active pair, keep one default
                // unused tail slot; a later append inserts its real pair before this tail.
                var pmapBytes = emptyTail
                    ? pmap.Rebuild(replacementDecoded: new Dictionary<int, byte[]> { [pmap.Entries.Count] = PmapTerrainCodec.CreateDefault() },
                        deleteImageNumbers: pairNumbers.Where(number => number != pmap.Entries.Count).ToArray())
                    : pmap.Rebuild(deleteImageNumbers: pairNumbers);
                files.Add(new MutationFile(pmapPath, pmapBytes, "同步删除对应内场景地形，保留未删除和尾部余项"));
            }
            var warnings = new List<string>();
            if (outer.Length > 0) warnings.Add($"外场景 {string.Join(",", outer)} 已改为同尺寸同编码黑色占位，保留前 40 个外场景槽位。");
            if (inner.Length > 0) warnings.Add($"内场景 {string.Join(",", inner)} 及对应地形将同步删除，后续内场景编号前移；剧本引用不会自动改写。");
            if (emptyTail) warnings.Add("全部内场景已删除，保留一条空地形预留；下次新增场景将正常配对。");
            var metadata = new Dictionary<string, string> { ["ScenePairProtocol"] = PairProtocol, ["ScenePairAction"] = inner.Length > 0 ? "Delete" : "ClearOuter", ["SceneMmapNumbers"] = string.Join(",", numbers) };
            if (emptyTail) metadata["SceneEmptyTailPlaceholder"] = PairProtocol;
            metadata["ScenePmapTailCountBefore"] = Math.Max(0, pmap.Entries.Count - (mmap.Entries.Count - OuterSceneCount)).ToString();
            metadata["ScenePmapTailCountAfter"] = emptyTail ? "1" : metadata["ScenePmapTailCountBefore"];
            var plan = new MutationPlan(Guid.NewGuid().ToString("N"), MutationKind.Delete, $"处理 {numbers.Length} 个场景及配对地形", files, warnings, true,
                metadata);
            ValidateMmapPlan(project, plan); return plan;
        });
    }

    public void ValidateMmapPlan(ProjectProfile project, MutationPlan plan)
    {
        var mmapPath = project.TryGetResource("Mmap.e5");
        if (mmapPath == null) return;
        var files = plan.Files.Where(file => SamePath(file.TargetPath, mmapPath)).ToArray();
        if (files.Length == 0) return;
        if (files.Length != 1 || files[0].DeleteTarget) throw new InvalidDataException("Mmap 结构事务不能删除整个文件或重复写入。");
        var before = E5Archive.OpenFresh(mmapPath); var after = E5Archive.Parse(mmapPath, files[0].CandidateBytes);
        if (before.Entries.Count == after.Entries.Count) return;
        EnsureWritable(project);
        if (plan.Metadata?.GetValueOrDefault("ScenePairProtocol") != PairProtocol) throw new InvalidDataException("Mmap 结构变化缺少配对地形事务，已拒绝写入。");
        var pmapPath = RequireResource(project, "Pmap.e5"); var pmapFile = SingleFile(plan, pmapPath);
        var oldPmap = E5Archive.OpenFresh(pmapPath); var nextPmap = E5Archive.Parse(pmapPath, pmapFile.CandidateBytes);
        var numbers = ParseNumbers(plan.Metadata.GetValueOrDefault("SceneMmapNumbers"));
        var action = plan.Metadata.GetValueOrDefault("ScenePairAction");
        if (action == "Append")
        {
            var count = after.Entries.Count - before.Entries.Count; var start = before.Entries.Count - OuterSceneCount + 1;
            if (count <= 0 || before.Entries.Count < OuterSceneCount || numbers.Length != count ||
                !numbers.SequenceEqual(Enumerable.Range(before.Entries.Count + 1, count)) || oldPmap.Entries.Count < start - 1 ||
                nextPmap.Entries.Count != oldPmap.Entries.Count + count) throw new InvalidDataException("Mmap/Pmap 新增配对数量或位置不一致。");
            for (var i = 1; i <= before.Entries.Count; i++) RequireStoredEqual(before, i, after, i);
            for (var i = 1; i < start; i++) RequireStoredEqual(oldPmap, i, nextPmap, i);
            for (var i = 0; i < count; i++)
                if (!PmapTerrainCodec.IsVerifiedPayload(nextPmap.ReadDecoded(start + i))) throw new InvalidDataException("新增地形结构或格值未经验证。");
            for (var i = start; i <= oldPmap.Entries.Count; i++) RequireStoredEqual(oldPmap, i, nextPmap, i + count);
        }
        else if (action == "Delete")
        {
            var inner = numbers.Where(number => number > OuterSceneCount).ToHashSet();
            var pairNumbers = inner.Select(number => number - OuterSceneCount).ToHashSet();
            var emptyTail = plan.Metadata.GetValueOrDefault("SceneEmptyTailPlaceholder") == PairProtocol;
            if (numbers.Any(number => number <= 0 || number > before.Entries.Count) || inner.Count == 0 ||
                before.Entries.Count - after.Entries.Count != inner.Count || pairNumbers.Any(number => number > oldPmap.Entries.Count) ||
                (!emptyTail && oldPmap.Entries.Count - nextPmap.Entries.Count != inner.Count)) throw new InvalidDataException("Mmap/Pmap 删除配对数量或位置不一致。");
            if (emptyTail && (after.Entries.Count != OuterSceneCount || nextPmap.Entries.Count != 1 || oldPmap.Entries.Count != pairNumbers.Count ||
                !nextPmap.ReadDecoded(1).AsSpan().SequenceEqual(PmapTerrainCodec.CreateDefault())))
                throw new InvalidDataException("最后一个内场景删除后的预留地形无效。");
            var nextNumber = 1;
            for (var i = 1; i <= before.Entries.Count; i++)
            {
                if (inner.Contains(i)) continue;
                if (!numbers.Contains(i)) RequireStoredEqual(before, i, after, nextNumber);
                else
                {
                    var expected = BlackPlaceholder(before.ReadDecoded(i));
                    if (!after.ReadDecoded(nextNumber).AsSpan().SequenceEqual(expected)) throw new InvalidDataException("外场景清空候选必须保留槽位与原画布编码。");
                }
                nextNumber++;
            }
            nextNumber = 1;
            for (var i = 1; i <= oldPmap.Entries.Count; i++)
                if (!pairNumbers.Contains(i)) RequireStoredEqual(oldPmap, i, nextPmap, nextNumber++);
        }
        else throw new InvalidDataException("未知的 Mmap/Pmap 配对结构操作。");
    }

    private static byte[] BlackPlaceholder(byte[] payload)
    {
        using var before = BmpPayloadService.Decode(payload); using var bitmap = new Bitmap(before.Width, before.Height);
        using (var graphics = Graphics.FromImage(bitmap)) graphics.Clear(Color.Black);
        return ImageImportTargetEncoding.Standard(payload, bitmap);
    }
    private static void RequireStoredEqual(E5Archive before, int beforeNumber, E5Archive after, int afterNumber)
    {
        if (before.Entries[beforeNumber - 1].DecodedLength != after.Entries[afterNumber - 1].DecodedLength ||
            !before.ReadStored(beforeNumber).AsSpan().SequenceEqual(after.ReadStored(afterNumber)))
            throw new InvalidDataException("配对结构操作改变了未选中条目的内容或顺序。");
    }
    private static MutationFile SingleFile(MutationPlan plan, string path)
    {
        var matches = plan.Files.Where(file => SamePath(file.TargetPath, path)).ToArray();
        if (matches.Length != 1 || matches[0].DeleteTarget) throw new InvalidDataException("场景配对事务缺少唯一完整候选：" + Path.GetFileName(path));
        matches[0].ExpectedSource.Verify(path); return matches[0];
    }
    private static Dictionary<string, string> CopyMetadata(MutationPlan plan) => plan.Metadata?.ToDictionary(pair => pair.Key, pair => pair.Value) ?? new();
    private static int[] ParseNumbers(string? value)
    {
        if (string.IsNullOrWhiteSpace(value)) throw new InvalidDataException("场景配对事务没有明确编号。");
        var numbers = value.Split(',').Select(text => int.TryParse(text, out var number) ? number : throw new InvalidDataException("场景配对编号无效。")).ToArray();
        if (numbers.Distinct().Count() != numbers.Length) throw new InvalidDataException("场景配对编号重复。");
        return numbers.Order().ToArray();
    }
    private static string RequireResource(ProjectProfile project, string name) => project.TryGetResource(name) is { } path && File.Exists(path)
        ? path : throw new FileNotFoundException("缺少场景资源：" + name);
    private static bool SamePath(string left, string right) => Path.GetFullPath(left).Equals(Path.GetFullPath(right), StringComparison.OrdinalIgnoreCase);
    private static string[] DependencyPaths(ProjectProfile project, string mmapPath, string? pmapPath)
        => new[] { mmapPath, pmapPath, project.TryGetResource("Ekd5.exe") }.Where(path => path != null).Cast<string>().Select(Path.GetFullPath).Distinct(StringComparer.OrdinalIgnoreCase).ToArray();
    private static Dictionary<string, MutationSourceSnapshot> CaptureDependencies(ProjectProfile project, string mmapPath, string? pmapPath)
        => DependencyPaths(project, mmapPath, pmapPath).ToDictionary(path => path, MutationSourceSnapshot.Capture, StringComparer.OrdinalIgnoreCase);
    private static void VerifyDependencies(IReadOnlyDictionary<string, MutationSourceSnapshot> snapshots)
    { foreach (var pair in snapshots) pair.Value.Verify(pair.Key); }
    private static void VerifyPlanSnapshots(MutationPlan plan)
    {
        if (plan.SourceSnapshots != null) VerifyDependencies(plan.SourceSnapshots);
        foreach (var file in plan.Files) file.ExpectedSource.Verify(file.TargetPath);
    }
    private static void RequireDocumentProject(ProjectProfile project, SceneTerrainDocument document)
    {
        if (project.TryGetResource("Mmap.e5") is not { } mmap || !SamePath(mmap, document.MmapPath) ||
            project.TryGetResource("Pmap.e5") is not { } pmap || document.PmapPath == null || !SamePath(pmap, document.PmapPath))
            throw new InvalidOperationException("地形文档不属于当前项目。");
    }
    private static void EnsureWritable(ProjectProfile project)
    {
        if (project.IsReadOnly) throw new InvalidOperationException("当前项目只读。");
        if (EngineDiagnostic(project) is { } reason) throw new InvalidOperationException(reason);
    }
    private static string? EngineDiagnostic(ProjectProfile project)
    {
        if (project.Version is not (ProjectVersion.Ccz64 or ProjectVersion.Ccz65 or ProjectVersion.Ccz66)) return "该引擎版本的场景地形尚未验证。";
        var path = project.TryGetResource("Ekd5.exe");
        if (path == null || !File.Exists(path)) return "缺少 Ekd5.exe，无法验证场景地形消费者。";
        try
        {
            var bytes = File.ReadAllBytes(path);
            using var pe = new PEReader(new MemoryStream(bytes, false)); var headers = pe.PEHeaders;
            if (headers.PEHeader == null) return "游戏引擎不是已验证 PE 文件。";
            bool Match(long va, string hex)
            {
                var rva = va - (long)headers.PEHeader.ImageBase; var signature = Convert.FromHexString(hex);
                foreach (var section in headers.SectionHeaders)
                    if (rva >= section.VirtualAddress && rva + signature.Length <= section.VirtualAddress + (long)section.SizeOfRawData)
                    {
                        var offset = section.PointerToRawData + (int)(rva - section.VirtualAddress);
                        return offset >= 0 && offset <= bytes.Length - signature.Length && bytes.AsSpan(offset, signature.Length).SequenceEqual(signature);
                    }
                return false;
            }
            // Identical consumers in the local 6.4 洗隋, 6.5 baseline and 6.6 revised/山贼 engines.
            return Match(0x40BBE1, "3C0275048345F828") &&
                   Match(0x4268BA, "558BEC6A06E8AD0100003945107D426A04E8A10100003945107D366A02E8950100003945087D2A500FAF4510506A04E8830100005A0FAFC25A0FAF550C03C2034508D1E083C010E878ADFDFF0FB700EB0466B800F05DC2") &&
                   Match(0x426A71, "558BEC8B4508E802ACFDFF0FB7005DC20400") && Match(0x48BB08, "504D41502E4535")
                ? null : "游戏引擎的固定 40 场景偏移或 16 位地形消费者与已验证样本不同，仅可查看。";
        }
        catch (Exception ex) when (ex is IOException or BadImageFormatException or InvalidDataException or OverflowException or UnauthorizedAccessException)
        { return "无法验证场景地形引擎：" + ex.Message; }
    }
}
