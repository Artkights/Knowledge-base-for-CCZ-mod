using System.Drawing;

namespace ImageManager.Core;

public sealed class SceneTerrainDocument : IDisposable
{
    private ushort[] _cells;
    private ushort[] _baseline;
    private readonly Stack<CellChange[]> _undo = new();
    private readonly Stack<CellChange[]> _redo = new();
    private Dictionary<int, ushort>? _stroke;
    internal SceneTerrainDocument(Bitmap background, string mmapPath, string? pmapPath, int mmapNumber,
        PmapTerrainData? terrain, bool canEdit, string diagnostic, IReadOnlyDictionary<string, MutationSourceSnapshot> snapshots)
    {
        Background = background; MmapPath = mmapPath; PmapPath = pmapPath;
        MmapImageNumber = mmapNumber; PmapImageNumber = mmapNumber - 40;
        Terrain = terrain; CanEdit = canEdit; Diagnostic = diagnostic; SourceSnapshots = snapshots;
        _cells = terrain?.Cells.ToArray() ?? []; _baseline = (ushort[])_cells.Clone();
        Geometry = new(background.Width, background.Height, terrain?.Width ?? 100, terrain?.Height ?? 100);
    }
    public Bitmap Background { get; }
    public string MmapPath { get; }
    public string? PmapPath { get; }
    public int MmapImageNumber { get; }
    public int PmapImageNumber { get; }
    public int Rows => Terrain?.Height ?? 0;
    public int Columns => Terrain?.Width ?? 0;
    public bool CanEdit { get; }
    public string Diagnostic { get; }
    public DiamondTerrainGeometry Geometry { get; }
    public bool IsDirty => !_cells.AsSpan().SequenceEqual(_baseline);
    public bool CanUndo => _undo.Count > 0;
    public bool CanRedo => _redo.Count > 0;
    internal PmapTerrainData? Terrain { get; }
    internal IReadOnlyDictionary<string, MutationSourceSnapshot> SourceSnapshots { get; private set; }
    public ushort GetCell(int x, int y) => _cells[GetIndex(x, y)];
    public bool IsBlocked(int x, int y) => GetCell(x, y) == PmapTerrainCodec.BlockedValue;
    public void BeginStroke() { if (_stroke != null) EndStroke(); _stroke = new(); }
    public bool SetCell(int x, int y, bool blocked)
    {
        if (!CanEdit) return false;
        var index = GetIndex(x, y); var next = blocked ? PmapTerrainCodec.BlockedValue : PmapTerrainCodec.ClearValue;
        if (_cells[index] == next) return false;
        var ownStroke = _stroke == null;
        if (ownStroke) BeginStroke();
        _stroke!.TryAdd(index, _cells[index]); _cells[index] = next;
        if (ownStroke) EndStroke();
        return true;
    }
    public bool EndStroke()
    {
        if (_stroke == null) return false;
        var changes = _stroke.Where(pair => pair.Value != _cells[pair.Key]).Select(pair => new CellChange(pair.Key, pair.Value, _cells[pair.Key])).ToArray();
        _stroke = null;
        if (changes.Length == 0) return false;
        _undo.Push(changes); _redo.Clear(); return true;
    }
    public bool Undo()
    {
        EndStroke(); if (!CanEdit || !_undo.TryPop(out var changes)) return false;
        foreach (var change in changes) _cells[change.Index] = change.Before;
        _redo.Push(changes); return true;
    }
    public bool Redo()
    {
        EndStroke(); if (!CanEdit || !_redo.TryPop(out var changes)) return false;
        foreach (var change in changes) _cells[change.Index] = change.After;
        _undo.Push(changes); return true;
    }
    internal byte[] BuildPayload() => PmapTerrainCodec.Encode(Terrain ?? throw new InvalidOperationException("缺少地形。"), _cells);
    internal void MarkSaved(IReadOnlyDictionary<string, MutationSourceSnapshot> snapshots)
    { _baseline = (ushort[])_cells.Clone(); SourceSnapshots = snapshots; }
    private int GetIndex(int x, int y)
    {
        if (x < 0 || x >= Columns || y < 0 || y >= Rows) throw new ArgumentOutOfRangeException(nameof(x));
        return checked(y * Columns + x);
    }
    public void Dispose() => Background.Dispose();
    private sealed record CellChange(int Index, ushort Before, ushort After);
}
