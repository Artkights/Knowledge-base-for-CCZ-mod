using System.Buffers.Binary;
using System.Collections;
using System.Reflection;
using DataManager.Core.Models;
using DataManager.Core.Scanner;

namespace DataManager.Tests;

/// <summary>
/// Uses a tiny synthetic PE and the production decoder/analyzers. Reflection only crosses
/// the internal analyzer boundary; production visibility and public contracts stay intact.
/// </summary>
internal static class OperandSharingSafetyTests
{
    private static readonly Assembly Core = typeof(EngineEffectScanService).Assembly;
    private const BindingFlags StaticMethods = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static;

    public static void Run()
    {
        RepeatedRegisterPushBlocksBothRoles();
        WrapperReadOnlyRoleStillConsumesDefinition();
        ItemOnlySharingRemainsWritable();
        OnlyCompleteRegisterZeroingProvesHighBits();
        Console.WriteLine("OPERAND_SHARING_SAFETY_TESTS_OK direct-cross-role wrapper-cross-role item-only-sharing full32-immediate partial-zeroing-safety");
    }

    private static void RepeatedRegisterPushBlocksBothRoles()
    {
        // push value; push stacking; mov eax,25h; push eax(item); push eax(personal).
        // A complete 32-bit MOV needs no preceding XOR to prove its entire value.
        var pushes = AnalyzePushes([0x55, 0x8B, 0xEC, 0x6A, 0x00, 0x6A, 0x01,
            0xB8, 0x25, 0x00, 0x00, 0x00, 0x50, 0x50, 0xC3]);
        var item = pushes[2];
        var personal = pushes[3];
        Assert(item.WritePlan.IsWritable && item.ResolvedValue == 0x25,
            "Fixture must initially resolve the first register push to its immediate: " + item.WritePlan.BlockReason);
        Assert(!personal.WritePlan.IsWritable && personal.Value == null && personal.ResolvedValue == null,
            "The second register push must remain unresolved after the intervening read.");
        Assert(personal.DefinitionChain.Any(definition => definition.ImmediateOffset != null &&
            definition.FileOffset + definition.ImmediateOffset == item.WritePlan.ImmediateFileOffset),
            "A blocked register use must preserve the physical immediate source for hazard checks.");

        Invoke("EngineEffectArgumentAnalyzer", "MarkSharedDefinitions",
            (object)new[] { Call(pushes) });
        AssertBlockedShared(item, "The item selector shares its MOV with a personal argument.");
        AssertBlockedShared(personal, "The unresolved personal argument still consumes the same MOV.");
        Assert(personal.Value == null && personal.ResolvedValue == null,
            "Shared-source detection must not promote an unresolved argument to a static value.");
        Console.WriteLine("PASS direct repeated-register cross-role source preserved; both plans blocked; personal stays unresolved");
    }

    private static void WrapperReadOnlyRoleStillConsumesDefinition()
    {
        var source = WritableItem();
        var readOnly = (EngineEffectPushArgument)Invoke("EngineEffectWrapperAnalyzer", "ReadOnly", source,
            "Synthetic shared wrapper constant in personal role.");
        Assert(!readOnly.WritePlan.IsWritable && readOnly.ResolvedValue == 0x25,
            "Wrapper clone must retain the known constant while disallowing standalone writes.");
        ApplyWrapperSharing([
            [new(), new(), source, new()],
            [new(), new(), new(), readOnly]
        ]);
        AssertBlockedShared(source, "A writable wrapper item source also consumed by a read-only personal role must be blocked.");
        AssertBlockedShared(readOnly, "A read-only wrapper consumer must participate in source sharing.");
        Console.WriteLine("PASS wrapper read-only cross-role consumer blocks the shared item immediate");
    }

    private static void ItemOnlySharingRemainsWritable()
    {
        var single = WritableItem();
        Invoke("EngineEffectArgumentAnalyzer", "MarkSharedDefinitions",
            (object)new[] { Call([new(), new(), single, new()]) });
        Assert(single.WritePlan.IsWritable && !single.WritePlan.IsSharedDefinition,
            "An isolated item immediate must remain independently writable.");
        Assert(single.ResolvedValue == 0x25 && single.WritePlan.ImmediateLength == 4,
            "A standalone MOV EAX,imm32 without XOR must resolve its full value and writable four-byte source.");

        var first = WritableItem();
        var second = WritableItem();
        Invoke("EngineEffectArgumentAnalyzer", "MarkSharedDefinitions", (object)new[] {
            Call([new(), new(), first, new()]), Call([new(), new(), second, new()]) });
        AssertWritableShared(first, "Direct item-only shared source must stay writable as a group.");
        AssertWritableShared(second, "Every item-only alias must have the shared marker.");

        var wrapperFirst = WritableItem();
        var wrapperSecond = WritableItem();
        ApplyWrapperSharing([
            [new(), new(), wrapperFirst, new()],
            [new(), new(), wrapperSecond, new()]
        ]);
        AssertWritableShared(wrapperFirst, "Wrapper item-only shared constant must stay writable as a group.");
        AssertWritableShared(wrapperSecond, "Wrapper shared aliases must retain their writable plans.");
        Console.WriteLine("PASS isolated item writable; direct and wrapper item-only aliases writable with shared marker");
    }

