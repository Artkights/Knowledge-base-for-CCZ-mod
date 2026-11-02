using System.Text;
using DataManager.Core.Binary;
using DataManager.Core.Editing;
using DataManager.Core.Scanner;

namespace DataManager.Tests;

internal static class EngineConstantAuditTests
{
    public static void Run(string sourceRoot)
    {
        var sourceHash = HashService.Sha256(Path.Combine(sourceRoot, "Ekd5.exe"));
        var copy = TestSupport.CreateCoreCopy(sourceRoot, restoreKnown65Snapshot: false);
        try
        {
            var workspace = new ProjectWorkspace();
            workspace.Open(copy);
            var service = new EngineConstantService();
            var exe = Path.Combine(copy, "Ekd5.exe");
            // 统一按扫描出的 profile 版本读写，和界面 Commit 使用的版本一致；
            // 改版基底不能只按目录名猜版本，否则读用一套布局、写用另一套布局。
            var version = workspace.ActiveProfile.Profile.Version;
            var values = service.Read(exe, version);
            TestSupport.Assert(values.Count == EngineConstantService.Definitions.Count, "常量页条目数量不符。");
            // 成对字段必须跟着主字段的同一相对位移，不能被独立漂移到别的函数。
            foreach (var value in values.Where(item => item.SignatureMatches &&
                         item.SecondaryFileOffset >= 0 && item.Layout.RelativePointerVa == 0))
                TestSupport.Assert(value.SecondaryFileOffset == value.FileOffset +
                        (long)value.Layout.SecondaryFieldVa - value.Layout.FieldVa,
                    $"{value.Definition.DisplayName} 成对字段没有跟随主字段定位。");

            var writable = 0;
            var readOnly = 0;
            var failed = new List<string>();
            // 三个官方基底要求“适用即可写”；改版基底可能把整段函数 nop 或重写，
            // 这类常量如实只读、不写入，只统计并打印，不当作审计失败。
            var officialBase = Path.GetFileName(sourceRoot) is "洗隋" or "加强版6.5未加密版" or "复刻版6.6山贼";
            foreach (var value in values)
            {
                var applicable = value.Definition.ApplicableBases is not { } bases ||
                                 bases.Contains(version, StringComparer.Ordinal);
                if (!applicable)
                {
                    TestSupport.Assert(!value.SignatureMatches,
                        $"{value.Definition.DisplayName} 在不适用的 {version} 上仍匹配签名。");
                    readOnly++;
                    continue;
                }
                if (!value.SignatureMatches)
                {
                    var applicableLayouts = value.Definition.Layouts
                        .Where(layout => layout.AppliesTo(version)).ToArray();
                    if (applicableLayouts.Length > 0 && applicableLayouts.All(layout => layout.Optional))
                    {
                        readOnly++;
                        continue;
                    }
                    if (officialBase)
                        failed.Add($"{value.Definition.Id}（{value.Definition.DisplayName}）：{value.Diagnostic}");
                    else
                    {
                        readOnly++;
                        Console.WriteLine($"MOD_CONSTANT_UNAVAILABLE {version} " +
                            $"{value.Definition.Id} {value.Definition.DisplayName}（{value.Diagnostic}）");
                    }
                    continue;
                }
                var original = value.NumericValue ?? 0;
                if (value.Definition.Kind == EngineConstantKind.Text)
                {
                    var originalText = value.TextValue;
                    var probeText = originalText == "自检文本" ? "自检文本乙" : "自检文本";
                    var writeText = service.Commit(workspace,
                        [new EngineConstantEdit(value.Definition.Id, null, probeText)]);
                    TestSupport.Assert(writeText.Success,
                        $"{value.Definition.DisplayName} 文本写入失败：{writeText.Message}");
                    var afterText = service.Read(exe, version)
                        .Single(item => item.Definition.Id == value.Definition.Id);
                    TestSupport.Assert(afterText.TextValue == probeText,
                        $"{value.Definition.DisplayName} 文本复读失败：{afterText.TextValue}");
                    var restoreText = service.Commit(workspace,
                        [new EngineConstantEdit(value.Definition.Id, null, originalText)]);
                    TestSupport.Assert(restoreText.Success,
                        $"{value.Definition.DisplayName} 文本回填失败：{restoreText.Message}");
                    writable++;
                    continue;
                }
                var probe = original <= value.Definition.Minimum
                    ? value.Definition.Minimum + 1
                    : original - 1;
                if (probe < value.Definition.Minimum || probe > value.Definition.Maximum)
                    probe = value.Definition.Maximum;
                var write = service.Commit(workspace,
                    [new EngineConstantEdit(value.Definition.Id, probe, null)]);
                TestSupport.Assert(write.Success,
                    $"{value.Definition.DisplayName} 写入失败：{write.Message}");
                var after = service.Read(exe, version)
                    .Single(item => item.Definition.Id == value.Definition.Id);
                TestSupport.Assert(after.NumericValue == probe,
                    $"{value.Definition.DisplayName} 复读不符：{after.NumericValue} != {probe}");
                var bytes = File.ReadAllBytes(exe);
                TestSupport.Assert(ReadNumber(bytes, value.FileOffset, value.Layout.Length, value.Definition.Kind) == probe,
                    $"{value.Definition.DisplayName} 文件字节未写到位。");
                if (value.SecondaryFileOffset >= 0)
                    TestSupport.Assert(ReadNumber(bytes, value.SecondaryFileOffset,
                            value.Layout.SecondaryLength > 0 ? value.Layout.SecondaryLength : value.Layout.Length,
                            value.Definition.Kind) == probe,
                        $"{value.Definition.DisplayName} 成对文件字节未写到位。");
                if (value.ExtraFileOffsets is { Count: > 0 } extraOffsets)
                    foreach (var extraOffset in extraOffsets)
                        TestSupport.Assert(ReadNumber(bytes, extraOffset, value.Layout.Length,
                                value.Definition.Kind) == probe,
                            $"{value.Definition.DisplayName} 附加同步字节未写到位（0x{extraOffset:X}）。");
                var restore = service.Commit(workspace,
                    [new EngineConstantEdit(value.Definition.Id, original, null)]);
                TestSupport.Assert(restore.Success,
                    $"{value.Definition.DisplayName} 回填失败：{restore.Message}");
                writable++;
            }
            TestSupport.Assert(failed.Count == 0,
                $"适用但签名不匹配的常量：{string.Join("；", failed)}");
            // 只对“当前基底原地址就完整命中”的布局要求签名全局唯一；改版里不存在的
            // 版本专属布局允许 0 处，未被采用的布局也不强行要求唯一。
            foreach (var check in service.ProbeRelocations(exe, version)
                         .Where(item => item.Applicable && item.Relocate))
                TestSupport.Assert(check.Optional || !check.ExactMatch || check.SignatureHits == 1,
                    $"{check.DefinitionId}（{check.Label}）签名不唯一：{check.SignatureHits} 处。");
            Console.WriteLine($"ENGINE_CONSTANT_AUDIT_OK {version} total={values.Count} writable={writable} " +
                $"readOnly={readOnly} layouts={service.ProbeRelocations(exe, version).Count(item => item.Applicable)}");
        }
        finally
        {
            Directory.Delete(copy, true);
            TestSupport.Assert(HashService.Sha256(Path.Combine(sourceRoot, "Ekd5.exe")) == sourceHash,
                "常量自检修改了真实基底。");
            Console.WriteLine("SOURCE_BASE_UNCHANGED " + sourceHash);
        }
    }

    private static int ReadNumber(byte[] bytes, long offset, int length, EngineConstantKind kind) =>
        kind == EngineConstantKind.Byte
            ? bytes[checked((int)offset)]
            : BitConverter.ToInt32(bytes, checked((int)offset));
}
