namespace Ccz.Shared;

/// <summary>Pure engine numbering rules shared by Data and image resource validation.</summary>
internal static class SImageNumberingRules
{
    internal const int JobCount = 80;
    internal const int FactionCount = 3;
    internal const int JobImageCount = JobCount * FactionCount;
    internal const int ThreeTurnPersonCount = 32;
    internal const int ThreeTurnImageEnd = JobImageCount + ThreeTurnPersonCount * 3;

    internal static int ResolveJobImageNumber(int jobId, int factionIndex = 0)
    {
        if (jobId is < 0 or >= JobCount) throw new ArgumentOutOfRangeException(nameof(jobId));
        if (factionIndex is < 0 or >= FactionCount) throw new ArgumentOutOfRangeException(nameof(factionIndex));
        return checked(jobId * FactionCount + factionIndex + 1);
    }

    internal static int GetPersonStageCount(int sId)
    {
        if (sId < 0) throw new ArgumentOutOfRangeException(nameof(sId));
        return sId is >= 1 and <= ThreeTurnPersonCount ? 3 : 1;
    }

    internal static int GetJobId(int physicalImageNumber)
    {
        if (physicalImageNumber is < 1 or > JobImageCount)
            throw new ArgumentOutOfRangeException(nameof(physicalImageNumber));
        return (physicalImageNumber - 1) / FactionCount;
    }

    internal static int GetFactionIndex(int physicalImageNumber)
    {
        if (physicalImageNumber is < 1 or > JobImageCount)
            throw new ArgumentOutOfRangeException(nameof(physicalImageNumber));
        return (physicalImageNumber - 1) % FactionCount;
    }

    internal static int ResolvePersonImageNumber(int sId, int jobId, int turn)
    {
        if (sId < 0) throw new ArgumentOutOfRangeException(nameof(sId));
        if (turn is < 1 or > 3) throw new ArgumentOutOfRangeException(nameof(turn));
        if (sId == 0) return ResolveJobImageNumber(jobId);
        return sId <= ThreeTurnPersonCount
            ? checked(JobImageCount + (sId - 1) * 3 + turn)
            : checked(ThreeTurnImageEnd + sId - ThreeTurnPersonCount);
    }

    /// <summary>S=0 can use any faction; a special S owns all its promotion images.</summary>
    internal static IReadOnlyList<int> GetAssignedPhysicalImageNumbers(int sId, int jobId)
        => sId == 0
            ? Enumerable.Range(0, FactionCount).Select(faction => ResolveJobImageNumber(jobId, faction)).ToArray()
            : Enumerable.Range(1, GetPersonStageCount(sId))
                .Select(turn => ResolvePersonImageNumber(sId, jobId, turn)).ToArray();

    internal static int GetMaximumCompletePersonSId(int commonPhysicalCount)
    {
        if (commonPhysicalCount < 0) throw new ArgumentOutOfRangeException(nameof(commonPhysicalCount));
        return Math.Min(ThreeTurnPersonCount, Math.Max(0, commonPhysicalCount - JobImageCount) / 3)
            + Math.Max(0, commonPhysicalCount - ThreeTurnImageEnd);
    }
}
