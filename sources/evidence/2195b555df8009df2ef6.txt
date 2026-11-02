namespace ImageManager.Core;

/// <summary>
/// A non-owning view of the currently previewed R/S set. Frame descriptors keep
/// their real physical image numbers and turns so a single-set atlas cannot
/// accidentally write another turn or the other S namespace.
/// </summary>
public sealed record ReferenceAtlasContext(
    LogicalImageAsset Asset,
    IReadOnlyList<DecodedFrame> Frames,
    int TargetTurn,
    int? PhysicalImageNumber)
{
    public string BaseName => Asset.Kind == ResourceKind.RComposite
        ? $"R{Asset.LogicalId:000}"
        : SResourceExchangeNaming.BaseName(Asset);

    public static ReferenceAtlasContext Create(LogicalImageAsset asset,
        IReadOnlyList<DecodedFrame> frames, int preferredTurn = 1)
    {
        ArgumentNullException.ThrowIfNull(asset);
        ArgumentNullException.ThrowIfNull(frames);
        if (asset.Kind is not (ResourceKind.RComposite or ResourceKind.SComposite))
            throw new InvalidOperationException("参考图只适用于 R/S 形象。");
        if (frames.Count == 0) throw new InvalidDataException("当前形象没有可用动作帧。");
        if (asset.Kind == ResourceKind.RComposite)
            return new ReferenceAtlasContext(asset, frames, 1, null);
        SResourceExchangeNaming.ValidateFrameSet(asset, frames.Select(frame => frame.Descriptor).ToArray());
        var selected = frames.ToArray();
        var physical = selected.Select(frame => frame.Descriptor.ImageNumber).Distinct().ToArray();
        if (selected.Length != 28 || physical.Length != 1)
            throw new InvalidDataException("当前 S 形象必须包含同一物理槽中的 11 个移动帧、12 个攻击帧和 5 个特技帧。");
        return new ReferenceAtlasContext(asset, selected, 1, physical[0]);
    }
}

public sealed record ReferenceAtlasExportOptions
{
    public int Scale { get; init; } = 4;
    public bool IncludeTransparent { get; init; }
}
