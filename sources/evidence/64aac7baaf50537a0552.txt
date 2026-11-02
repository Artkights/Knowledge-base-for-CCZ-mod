namespace ImageManager.Core;

/// <summary>Native scene collision cells. This is not an indexed raster image.</summary>
public sealed class PmapTerrainData
{
    private readonly byte[] _header;
    private readonly ushort[] _cells;
    internal PmapTerrainData(byte[] header, int width, int height, int layers, ushort[] cells)
    {
        _header = (byte[])header.Clone(); _cells = (ushort[])cells.Clone();
        Width = width; Height = height; Layers = layers;
        CanEdit = width == 100 && height == 100 && layers == 1 &&
                  cells.All(value => value is PmapTerrainCodec.ClearValue or PmapTerrainCodec.BlockedValue);
        Diagnostic = CanEdit ? string.Empty : "该地形的尺寸、层数或格值尚未验证，仅可查看。";
    }
    public int Width { get; }
    public int Height { get; }
    public int Layers { get; }
    public ReadOnlyMemory<byte> Header => _header;
    public IReadOnlyList<ushort> Cells => Array.AsReadOnly(_cells);
    public bool CanEdit { get; }
    public string Diagnostic { get; }
    public ushort GetCell(int x, int y)
    {
        if (x < 0 || x >= Width || y < 0 || y >= Height) throw new ArgumentOutOfRangeException(nameof(x));
        return _cells[checked(y * Width + x)];
    }
}
