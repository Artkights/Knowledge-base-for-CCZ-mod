using DataManager.Core.Binary;
using DataManager.Core.History;
using DataManager.Core.Models;
using System.Text.Json;

namespace DataManager.Core.Appearance;

/// <summary>Prepared save contributions; the caller records their changes in its own history operation.</summary>
public sealed class AppearanceSyncSession
{
    private readonly string _root;
    private readonly IReadOnlyDictionary<string, AppliedAppearanceFile> _candidates;
    private readonly List<AppliedAppearanceFile> _applied = [];
    private readonly BinaryTableWriter _writer = new();
    private readonly string? _lockPath;
    private bool _committed;
    public AppearanceSyncReport Report { get; }
    public IReadOnlyList<PreparedAppearanceSaveGroup> PreparedGroups { get; }
    public IReadOnlyList<AppliedAppearanceFile> AppliedFiles => _applied;
    public string? RecoverySnapshotDirectory { get; private set; }

    internal AppearanceSyncSession(string root, AppearanceSyncReport report, IReadOnlyList<PreparedAppearanceSaveGroup> groups,
        IReadOnlyDictionary<string, AppliedAppearanceFile> candidates, string? lockPath)
    {
        _root = root; Report = report; PreparedGroups = groups; _candidates = candidates; _lockPath = lockPath;
    }

    public void Commit()
    {
        if (_committed) return;
        _committed = true;
        if (PreparedGroups.Count == 0) return;
        FileStream? rootLock = null;
        try
        {
            if (_lockPath is not null && File.Exists(_lockPath))
            {
                try { rootLock = new FileStream(_lockPath, FileMode.Open, FileAccess.ReadWrite, FileShare.None); }
                catch (Exception ex) when (IsFileFailure(ex))
                {
                    foreach (var group in PreparedGroups) Skip(group, "游戏存档事务锁被占用或不可访问：" + ex.Message);
                    return;
                }
            }
            foreach (var group in PreparedGroups) CommitGroup(group);
        }
        finally { rootLock?.Dispose(); }
    }

    private void CommitGroup(PreparedAppearanceSaveGroup group)
    {
        var touched = new List<AppliedAppearanceFile>();
        try
        {
            // Validate every group member before replacing its first file.
            foreach (var file in group.Files)
            {
                var prepared = _candidates[file.RelativePath];
                if (!HashService.Sha256(Path.Combine(_root, file.RelativePath)).Equals(file.ExpectedFileHash, StringComparison.OrdinalIgnoreCase))
                    throw new IOException($"提交前文件已被外部修改：{file.RelativePath}。");
                if (!file.CandidateBytes.AsSpan().SequenceEqual(prepared.AfterBytes))
                    throw new InvalidDataException($"候选快照已改变：{file.RelativePath}。");
                file.CandidateVerifier?.Invoke((byte[])file.CandidateBytes.Clone());
            }
            foreach (var file in group.Files)
            {
                var prepared = _candidates[file.RelativePath];
                // Write may replace the file and then fail its final verification. Track it
                // before entering that boundary so every possible replacement can be restored.
                Remember(prepared, touched);
                _writer.Write(prepared.Change, _root, useNewBytes: true);
                var disk = File.ReadAllBytes(Path.Combine(_root, file.RelativePath));
                if (!disk.AsSpan().SequenceEqual(prepared.AfterBytes)) throw new IOException($"写后逐字节复读失败：{file.RelativePath}。");
                file.CandidateVerifier?.Invoke(disk);
            }
            Report.UpdatedSaves++;
            Report.UpdatedPersonFields += group.UpdatedPersonFields;
        }
        catch (Exception ex) when (IsFileFailure(ex))
        {
            Skip(group, ex.Message);
            try { RestoreFiles(touched); }
            catch (Exception restore) when (IsFileFailure(restore))
            {
                Report.Add($"{group.SaveRelativePath}：本组恢复未完成；{PreserveRecovery(restore.Message)}");
                throw new IOException($"存档同步组恢复未完成：{group.SaveRelativePath}。{restore.Message}", ex);
            }
        }
    }

    private void Remember(AppliedAppearanceFile file, List<AppliedAppearanceFile> touched)
    {
        touched.Add(file); _applied.Add(file);
    }

    private void Skip(PreparedAppearanceSaveGroup group, string reason)
    {
        Report.SkippedSaves++;
        Report.Add($"{group.SaveRelativePath}：未同步，{reason}");
    }

