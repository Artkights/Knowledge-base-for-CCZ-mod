using System.Buffers.Binary;

namespace DataManager.Core.Profiles;

/// <summary>Independent, complete consumer chains of the 6.4 Xisui configuration layout.</summary>
public static class Ccz64ConfigurationProbe
{
    public sealed record Result(bool RetreatQuotes, bool PersonDefaults, bool EquipmentPermissions, bool SpecialCriticalMap)
    {
        public string RetreatEvidence => RetreatQuotes
            ? "洗隋完整撤退调用链：人物ID<49，消息索引650+ID，200字节读取/尾NUL；同一IMSG.E5对象加载并用于对话，文件+130000，49×200。"
            : "当前6.4 EXE未通过完整撤退/200字节读取/IMSG对象加载/对话调用链，禁止读取猜测的撤退区。";
        public string PersonEvidence => PersonDefaults
            ? "洗隋完整人物构造及1024行/32字节调用链：源+27级别、+28经验、+29武器、+30防具、+31辅助；级别0由引擎转1。"
            : "当前6.4 EXE的人物完整构造/1024行/32字节步长链不匹配；级别、经验和默认装备保留原字节。";
        public string PermissionEvidence => EquipmentPermissions
            ? "洗隋完整80×35加载、兵种索引、装备类别、类型0..25筛选及许可调用链：记录+9+类型读取UInt8，非零允许。"
            : "当前6.4 EXE未通过80×35加载/26类型边界/原生装备许可完整消费链，许可字节保留。";
        public string CriticalEvidence => SpecialCriticalMap
            ? "洗隋完整暴击消费者：21项上限、UInt32人物ID、VA0x48B230映射文件+0x89C30；命中后读取对应200字节台词。"
            : "当前6.4 EXE未通过21项特殊暴击人物映射及200字节台词消费链，映射不可用。";
    }

    public static Result Inspect(byte[] executable)
    {
        var pe = Pe.TryRead(executable);
        if (pe is null) return new(false, false, false, false);
        var messages = pe.Code(0x40BF56, MessageReader) && pe.Code(0x42BC56, MessageLoader) &&
            pe.Bytes(0x48BB68, "494D53472E453500");
        var persons = pe.Code(0x408C0C, PersonConstructor) && pe.Code(0x41B617, PersonByIndex) &&
            pe.Code(0x41B666, PersonLoader) && pe.Bytes(0x48BB60, "444154412E453500");
        var permission = pe.Code(0x41B73E, JobLoader) && pe.Code(0x41B782, JobAccessor) &&
            pe.Code(0x4202BD, JobConstructor) && pe.Code(0x41C60F, PermissionAccessor) &&
            pe.Code(0x407961, EquipmentCheck) && pe.Code(0x43AD20, TypeAccessor) &&
            pe.Code(0x40B444, EquipmentCategory) && pe.Code(0x41FECC, ItemConstructor) &&
            pe.Code(0x408063, EquipmentChooser) && pe.Bytes(0x48BB60, "444154412E453500");
        return new(messages && pe.Code(0x40C011, RetreatReader) && pe.Code(0x44197B, RetreatCaller) && pe.Code(0x44179C, RetreatDispatch),
            persons, permission, messages && pe.Code(0x40C02F, SpecialCritical) && pe.HasRawRange(0x48B230, 21 * 4, 0x89C30));
    }

    private const string RetreatDispatch = "8B4DF88A411F909084C0741A8B4DF8E8A4E7FFFF85C0740E8B55F88B0250E8BC01000083C404";
    private const string RetreatReader = "558BEC8B450C83F8317311058A02000050FF7508E82CFFFFFF83C4085DC3";
    private const string MessageReader = "558BEC68C8000000FF75088B4D0C69C9C800000051B9BCE44A00E80FD200008B5508C682C8000000005DC3";
    private const string RetreatCaller = "558BEC81ECCC000000837D083173288B4508508D8D34FFFFFF51E877A6FCFF83C4088B5508528D8534FFFFFF50B9F05D4B00E8AB7C01008BE55DC3";
    private const string MessageLoader = "558BECB8F8BA4800B940C64A00E850A9FEFFB828BB4800B938C54A00E841A9FEFF6A006868BB4800B9BCE44A00E8D4D2FEFF68A0BB4800E8482C01005DC3";
    private const string PersonConstructor = "558BECFF750C51518345F8086A006A486A00FF75F4E80A7F070083C40C8B450880CC108B4DF48901EB03FE45F0807DF00C73128B55F88B45FC8A08880AFF45F8FF45FCEBE58B4DF4E8D31A000083450C0D8B450C0FB7108B4DF489510452FF751051E823A6000083450C038B450C8B108B4DF488512688712A83450C02C645F000EB03FE45F08B45F03C0573128B550C0FB61410668954411188540821EBE483450C058B450C0FB7108B4DF489511B8A500288511F8B500389512B8B50078851318871346681791BF401760666C7411BF40180791FFA7604C6411FFA80792C007503FE412C83C0098BE55DC20C00";
    private const string PersonByIndex = "558BECFF750CE8C2ABFEFF8B450CC1E005034508FF751050FF750CE8D5D5FEFF5DC3";
    private const string PersonLoader = "558BECA1606F490050506A006860BB4800E8A2FEFFFF85C074276A00EB03FF45F88B45F83D0004000073166A00FF75FC5050E847ABFEFFE86AD5FEFF8945FCEBDD8BE55DC3";
    private const string JobLoader = "558BECFF35606F49006A036860BB4800E8CBFDFFFF85C07427FF35606F49006A00EB03FF45F88B4DF883F9507312E811000000FF75FCE8444B00008945FCEBE38BE55DC3";
    private const string JobAccessor = "558BEC6BC92381C1272A4A005DC3";
    private const string JobConstructor = "558BEC6A23FF750851E81517060083C40C8B450883C0235DC20400";
    private const string PermissionAccessor = "558BEC034D080FB641095DC20400";
    private const string EquipmentCheck = "558BEC5183EC0C33C00FB64D0880F9FF750340EB5EE847BE0700894DF4E8C13A00003C03750433C0EB493C02752B8B4DF4E8603B01008945F88B4DF4E87E3303008945F08B4DFCE85F4500008B55F08B4DF8E8CB940100EB1A8B4DF4E85E330300508B45FC0FB6482BE8B33D0100E83B4C01008BE55DC20400";
    private const string TypeAccessor = "558BEC0FB641115DC3";
    private const string EquipmentCategory = "558BEC0FB641113C14730433C0EB0B3C1A7304B001EB038A41145DC3";
    private const string ItemConstructor = "558BEC516A1051FF7508E822FE050083C40C8B4DFCC6410E008B450883C0118A10885111408A1088511440668B106689511283C0028B1089511583C0048BE55DC20400";
    private const string EquipmentChooser = "8B45F43C14731B508B4DF00FB6492BE80B370100E89345010084C07505FF45F4EBDE8B45F43C147239EB33807D0801755F8345F4148B45F43C1A731B508B4DF00FB6492BE8D6360100E85E45010084C07505FF45F4EBDE8B45F43C1A7204B1FFEB0B";
    private const string SpecialCritical = "558BEC33C0505066485081ECCC000000EB03FF45F88B45F83C1573118B550C3B148530B2480075EA8945F4EBE5817DF4FFFF0000751FFF750CE877A1FFFF0FB641266BC00383C0158945F46A03E8923A07000145F48B55F481C2BC020000528D8528FFFFFF50E8BCFEFFFF83C408";

