namespace DataManager.Core.Workbooks;

public sealed record WorkbookCellChange(string Sheet, string Cell, string Id, string Field, string OldValue, string NewValue);

/// <summary>A validated, immutable proposal. No game data is changed until ApplyImport.</summary>
public sealed class PageWorkbookImportPreview
{
    public IReadOnlyList<WorkbookCellChange> Changes { get; internal init; } = [];
    public int ChangedCells => Changes.Count;
    internal string ProjectIdentity { get; init; } = "";
    internal DataManager.Core.Domain.BusinessPageKind Page { get; init; }
    internal IReadOnlyList<WorkbookProposal> Proposals { get; init; } = [];
}

internal sealed record WorkbookProposal(string Dataset, string Id, string Field, string Before, string After);
internal sealed record WorkbookColumn(string Key, string Label, bool Editable = false,
    bool Numeric = false, long Minimum = 0, long Maximum = uint.MaxValue);
internal sealed record WorkbookRow(string Id, string[] Values);
internal sealed record WorkbookDataset(string Key, string Label, WorkbookColumn[] Columns, WorkbookRow[] Rows);
internal sealed record WorkbookSheetRegistration(string Key, uint SheetId, uint BaselineSheetId);
internal sealed record WorkbookManifest(string Schema, string Profile, string Variant, string Layout,
    string Page, IReadOnlyList<WorkbookSheetRegistration> Datasets);
