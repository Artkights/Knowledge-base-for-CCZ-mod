using System.Buffers.Binary;
using System.Drawing;
using System.Drawing.Imaging;
using ImageManager.Core;

namespace ImageManager.Tests;

internal static class FlexibleAtlasTests
{
    public static void Run()
    {
        var workspace=FindWorkspace();
        var evidence=Path.Combine(workspace,"data管理器","验证","参考图灵活回导-20261026");
        Directory.CreateDirectory(evidence);
        var temporary=Path.Combine(Path.GetTempPath(),"FlexibleAtlas_"+Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(temporary);
        var frames=new List<DecodedFrame>();
        try
        {
            var resources=new Dictionary<string,string>(StringComparer.OrdinalIgnoreCase);
            foreach(var spec in new[]{(Action:"mov",Size:48,Count:11),(Action:"atk",Size:64,Count:12),(Action:"spc",Size:48,Count:5)})
            {
                var key="Unit_"+spec.Action+".e5";var path=Path.Combine(temporary,key);resources[key]=path;
                using var strip=new Bitmap(spec.Size,spec.Size*spec.Count,PixelFormat.Format32bppArgb);
                using(var g=Graphics.FromImage(strip))
                {
                    g.Clear(Color.Transparent);
                    for(var i=0;i<spec.Count;i++)
                    {
                        using var b=new SolidBrush(Color.FromArgb(60+i*9,140,50));
                        g.FillRectangle(b,12,i*spec.Size+9,22,30);
                    }
                }
                using var ms=new MemoryStream();strip.Save(ms,ImageFormat.Png);
                File.WriteAllBytes(path,Archive([ms.ToArray(),ms.ToArray(),ms.ToArray()]));
                for(var i=0;i<spec.Count;i++)
                {
                    var frame=strip.Clone(new Rectangle(0,i*spec.Size,spec.Size,spec.Size),PixelFormat.Format32bppArgb);
                    frames.Add(new(new(key,path,2,i,1,spec.Action,"front",spec.Size,spec.Size),frame));
                }
            }
            var project=new ProjectProfile(temporary,"flexible atlas",ProjectVersion.Ccz65,false,resources,[]);
            var asset=new LogicalImageAsset("SComposite",2,"S_002",ImageCategory.CharacterS,ResourceKind.SComposite,
                frames.Select(f=>f.Descriptor).ToArray(),[],true,false,string.Empty)
                {SMapping=new SLogicalAssetMapping(2,false,[new(1,2)],3),SMode=SImageMode.Job,IsFixedSlot=true};
            var context=ReferenceAtlasContext.Create(asset,frames);
            var service=new ReferenceAtlasService();
            var canonical=service.Export(Path.Combine(temporary,"export"),context,Color.Magenta,new(){Scale=2});
            using(var round=service.Normalize(canonical.PngPath,context,new()))
            {
                Require(!round.HasBlockingIssues,"规范图往返出现阻断");
                foreach(var f in round.Frames)Require(ReferenceAtlasService.PixelHash(f.Bitmap)==ReferenceAtlasService.PixelHash(frames.Single(x=>x.Descriptor==f.Descriptor).Bitmap),"规范图像素往返不一致");
                TestManualRepair(service,context,canonical.PngPath,round.SourceMapping!);
            }
            using(var original=new Bitmap(canonical.PngPath))
            using(var padded=new Bitmap(original.Width+220,original.Height+97))
            {
                using(var g=Graphics.FromImage(padded)){g.Clear(Color.Magenta);g.DrawImageUnscaled(original,111,53);}
                var paddedPath=Path.Combine(temporary,"non-square.png");padded.Save(paddedPath,ImageFormat.Png);
                var mapped=AtlasManifest.Load(canonical.ManifestPath).CreateSourceMapping(context,padded.Size,new Rectangle(111,53,original.Width,original.Height));
                using var result=service.Normalize(paddedPath,context,new(){SourceMapping=mapped});
                Require(!result.HasBlockingIssues,"长方形非对称留白未通过");
                foreach(var f in result.Frames)Require(ReferenceAtlasService.PixelHash(f.Bitmap)==ReferenceAtlasService.PixelHash(frames.Single(x=>x.Descriptor==f.Descriptor).Bitmap),"长方形裁剪破坏比例或像素");
            }
            TestCanvasVariants(service,context,canonical.PngPath,temporary);
            foreach(var name in new[]{"暗紫背景-2048.png","白底边框-663.png"})
            {
                var path=Path.Combine(workspace,"形象管理器","src","ImageManager.Tests","Fixtures","Atlas",name);
                using var result=service.Normalize(path,context,new());
                File.WriteAllLines(Path.Combine(evidence,name+".diagnostics.txt"),result.Diagnostics.Concat(result.FrameDiagnostics.Select(d=>$"{d.FrameKey}: {d.SourceBounds} {d.Severity} {d.Message}")));
                result.NormalizedAtlas.Save(Path.Combine(evidence,name+".归一化.png"),ImageFormat.Png);
                result.MaskPreview.Save(Path.Combine(evidence,name+".蒙版.png"),ImageFormat.Png);
                Require(result.Frames.Count==28,"真实图未产生28帧");
                Require(!result.HasBlockingIssues,"真实图映射阻断："+name+" / "+string.Join(";",result.FrameDiagnostics.Where(d=>d.Severity==AtlasIssueSeverity.Error).Select(d=>$"{d.Descriptor.Action}{d.Descriptor.FrameIndex}:{d.Message}")));
                if(name.StartsWith("白底"))Require(result.SourceMapping!.EffectiveBounds.Width<663,"外框未自动剔除");
                TestTransaction(project,asset,result.Frames);
                Console.WriteLine($"REAL_ATLAS_OK {name} roi={result.SourceMapping!.EffectiveBounds} warnings={result.FrameDiagnostics.Count(d=>d.Severity==AtlasIssueSeverity.Warning)}");
            }
            TestProtectedColor(service,context,canonical.PngPath,temporary);
            Console.WriteLine("FLEXIBLE_ATLAS_TESTS_OK");
        }
        finally{foreach(var f in frames)f.Dispose();Directory.Delete(temporary,true);}
    }

    private static void TestManualRepair(ReferenceAtlasService service,ReferenceAtlasContext context,string path,AtlasSourceMapping valid)
    {
        var key=AiAtlasNormalizer.FrameKey(context.Frames[0].Descriptor);
        var other=AiAtlasNormalizer.FrameKey(context.Frames[1].Descriptor);
        var bad=valid.Clone();bad.FrameRectangles[key]=bad.FrameRectangles[other];bad.ConfirmedFrames.Add(key);
        using(var duplicate=service.Normalize(path,context,new(){SourceMapping=bad}))Require(duplicate.HasBlockingIssues,"重复帧未阻止");
        bad.FrameRectangles[key]=valid.FrameRectangles[key];bad.ConfirmedFrames.Add(key);
        using(var fixedResult=service.Normalize(path,context,new(){SourceMapping=bad}))Require(!fixedResult.HasBlockingIssues,"人工修正未解除阻断");
        bad.FrameRectangles[key]=new Rectangle(-10,0,48,48);
        using(var invalid=service.Normalize(path,context,new(){SourceMapping=bad}))Require(invalid.HasBlockingIssues,"越界源框未阻止");
    }

    private static void TestProtectedColor(ReferenceAtlasService service,ReferenceAtlasContext context,string path,string root)
    {
        using var image=new Bitmap(path);
        // An enclosed magenta detail must survive unless explicitly sampled as background.
        var layout=new ReferenceAtlasLayoutPlanner().Plan(context.Asset,context.Frames);
        var placement=layout.Placements[0];
        var x=placement.Bounds.X*2+38;var y=placement.Bounds.Y*2+38;
        using(var g=Graphics.FromImage(image)) {g.FillRectangle(Brushes.Black,x-5,y-5,14,14);g.FillRectangle(Brushes.Magenta,x,y,4,4);}
        var testPath=Path.Combine(root,"protected-magenta.png");image.Save(testPath,ImageFormat.Png);
        using var result=service.Normalize(testPath,context,new());
        var frame=result.FrameComparisons[AiAtlasNormalizer.FrameKey(placement.Frame.Descriptor)].RawAiFrame;
        Require(frame.GetPixel(19,19).A>0&&frame.GetPixel(19,19).R>240,"封闭品红特效被全局删除");
    }

    private static void TestCanvasVariants(ReferenceAtlasService service,ReferenceAtlasContext context,string path,string root)
    {
        using var source=new Bitmap(path);
        foreach(var dimensions in new[]{new Size(511,511),new Size(817,1230),new Size(1230,817)})
        {
            using var output=new Bitmap(dimensions.Width,dimensions.Height);
            var side=Math.Min(dimensions.Width-31,dimensions.Height-43);
            using(var graphics=Graphics.FromImage(output))
            {
                graphics.Clear(Color.Magenta);
                graphics.InterpolationMode=System.Drawing.Drawing2D.InterpolationMode.NearestNeighbor;
                graphics.PixelOffsetMode=System.Drawing.Drawing2D.PixelOffsetMode.Half;
                graphics.DrawImage(source,new Rectangle(13,19,side,side),new Rectangle(Point.Empty,source.Size),GraphicsUnit.Pixel);
            }
            var outputPath=Path.Combine(root,$"variant-{dimensions.Width}-{dimensions.Height}.png");output.Save(outputPath,ImageFormat.Png);
            using var result=service.Normalize(outputPath,context,new());
            Require(!result.HasBlockingIssues,$"非整数/横竖画布映射失败 {dimensions}: "+string.Join(";",result.FrameDiagnostics.Where(d=>d.Severity==AtlasIssueSeverity.Error).Select(d=>d.Message)));
            Require(result.Frames.All(f=>f.Bitmap.Size==new Size(f.Descriptor.Width,f.Descriptor.Height)),"还原画布尺寸错误");
        }
        // Change row spacing and move each row independently; semantic order stays fixed.
        var layout=new ReferenceAtlasLayoutPlanner().Plan(context.Asset,context.Frames);
        using var drift=new Bitmap(1000,1250);
        using(var graphics=Graphics.FromImage(drift))
        {
            graphics.Clear(Color.Magenta);
            foreach(var row in layout.Placements.GroupBy(p=>p.Bounds.Y).OrderBy(g=>g.Key).Select((g,i)=>(Frames:g.ToArray(),Row:i)))
            foreach(var placement in row.Frames)
            {
                var col=Array.IndexOf(row.Frames,placement);
                var size=placement.Bounds.Width*2;
                var x=40+(row.Row%2)*19+col*(size+11);
                var y=15+row.Row*202;
                graphics.DrawImage(placement.Frame.Bitmap,new Rectangle(x,y,size,size));
            }
        }
        var driftPath=Path.Combine(root,"row-drift.png");drift.Save(driftPath,ImageFormat.Png);
        using var driftResult=service.Normalize(driftPath,context,new());
        Require(!driftResult.HasBlockingIssues,"分区/行间距变化不能配准");
    }

    private static void TestTransaction(ProjectProfile project,LogicalImageAsset asset,IReadOnlyList<DecodedFrame> frames)
    {
        var before=asset.Frames.Select(f=>f.SourcePath).Distinct().ToDictionary(p=>p,File.ReadAllBytes);
        var history=new HistoryService(Path.Combine(project.RootPath,"history"));
        var mutation=new ImageMutationService(history);
        var plan=new RsImportService().PlanImport(project,asset,frames);
        Require(plan.Files.Count==3,"不是三文件事务");
        var committed=mutation.Commit(project,plan);Require(committed.Success,"副本写入失败："+committed);
        foreach(var file in plan.Files)
        {
            var old=E5Archive.Parse(file.TargetPath,before[file.TargetPath]);var current=E5Archive.OpenFresh(file.TargetPath);
            Require(old.ReadStored(1).SequenceEqual(current.ReadStored(1))&&old.ReadStored(3).SequenceEqual(current.ReadStored(3)),"非目标条目存储内容改变");
            Require(current.ReadDecoded(2).SequenceEqual(E5Archive.Parse(file.TargetPath,file.CandidateBytes).ReadDecoded(2)),"目标条目写后复读不一致");
        }
        Require(history.Undo(project,committed.HistoryId!).Success,"撤回失败");
        foreach(var pair in before)Require(File.ReadAllBytes(pair.Key).SequenceEqual(pair.Value),"撤回非原始字节");
        Require(history.Redo(project,committed.HistoryId!).Success,"重做失败");
        Require(history.Undo(project,committed.HistoryId!).Success,"重做后撤回失败");
    }

    private static byte[] Archive(IReadOnlyList<byte[]> payloads)
    {
        var offset=E5Archive.IndexOffset+payloads.Count*E5Archive.EntrySize;var bytes=new byte[offset+payloads.Sum(p=>p.Length)];
        for(var i=0;i<payloads.Count;i++)
        {var slot=E5Archive.IndexOffset+i*E5Archive.EntrySize;BinaryPrimitives.WriteUInt32BigEndian(bytes.AsSpan(slot,4),(uint)payloads[i].Length);BinaryPrimitives.WriteUInt32BigEndian(bytes.AsSpan(slot+4,4),(uint)payloads[i].Length);BinaryPrimitives.WriteUInt32BigEndian(bytes.AsSpan(slot+8,4),(uint)offset);payloads[i].CopyTo(bytes,offset);offset+=payloads[i].Length;}
        return bytes;
    }

    private static string FindWorkspace()
    {
        for(var d=new DirectoryInfo(Directory.GetCurrentDirectory());d!=null;d=d.Parent)
            if(Directory.Exists(Path.Combine(d.FullName,"形象管理器","src")))return d.FullName;
        throw new DirectoryNotFoundException("请在项目目录运行参考图验收。");
    }
    private static void Require(bool condition,string message){if(!condition)throw new InvalidOperationException(message);}
}
