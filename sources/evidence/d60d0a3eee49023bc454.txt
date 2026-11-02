using System.Buffers.Binary;

namespace ImageManager.Core;

public static class PmapTerrainCodec
{
    public const ushort ClearValue = 0xFFFF;
    public const ushort BlockedValue = 0xF0FF;
    public const int HeaderLength = 16;
    public static PmapTerrainData Decode(byte[] payload)
    {
        if (payload.Length < HeaderLength) throw new InvalidDataException("Pmap 地形头不足 16 字节。");
        var width = BinaryPrimitives.ReadUInt16LittleEndian(payload.AsSpan(2, 2));
        var height = BinaryPrimitives.ReadUInt16LittleEndian(payload.AsSpan(4, 2));
        var layers = BinaryPrimitives.ReadUInt16LittleEndian(payload.AsSpan(6, 2));
        var count = (long)width * height * layers;
        if (width == 0 || height == 0 || layers == 0 || count > int.MaxValue || HeaderLength + count * 2 != payload.Length)
            throw new InvalidDataException("Pmap 地形尺寸、层数与 16 位单元载荷长度不一致。");
        var cells = new ushort[(int)count];
        for (var i = 0; i < cells.Length; i++) cells[i] = BinaryPrimitives.ReadUInt16LittleEndian(payload.AsSpan(HeaderLength + i * 2, 2));
        return new PmapTerrainData(payload.AsSpan(0, HeaderLength).ToArray(), width, height, layers, cells);
    }

    public static bool IsVerifiedPayload(byte[] payload)
    {
        try { return Decode(payload).CanEdit; }
        catch (Exception ex) when (ex is InvalidDataException or OverflowException) { return false; }
    }

    public static byte[] Encode(PmapTerrainData data, IReadOnlyList<ushort>? cells = null)
    {
        cells ??= data.Cells;
        if (cells.Count != data.Cells.Count) throw new InvalidDataException("Pmap 地形格数量发生变化。");
        var output = new byte[checked(HeaderLength + cells.Count * 2)];
        data.Header.Span.CopyTo(output);
        for (var i = 0; i < cells.Count; i++) BinaryPrimitives.WriteUInt16LittleEndian(output.AsSpan(HeaderLength + i * 2, 2), cells[i]);
        return output;
    }

    public static byte[] CreateDefault()
    {
        // Matches the 6.5 and 6.6x official assigner's Source/addPmap.e5.
        var output = new byte[20016];
        Convert.FromHexString("1700640064000100C8006400010041FF").CopyTo(output, 0);
        output.AsSpan(HeaderLength).Fill(0xFF);
        return output;
    }
}
