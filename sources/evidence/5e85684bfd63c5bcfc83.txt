using System.Buffers.Binary;
using System.Drawing;
using System.Drawing.Imaging;
using System.Security.Cryptography;
using System.Text.Json;
using ImageManager.Core;

namespace ImageManager.Tests;

internal static class SceneTerrainTests
{
    private static readonly List<string> Checks = [];

    public static void Run(string repositoryRoot)
    {
        var repo = Path.GetFullPath(repositoryRoot);
        var output = Path.Combine(repo, "data管理器", "验证", "2026-10-23-内场景地形编辑", "core");
        Directory.CreateDirectory(output);
        var temp = Path.Combine(output, ".work-core-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(temp);
        try
        {
            CheckCodec();
            CheckGeometry();
            var exe = Path.Combine(repo, "基底", "加强版6.5未加密版", "Ekd5.exe");
            CheckEditingAndTransactions(temp, exe);
            CheckPairMutations(temp, exe);
            CheckLastPairRemoval(temp, exe);
            var real = new[]
            {
                CheckRealSample(repo, temp, output, "6.4", "洗隋", ProjectVersion.Ccz64),
                CheckRealSample(repo, temp, output, "6.5", "加强版6.5未加密版", ProjectVersion.Ccz65),
                CheckRealSample(repo, temp, output, "6.6", "新改曹操傳6.6修正版", ProjectVersion.Ccz66),
                CheckRealSample(repo, temp, output, "6.6山贼", "复刻版6.6山贼", ProjectVersion.Ccz66)
            };
            File.WriteAllText(Path.Combine(output, "scene-terrain-core-results.json"), JsonSerializer.Serialize(new
            {
                Passed = true, Checks, RealSamples = real,
                CoordinateEvidence = new
                {
                    PixelToGame = "floor(px/16+py/8+4.625),floor(py/8-px/16+46.625)",
                    GameToFile = "(gameX,gameY-2)",
                    FileCellCenter = "(8*(fileX-fileY+40),4*(fileX+fileY-48)-1)",
                    Old65MouseVA = "0x53F688-0x53F78C", Old65WriteVA = "0x53EF99-0x53F067",
                    Old66MouseVA = "0x54ECBE-0x54EDB6", Old66WriteVA = "0x54E5D9-0x54E655"
                }
            }, new JsonSerializerOptions { WriteIndented = true }));
            Console.WriteLine("SCENE_TERRAIN_TESTS_OK " + output);
        }
        finally
        {
            foreach (var path in Directory.EnumerateFiles(temp, "*", SearchOption.AllDirectories)) File.SetAttributes(path, FileAttributes.Normal);
            Directory.Delete(temp, true);
        }
    }

    private static void CheckCodec()
    {
        var bytes = Payload();
        BinaryPrimitives.WriteUInt16LittleEndian(bytes.AsSpan(16 + 2 * (21 * 100 + 17), 2), 0xF0FF);
        var decoded = PmapTerrainCodec.Decode(bytes);
        Require(decoded.Width == 100 && decoded.Height == 100 && decoded.Layers == 1 && decoded.CanEdit, "100x100 UInt16 Pmap未识别");
        Require(decoded.GetCell(17, 21) == 0xF0FF && decoded.GetCell(18, 21) == 0xFFFF, "Pmap行列或大小端错误");
        Equal(bytes, PmapTerrainCodec.Encode(decoded), "未改Pmap编码不能逐字节往返");
        var cells = decoded.Cells.ToArray(); cells[21 * 100 + 18] = 0xF0FF;
        var edited = PmapTerrainCodec.Encode(decoded, cells);
        Require(Enumerable.Range(0, bytes.Length).Where(index => bytes[index] != edited[index]).SequenceEqual(new[] { 16 + 2 * (21 * 100 + 18) + 1 }), "编辑单格改动了头部、低字节或其他格");
        foreach (var invalid in new[] { bytes[..^1], bytes.Concat(new byte[] { 0 }).ToArray(), new byte[16], UnknownPayload() })
        {
            var blocked = false;
            try { blocked = !PmapTerrainCodec.Decode(invalid).CanEdit; }
            catch (InvalidDataException) { blocked = true; }
            Require(blocked, "损坏长度或未知低字节未拒绝编辑");
        }
        var layered = new byte[40016]; bytes[..16].CopyTo(layered, 0);
        BinaryPrimitives.WriteUInt16LittleEndian(layered.AsSpan(6, 2), 2); Array.Fill(layered, (byte)0xFF, 16, 40000);
        var safe = false;
        try { safe = !PmapTerrainCodec.Decode(layered).CanEdit; }
        catch (InvalidDataException) { safe = true; }
        Require(safe, "多层Pmap未经验证就允许单层画笔");
        Require(PmapTerrainCodec.Decode(PmapTerrainCodec.CreateDefault()).CanEdit, "默认新地形模板不可编辑");
        Checks.Add("真实头字段、UInt16行主序、单字节差异、损坏/未知值/多层拒写");
    }

    private static void CheckGeometry()
    {
        var geometry = new DiamondTerrainGeometry();
        // This expected phase comes from both old tool binaries, not from the implementation.
        foreach (var cell in new[] { new Point(4, 44), new Point(25, 35), new Point(60, 50), new Point(92, 52) })
        {
            var expected = new PointF(8 * (cell.X - cell.Y + 40), 4 * (cell.X + cell.Y - 48) - 1);
            Require(geometry.CellCenter(cell.X, cell.Y) == expected, "菱形中心相位偏移");
            if (expected.Y >= 0 && expected.X >= 0 && expected.X < 640 && expected.Y < 400)
            {
                Require(geometry.HitTest(expected) == cell, "格中心无法命中自身");
                foreach (var delta in new[] { new PointF(0, 3.9f), new PointF(0, -3.9f), new PointF(7.9f, 0), new PointF(-7.9f, 0) })
                    Require(geometry.HitTest(new PointF(expected.X + delta.X, expected.Y + delta.Y)) == cell, "菱形边界内命中错格");
            }
        }
        var center = geometry.CellCenter(25, 35);
        Require(geometry.HitTest(new PointF(center.X + 4.1f, center.Y + 2.1f)) == new Point(26, 35), "右下菱形边界外没有换格");
        Require(geometry.HitTest(new PointF(center.X - 4.1f, center.Y + 2.1f)) == new Point(25, 36), "左下菱形边界外没有换格");
        Require(geometry.HitTest(new PointF(-1, 20)) == null && geometry.HitTest(new PointF(640, 20)) == null && geometry.HitTest(new PointF(20, 400)) == null, "图片外仍命中可写格");
        Require(geometry.FileToGame(new Point(25, 35)) == new Point(25, 37) && geometry.GameToFile(new Point(25, 37)) == new Point(25, 35), "文件行与游戏坐标Y-2转换不一致");
        var crossed = geometry.TraceCells(geometry.CellCenter(25, 35), geometry.CellCenter(65, 35));
        Require(Enumerable.Range(25, 41).All(x => crossed.Contains(new Point(x, 35))), "快速拖动跨格漏填");
        Require(geometry.CellPolygon(25, 35).Select(point => point.X).Max() - geometry.CellPolygon(25, 35).Select(point => point.X).Min() == 16, "网格不是16像素菱形");
        Checks.Add("旧工具相位、四个边界内外、画布外、文件/游戏坐标与快速跨格插值");
    }

    private static void CheckEditingAndTransactions(string temp, string exe)
    {
        var project = Fixture(Path.Combine(temp, "edit"), exe, 42, 3);
        var history = new HistoryService(Path.Combine(temp, "edit-history"));
        var mutations = new ImageMutationService(history);
        var service = new SceneTerrainService();
        using var document = service.Load(project, 41);
        Require(document.CanEdit && !document.IsDirty, "内场景初始编辑状态错误：" + document.Diagnostic);
        document.BeginStroke(); document.SetCell(25, 35, true); document.SetCell(26, 35, true); document.SetCell(25, 35, true);
        Require(document.EndStroke() && document.IsDirty && document.CanUndo, "画笔未合并为一个笔画");
        Require(document.Undo() && !document.IsDirty && document.GetCell(25, 35) == 0xFFFF && document.GetCell(26, 35) == 0xFFFF, "一次撤销未恢复整条笔画");
        Require(document.Redo() && document.GetCell(25, 35) == 0xF0FF && document.GetCell(26, 35) == 0xF0FF, "重做未恢复整条笔画");
        document.BeginStroke(); document.SetCell(25, 35, true); Require(!document.EndStroke(), "相同地形空笔画增加撤销步骤");
        var pmap = project.TryGetResource("Pmap.e5")!; var mmap = project.TryGetResource("Mmap.e5")!;
        var original = File.ReadAllBytes(pmap); var mmapHash = Hash(mmap);
        var plan = service.PlanEdit(project, document);
        Require(plan.Files.Count == 1 && Path.GetFullPath(plan.Files[0].TargetPath) == pmap, "仅地形编辑计划改动了Mmap或其他文件");
        var result = mutations.Commit(project, plan); Require(result.Success, "保存失败：" + string.Join(";", result.Diagnostics));
        service.AcceptSaved(project, document); Require(!document.IsDirty, "保存成功后未更新脏状态");
        Require(Hash(mmap) == mmapHash, "地形保存修改了背景档案");
        using (var reread = service.Load(project, 41)) Require(reread.GetCell(25, 35) == 0xF0FF, "地形保存后复读不一致");
        Require(history.List(project).Any(item => item.Id == result.HistoryId), "地形保存未落入真实资源历史");
        Require(history.Undo(project, result.HistoryId!).Success, "磁盘历史撤销失败"); Equal(original, File.ReadAllBytes(pmap), "历史撤销未恢复原档案");
        Require(history.Redo(project, result.HistoryId!).Success, "磁盘历史重做失败");
        using var stale = service.Load(project, 41); stale.SetCell(29, 35, true); var stalePlan = service.PlanEdit(project, stale);
        var external = File.ReadAllBytes(pmap); external[17] ^= 1; File.WriteAllBytes(pmap, external);
        Require(!mutations.Commit(project, stalePlan).Success, "过期地形会话覆盖外部修改"); Equal(external, File.ReadAllBytes(pmap), "冲突失败破坏外部文件");
        File.WriteAllBytes(pmap, original);
        using var rollback = service.Load(project, 41); rollback.SetCell(30, 35, true); var rollbackPlan = service.PlanEdit(project, rollback);
        var journal = Path.Combine(history.BackupRoot(project), "History", "history.jsonl");
        using (var locked = new FileStream(journal, FileMode.Open, FileAccess.Read, FileShare.Read))
            Require(!mutations.Commit(project, rollbackPlan).Success, "历史日志锁定时仍报告保存成功");
        Equal(original, File.ReadAllBytes(pmap), "历史持久化失败没有回滚地形文件");
        Require(rollback.IsDirty, "保存失败丢失未保存笔画");
        Checks.Add("笔画撤销重做、空笔画、只写Pmap、磁盘复读、资源历史、过期会话拒绝、日志失败回滚");
    }

    private static void CheckPairMutations(string temp, string exe)
    {
        var project = Fixture(Path.Combine(temp, "pairs"), exe, 42, 3);
        var service = new SceneTerrainService();
        var mmap = E5Archive.OpenFresh(project.TryGetResource("Mmap.e5")!);
        var pmap = E5Archive.OpenFresh(project.TryGetResource("Pmap.e5")!);
        var extra = pmap.ReadStored(3);
        var append = new MutationPlan(Guid.NewGuid().ToString("N"), MutationKind.Append, "新增场景",
            [new(project.TryGetResource("Mmap.e5")!, mmap.Rebuild(appendDecoded: [ImagePayload(Color.Green)]), "新增背景")], [], false);
        var paired = service.AugmentAppend(project, append);
        Require(paired.Files.Count == 2, "Mmap追加没有包含Pmap联动文件");
        var appendedPmap = Candidate(paired, "Pmap.e5");
        Require(appendedPmap.Entries.Count == 4, "追加Pmap数量错误");
        Equal(pmap.ReadStored(1), appendedPmap.ReadStored(1), "追加改动已有内场景1");
        Equal(pmap.ReadStored(2), appendedPmap.ReadStored(2), "追加改动已有内场景2");
        Equal(extra, appendedPmap.ReadStored(4), "新Pmap没有插在多余尾条目前");
        Require(PmapTerrainCodec.Decode(appendedPmap.ReadDecoded(3)).Cells.All(value => value == 0xFFFF), "新增场景默认地形不是全通行");
        var copied = service.AugmentAppend(project, append, 42);
        Equal(pmap.ReadDecoded(2), Candidate(copied, "Pmap.e5").ReadDecoded(3), "复制场景没有同时复制地形");
        var innerDelete = service.PlanDelete(project, [Asset(project, 41)]);
        Require(Candidate(innerDelete, "Mmap.e5").Entries.Count == 41 && Candidate(innerDelete, "Pmap.e5").Entries.Count == 2, "内场景删除没有同步缩短两档案");
        Equal(pmap.ReadStored(2), Candidate(innerDelete, "Pmap.e5").ReadStored(1), "内场景删除错位了后续配对");
        Equal(extra, Candidate(innerDelete, "Pmap.e5").ReadStored(2), "内场景删除丢失额外尾条目");
        var outsideDelete = service.PlanDelete(project, [Asset(project, 1)]);
        var outsideCandidate = Candidate(outsideDelete, "Mmap.e5");
        Require(outsideCandidate.Entries.Count == 42 && outsideDelete.Files.Count == 1, "外场景删除移动了固定前40槽或改动Pmap");
        using (var black = ImageRendering.DecodeStandardImage(outsideCandidate.ReadDecoded(1)))
            Require(black.Size == new Size(640, 400) && black.GetPixel(100, 100).ToArgb() == Color.Black.ToArgb(), "外场景没有同尺寸黑图占位");
        var history = new HistoryService(Path.Combine(temp, "pair-history")); var mutations = new ImageMutationService(history);
        var beforeM = File.ReadAllBytes(project.TryGetResource("Mmap.e5")!); var beforeP = File.ReadAllBytes(project.TryGetResource("Pmap.e5")!);
        var journal = Path.Combine(history.BackupRoot(project), "History", "history.jsonl"); Directory.CreateDirectory(Path.GetDirectoryName(journal)!); File.WriteAllText(journal, "");
        using (var locked = new FileStream(journal, FileMode.Open, FileAccess.Read, FileShare.Read))
            Require(!mutations.Commit(project, paired).Success, "双文件历史失败仍成功");
        Equal(beforeM, File.ReadAllBytes(project.TryGetResource("Mmap.e5")!), "联动失败没有回滚Mmap"); Equal(beforeP, File.ReadAllBytes(project.TryGetResource("Pmap.e5")!), "联动失败没有回滚Pmap");
        var committed = mutations.Commit(project, paired with { OperationId = Guid.NewGuid().ToString("N") }); Require(committed.Success, "双文件追加提交失败：" + string.Join(";", committed.Diagnostics));
        Require(history.Undo(project, committed.HistoryId!).Success, "双文件历史撤回失败");
        Equal(beforeM, File.ReadAllBytes(project.TryGetResource("Mmap.e5")!), "双文件历史撤回Mmap错误"); Equal(beforeP, File.ReadAllBytes(project.TryGetResource("Pmap.e5")!), "双文件历史撤回Pmap错误");
        Checks.Add("追加/复制配对、额外Pmap尾条目前插入、内场景同步删除、外场景黑图固定槽、双文件回滚和历史");
    }

    private static void CheckLastPairRemoval(string temp, string exe)
    {
        var project = Fixture(Path.Combine(temp, "last-pair"), exe, 41, 1);
        var pmapPath = project.TryGetResource("Pmap.e5")!;
        var original = E5Archive.OpenFresh(pmapPath); var blocked = Payload();
        BinaryPrimitives.WriteUInt16LittleEndian(blocked.AsSpan(16 + 2 * (35 * 100 + 25), 2), 0xF0FF);
        File.WriteAllBytes(pmapPath, original.Rebuild(replacementDecoded: new Dictionary<int, byte[]> { [1] = blocked }));
        var history = new HistoryService(Path.Combine(temp, "last-pair-history")); var mutations = new ImageMutationService(history);
        var service = new SceneTerrainService(); var delete = service.PlanDelete(project, [Asset(project, 41)]);
        Require(delete.Metadata?.GetValueOrDefault("SceneEmptyTailPlaceholder") == "v1", "最后内场景删除没有声明空尾预留");
        Require(mutations.Commit(project, delete).Success, "最后内场景删除提交失败");
        Require(E5Archive.OpenFresh(project.TryGetResource("Mmap.e5")!).Entries.Count == 40, "最后内场景删除后仍留有内场景图片");
        var empty = E5Archive.OpenFresh(pmapPath);
        Require(empty.Entries.Count == 1 && PmapTerrainCodec.Decode(empty.ReadDecoded(1)).Cells.All(cell => cell == 0xFFFF), "最后内场景删除未保留全通行预留，或旧障碍遗留");
        var mmap = E5Archive.OpenFresh(project.TryGetResource("Mmap.e5")!);
        var append = new MutationPlan(Guid.NewGuid().ToString("N"), MutationKind.Append, "重新新增场景",
            [new(project.TryGetResource("Mmap.e5")!, mmap.Rebuild(appendDecoded: [ImagePayload(Color.Gray)]), "新增背景")], [], false);
        var paired = service.AugmentAppend(project, append);
        Require(mutations.Commit(project, paired).Success, "删除最后内场景后重新新增失败");
        var next = E5Archive.OpenFresh(pmapPath);
        Require(next.Entries.Count == 2 && PmapTerrainCodec.Decode(next.ReadDecoded(1)).Cells.All(cell => cell == 0xFFFF), "重新新增没有在预留条目前插入全通行配对");
        Equal(empty.ReadStored(1), next.ReadStored(2), "重新新增没有保留并后移尾部预留");
        Checks.Add("最后内场景删除保留全FFFF尾部预留；重新新增在预留前插入且旧障碍不复活");
    }

    private static object CheckRealSample(string repo, string temp, string output, string version, string relative, ProjectVersion expected)
    {
        var source = Path.Combine(repo, "基底", relative);
        var detected = new ProjectProfileService().Detect(source);
        Require(detected.Version == expected, "真实样本版本识别错误：" + source);
        var sourcePaths = new[] { "Ekd5.exe", "Mmap.e5", "Pmap.e5" }.ToDictionary(key => key, key => detected.TryGetResource(key) ?? throw new InvalidDataException("真实样本缺少" + key));
        var hashes = sourcePaths.ToDictionary(pair => pair.Key, pair => Hash(pair.Value));
        var destination = Path.Combine(temp, version); Directory.CreateDirectory(destination);
        var copied = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        foreach (var pair in sourcePaths) { copied[pair.Key] = Path.Combine(destination, pair.Key); File.Copy(pair.Value, copied[pair.Key]); }
        var project = new ProjectProfile(destination, version + "地形副本", expected, false, copied, []);
        var engine = File.ReadAllBytes(copied["Ekd5.exe"]);
        var blockedSignature = Convert.FromHexString("2500FF00003D00F00000");
        var indexSignature = Convert.FromHexString("03C2034508D1E083C010");
        var blockedAt = Find(engine, blockedSignature); var indexAt = Find(engine, indexSignature);
        Require(blockedAt >= 0 && indexAt >= 0, "真实引擎缺少已确认UInt16索引/高字节障碍消费者");
        var mmap = E5Archive.OpenFresh(copied["Mmap.e5"]); var pmap = E5Archive.OpenFresh(copied["Pmap.e5"]);
        var service = new SceneTerrainService();
        using var doc = service.Load(project, 42);
        Require(doc.CanEdit && doc.MmapImageNumber == 42 && doc.PmapImageNumber == 2, "真实内场景配对/可编辑状态错误：" + doc.Diagnostic);
        var before = File.ReadAllBytes(copied["Pmap.e5"]); var beforeArchive = E5Archive.Parse("before.e5", before);
        var original = doc.GetCell(25, 35); doc.SetCell(25, 35, original != 0xF0FF);
        var plan = service.PlanEdit(project, doc); var history = new HistoryService(Path.Combine(temp, "history-" + version));
        var result = new ImageMutationService(history).Commit(project, plan); Require(result.Success, "真实地形副本保存失败：" + string.Join(";", result.Diagnostics));
        var afterArchive = E5Archive.OpenFresh(copied["Pmap.e5"]);
        foreach (var entry in beforeArchive.Entries.Where(entry => entry.ImageNumber != 2))
            Equal(beforeArchive.ReadStored(entry.ImageNumber), afterArchive.ReadStored(entry.ImageNumber), "真实保存重写了未改动压缩条目：" + entry.ImageNumber);
        var originalDecoded = beforeArchive.ReadDecoded(2); var afterDecoded = afterArchive.ReadDecoded(2);
        Require(Enumerable.Range(0, originalDecoded.Length).Where(at => originalDecoded[at] != afterDecoded[at]).SequenceEqual(new[] { 16 + (35 * 100 + 25) * 2 + 1 }), "真实保存没有只改目标高字节");
        Require(history.Undo(project, result.HistoryId!).Success, "真实副本资源历史撤销失败"); Equal(before, File.ReadAllBytes(copied["Pmap.e5"]), "真实副本撤销不能还原完整压缩档案");
        var landmarks = new[]
        {
            (Label: "wall", Pixel: new PointF(20, 20), Cell: new Point(8, 45), Word: (ushort)0xF0FF),
            (Label: "doorway", Pixel: new PointF(575, 70), Cell: new Point(49, 17), Word: (ushort)0xFFFF),
            (Label: "floor", Pixel: new PointF(400, 180), Cell: new Point(52, 42), Word: (ushort)0xFFFF)
        };
        using var landmarkDocument = service.Load(project, 42);
        foreach (var mark in landmarks)
        {
            Require(landmarkDocument.Geometry.HitTest(mark.Pixel) == mark.Cell, "墙/门口/地面像素坐标与旧工具literal不符：" + mark.Label);
            Require(landmarkDocument.GetCell(mark.Cell.X, mark.Cell.Y) == mark.Word, "墙/门口/地面独立解码原始值不符：" + mark.Label);
        }
        landmarkDocument.BeginStroke();
        foreach (var mark in landmarks) landmarkDocument.SetCell(mark.Cell.X, mark.Cell.Y, mark.Word != 0xF0FF);
        Require(landmarkDocument.EndStroke(), "墙/门口/地面测试笔画没有变化");
        var landmarkResult = new ImageMutationService(history).Commit(project, service.PlanEdit(project, landmarkDocument));
        Require(landmarkResult.Success, "墙/门口/地面真实副本保存失败"); service.AcceptSaved(project, landmarkDocument);
        Require(!landmarkDocument.IsDirty, "墙/门口/地面真实副本保存未更新已保存基线");
        using (var reopened = service.Load(project, 42))
            foreach (var mark in landmarks) Require(reopened.GetCell(mark.Cell.X, mark.Cell.Y) == (mark.Word == 0xF0FF ? 0xFFFF : 0xF0FF), "墙/门口/地面保存重新打开不一致：" + mark.Label);
        var landmarkPayload = E5Archive.OpenFresh(copied["Pmap.e5"]).ReadDecoded(2);
        var expectedChanges = landmarks.Select(mark => 16 + 2 * (mark.Cell.Y * 100 + mark.Cell.X) + 1).Order().ToArray();
        Require(Enumerable.Range(0, originalDecoded.Length).Where(at => originalDecoded[at] != landmarkPayload[at]).SequenceEqual(expectedChanges), "墙/门口/地面保存改变了三个目标高字节以外内容");
        Require(history.Undo(project, landmarkResult.HistoryId!).Success, "墙/门口/地面真实副本历史撤回失败");
        Equal(before, File.ReadAllBytes(copied["Pmap.e5"]), "墙/门口/地面历史撤回未恢复原始完整压缩档案");
        using var originalDoc = service.Load(project, 42); RenderEvidence(originalDoc, Path.Combine(output, version + "-Mmap42-Pmap2-overlay.png"));
        foreach (var pair in sourcePaths) Require(Hash(pair.Value) == hashes[pair.Key], "验收改动了真实源文件：" + pair.Value);
        Checks.Add(version + "真实样本副本编辑保存/压缩保持/历史撤回/源文件哈希保持");
        return new { Version = version, Source = source, Hashes = hashes, MmapCount = mmap.Entries.Count, PmapCount = pmap.Entries.Count,
            PmapCompressedEntries = pmap.Entries.Count(entry => entry.IsCompressed), EngineBlockedConsumerFileOffset = blockedAt,
            EngineWordIndexFileOffset = indexAt, CoordinateRoundTrip = true, OriginalWord = original, EditedWord = original == 0xF0FF ? 0xFFFF : 0xF0FF,
            LandmarkWriteback = landmarks.Select(mark => new { mark.Label, NativePixel = new[] { mark.Pixel.X, mark.Pixel.Y }, FileCell = new[] { mark.Cell.X, mark.Cell.Y },
                GameCell = new[] { mark.Cell.X, mark.Cell.Y + 2 }, ByteOffset = 16 + 2 * (mark.Cell.Y * 100 + mark.Cell.X), OriginalWord = $"0x{mark.Word:X4}",
                EditedWord = mark.Word == 0xF0FF ? "0xFFFF" : "0xF0FF", SavedAndReopened = true, UndoRestoredOriginalArchive = true }).ToArray() };
    }

    private static void RenderEvidence(SceneTerrainDocument document, string path)
    {
        using var bitmap = new Bitmap(1280, 800); using var graphics = Graphics.FromImage(bitmap);
        graphics.ScaleTransform(2, 2); graphics.DrawImage(document.Background, new Rectangle(Point.Empty, document.Background.Size),
            0, 0, document.Background.Width, document.Background.Height, GraphicsUnit.Pixel);
        using var grid = new Pen(Color.FromArgb(100, Color.Black), .5f);
        for (var y = 0; y < document.Rows; y++) for (var x = 0; x < document.Columns; x++)
        {
            var center = document.Geometry.CellCenter(x, y);
            if (center.X < -8 || center.X > 648 || center.Y < -4 || center.Y > 404) continue;
            graphics.DrawPolygon(grid, document.Geometry.CellPolygon(x, y));
            if (document.IsBlocked(x, y)) graphics.FillEllipse(Brushes.Red, center.X - 1.5f, center.Y - 1.5f, 3, 3);
        }
        bitmap.Save(path, ImageFormat.Png);
    }

    private static ProjectProfile Fixture(string root, string exe, int mmapCount, int pmapCount)
    {
        Directory.CreateDirectory(root); var resources = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        foreach (var name in new[] { "Ekd5.exe", "Mmap.e5", "Pmap.e5" }) resources[name] = Path.Combine(root, name);
        File.Copy(exe, resources["Ekd5.exe"]);
        File.WriteAllBytes(resources["Mmap.e5"], Archive(Enumerable.Range(0, mmapCount).Select(index => ImagePayload(index < 40 ? Color.Blue : Color.Gray)).ToArray()));
        var payloads = Enumerable.Range(0, pmapCount).Select(_ => Payload()).ToArray();
        if (pmapCount > 1) BinaryPrimitives.WriteUInt16LittleEndian(payloads[1].AsSpan(16 + 2 * (10 * 100 + 10), 2), 0xF0FF);
        File.WriteAllBytes(resources["Pmap.e5"], Archive(payloads));
        return new(root, "场景地形测试", ProjectVersion.Ccz65, false, resources, []);
    }

    private static LogicalImageAsset Asset(ProjectProfile project, int number) => new("Mmap.e5", number, "场景" + number, ImageCategory.Scene,
        ResourceKind.E5Indexed, [new("Mmap.e5", project.TryGetResource("Mmap.e5")!, number, 0, 1, "", "", 640, 400)], [], false, false, "") { PhysicalImageNumber = number };
    private static E5Archive Candidate(MutationPlan plan, string name) => E5Archive.Parse(name, plan.Files.Single(file => Path.GetFileName(file.TargetPath).Equals(name, StringComparison.OrdinalIgnoreCase)).CandidateBytes);
    private static byte[] Payload()
    {
        var bytes = new byte[20016]; BinaryPrimitives.WriteUInt16LittleEndian(bytes.AsSpan(2), 100); BinaryPrimitives.WriteUInt16LittleEndian(bytes.AsSpan(4), 100);
        BinaryPrimitives.WriteUInt16LittleEndian(bytes.AsSpan(6), 1); BinaryPrimitives.WriteUInt16LittleEndian(bytes.AsSpan(8), 200); BinaryPrimitives.WriteUInt16LittleEndian(bytes.AsSpan(10), 100);
        Array.Fill(bytes, (byte)0xFF, 16, 20000); return bytes;
    }
    private static byte[] UnknownPayload() { var bytes = Payload(); bytes[16] = 0xA5; return bytes; }
    private static byte[] ImagePayload(Color color) { using var bitmap = new Bitmap(640, 400); using (var graphics = Graphics.FromImage(bitmap)) graphics.Clear(color); using var stream = new MemoryStream(); bitmap.Save(stream, ImageFormat.Png); return stream.ToArray(); }
    private static byte[] Archive(IReadOnlyList<byte[]> entries)
    {
        var at = E5Archive.IndexOffset + entries.Count * E5Archive.EntrySize + 4; var bytes = new byte[at + entries.Sum(entry => entry.Length)]; "Ls12"u8.CopyTo(bytes);
        for (var index = 0; index < entries.Count; index++) { var p = E5Archive.IndexOffset + index * 12; BinaryPrimitives.WriteUInt32BigEndian(bytes.AsSpan(p), (uint)entries[index].Length); BinaryPrimitives.WriteUInt32BigEndian(bytes.AsSpan(p + 4), (uint)entries[index].Length); BinaryPrimitives.WriteUInt32BigEndian(bytes.AsSpan(p + 8), (uint)at); entries[index].CopyTo(bytes, at); at += entries[index].Length; }
        return bytes;
    }
    private static int Find(byte[] bytes, byte[] pattern) => bytes.AsSpan().IndexOf(pattern);
    private static string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path)));
    private static void Equal(byte[] expected, byte[] actual, string message) => Require(expected.AsSpan().SequenceEqual(actual), message);
    private static void Require(bool value, string message) { if (!value) throw new InvalidOperationException(message); }
}
