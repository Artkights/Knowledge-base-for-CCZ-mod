using System.Drawing;

namespace ImageManager.Core;

public sealed class ReferenceAtlasLayoutPlanner : IReferenceAtlasLayoutPlanner
{
    public const string SLayoutId = "s-semantic-size-grid-v3";
    public const int FrameGutter = 2;

    public ReferenceAtlasLayoutPlan Plan(LogicalImageAsset asset, IReadOnlyList<DecodedFrame> frames)
    {
        if (frames.Count == 0) throw new InvalidOperationException("没有可规划的参考图帧。");
        return asset.Kind switch
        {
            ResourceKind.RComposite => PlanLegacyR(frames),
            ResourceKind.SComposite => PlanS(frames, asset.PhysicalImageNumber.HasValue),
            _ => throw new InvalidOperationException("参考总图只适用于 R/S 逻辑形象。")
        };
    }

    private static ReferenceAtlasLayoutPlan PlanLegacyR(IReadOnlyList<DecodedFrame> frames)
    {
        var ordered = frames.OrderBy(frame => frame.Descriptor.Direction == "front" ? 0 : 1)
            .ThenBy(frame => frame.Descriptor.FrameIndex).ToArray();
        var cell = ordered.Max(frame => Math.Max(frame.Bitmap.Width, frame.Bitmap.Height));
        var columns = (int)Math.Ceiling(Math.Sqrt(ordered.Length));
        var canvas = checked(cell * columns);
        var placements = ordered.Select((frame, index) => new ReferenceAtlasPlacement(frame,
            new Rectangle(index % columns * cell, index / columns * cell, frame.Bitmap.Width, frame.Bitmap.Height))).ToArray();
        return new ReferenceAtlasLayoutPlan(canvas, "r-square-grid-v1", 0, 1, placements, Array.Empty<ReferenceAtlasSection>());
    }

    private static ReferenceAtlasLayoutPlan PlanS(IReadOnlyList<DecodedFrame> frames, bool physicalSlot)
    {
        var turns = frames.Select(frame => frame.Descriptor.Turn).Distinct().Order().ToArray();
        if (turns.Length is not (1 or 3) || turns.Length == 3 && !turns.SequenceEqual(new[] { 1, 2, 3 }))
            throw new InvalidDataException("S 参考图要求一转或完整的一至三转帧。");
        if (turns.Length == 1 && turns[0] is < 1 or > 3 || frames.Count != turns.Length * 28)
            throw new InvalidDataException("S 参考图包含未知动作、重复帧或无效转数。");
        if (physicalSlot && turns.Length != 1)
            throw new InvalidDataException("物理 S 参考图只能包含所选 Unit 图号的 28 帧。");
        var placements = new List<ReferenceAtlasPlacement>(turns.Length * 28);
        var sections = new List<ReferenceAtlasSection>(turns.Length * 2);
        for (var turnOrdinal = 0; turnOrdinal < turns.Length; turnOrdinal++)
        {
            var turn = turns[turnOrdinal];
            var byAction = frames.Where(frame => frame.Descriptor.Turn == turn)
                .GroupBy(frame => frame.Descriptor.Action).ToDictionary(group => group.Key, group => group.ToArray());
            var mov = RequireFrames(byAction, turn, "mov", 11, 48);
            var spc = RequireFrames(byAction, turn, "spc", 5, 48);
            var atk = RequireFrames(byAction, turn, "atk", 12, 64);
            for (var index = 0; index < mov.Length; index++)
                placements.Add(new ReferenceAtlasPlacement(mov[index], SmallBounds(turns.Length, turnOrdinal,
                    index < 6 ? 0 : 1, index < 6 ? index : index - 6)));
            for (var index = 0; index < spc.Length; index++)
                placements.Add(new ReferenceAtlasPlacement(spc[index], SmallBounds(turns.Length, turnOrdinal, 2, index)));
            for (var index = 0; index < atk.Length; index++)
                placements.Add(new ReferenceAtlasPlacement(atk[index], AttackBounds(turns.Length, turnOrdinal, index / 4, index % 4)));

            var smallOrigin = SmallBounds(turns.Length, turnOrdinal, 0, 0);
            var attackOrigin = AttackBounds(turns.Length, turnOrdinal, 0, 0);
            sections.Add(new ReferenceAtlasSection
            {
                Name = (physicalSlot ? string.Empty : $"{ChineseTurn(turn)}转 ") + "48x48 移动与特技", Turn = turn, Action = "mov+spc",
                X = smallOrigin.X, Y = smallOrigin.Y, Width = 298, Height = 148
            });
            sections.Add(new ReferenceAtlasSection
            {
                Name = (physicalSlot ? string.Empty : $"{ChineseTurn(turn)}转 ") + "64x64 攻击", Turn = turn, Action = "atk",
                X = attackOrigin.X, Y = attackOrigin.Y, Width = 262, Height = 196
            });
        }
        return new ReferenceAtlasLayoutPlan(turns.Length == 1 ? 348 : 592, SLayoutId, FrameGutter,
            turns.Length, placements, sections);
    }

    private static DecodedFrame[] RequireFrames(IReadOnlyDictionary<string, DecodedFrame[]> groups, int turn,
        string action, int count, int size)
    {
        if (!groups.TryGetValue(action, out var frames))
            throw new InvalidDataException($"S 参考图缺少 {ChineseTurn(turn)}转 {action} 帧。");
        var ordered = frames.OrderBy(frame => frame.Descriptor.FrameIndex).ToArray();
        if (ordered.Length != count || !ordered.Select(frame => frame.Descriptor.FrameIndex).SequenceEqual(Enumerable.Range(0, count)))
            throw new InvalidDataException($"S 参考图 {ChineseTurn(turn)}转 {action} 帧号必须完整且唯一。");
        if (ordered.Any(frame => frame.Bitmap.Width != size || frame.Bitmap.Height != size))
            throw new InvalidDataException($"S 参考图 {action} 帧尺寸必须为 {size}x{size}。");
        return ordered;
    }

    private static Rectangle SmallBounds(int turnCount, int turnOrdinal, int row, int column)
    {
        var originX = turnCount == 1 ? 25 : 14;
        var originY = turnCount == 1 ? 0 : turnOrdinal * 150;
        return new Rectangle(originX + column * 50, originY + row * 50, 48, 48);
    }

    private static Rectangle AttackBounds(int turnCount, int turnOrdinal, int row, int column)
    {
        var originX = turnCount == 1 ? 43 : 316;
        var originY = turnCount == 1 ? 152 : turnOrdinal * 198;
        return new Rectangle(originX + column * 66, originY + row * 66, 64, 64);
    }

    private static string ChineseTurn(int turn) => turn switch { 1 => "一", 2 => "二", 3 => "三", _ => turn.ToString() };
}
