using System.Buffers.Binary;
using System.Globalization;
using System.Security.Cryptography;
using System.Text;
using Ccz.Shared;
using DataManager.Core.Binary;
using DataManager.Core.Domain;
using DataManager.Core.History;
using DataManager.Core.Models;

namespace DataManager.Core.Profiles;

/// <summary>Runtime evidence gates for layouts embedded in a modified executable.</summary>
public sealed class ProfileAugmentationService
{
    public const long SpecialQuoteOffset = 0x89C30;
    public const long RAssignmentOffset65 = 0xE1000;
    public const long SAssignmentOffset65 = 0xD2800;
    private const int AssignmentRows = 1024;
    private const int AssignmentWidth = 2;

    public ResolvedProfile Apply(string root, ResolvedProfile profile) => ApplyCore(root, profile, false);

    // Only used to reproduce the frozen, shipped 6.4 CSV/history identity.
    internal ResolvedProfile ApplyPreConfiguration64(string root, ResolvedProfile profile) => ApplyCore(root, profile, true);

    private ResolvedProfile ApplyCore(string root, ResolvedProfile profile, bool preConfiguration64)
    {
        if (string.IsNullOrWhiteSpace(root)) return profile;
        var path = ProjectFileLocator.Resolve(root, "Ekd5.exe");
        var executable = File.Exists(path) ? File.ReadAllBytes(path) : [];
        var is64 = profile.ProfileId.Equals("ccz-6.4", StringComparison.OrdinalIgnoreCase);
        var configuration64 = is64 && !preConfiguration64 ? Ccz64ConfigurationProbe.Inspect(executable) : null;
        var personalEffectNames = new EffectNamePoolProbe().Inspect(executable, is64 ? 180 : 255);
        var evidence = "特殊暴击人物映射缺少可验证的 PE 引用。";
        var supported = executable.Length > 0 && HasExecutableReference(executable, SpecialQuoteOffset, out evidence);
        if (configuration64 is not null)
        {
            supported = configuration64.SpecialCriticalMap;
            evidence = configuration64.CriticalEvidence;
        }
        var table = new TableDefinition("person-critical-special-map", "特殊暴击人物分配", "Ekd5.exe",
            SpecialQuoteOffset, 21, 4, 0,
            [new TableFieldDefinition("人物ID", 0, 4, FieldKind.UInt32, Maximum: 1024, ReferenceTable: "persons")],
            "人物", VerificationLevel: supported ? VerificationLevel.SourceReviewed : VerificationLevel.InheritedUnverified,
            Capability: supported ? TableCapability.Editable : TableCapability.Unavailable, CapabilityEvidence: evidence);
        var is66 = profile.ProfileId.Equals("ccz-6.6", StringComparison.OrdinalIgnoreCase);
        var assignments65 = !is66 ? EmbeddedEngineLayoutProbe.InspectAssignments65(executable) : null;
        var assignmentEvidence = InspectAssignmentLayout(root, profile, executable, assignments65);
        var assignments66 = is66 ? EmbeddedEngineLayoutProbe.InspectAssignments(executable) : null;
        var terrain66 = is66 || is64 ? EmbeddedEngineLayoutProbe.InspectStrategyTerrain(executable) : null;
        var ini66 = is66 ? ReadAssignmentIni(root, assignments66!.R.Offset, assignments66.S.Offset) : default;
        var tables = profile.Tables.Where(item => item.Key != table.Key).Select(item =>
        {
            item = AugmentExtensionGeometry(root, item);
            if (configuration64 is not null)
            {
                if (item.Key == "person-retreat-quotes")
                    return item with { DataOffset = 130000, RowCount = 49, RowSize = 200,
                        Capability = configuration64.RetreatQuotes ? TableCapability.Editable : TableCapability.Unavailable,
                        CapabilityEvidence = configuration64.RetreatEvidence,
                        VerificationLevel = configuration64.RetreatQuotes ? VerificationLevel.SourceReviewed : VerificationLevel.InheritedUnverified };
                if (item.Key == "persons")
                    return item with { Fields = item.Fields.Select(field => field.Offset >= 27
                            ? field with { Policy = configuration64.PersonDefaults ? FieldPolicy.Editable : FieldPolicy.Preserve } : field).ToArray(),
                        CapabilityEvidence = configuration64.PersonEvidence };
                if (item.Key == "detailed-job-growth")
                    return item with { Fields = item.Fields.Select(field => field.Offset >= 9
                            ? field with { Policy = configuration64.EquipmentPermissions ? FieldPolicy.Editable : FieldPolicy.Preserve } : field).ToArray(),
                        CapabilityEvidence = configuration64.PermissionEvidence };
            }
            if (item.Key == "effect-names")
                return item with { DataOffset = personalEffectNames.Success ? personalEffectNames.FileOffset!.Value : item.DataOffset,
                    Capability = is64 && !personalEffectNames.Success ? TableCapability.Unavailable : TableCapability.ReadOnly,
                    CapabilityEvidence = personalEffectNames.Message,
                    VerificationLevel = personalEffectNames.Success ? VerificationLevel.SourceReviewed : VerificationLevel.InheritedUnverified };
            if (is66 && (item.Key is "person-r-assign" or "person-s-assign"))
            {
                var probe = item.Key == "person-r-assign" ? assignments66!.R : assignments66!.S;
                var verified = probe.Verified && !(ini66.HasAssignmentKeys && !ini66.MatchesKnownLayout);
                return item with { DataOffset = verified ? probe.Offset : item.DataOffset, RowCount = AssignmentRows, RowSize = AssignmentWidth,
                    Capability = verified ? TableCapability.Editable : TableCapability.Unavailable,
                    CapabilityEvidence = probe.Evidence + (ini66.HasAssignmentKeys ? " " + ini66.Evidence : " 本项目无指定器 INI；以独立消费者/PE 映射为准。"),
                    VerificationLevel = verified ? VerificationLevel.SourceReviewed : VerificationLevel.InheritedUnverified };
            }
            if ((is66 || is64) && item.Key == "strategy-terrain-availability")
                return item with { DataOffset = terrain66!.Verified ? terrain66.Offset : item.DataOffset, RowCount = 30, RowSize = 1,
                    Capability = terrain66.Verified ? TableCapability.Editable : TableCapability.Unavailable,
                    CapabilityEvidence = terrain66.Evidence,
                    VerificationLevel = terrain66.Verified ? VerificationLevel.SourceReviewed : VerificationLevel.InheritedUnverified };
            return item.Key is "person-r-assign" or "person-s-assign"
                ? item with { DataOffset = assignmentEvidence.Capability == TableCapability.Editable && assignments65 is { R.Verified: true, S.Verified: true }
                        ? item.Key == "person-r-assign" ? assignments65.R.Offset : assignments65.S.Offset : item.DataOffset,
                    Capability = assignmentEvidence.Capability, CapabilityEvidence = assignmentEvidence.Evidence,
                    VerificationLevel = assignmentEvidence.Capability == TableCapability.Editable ? VerificationLevel.SourceReviewed : VerificationLevel.InheritedUnverified }
                : item;
        }).Append(table).ToArray();
        tables = ExtendedItemLayoutProbe.Apply(root, tables, executable).ToArray();
        var equipmentTables = EquipmentTypeCatalogService.BuildTables(executable);
        tables = tables.Where(item => !equipmentTables.Any(equipment => equipment.Key == item.Key)).Concat(equipmentTables).ToArray();
        tables = TextConsumerEvidence.Apply(tables, executable).ToArray();
        var modules = profile.Modules.Select(module => module.Key == "人物"
            ? module with { TableKeys = module.TableKeys.Where(key => key != table.Key).Append(table.Key).ToArray() }
            : module.Key == "宝物" ? module with { TableKeys = module.TableKeys.Concat(equipmentTables.Select(item => item.Key)).Distinct().ToArray() }
            : module).ToArray();
        // Evidence text/SHA changes after a valid save. Only capability and geometry
        // affect the layout identity, so a checked history chain keeps undo/redo valid.
        var geometry = string.Join("|", tables.Where(item => item.Key is "person-r-assign" or "person-s-assign" or "person-critical-special-map" or "strategy-terrain-availability" or "equipment-type-names" or "equipment-type-display")
            .OrderBy(item => item.Key).Select(item => $"{item.Key}:{item.Capability}:{item.DataOffset}:{item.RowCount}:{item.RowSize}"));
        if (configuration64 is not null)
            geometry += $"|64-configuration:{configuration64.RetreatQuotes}:{configuration64.PersonDefaults}:{configuration64.EquipmentPermissions}:{configuration64.SpecialCriticalMap}";
        // Keep existing history identities when extension geometry is unchanged.
        // Actual short/long, complete physical files get their own layout identity.
        var extensionChanges = tables.Where(item => IsExtension(item.Key) && profile.Tables.Any(original =>
            original.Key == item.Key && (original.RowCount != item.RowCount || original.Capability != item.Capability)))
            .OrderBy(item => item.Key).Select(item => $"{item.Key}:{item.Capability}:{item.DataOffset}:{item.RowCount}:{item.RowSize}").ToArray();
        if (extensionChanges.Length > 0) geometry += "|" + string.Join("|", extensionChanges);
        var itemChanges = tables.Where(item => item.Key is "items-high" or "item-description-high" or "items-extended" or "item-description-extended")
            .Where(item => profile.Tables.Any(original => original.Key == item.Key &&
                (original.FileName != item.FileName || original.DataOffset != item.DataOffset || original.RowCount != item.RowCount ||
                 original.RecordCodecKey != item.RecordCodecKey || original.Capability != item.Capability)))
            .OrderBy(item => item.Key).Select(item => $"{item.Key}:{item.FileName}:{item.DataOffset}:{item.RowCount}:{item.RowSize}:{item.RecordCodecKey}:{item.Capability}").ToArray();
        if (itemChanges.Length > 0) geometry += "|item-extension:" + string.Join("|", itemChanges);
        var revision = Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(profile.LayoutRevision + "|" + geometry)))[..16];
        return new ResolvedProfile { Profile = profile.Profile, Variant = profile.Variant, Tables = tables, Modules = modules, LayoutRevision = revision };
    }

    private static (TableCapability Capability, string Evidence) InspectAssignmentLayout(string root, ResolvedProfile profile, byte[] executable,
        EmbeddedEngineLayoutProbe.Assignments? consumers)
    {
        if (profile.ProfileId is not ("ccz-6.4" or "ccz-6.5"))
            return (TableCapability.Unavailable, "6.6 R/S 指定尚无独立布局证据，禁止套用 6.5 System.ini 或固定偏移。");
        var version = profile.Profile.Version;
        var r = profile.Tables.FirstOrDefault(item => item.Key == "person-r-assign");
        var s = profile.Tables.FirstOrDefault(item => item.Key == "person-s-assign");
        if (r == null || s == null || r.DataOffset != RAssignmentOffset65 || s.DataOffset != SAssignmentOffset65 ||
            r.RowCount != AssignmentRows || s.RowCount != AssignmentRows || r.RowSize != AssignmentWidth || s.RowSize != AssignmentWidth)
            return (TableCapability.Unavailable, $"{version} R/S 表几何与已验证的 1024×UInt16 布局不一致，未开放偏移覆盖。");
        var dynamicVerified = consumers is { R.Verified: true, S.Verified: true };
        if (!dynamicVerified && executable.LongLength < Math.Max(r.EndOffsetExclusive, s.EndOffsetExclusive))
            return (TableCapability.Unavailable, "Ekd5.exe 长度不足，R/S 指定表越过文件边界。");

        var ini = dynamicVerified ? ReadAssignmentIni(root, consumers!.R.Offset, consumers.S.Offset) : ReadAssignmentIni(root);
        if (ini.HasAssignmentKeys && !ini.MatchesKnownLayout)
            return (TableCapability.Unavailable, ini.Evidence);
        var knownHashes = profile.Profile.Variants.SelectMany(variant => variant.Fingerprints)
            .Where(fingerprint => fingerprint.Sha256.ContainsKey("Ekd5.exe"))
            .Select(fingerprint => fingerprint.Sha256["Ekd5.exe"]).ToHashSet(StringComparer.OrdinalIgnoreCase);
        var currentHash = HashService.Sha256(executable);
        if (knownHashes.Contains(currentHash))
            return (TableCapability.Editable, $"Ekd5.exe SHA-256 匹配已验证的 {version} 原样样本；R +0xE1000、S +0xD2800，1024×UInt16 边界已核对。" +
                (ini.MatchesKnownLayout ? " 本项目 System.ini FileHead/RFileHead 与样本一致。" : " 本项目未提供指定器 INI，沿用已验证样本几何。"));
        if (TryRecoverVerifiedExecutable(root, profile, executable, knownHashes, out var historyEvidence))
            return (TableCapability.Editable, historyEvidence + "；R/S 沿用已验证样本几何，保存后的 SHA 变化不改变布局身份。");
        if (dynamicVerified)
            return (TableCapability.Editable, consumers!.R.Evidence + " " + consumers.S.Evidence +
                (ini.HasAssignmentKeys ? " " + ini.Evidence : " 无需 SHA 白名单或指定器 INI；本项目完整消费函数与 PE 可写节映射构成独立证据。"));
        if (!ini.MatchesKnownLayout)
            return (TableCapability.Unavailable, "未知 Ekd5.exe SHA-256，且缺少本项目 System.ini 的 FileHead/RFileHead 布局证据；不读取或写入猜测的 R/S 偏移。");
        if (!ValidateAssignmentResources(root, executable, out var resourceEvidence))
            return (TableCapability.Unavailable, "未知 Ekd5.exe SHA-256；" + ini.Evidence + "；" + resourceEvidence);
        return (TableCapability.ReadOnly, ini.Evidence + "；" + resourceEvidence +
            "。目录与数值检查不能证明未知引擎的地址引用，R/S 当前只读；取得独立布局证据前不开放写入。");
    }

    private static bool IsExtension(string key)
        => key is "effect-archive" or "effect-messages" or "strategy-study-extended" or "forge";

    private static TableDefinition AugmentExtensionGeometry(string root, TableDefinition table)
    {
        if (!IsExtension(table.Key)) return table;
        var path = ProjectFileLocator.Resolve(root, table.FileName);
        if (!File.Exists(path)) return table;
        var length = new FileInfo(path).Length;
        var maximumRows = table.Key == "effect-messages" ? 256 : 1024;
        if (table.DataOffset != 0 || table.RowSize <= 0 || length == 0 || length % table.RowSize != 0 ||
            length / table.RowSize > maximumRows)
            return table with { Capability = TableCapability.Unavailable,
                CapabilityEvidence = $"{table.FileName} 长度 {length} 不能组成 1..{maximumRows} 条完整的 {table.RowSize} 字节无头记录；禁止按默认行数截断读取。" };
        var rows = checked((int)(length / table.RowSize));
        return table with { RowCount = rows,
            CapabilityEvidence = $"{table.FileName} 为无头定宽物理表：长度 {length} = {rows}×{table.RowSize}；完整行边界已核对，保留未拆字段。" };
    }

    private static (bool HasAssignmentKeys, bool MatchesKnownLayout, string Evidence) ReadAssignmentIni(string root,
        long expectedR = RAssignmentOffset65, long expectedS = SAssignmentOffset65)
    {
        var paths = new[] { Path.Combine(root, "System.ini"), Path.Combine(root, "RS", "System.ini") }.Where(File.Exists).ToArray();
        var found = false;
        foreach (var path in paths)
        {
            var values = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
            foreach (var rawLine in File.ReadLines(path, Encoding.Latin1))
            {
                var line = rawLine.Split(';', '#')[0].Trim();
                var separator = line.IndexOf('=');
                if (separator <= 0) continue;
                var key = line[..separator].Trim();
                if (!key.Equals("FileHead", StringComparison.OrdinalIgnoreCase) && !key.Equals("RFileHead", StringComparison.OrdinalIgnoreCase)) continue;
                found = true;
                var value = line[(separator + 1)..].Trim();
                if (values.TryGetValue(key, out var prior) && !prior.Equals(value, StringComparison.OrdinalIgnoreCase))
                    return (true, false, $"{Path.GetRelativePath(root, path)} 的 {key} 重复且值冲突，R/S 指定不可用。");
                values[key] = value;
            }
            if (values.Count == 0) continue;
            if (!TryIniHex(values.GetValueOrDefault("FileHead"), out var s) || !TryIniHex(values.GetValueOrDefault("RFileHead"), out var r))
                return (true, false, $"{Path.GetRelativePath(root, path)} 的 FileHead/RFileHead 缺失或不是十六进制偏移，R/S 指定不可用。");
            if (s != expectedS || r != expectedR)
                return (true, false, $"{Path.GetRelativePath(root, path)} 的 FileHead=0x{s:X}/RFileHead=0x{r:X} 与已验证几何冲突，禁止自动套用或移动 R/S 表。");
        }
        return (found, found, found ? $"本项目 System.ini 的 FileHead={expectedS:X}、RFileHead={expectedR:X} 已核对" : "未提供本项目形象指定器 System.ini");
    }

    private static bool TryIniHex(string? text, out long value)
    {
        value = 0;
        if (string.IsNullOrWhiteSpace(text)) return false;
        var input = text.Trim();
        if (input.StartsWith("0x", StringComparison.OrdinalIgnoreCase)) input = input[2..];
        return long.TryParse(input, NumberStyles.AllowHexSpecifier, CultureInfo.InvariantCulture, out value) && value >= 0;
    }

    private static bool TryRecoverVerifiedExecutable(string root, ResolvedProfile profile, byte[] executable, IReadOnlySet<string> knownHashes, out string evidence)
    {
        evidence = string.Empty;
        var history = new HistoryStore().Load(root).Where(entry => entry.SchemaVersion == "2.0" &&
                entry.ProfileId.Equals(profile.ProfileId, StringComparison.OrdinalIgnoreCase) && entry.VariantId.Equals(profile.VariantId, StringComparison.OrdinalIgnoreCase) &&
                entry.Status is HistoryStatus.Active or HistoryStatus.Reverted)
            .OrderByDescending(entry => entry.CreatedAt).SelectMany(entry => entry.Files)
            .Where(file => Path.GetFileName(file.RelativePath).Equals("Ekd5.exe", StringComparison.OrdinalIgnoreCase)).ToArray();
        var current = executable;
        var currentHash = HashService.Sha256(current);
        var visited = new HashSet<string>(StringComparer.OrdinalIgnoreCase) { currentHash };
        for (var step = 0; step < history.Length; step++)
        {
            byte[]? prior = null;
            string? priorHash = null;
            foreach (var file in history.Where(file => file.FileLength == current.LongLength && file.AfterHash.Equals(currentHash, StringComparison.OrdinalIgnoreCase)))
            {
                var candidate = current.ToArray();
                var valid = true;
                long previousEnd = -1;
                foreach (var chunk in file.Chunks.OrderBy(chunk => chunk.Offset))
                {
                    if (chunk.OldBytes.Length != chunk.NewBytes.Length || chunk.Length == 0 || chunk.Offset < 0 || chunk.Offset < previousEnd ||
                        chunk.Offset > candidate.LongLength - chunk.Length || !candidate.AsSpan((int)chunk.Offset, chunk.Length).SequenceEqual(chunk.NewBytes))
                    { valid = false; break; }
                    chunk.OldBytes.CopyTo(candidate, (int)chunk.Offset);
                    previousEnd = chunk.Offset + chunk.Length;
                }
                if (!valid || !HashService.Sha256(candidate).Equals(file.BeforeHash, StringComparison.OrdinalIgnoreCase)) continue;
                prior = candidate;
                priorHash = file.BeforeHash;
                break;
            }
            if (prior == null || priorHash == null || !visited.Add(priorHash)) return false;
            if (knownHashes.Contains(priorHash))
            {
                evidence = $"通过 {step + 1} 条逐字节/前后 SHA-256 校验的本项目保存历史回溯到已验证 {profile.Profile.Version} EXE 样本";
                return true;
            }
            current = prior;
            currentHash = priorHash;
        }
        return false;
    }

    private static bool ValidateAssignmentResources(string root, byte[] executable, out string evidence)
    {
        evidence = string.Empty;
        try
        {
            var rCount = ProbeE5Directory(ProjectFileLocator.Resolve(root, "Pmapobj.e5"), 48 * 64 * 20);
            if (rCount % 2 != 0) throw new InvalidDataException("Pmapobj.e5 不是完整正反面配对资源");
            var sCount = new[] { ("Unit_mov.e5", 48 * 48 * 11), ("Unit_atk.e5", 64 * 64 * 12), ("Unit_spc.e5", 48 * 48 * 5) }
                .Select(item => ProbeE5Directory(ProjectFileLocator.Resolve(root, item.Item1), item.Item2)).Min();
            var dataPath = ProjectFileLocator.Resolve(root, "Data.e5");
            var data = File.ReadAllBytes(dataPath);
            if (data.Length < 396 + AssignmentRows * 32) throw new InvalidDataException("Data.e5 人物样本长度不足");
            var nonzeroR = false;
            var nonzeroS = false;
            for (var index = 0; index < AssignmentRows; index++)
            {
                var r = BinaryPrimitives.ReadUInt16LittleEndian(executable.AsSpan((int)RAssignmentOffset65 + index * AssignmentWidth, AssignmentWidth));
                var s = BinaryPrimitives.ReadUInt16LittleEndian(executable.AsSpan((int)SAssignmentOffset65 + index * AssignmentWidth, AssignmentWidth));
                var job = data[396 + index * 32 + 26];
                var sPhysical = SImageNumberingRules.GetAssignedPhysicalImageNumbers(s, job).Max();
                if ((long)(r + 1) * 2 > rCount || sPhysical > sCount)
                    throw new InvalidDataException($"人物 {index} 的 R/S 数值超出完整资源组范围（R{r}/S{s}）");
                nonzeroR |= r > 0;
                nonzeroS |= s > 0;
            }
            if (!nonzeroR || !nonzeroS) throw new InvalidDataException("R/S 样本全零，不能确认为人物指定表");
            evidence = $"R/S 三资源 E5 目录边界/声明帧尺寸与 1024 项人物数值已核对（R {rCount / 2} 组，S {sCount} 物理槽；未证明未知 EXE 引用）";
            return true;
        }
        catch (Exception ex) when (ex is IOException or InvalidDataException or UnauthorizedAccessException or ArgumentException or OverflowException)
        {
            evidence = "R/S 资源或样本证据不足：" + ex.Message;
            return false;
        }
    }

    private static int ProbeE5Directory(string path, int minimumDecodedLength)
    {
        using var stream = File.OpenRead(path);
        if (stream.Length < 0x110 + 12) throw new InvalidDataException($"{Path.GetFileName(path)} 缺少 E5 索引");
        stream.Position = 0x110;
        var first = new byte[12];
        stream.ReadExactly(first);
        var payloadStart = BinaryPrimitives.ReadUInt32BigEndian(first.AsSpan(8));
        var directoryLength = (long)payloadStart - 0x110;
        var trailer = directoryLength % 12;
        if (payloadStart > stream.Length || directoryLength < 12 || trailer is not (0 or 4) || directoryLength > int.MaxValue)
            throw new InvalidDataException($"{Path.GetFileName(path)} E5 目录边界不成立");
        var directory = new byte[(int)directoryLength];
        stream.Position = 0x110;
        stream.ReadExactly(directory);
        if (trailer == 4 && directory.AsSpan(directory.Length - 4).IndexOfAnyExcept((byte)0) >= 0)
            throw new InvalidDataException($"{Path.GetFileName(path)} E5 目录尾不是零");
        var count = (directory.Length - (int)trailer) / 12;
        for (var index = 0; index < count; index++)
        {
            var slot = directory.AsSpan(index * 12, 12);
            var stored = BinaryPrimitives.ReadUInt32BigEndian(slot);
            var decoded = BinaryPrimitives.ReadUInt32BigEndian(slot[4..]);
            var offset = BinaryPrimitives.ReadUInt32BigEndian(slot[8..]);
            if (stored == 0 || decoded < minimumDecodedLength || offset < payloadStart || (long)offset + stored > stream.Length)
                throw new InvalidDataException($"{Path.GetFileName(path)} 第 {index + 1} 项边界或声明帧尺寸不成立");
        }
        return count;
    }

    public static bool HasExecutableReference(byte[] bytes, long targetOffset, out string evidence)
    {
        evidence = "Ekd5.exe 不是完整的 PE32 文件，映射不可用。";
        try
        {
            if (bytes.Length < 0x40 || bytes[0] != 'M' || bytes[1] != 'Z') return false;
            var pe = BinaryPrimitives.ReadInt32LittleEndian(bytes.AsSpan(0x3C, 4));
            if (pe < 0 || pe > bytes.Length - 24 || BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(pe, 4)) != 0x4550) return false;
            var count = BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(pe + 6, 2));
            var optionalSize = BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(pe + 20, 2));
            var optional = pe + 24;
            if (optionalSize < 32 || optional > bytes.Length - optionalSize || BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(optional, 2)) != 0x10B) return false;
            var imageBase = BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(optional + 28, 4));
            var sections = new List<(uint Rva, uint Size, uint Raw, uint Flags)>();
            for (var index = 0; index < count; index++)
            {
                var position = optional + optionalSize + index * 40;
                if (position > bytes.Length - 40) return false;
                sections.Add((BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(position + 12, 4)),
                    BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(position + 16, 4)),
                    BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(position + 20, 4)),
                    BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(position + 36, 4))));
            }
            if (targetOffset < 0 || targetOffset + 84 > bytes.Length) return false;
            var containing = sections.FirstOrDefault(section => targetOffset >= section.Raw && targetOffset + 84 <= section.Raw + (long)section.Size);
            if (containing.Size == 0) return false;
            var va = checked(imageBase + containing.Rva + (uint)(targetOffset - containing.Raw));
            var pointer = BitConverter.GetBytes(va);
            foreach (var section in sections.Where(section => (section.Flags & 0x20000000u) != 0))
            {
                if (section.Raw >= bytes.Length || section.Size > int.MaxValue) continue;
                var length = Math.Min((int)section.Size, bytes.Length - (int)section.Raw);
                var relative = bytes.AsSpan((int)section.Raw, length).IndexOf(pointer);
                if (relative < 0) continue;
                // Reject unrelated data that happens to contain a pointer.
                for (var slot = 0; slot < 21; slot++)
                    if (BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan((int)targetOffset + slot * 4, 4)) > 1024)
                    { evidence = "特殊人物槽包含超出 0..1024 的值，布局验证失败。"; return false; }
                evidence = $"PE 可执行节 +0x{section.Raw + relative:X} 引用 VA 0x{va:X8}；21 个 UInt32 人物 ID 已校验。";
                return true;
            }
            evidence = $"没有找到指向 VA 0x{va:X8}（文件 +0x{targetOffset:X}）的可执行节引用。";
            return false;
        }
        catch (Exception ex) when (ex is ArgumentException or OverflowException)
        { evidence = "PE 布局验证失败：" + ex.Message; return false; }
    }
}
