using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;

namespace ImageManager.Core;

public sealed class ReferenceAtlasService : IReferenceAtlasService
{
    private readonly IReferenceAtlasLayoutPlanner _layouts;
    private readonly IAiAtlasNormalizer _normalizer;

    public ReferenceAtlasService(IReferenceAtlasLayoutPlanner? layouts = null, IAiAtlasNormalizer? normalizer = null)
    {
        _layouts = layouts ?? new ReferenceAtlasLayoutPlanner();
        _normalizer = normalizer ?? new AiAtlasNormalizer(_layouts);
    }

    public ReferenceAtlasExportResult Export(string destinationDirectory, LogicalImageAsset asset,
        IReadOnlyList<DecodedFrame> frames, Color keyColor)
        => ExportCore(destinationDirectory, asset, frames, keyColor,
            asset.Kind == ResourceKind.RComposite ? $"R{asset.LogicalId:000}" : SResourceExchangeNaming.BaseName(asset),
            new ReferenceAtlasExportOptions { Scale = 1, IncludeTransparent = true });

    public ReferenceAtlasExportResult Export(string destinationDirectory, ReferenceAtlasContext context,
        Color keyColor, ReferenceAtlasExportOptions? options = null)
        => ExportCore(destinationDirectory, context.Asset, context.Frames, keyColor,
            context.BaseName, options ?? new ReferenceAtlasExportOptions());

    private ReferenceAtlasExportResult ExportCore(string destinationDirectory, LogicalImageAsset asset,
        IReadOnlyList<DecodedFrame> frames, Color keyColor, string baseName, ReferenceAtlasExportOptions options)
    {
        if (asset.Kind is not (ResourceKind.RComposite or ResourceKind.SComposite))
            throw new InvalidOperationException("参考总图只适用于 R/S 逻辑形象。");
        if (frames.Count == 0) throw new InvalidOperationException("没有可导出的帧。");
        if (asset.Kind == ResourceKind.SComposite)
            SResourceExchangeNaming.ValidateFrameSet(asset, frames.Select(frame => frame.Descriptor).ToArray());
        if (options.Scale is not (1 or 2 or 4))
            throw new ArgumentOutOfRangeException(nameof(options), "参考图倍率只支持 1、2、4。");
        if (asset.Kind == ResourceKind.SComposite)
            destinationDirectory = Path.Combine(destinationDirectory, SResourceExchangeNaming.Category(asset));
        Directory.CreateDirectory(destinationDirectory);

        var layout = _layouts.Plan(asset, frames);
        using var transparent = new Bitmap(layout.CanvasSize, layout.CanvasSize, PixelFormat.Format32bppArgb);
        using var keyed = new Bitmap(layout.CanvasSize, layout.CanvasSize, PixelFormat.Format32bppArgb);
        using (var graphics = Graphics.FromImage(transparent))
        {
            graphics.Clear(Color.Transparent);
            graphics.CompositingMode = CompositingMode.SourceOver;
            foreach (var placement in layout.Placements)
            {
                using var frame = MakeKeyTransparent(placement.Frame.Bitmap, keyColor);
                graphics.DrawImageUnscaled(frame, placement.Bounds.X, placement.Bounds.Y);
            }
        }
        using (var graphics = Graphics.FromImage(keyed))
        {
            graphics.Clear(Color.FromArgb(255, keyColor.R, keyColor.G, keyColor.B));
            graphics.CompositingMode = CompositingMode.SourceOver;
            graphics.DrawImageUnscaled(transparent, 0, 0);
        }

        var pngPath = Path.Combine(destinationDirectory, baseName + ".png");
        var transparentPath = options.IncludeTransparent
            ? Path.Combine(destinationDirectory, baseName + ".transparent.png") : string.Empty;
        SaveScaledPng(keyed, pngPath, options.Scale);
        if (options.IncludeTransparent) SaveScaledPng(transparent, transparentPath, options.Scale);
        var manifestPath = Path.Combine(destinationDirectory, baseName + ".atlas.json");
        AtlasManifest.Create(asset, layout, options.Scale).Save(manifestPath);
        var guidePath = Path.Combine(destinationDirectory, baseName + ".动作对照.png");
        SaveGuide(keyed, layout, guidePath, baseName, options.Scale);
        var promptPath = UpdatePromptDocument(destinationDirectory, asset, layout, keyColor, baseName, options);
        return new ReferenceAtlasExportResult(pngPath, transparentPath, promptPath)
        { ManifestPath = manifestPath, GuidePath = guidePath };
    }

    public AiAtlasNormalizationResult Normalize(string pngPath, LogicalImageAsset asset,
        IReadOnlyList<DecodedFrame> referenceFrames, AiAtlasNormalizationOptions options)
        => _normalizer.Normalize(pngPath, asset, referenceFrames, options);

