using System.Buffers.Binary;
using System.Text.RegularExpressions;
using DataManager.Core.Binary;
using DataManager.Core.Models;
using DataManager.Core.Profiles;

namespace DataManager.Core.Appearance;

/// <summary>Synchronizes only explicitly changed R/S assignments into proven native saves.</summary>
public static class SaveAppearanceSyncService
{
    public static AppearanceSyncSession Prepare(string root, string profileId, byte[] executableBytes,
        IReadOnlyList<PersonAppearanceUpdate> updates)
    {
        try { return PrepareCore(root, profileId, executableBytes, updates); }
        catch (Exception ex) when (ex is not OutOfMemoryException and not StackOverflowException)
        {
            // Preparation is optional and read-only. An unexpected discovery failure must
            // never turn a successful primary appearance save into a failed primary save.
            var report = new AppearanceSyncReport();
            report.Add("自动存档形象同步准备未完成，形象保存可继续：" + ex.Message);
            return new(root, report, [], new Dictionary<string, AppliedAppearanceFile>(), null);
        }
    }

    private static AppearanceSyncSession PrepareCore(string root, string profileId, byte[] executableBytes,
        IReadOnlyList<PersonAppearanceUpdate> updates)
    {
        root = Path.GetFullPath(root);
        var report = new AppearanceSyncReport();
        var groups = new List<PreparedAppearanceSaveGroup>();
        var candidates = new Dictionary<string, AppliedAppearanceFile>(StringComparer.OrdinalIgnoreCase);
        var privateRoot = profileId switch { "ccz-6.4" => "xiaoan64", "ccz-6.5" => "xiaoan65", "ccz-6.6" => "xiaoan66", _ => null };
        var privatePath = privateRoot is null ? null : Path.Combine(root, "patch", privateRoot);
        var lockPath = privatePath is null ? null : Path.Combine(privatePath, "transactions", "root.lock");
        var session = new AppearanceSyncSession(root, report, groups, candidates, lockPath);
        var merged = new Dictionary<int, PersonAppearanceUpdate>();
        foreach (var update in updates)
        {
            if (update.PersonId is < 0 or >= 1024)
            {
                report.Add($"人物 {update.PersonId} 超出已验证的 0..1023 范围，其存档同步请求被忽略。");
                continue;
            }
            merged.TryGetValue(update.PersonId, out var old);
            merged[update.PersonId] = new(update.PersonId, update.RId ?? old?.RId, update.SId ?? old?.SId);
        }
        var changes = merged.Values.Where(item => item.RId.HasValue || item.SId.HasValue).ToArray();
        if (changes.Length == 0) return session;
        SaveAppearanceLayoutProbe.Layout layout;
        try { layout = SaveAppearanceLayoutProbe.Inspect(executableBytes, profileId); }
        catch (Exception ex) when (AppearanceSyncSession.IsFileFailure(ex) || ex is OverflowException)
        {
            report.Add("无法验证原生存档布局：" + ex.Message);
            layout = new(false, 0, 0, 0, 0, 0, ex.Message);
        }
        var saveDirectory = Path.Combine(root, "SV");
        IEnumerable<string> paths = Enumerate(saveDirectory, root, report, indexedAutosaves: false);
        if (privatePath is not null) paths = paths.Concat(Enumerate(Path.Combine(privatePath, "autosave"), root, report, indexedAutosaves: true));
        foreach (var path in paths.Distinct(StringComparer.OrdinalIgnoreCase).OrderBy(path => path, StringComparer.OrdinalIgnoreCase))
        {
            var relative = Path.GetRelativePath(root, path);
            try
            {
                if (!layout.Verified) throw new InvalidDataException("当前 EXE 没有通过原生存档布局验证：" + layout.Evidence);
                EnsureRegularInside(root, path);
                var before = ReadBounded(path, 128 * 1024 * 1024);
                var nativeLength = SaveAppearanceFormats.ValidateSave(before, layout.PrefixLength);
                var after = (byte[])before.Clone();
                var fields = 0;
                foreach (var update in changes)
                {
                    Apply(update.PersonId, layout.ROffset, update.RId);
                    Apply(update.PersonId, layout.SOffset, update.SId);
                }
                if (fields == 0) { report.UnchangedSaves++; continue; }
                SaveAppearanceFormats.UpdateEmbeddedHash(after, nativeLength);
                SaveAppearanceFormats.ValidateSave(after, layout.PrefixLength);
                var beforeHash = HashService.Sha256(before); var afterHash = HashService.Sha256(after);
                var files = new List<PreparedFileEdit>();
                var local = new List<AppliedAppearanceFile>();
                Add(path, before, after, bytes => SaveAppearanceFormats.ValidateSave(bytes, layout.PrefixLength));
                var stem = Path.GetFileNameWithoutExtension(path);
                var beside = Path.ChangeExtension(path, ".stats");
                var sidecars = new List<string> { beside };
                if (Path.GetDirectoryName(path)!.Equals(saveDirectory, StringComparison.OrdinalIgnoreCase) && privatePath is not null)
                    sidecars.Add(Path.Combine(privatePath, "save-index", stem + ".stats"));
                foreach (var sidecar in sidecars.Distinct(StringComparer.OrdinalIgnoreCase).Where(File.Exists))
                {
                    EnsureRegularInside(root, sidecar);
                    var statsBefore = ReadBounded(sidecar, 1024 * 1024);
                    var statsAfter = SaveAppearanceFormats.UpdateSidecar(statsBefore, beforeHash, afterHash);
                    Add(sidecar, statsBefore, statsAfter, bytes => SaveAppearanceFormats.UpdateSidecar(bytes, afterHash, afterHash));
                }
                var indexes = new List<string> { Path.ChangeExtension(path, ".ini") };
                if (Path.GetDirectoryName(path)!.Equals(saveDirectory, StringComparison.OrdinalIgnoreCase) && privatePath is not null)
                    indexes.Add(Path.Combine(privatePath, "save-index", stem + ".ini"));
                foreach (var index in indexes.Distinct(StringComparer.OrdinalIgnoreCase).Where(File.Exists))
                {
                    EnsureRegularInside(root, index);
                    var indexBefore = ReadBounded(index, 1024 * 1024);
                    var requireHash = !Path.GetDirectoryName(path)!.Equals(saveDirectory, StringComparison.OrdinalIgnoreCase);
                    var indexAfter = SaveAppearanceFormats.UpdateIni(indexBefore, beforeHash, afterHash, requireHash);
                    if (!indexBefore.AsSpan().SequenceEqual(indexAfter))
                        Add(index, indexBefore, indexAfter, bytes => SaveAppearanceFormats.UpdateIni(bytes, afterHash, afterHash, requireHash));
                }
                foreach (var file in local) candidates.Add(file.RelativePath, file);
                groups.Add(new(relative, files) { UpdatedPersonFields = fields });

                void Apply(int personId, int start, ushort? value)
                {
                    if (!value.HasValue) return;
                    var offset = checked(start + personId * 2);
                    if (offset < 0 || offset > layout.PrefixLength - 2) throw new InvalidDataException("形象数组超出已验证的原生首段。");
                    if (BinaryPrimitives.ReadUInt16LittleEndian(after.AsSpan(offset, 2)) == value.Value) return;
                    BinaryPrimitives.WriteUInt16LittleEndian(after.AsSpan(offset, 2), value.Value); fields++;
                }
                void Add(string filePath, byte[] original, byte[] candidate, Action<byte[]> verifier)
                {
                    var fileRelative = Path.GetRelativePath(root, filePath);
                    files.Add(new(fileRelative, HashService.Sha256(original), candidate, "存档形象同步", "同步本次人物 R/S 形象及关联统计校验", verifier));
                    local.Add(new(fileRelative, original, (byte[])candidate.Clone(), File.GetAttributes(filePath), BuildChange(fileRelative, original, candidate)));
                }
            }
            catch (Exception ex) when (AppearanceSyncSession.IsFileFailure(ex) || ex is OverflowException)
            {
                report.SkippedSaves++;
                report.Add($"{relative}：未同步，{ex.Message}");
            }
        }
        return session;
    }

