using System.Drawing;

namespace ImageManager.Core;

public sealed class StrategyAnimationResourceCodec : IResourceCodec
{
    public ResourceKind Kind => ResourceKind.McallAnimation;

    public bool CanHandle(ImageResourceDescriptor resource)
        => resource.Kind == ResourceKind.McallAnimation || resource.Key.Equals("Meff.e5", StringComparison.OrdinalIgnoreCase);

    public IReadOnlyList<LogicalImageAsset> ReadAssets(ProjectProfile project, ImageResourceDescriptor resource)
    {
        if (resource.Kind == ResourceKind.McallAnimation)
        {
            var frame = new FrameDescriptor(resource.Key, resource.Paths.Single(), 0, 0, 1, "mcall", "none", 0, 0);
            var id = ParseMcallId(resource.Paths.Single());
            var references = ReadStrategyRows(project).Where(row => row.McallId != 255 && row.McallId == id + 100)
                .Select(row => $"策略行 {row.RowIndex:000} {row.Name}（Mcall={row.McallId}）").ToArray();
            return [new LogicalImageAsset(resource.Key, id, resource.DisplayName,
                ImageCategory.StrategyAnimation, resource.Kind, [frame], references, false,
                resource.IsExperimental, resource.Status)];
        }
        var path = resource.Paths.Single();
        var archive = E5Archive.OpenMeff(path);
        var referencesById = ReadStrategyRows(project).Where(row => row.MeffId != 255)
            .GroupBy(row => row.MeffId).ToDictionary(group => group.Key, group => group
                .Select(row => $"策略行 {row.RowIndex:000} {row.Name}（Meff={row.MeffId}）").ToArray());
        return archive.Entries.Select(entry =>
        {
            var frame = new FrameDescriptor(resource.Key, path, entry.ImageNumber, 0, 1, "meff", "none", 0, 0);
            var id = entry.ImageNumber - 1;
            var status = resource.Status;
            try
            {
                // Probe every entry while building the gallery.  A legacy
                // Meff archive can contain a valid 64-entry index with a few
                // opaque/reserved payloads at the end; keep those rows visible
                // and report their payload status instead of dropping the
                // entire archive.
                if (archive.Entries.Count == 64 && entry.ImageNumber > 60)
                    status += "；载荷探针失败：保留的 Meff 尾部条目不是可播放动画";
                else
                    status += "；" + StrategyAnimationPackageCodec.Probe(archive.ReadDecoded(entry.ImageNumber));
            }
            catch (Exception ex) when (ex is InvalidDataException or IOException)
            {
                status += "；载荷探针失败：" + ex.Message;
            }
            return new LogicalImageAsset(resource.Key, entry.ImageNumber - 1, $"Meff {entry.ImageNumber - 1:000}",
                ImageCategory.StrategyAnimation, ResourceKind.E5Indexed, [frame],
                referencesById.GetValueOrDefault(id) ?? Array.Empty<string>(), false,
                resource.IsExperimental, status);
        }).ToArray();
    }

    public IReadOnlyList<DecodedFrame> DecodeFrames(ProjectProfile project, LogicalImageAsset asset)
    {
        var source = asset.Frames.Single();
        var bytes = ReadPackageBytes(source);
        using var animation = StrategyAnimationDecoder.Decode(project, bytes);
        return animation.Frames.Select((bitmap, index) =>
        {
            var descriptor = source with { FrameIndex = index, Width = bitmap.Width, Height = bitmap.Height };
            return new DecodedFrame(descriptor, new Bitmap(bitmap));
        }).ToArray();
    }

    public DecodedFrame DecodePreviewFrame(ProjectProfile project, LogicalImageAsset asset, FrameDescriptor descriptor,
        CancellationToken cancellationToken = default)
    {
        cancellationToken.ThrowIfCancellationRequested();
        var source = asset.Frames.Single();
        var bytes = ReadPackageBytes(source);
        cancellationToken.ThrowIfCancellationRequested();
        using var bitmap = new StrategyAnimationPackageCodec().DecodePreviewFrame(project, bytes,
            descriptor.FrameIndex, cancellationToken);
        return new DecodedFrame(source with
            { FrameIndex = descriptor.FrameIndex, Width = bitmap.Width, Height = bitmap.Height }, new Bitmap(bitmap));
    }

    private static int ParseMcallId(string path)
    {
        var digits = new string(Path.GetFileNameWithoutExtension(path).Where(char.IsDigit).ToArray());
        return int.TryParse(digits, out var value) ? value : 0;
    }

    /// <summary>
    /// Reads one strategy animation package for playback, timing, export or plane editing.
    /// Standalone Mcall packages use image number zero; indexed packages are Meff entries
    /// and must use the same legacy-directory reader as the animation decoder.
    /// </summary>
    public static byte[] ReadPackageBytes(FrameDescriptor source)
        => source.ImageNumber == 0 ? File.ReadAllBytes(source.SourcePath)
            : E5Archive.OpenMeff(source.SourcePath).ReadDecoded(source.ImageNumber);

    private static IReadOnlyList<StrategyRow> ReadStrategyRows(ProjectProfile project)
    {
        try { return new StrategyRowService().Read(project); }
        catch (Exception) { return Array.Empty<StrategyRow>(); }
    }
}
