using ImageManager.Core;

namespace DataManager.Images;

/// <summary>Scene pairing belongs to the integrated editor; the standalone image editor opts out.</summary>
internal static class IntegratedSceneMutationPolicy
{
    private static readonly SceneTerrainService Terrain = new();

    internal static bool IsMmap(string key) => key.Equals("Mmap.e5", StringComparison.OrdinalIgnoreCase);

    internal static void RequireImageResource(string key)
    {
        if (key.Equals("Pmap.e5", StringComparison.OrdinalIgnoreCase))
            throw new InvalidOperationException("Pmap 是内场景地形数据，请在 Mmap 场景背景中使用“地形编辑”。");
    }

    internal static MutationPlan Append(ProjectProfile project, string resourceKey, Func<MutationPlan> build,
        int? copySourceMmapNumber = null)
    {
        RequireImageResource(resourceKey);
        if (!IsMmap(resourceKey)) return build();
        // Capture both files before the image builder reads its template or opens a source image.
        var snapshot = CapturePair(project);
        return snapshot.Complete(Terrain.AugmentAppend(project, build(), copySourceMmapNumber));
    }

    internal static MutationPlan Delete(ProjectProfile project, IReadOnlyList<LogicalImageAsset> assets,
        Func<MutationPlan> build)
    {
        foreach (var asset in assets) RequireImageResource(asset.ResourceKey);
        return assets.Any(asset => IsMmap(asset.ResourceKey)) ? Terrain.PlanDelete(project, assets) : build();
    }

    internal static void ValidateCommit(ProjectProfile project, MutationPlan plan)
        => Terrain.ValidateMmapPlan(project, plan);

    internal static async Task<PreparedImageImport> PrepareAsync(IImageImportPreparationService inner,
        ImageImportRequest request, CancellationToken cancellationToken)
    {
        RequireImageResource(request.Resource.Key);
        var snapshot = IsMmap(request.Resource.Key) && request.Operation == ImageImportOperation.Append
            ? CapturePair(request.Project) : null;
        var prepared = await inner.PrepareAsync(request, cancellationToken).ConfigureAwait(false);
        if (snapshot == null || !prepared.CanCommit) return prepared;
        try
        {
            cancellationToken.ThrowIfCancellationRequested();
            var plan = snapshot.Complete(Terrain.AugmentAppend(request.Project, prepared.Plan!));
            // Ownership of the preview rows moves to the replacement result. The old holder has no finalizer.
            return new PreparedImageImport(plan, prepared.Rows);
        }
        catch
        {
            prepared.Dispose();
            throw;
        }
    }

    private static MutationPlanningSnapshot CapturePair(ProjectProfile project)
        => MutationPlanningSnapshot.Capture(new[] { "Mmap.e5", "Pmap.e5" }.Select(key =>
            project.TryGetResource(key) ?? throw new FileNotFoundException("缺少场景配对资源：" + key)));
}
