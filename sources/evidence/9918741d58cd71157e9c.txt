using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using DataManager.Core.Models;
using DataManager.Core.Binary;

namespace DataManager.Core.Profiles;

public sealed class ProfileRegistry
{
    private readonly Dictionary<string, ProfileConfig> _configs;
    private readonly JsonSerializerOptions _json = new()
    {
        PropertyNameCaseInsensitive = true,
        Converters = { new JsonStringEnumConverter() }
    };

    public ProfileRegistry() : this(useLegacyExtensionManifest: false)
    {
    }

    internal ProfileRegistry(bool useLegacyExtensionManifest, bool usePreSimplificationManifest = false, bool usePreConfiguration64Manifest = false)
    {
        _configs = LoadEmbeddedConfigs(useLegacyExtensionManifest, usePreSimplificationManifest, usePreConfiguration64Manifest);
        Profiles = _configs.Values
            .OrderBy(config => config.Version, StringComparer.Ordinal)
            .Select(ToProfile)
            .ToArray();
        foreach (var profile in Profiles)
        {
            _ = Resolve(profile.Id, profile.DefaultVariantId);
        }
    }

    public IReadOnlyList<DataProfile> Profiles { get; }

    public DataProfile GetProfile(string profileId)
        => Profiles.FirstOrDefault(profile => profile.Id.Equals(profileId, StringComparison.OrdinalIgnoreCase))
           ?? throw new KeyNotFoundException($"未知数据 Profile：{profileId}");

    public ResolvedProfile Resolve(string profileId, string? variantId = null)
    {
        var profile = GetProfile(profileId);
        var variant = profile.Variants.FirstOrDefault(item => item.Id.Equals(variantId ?? profile.DefaultVariantId, StringComparison.OrdinalIgnoreCase))
            ?? throw new KeyNotFoundException($"Profile {profileId} 不包含布局变体 {variantId}。");
        var config = _configs[profile.Id];
        var chain = GetInheritanceChain(config);
        var modules = new Dictionary<string, ModuleDefinition>(StringComparer.OrdinalIgnoreCase);
        var tables = new Dictionary<string, TableDefinition>(StringComparer.OrdinalIgnoreCase);
        foreach (var layer in chain)
        {
            foreach (var module in layer.Modules ?? [])
            {
                modules[module.Key] = new ModuleDefinition(module.Key, module.DisplayName, module.TableKeys);
            }
            foreach (var table in layer.Tables ?? [])
            {
                var existing = tables.GetValueOrDefault(table.Key);
                tables[table.Key] = BuildTable(table, existing, layer.Id);
            }
        }

        foreach (var layer in chain)
        {
            var variantConfig = layer.Variants?.FirstOrDefault(item => item.Id.Equals(variant.Id, StringComparison.OrdinalIgnoreCase));
            foreach (var table in variantConfig?.TableOverrides ?? [])
            {
                var existing = tables.GetValueOrDefault(table.Key)
                    ?? throw new InvalidDataException($"Profile {profileId} 的变体 {variant.Id} 覆盖了不存在的表 {table.Key}。");
                tables[table.Key] = BuildTable(table, existing, $"{layer.Id}/{variant.Id}");
            }
        }

        var orderedTables = tables.Values.Select(TextFieldConstraints.Apply).ToArray();
        Validate(orderedTables);
        return new ResolvedProfile
        {
            Profile = profile,
            Variant = variant,
            Tables = orderedTables,
            Modules = modules.Values.ToArray(),
            LayoutRevision = ComputeLayoutRevision(profile.Id, variant.Id, orderedTables)
        };
    }

    private Dictionary<string, ProfileConfig> LoadEmbeddedConfigs(bool useLegacyExtensionManifest, bool usePreSimplificationManifest, bool usePreConfiguration64Manifest)
    {
        var result = new Dictionary<string, ProfileConfig>(StringComparer.OrdinalIgnoreCase);
        var assembly = typeof(ProfileRegistry).Assembly;
        var suffix65 = usePreSimplificationManifest ? "ccz-6.5.before-simplification.json" : useLegacyExtensionManifest ? "ccz-6.5.extenddata-v1.json" : "ccz-6.5.json";
        var suffix66 = usePreSimplificationManifest ? "ccz-6.6.before-simplification.json" : useLegacyExtensionManifest ? "ccz-6.6.extenddata-v1.json" : "ccz-6.6.json";
        var suffix64 = usePreConfiguration64Manifest ? "ccz-6.4.before-configuration.json" : "ccz-6.4.json";
        var names = assembly.GetManifestResourceNames()
            .Where(name => name.EndsWith(suffix65, StringComparison.OrdinalIgnoreCase) || name.EndsWith(suffix66, StringComparison.OrdinalIgnoreCase) ||
                !useLegacyExtensionManifest && !usePreSimplificationManifest && name.EndsWith(suffix64, StringComparison.OrdinalIgnoreCase))
            .OrderBy(name => name, StringComparer.Ordinal)
            .ToArray();
        var expectedCount = useLegacyExtensionManifest || usePreSimplificationManifest ? 2 : 3;
        if (names.Length != expectedCount) throw new InvalidDataException($"应嵌入 {expectedCount} 个 Profile 配置，实际找到 {names.Length} 个。");
        foreach (var name in names)
        {
            using var stream = assembly.GetManifestResourceStream(name) ?? throw new InvalidDataException($"无法读取嵌入配置：{name}");
            var config = JsonSerializer.Deserialize<ProfileConfig>(stream, _json) ?? throw new InvalidDataException($"Profile 配置为空：{name}");
            if (string.IsNullOrWhiteSpace(config.Id)) throw new InvalidDataException($"Profile 配置缺少 id：{name}");
            result.Add(config.Id, config);
        }
        return result;
    }

