using System.Drawing;

namespace ImageManager.Core;

public sealed partial class AiAtlasNormalizer
{
    private static Rectangle ResolveEffectiveBounds(int[] pixels, Size size, Rectangle? requested)
    {
        var full = new Rectangle(Point.Empty, size);
        if (requested is { IsEmpty: false } bounds)
        {
            if (bounds.Width <= 0 || bounds.Height <= 0 || !full.Contains(bounds))
                throw new InvalidDataException("有效画布必须在源图范围内，且宽高大于零。");
            return bounds;
        }
        // Only remove an enclosing, nearly uniform frame with a different inner canvas.
        // Empty margins in a normal atlas are part of its coordinate system.
        var outer = Color.FromArgb(pixels[0]);
        bool Similar(int argb, Color color, int distance = 24)
        {
            var c = Color.FromArgb(argb);
            return Math.Abs(c.R - color.R) + Math.Abs(c.G - color.G) + Math.Abs(c.B - color.B) < distance;
        }
        bool UniformLine(bool horizontal, int at)
        {
            var length = horizontal ? size.Width : size.Height;
            var hits = 0; var total = 0;
            for (var p = 0; p < length; p += Math.Max(1, length / 256))
            { total++; if (Similar(pixels[horizontal ? at * size.Width + p : p * size.Width + at], outer)) hits++; }
            return hits >= total * .96;
        }
        int Strip(bool horizontal, bool reverse)
        {
            var length = horizontal ? size.Height : size.Width;
            var count = 0;
            while (count < Math.Max(1, length / 20) && UniformLine(horizontal, reverse ? length - 1 - count : count)) count++;
            return count;
        }
        var top = Strip(true, false); var bottom = Strip(true, true);
        var left = Strip(false, false); var right = Strip(false, true);
        if (new[] { top, bottom, left, right }.Any(v => v == 0)) return full;
        var inner = Rectangle.FromLTRB(left, top, size.Width - right, size.Height - bottom);
        var c = Color.FromArgb(pixels[inner.Top * size.Width + inner.Left]);
        if (Similar(c.ToArgb(), outer, 70)) return full;
        var matching = 0; var sampled = 0;
        for (var x = inner.Left; x < inner.Right; x += Math.Max(1, inner.Width / 128))
        { sampled += 2; if (Similar(pixels[inner.Top * size.Width + x], c)) matching++; if (Similar(pixels[(inner.Bottom - 1) * size.Width + x], c)) matching++; }
        return matching >= sampled * .85 ? inner : full;
    }

    private static BackgroundInfo ClassifyEffectiveBackground(int[] pixels, Size size, Rectangle roi, AiAtlasNormalizationOptions options)
    {
        var border = new List<Color>(); var transparent = 0; var count = 0;
        for (var y = roi.Top; y < roi.Bottom; y += Math.Max(1, roi.Height / 350))
            for (var x = roi.Left; x < roi.Right; x += Math.Max(1, roi.Width / 350))
            { count++; if ((uint)pixels[y * size.Width + x] >> 24 < 250) transparent++; }
        if (transparent > count / 1000) return new(AtlasBackgroundKind.Transparent, Color.Transparent);
        foreach (var p in EffectiveBorder(roi)) border.Add(Color.FromArgb(pixels[p.Y * size.Width + p.X]));
        var sample = options.BackgroundSamples.Concat(options.BackgroundSample is Point samplePoint ? new[] { samplePoint } : Array.Empty<Point>()).FirstOrDefault(p => roi.Contains(p), new Point(-1, -1));
        var color = sample.X >= 0 ? Color.FromArgb(pixels[sample.Y * size.Width + sample.X]) : DominantBorderColor(border);
        return new(color.B >= 235 && color.G <= 28 && color.R >= 220 ? AtlasBackgroundKind.KeyColor : AtlasBackgroundKind.OpaqueColor, color);
    }

    private static IEnumerable<Point> EffectiveBorder(Rectangle roi)
    {
        var step = Math.Max(1, Math.Min(roi.Width, roi.Height) / 256);
        for (var x = roi.Left; x < roi.Right; x += step) { yield return new(x, roi.Top); yield return new(x, roi.Bottom - 1); }
        for (var y = roi.Top; y < roi.Bottom; y += step) { yield return new(roi.Left, y); yield return new(roi.Right - 1, y); }
    }

