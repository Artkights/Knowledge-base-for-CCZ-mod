using System.Data;
using DataManager.Core.Models;

namespace DataManager.Core.Binary;

public sealed class BinaryTableReader
{
    private readonly RecordCodecRegistry _codecs;

    public BinaryTableReader(RecordCodecRegistry? codecs = null)
    {
        _codecs = codecs ?? new RecordCodecRegistry();
    }

    public TableValidation Validate(string rootPath, TableDefinition definition)
    {
        if (definition.Capability != TableCapability.Unavailable &&
            (definition.Key == "items-extended" && definition.FileName.Equals("Item.e5", StringComparison.OrdinalIgnoreCase) ||
             definition.Key == "item-description-extended" && definition.FileName.Equals("Itemmsg.e5", StringComparison.OrdinalIgnoreCase)))
            return ValidateRootExtensionTable(rootPath, definition);
        var path = ProjectFileLocator.Resolve(rootPath, definition.FileName);
        if (definition.Capability == TableCapability.Unavailable)
        {
            // A table without layout evidence may retain inherited geometry
            // in the profile for diagnostics. Never interpret those bytes.
            return new TableValidation
            {
                Definition = definition,
                Path = path,
                FileExists = File.Exists(path),
                Message = string.IsNullOrWhiteSpace(definition.CapabilityEvidence)
                    ? "不可用：未提供布局证据"
                    : $"不可用：{definition.CapabilityEvidence}"
            };
        }
        if (!File.Exists(path))
        {
            return new TableValidation { Definition = definition, Path = path, FileExists = false, Message = "文件不存在" };
        }

        var length = new FileInfo(path).Length;
        var hasEnough = length >= definition.EndOffsetExclusive;
        return new TableValidation
        {
            Definition = definition,
            Path = path,
            FileExists = true,
            ActualLength = length,
            HasEnoughBytes = hasEnough,
            Message = !hasEnough
                ? $"文件长度不足，需要至少 {definition.EndOffsetExclusive} 字节"
                : definition.Capability == TableCapability.Editable
                    ? "可读取"
                    : $"可读取（只读：{definition.CapabilityEvidence}）"
        };
    }

    /// <summary>
    /// Item.e5 is deliberately ambiguous: the root file is the optional
    /// 256-row data table while E5\Item.e5 is an indexed icon archive.  A
    /// filename-only resolver would accept the icon archive whenever the root
    /// data file is absent because it is usually larger than the required
    /// number of bytes.  Require the root path and exact extension geometry
    /// before exposing either extended table to the workspace.
    /// </summary>
    private static TableValidation ValidateRootExtensionTable(string rootPath, TableDefinition definition)
    {
        var root = Directory.Exists(rootPath)
            ? Directory.EnumerateFiles(rootPath).FirstOrDefault(path =>
                Path.GetFileName(path).Equals(definition.FileName, StringComparison.OrdinalIgnoreCase))
            : null;
        var e5 = Directory.Exists(Path.Combine(rootPath, "E5"))
            ? Directory.EnumerateFiles(Path.Combine(rootPath, "E5")).FirstOrDefault(path =>
                Path.GetFileName(path).Equals(definition.FileName, StringComparison.OrdinalIgnoreCase))
            : null;
        var expected = definition.EndOffsetExclusive;
        if (root != null)
        {
            var length = new FileInfo(root).Length;
            if (length == expected)
                return new TableValidation
                {
                    Definition = definition, Path = root, FileExists = true,
                    ActualLength = length, HasEnoughBytes = true,
                    Message = e5 == null
                        ? $"根目录 {definition.FileName}：{definition.RowCount}×{definition.RowSize} 扩展数据"
                        : $"根目录 {definition.FileName}：{definition.RowCount}×{definition.RowSize} 扩展数据；E5\\{definition.FileName} 同名文件按独立档案处理。"
                };
            return new TableValidation
            {
                Definition = definition, Path = root, FileExists = true,
                ActualLength = length, HasEnoughBytes = false,
                Message = e5 == null
                    ? $"根目录 {definition.FileName} 几何不符：实际 {length} 字节，需要精确 {expected} 字节。"
                    : $"根目录 {definition.FileName} 几何不符：实际 {length} 字节，需要精确 {expected} 字节；E5\\{definition.FileName} 不能作为扩展数据。"
            };
        }
        var missingPath = Path.Combine(rootPath, definition.FileName);
        return new TableValidation
        {
            Definition = definition, Path = missingPath, FileExists = false,
            ActualLength = e5 == null ? 0 : new FileInfo(e5).Length,
            HasEnoughBytes = false,
            Message = e5 == null
                ? $"根目录缺少 {definition.FileName}（需要 {expected} 字节扩展表）。"
                : $"仅发现 E5\\{definition.FileName}（{new FileInfo(e5).Length} 字节）；它是 E5 档案，不作为根目录扩展表。"
        };
    }