    public AiAtlasNormalizationResult Normalize(string pngPath, ReferenceAtlasContext context,
        AiAtlasNormalizationOptions options, CancellationToken cancellationToken = default)
        => _normalizer.Normalize(pngPath, context.Asset, context.Frames, options, cancellationToken);

    public static Color ResolveKeyColor(IReadOnlyList<Color> palette)
    {
        var preferred = palette.FirstOrDefault(color => color.G == 0 && color.B == 255 && color.R is 247 or 255);
        return preferred.IsEmpty ? Color.Magenta : Color.FromArgb(255, preferred.R, preferred.G, preferred.B);
    }

    public static string PixelHash(Bitmap bitmap)
    {
        using var normalized = new Bitmap(bitmap.Width, bitmap.Height, PixelFormat.Format32bppArgb);
        using (var graphics = Graphics.FromImage(normalized)) graphics.DrawImageUnscaled(bitmap, 0, 0);
        var data = normalized.LockBits(new Rectangle(0, 0, normalized.Width, normalized.Height),
            ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
        try
        {
            var rowLength = checked(normalized.Width * 4);
            using var stream = new MemoryStream(checked(rowLength * normalized.Height));
            var row = new byte[rowLength];
            for (var y = 0; y < normalized.Height; y++)
            {
                Marshal.Copy(data.Scan0 + y * data.Stride, row, 0, row.Length);
                stream.Write(row);
            }
            return Convert.ToHexString(SHA256.HashData(stream.ToArray()));
        }
        finally { normalized.UnlockBits(data); }
    }

    private static Bitmap MakeKeyTransparent(Bitmap source, Color keyColor)
    {
        var output = new Bitmap(source.Width, source.Height, PixelFormat.Format32bppArgb);
        for (var y = 0; y < source.Height; y++)
        for (var x = 0; x < source.Width; x++)
        {
            var color = source.GetPixel(x, y);
            var key = color.G == 0 && color.B == 255 && color.R is 247 or 255 ||
                      color.R == keyColor.R && color.G == keyColor.G && color.B == keyColor.B;
            output.SetPixel(x, y, color.A == 0 || key ? Color.Transparent : color);
        }
        return output;
    }

    private static void SavePngAtomically(Bitmap bitmap, string target)
    {
        var temporary = target + "." + Guid.NewGuid().ToString("N") + ".tmp";
        try
        {
            bitmap.Save(temporary, ImageFormat.Png);
            File.Move(temporary, target, true);
        }
        finally
        {
            if (File.Exists(temporary)) File.Delete(temporary);
        }
    }

    private static void SaveScaledPng(Bitmap bitmap, string path, int scale)
    {
        if (scale == 1) { SavePngAtomically(bitmap, path); return; }
        using var enlarged = new Bitmap(bitmap.Width * scale, bitmap.Height * scale, PixelFormat.Format32bppArgb);
        using (var graphics = Graphics.FromImage(enlarged))
        {
            graphics.CompositingMode = CompositingMode.SourceCopy;
            graphics.InterpolationMode = InterpolationMode.NearestNeighbor;
            graphics.PixelOffsetMode = PixelOffsetMode.Half;
            graphics.SmoothingMode = SmoothingMode.None;
            graphics.DrawImage(bitmap, new Rectangle(0, 0, enlarged.Width, enlarged.Height),
                new Rectangle(Point.Empty, bitmap.Size), GraphicsUnit.Pixel);
        }
        SavePngAtomically(enlarged, path);
    }

    private static void SaveGuide(Bitmap keyed, ReferenceAtlasLayoutPlan layout, string path, string baseName, int exportScale)
    {
        // Labels live on a separate image so AI source pixels and exact grid positions remain untouched.
        var scale = Math.Max(3, exportScale);
        var side = checked(layout.CanvasSize * scale);
        const int headerHeight = 62;
        using var guide = new Bitmap(side, side + headerHeight, PixelFormat.Format32bppArgb);
        using (var graphics = Graphics.FromImage(guide))
        using (var font = new Font("Microsoft YaHei UI", 10, FontStyle.Bold))
        using (var titleFont = new Font("Microsoft YaHei UI", 12, FontStyle.Bold))
        using (var grid = new Pen(Color.FromArgb(230, 255, 255, 255), 2))
        using (var reservedPen = new Pen(Color.Yellow, 2) { DashStyle = DashStyle.Dash })
        using (var labelBackground = new SolidBrush(Color.FromArgb(220, 20, 20, 20)))
        {
            graphics.Clear(Color.FromArgb(28, 28, 32));
            graphics.DrawString(baseName + " · 动作编号对照（请勿作为 AI 主图）", titleFont, Brushes.White, 10, 5);
            graphics.DrawString("参考图只提供动作格式；导入目标始终是图库当前所选形象。", font, Brushes.White, 10, 32);
            graphics.InterpolationMode = InterpolationMode.NearestNeighbor;
            graphics.PixelOffsetMode = PixelOffsetMode.Half;
            graphics.DrawImage(keyed, new Rectangle(0, headerHeight, side, side),
                new Rectangle(Point.Empty, keyed.Size), GraphicsUnit.Pixel);
            foreach (var placement in layout.Placements)
            {
                var bounds = placement.Bounds;
                var box = new Rectangle(bounds.X * scale, headerHeight + bounds.Y * scale,
                    bounds.Width * scale, bounds.Height * scale);
                graphics.DrawRectangle(grid, box);
                var descriptor = placement.Frame.Descriptor;
                var label = (layout.TurnCount > 1 ? $"{descriptor.Turn}转 " : string.Empty) +
                    $"{descriptor.Action}{descriptor.FrameIndex} · {DirectionLabel(descriptor.Direction)}";
                var size = graphics.MeasureString(label, font);
                graphics.FillRectangle(labelBackground, box.X + 2, box.Y + 2, Math.Min(box.Width - 4, size.Width + 6), size.Height + 3);
                graphics.DrawString(label, font, Brushes.White, box.X + 4, box.Y + 3);
            }
            if (layout.LayoutId == ReferenceAtlasLayoutPlanner.SLayoutId)
                foreach (var section in layout.Sections.Where(item => item.Action == "mov+spc"))
                foreach (var row in new[] { 1, 2 })
                {
                    var box = new Rectangle((section.X + 250) * scale,
                        headerHeight + (section.Y + row * 50) * scale, 48 * scale, 48 * scale);
                    graphics.DrawRectangle(reservedPen, box);
                    graphics.DrawString("保留空格", font, Brushes.Yellow, box.X + 4, box.Y + 5);
                }
        }
        SavePngAtomically(guide, path);
    }

    private static string DirectionLabel(string direction) => direction switch
    {
        "front" => "正面", "back" => "背面", "side" => "侧面", "none" => "动作", _ => direction
    };

    private static string UpdatePromptDocument(string directory, LogicalImageAsset asset,
        ReferenceAtlasLayoutPlan layout, Color keyColor, string baseName, ReferenceAtlasExportOptions options)
    {
        var start = $"<!-- asset:{baseName}:start -->";
        var end = $"<!-- asset:{baseName}:end -->";
        var target = Path.Combine(directory, "形象图提示词.md");
        var text = File.Exists(target) ? File.ReadAllText(target) : string.Empty;
        if (!text.Contains("<!-- image-manager-atlas-prompt-v6 -->", StringComparison.Ordinal))
            text = PromptHeader(keyColor);

        var entry = BuildPromptEntry(start, end, baseName, layout, keyColor, options);
        var startIndex = text.IndexOf(start, StringComparison.Ordinal);
        var endIndex = startIndex < 0 ? -1 : text.IndexOf(end, startIndex, StringComparison.Ordinal);
        if (startIndex >= 0 && endIndex >= 0)
            text = text[..startIndex] + entry + text[(endIndex + end.Length)..];
        else
            text = text.TrimEnd() + Environment.NewLine + Environment.NewLine + entry;

        var temporary = target + "." + Guid.NewGuid().ToString("N") + ".tmp";
        File.WriteAllText(temporary, text.TrimEnd() + Environment.NewLine, new UTF8Encoding(false));
        File.Move(temporary, target, true);
        return target;
    }

    private static string PromptHeader(Color keyColor)
    {
        var hex = $"#{keyColor.R:X2}{keyColor.G:X2}{keyColor.B:X2}";
        return """
<!-- image-manager-atlas-prompt-v6 -->
# 形象图 AI 修改提示词

## 必须遵守

- 优先把无 `.transparent` 后缀的 PNG 作为动作格式参考图；它使用不透明键色背景，避免 AI 平台把透明层压成黑色。
- 透明版只用于人工观察，不要同时把两版作为两个不同角色或两套动作理解。
- 当前文件只是一套完整动作，不要额外生成进阶版本、其他人物或其他套动作。
- 原参考人物只提供动作格式：动作、方向、帧序与原生画布规格。新人物的服装、武器、配色、体型和轮廓以本次角色要求为准，不必贴合原人物。
- 保持格子数量、动作顺序、方向和空白保留格；每格只能出现对应的一帧。建议保持原画布和间距，方便直接回导。
- 不得合并帧、交换行列、裁掉攻击特效或在空白保留格中新增内容。
- 输出使用无损 PNG。若平台调整尺寸、增加留白或改变画布比例，保持全部动作完整且顺序不变，回导时通过有效画布和源分格校正；不要裁掉人物或刀光。
- 建议使用本项目纯键色背景或有效透明背景；不要添加场景或棋盘格。背景改成白色、黑色或有色差时，回导前检查并校正蒙版。
- 同一人物各方向和动作应保持造型、装备、配色、光源及像素风格一致。
- 攻击和特技可以使用格内空间，但不得进入相邻格。
- 沿用每格动作和朝向，保持同一角色在连续动作中的比例与相对落点；倒地、退场等动作保留各自的位移。武器和特效需要完整。
- 像素边缘必须硬朗，保持原生 48×48、48×64 或 64×64 像素的细节尺度；整数倍参考图中，一个原生像素对应一个同色方块。禁止抗锯齿、模糊、渐变、插值、景深、柔光、高清插画和微小纹理。
- 格间空隙必须保持纯键色，不得绘制网格线、文字、编号、水印、边框或标注。不得镜像、复制同一姿态充当不同动作。
- 导回默认保持新人物比例并使用最近邻还原，先校正源裁剪格，再检查蒙版、连续动画和最终原生像素结果。格位漂移可自动配准或手动拖框修正。
- 索引图片导回时使用目标原有调色板，默认不抖动，颜色损失会在确认窗口中单独统计；真彩图片保持原有真彩存储。
- `.atlas.json` 是布局清单，`.动作对照.png` 是人工编号图，两者均不作为 AI 人物参考图。回图可改名；清单只辅助布局，实际写入目标始终由图库当前选择确定。

## S 形象统一语义

- 48x48 第 1 行 mov0..5：正面移动两帧、背面移动两帧、侧面移动两帧。
- 48x48 第 2 行 mov6..10：正面受击、背面受击、侧面受击、倒地、退场；末格为空。
- 48x48 第 3 行 spc0..4：特技五帧；末格为空。
- 64x64 三行分别为正面 atk0..3、背面 atk4..7、侧面 atk8..11。

当前项目键色：KEY_COLOR
""".Replace("KEY_COLOR", hex, StringComparison.Ordinal);
    }

    private static string BuildPromptEntry(string start, string end, string baseName,
        ReferenceAtlasLayoutPlan layout, Color keyColor, ReferenceAtlasExportOptions options)
    {
        var builder = new StringBuilder();
        builder.AppendLine(start).AppendLine($"## {baseName}").AppendLine();
        builder.AppendLine($"- AI 主文件：`{baseName}.png`");
        builder.AppendLine($"- 配套布局：`{baseName}.atlas.json`；人工动作编号：`{baseName}.动作对照.png`。");
        if (options.IncludeTransparent) builder.AppendLine($"- 透明观察版：`{baseName}.transparent.png`；它与主文件是同一套动作。");
        var exportedSize = layout.CanvasSize * options.Scale;
        builder.AppendLine($"- 推荐输出：`{exportedSize}×{exportedSize}` PNG；平台改变尺寸或添加留白后，可在管理器中校正有效画布和分格。");
        builder.AppendLine($"- 原生画布：`{layout.CanvasSize}×{layout.CanvasSize}`；放大倍率：`{options.Scale}`；每个原生像素必须是 `{options.Scale}×{options.Scale}` 的同色方块。");
        builder.AppendLine($"- 帧数：`{layout.Placements.Count}`；键色：`#{keyColor.R:X2}{keyColor.G:X2}{keyColor.B:X2}`；下表坐标已按输出倍率换算。");
        foreach (var section in layout.Sections)
            builder.AppendLine($"- {section.Name.Replace(ChineseTurn(section.Turn) + "转 ", string.Empty, StringComparison.Ordinal)}：({section.X * options.Scale},{section.Y * options.Scale}) {section.Width * options.Scale}×{section.Height * options.Scale}");
        builder.AppendLine().AppendLine(layout.TurnCount > 1
            ? "| 套号 | 动作 | 方向 | 帧号 | 输出矩形 |" : "| 动作 | 方向 | 帧号 | 输出矩形 |");
        builder.AppendLine(layout.TurnCount > 1 ? "| ---: | --- | --- | ---: | --- |" : "| --- | --- | ---: | --- |");
        foreach (var placement in layout.Placements)
        {
            var frame = placement.Frame.Descriptor;
            builder.AppendLine($"| {(layout.TurnCount > 1 ? frame.Turn + " | " : string.Empty)}{frame.Action} | {frame.Direction} | {frame.FrameIndex} | " +
                               $"({placement.Bounds.X * options.Scale},{placement.Bounds.Y * options.Scale}) {placement.Bounds.Width * options.Scale}×{placement.Bounds.Height * options.Scale} |");
        }
        builder.AppendLine(end);
        return builder.ToString().TrimEnd();
    }

    private static string ChineseTurn(int turn) => turn switch
    {
        1 => "一",
        2 => "二",
        3 => "三",
        _ => turn.ToString()
    };
}
