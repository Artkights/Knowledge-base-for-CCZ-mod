using System.Buffers.Binary;
using DataManager.Core.Models;

namespace DataManager.Core.Scanner;

public sealed partial class EngineEffectAssignmentService
{
    /// <summary>Inspects a PE file buffer; never runs or writes the engine.</summary>
    public static EffectAssignmentLayout ProbeJobLayout(byte[] bytes)
        => ProbeJobLayout(EngineEffectBinaryImage.Read(bytes));

    internal static EffectAssignmentLayout ProbeJobLayout(EngineEffectBinaryImage image)
    {
        static EffectAssignmentLayout Reject(string reason) => new()
        {
            Evidence = "真实兵种分配存储未定位：" + reason + "；未把个人/兵种特效号当作兵种ID。"
        };
        byte[] Read(uint address, int length)
        {
            // Virtual tails have no editable disk bytes, even when later file data exists.
            var section = image.SectionOf(address);
            if (section == null || length < 0 || (ulong)(address - section.VirtualAddress) + (uint)length > section.RawSize)
                return [];
            return image.VirtualAddressToFileOffset(address) is { } offset ? image.ReadBytes(offset, length) ?? [] : [];
        }
        bool Is(uint address, params byte[] expected) => Read(address, expected.Length).AsSpan().SequenceEqual(expected);
        bool Pattern(uint address, string pattern)
        {
            var tokens = pattern.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            var raw = Read(address, tokens.Length);
            return raw.Length == tokens.Length && tokens.Select((token, index) =>
                token == "??" || raw[index] == Convert.ToByte(token, 16)).All(match => match);
        }
        uint? Dword(uint address)
        {
            var raw = Read(address, 4);
            return raw.Length == 4 ? BinaryPrimitives.ReadUInt32LittleEndian(raw) : null;
        }
        bool Call(uint address, uint target)
        {
            var raw = Read(address, 5);
            return raw.Length == 5 && raw[0] == 0xE8 &&
                unchecked((uint)(address + 5 + BinaryPrimitives.ReadInt32LittleEndian(raw.AsSpan(1)))) == target;
        }
        bool FamilyRet4(uint address) => Pattern(address,
            "55 8B EC 0F B6 45 08 3C 3C 73 09 6A 03 E8 ?? ?? ?? ?? " +
            "EB 0A 3C 50 73 04 2C 28 EB 02 B0 28 5D C2 04 00") &&
            Call(address + 13, 0x40BAD4) && Is(0x40BAD4, 0x33, 0xD2, 0xF7, 0x7C, 0x24, 0x04, 0xC2, 0x04, 0);

        if (!Is(0x41301E, 0x55, 0x8B, 0xEC, 0x51)) return Reject("41301E取值provider入口不符");
        var eight = Is(0x4198BE, 0x55, 0x8B, 0xEC, 0xC1, 0x65, 0x08, 0x03);
        var sixteen = Is(0x4198BE, 0x55, 0x8B, 0xEC, 0x8B, 0x4D, 0x08, 0xC1, 0xE1, 0x04, 0x03, 0xD1);
        if (!eight && !sixteen) return Reject("4198BE不是已定位的8/16字节行读取器");

        var providerLoad = eight ? 0x413031u : 0x413038u;
        var providerCall = eight ? 0x413037u : 0x41303Eu;
        var providerTail = eight ? 0x413070u : 0x413077u;
        if (!Is(providerLoad, 0x8B, 0x15) || !Call(providerCall, 0x4198BE) ||
            !Is(providerTail, 0x8B, 0xE5, 0x5D, 0xC2, 0x10, 0))
            return Reject("provider的表指针读取、查询调用或四参数清栈不符");
        var pointerAddress = Dword(providerLoad + 2);
        if (pointerAddress == null) return Reject("表指针操作数未映射");

        int rowCount;
        uint matcher;
        string matcherAbi;
        if (eight)
        {
            if (!Pattern(0x4198BE,
                "55 8B EC C1 65 08 03 03 55 08 52 6A 00 EB 03 FF 45 F8 " +
                "8B 55 F8 83 FA 03 73 13 D1 E2 03 55 FC 66 3B 02 75 EB " +
                "8B 55 FC 0F B6 52 07 EB 02 33 D2 52 E8 ?? ?? ?? ?? 50 " +
                "8B 4D FC 83 C1 06 0F B6 01 50 E8 ?? ?? ?? ?? 5A 84 C0 " +
                "74 04 33 C0 EB 09 8B 4D FC 83 C1 07 0F B6 01 8B 4D 0C " +
                "83 F9 02 75 06 85 D2 75 02 8B D0 E8 ?? ?? ?? ?? 8B E5 5D C2 08 00") ||
                !Call(0x4198EE, 0x406610) || !Call(0x4198FE, 0x422DA8) || !Call(0x419923, 0x40BF2F))
                return Reject("8字节行的三个人物槽、单兵种槽、共享N或读取器ABI不符");
            if (!Pattern(0x408839,
                "0F B6 45 F8 3C ?? 77 24 6B C8 08 03 0D ?? ?? ?? ?? " +
                "8A 45 F9 3C 03 77 14 6B D0 02 03 CA 66 8B 55 FA " +
                "3C 03 74 05 66 89 11 EB 02 88 11 8B E5 5D C2 04 00") ||
                Dword(0x408846) != pointerAddress)
                return Reject("8字节行的指针写入器、单槽字节宽度或写入器ABI不符");
            if (!Pattern(0x40116D,
                "50 83 EC 08 68 ?? ?? ?? ?? 68 ?? ?? ?? ?? 6A 03 6A 00 " +
                "FF 75 E8 8D 4D E0 51 E8 ?? ?? ?? ?? 68 ?? ?? ?? ?? 68 " +
                "?? ?? ?? ?? 6A 01 6A 01 FF 75 E8 8D 4D E0 51 E8 ?? ?? ?? ??") ||
                !Call(0x401186, 0x40F436) || !Call(0x4011A0, 0x40F436) ||
                Dword(0x401177) != pointerAddress || Dword(0x401191) != pointerAddress)
                return Reject("8字节初始化器的3+1槽数或表指针与读写器不一致");
            var upper = Read(0x40883E, 1)[0];
            if (upper is not (0xB3 or 0xFE) || Dword(0x401172) != upper || Dword(0x40118C) != upper)
                return Reject("8字节初始化器与写入器的180/255行上界不一致");
            rowCount = upper + 1;
            matcher = 0x422DA8;
            if (!Pattern(matcher, "55 8B EC 8B 45 08 3C 50 73 ?? 80 3D ?? ?? ?? ?? 00 74 07 3A 45 0C 74 ?? EB ??"))
                return Reject("单槽兵种匹配器的80上界及精确模式分支不符");
            if (rowCount == 180)
            {
                if (!Pattern(0x422DC2,
                    "FF 75 0C E8 ?? ?? ?? ?? 83 C4 04 50 FF 75 08 E8 ?? ?? ?? ?? " +
                    "83 C4 04 59 3B C1 75 0C 8B 45 08 3B 45 0C 77 04 33 C0 EB 02 B0 01 5D C2 08 00") ||
                    !Call(0x422DC5, 0x40687C) || !Call(0x422DD1, 0x40687C) ||
                    !Pattern(0x40687C,
                    "55 8B EC 8B 45 08 3C 3B 77 0F 25 FF 00 00 00 99 B9 03 00 00 00 " +
                    "F7 F9 EB 0A 3C 50 7D 04 2C 28 EB 02 B0 28 5D C3") ||
                    !Is(0x422DB0, 0x73, 0x38) || !Is(0x422DBE, 0x74, 0x26, 0xEB, 0x28))
                    return Reject("180行兵种同族计算或cdecl清栈合约不符");
                matcherAbi = "同族函数cdecl，匹配器ret8";
            }
            else
            {
                if (!Pattern(0x422DC2,
                    "FF 75 0C E8 ?? ?? ?? ?? 50 FF 75 08 E8 ?? ?? ?? ?? 59 3B C1 75 0C " +
                    "8B 45 08 3B 45 0C 77 04 33 C0 EB 02 B0 01 5D C2 08 00") ||
                    !Call(0x422DC5, 0x40687C) || !Call(0x422DCE, 0x40687C) || !FamilyRet4(0x40687C) ||
                    !Is(0x422DB0, 0x73, 0x32) || !Is(0x422DBE, 0x74, 0x20, 0xEB, 0x22))
                    return Reject("255行兵种同族计算或ret4/ret8清栈合约不符");
                matcherAbi = "同族函数ret4，匹配器ret8";
            }
        }
        else
        {
            if (!Is(0x41990F, 0x8B, 0x45, 0xF4, 0x3C, 0x02) ||
                !Is(0x419916, 0xD1, 0xE0, 0x83, 0xC0, 0x0C, 0x03, 0x45, 0xFC) ||
                !Call(0x419926, 0x42F998) || !Is(0x419930, 0x0F, 0xB6, 0x41, 0x01) ||
                !Is(0x419948, 0x8B, 0xE5, 0x5D, 0xC2, 0x0C, 0))
                return Reject("16字节行的0C/0E双槽、独立值或读取器ABI不符");
            if (!Pattern(0x408824,
                "0F B6 45 F4 3C FE 77 3C 6B C8 10 03 0D ?? ?? ?? ?? 8A 45 F6 " +
                "3C 03 77 05 6B D0 03 EB 10 3C 05 77 23 83 E8 04 6B D0 02 83 C2 0C " +
                "83 C0 04 03 CA 8A 55 FA 3C 03 76 05 88 55 F9 EB 03 88 51 02 " +
                "8B 55 F8 66 89 11 8B E5 5D C2 04 00") || Dword(0x408831) != pointerAddress)
                return Reject("16字节行的255行上界、4+2写入器或写入器ABI不符");
            if (!Pattern(0x40116D,
                "50 83 EC 08 54 68 ?? ?? ?? ?? 6A 04 6A 00 FF 75 E8 6A FE E8 ?? ?? ?? ?? " +
                "54 68 ?? ?? ?? ?? 6A 02 6A 01 FF 75 E8 6A FE E8 ?? ?? ?? ??") ||
                Dword(0x401173) != pointerAddress || Dword(0x401187) != pointerAddress ||
                !Call(0x401180, 0x40F436) || !Call(0x401194, 0x40F436))
                return Reject("16字节初始化器的4+2槽数、上界或表指针与读写器不一致");
            if (!Pattern(0x42F998,
                "55 8B EC 8B 45 08 3C 50 73 32 80 3D ?? ?? ?? ?? 00 74 07 3A 45 0C 74 20 EB 22 " +
                "FF 75 0C E8 ?? ?? ?? ?? 50 FF 75 08 E8 ?? ?? ?? ?? 59 3B C1 75 0C " +
                "8B 45 08 3B 45 0C 77 04 33 C0 EB 02 B0 01 5D C2 08 00") ||
                !Call(0x42F9B5, 0x40687F) || !Call(0x42F9BE, 0x40687F) || !FamilyRet4(0x40687F))
                return Reject("双槽兵种匹配器的80上界、同族继承或清栈合约不符");
            rowCount = 255;
            matcher = 0x42F998;
            matcherAbi = "同族函数ret4，匹配器ret8";
        }

        var tableAddress = Dword(pointerAddress.Value);
        var rowSize = eight ? 8 : 16;
        if (tableAddress == null || Read(tableAddress.Value, rowCount * rowSize).Length != rowCount * rowSize ||
            image.VirtualAddressToFileOffset(tableAddress.Value) is not { } tableOffset)
            return Reject($"实际表指针目标没有完整的{rowCount}×{rowSize}字节磁盘映射");
        var modeAddress = Dword(matcher + 12);
        var mode = modeAddress is { } address ? Read(address, 1) : [];
        if (mode.Length != 1) return Reject("兵种匹配模式开关未映射");
        return new EffectAssignmentLayout
        {
            Verified = true, TableOffset = tableOffset, TableAddress = tableAddress.Value,
            PointerAddress = pointerAddress.Value, RowCount = rowCount, RowSize = rowSize,
            JobIdOffsets = eight ? [6] : [12, 14], JobValueOffsets = eight ? [7] : [13, 15],
            PersonIdOffsets = eight ? [0, 2, 4] : [0, 3, 6, 9],
            PersonValueOffsets = eight ? [7, 7, 7] : [2, 5, 8, 11],
            SharedValue = eight, ExactMode = mode[0] != 0,
            Evidence = $"已定位provider→[0x{pointerAddress:X8}]=0x{tableAddress:X8}→4198BE；文件+0x{tableOffset:X}；" +
                $"{rowCount}×{rowSize}字节，" + (eight ? "3个人物槽、1个兵种槽，+07为全行共享N；" : "4个人物槽、2个兵种槽，每槽独立N；") +
                $"初始化器/写入器上界一致，{matcherAbi}；兵种0..79，FF为空；模式开关0x{modeAddress:X8}初值{mode[0]}。"
        };
    }
}