    public void Rollback()
    {
        if (_applied.Count == 0) return;
        try
        {
            using var rootLock = _lockPath is null || !File.Exists(_lockPath) ? null : new FileStream(_lockPath, FileMode.Open, FileAccess.ReadWrite, FileShare.None);
            RestoreFiles(_applied.ToArray());
            Report.UpdatedSaves = 0; Report.UpdatedPersonFields = 0;
        }
        catch (Exception ex) when (IsFileFailure(ex))
        {
            var recovery = PreserveRecovery(ex.Message);
            Report.Add("存档形象恢复未完成；" + recovery);
            throw new IOException("存档形象恢复失败；外部修改与未恢复快照均被保留。" + recovery, ex);
        }
    }

    private string PreserveRecovery(string reason)
    {
        if (_applied.Count == 0) return reason;
        try
        {
            var storage = Path.Combine(ProjectHistoryPaths.GetDataRoot(_root), "存档形象恢复");
            if (ProjectHistoryPaths.IsInside(storage, _root))
                storage = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "DataManager", "AppearanceRecovery",
                    HashService.Sha256(System.Text.Encoding.UTF8.GetBytes(_root.ToUpperInvariant())));
            RecoverySnapshotDirectory ??= Path.Combine(storage, DateTime.UtcNow.ToString("yyyyMMddTHHmmssfff") + "-" + Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(RecoverySnapshotDirectory);
            var files = new List<object>();
            for (var index = 0; index < _applied.Count; index++)
            {
                var file = _applied[index];
                var beforeName = $"{index:D4}.before.bin"; var afterName = $"{index:D4}.after.bin";
                WriteFlushed(Path.Combine(RecoverySnapshotDirectory, beforeName), file.BeforeBytes);
                WriteFlushed(Path.Combine(RecoverySnapshotDirectory, afterName), file.AfterBytes);
                files.Add(new { file.RelativePath, file.Change.BeforeHash, file.Change.AfterHash,
                    BeforeAttributes = (int)file.BeforeAttributes, BeforeSnapshot = beforeName, AfterSnapshot = afterName });
            }
            WriteFlushed(Path.Combine(RecoverySnapshotDirectory, "manifest.json"), JsonSerializer.SerializeToUtf8Bytes(new
            {
                SchemaVersion = 1, ProjectRoot = _root, Reason = reason, CreatedUtc = DateTime.UtcNow, Files = files
            }, new JsonSerializerOptions { WriteIndented = true }));
            return "恢复前后快照和 manifest 已持久保存在：" + RecoverySnapshotDirectory + "；" + reason;
        }
        catch (Exception ex) when (IsFileFailure(ex))
        {
            return "内存恢复快照已保留，但持久快照写入失败：" + ex.Message + "；" + reason;
        }
    }

    private static void WriteFlushed(string path, byte[] bytes)
    {
        using var stream = new FileStream(path, FileMode.Create, FileAccess.Write, FileShare.Read);
        stream.Write(bytes); stream.Flush(flushToDisk: true);
    }

    private void RestoreFiles(IReadOnlyList<AppliedAppearanceFile> files)
    {
        // Check the entire requested rollback before changing anything. External values survive a conflict.
        foreach (var file in files)
        {
            var hash = HashService.Sha256(Path.Combine(_root, file.RelativePath));
            if (!hash.Equals(file.Change.AfterHash, StringComparison.OrdinalIgnoreCase) &&
                !hash.Equals(file.Change.BeforeHash, StringComparison.OrdinalIgnoreCase))
                throw new IOException($"存档形象恢复冲突：{file.RelativePath} 已被外部修改，保留当前外部内容。");
        }
        foreach (var file in files.Reverse())
        {
            var path = Path.Combine(_root, file.RelativePath);
            if (!HashService.Sha256(path).Equals(file.Change.BeforeHash, StringComparison.OrdinalIgnoreCase))
                _writer.Write(file.Change, _root, useNewBytes: false);
            File.SetAttributes(path, file.BeforeAttributes);
            if (!File.ReadAllBytes(path).AsSpan().SequenceEqual(file.BeforeBytes))
                throw new IOException($"存档形象恢复复读失败：{file.RelativePath}。");
            _applied.Remove(file);
        }
    }

    internal static bool IsFileFailure(Exception ex) => ex is IOException or InvalidDataException or UnauthorizedAccessException or
        ArgumentException or FormatException or NotSupportedException or System.Security.SecurityException or InvalidOperationException;
}