    private static bool[] BuildEffectiveForeground(int[] pixels, Size size, Rectangle roi, BackgroundInfo background,
        AiAtlasNormalizationOptions options, CancellationToken token)
    {
        var foreground = new bool[pixels.Length];
        if (background.Kind == AtlasBackgroundKind.Transparent)
        {
            for (var y = roi.Top; y < roi.Bottom; y++)
            { token.ThrowIfCancellationRequested(); for (var x = roi.Left; x < roi.Right; x++) foreground[y * size.Width + x] = (uint)pixels[y * size.Width + x] >> 24 >= 16; }
        }
        else
        {
            var samples = options.BackgroundSamples.Concat(options.BackgroundSample is Point p ? new[] { p } : Array.Empty<Point>()).Where(roi.Contains).Distinct().ToArray();
            var colors = samples.Select(p => Color.FromArgb(pixels[p.Y * size.Width + p.X])).Prepend(background.Color).Select(ToLab).ToArray();
            var cache = new Dictionary<int, bool>(); var candidate = new bool[pixels.Length]; var threshold = Math.Max(3, options.BackgroundTolerance);
            for (var y = roi.Top; y < roi.Bottom; y++)
            {
                token.ThrowIfCancellationRequested();
                for (var x = roi.Left; x < roi.Right; x++)
                {
                    var i = y * size.Width + x; var color = pixels[i];
                    if (!cache.TryGetValue(color, out var isBackground))
                    { var lab = ToLab(Color.FromArgb(color)); isBackground = colors.Any(c => LabDistance(c, lab) <= threshold); cache[color] = isBackground; }
                    candidate[i] = isBackground || (uint)color >> 24 < 16;
                }
            }
            var flooded = new bool[pixels.Length]; var queue = new Queue<int>();
            void Add(int x, int y) { var i = y * size.Width + x; if (candidate[i] && !flooded[i]) { flooded[i] = true; queue.Enqueue(i); } }
            for (var x = roi.Left; x < roi.Right; x++) { Add(x, roi.Top); Add(x, roi.Bottom - 1); }
            for (var y = roi.Top; y < roi.Bottom; y++) { Add(roi.Left, y); Add(roi.Right - 1, y); }
            foreach (var sample in samples) Add(sample.X, sample.Y);
            var iterations = 0;
            while (queue.Count > 0)
            {
                if ((iterations++ & 0x3FFF) == 0) token.ThrowIfCancellationRequested();
                var i = queue.Dequeue(); var x = i % size.Width; var y = i / size.Width;
                if (x > roi.Left) Add(x - 1, y); if (x + 1 < roi.Right) Add(x + 1, y); if (y > roi.Top) Add(x, y - 1); if (y + 1 < roi.Bottom) Add(x, y + 1);
            }
            for (var y = roi.Top; y < roi.Bottom; y++) for (var x = roi.Left; x < roi.Right; x++)
                { var i = y * size.Width + x; foreground[i] = !flooded[i] && (uint)pixels[i] >> 24 >= 16; }
        }
        foreach (var stroke in options.MaskStrokes)
            for (var y = Math.Max(roi.Top, stroke.Center.Y - stroke.Radius); y < Math.Min(roi.Bottom, stroke.Center.Y + stroke.Radius + 1); y++)
                for (var x = Math.Max(roi.Left, stroke.Center.X - stroke.Radius); x < Math.Min(roi.Right, stroke.Center.X + stroke.Radius + 1); x++)
                    if ((x - stroke.Center.X) * (x - stroke.Center.X) + (y - stroke.Center.Y) * (y - stroke.Center.Y) <= stroke.Radius * stroke.Radius) foreground[y * size.Width + x] = stroke.Keep;
        return foreground;
    }

