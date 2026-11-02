using System.Drawing;
using System.Text;
using System.Text.Json;

namespace ImageManager.Core;

/// <summary>Layout-only interchange data. Source identities are descriptive and never select write targets.</summary>
public sealed record AtlasManifest
{
    public const int CurrentVersion = 1;
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        PropertyNameCaseInsensitive = true,
        WriteIndented = true
    };

    public int Version { get; init; } = CurrentVersion;
    public string LayoutId { get; init; } = string.Empty;
    public int NativeCanvasSize { get; init; }
    public int ExportScale { get; init; }
    public int ExportWidth { get; init; }
    public int ExportHeight { get; init; }
    public string ResourceKind { get; init; } = string.Empty;
    public int? SourcePhysicalImageNumber { get; init; }
    public string[] SourceResourceKeys { get; init; } = [];
    public AtlasManifestSection[] Sections { get; init; } = [];
    public AtlasManifestFrame[] Frames { get; init; } = [];

    public static AtlasManifest Create(LogicalImageAsset asset, ReferenceAtlasLayoutPlan layout, int scale)
        => new()
        {
            LayoutId = layout.LayoutId, NativeCanvasSize = layout.CanvasSize, ExportScale = scale,
            ExportWidth = checked(layout.CanvasSize * scale), ExportHeight = checked(layout.CanvasSize * scale),
            ResourceKind = asset.Kind.ToString(),
            SourcePhysicalImageNumber = asset.PhysicalImageNumber ??
                (asset.Kind == global::ImageManager.Core.ResourceKind.SComposite ? layout.Placements[0].Frame.Descriptor.ImageNumber : null),
            SourceResourceKeys = layout.Placements.Select(item => item.Frame.Descriptor.SourceKey).Distinct().ToArray(),
            Sections = layout.Sections.Select(section => new AtlasManifestSection(section.Name, section.Turn,
                section.Action, new(section.X, section.Y, section.Width, section.Height))).ToArray(),
            Frames = layout.Placements.Select(item => new AtlasManifestFrame(
                AiAtlasNormalizer.FrameKey(item.Frame.Descriptor), item.Frame.Descriptor.Turn,
                item.Frame.Descriptor.Action, item.Frame.Descriptor.Direction, item.Frame.Descriptor.FrameIndex,
                item.Frame.Descriptor.Width, item.Frame.Descriptor.Height,
                AtlasManifestBounds.FromRectangle(item.Bounds),
                new(item.Bounds.X * scale, item.Bounds.Y * scale, item.Bounds.Width * scale, item.Bounds.Height * scale))).ToArray()
        };

    public static AtlasManifest Load(string path)
    {
        ArgumentException.ThrowIfNullOrWhiteSpace(path);
        if (new FileInfo(path).Length > 2 * 1024 * 1024)
            throw new InvalidDataException("布局清单过大，请选择管理器导出的 .atlas.json。");
        try
        {
            var manifest = JsonSerializer.Deserialize<AtlasManifest>(File.ReadAllText(path, Encoding.UTF8), JsonOptions)
                ?? throw new InvalidDataException("布局清单为空。");
            manifest.ValidateStructure();
            return manifest;
        }
        catch (JsonException error) { throw new InvalidDataException("布局清单不是有效 JSON。", error); }
    }

    public void Save(string path)
    {
        ValidateStructure();
        var temporary = path + "." + Guid.NewGuid().ToString("N") + ".tmp";
        try
        {
            File.WriteAllText(temporary, JsonSerializer.Serialize(this, JsonOptions) + Environment.NewLine,
                new UTF8Encoding(false));
            File.Move(temporary, path, true);
        }
        finally { if (File.Exists(temporary)) File.Delete(temporary); }
    }

    public void ValidateFor(ReferenceAtlasContext context)
    {
        ArgumentNullException.ThrowIfNull(context);
        ValidateStructure();
        var expected = new ReferenceAtlasLayoutPlanner().Plan(context.Asset, context.Frames);
        if (ResourceKind != context.Asset.Kind.ToString() || LayoutId != expected.LayoutId ||
            Frames.Length != expected.Placements.Count)
            throw new InvalidDataException("布局清单的动作类型、布局版本或帧数与当前所选形象不一致。");
        foreach (var placement in expected.Placements)
        {
            var descriptor = placement.Frame.Descriptor;
            var match = Frames.SingleOrDefault(frame => Matches(frame, descriptor));
            if (match == null || match.NativeWidth != descriptor.Width || match.NativeHeight != descriptor.Height)
                throw new InvalidDataException($"布局清单缺少当前形象的 {descriptor.Action}/{descriptor.Direction}/{descriptor.FrameIndex} 帧或原生尺寸不符。");
        }
    }

    public AtlasSourceMapping CreateSourceMapping(ReferenceAtlasContext context, Size sourceSize,
        Rectangle? effectiveBounds = null)
    {
        ValidateFor(context);
        var roi = effectiveBounds ?? new Rectangle(Point.Empty, sourceSize);
        if (roi.Width <= 0 || roi.Height <= 0 || !new Rectangle(Point.Empty, sourceSize).Contains(roi))
            throw new InvalidDataException("清单映射的有效画布必须位于当前源图内。");
        var mapping = new AtlasSourceMapping { EffectiveBounds = roi };
        foreach (var frame in context.Frames)
        {
            var entry = Frames.Single(candidate => Matches(candidate, frame.Descriptor));
            var native = entry.NativeBounds;
            var left = roi.Left + (int)Math.Round(native.X * roi.Width / (double)NativeCanvasSize);
            var top = roi.Top + (int)Math.Round(native.Y * roi.Height / (double)NativeCanvasSize);
            var right = roi.Left + (int)Math.Round((native.X + native.Width) * roi.Width / (double)NativeCanvasSize);
            var bottom = roi.Top + (int)Math.Round((native.Y + native.Height) * roi.Height / (double)NativeCanvasSize);
            mapping.FrameRectangles[AiAtlasNormalizer.FrameKey(frame.Descriptor)] = Rectangle.FromLTRB(left, top, right, bottom);
        }
        return mapping;
    }

    private static bool Matches(AtlasManifestFrame frame, FrameDescriptor descriptor)
        => frame.Turn == descriptor.Turn && frame.Action == descriptor.Action &&
           frame.Direction == descriptor.Direction && frame.FrameIndex == descriptor.FrameIndex;

    private void ValidateStructure()
    {
        if (Version != CurrentVersion) throw new InvalidDataException($"不支持布局清单版本 {Version}。");
        if (string.IsNullOrWhiteSpace(LayoutId) || NativeCanvasSize is <= 0 or > 16384 ||
            ExportScale is not (1 or 2 or 4) || ExportWidth != NativeCanvasSize * ExportScale ||
            ExportHeight != NativeCanvasSize * ExportScale || Frames == null || Frames.Length is < 1 or > 256 ||
            Sections == null || SourceResourceKeys == null)
            throw new InvalidDataException("布局清单的画布、倍率或帧记录无效。");
        if (Frames.Any(frame => frame == null || frame.NativeBounds == null || frame.OutputBounds == null ||
            string.IsNullOrWhiteSpace(frame.Action) || string.IsNullOrWhiteSpace(frame.Direction) ||
            frame.NativeWidth <= 0 || frame.NativeHeight <= 0 ||
            !IsInside(frame.NativeBounds, NativeCanvasSize) || !IsInside(frame.OutputBounds, ExportWidth)))
            throw new InvalidDataException("布局清单含有无效或越界的动作格。");
        if (Frames.Select(frame => (frame.Turn, frame.Action, frame.Direction, frame.FrameIndex)).Distinct().Count() != Frames.Length)
            throw new InvalidDataException("布局清单含有重复动作帧。");
    }

    private static bool IsInside(AtlasManifestBounds bounds, int size)
        => bounds.X >= 0 && bounds.Y >= 0 && bounds.Width > 0 && bounds.Height > 0 &&
           (long)bounds.X + bounds.Width <= size && (long)bounds.Y + bounds.Height <= size;
}

public sealed record AtlasManifestBounds(int X, int Y, int Width, int Height)
{
    public Rectangle ToRectangle() => new(X, Y, Width, Height);
    public static AtlasManifestBounds FromRectangle(Rectangle bounds) => new(bounds.X, bounds.Y, bounds.Width, bounds.Height);
}

public sealed record AtlasManifestSection(string Name, int Turn, string Action, AtlasManifestBounds NativeBounds);

public sealed record AtlasManifestFrame(string Key, int Turn, string Action, string Direction, int FrameIndex,
    int NativeWidth, int NativeHeight, AtlasManifestBounds NativeBounds, AtlasManifestBounds OutputBounds);