    public TableDocument Read(string rootPath, TableDefinition definition)
    {
        var validation = Validate(rootPath, definition);
        if (!validation.IsUsable)
        {
            throw new InvalidDataException($"{definition.DisplayName}：{validation.Message}（{definition.FileName}）");
        }

        return ReadBytes(validation.Path, definition, File.ReadAllBytes(validation.Path));
    }

    /// <summary>Decode a complete candidate using exactly the same path as reopening the project.</summary>
    public TableDocument ReadBytes(string filePath, TableDefinition definition, byte[] bytes)
    {
        if (definition.Capability == TableCapability.Unavailable || bytes.LongLength < definition.EndOffsetExclusive)
            throw new InvalidDataException($"{definition.DisplayName}：候选文件不满足完整表的读取条件。");
        var codec = _codecs.Get(definition.RecordCodecKey);
        var table = new DataTable(definition.DisplayName);
        var textDecodeWarnings = new List<string>();
        table.ExtendedProperties["TextDecodeWarnings"] = textDecodeWarnings;
        table.Columns.Add("ID", typeof(int));
        table.Columns["ID"]!.ReadOnly = true;
        if (definition.Key == "job-series-attributes")
        {
            table.Columns.Add("属性", typeof(string));
            table.Columns["属性"]!.ReadOnly = true;
        }
        foreach (var field in definition.Fields.Where(field => field.Policy != FieldPolicy.Preserve && field.Size != 0))
        {
            var type = field.Kind switch
            {
                FieldKind.FixedString => typeof(string),
                FieldKind.UInt16 => typeof(int),
                FieldKind.UInt8 => typeof(int),
                FieldKind.UInt32 => typeof(long),
                FieldKind.RawBytes => typeof(string),
                _ => typeof(string)
            };
            table.Columns.Add(field.Name, type);
            table.Columns[field.Name]!.ExtendedProperties["Field"] = field;
            table.Columns[field.Name]!.ReadOnly = definition.Capability != TableCapability.Editable || field.Policy == FieldPolicy.ReadOnly;
        }

        for (var rowIndex = 0; rowIndex < definition.RowCount; rowIndex++)
        {
            var rowOffset = checked((int)(definition.DataOffset + (long)rowIndex * definition.RowSize));
            var rowBytes = bytes.AsSpan(rowOffset, definition.RowSize);
            var values = new object?[table.Columns.Count];
            values[0] = definition.BeginId + rowIndex;
            var columnIndex = 1;
            if (definition.Key == "job-series-attributes")
            {
                values[columnIndex++] = rowIndex switch
                {
                    0 => "移动声音",
                    1 => "移动速度",
                    2 => "攻击声音",
                    3 => "远程兵种",
                    4 => "攻击延迟",
                    5 => "兵种类型",
                    6 => "策略伤害",
                    7 => "参与围攻",
                    _ => $"属性{rowIndex}"
                };
            }
            foreach (var field in definition.Fields.Where(field => field.Policy != FieldPolicy.Preserve && field.Size != 0))
            {
                try
                {
                    var decoded = codec.Decode(rowBytes, field);
                    if (field.Kind == FieldKind.FixedString && decoded is string text && EncodingService.HasPreservedInvalidBytes(text))
                        textDecodeWarnings.Add($"{definition.DisplayName}（{definition.Key}）ID={definition.BeginId + rowIndex} 字段“{field.Name}”含无效 GBK 字节（文件偏移 0x{rowOffset + field.Offset:X}）；未修改时保留原始字节，编辑该文本须替换损坏字符。");
                    values[columnIndex++] = decoded;
                }
                catch (System.Text.DecoderFallbackException ex)
                {
                    throw new InvalidDataException($"{definition.DisplayName}（{definition.Key}）ID={definition.BeginId + rowIndex} 字段“{field.Name}”含无效 GBK 字节（文件偏移 0x{rowOffset + field.Offset:X}）；原始文件未修改。", ex);
                }
            }
            table.Rows.Add(values);
        }

        var document = new TableDocument
        {
            Definition = definition,
            FilePath = filePath,
            Data = table,
            OriginalFileBytes = bytes,
            OriginalFileHash = HashService.Sha256(bytes)
        };
        document.CaptureOriginalValues();
        return document;
    }
}
