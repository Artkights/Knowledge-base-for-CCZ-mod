using System.Buffers.Binary;
using System.Text;
using DataManager.Core.Appearance;
using DataManager.Core.Binary;
using DataManager.Core.Models;

namespace DataManager.Tests;

internal static class SaveAppearanceSyncTests
{
    public static void Run(string basePath)
    {
        var source = ResolveBase(basePath);
        NativeFieldsAndScope(source);
        StatisticsAndEncodings(source);
        RejectionAndIndependentGroups(source);
        LateFailureAndRollbackConflict(source);
        AutomaticSavesAndDirectoryLock(source);
        RealEmbeddedStatistics(source);
        Console.WriteLine("SAVE_APPEARANCE_SYNC_OK");
    }

    private static string ResolveBase(string path)
    {
        if (File.Exists(Path.Combine(path, "Ekd5.exe"))) return path;
        var candidate = Path.Combine(path, "基底", "加强版6.5未加密版");
        if (!File.Exists(Path.Combine(candidate, "Ekd5.exe"))) throw new DirectoryNotFoundException("缺少真实 6.5 存档同步测试基底。");
        return candidate;
    }

    private static void NativeFieldsAndScope(string source)
    {
        WithFixture(source, (root, executable, native) =>
        {
            var path = Put(root, "SV/SV001.E5S", native);
            var metadata = Encoding.ASCII.GetBytes("slot metadata"); Put(root, "SV/SV.E5S", metadata);
            Put(root, "SV/backup/SV001.E5S", native);
            var session = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", executable,
                [new(0, 600, 601), new(1, SId: 0)]);
            TestSupport.Assert(session.PreparedGroups.Count == 1 && File.ReadAllBytes(path).AsSpan().SequenceEqual(native), "Prepare必须只读，且只枚举活动存档。");
            session.Commit();
            var after = File.ReadAllBytes(path);
            AssertWord(after, 0xE800, 600); AssertWord(after, 0, 601); AssertWord(after, 2, 0);
            TestSupport.Assert(Differences(native, after).All(index => index is 0 or 1 or 2 or 3 or 0xE800 or 0xE801), "同步修改了本次人物/字段以外的字节。");
            TestSupport.Assert(File.ReadAllBytes(Path.Combine(root, "SV", "SV.E5S")).AsSpan().SequenceEqual(metadata) &&
                File.ReadAllBytes(Path.Combine(root, "SV", "backup", "SV001.E5S")).AsSpan().SequenceEqual(native), "同步误改元信息或备份目录。");
            TestSupport.Assert(session.Report.UpdatedSaves == 1 && session.Report.UpdatedPersonFields == 3 && session.AppliedFiles.Count == 1, "同步计数或历史贡献错误。");
            session.Commit();
            TestSupport.Assert(session.Report.UpdatedSaves == 1, "同一session重复Commit造成重复写入。");
            var noop = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", executable, [new(0, 600, 601), new(1, SId: 0)]);
            noop.Commit();
            TestSupport.Assert(noop.PreparedGroups.Count == 0 && noop.Report.UnchangedSaves == 1 && noop.AppliedFiles.Count == 0, "已一致的存档不应重复写入。");
            session.Rollback();
            TestSupport.Assert(File.ReadAllBytes(path).AsSpan().SequenceEqual(native) && session.AppliedFiles.Count == 0, "Rollback未逐字节恢复原存档。");
        });
    }

    private static void StatisticsAndEncodings(string source)
    {
        Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
        var encodings = new[] { new UTF8Encoding(false), new UTF8Encoding(true), new UnicodeEncoding(false, true),
            new UnicodeEncoding(true, true), Encoding.GetEncoding(936) };
        foreach (var encoding in encodings)
        WithFixture(source, (root, executable, native) =>
        {
            var save = Put(root, "SV/SV001.E5S", native);
            var sidecarBefore = EmptySidecar(HashService.Sha256(native));
            var sidecar = Put(root, "patch/xiaoan65/save-index/SV001.stats", sidecarBefore);
            var text = "; 保留中文、空格和注释\r\n[Save]\r\n  Hash = " + HashService.Sha256(native) + " ; 校验\r\n[User]\r\nNote=保持原样\r\n";
            var indexBefore = encoding.GetPreamble().Concat(encoding.GetBytes(text)).ToArray();
            var index = Put(root, "patch/xiaoan65/save-index/SV001.ini", indexBefore);
            File.SetAttributes(sidecar, File.GetAttributes(sidecar) | FileAttributes.ReadOnly);
            var originalAttributes = File.GetAttributes(sidecar);
            var session = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", executable, [new(0, SId: 501)]);
            session.Commit();
            TestSupport.Assert(session.Report.UpdatedSaves == 1 && session.AppliedFiles.Count == 3, "schema1/索引组同步失败：" + string.Join("；", session.Report.Diagnostics));
            var afterSave = File.ReadAllBytes(save);
            var afterStats = File.ReadAllBytes(sidecar);
            TestSupport.Assert(Encoding.ASCII.GetString(afterStats, 32, 64) == HashService.Sha256(afterSave).ToLowerInvariant() &&
                Differences(sidecarBefore, afterStats).All(index => index is >= 32 and < 96), "schema1历史数据或小写哈希错误。");
            var expectedText = text.Replace(HashService.Sha256(native), HashService.Sha256(afterSave), StringComparison.Ordinal);
            var expectedBytes = encoding.GetPreamble().Concat(encoding.GetBytes(expectedText)).ToArray();
            TestSupport.Assert(File.ReadAllBytes(index).AsSpan().SequenceEqual(expectedBytes), "INI编码、BOM、注释、换行或用户内容未保留。");
            TestSupport.Assert(File.GetAttributes(sidecar) == originalAttributes, "同步未恢复只读属性。");
            session.Rollback();
            TestSupport.Assert(File.ReadAllBytes(save).AsSpan().SequenceEqual(native) && File.ReadAllBytes(sidecar).AsSpan().SequenceEqual(sidecarBefore) &&
                File.ReadAllBytes(index).AsSpan().SequenceEqual(indexBefore) && File.GetAttributes(sidecar) == originalAttributes,
                "统计保存组Rollback未恢复全部字节和属性。");
        });
    }

    private static void RejectionAndIndependentGroups(string source)
    {
        WithFixture(source, (root, executable, native) =>
        {
            var good = Put(root, "SV/SV001.E5S", native);
            var occupied = Put(root, "SV/SV002.E5S", native);
            var corrupt = (byte[])native.Clone(); corrupt[0x30000] = 0; Put(root, "SV/SV003.E5S", corrupt);
            Put(root, "SV/SV004.E5S", native.Concat(new byte[] { 0x77 }).ToArray());
            Put(root, "SV/SV005.E5S", native);
            Put(root, "patch/xiaoan65/save-index/SV005.stats", EmptySidecar(new string('0', 64)));
            var outside = Put(root, "SV/SV006.E5S", native);
            var session = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", executable, [new(0, RId: 700)]);
            var external = (byte[])native.Clone(); external[0x9000] ^= 0x5A; File.WriteAllBytes(outside, external);
            using (var locked = new FileStream(occupied, FileMode.Open, FileAccess.ReadWrite, FileShare.None)) session.Commit();
            TestSupport.Assert(session.Report.UpdatedSaves == 1 && session.Report.SkippedSaves == 5 && session.Report.Summary.Contains("部分同步"),
                "坏档/占用/外改未逐档跳过并继续：" + session.Report.Summary + string.Join("；", session.Report.Diagnostics));
            AssertWord(File.ReadAllBytes(good), 0xE800, 700);
            TestSupport.Assert(File.ReadAllBytes(occupied).AsSpan().SequenceEqual(native) && File.ReadAllBytes(outside).AsSpan().SequenceEqual(external) &&
                File.ReadAllBytes(Path.Combine(root, "SV", "SV005.E5S")).AsSpan().SequenceEqual(native), "失败组或外部内容被覆盖。");
            var unavailable = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", new byte[100], [new(0, RId: 701)]);
            unavailable.Commit();
            TestSupport.Assert(unavailable.Report.SkippedSaves == 6 && unavailable.AppliedFiles.Count == 0, "布局未验证时仍改写了存档。");
        });
    }

    private static void LateFailureAndRollbackConflict(string source)
    {
        WithFixture(source, (root, executable, native) =>
        {
            var save = Put(root, "SV/SV001.E5S", native);
            var beforeStats = EmptySidecar(HashService.Sha256(native));
            var stats = Put(root, "patch/xiaoan65/save-index/SV001.stats", beforeStats);
            var session = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", executable, [new(0, SId: 800)]);
            var second = session.PreparedGroups.Single().Files[1];
            var originalVerifier = second.CandidateVerifier;
            var calls = 0;
            // Exercise the existing before/after semantic-verifier boundary without adding a production fault API.
            typeof(PreparedFileEdit).GetProperty(nameof(PreparedFileEdit.CandidateVerifier))!.SetValue(second, (Action<byte[]>)(bytes =>
            {
                originalVerifier?.Invoke(bytes);
                if (++calls == 2) throw new InvalidDataException("测试：统计成员写后失败");
            }));
            session.Commit();
            TestSupport.Assert(calls == 2 && session.Report.SkippedSaves == 1 && session.Report.UpdatedSaves == 0 && session.AppliedFiles.Count == 0 &&
                File.ReadAllBytes(save).AsSpan().SequenceEqual(native) && File.ReadAllBytes(stats).AsSpan().SequenceEqual(beforeStats),
                "第二成员写后失败没有恢复整个存档组。");
            var retry = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", executable, [new(0, SId: 800)]);
            retry.Commit();
            var after = File.ReadAllBytes(save); var external = (byte[])after.Clone(); external[0x9000] ^= 0xA5;
            File.WriteAllBytes(save, external);
            var conflict = false;
            try { retry.Rollback(); } catch (IOException ex) { conflict = ex.Message.Contains("外部"); }
            TestSupport.Assert(conflict && retry.AppliedFiles.Count == 2 && File.ReadAllBytes(save).AsSpan().SequenceEqual(external),
                "Rollback冲突未保留外部内容或丢失恢复快照。");
            TestSupport.Assert(retry.RecoverySnapshotDirectory is { } recovery && File.Exists(Path.Combine(recovery, "manifest.json")) &&
                !DataManager.Core.History.ProjectHistoryPaths.IsInside(recovery, root) &&
                File.ReadAllBytes(Path.Combine(recovery, "0000.before.bin")).AsSpan().SequenceEqual(native) &&
                File.ReadAllBytes(Path.Combine(recovery, "0000.after.bin")).AsSpan().SequenceEqual(after),
                "恢复冲突没有在原基底以外持久保存可复核的原始/候选快照与manifest。");
            File.WriteAllBytes(save, after); retry.Rollback();
            TestSupport.Assert(File.ReadAllBytes(save).AsSpan().SequenceEqual(native) && File.ReadAllBytes(stats).AsSpan().SequenceEqual(beforeStats), "冲突解除后无法恢复保存组。");
        });
    }

    private static void RealEmbeddedStatistics(string source)
    {
        var repository = TestSupport.RepositoryRootFromBase(source);
        var realRoot = Path.Combine(repository, "基底", "复刻版6.6山贼 国庆");
        var sourceSave = Path.Combine(realRoot, "SV", "SV000.E5S");
        if (!File.Exists(sourceSave)) throw new FileNotFoundException("缺少真实schema2统计存档测试样本。", sourceSave);
        var originalSourceHash = HashService.Sha256(sourceSave);
        var before = File.ReadAllBytes(sourceSave);
        var temporary = CreateTemporary();
        try
        {
            var save = Put(temporary, "SV/SV000.E5S", before);
            var executable = File.ReadAllBytes(Path.Combine(realRoot, "Ekd5.exe"));
            var session = SaveAppearanceSyncService.Prepare(temporary, "ccz-6.6", executable, [new(0, RId: 900, SId: 901)]);
            session.Commit();
            TestSupport.Assert(session.Report.UpdatedSaves == 1, "真实schema2档不能同步：" + string.Join("；", session.Report.Diagnostics));
            var after = File.ReadAllBytes(save); var footer = after.Length - 168;
            TestSupport.Assert(Encoding.ASCII.GetString(after, footer + 32, 64) == HashService.Sha256(after[..0x43A86]) &&
                Differences(before, after).All(index => index is 0 or 1 or 0xE800 or 0xE801 || index >= footer + 32 && index < footer + 96),
                "schema2统计payload、非形象原生字段或大写哈希被误改。");
            session.Rollback();
            TestSupport.Assert(File.ReadAllBytes(save).AsSpan().SequenceEqual(before), "schema2回滚没有恢复完整原文件。");
            var broken = (byte[])before.Clone(); broken[^80] ^= 1; File.WriteAllBytes(save, broken);
            var rejected = SaveAppearanceSyncService.Prepare(temporary, "ccz-6.6", executable, [new(0, SId: 901)]);
            rejected.Commit();
            TestSupport.Assert(rejected.Report.SkippedSaves == 1 && File.ReadAllBytes(save).AsSpan().SequenceEqual(broken), "损坏schema2仍被修改。");
        }
        finally { DeleteTemporary(temporary); }
        TestSupport.Assert(HashService.Sha256(sourceSave) == originalSourceHash, "实档测试污染了原基底。");
    }

    private static void AutomaticSavesAndDirectoryLock(string source)
    {
        WithFixture(source, (root, executable, native) =>
        {
            var auto = Put(root, "patch/xiaoan65/autosave/start-001.E5S", native);
            var indexBefore = Encoding.UTF8.GetBytes("[Save]\nHash=" + HashService.Sha256(native) + "\n[User]\nNote=自动档\n");
            var index = Put(root, "patch/xiaoan65/autosave/start-001.ini", indexBefore);
            var blocked = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", executable, [new(0, RId: 950)]);
            // A plugin may create its first transaction lock after preparation.
            var lockPath = Put(root, "patch/xiaoan65/transactions/root.lock", []);
            using (var held = new FileStream(lockPath, FileMode.Open, FileAccess.ReadWrite, FileShare.None))
            {
                blocked.Commit(); blocked.Rollback();
                TestSupport.Assert(blocked.Report.SkippedSaves == 1 && blocked.AppliedFiles.Count == 0 && File.ReadAllBytes(auto).AsSpan().SequenceEqual(native),
                    "已有小暗目录锁未阻止自动档同步，或空Rollback尝试操作文件。");
            }
            var session = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", executable, [new(0, RId: 950)]);
            session.Commit();
            TestSupport.Assert(session.Report.UpdatedSaves == 1 && session.AppliedFiles.Count == 2 &&
                Encoding.UTF8.GetString(File.ReadAllBytes(index)).Contains(HashService.Sha256(File.ReadAllBytes(auto))) &&
                !File.Exists(Path.ChangeExtension(auto, ".stats")), "自动档或同名索引未同步，或错误创建缺失统计旁文件。");
            session.Rollback();
            TestSupport.Assert(File.ReadAllBytes(auto).AsSpan().SequenceEqual(native) && File.ReadAllBytes(index).AsSpan().SequenceEqual(indexBefore), "自动档组不能恢复原始字节。");
            var orphan = Put(root, "patch/xiaoan65/autosave/orphan.E5S", native);
            var broken = Put(root, "patch/xiaoan65/autosave/end-001.E5S", native);
            Put(root, "patch/xiaoan65/autosave/end-001.ini", Encoding.UTF8.GetBytes("[Save]\nTurn=1\n"));
            var ordinary = Put(root, "SV/SV001.E5S", native);
            var note = Encoding.UTF8.GetBytes("[User]\nNote=普通存档合法注释\n");
            Put(root, "patch/xiaoan65/save-index/SV001.ini", note);
            var backup = Put(root, "SV/SV001.backup.E5S", native);
            var scoped = SaveAppearanceSyncService.Prepare(root, "ccz-6.5", executable, [new(0, RId: 950)]);
            scoped.Commit();
            TestSupport.Assert(scoped.Report.UpdatedSaves == 2 && scoped.Report.SkippedSaves == 1 &&
                File.ReadAllBytes(orphan).AsSpan().SequenceEqual(native) && File.ReadAllBytes(backup).AsSpan().SequenceEqual(native) &&
                File.ReadAllBytes(broken).AsSpan().SequenceEqual(native) &&
                File.ReadAllBytes(Path.Combine(root, "patch", "xiaoan65", "save-index", "SV001.ini")).AsSpan().SequenceEqual(note),
                "自动档孤立文件、备份命名、缺Hash索引或普通User注释边界错误。");
            AssertWord(File.ReadAllBytes(ordinary), 0xE800, 950);
        });
    }

    private static byte[] EmptySidecar(string saveHash)
    {
        var bytes = new byte[96]; "XA66STAT"u8.CopyTo(bytes); BinaryPrimitives.WriteUInt32LittleEndian(bytes.AsSpan(8), 1);
        Encoding.ASCII.GetBytes(saveHash.ToLowerInvariant()).CopyTo(bytes, 32); return bytes;
    }

    private static void WithFixture(string source, Action<string, byte[], byte[]> action)
    {
        var root = CreateTemporary();
        var save = Path.Combine(source, "SV", "SV001.E5S");
        var exe = Path.Combine(source, "Ekd5.exe");
        var beforeSaveHash = HashService.Sha256(save); var beforeExeHash = HashService.Sha256(exe);
        try { action(root, File.ReadAllBytes(exe), File.ReadAllBytes(save)); }
        finally { DeleteTemporary(root); }
        TestSupport.Assert(HashService.Sha256(save) == beforeSaveHash && HashService.Sha256(exe) == beforeExeHash, "隔离测试修改了原基底。");
    }

    private static string CreateTemporary()
    {
        var root = Path.Combine(Path.GetTempPath(), "DataManagerAppearanceSync_" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(root); return root;
    }
    private static string Put(string root, string relative, byte[] bytes)
    {
        var path = Path.Combine(root, relative.Replace('/', Path.DirectorySeparatorChar));
        Directory.CreateDirectory(Path.GetDirectoryName(path)!); File.WriteAllBytes(path, bytes); return path;
    }
    private static void DeleteTemporary(string root)
    {
        foreach (var file in Directory.EnumerateFiles(root, "*", SearchOption.AllDirectories)) File.SetAttributes(file, FileAttributes.Normal);
        Directory.Delete(root, true);
    }
    private static IEnumerable<int> Differences(byte[] before, byte[] after)
    {
        TestSupport.Assert(before.Length == after.Length, "定长同步改变了文件长度。");
        return Enumerable.Range(0, before.Length).Where(index => before[index] != after[index]);
    }
    private static void AssertWord(byte[] bytes, int offset, ushort value)
        => TestSupport.Assert(BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(offset, 2)) == value, $"形象字段0x{offset:X}不是{value}。");
}