    private DataProfile ToProfile(ProfileConfig config)
        => new()
        {
            Id = config.Id,
            Version = config.Version,
            DisplayName = config.DisplayName,
            DefaultVariantId = config.DefaultVariantId,
            Variants = (config.Variants ?? []).Select(variant => new ProfileVariant
            {
                Id = variant.Id,
                DisplayName = variant.DisplayName,
                LayoutId = variant.LayoutId,
                Fingerprints = (variant.Fingerprints ?? []).Select(fingerprint => new ProfileFingerprint
                {
                    SampleId = fingerprint.SampleId,
                    FileLengths = new Dictionary<string, long>(fingerprint.FileLengths ?? [], StringComparer.OrdinalIgnoreCase),
                    Sha256 = new Dictionary<string, string>(fingerprint.Sha256 ?? [], StringComparer.OrdinalIgnoreCase)
                }).ToList()
            }).ToArray()
        };

    private IReadOnlyList<ProfileConfig> GetInheritanceChain(ProfileConfig config)
    {
        var result = new List<ProfileConfig>();
        var visiting = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        void Add(ProfileConfig current)
        {
            if (!visiting.Add(current.Id)) throw new InvalidDataException($"Profile 继承循环：{current.Id}");
            if (!string.IsNullOrWhiteSpace(current.Inherits))
            {
                if (!_configs.TryGetValue(current.Inherits, out var parent)) throw new InvalidDataException($"Profile {current.Id} 的父级不存在：{current.Inherits}");
                Add(parent);
            }
            result.Add(current);
        }
        Add(config);
        return result;
    }

    private static TableDefinition BuildTable(TableConfig source, TableDefinition? existing, string sourceId)
    {
        var rowSize = source.RowSize ?? existing?.RowSize ?? throw Missing(source.Key, "rowSize");
        var fields = source.Fields != null ? ExpandFields(source.Fields) : existing?.Fields ?? throw Missing(source.Key, "fields");
        return new TableDefinition(
            source.Key,
            source.DisplayName ?? existing?.DisplayName ?? throw Missing(source.Key, "displayName"),
            source.FileName ?? existing?.FileName ?? throw Missing(source.Key, "fileName"),
            source.DataOffset ?? existing?.DataOffset ?? throw Missing(source.Key, "dataOffset"),
            source.RowCount ?? existing?.RowCount ?? throw Missing(source.Key, "rowCount"),
            rowSize,
            source.BeginId ?? existing?.BeginId ?? 0,
            fields,
            source.Module ?? existing?.Module ?? throw Missing(source.Key, "module"),
            source.ParentKey ?? existing?.ParentKey,
            source.RecordCodecKey ?? existing?.RecordCodecKey ?? "fixed-record-v1",
            source.VerificationLevel ?? existing?.VerificationLevel ?? VerificationLevel.InheritedUnverified,
            source.LayoutSource ?? existing?.LayoutSource ?? sourceId,
            source.Capability ?? existing?.Capability ?? TableCapability.Editable,
            source.CapabilityEvidence ?? existing?.CapabilityEvidence ?? string.Empty);
    }

    private static IReadOnlyList<TableFieldDefinition> ExpandFields(IEnumerable<FieldConfig> configs)
    {
        var result = new List<TableFieldDefinition>();
        foreach (var field in configs)
        {
            var names = field.Names is { Count: > 0 }
                ? field.Names
                : field.Count > 1
                    ? Enumerable.Range(0, field.Count).Select(index => string.Format(System.Globalization.CultureInfo.InvariantCulture, field.NamePattern ?? field.Name, index)).ToList()
                    : [field.Name];
            for (var index = 0; index < names.Count; index++)
            {
                var offset = field.Offset + index * (field.Stride ?? field.Size);
                var maximum = field.Maximum ?? field.Kind switch
                {
                    FieldKind.UInt16 => ushort.MaxValue,
                    FieldKind.UInt32 => uint.MaxValue,
                    _ => byte.MaxValue
                };
                result.Add(new TableFieldDefinition(names[index], offset, field.Size, field.Kind, field.Policy, field.Minimum ?? 0, maximum, field.ReferenceTable, field.CsvName));
            }
        }
        return result;
    }

