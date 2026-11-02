using Ccz.Shared;

namespace ImageManager.Core;

public interface ISPhysicalMappingService
{
    SPhysicalMapping Resolve(int sId, int jobId, int turn);
    IReadOnlySet<int> ResolveUsedPhysicalIds(IEnumerable<CharacterAssignment> assignments);
}

public interface ISLogicalAssetMappingService
{
    IReadOnlyList<SLogicalAssetMapping> Build(int commonPhysicalCount);
    IReadOnlyList<SLogicalAssetMapping> BuildJobs(int commonPhysicalCount);
    IReadOnlyList<SLogicalAssetMapping> BuildPersonAssignments(int commonPhysicalCount);
    SLogicalAssetMapping? Resolve(int sId, int commonPhysicalCount);
}

public sealed class SPhysicalMappingService : ISPhysicalMappingService
{
    public SPhysicalMapping Resolve(int sId, int jobId, int turn)
    {
        if (sId < 0) throw new ArgumentOutOfRangeException(nameof(sId));
        if (turn is < 1 or > 3) throw new ArgumentOutOfRangeException(nameof(turn));

        if (sId == 0)
        {
            // Jobs 0..59 already include promotion: every three consecutive
            // jobs are the three turns of one family. Each job owns an
            // ally/friend/enemy triplet. The later 20 jobs have one turn.
            var effectiveTurn = jobId < 60 ? jobId % 3 + 1 : 1;
            return new SPhysicalMapping(SImageNumberingRules.ResolveJobImageNumber(jobId), turn == effectiveTurn, effectiveTurn,
                jobId < 60 ? "按兵种 ID 读取对应转职我军图" : "兵种仅一转我军图");
        }

        var stages = SImageNumberingRules.GetPersonStageCount(sId);
        var effectiveStage = stages == 3 ? turn : 1;
        return new SPhysicalMapping(SImageNumberingRules.ResolvePersonImageNumber(sId, jobId, effectiveStage),
            stages == 3 || turn == 1, effectiveStage,
            stages == 3 ? "人物紧凑 S 编号对应三转特殊形象" : "人物紧凑 S 编号对应单转特殊形象");
    }

    public IReadOnlySet<int> ResolveUsedPhysicalIds(IEnumerable<CharacterAssignment> assignments)
    {
        var result = new HashSet<int>();
        foreach (var row in assignments)
            result.UnionWith(SImageNumberingRules.GetAssignedPhysicalImageNumbers(row.SId, row.JobId));
        return result;
    }
}

public sealed class SLogicalAssetMappingService : ISLogicalAssetMappingService
{
    public IReadOnlyList<SLogicalAssetMapping> Build(int commonPhysicalCount)
    {
        if (commonPhysicalCount < 0) throw new ArgumentOutOfRangeException(nameof(commonPhysicalCount));
        return Enumerable.Range(SImageNumberingRules.JobImageCount + 1,
                Math.Max(0, commonPhysicalCount - SImageNumberingRules.JobImageCount))
            .Select(imageNumber => new SLogicalAssetMapping(imageNumber, false,
                [new STurnPhysicalBinding(1, imageNumber)], commonPhysicalCount))
            .ToArray();
    }

    public SLogicalAssetMapping? Resolve(int sId, int commonPhysicalCount)
        => Build(commonPhysicalCount).FirstOrDefault(item => item.SId == sId);

    /// <summary>
    /// Both gallery modes use physical Unit image numbers. Job images occupy
    /// 1..240 and general images occupy 241 onward. Neither is a Data S ID.
    /// </summary>
    public IReadOnlyList<SLogicalAssetMapping> BuildJobs(int commonPhysicalCount)
    {
        if (commonPhysicalCount < 0) throw new ArgumentOutOfRangeException(nameof(commonPhysicalCount));
        var count = Math.Min(SImageNumberingRules.JobImageCount, commonPhysicalCount);
        return Enumerable.Range(1, count)
            .Select(imageNumber => new SLogicalAssetMapping(imageNumber, false,
                [new STurnPhysicalBinding(1, imageNumber)], commonPhysicalCount))
            .ToArray();
    }

    /// <summary>Compact Data S IDs, independent of the physical gallery. S=0 is contextual.</summary>
    public IReadOnlyList<SLogicalAssetMapping> BuildPersonAssignments(int commonPhysicalCount)
        => Enumerable.Range(1, SImageNumberingRules.GetMaximumCompletePersonSId(commonPhysicalCount))
            .Select(sId => new SLogicalAssetMapping(sId, SImageNumberingRules.GetPersonStageCount(sId) == 3,
                Enumerable.Range(1, SImageNumberingRules.GetPersonStageCount(sId))
                    .Select(turn => new STurnPhysicalBinding(turn,
                        SImageNumberingRules.ResolvePersonImageNumber(sId, 0, turn))).ToArray(), commonPhysicalCount))
            .ToArray();
}