    private static SourceMapping BuildFlexibleMapping(ReferenceAtlasLayoutPlan layout, bool[] foreground, Size size, Rectangle roi,
        AiAtlasNormalizationOptions options, List<string> diagnostics, CancellationToken token)
    {
        var scale = roi.Width / (double)layout.CanvasSize;
        var canonical = roi.Width == roi.Height;
        bool GridHasCleanGutters()
        {
            var inside = 0; var outside = 0;
            for (var y = roi.Top; y < roi.Bottom; y += Math.Max(1, roi.Height / 350))
                for (var x = roi.Left; x < roi.Right; x += Math.Max(1, roi.Width / 350))
                {
                    if (!foreground[y * size.Width + x]) continue;
                    var native = new Point((int)((x - roi.Left) / scale), (int)((y - roi.Top) / scale));
                    if (layout.Placements.Any(p => p.Bounds.Contains(native))) inside++; else outside++;
                }
            return outside <= Math.Max(2, inside * .003);
        }
        var mapping = new SourceMapping();
        Rectangle CanonicalRect(Rectangle b) => new(roi.Left + (int)Math.Round(b.X * roi.Width / (double)layout.CanvasSize), roi.Top + (int)Math.Round(b.Y * roi.Height / (double)layout.CanvasSize), Math.Max(1, (int)Math.Round(b.Width * roi.Width / (double)layout.CanvasSize)), Math.Max(1, (int)Math.Round(b.Height * roi.Height / (double)layout.CanvasSize)));
        foreach (var p in layout.Placements)
        { var key = FrameKey(p.Frame.Descriptor); mapping.Rectangles[key] = Clamp(CanonicalRect(p.Bounds), size); mapping.SectionKeys[key] = SectionKey(p.Frame.Descriptor); mapping.Confidences[key] = .45; }
        if (canonical && GridHasCleanGutters())
        {
            foreach (var key in mapping.Rectangles.Keys) mapping.Confidences[key] = 1;
            mapping.ReservedRectangles.AddRange(CanonicalReservedRectangles(layout).Select(r => r with { Bounds = CanonicalRect(r.Bounds) }));
            diagnostics.Add("有效区域符合规范格位，保持原始相对位置直接还原。");
        }
        else
        {
            var rows = layout.Placements.GroupBy(p => p.Bounds.Y).OrderBy(g => g.Key).ToArray();
            var detected = DetectRows(foreground, size, roi, rows.Length);
            if (detected == null)
                foreach (var key in mapping.Rectangles.Keys) mapping.Issues[key] = "语义行识别有歧义，请校正对应源框并确认。";
            else
                for (var row = 0; row < rows.Length; row++)
                {
                    token.ThrowIfCancellationRequested();
                    var placements = rows[row].OrderBy(p => p.Bounds.X).ToArray();
                    var band = new Rectangle(roi.Left, detected[row].Top, roi.Width, detected[row].Height);
                    var columns = DetectColumns(foreground, size, band, placements.Length);
                    if (columns == null)
                    {
                        foreach (var p in placements) mapping.Issues[FrameKey(p.Frame.Descriptor)] = "该行动作数量或间隔不明确，请校正源框并确认。";
                        continue;
                    }
                    var pitch = columns.Length > 1 ? Median(columns.Zip(columns.Skip(1), (a, b) => (b.Left + b.Right - a.Left - a.Right) / 2d).ToArray()) : band.Height;
                    var origin = Median(columns.Select((column, index) => (column.Left + column.Right) / 2d - index * pitch).ToArray());
                    var expectedNative = placements[0].Bounds.Width;
                    var cell = Math.Max(band.Height, pitch * expectedNative / (expectedNative + 2d));
                    cell = Math.Max(cell, columns.Max(c => c.Width));
                    for (var col = 0; col < placements.Length; col++)
                    {
                        var p = placements[col]; var key = FrameKey(p.Frame.Descriptor); var component = columns[col];
                        // Keep the complete silhouette, with a little room for detached effects.
                        var x = (int)Math.Floor(origin + col * pitch - cell / 2);
                        var y = (int)Math.Floor(band.Bottom - cell);
                        mapping.Rectangles[key] = Rectangle.Intersect(roi, new Rectangle(x, y, (int)Math.Ceiling(cell), (int)Math.Ceiling(cell)));
                        mapping.Confidences[key] = Math.Min(.9, detected[row].Confidence);
                    }
                }
            diagnostics.Add("按动作顺序分别识别语义行和横向格位；可拖动源框校正。");
        }
        if (options.SourceMapping is { } manual)
            foreach (var pair in manual.FrameRectangles)
            {
                if (!mapping.Rectangles.ContainsKey(pair.Key)) continue;
                if (pair.Value.Width <= 0 || pair.Value.Height <= 0 || !roi.Contains(pair.Value))
                { mapping.Issues[pair.Key] = "源框无效或超出有效画布，请修正后重新处理。"; continue; }
                mapping.Rectangles[pair.Key] = pair.Value;
                if (manual.ConfirmedFrames.Contains(pair.Key)) { mapping.Issues.Remove(pair.Key); mapping.Confidences[pair.Key] = 1; }
            }
        foreach (var duplicates in mapping.Rectangles.GroupBy(p => p.Value).Where(g => g.Count() > 1))
            foreach (var pair in duplicates) mapping.Issues[pair.Key] = "多个必需动作使用相同源框，请分别指定对应动作。";
        foreach (var group in layout.Placements.GroupBy(p => SectionKey(p.Frame.Descriptor)))
        {
            var scales = group.Select(p => { var b = mapping.Rectangles[FrameKey(p.Frame.Descriptor)]; return Math.Max(b.Width / (double)p.Bounds.Width, b.Height / (double)p.Bounds.Height); }).ToArray();
            // A shared scale keeps an edited crop from changing one frame's character size.
            mapping.GroupScales[group.Key] = scales.Max();
        }
        diagnostics.Add($"有效区域 {roi.X},{roi.Y} {roi.Width}×{roi.Height}；源框校正先于去底色和像素还原。");
        return mapping;
    }