    private static void OnlyCompleteRegisterZeroingProvesHighBits()
    {
        foreach (var (label, zeroing) in new (string, byte[])[] {
            ("xor eax,eax", [0x31, 0xC0]), ("sub eax,eax", [0x29, 0xC0]) })
        {
            var argument = PartialAfter(zeroing);
            Assert(argument.ResolvedValue == 0x25 && argument.WritePlan.IsWritable &&
                argument.WritePlan.ImmediateLength == 1,
                label + " must prove the high bits before MOV AL,25h; PUSH EAX.");
        }
        foreach (var (label, zeroing) in new (string, byte[])[] {
            ("xor ax,ax", [0x66, 0x31, 0xC0]), ("xor al,al", [0x30, 0xC0]),
            ("sub ax,ax", [0x66, 0x29, 0xC0]), ("sub al,al", [0x28, 0xC0]),
            ("xor al,ah", [0x30, 0xE0]), ("no zeroing", []) })
        {
            var argument = PartialAfter(zeroing);
            Assert(!argument.WritePlan.IsWritable && argument.Value == null && argument.ResolvedValue == null,
                label + " must not prove the full EAX value after MOV AL,25h; PUSH EAX.");
        }
        Console.WriteLine("PASS complete MOV EAX immediate writable without XOR; only full32 XOR/SUB prove high bits; partial/no zeroing stays unresolved read-only");

        static EngineEffectPushArgument PartialAfter(byte[] zeroing)
            => AnalyzePushes([0x55, 0x8B, 0xEC, .. zeroing, 0xB0, 0x25, 0x50, 0xC3]).Single();
    }

    private static EngineEffectPushArgument WritableItem()
        => AnalyzePushes([0x55, 0x8B, 0xEC, 0xB8, 0x25, 0x00, 0x00, 0x00, 0x50, 0xC3]).Single();

    private static EngineEffectCallSite Call(EngineEffectPushArgument[] pushes)
        => new() { Pushes = pushes };

    private static void ApplyWrapperSharing(EngineEffectPushArgument[][] arguments)
    {
        var workType = Type("EngineEffectWrapperAnalyzer").GetNestedType("DerivedWork", BindingFlags.NonPublic)!;
        var work = Array.CreateInstance(workType, arguments.Length);
        for (var index = 0; index < arguments.Length; index++)
        {
            var item = Activator.CreateInstance(workType, nonPublic: true)!;
            workType.GetProperty("Arguments")!.SetValue(item, arguments[index]);
            work.SetValue(item, index);
        }
        Invoke("EngineEffectWrapperAnalyzer", "ApplySharedDefinitions", work);
    }

    private static EngineEffectPushArgument[] AnalyzePushes(byte[] code)
    {
        var image = Invoke("EngineEffectBinaryImage", "Read", MinimalPe(code), CancellationToken.None);
        var decoded = (IEnumerable)Invoke("EngineEffectDecoder", "DecodeForward", image, 0x401010u, code.Length, false);
        return decoded.Cast<object>()
            .Where(instruction => (bool)instruction.GetType().GetProperty("IsPush")!.GetValue(instruction)! &&
                (uint)instruction.GetType().GetProperty("Address")!.GetValue(instruction)! != 0x401010u)
            .Select(instruction => (EngineEffectPushArgument)Invoke("EngineEffectArgumentAnalyzer", "Analyze", image, instruction))
            .ToArray();
    }

    private static byte[] MinimalPe(byte[] code)
    {
        var bytes = new byte[0x400];
        bytes[0] = (byte)'M'; bytes[1] = (byte)'Z';
        Write32(0x3C, 0x80); Write32(0x80, 0x4550);
        Write16(0x84, 0x14C); Write16(0x86, 1); Write16(0x94, 0xE0);
        Write16(0x98, 0x10B); Write32(0xA8, 0x1010); Write32(0xB4, 0x400000);
        const int section = 0x178;
        ".text"u8.CopyTo(bytes.AsSpan(section));
        Write32(section + 8, 0x200); Write32(section + 12, 0x1000);
        Write32(section + 16, 0x200); Write32(section + 20, 0x200);
        Write32(section + 36, 0x60000020);
        bytes.AsSpan(0x200).Fill(0xCC);
        code.CopyTo(bytes, 0x210);
        return bytes;

        void Write16(int offset, ushort value) => BinaryPrimitives.WriteUInt16LittleEndian(bytes.AsSpan(offset, 2), value);
        void Write32(int offset, uint value) => BinaryPrimitives.WriteUInt32LittleEndian(bytes.AsSpan(offset, 4), value);
    }

    private static Type Type(string name) => Core.GetType("DataManager.Core.Scanner." + name, throwOnError: true)!;
    private static object Invoke(string type, string method, params object[] arguments)
        => Type(type).GetMethod(method, StaticMethods)!.Invoke(null, arguments)!;

    private static void AssertBlockedShared(EngineEffectPushArgument argument, string message)
        => Assert(!argument.WritePlan.IsWritable && argument.WritePlan.IsSharedDefinition &&
            argument.WritePlan.BlockReason?.Contains("跨不同参数") == true, message);

    private static void AssertWritableShared(EngineEffectPushArgument argument, string message)
        => Assert(argument.WritePlan.IsWritable && argument.WritePlan.IsSharedDefinition &&
            argument.WritePlan.ImmediateLength == 4 && argument.WritePlan.BeforeBytes.SequenceEqual(new byte[] { 0x25, 0, 0, 0 }), message);

    private static void Assert(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }
}