    private static IReadOnlyList<string> Enumerate(string directory, string root, AppearanceSyncReport report, bool indexedAutosaves)
    {
        if (!Directory.Exists(directory)) return [];
        try
        {
            EnsureRegularInside(root, directory);
            var files = Directory.EnumerateFiles(directory);
            if (indexedAutosaves)
                return files.Where(path => Path.GetExtension(path).Equals(".ini", StringComparison.OrdinalIgnoreCase))
                    .Select(path => Path.ChangeExtension(path, ".E5S")).Where(File.Exists).ToArray();
            // The native filename uses %03u (minimum width, not a three-digit cap).
            return files.Where(path => Regex.IsMatch(Path.GetFileName(path), @"^SV[0-9]{3,}\.E5S$", RegexOptions.IgnoreCase)).ToArray();
        }
        catch (Exception ex) when (AppearanceSyncSession.IsFileFailure(ex))
        {
            report.Add($"{Path.GetRelativePath(root, directory)}：无法枚举存档，{ex.Message}");
            return [];
        }
    }

    private static void EnsureRegularInside(string root, string path)
    {
        var fullRoot = Path.TrimEndingDirectorySeparator(Path.GetFullPath(root)) + Path.DirectorySeparatorChar;
        var full = Path.GetFullPath(path);
        if (!full.StartsWith(fullRoot, StringComparison.OrdinalIgnoreCase)) throw new IOException("存档路径超出当前游戏目录。");
        for (var current = full; current.Length >= fullRoot.Length; current = Path.GetDirectoryName(current)!)
        {
            if ((File.GetAttributes(current) & FileAttributes.ReparsePoint) != 0) throw new IOException("不自动同步符号链接或重定向目录中的存档。");
        }
    }

    private static byte[] ReadBounded(string path, int maximum)
    {
        using var stream = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read);
        if (stream.Length > maximum) throw new InvalidDataException("文件超过已支持的存档格式长度上限。");
        var bytes = new byte[checked((int)stream.Length)];
        stream.ReadExactly(bytes);
        return bytes;
    }

    private static FileByteChange BuildChange(string relative, byte[] before, byte[] after)
    {
        var chunks = new List<ByteChunk>();
        var offset = 0;
        while (offset < before.Length)
        {
            if (before[offset] == after[offset]) { offset++; continue; }
            var start = offset++;
            while (offset < before.Length && before[offset] != after[offset]) offset++;
            chunks.Add(new(start, before.AsSpan(start, offset - start).ToArray(), after.AsSpan(start, offset - start).ToArray()));
        }
        return new(relative, HashService.Sha256(before), HashService.Sha256(after), after.Length, chunks);
    }
}