    private static Rectangle[]? DetectColumns(bool[] foreground, Size size, Rectangle band, int expected)
    {
        var values = new int[band.Width];
        for (var x = band.Left; x < band.Right; x++) for (var y = band.Top; y < band.Bottom; y++) if (foreground[y * size.Width + x]) values[x - band.Left]++;
        var runs = new List<Rectangle>(); var start = -1; var threshold = Math.Max(1, band.Height / 150);
        for (var x = 0; x <= values.Length; x++)
        {
            var active = x < values.Length && values[x] >= threshold;
            if (active && start < 0) start = x;
            if (!active && start >= 0) { runs.Add(new Rectangle(band.Left + start, band.Top, x - start, band.Height)); start = -1; }
        }
        while (runs.Count > expected)
        {
            var at = Enumerable.Range(0, runs.Count - 1).MinBy(i => runs[i + 1].Left - runs[i].Right);
            runs[at] = Rectangle.Union(runs[at], runs[at + 1]); runs.RemoveAt(at + 1);
        }
        return runs.Count == expected ? runs.ToArray() : null;
    }

    private static double Median(double[] values)
    { Array.Sort(values); return values.Length == 0 ? 1 : values.Length % 2 == 1 ? values[values.Length / 2] : (values[values.Length / 2 - 1] + values[values.Length / 2]) / 2; }

    private static AtlasSourceMapping ToPublicMapping(SourceMapping mapping, Rectangle roi, AiAtlasNormalizationOptions options)
    {
        var output = new AtlasSourceMapping { EffectiveBounds = roi, RepairAspectRatio = options.SourceMapping?.RepairAspectRatio == true };
        foreach (var pair in mapping.Rectangles) output.FrameRectangles.Add(pair.Key, pair.Value);
        if (options.SourceMapping != null) output.ConfirmedFrames.UnionWith(options.SourceMapping.ConfirmedFrames);
        return output;
    }

    private static Bitmap RestoreMappedFrame(int[] pixels, bool[] foreground, Size size, Rectangle source, Size target,
        SourceMapping mapping, string key, AiAtlasNormalizationOptions options)
    {
        if (options.SourceMapping?.RepairAspectRatio == true) return Resample(pixels, foreground, size, source, target, options.Kernel);
        var groupScale = mapping.GroupScales[mapping.SectionKeys[key]];
        var factor = 1 / Math.Max(.001, groupScale);
        factor = Math.Min(factor, Math.Min(target.Width / (double)source.Width, target.Height / (double)source.Height));
        var restoredSize = new Size(Math.Max(1, (int)Math.Round(source.Width * factor)), Math.Max(1, (int)Math.Round(source.Height * factor)));
        using var restored = Resample(pixels, foreground, size, source, restoredSize, options.Kernel);
        var output = new Bitmap(target.Width, target.Height, System.Drawing.Imaging.PixelFormat.Format32bppArgb);
        using var graphics = Graphics.FromImage(output);
        graphics.DrawImageUnscaled(restored, (target.Width - restored.Width) / 2, target.Height - restored.Height);
        return output;
    }
}
