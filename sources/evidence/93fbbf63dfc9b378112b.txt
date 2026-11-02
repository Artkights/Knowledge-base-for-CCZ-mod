using System.Buffers.Binary;
using System.Diagnostics;
using System.Drawing.Imaging;
using System.Reflection;
using System.Text.Json;
using DataManager.Images;
using ImageManager.App;
using ImageManager.Core;

namespace DataManager.Tests;

internal static class SceneTerrainIntegrationTests
{
    private const BindingFlags Private = BindingFlags.Instance | BindingFlags.NonPublic;
    private static readonly List<string> Checks = [];

    public static void Run(string repositoryRoot)
    {
        var repo = Path.GetFullPath(repositoryRoot);
        var output = Path.Combine(repo, "data管理器", "验证", "2026-10-23-内场景地形编辑", "ui");
        Directory.CreateDirectory(output);
        var temp = Path.Combine(output, ".work-ui-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(temp);
        try
        {
            var exe = Path.Combine(repo, "基底", "加强版6.5未加密版", "Ekd5.exe");
            CheckAdapter(Fixture(Path.Combine(temp, "adapter"), exe));
            CheckLiveService(Fixture(Path.Combine(temp, "live"), exe));
            CheckNavigation(Fixture(Path.Combine(temp, "navigation"), exe));
            CheckPopup(repo, temp, output);
            File.WriteAllText(Path.Combine(output, "scene-terrain-ui-results.json"),
                JsonSerializer.Serialize(new { Passed = true, Checks }, new JsonSerializerOptions { WriteIndented = true }));
            Console.WriteLine("SCENE_TERRAIN_INTEGRATION_TESTS_OK " + output);
        }
        finally
        {
            foreach (var file in Directory.EnumerateFiles(temp, "*", SearchOption.AllDirectories)) File.SetAttributes(file, FileAttributes.Normal);
            Directory.Delete(temp, true);
        }
    }

    private static void CheckAdapter(ProjectProfile project)
    {
        using var adapter = new ResourceCatalogAdapter();
        var root = project.RootPath; var pmap = project.TryGetResource("Pmap.e5")!; var mmap = project.TryGetResource("Mmap.e5")!;
        var original = E5Archive.OpenFresh(pmap); var tail = original.ReadStored(3);
        var source = Path.Combine(root, "source.png"); File.WriteAllBytes(source, ImagePayload(Color.Olive));
        var added = adapter.Append(root, "Mmap.e5", [source]);
        Require(added.Success && added.WrittenPaths.Count == 2, "适配层Mmap新增未提交双文件：" + string.Join(";", added.Diagnostics));
        var afterAppend = E5Archive.OpenFresh(pmap);
        Require(E5Archive.OpenFresh(mmap).Entries.Count == 43 && afterAppend.Entries.Count == 4, "适配层新增数量错误");
        Equal(tail, afterAppend.ReadStored(4), "适配层把新增地形写到额外尾条目后");
        var remainingPair = afterAppend.ReadStored(3);
        var removed = adapter.Delete(root, "Mmap.e5", [42]);
        Require(removed.Success && removed.WrittenPaths.Count == 2, "适配层删除内场景未提交双文件");
        var afterDelete = E5Archive.OpenFresh(pmap);
        Require(E5Archive.OpenFresh(mmap).Entries.Count == 42 && afterDelete.Entries.Count == 3, "适配层删除数量错误");
        Equal(remainingPair, afterDelete.ReadStored(2), "适配层内场景删除后配对错位");
        Equal(tail, afterDelete.ReadStored(3), "适配层删除丢失额外尾条目");
        var pmapBeforeOuter = File.ReadAllBytes(pmap);
        Require(adapter.Delete(root, "Mmap.e5", [5]).Success, "适配层外场景删除失败");
        Require(E5Archive.OpenFresh(mmap).Entries.Count == 42, "适配层外场景删除缩短固定前40槽");
        Equal(pmapBeforeOuter, File.ReadAllBytes(pmap), "适配层外场景删除修改Pmap");
        using (var black = ImageRendering.DecodeStandardImage(E5Archive.OpenFresh(mmap).ReadDecoded(5)))
            Require(black.GetPixel(100, 100).ToArgb() == Color.Black.ToArgb(), "适配层外场景未使用黑图占位");
        Reject(() => adapter.Append(root, "Pmap.e5", [source]), "适配层开放Pmap直接新增");
        Reject(() => adapter.Replace(root, "Pmap.e5", [1], [source]), "适配层开放Pmap直接图片替换");
        Reject(() => adapter.Delete(root, "Pmap.e5", [1]), "适配层开放Pmap直接删除");
        Equal(pmapBeforeOuter, File.ReadAllBytes(pmap), "Pmap直接操作拒绝后仍修改了文件");
        Require(ProjectImageHistory.List(project).Count >= 3, "适配层操作没有纳入项目资源历史");
        Checks.Add("ResourceCatalogAdapter实际新增/内场景删除/外场景占位、尾条目保留、Pmap直接操作拒绝、项目历史");
    }

    private static void CheckLiveService(ProjectProfile project)
    {
        using var adapter = new ResourceCatalogAdapter();
        var type = typeof(IntegratedResourcePanel).GetNestedType("LiveImageMutationService", BindingFlags.NonPublic)!;
        var service = (IImageMutationService)Activator.CreateInstance(type, BindingFlags.Public | Private, null,
            [adapter, ProjectImageHistory.Create(project)], null)!;
        var catalog = new ImageCatalogService();
        var descriptors = catalog.BuildCatalog(project); var descriptor = descriptors.Single(item => item.Key == "Mmap.e5");
        var assets = catalog.ReadAssets(project, descriptor);
        var source = Path.Combine(project.RootPath, "source.png"); File.WriteAllBytes(source, ImagePayload(Color.Purple));
        var plan = service.PlanAppend(project, descriptor, [source]);
        Require(plan.Files.Count == 2, "图库Live新增没有Pmap配对");
        Require(service.Commit(project, plan).Success, "图库Live双文件新增提交失败");
        var after = E5Archive.OpenFresh(project.TryGetResource("Pmap.e5")!);
        Require(after.Entries.Count == 4, "图库Live追加没有落盘Pmap");
        var innerDelete = service.PlanDelete(project, [assets.Single(asset => asset.Frames[0].ImageNumber == 41)]);
        Require(innerDelete.Files.Count == 2, "图库Live内场景删除未配对");
        using var edited = new Bitmap(640, 400);
        var original = assets.Single(asset => asset.Frames[0].ImageNumber == 42);
        var copied = service.PlanReplaceSingleFrame(project, original, original.Frames[0], edited, true);
        Require(copied.Files.Count == 2, "图库Live图片编辑后另存副本没有复制地形");
        var candidate = E5Archive.Parse("copy.e5", copied.Files.Single(file => Path.GetFileName(file.TargetPath) == "Pmap.e5").CandidateBytes);
        Equal(after.ReadDecoded(2), candidate.ReadDecoded(4), "图库Live副本地形没有取来源物理条目");
        var pmapAsset = new LogicalImageAsset("Pmap.e5", 1, "地形", ImageCategory.Scene, ResourceKind.PmapSpecial,
            [new("Pmap.e5", project.TryGetResource("Pmap.e5")!, 1, 0, 1, "", "", 100, 100)], [], false, false, "");
        Reject(() => service.PlanReplace(project, [pmapAsset], [source]), "图库Live允许直接替换Pmap图片");
        Reject(() => service.PlanDelete(project, [pmapAsset]), "图库Live允许直接删除Pmap");
        Reject(() => service.PlanReplaceSingleFrame(project, pmapAsset, pmapAsset.Frames[0], edited, true), "图库Live允许Pmap像素副本");
        var plain = new ImageMutationService(ProjectImageHistory.Create(project)).PlanAppend(project, descriptor, [source]);
        Reject(() => service.Commit(project, plain), "图库Live提交门禁接受了没有配对的Mmap新增计划");
        var preparationType = typeof(IntegratedResourcePanel).GetNestedType("LiveImageImportPreparationService", BindingFlags.NonPublic)!;
        var preparation = (IImageImportPreparationService)Activator.CreateInstance(preparationType, true)!;
        var prepareTask = preparation.PrepareAsync(new(project, descriptor, ImageImportOperation.Append, [new(null, "image", source)]));
        Wait(prepareTask); using var prepared = prepareTask.Result;
        Require(prepared.CanCommit && prepared.Plan!.Files.Count == 2, "图库真实导入预检没有建立双文件候选");
        Checks.Add("图库Live服务新增/删除/编辑副本、Pmap写入门禁、缺配对提交拒绝与真实导入预检");
    }

    private static void CheckNavigation(ProjectProfile project)
    {
        using var host = new Form { ShowInTaskbar = false, Location = new Point(-32000, -32000), StartPosition = FormStartPosition.Manual };
        using var panel = new IntegratedResourcePanel { Dock = DockStyle.Fill }; host.Controls.Add(panel); host.Show();
        panel.LoadProject(project.RootPath, "resource:PMAP.E5"); Wait(panel.LoadingTask);
        var page = Descendants(panel).OfType<ImageGridPage>().Single();
        var buttons = (Dictionary<string, Button>)typeof(ImageGridPage).GetField("_buttons", Private)!.GetValue(page)!;
        Require(buttons.TryGetValue("terrain", out var terrain) && terrain.Visible, "旧Pmap分类没有导向Mmap地形入口");
        var gallery = Descendants(page).OfType<VirtualImageGallery>().Single();
        Require(gallery.ItemCount == 42, "旧Pmap分类仍展示地形位图条目");
        Require(!panel.ProjectCategories.Any(category => category.Key.Equals("Resource:Pmap.e5", StringComparison.OrdinalIgnoreCase)), "形象分类仍显示Pmap独立入口");
        using var adapter = new ResourceCatalogAdapter();
        var assets = adapter.ReadAssets(project.RootPath, "Mmap.e5");
        void Focus(int number)
        {
            typeof(ImageGridPage).GetMethod("ActivatePreview", Private)!.Invoke(page, [assets.Single(asset => asset.Frames[0].ImageNumber == number)]);
            Application.DoEvents(); Wait(page.TerrainAvailabilityTask);
        }
        Focus(1); Require(!terrain!.Enabled, "外场景仍启用地形编辑");
        Focus(41); Require(terrain.Enabled, "已验证内场景没有启用地形编辑");
        var pmapPath = project.TryGetResource("Pmap.e5")!; var originalPmap = File.ReadAllBytes(pmapPath);
        File.Delete(pmapPath); page.InvalidateResources([pmapPath]); Wait(page.TerrainAvailabilityTask);
        Require(!terrain.Enabled, "缺少Pmap仍启用地形编辑");
        File.WriteAllBytes(pmapPath, [1, 2, 3, 4]); page.InvalidateResources([pmapPath]); Wait(page.TerrainAvailabilityTask);
        Require(!terrain.Enabled, "损坏Pmap仍启用地形编辑");
        var valid = PmapTerrainCodec.CreateDefault(); var unknown = (byte[])valid.Clone(); unknown[16] = 0xA5;
        File.WriteAllBytes(pmapPath, Archive([unknown])); page.InvalidateResources([pmapPath]); Wait(page.TerrainAvailabilityTask);
        Require(!terrain.Enabled, "未知地形格值仍启用地形编辑");
        File.WriteAllBytes(pmapPath, Archive([valid])); page.InvalidateResources([pmapPath]); Focus(42);
        Require(!terrain.Enabled, "缺少配对条目仍启用地形编辑");
        File.WriteAllBytes(pmapPath, originalPmap); page.InvalidateResources([pmapPath]); Focus(41);
        Require(terrain.Enabled, "修复Pmap并失效缓存后未恢复地形编辑");
        var current = typeof(ImageGridPage).GetField("_project", Private)!.GetValue(page) as ProjectProfile;
        Require(current != null, "图库未装载项目");
        var resource = new ImageResourceDescriptor("Tr.e5", "过场", ImageCategory.Scene, ResourceKind.E5Indexed,
            [project.TryGetResource("Mmap.e5")!], 42, true, true, false, "", "");
        ConfigureResource(page, resource);
        Require(!terrain!.Visible, "Mmap以外资源出现地形编辑入口");
        host.Close();
        Checks.Add("大小写旧Pmap分类导向Mmap、分类移除Pmap、外场景/缺失/损坏/未知格/缺条地形入口禁用、修复后恢复、其他图库无入口");
    }

    private static void CheckPopup(string repo, string temp, string output)
    {
        foreach (var sample in new[] { ("6.4", "洗隋"), ("6.5", "加强版6.5未加密版"), ("6.6", "新改曹操傳6.6修正版"), ("6.6山贼", "复刻版6.6山贼") })
        {
            var detected = new ProjectProfileService().Detect(Path.Combine(repo, "基底", sample.Item2));
            var root = Path.Combine(temp, "popup-" + sample.Item1); Directory.CreateDirectory(root);
            var paths = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
            foreach (var name in new[] { "Ekd5.exe", "Mmap.e5", "Pmap.e5" })
            { paths[name] = Path.Combine(root, name); File.Copy(detected.TryGetResource(name)!, paths[name]); }
            var project = detected with { RootPath = root, ResourcePaths = paths };
            var terrain = new SceneTerrainService(); using var document = terrain.Load(project, 42);
            Require(document.CanEdit, "弹窗真实样本不可编辑：" + document.Diagnostic);
            var saves = 0;
            using var dialog = new SceneTerrainEditorDialog(document, () =>
            {
                saves++; var result = ProjectImageHistory.Commit(project, terrain.PlanEdit(project, document));
                if (result.Success) terrain.AcceptSaved(project, document);
                return Task.FromResult(result.Success);
            }) { StartPosition = FormStartPosition.Manual, Location = new Point(-32000, -32000), ShowInTaskbar = false };
            dialog.Show(); Application.DoEvents();
            var canvas = Descendants(dialog).OfType<DiamondTerrainCanvas>().Single(); canvas.Zoom = 1;
            var showTerrain = Descendants(dialog).OfType<CheckBox>().Single(control => control.Name == "ShowTerrain");
            var showGrid = Descendants(dialog).OfType<CheckBox>().Single(control => control.Name == "ShowGrid");
            Require(!Descendants(dialog).OfType<Button>().Any(), "地形弹窗重复出现图库下方操作按钮");
            var start = document.Geometry.CellCenter(25, 35); var finish = document.Geometry.CellCenter(55, 35);
            var original = document.GetCell(25, 35);
            showTerrain.Checked = false; Mouse(canvas, "OnMouseDown", MouseButtons.Left, start); Mouse(canvas, "OnMouseUp", MouseButtons.Left, start);
            Require(document.GetCell(25, 35) == original && !document.IsDirty, "关闭显示地形后仍可涂写");
            showTerrain.Checked = true;
            Mouse(canvas, "OnMouseDown", MouseButtons.Left, start); Mouse(canvas, "OnMouseUp", MouseButtons.Left, finish);
            Require(Enumerable.Range(25, 31).All(x => document.IsBlocked(x, 35)), "弹窗快速左键跨格填涂漏格");
            canvas.Undo(); Require(document.GetCell(25, 35) == original && !document.IsDirty, "弹窗一次撤回没有恢复整条笔画");
            canvas.Redo(); Mouse(canvas, "OnMouseDown", MouseButtons.Right, start); Mouse(canvas, "OnMouseUp", MouseButtons.Right, finish);
            Require(Enumerable.Range(25, 31).All(x => !document.IsBlocked(x, 35)), "弹窗快速右键跨格擦除漏格");
            canvas.Undo();
            var boundaryStart = document.Geometry.CellCenter(60, 35);
            var boundaryFinish = document.Geometry.CellCenter(65, 35);
            var beforeBoundary = document.GetCell(65, 35);
            var boundaryButton = document.IsBlocked(60, 35) ? MouseButtons.Right : MouseButtons.Left;
            Mouse(canvas, "OnMouseDown", boundaryButton, boundaryStart);
            Mouse(canvas, "OnMouseMove", boundaryButton, new PointF(-1, 12));
            Mouse(canvas, "OnMouseUp", boundaryButton, boundaryFinish);
            Require(document.GetCell(65, 35) == beforeBoundary, "离开有效区域后松键仍跨区补画");
            canvas.Undo();
            Mouse(canvas, "OnMouseMove", MouseButtons.None, start);
            var coordinates = Descendants(dialog).OfType<Label>().Single(control => control.Name == "TerrainCoordinates");
            Require(coordinates.Text == "X：25  Y：37", "弹窗右下角坐标没有对应旧工具游戏坐标：" + coordinates.Text);
            var scroll = Descendants(dialog).OfType<Panel>().Single(control => control.Name == "TerrainScroll");
            beforeBoundary = document.GetCell(65, 35);
            boundaryButton = document.IsBlocked(60, 35) ? MouseButtons.Right : MouseButtons.Left;
            Mouse(canvas, "OnMouseDown", boundaryButton, boundaryStart);
            typeof(Panel).GetMethod("OnScroll", Private)!.Invoke(scroll, [new ScrollEventArgs(ScrollEventType.ThumbPosition, 12, ScrollOrientation.VerticalScroll)]);
            Application.DoEvents(); Application.DoEvents();
            Require(coordinates.Text == "X：—  Y：—", "滚动后静止指针仍保留旧格坐标");
            Mouse(canvas, "OnMouseUp", boundaryButton, boundaryFinish);
            Require(document.GetCell(65, 35) == beforeBoundary, "普通滚动后松键仍连接到旧笔画");
            canvas.Undo();
            canvas.Zoom = 1.75; canvas.Size = new Size(1234, 567);
            typeof(DiamondTerrainCanvas).GetMethod("OnDpiChangedAfterParent", Private)!.Invoke(canvas, [EventArgs.Empty]);
            Require(canvas.Size == new Size((int)Math.Ceiling(canvas.SourceSize.Width * 1.75), (int)Math.Ceiling(canvas.SourceSize.Height * 1.75)), "DPI变化后的画布尺寸与绘制/命中缩放不一致");
            canvas.Zoom = 1; Application.DoEvents(); Mouse(canvas, "OnMouseMove", MouseButtons.None, start);
            showGrid.Checked = false; Require(!canvas.ShowGrid, "显示网格复选框未生效"); showGrid.Checked = true;
            using (var bitmap = new Bitmap(dialog.Width, dialog.Height))
            { dialog.DrawToBitmap(bitmap, new Rectangle(Point.Empty, bitmap.Size)); bitmap.Save(Path.Combine(output, sample.Item1 + "-terrain-popup.png"), ImageFormat.Png); }
            var saved = (Task<bool>)typeof(SceneTerrainEditorDialog).GetMethod("SaveDocument", Private)!.Invoke(dialog, null)!;
            Wait(saved); Require(saved.Result && saves == 1 && !document.IsDirty, "弹窗保存回调没有清除脏状态");
            using (var reread = terrain.Load(project, 42)) Require(reread.IsBlocked(25, 35), "弹窗真实副本保存复读失败");
            dialog.Close();
            using var readOnlyDocument = terrain.Load(project with { IsReadOnly = true }, 42);
            using var readOnlyDialog = new SceneTerrainEditorDialog(readOnlyDocument, () => Task.FromResult(false));
            var readOnlyCanvas = Descendants(readOnlyDialog).OfType<DiamondTerrainCanvas>().Single();
            var before = readOnlyDocument.GetCell(25, 35);
            Mouse(readOnlyCanvas, "OnMouseDown", MouseButtons.Right, start); Mouse(readOnlyCanvas, "OnMouseUp", MouseButtons.Right, start);
            Require(!readOnlyCanvas.EditingEnabled && readOnlyDocument.GetCell(25, 35) == before && !readOnlyDocument.IsDirty, "只读弹窗仍允许绘制");
            Checks.Add(sample.Item1 + "真实弹窗：显示开关、左右快速笔画、出界/滚动结束笔画、静止指针坐标刷新、DPI缩放、撤回重做、游戏坐标、保存复读、只读拒写与实际WinForms截图");
        }
    }

    private static ProjectProfile Fixture(string root, string exe)
    {
        Directory.CreateDirectory(root); var paths = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        foreach (var name in new[] { "Ekd5.exe", "Mmap.e5", "Pmap.e5" }) paths[name] = Path.Combine(root, name);
        File.Copy(exe, paths["Ekd5.exe"]);
        File.WriteAllBytes(paths["Mmap.e5"], Archive(Enumerable.Range(1, 42).Select(index => ImagePayload(index <= 40 ? Color.Navy : Color.Gray)).ToArray()));
        var terrains = Enumerable.Range(1, 3).Select(_ => PmapTerrainCodec.CreateDefault()).ToArray();
        BinaryPrimitives.WriteUInt16LittleEndian(terrains[1].AsSpan(16 + 2 * (10 * 100 + 10)), 0xF0FF);
        File.WriteAllBytes(paths["Pmap.e5"], Archive(terrains));
        var profile = new ProjectProfileService().Detect(root);
        Require(profile.Version == ProjectVersion.Ccz65 && !profile.IsReadOnly, "适配层测试副本未识别为可写6.5");
        return profile;
    }

    private static void ConfigureResource(ImageGridPage page, ImageResourceDescriptor resource)
    {
        var selector = (ComboBox)typeof(ImageGridPage).GetField("_resourceSelector", Private)!.GetValue(page)!;
        var itemType = typeof(ImageGridPage).GetNestedType("ResourceItem", BindingFlags.NonPublic)!;
        var item = Activator.CreateInstance(itemType, BindingFlags.Public | Private, null, [resource, false], null)!;
        var initializing = typeof(ImageGridPage).GetField("_initializing", Private)!; initializing.SetValue(page, true);
        try { selector.DataSource = null; selector.Items.Clear(); selector.Items.Add(item); selector.SelectedIndex = 0; }
        finally { initializing.SetValue(page, false); }
        typeof(ImageGridPage).GetMethod("ConfigureWriteButtons", Private)!.Invoke(page, [resource]);
        typeof(ImageGridPage).GetMethod("UpdateWriteConstraints", Private)!.Invoke(page, null);
    }
    private static IEnumerable<Control> Descendants(Control root)
    { foreach (Control child in root.Controls) { yield return child; foreach (var descendant in Descendants(child)) yield return descendant; } }
    private static void Mouse(Control control, string method, MouseButtons button, PointF point)
        => control.GetType().GetMethod(method, Private)!.Invoke(control, [new MouseEventArgs(button, 1, (int)point.X, (int)point.Y, 0)]);
    private static void Wait(Task task)
    { var watch = Stopwatch.StartNew(); while (!task.IsCompleted) { if (watch.Elapsed > TimeSpan.FromSeconds(30)) throw new TimeoutException("地形UI测试超时"); Application.DoEvents(); Thread.Sleep(5); } task.GetAwaiter().GetResult(); Application.DoEvents(); }
    private static void Reject(Action action, string message)
    { var rejected = false; try { action(); } catch (Exception ex) when (ex is InvalidOperationException or InvalidDataException) { rejected = true; } Require(rejected, message); }
    private static void Equal(byte[] expected, byte[] actual, string message) => Require(expected.AsSpan().SequenceEqual(actual), message);
    private static void Require(bool value, string message) { if (!value) throw new InvalidOperationException(message); }
    private static byte[] ImagePayload(Color color)
    { using var bitmap = new Bitmap(640, 400); using (var graphics = Graphics.FromImage(bitmap)) graphics.Clear(color); using var stream = new MemoryStream(); bitmap.Save(stream, ImageFormat.Png); return stream.ToArray(); }
    private static byte[] Archive(IReadOnlyList<byte[]> entries)
    {
        var at = E5Archive.IndexOffset + entries.Count * E5Archive.EntrySize + 4;
        var bytes = new byte[at + entries.Sum(entry => entry.Length)]; "Ls12"u8.CopyTo(bytes);
        for (var index = 0; index < entries.Count; index++)
        { var p = E5Archive.IndexOffset + index * 12; BinaryPrimitives.WriteUInt32BigEndian(bytes.AsSpan(p), (uint)entries[index].Length); BinaryPrimitives.WriteUInt32BigEndian(bytes.AsSpan(p + 4), (uint)entries[index].Length); BinaryPrimitives.WriteUInt32BigEndian(bytes.AsSpan(p + 8), (uint)at); entries[index].CopyTo(bytes, at); at += entries[index].Length; }
        return bytes;
    }
}
