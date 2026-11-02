using System.Drawing;
using System.Text.Json;
using ImageManager.Core;

namespace ImageManager.Tests;

internal static class AtlasPackageTests
{
    public static void Run()
    {
        var directory = Path.Combine(Path.GetTempPath(), "ImageManager.AtlasPackage", Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(directory);
        var frames = CreateFrames(242);
        var otherFrames = CreateFrames(337);
        try
        {
            var asset = Asset(242, frames);
            var context = ReferenceAtlasContext.Create(asset, frames);
            var service = new ReferenceAtlasService();
            var files = service.Export(directory, context, Color.Magenta);
            Require(new ReferenceAtlasExportOptions().Scale == 4, "新的参考包默认倍率必须为4。");
            Require(File.Exists(files.PngPath) && File.Exists(files.ManifestPath) && File.Exists(files.GuidePath) &&
                File.Exists(files.PromptPath) && files.TransparentPngPath.Length == 0,
                "默认参考包未生成四个独立文件。");
            using (var main = new Bitmap(files.PngPath))
            using (var guide = new Bitmap(files.GuidePath))
            {
                Require(main.Size == new Size(1392, 1392), "四倍S主图不是1392x1392。");
                Require(guide.Height > main.Height && guide.Width == main.Width, "动作对照图必须具有独立标注区域。");
                Require(main.GetPixel(0, 0).ToArgb() == Color.Magenta.ToArgb(), "主图被编号或标题污染。");
                Require(main.GetPixel((25 + 10) * 4, 12 * 4).ToArgb() == Color.Red.ToArgb(),
                    "四倍导出没有保留最近邻像素。");
                Require(main.GetPixel(323 * 4, 60 * 4).ToArgb() == Color.Magenta.ToArgb(),
                    "空白保留格或格间被绘入编号。");
            }

            var manifest = AtlasManifest.Load(files.ManifestPath);
            manifest.ValidateFor(context);
            Require(manifest.Version == 1 && manifest.SourcePhysicalImageNumber == 242 && manifest.Frames.Length == 28 &&
                manifest.SourceResourceKeys.Length == 3 && manifest.Sections.Length == 2,
                "清单丢失版本、真实物理号或完整动作结构。");
            var rowCounts = manifest.Frames.GroupBy(frame => frame.NativeBounds.Y).OrderBy(row => row.Key).Select(row => row.Count());
            Require(rowCounts.SequenceEqual(new[] { 6, 5, 5, 4, 4, 4 }), "S清单语义行不是6/5/5/4/4/4。");

            // A renamed image may use the old layout, but all destination keys must come from the new selection.
            var otherContext = ReferenceAtlasContext.Create(Asset(337, otherFrames), otherFrames);
            var roi = new Rectangle(50, 30, 696, 696);
            var mapping = manifest.CreateSourceMapping(otherContext, new Size(900, 760), roi);
            Require(mapping.EffectiveBounds == roi && mapping.ConfirmedFrames.Count == 0 && !mapping.RepairAspectRatio,
                "清单映射不得自动确认或默认变形人物。");
            Require(mapping.FrameRectangles.Keys.ToHashSet().SetEquals(otherFrames.Select(frame => AiAtlasNormalizer.FrameKey(frame.Descriptor))),
                "关联旧导出清单后使用了原图号的帧键。");
            var mov0 = otherFrames.Single(frame => frame.Descriptor.Action == "mov" && frame.Descriptor.FrameIndex == 0);
            Require(mapping.FrameRectangles[AiAtlasNormalizer.FrameKey(mov0.Descriptor)] == new Rectangle(100, 30, 96, 96),
                "非方形源图有效区域内的源坐标换算错误。");
            Require(otherContext.PhysicalImageNumber == 337, "清单来源号改变了当前选中目标。");

            var duplicate = manifest with { Frames = manifest.Frames.Select((frame, index) => index == 1 ? manifest.Frames[0] : frame).ToArray() };
            Throws(() => duplicate.ValidateFor(context), "重复动作清单必须拒绝。");
            var missing = manifest with { Frames = manifest.Frames.Skip(1).ToArray() };
            Throws(() => missing.ValidateFor(context), "不完整动作清单必须拒绝。");
            var unknownVersion = Path.Combine(directory, "unknown.atlas.json");
            File.WriteAllText(unknownVersion, JsonSerializer.Serialize(manifest with { Version = 99 }));
            Throws(() => AtlasManifest.Load(unknownVersion), "不支持版本必须拒绝。");
            var badBounds = manifest.Frames[0] with { NativeBounds = new(-1, 0, 48, 48) };
            Throws(() => (manifest with { Frames = new[] { badBounds }.Concat(manifest.Frames.Skip(1)).ToArray() }).ValidateFor(context),
                "越界动作格必须拒绝。");
            Throws(() => manifest.CreateSourceMapping(otherContext, new Size(900, 760), new Rectangle(800, 0, 200, 200)),
                "越界有效区域必须拒绝。");

            var prompt = File.ReadAllText(files.PromptPath);
            Require(prompt.Contains("只提供动作格式", StringComparison.Ordinal) && prompt.Contains("源裁剪格", StringComparison.Ordinal) &&
                prompt.Contains("图库当前选择", StringComparison.Ordinal) && !prompt.Contains("严格沿用原参考图每一格", StringComparison.Ordinal),
                "提示词仍然要求贴合旧人物或缺少灵活回导说明。");

            var legacyFiles = service.Export(Path.Combine(directory, "legacy"), asset, frames, Color.Magenta);
            using var legacy = new Bitmap(legacyFiles.PngPath);
            Require(legacy.Size == new Size(348, 348) && File.Exists(legacyFiles.TransparentPngPath),
                "既有asset+frames重载的原生倍率和透明观察版发生不兼容变化。");
        }
        finally
        {
            foreach (var frame in frames.Concat(otherFrames)) frame.Dispose();
            Directory.Delete(directory, true);
        }
    }

    private static List<DecodedFrame> CreateFrames(int imageNumber)
    {
        var frames = new List<DecodedFrame>();
        foreach (var action in new[] { (Name: "mov", Count: 11, Size: 48), (Name: "spc", Count: 5, Size: 48), (Name: "atk", Count: 12, Size: 64) })
        for (var index = 0; index < action.Count; index++)
        {
            var bitmap = new Bitmap(action.Size, action.Size);
            using (var graphics = Graphics.FromImage(bitmap))
            {
                graphics.Clear(Color.Transparent);
                graphics.FillRectangle(Brushes.Red, 10, 12, 15, 24);
            }
            frames.Add(new(new("Unit_" + action.Name + ".e5", "descriptive-only.e5", imageNumber, index, 1,
                action.Name, "front", action.Size, action.Size), bitmap));
        }
        return frames;
    }

    private static LogicalImageAsset Asset(int imageNumber, IReadOnlyList<DecodedFrame> frames)
        => new("SComposite", imageNumber, $"S_{imageNumber:000}", ImageCategory.CharacterS, ResourceKind.SComposite,
            frames.Select(frame => frame.Descriptor).ToArray(), [], false, false, string.Empty)
        { PhysicalImageNumber = imageNumber };

    private static void Require(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }

    private static void Throws(Action action, string message)
    {
        try { action(); }
        catch (InvalidDataException) { return; }
        throw new InvalidOperationException(message);
    }
}
