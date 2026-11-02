using System.Text;

namespace DataManager.Core.Binary;

public static class EncodingService
{
    static EncodingService()
    {
        Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
    }

    public static Encoding GameEncoding
    {
        get => Encoding.GetEncoding(936, EncoderFallback.ExceptionFallback, DecoderFallback.ExceptionFallback);
    }

    public static string DecodeFixedString(ReadOnlySpan<byte> bytes)
    {
        var end = bytes.IndexOf((byte)0);
        if (end >= 0) bytes = bytes[..end];
        // Spaces and formatting/control bytes are payload, not disposable padding.
        return GameEncoding.GetString(bytes);
    }

    /// <summary>
    /// Keeps malformed legacy bytes distinguishable from real question marks.
    /// Their supplementary private-use placeholders cannot be encoded by GBK; an
    /// unchanged value retains its original slot, while an edit must repair it.
    /// </summary>
    public static string DecodeFixedStringPreservingInvalidBytes(ReadOnlySpan<byte> bytes)
    {
        var end = bytes.IndexOf((byte)0);
        if (end >= 0) bytes = bytes[..end];
        try { return GameEncoding.GetString(bytes); }
        catch (DecoderFallbackException)
        {
            var lossless = Encoding.GetEncoding(936, EncoderFallback.ExceptionFallback, new PreservedByteFallback());
            return lossless.GetString(bytes);
        }
    }

    public static bool HasPreservedInvalidBytes(string value)
    {
        for (var i = 0; i + 1 < value.Length; i++)
            if (value[i] == '\uDB80' && value[i + 1] is >= '\uDC00' and <= '\uDCFF') return true;
        return false;
    }

    public static byte[] EncodeFixedString(string? value, int size)
    {
        return EncodeFixedString(value, new TextFieldConstraint(size, size, false, "物理槽位容量。"));
    }

    public static byte[] EncodeFixedString(string? value, TextFieldConstraint constraint)
    {
        var bytes = constraint.Encode(value);
        var output = new byte[constraint.StorageBytes];
        Buffer.BlockCopy(bytes, 0, output, 0, bytes.Length);
        return output;
    }

    public static byte[] EncodeFixedStringPreservingTail(string? value, ReadOnlySpan<byte> original, TextFieldConstraint constraint)
    {
        if (original.Length != constraint.StorageBytes) throw new InvalidDataException("文本原始槽位长度与约束不一致。");
        value ??= string.Empty;
        // No-op edits must retain the exact original slot, including unusual
        // legacy values which exceed today's verified runtime budget.
        if (DecodeFixedStringPreservingInvalidBytes(original).Equals(value, StringComparison.Ordinal)) return original.ToArray();
        var bytes = constraint.ForOriginalSlot(original).Encode(value);
        var oldEnd = original.IndexOf((byte)0);
        if (oldEnd < 0) oldEnd = original.Length;
        var writeEnd = bytes.Length + (bytes.Length < original.Length ? 1 : 0);
        // Nonzero bytes beyond the old terminator can carry private parameters.
        // Growth may consume zero padding but must never overwrite that tail.
        for (var i = oldEnd + 1; i < writeEnd; i++)
            if (original[i] != 0)
                throw new ArgumentException($"名称增长会覆盖槽内第 {i + 1} 字节的非零保留数据；请缩短文本。", nameof(value));
        var output = original.ToArray();
        // Erase only the old visible text, preserving every byte beyond its NUL.
        output.AsSpan(0, oldEnd).Clear();
        bytes.CopyTo(output, 0);
        if (bytes.Length < output.Length) output[bytes.Length] = 0;
        return output;
    }

    private sealed class PreservedByteFallback : DecoderFallback
    {
        public override int MaxCharCount => 8;
        public override DecoderFallbackBuffer CreateFallbackBuffer() => new PreservedByteFallbackBuffer();
    }

    private sealed class PreservedByteFallbackBuffer : DecoderFallbackBuffer
    {
        private byte[] _bytes = [];
        private int _position;
        public override bool Fallback(byte[] bytesUnknown, int index)
        {
            if (Remaining != 0) throw new InvalidOperationException("解码保留字节缓冲区尚未读完。");
            _bytes = bytesUnknown; _position = 0;
            return _bytes.Length != 0;
        }
        public override char GetNextChar()
        {
            if (_position >= _bytes.Length * 2) return '\0';
            var position = _position++;
            return position % 2 == 0 ? '\uDB80' : (char)(0xDC00 + _bytes[position / 2]);
        }
        public override bool MovePrevious()
        {
            if (_position == 0) return false;
            _position--; return true;
        }
        public override int Remaining => _bytes.Length * 2 - _position;
        public override void Reset() { _bytes = []; _position = 0; base.Reset(); }
    }
}