    private static void Validate(IEnumerable<TableDefinition> tables)
    {
        var keys = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var table in tables)
        {
            if (!keys.Add(table.Key)) throw new InvalidDataException($"重复表 key：{table.Key}");
            if (table.RowCount <= 0 || table.RowSize <= 0 || table.DataOffset < 0) throw new InvalidDataException($"表 {table.Key} 的几何定义无效。");
            var fieldNames = new HashSet<string>(StringComparer.Ordinal);
            foreach (var field in table.Fields)
            {
                if (!fieldNames.Add(field.Name)) throw new InvalidDataException($"表 {table.Key} 包含重复字段：{field.Name}");
                if (field.Size < 0 || field.Offset < 0 || field.Offset + field.Size > table.RowSize)
                {
                    throw new InvalidDataException($"表 {table.Key} 字段 {field.Name} 越过行宽 {table.RowSize}。");
                }
            }
        }
    }

    // This is the v1 fingerprint contract. Keep its ordering and included values
    // stable: the frozen ExtendData manifests use it to identify existing CSVs
    // and byte history, rather than accepting arbitrary revision strings.
    internal static string ComputeLayoutRevision(string profileId, string variantId, IEnumerable<TableDefinition> tables)
    {
        var text = new StringBuilder().Append(profileId).Append('|').Append(variantId);
        foreach (var table in tables.OrderBy(table => table.Key, StringComparer.Ordinal))
        {
            text.Append('|').Append(table.Key).Append(':').Append(table.FileName).Append(':').Append(table.DataOffset).Append(':').Append(table.RowCount).Append(':').Append(table.RowSize).Append(':').Append(table.RecordCodecKey).Append(':').Append(table.Capability).Append(':').Append(table.CapabilityEvidence);
            foreach (var field in table.Fields) text.Append(';').Append(field.Name).Append('@').Append(field.Offset).Append('+').Append(field.Size).Append(':').Append(field.Kind).Append(':').Append(field.Policy);
        }
        return Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes(text.ToString())))[..16];
    }

    private static InvalidDataException Missing(string key, string property)
        => new($"表 {key} 缺少必需属性 {property}。");

    private sealed class ProfileConfig
    {
        public string Id { get; set; } = string.Empty;
        public string Version { get; set; } = string.Empty;
        public string DisplayName { get; set; } = string.Empty;
        public string? Inherits { get; set; }
        public string DefaultVariantId { get; set; } = string.Empty;
        public List<ModuleConfig>? Modules { get; set; }
        public List<TableConfig>? Tables { get; set; }
        public List<VariantConfig>? Variants { get; set; }
    }

    private sealed class ModuleConfig
    {
        public string Key { get; set; } = string.Empty;
        public string DisplayName { get; set; } = string.Empty;
        public List<string> TableKeys { get; set; } = [];
    }

    private sealed class VariantConfig
    {
        public string Id { get; set; } = string.Empty;
        public string DisplayName { get; set; } = string.Empty;
        public string LayoutId { get; set; } = string.Empty;
        public List<FingerprintConfig>? Fingerprints { get; set; }
        public List<TableConfig>? TableOverrides { get; set; }
    }

    private sealed class FingerprintConfig
    {
        public string SampleId { get; set; } = string.Empty;
        public Dictionary<string, long>? FileLengths { get; set; }
        public Dictionary<string, string>? Sha256 { get; set; }
    }

    private sealed class TableConfig
    {
        public string Key { get; set; } = string.Empty;
        public string? DisplayName { get; set; }
        [JsonPropertyName("file")] public string? FileName { get; set; }
        [JsonPropertyName("offset")] public long? DataOffset { get; set; }
        [JsonPropertyName("rows")] public int? RowCount { get; set; }
        public int? RowSize { get; set; }
        public int? BeginId { get; set; }
        public string? Module { get; set; }
        public string? ParentKey { get; set; }
        public string? RecordCodecKey { get; set; }
        public VerificationLevel? VerificationLevel { get; set; }
        public string? LayoutSource { get; set; }
        public TableCapability? Capability { get; set; }
        public string? CapabilityEvidence { get; set; }
        public List<FieldConfig>? Fields { get; set; }
    }

    private sealed class FieldConfig
    {
        public string Name { get; set; } = string.Empty;
        public List<string>? Names { get; set; }
        public string? NamePattern { get; set; }
        public int Count { get; set; } = 1;
        public int Offset { get; set; }
        public int Size { get; set; }
        public int? Stride { get; set; }
        public FieldKind Kind { get; set; }
        public FieldPolicy Policy { get; set; } = FieldPolicy.Editable;
        public long? Minimum { get; set; }
        public long? Maximum { get; set; }
        public string? ReferenceTable { get; set; }
        public string? CsvName { get; set; }
    }
}
