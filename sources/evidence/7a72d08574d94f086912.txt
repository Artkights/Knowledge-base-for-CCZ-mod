using System.Drawing;

namespace ImageManager.Core;

/// <summary>Source pixel coordinates. Keys always belong to the selected target context.</summary>
public sealed class AtlasSourceMapping
{
    public Rectangle EffectiveBounds { get; set; }
    public Dictionary<string, Rectangle> FrameRectangles { get; } = new(StringComparer.Ordinal);
    public HashSet<string> ConfirmedFrames { get; } = new(StringComparer.Ordinal);
    public bool RepairAspectRatio { get; set; }

    public AtlasSourceMapping Clone()
    {
        var copy = new AtlasSourceMapping { EffectiveBounds = EffectiveBounds, RepairAspectRatio = RepairAspectRatio };
        foreach (var pair in FrameRectangles) copy.FrameRectangles.Add(pair.Key, pair.Value);
        copy.ConfirmedFrames.UnionWith(ConfirmedFrames);
        return copy;
    }
}
