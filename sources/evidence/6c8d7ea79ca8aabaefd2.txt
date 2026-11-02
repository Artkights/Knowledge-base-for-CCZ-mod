using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using ImageManager.Core;

namespace ImageManager.Tests;

internal static class AtlasTransformTests
{
    public static void Run()
    {
        var directory = Path.Combine(Path.GetTempPath(), "ImageManager.AtlasTransforms", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(directory);
        var frames = new List<DecodedFrame>();
        try
        {
            foreach (var spec in new[] { (Action: "mov", Count: 11, Size: 48), (Action: "spc", Count: 5, Size: 48), (Action: "atk", Count: 12, Size: 64) })
            for (var index = 0; index < spec.Count; index++)
            {
                var bitmap = new Bitmap(spec.Size, spec.Size);
                using (var graphics = Graphics.FromImage(bitmap))
                {
                    graphics.Clear(Color.Transparent);
                    // Preserve visible animation offsets: a crop must not center every silhouette independently.
                    graphics.FillRectangle(Brushes.Red, 10 + index % 2 * 6, 10 + index % 3 * 2, 20, 20);
                }
                frames.Add(new(new("Unit_" + spec.Action + ".e5", "memory.e5", 242, index, 1,
                    spec.Action, "front", spec.Size, spec.Size), bitmap));
            }
            var asset = new LogicalImageAsset("SComposite", 242, "S_242", ImageCategory.CharacterS, ResourceKind.SComposite,
                frames.Select(frame => frame.Descriptor).ToArray(), [], false, false, string.Empty) { PhysicalImageNumber = 242 };
            var context = ReferenceAtlasContext.Create(asset, frames);
            var service = new ReferenceAtlasService();
            var exported = service.Export(directory, context, Color.Magenta, new() { Scale = 1 });
            var manifest = AtlasManifest.Load(exported.ManifestPath);

            foreach (var dimensions in new[] { new Size(810, 430), new Size(430, 910) })
            {
                using var padded = new Bitmap(dimensions.Width, dimensions.Height);
                using (var source = new Bitmap(exported.PngPath))
                using (var graphics = Graphics.FromImage(padded))
                {
                    graphics.Clear(Color.White);
                    graphics.DrawImageUnscaled(source, 31, 43);
                }
                var path = Path.Combine(directory, $"padding-{dimensions.Width}.png");
                padded.Save(path, ImageFormat.Png);
                var mapping = manifest.CreateSourceMapping(context, dimensions, new Rectangle(31, 43, 348, 348));
                using var normalized = service.Normalize(path, context, new() { SourceMapping = mapping });
                Require(!normalized.HasBlockingIssues, "横/竖画布的有效区域裁剪失败。");
                foreach (var frame in normalized.Frames)
                    Require(ReferenceAtlasService.PixelHash(frame.Bitmap) == ReferenceAtlasService.PixelHash(
                        frames.Single(original => original.Descriptor == frame.Descriptor).Bitmap), "横/竖留白还原改变像素或动作偏移。");
            }

            var scaledPath = Path.Combine(directory, "noninteger-offsets.png");
            Resize(exported.PngPath, scaledPath, new Size(1024, 1024));
            using (var normalized = service.Normalize(scaledPath, context, new()))
            {
                Require(!normalized.HasBlockingIssues, "非整数规范图出现阻断。");
                var first = Foreground(normalized.Frames.Single(frame => frame.Descriptor.Action == "mov" && frame.Descriptor.FrameIndex == 0).Bitmap);
                var second = Foreground(normalized.Frames.Single(frame => frame.Descriptor.Action == "mov" && frame.Descriptor.FrameIndex == 1).Bitmap);
                Require(Math.Abs((second.Left - first.Left) - 6) <= 1,
                    $"非整数还原抹掉动作横向偏移：原始6px，输出{second.Left - first.Left}px。");
                Require(Math.Abs((second.Top - first.Top) - 2) <= 1,
                    $"非整数还原抹掉动作纵向偏移：原始2px，输出{second.Top - first.Top}px。");
            }

            var stretchedPath = Path.Combine(directory, "horizontal-stretch.png");
            Resize(exported.PngPath, stretchedPath, new Size(696, 348));
            var stretched = manifest.CreateSourceMapping(context, new Size(696, 348));
            stretched.ConfirmedFrames.UnionWith(stretched.FrameRectangles.Keys);
            using (var keepRatio = service.Normalize(stretchedPath, context, new() { SourceMapping = stretched }))
            {
                var bounds = Foreground(keepRatio.Frames[0].Bitmap);
                Require(bounds.Width >= bounds.Height * 1.8, "默认等比还原擅自修复了源图横纵比例。");
            }
            stretched.RepairAspectRatio = true;
            using (var repaired = service.Normalize(stretchedPath, context, new() { SourceMapping = stretched }))
            {
                var bounds = Foreground(repaired.Frames[0].Bitmap);
                Require(Math.Abs(bounds.Width - bounds.Height) <= 1, "显式横纵拉伸修复没有恢复原始比例。");
            }

            // Empty required frames must still block even when their source rectangle was manually confirmed.
            using (var missing = new Bitmap(exported.PngPath))
            {
                var source = manifest.Frames.Single(frame => frame.Action == "mov" && frame.FrameIndex == 0).NativeBounds.ToRectangle();
                using (var graphics = Graphics.FromImage(missing)) graphics.FillRectangle(Brushes.Magenta, source);
                var path = Path.Combine(directory, "missing.png");
                missing.Save(path, ImageFormat.Png);
                var mapping = manifest.CreateSourceMapping(context, missing.Size);
                mapping.ConfirmedFrames.UnionWith(mapping.FrameRectangles.Keys);
                using var normalized = service.Normalize(path, context, new() { SourceMapping = mapping });
                Require(normalized.HasBlockingIssues && normalized.FrameDiagnostics.Any(issue => issue.Descriptor.Action == "mov" &&
                    issue.Descriptor.FrameIndex == 0 && issue.Severity == AtlasIssueSeverity.Error), "已确认源框掩盖了真正缺帧。");
            }
        }
        finally
        {
            foreach (var frame in frames) frame.Dispose();
            Directory.Delete(directory, true);
        }
    }

    private static void Resize(string sourcePath, string targetPath, Size size)
    {
        using var source = new Bitmap(sourcePath);
        using var target = new Bitmap(size.Width, size.Height);
        using (var graphics = Graphics.FromImage(target))
        {
            graphics.InterpolationMode = InterpolationMode.NearestNeighbor;
            graphics.PixelOffsetMode = PixelOffsetMode.Half;
            graphics.DrawImage(source, new Rectangle(Point.Empty, size), new Rectangle(Point.Empty, source.Size), GraphicsUnit.Pixel);
        }
        target.Save(targetPath, ImageFormat.Png);
    }

    private static Rectangle Foreground(Bitmap bitmap)
    {
        var left = bitmap.Width; var top = bitmap.Height; var right = 0; var bottom = 0;
        for (var y = 0; y < bitmap.Height; y++)
        for (var x = 0; x < bitmap.Width; x++)
            if (bitmap.GetPixel(x, y).A > 16)
            { left = Math.Min(left, x); top = Math.Min(top, y); right = Math.Max(right, x + 1); bottom = Math.Max(bottom, y + 1); }
        return right <= left || bottom <= top ? Rectangle.Empty : Rectangle.FromLTRB(left, top, right, bottom);
    }

    private static void Require(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }
}
