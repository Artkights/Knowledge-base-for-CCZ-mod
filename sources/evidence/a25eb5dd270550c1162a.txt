using System.Globalization;
using System.Reflection;
using DataManager.Core.Workbooks;

namespace DataManager.Tests;

internal static class WorkbookTextEncodingTests
{
    public static void Run()
    {
        var type = typeof(PageWorkbookService).Assembly.GetType("DataManager.Core.Workbooks.WorkbookPackage", throwOnError: true)!;
        var encode = type.GetMethod("EncodeSpreadsheetText", BindingFlags.Static | BindingFlags.NonPublic)!.CreateDelegate<Func<string, string>>();
        var decode = type.GetMethod("DecodeSpreadsheetText", BindingFlags.Static | BindingFlags.NonPublic)!.CreateDelegate<Func<string, string>>();
        foreach (var text in new[] { "", "普通中文与 English 123", "甲\r\n乙\n丙\r尾  \u0001\u001A", "_x000D_", "_XFFFF_", "_x005F_x000D_", "_x0041__X0042_", "_x0041_x0042_", "_xGGGG_ _x123_ _x12345_ _x1234 _y1234_", "😀 𝄞" })
            TestSupport.Assert(decode(encode(text)) == text, "OOXML 文本往返改变原文：" + text);
        TestSupport.Assert(encode("\r\u0001\u001A\uFFFE\uFFFF") == "_x000D__x0001__x001A__xFFFE__xFFFF_", "原生控制码未按 ST_Xstring 编码");
        TestSupport.Assert(decode("_x005F_x000D_") == "_x000D_", "字面转义被递归解码");
        TestSupport.Assert(decode("_x0041__X0042_") == "AB", "相邻大小写转义未被解码");
        TestSupport.Assert(decode("_x0041_x0042_") == "Ax0042_", "重叠转义被重复消费");
        var malformed = "_xGGGG_ _x123_ _x12345_ _x1234 _y1234_";
        TestSupport.Assert(decode(malformed) == malformed, "不完整或非法转义改变原文");
        for (var code = 0; code <= ushort.MaxValue; code++)
        {
            var token = "_x" + code.ToString("X4", CultureInfo.InvariantCulture) + "_";
            TestSupport.Assert(decode(token) == ((char)code).ToString(), "ST_Xstring UTF-16 解码不符：" + token);
            TestSupport.Assert(decode(encode(token)) == token, "字面 UTF-16 转义未被保护：" + token);
        }
        var allCodeUnits = new string(Enumerable.Range(0, 65536).Select(c => (char)c).ToArray());
        TestSupport.Assert(decode(encode(allCodeUnits)) == allCodeUnits, "完整 UTF-16 编码空间往返改变原文");
        Console.WriteLine("WORKBOOK_TEXT_ENCODING_OK controls/literals/adjacent/overlap/malformed/all-65536-code-units");
    }
}
