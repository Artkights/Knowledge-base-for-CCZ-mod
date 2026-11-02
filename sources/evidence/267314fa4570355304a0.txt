using ImageManager.Core;

namespace DataManager.Images;

/// <summary>Chinese labels for the integrated editor; stable resource keys remain unchanged.</summary>
internal static class ResourceDisplayNames
{
    public static string Name(ImageResourceDescriptor resource) => resource.Key switch
    {
        "Pmapobj.e5" => "R 形象",
        "SComposite" => "S 形象",
        "Face" => "头像",
        "Tou" => "大头像",
        "Item.e5" or "Itemicon.dll" => "宝物图标",
        "Mtem.e5" or "Mgcicon.dll" => "策略图标",
        "Meff.e5" => "小动画",
        "Hitarea.e5" => "攻击范围",
        "Effarea.e5" => "穿透范围",
        "Logo.e5" => "背景插图",
        "Mmap.e5" => "场景背景",
        "Tr.e5" => "过场图片",
        "Gate.e5" => "场景门图",
        "Pmap.e5" => "内场景地形",
        "MapPairs" => "战场地图",
        "Weather.e5" => "天气图片",
        "DT.e5" => "动态半身像",
        "Fb.e5" => "半身像",
        "U_select.e5" => "选择光标",
        "Cmdicon.dll" => "命令图标",
        "Mark.e5" => "标记图片",
        _ when resource.Key.StartsWith("Mcall:", StringComparison.OrdinalIgnoreCase) =>
            "大动画 " + resource.Key[6..],
        _ when resource.Key.StartsWith("Discovered:", StringComparison.OrdinalIgnoreCase) =>
            "其他图片：" + Path.GetFileNameWithoutExtension(resource.Key[11..]),
        _ => resource.DisplayName
    };

    public static string WithSources(string name, IEnumerable<ImageResourceDescriptor> resources)
    {
        var descriptors = resources.ToArray();
        var files = descriptors.SelectMany(resource => resource.Paths).Select(Path.GetFileName)
            .Where(file => !string.IsNullOrWhiteSpace(file)).Cast<string>()
            .Distinct(StringComparer.OrdinalIgnoreCase).OrderBy(file => file, StringComparer.OrdinalIgnoreCase).ToList();
        if (descriptors.Any(resource => resource.Kind == ResourceKind.MapPair))
        {
            files.RemoveAll(file => Path.GetExtension(file).Equals(".jpg", StringComparison.OrdinalIgnoreCase) ||
                                    Path.GetExtension(file).Equals(".jpeg", StringComparison.OrdinalIgnoreCase));
            files.Add("Map/M*.JPG"); files.Add("Hexzmap.e5");
        }
        if (files.Count > 3 && descriptors.All(resource => resource.Kind == ResourceKind.McallAnimation))
            files = ["Mcall*.e5"];
        return $"{name}（{(files.Count == 0 ? "未找到资源" : string.Join('、', files))}）";
    }

    public static string WithSources(ImageResourceDescriptor resource) => WithSources(Name(resource), [resource]);

    public static string Category(ImageCategory category) => category switch
    {
        ImageCategory.CharacterR => "R 形象",
        ImageCategory.CharacterS => "S 形象",
        ImageCategory.Portrait => "头像",
        ImageCategory.ItemIcon => "宝物图标",
        ImageCategory.StrategyIcon => "策略图标",
        ImageCategory.Scene => "场景与地图",
        ImageCategory.Range => "范围图片",
        ImageCategory.Interface => "界面图片",
        ImageCategory.Dynamic => "动态图片",
        ImageCategory.HalfBody => "半身像",
        ImageCategory.StrategyAnimation => "策略动画",
        ImageCategory.Discovered => "其他图片",
        ImageCategory.Experimental => "待确认图片",
        _ => "其他图片"
    };

    public static string Kind(ResourceKind kind) => kind switch
    {
        ResourceKind.E5Indexed => "索引图片档案",
        ResourceKind.PmapSpecial => "内场景地形数据",
        ResourceKind.WeatherSpecial => "天气专用图片",
        ResourceKind.DtAnimation => "半身像动画",
        ResourceKind.DllBitmap => "位图资源库",
        ResourceKind.RComposite => "R 形象组合",
        ResourceKind.SComposite => "S 形象组合",
        ResourceKind.FaceComposite => "头像组合",
        ResourceKind.MapPair => "地图与地形",
        ResourceKind.McallAnimation => "大动画整包",
        ResourceKind.MarkRaw => "标记专用格式",
        _ => "待确认格式"
    };
}
