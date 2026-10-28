using DataManager.Core.Binary;
using DataManager.Core.Models;
using DataManager.Core.Profiles;

namespace DataManager.Core.Editing;

public sealed record WorkspaceBinaryCandidate(string FilePath, byte[] BeforeBytes, byte[] AfterBytes, string Module);

/// <summary>
/// Commits specialized binary codecs through the same SHA and saved-history contract
/// as physical tables. Callers supply complete candidate bytes and a semantic reread.
/// </summary>
public sealed class WorkspaceBinaryTransaction
{
    public SaveResult Commit(ProjectWorkspace workspace, string summary,
        IReadOnlyList<WorkspaceBinaryCandidate> candidates, Action? verify = null)
    {
        ArgumentNullException.ThrowIfNull(workspace);
        if (string.IsNullOrWhiteSpace(workspace.RootPath))
            return new SaveResult(false, 0, 0, 0, null, ["尚未打开项目。"]);
        // A reload after binary mutation would discard unsaved DataRows. Require one
        // coherent saved state instead of silently overwriting pending page/CSV drafts.
        if (workspace.IsDirty)
            return new SaveResult(false, 0, 0, 0, null, ["存在未保存的数据草稿，请先保存或撤销草稿，再写入专用二进制数据。"]);

        var changes = new List<(WorkspaceBinaryCandidate Candidate, FileByteChange Change)>();
        try
        {
            var seenPaths = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var candidate in candidates)
            {
                var path = ValidatePath(workspace.RootPath, candidate.FilePath);
                if (!seenPaths.Add(path)) throw new InvalidOperationException($"同一文件不能有多个候选：{path}");
                var beforeHash = HashService.Sha256(candidate.BeforeBytes);
                var baselines = workspace.Documents.Values
                    .Where(document => Path.GetFullPath(document.FilePath).Equals(path, StringComparison.OrdinalIgnoreCase))
                    .Select(document => document.OriginalFileHash).Distinct(StringComparer.OrdinalIgnoreCase).ToArray();
                if (baselines.Length != 1 || !beforeHash.Equals(baselines[0], StringComparison.OrdinalIgnoreCase))
                    throw new IOException($"工作区基线冲突：{Path.GetFileName(path)} 已被工具外修改，请重新打开项目。");
                VerifyHash(path, beforeHash);
                var afterHash = HashService.Sha256(candidate.AfterBytes);
                if (beforeHash.Equals(afterHash, StringComparison.OrdinalIgnoreCase)) continue;
                var resized = candidate.BeforeBytes.Length != candidate.AfterBytes.Length;
                IReadOnlyList<ByteChunk> chunks = resized
                    ? [new ByteChunk(0, candidate.BeforeBytes, candidate.AfterBytes)]
                    : BuildChunks(candidate.BeforeBytes, candidate.AfterBytes);
                changes.Add((candidate, new FileByteChange(Path.GetRelativePath(workspace.RootPath, path), beforeHash,
                    afterHash, candidate.AfterBytes.Length, chunks)
                    { WholeFileReplacement = resized, BeforeLength = resized ? candidate.BeforeBytes.Length : null }));
            }
        }
        catch (Exception ex) { return new SaveResult(false, 0, 0, 0, null, [$"专用数据保存中止：{ex.Message}"]); }
        if (changes.Count == 0) return new SaveResult(true, 0, 0, 0, null, ["没有需要写入的专用数据修改。"]);