    private sealed record Section(uint Rva, uint Length, uint Raw, uint Flags);
    private sealed class Pe(byte[] bytes, uint imageBase, Section[] sections)
    {
        public bool HasRawRange(uint address, int length, int expectedOffset) => Offset(address, length, false) == expectedOffset;
        public bool Bytes(uint address, string hex)
        {
            var pattern = Convert.FromHexString(hex); var offset = Offset(address, pattern.Length, false);
            return offset >= 0 && bytes.AsSpan(offset, pattern.Length).SequenceEqual(pattern);
        }
        public bool Code(uint address, string hex)
        {
            var pattern = Convert.FromHexString(hex); var offset = Offset(address, pattern.Length, true);
            if (offset < 0 || !bytes.AsSpan(offset, pattern.Length).SequenceEqual(pattern)) return false;
            // A duplicate whole consumer is ambiguous: do not choose a convenient occurrence.
            var matches = 0;
            foreach (var section in sections.Where(s => (s.Flags & 0x20000000) != 0))
            {
                var span = bytes.AsSpan((int)section.Raw, (int)section.Length);
                var next = 0;
                while (next <= span.Length - pattern.Length)
                {
                    var index = span[next..].IndexOf(pattern); if (index < 0) break;
                    if (++matches > 1) return false; next += index + 1;
                }
            }
            return matches == 1;
        }
        private int Offset(uint address, int length, bool executable)
        {
            if (length < 0 || address < imageBase) return -1;
            var rva = (long)address - imageBase;
            var candidates = sections.Where(s => rva >= s.Rva && rva + length <= (long)s.Rva + s.Length &&
                (!executable || (s.Flags & 0x20000000) != 0)).ToArray();
            return candidates.Length == 1 ? checked((int)(candidates[0].Raw + rva - candidates[0].Rva)) : -1;
        }
        public static Pe? TryRead(byte[] bytes)
        {
            if (bytes.Length < 0x40 || U16(bytes, 0) != 0x5A4D) return null;
            var header = U32(bytes, 0x3C);
            if (header > bytes.Length - 24 || U32(bytes, (int)header) != 0x4550 || U16(bytes, (int)header + 4) != 0x14C) return null;
            var count = U16(bytes, (int)header + 6); var optionalSize = U16(bytes, (int)header + 20);
            var optional = (long)header + 24; var table = optional + optionalSize;
            if (optionalSize < 32 || optional + optionalSize > bytes.Length || U16(bytes, (int)optional) != 0x10B ||
                count is 0 or > 96 || table + count * 40L > bytes.Length) return null;
            var sections = new List<Section>();
            for (var i = 0; i < count; i++)
            {
                var section = (int)table + i * 40; var length = U32(bytes, section + 16); var raw = U32(bytes, section + 20);
                if ((long)raw + length > bytes.Length || raw > int.MaxValue || length > int.MaxValue) return null;
                if (length > 0) sections.Add(new(U32(bytes, section + 12), length, raw, U32(bytes, section + 36)));
            }
            return new(bytes, U32(bytes, (int)optional + 28), sections.ToArray());
        }
        private static ushort U16(byte[] bytes, int at) => BinaryPrimitives.ReadUInt16LittleEndian(bytes.AsSpan(at, 2));
        private static uint U32(byte[] bytes, int at) => BinaryPrimitives.ReadUInt32LittleEndian(bytes.AsSpan(at, 4));
    }
}
