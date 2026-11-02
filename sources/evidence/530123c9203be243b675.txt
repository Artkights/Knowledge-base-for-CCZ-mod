using System.Drawing;

namespace ImageManager.Core;

/// <summary>Native 16×8 diamond geometry, verified against the original scene editor.</summary>
public sealed class DiamondTerrainGeometry
{
    public DiamondTerrainGeometry(int imageWidth = 640, int imageHeight = 400, int columns = 100, int rows = 100)
    {
        if (imageWidth <= 0 || imageHeight <= 0 || columns <= 0 || rows <= 0) throw new ArgumentOutOfRangeException(nameof(imageWidth));
        ImageWidth = imageWidth; ImageHeight = imageHeight; Columns = columns; Rows = rows;
    }
    public int ImageWidth { get; }
    public int ImageHeight { get; }
    public int Columns { get; }
    public int Rows { get; }
    public Point? HitTest(PointF pixel)
    {
        if (!float.IsFinite(pixel.X) || !float.IsFinite(pixel.Y) || pixel.X < 0 || pixel.Y < 0 || pixel.X >= ImageWidth || pixel.Y >= ImageHeight) return null;
        var x = (int)Math.Floor(pixel.X / 16d + pixel.Y / 8d + 4.625);
        var y = (int)Math.Floor(pixel.Y / 8d - pixel.X / 16d + 44.625);
        return x >= 0 && x < Columns && y >= 0 && y < Rows ? new Point(x, y) : null;
    }
    public PointF CellCenter(int x, int y) => new(8 * (x - y + 40), 4 * (x + y - 48) - 1);
    public PointF[] CellPolygon(int x, int y)
    {
        var center = CellCenter(x, y);
        return [new(center.X, center.Y - 4), new(center.X + 8, center.Y), new(center.X, center.Y + 4), new(center.X - 8, center.Y)];
    }
    public Point FileToGame(Point cell) => new(cell.X, cell.Y + 2);
    public Point GameToFile(Point cell) => new(cell.X, cell.Y - 2);

    public IReadOnlyList<Point> TraceCells(PointF from, PointF to)
    {
        // Traverse every crossed boundary in the two oblique coordinate axes.
        // Sampling mouse events can skip arbitrarily many diamonds at high speed.
        if (!float.IsFinite(from.X) || !float.IsFinite(from.Y) || !float.IsFinite(to.X) || !float.IsFinite(to.Y)) return [];
        if (!ClipToImage(ref from, ref to)) return [];
        var a0 = from.X / 16d + from.Y / 8d + 4.625;
        var b0 = from.Y / 8d - from.X / 16d + 44.625;
        var a1 = to.X / 16d + to.Y / 8d + 4.625;
        var b1 = to.Y / 8d - to.X / 16d + 44.625;
        var breaks = new SortedSet<double> { 0, 1 };
        AddCrossings(a0, a1, breaks); AddCrossings(b0, b1, breaks);
        var times = breaks.ToArray(); var result = new List<Point>(); var seen = new HashSet<Point>();
        void Add(double t)
        {
            var p = new PointF((float)(from.X + (to.X - from.X) * t), (float)(from.Y + (to.Y - from.Y) * t));
            if (HitTest(p) is { } cell && seen.Add(cell)) result.Add(cell);
        }
        Add(0);
        for (var i = 1; i < times.Length; i++) Add((times[i - 1] + times[i]) / 2);
        Add(1);
        return result;
    }
    private static void AddCrossings(double start, double end, SortedSet<double> result)
    {
        if (start == end) return;
        var minimum = (int)Math.Ceiling(Math.Max(-10000, Math.Min(start, end)));
        var maximum = (int)Math.Floor(Math.Min(10000, Math.Max(start, end)));
        for (var boundary = minimum; boundary <= maximum; boundary++)
        {
            var t = (boundary - start) / (end - start);
            if (t > 0 && t < 1) result.Add(t);
        }
    }

    private bool ClipToImage(ref PointF from, ref PointF to)
    {
        double first = 0, last = 1;
        var start = from; var dx = (double)to.X - from.X; var dy = (double)to.Y - from.Y;
        bool Clip(double direction, double distance)
        {
            if (direction == 0) return distance >= 0;
            var t = distance / direction;
            if (direction < 0) { if (t > last) return false; first = Math.Max(first, t); }
            else { if (t < first) return false; last = Math.Min(last, t); }
            return true;
        }
        if (!Clip(-dx, start.X) || !Clip(dx, ImageWidth - start.X) || !Clip(-dy, start.Y) || !Clip(dy, ImageHeight - start.Y)) return false;
        from = new((float)(start.X + first * dx), (float)(start.Y + first * dy));
        to = new((float)(start.X + last * dx), (float)(start.Y + last * dy));
        return true;
    }
}