        var history = new HistoryEntry
        {
            OperationKind = "专用二进制保存",
            Summary = summary,
            Status = HistoryStatus.Pending,
            ProfileId = workspace.ActiveProfile.ProfileId,
            VariantId = workspace.ActiveProfile.VariantId,
            LayoutRevision = workspace.ActiveProfile.LayoutRevision,
            DetectionMethod = workspace.ProfileMatch?.DetectionMethod ?? "未知",
            CoreFileFingerprints = ProfileDetector.CoreFiles.Select(name => (Name: name, Path: ProjectFileLocator.Resolve(workspace.RootPath, name)))
                .Where(item => File.Exists(item.Path)).ToDictionary(item => item.Name, item => HashService.Sha256(item.Path), StringComparer.OrdinalIgnoreCase),
            Modules = changes.Select(item => item.Candidate.Module).Distinct(StringComparer.Ordinal).ToList(),
            Files = changes.Select(item => item.Change).ToList()
        };
        var written = new List<(WorkspaceBinaryCandidate Candidate, FileByteChange Change)>();
        var registered = false;
        try
        {
            workspace.History.Append(workspace.RootPath, history);
            registered = true;
            foreach (var item in changes)
            {
                written.Add(item);
                AtomicReplace(item.Candidate.FilePath, item.Candidate.AfterBytes, item.Change.BeforeHash, item.Change.AfterHash);
            }
            verify?.Invoke();
            history.Status = HistoryStatus.Active;
            workspace.History.Update(workspace.RootPath, history);
            workspace.ReloadLoadedDocuments();
            return new SaveResult(true, changes.Count, changes.Count, changes.Sum(item => item.Change.Chunks.Sum(chunk => chunk.Length)),
                history, ["专用数据保存成功，已写入可撤回历史并刷新工作区。"]);
        }
        catch (Exception ex)
        {
            var failures = new List<string>();
            foreach (var item in written.AsEnumerable().Reverse())
            {
                try
                {
                    var path = item.Candidate.FilePath;
                    var currentHash = HashService.Sha256(path);
                    if (currentHash.Equals(item.Change.BeforeHash, StringComparison.OrdinalIgnoreCase)) continue;
                    AtomicReplace(path, item.Candidate.BeforeBytes, item.Change.AfterHash, item.Change.BeforeHash);
                }
                catch (Exception rollback) { failures.Add(rollback.Message); }
            }
            history.Status = failures.Count == 0 ? HistoryStatus.Failed : HistoryStatus.Conflict;
            if (registered)
            {
                try { workspace.History.Update(workspace.RootPath, history); }
                catch (Exception historyError) { failures.Add($"历史更新失败：{historyError.Message}"); }
            }
            return new SaveResult(false, 0, 0, 0, history,
                [$"专用数据保存失败：{ex.Message}", failures.Count == 0 ? "已恢复写前文件。" : $"回滚需要检查：{string.Join("；", failures)}"]);
        }
    }

    private static string ValidatePath(string root, string path)
    {
        var absoluteRoot = Path.TrimEndingDirectorySeparator(Path.GetFullPath(root));
        var absolutePath = Path.GetFullPath(path);
        if (!absolutePath.StartsWith(absoluteRoot + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase))
            throw new InvalidOperationException("专用二进制候选超出当前项目。");
        return absolutePath;
    }

    private static void AtomicReplace(string path, byte[] bytes, string expectedHash, string resultHash)
    {
        VerifyHash(path, expectedHash);
        var temporary = path + ".data管理器.binary." + Guid.NewGuid().ToString("N") + ".tmp";
        try
        {
            File.WriteAllBytes(temporary, bytes);
            VerifyHash(temporary, resultHash);
            VerifyHash(path, expectedHash);
            File.Move(temporary, path, true);
            VerifyHash(path, resultHash);
        }
        finally { if (File.Exists(temporary)) File.Delete(temporary); }
    }

    private static void VerifyHash(string path, string expectedHash)
    {
        if (!File.Exists(path) || !HashService.Sha256(path).Equals(expectedHash, StringComparison.OrdinalIgnoreCase))
            throw new IOException($"SHA-256 校验失败：{Path.GetFileName(path)} 当前文件已被工具外修改。");
    }

    private static IReadOnlyList<ByteChunk> BuildChunks(byte[] before, byte[] after)
    {
        var chunks = new List<ByteChunk>();
        for (var offset = 0; offset < before.Length; offset++)
        {
            if (before[offset] == after[offset]) continue;
            var start = offset;
            while (offset + 1 < before.Length && before[offset + 1] != after[offset + 1]) offset++;
            var length = offset - start + 1;
            chunks.Add(new ByteChunk(start, before.AsSpan(start, length).ToArray(), after.AsSpan(start, length).ToArray()));
        }
        return chunks;
    }
}
