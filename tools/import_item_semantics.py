"""Import reviewed item byte evidence and category semantics.

Run after import_data_manager_facts.py with --workspace <source-workspace>.
Only relative source paths, hashes and small structured byte observations are
published. Original game files, executables and editor build outputs stay out.
The importer is deterministic and does not turn editor labels into runtime proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROFILE65 = "profile.ccz65.unencrypted.f9a"
PROFILE66 = "profile.ccz66.shanzai.guoqing.f36"
SOURCE_FILES = {
    "semantic-resolver": "data管理器/src/DataManager.Core/Domain/ItemSemanticResolver.cs",
    "consumable-catalog": "data管理器/src/DataManager.Core/Domain/ConsumableItemEffectCatalogService.cs",
    "semantic-tests": "data管理器/src/DataManager.Tests/ItemSemanticEditingTests.cs",
    "business-ui": "data管理器/src/DataManager.App/BusinessEditorPanel.cs",
    "business-compact-ui": "data管理器/src/DataManager.App/BusinessEditorPanel.Compact.cs",
    "semantic-report": "data管理器/验证/2026-10-20-宝物读写修复/验收报告.md",
    "legacy-equipment": "老版游戏制作工具/CCZ-ExtendModifier-main/ExtendModifier/ExtendModifierZHUANGBEI.cpp",
    "legacy-consumable": "老版游戏制作工具/CCZ-ExtendModifier-main/ExtendModifier/ExtendModifierDAOJU.cpp",
    "publish-report": "data管理器/验证/2026-10-20-单文件发布验收.md",
    "meff-gallery-codec": "形象管理器/src/ImageManager.Core/StrategyAnimationResourceCodec.cs",
    "meff-player": "形象管理器/src/ImageManager.App/SelectedAnimationPreview.cs",
    "meff-preview-report": "data管理器/验证/2026-10-20-Meff图库点击播放修复.md",
}


def read(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))


def write(relative: str, value: dict) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def observe(workspace: Path) -> dict:
    cases = []
    relative = Path("基底/复刻版6.6山贼 国庆")
    raw = (workspace / relative / "Star.e5").read_bytes()
    for item_id, expected, job_name in [(154, 1, "侠客"), (156, 5, "君主"), (157, 60, "侠客"), (149, 22, "所有兵种"), (139, 7, "上将")]:
        offset = (item_id - 104) * 25
        row = raw[offset:offset + 25]
        if row[0x15] != expected:
            raise ValueError(f"sample changed: {item_id}; re-audit before importing")
        cases.append({"itemId": item_id, "name": row[:15].split(b"\0")[0].decode("gbk"),
                      "fileOffset": f"0x{offset:X}", "rawRowHex": row.hex(" ").upper(),
                      "actualEffectId": row[0x11], "categoryMarker": row[0x12], "effectValue": row[0x15],
                      "reserved16": row[0x16], "suitableJob": row[0x17], "jobName": job_name,
                      "price": row[0x13], "gallery": row[0x18]})
    sample65 = Path("基底/加强版6.5未加密版")
    star65 = (workspace / sample65 / "Star.e5").read_bytes()
    consumables = []
    for index in range(151):
        row = star65[index * 25:(index + 1) * 25]
        if row[0x12] != 3:
            continue
        consumables.append({"itemId": index + 104, "name": row[:17].split(b"\0")[0].decode("gbk"),
                            "actualEffectId": f"0x{row[0x11]:02X}", "parameter": row[0x15] | row[0x16] << 8,
                            "rawRowHex": row.hex(" ").upper()})
    value = {"schemaVersion": 1, "observationDate": "2026-10-20", "evidence": "sample-byte-observed",
             "sample66": {"profile": PROFILE66, "relativePath": relative.as_posix(),
                          "files": [{"name": name, "length": (workspace / relative / name).stat().st_size,
                                     "sha256": digest(workspace / relative / name)}
                                    for name in ["Data.e5", "Star.e5", "Ekd5.exe", "Imsg.e5"]],
                          "accessoryCases": cases},
             "sample65": {"profile": PROFILE65, "relativePath": sample65.as_posix(),
                          "file": "Star.e5", "length": len(star65), "sha256": digest(workspace / sample65 / "Star.e5"),
                          "consumableCases": consumables},
             "limits": ["原始字节可证明偏移和值；业务名称另有用户确认及旧工具源码佐证。",
                        "编辑器保存/CSV复读可证明文件读写一致，不等同于每种效果的游戏内运行时验证。",
                        "F36当前数据文件哈希与历史A346/AA3D样本不同，不覆盖历史指纹，不归入仅有长度的old-shanzhai画像。"]}
    write("sources/item-semantic-byte-evidence.json", value)
    return value


def register_sources(workspace: Path) -> None:
    manifest = read("sources/source-manifest.json")
    sources = {entry["id"]: entry for entry in manifest["entries"]}
    sources.pop("src.items.meff-preview-tests", None)
    for key, relative in SOURCE_FILES.items():
        sources["src.items." + key] = {
            "id": "src.items." + key, "path": relative, "sha256": digest(workspace / relative),
            "sourceType": "test-report" if key.endswith("report") else "first-party-source",
            "published": False, "usedFor": "类别感知宝物读写、独立消耗品目录与可复现回归；不扩大游戏消费者证据"}
    for key, relative, kind in [("user-confirmation", "sources/item-consumable-user-confirmation.md", "user-confirmation"),
                                ("byte-evidence", "sources/item-semantic-byte-evidence.json", "sample-byte-audit")]:
        sources["src.items." + key] = {"id": "src.items." + key, "path": relative,
                                     "sha256": digest(ROOT / relative), "sourceType": kind,
                                     "published": True, "usedFor": "本轮用户命名来源与独立原始字节，区分标签/样本/运行时证据"}
    manifest["entries"] = sorted(sources.values(), key=lambda entry: entry["id"])
    write("sources/source-manifest.json", manifest)


def semantic_structure(version: str, observation: dict) -> None:
    code = version.replace(".", "")
    profile = PROFILE65 if version == "6.5" else PROFILE66
    fields = [
        ("类型或实际特效", "0x11", "普通武器/防具为装备类型；辅助/消耗品为实际特效号。6.6动态Codec以原始+0x11>=26且原始+0x12为2/3的联合条件决定逻辑列映射。"),
        ("特效或类别标记", "0x12", "普通武器/防具为装备特效号；辅助=2、消耗品=3类别标记，不得显示成枪许可或普通装备特效。"),
        ("价格", "0x13", "价格单位100；255表示不可买卖。辅助+0x17是适用兵种，不是价格。"),
        ("初始属性或辅助效果或参数低字节", "0x15", "武器/防具=初始属性；辅助=特殊效果值；消耗品=LE UInt16参数低字节。原CSV列名初始能力。"),
        ("装备效果或保留或参数高字节", "0x16", "武器/防具=特殊效果值；辅助=空/保留；消耗品=参数高字节。原CSV列名装备特效值。"),
        ("成长或适用兵种或保留", "0x17", "武器/防具=能力成长；辅助=适用兵种系ID（255=所有兵种）；消耗品=空/保留。原CSV列名能力成长。"),
        ("图鉴", "0x18", "图鉴标记。勾选框主动修改写0/1，未主动修改的非零原值保持；不在只读浏览时归一化。")]
    entry = {"id": f"struct.{code}.item-category-semantics", "title": version + " 宝物按类别解释与字段读写契约",
             "aliases": ["辅助特殊效果值", "适用兵种", "适合兵种", "图鉴勾选框", "255表示不可买卖", "0x15", "0x17"],
             "versions": [version], "profile": profile, "status": "canonical",
             "evidence": "legacy-source-reviewed-sample-bytes-editor-roundtrip", "stride": 25,
             "indexFormula": "row = Data.e5[0x818C + ID*25] for 0<=ID<=103; row = Star.e5[(ID-104)*25] for 104<=ID<=254; field = row + field_offset",
             "endianness": "little", "encoding": "GBK；名称宽度和图标位置按目标Codec，不从类别推断",
             "fields": [{"name": name, "offset": offset, "width": 1, "type": "uint8", "meaning": meaning} for name, offset, meaning in fields],
             "relations": ["format.data-manager.item-codecs", "format.item.split-data-star", "mechanism.shared.consumable-effect-namespace"],
             "notes": ["本实体说明类别语义；物理文件基址、名称/图标布局和每个Variant的写入门禁由既有物理表实体负责。",
                       "分类先读取本项目System.ini的DefID/AssID（缺失时70/109），再结合ID区段、当前草稿和Codec类别标记，不能按特效号大小臆测类别。",
                       "辅助适用兵种的0..39是兵种系编号，名称来自当前项目；它不是detailed-job-growth的26个普通装备许可列。",
                       "业务名称可变，CSV继续使用原物理列名；固定6.5与动态6.6不能靠相同列名直接复制字节。",
                       "同表跨类别切换必须更新布局和选项；摘要从草稿按原始类别标记选地址，不能只读OriginalFileBytes。"],
             "writeGates": ["源文件SHA、Profile/Variant、25字节行边界和字段范围均通过后，只对主动修改字段生成补丁。",
                            "已知图鉴/辅助适用兵种/参数可编辑；空或保留字节只在明确的原始字段入口编辑，未修改必须原样保持。",
                            "6.6名称布局的Preserve字节仍不开放普通字段编辑；类别变化不自动改写保留字节。",
                            "保存前草稿可整体撤回；保存后按相同Codec复读并逐字节限制变更范围，失败回滚；本契约不证明游戏内效果已经运行。"],
             "sourceRefs": ["src.data-manager.item-types", "src.data-manager.codecs", "src.items.semantic-resolver",
                            "src.items.legacy-equipment", "src.items.legacy-consumable", "src.items.semantic-tests", "src.items.user-confirmation", "src.items.byte-evidence"]}
    if version == "6.6":
        entry["sampleCases"] = observation["sample66"]["accessoryCases"]
        entry["notes"].append("五例绑定当前F36 EXE与B392 Star数据哈希；测试强制66-shanzhai-legacy仅用于相同Codec的字段回归，不证明旧1146880字节EXE画像可写。")
    write(f"{version}/data/structures/item-category-semantics.json", {"schemaVersion": 1, "entityType": "data-structure", "entries": [entry]})


def update_existing() -> None:
    path = "6.5/data/file-formats/data-manager-formats.json"
    formats = read(path)
    for entry in formats["entries"]:
        if entry["id"] == "format.data-manager.item-codecs":
            entry["entryFields"] = [field for field in entry["entryFields"] if field["offset"] != "0x15"]
            for field in entry["entryFields"]:
                if field["offset"] == "0x13": field["meaning"] = "价格单位100；255表示不可买卖，不能用辅助+0x17替代。"
                if field["offset"] in {"0x0", "0xF"}:
                    field["overlay"] = "item-name-icon-layout"
            entry["entryFields"].append({"name": "类别相关尾部", "offset": "0x15", "width": 4, "type": "uint8[4]",
                                         "meaning": "按类别解释：武器/防具为初始属性、特效值、成长、图鉴；辅助为特效值、保留、适用兵种、图鉴；消耗品为LE参数低/高字节、保留、图鉴。"})
            entry["relations"] = ["struct.65.item-category-semantics", "struct.66.item-category-semantics", "mechanism.shared.consumable-effect-namespace"]
            new = ["物理CSV列名与业务语义分离：辅助效果写初始能力(+0x15)、适用兵种写能力成长(+0x17)，图鉴主动修改写0/1；未修改字节保留。",
                   "item-name-icon-layout 为互斥Variant的布局overlay：17字节名称布局不含+0x0F图标，15字节名称布局在+0x0F存图标；按Profile选择一种，不能同时解析为两个可写字段。",
                   "消耗品实际特效号来自+0x11，使用独立道具目录；固定17字节Codec的实际特效逻辑列是宝物类型，动态15字节Codec是装备特效号。",
                   "ID255不创建有效物品行；标准Data/Star读取0..103和104..254；根Item/Itemmsg读取256..511且必须分别检查表几何和运行时加载器。"]
            entry["semantics"] = [x for x in entry["semantics"] if x not in new] + new
            entry["sourceRefs"] = sorted(set(entry["sourceRefs"] + ["src.items.semantic-resolver", "src.items.byte-evidence", "src.items.semantic-tests"]))
        if entry["id"] in {"format.data-manager.strategy-animation-payload", "format.data-manager.image-resources"}:
            note = "Meff规范路径优先E5/Meff.e5；十八州样本目录四字节尾部可非零，必须用OpenMeff专用读取，普通E5保持严格零尾部。缩略图、完整解码、播放间隔、导出和原生平面均复用ReadPackageBytes；只让首帧解码成功仍会导致图库点击播放失败。"
            entry["semantics"] = [x for x in entry["semantics"] if x != note] + [note]
            entry["sourceRefs"] = sorted(set([ref for ref in entry["sourceRefs"] if ref != "src.items.meff-preview-tests"] +
                                             ["src.items.meff-gallery-codec", "src.items.meff-player", "src.data-manager.image-animation-preview-ui-tests"]))
    write(path, formats)
    for path in ["6.6/data/structures/runtime-structures.json", "6.6/data/structures/f36-shanzai-structures.json"]:
        doc = read(path)
        for entry in doc["entries"]:
            if entry["id"] not in {"struct.66.item-record", "struct.66.f36.item-record"}: continue
            if entry["id"] == "struct.66.item-record":
                entry["indexFormula"] = "Data.e5 + 0x818C + item_id*0x19 for 0..103; Star.e5 + (item_id-104)*0x19 for 104..254; ID255 reserved"
            for field in entry["fields"]:
                if field["offset"] == "0x15": field["meaning"] = "普通装备初始属性；辅助特效值；消耗品参数低字节；按类别解释。"
                if field["offset"] == "0x16": field["meaning"] = "普通装备特效值；辅助保留；消耗品参数高字节。运行时该字段消费仍按原静态证据边界，不推广为所有类别通用效果值。"
                if field["offset"] == "0x17": field["meaning"] = "普通装备成长；辅助适用兵种；消耗品保留。"
                if field["offset"] == "0x13": field["meaning"] = "价格单位100，255不可买卖。"
            entry["relations"] = sorted(set(entry.get("relations", []) + ["struct.66.item-category-semantics"]))
            entry["sourceRefs"] = sorted(set(entry["sourceRefs"] + ["src.items.semantic-resolver", "src.items.byte-evidence"]))
        write(path, doc)


def link_consumable_evidence(observations: dict) -> None:
    path = "6.5/data/mechanisms/consumable-effects.json"
    doc = read(path)
    entry = next(item for item in doc["entries"] if item["id"] == "mechanism.shared.consumable-effect-namespace")
    samples = observations["sample65"]["consumableCases"]
    for effect in entry["effects"]:
        matched = [sample for sample in samples if sample["actualEffectId"] == effect["id"]]
        if not matched:
            continue
        effect["sampleItems"] = [{"itemId": sample["itemId"], "name": sample["name"],
                                  "sourceRef": "src.items.byte-evidence"} for sample in matched]
        effect["sourceRefs"] = sorted(set(effect["sourceRefs"] + ["src.items.byte-evidence"]))
    entry["relations"] = sorted(set(entry["relations"] + [
        "format.data-manager.item-codecs", "struct.65.item-category-semantics",
        "struct.66.item-category-semantics", PROFILE65, PROFILE66]))
    entry["sourceRefs"] = sorted(set(entry["sourceRefs"] + ["src.items.byte-evidence"]))
    write(path, doc)

    path = "research/research-gaps.json"
    doc = read(path)
    gap = {"id": "research.shared.consumable-effect-consumers", "title": "消耗品 0x1A–0x3D 分发表、参数消费与效果闭环",
           "versions": ["6.5", "6.6"], "status": "open", "evidence": "labels-and-sample-bytes-without-per-effect-runtime",
           "known": ["独立目录覆盖36个编号；用户标签、编辑器源码与样本原始字节已分别登记。",
                     "6.5 Star.e5 的25个消耗品样本可核对实际特效号及+0x15/+0x16参数原值，但样本名称不能独立证明执行行为。",
                     "原请求重复写0x28；目录采用0x28恢复SP，0x2B MP上升为仙酒样本支持的推定。"],
           "needed": ["对精确SHA的6.5/6.6目标EXE分别定位消耗品分发表，登记每个编号的入口、调用契约及参数宽度、单位和上下限。",
                      "用正负样本验证0x28恢复SP与0x2B MP上升，记录前后状态及副作用，不能仅凭目录名称消解冲突。",
                      "区分0x2C–0x30和0x35–0x39的数字显示策略与真实行为；补齐0x31–0x34及0x3A–0x3D的目标、技能/策略ID和材料消费规则。",
                      "逐编号完成静态消费者或运行时闭环后更新既有目录证据，不能把整个候选目录一次性升级为运行时事实。"],
           "sourceRefs": ["src.items.consumable-catalog", "src.items.user-confirmation", "src.items.byte-evidence"]}
    doc["entries"] = [item for item in doc["entries"] if item["id"] != gap["id"]] + [gap]
    write(path, doc)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    workspace = parser.parse_args().workspace.resolve()
    observations = observe(workspace)
    register_sources(workspace)
    profiles = read("6.6/data/profiles/engine-profiles.json")
    profile = next(entry for entry in profiles["entries"] if entry["id"] == PROFILE66)
    profile["companionDataFiles"] = observations["sample66"]["files"]
    profile["sourceRefs"] = sorted(set(profile["sourceRefs"] + ["src.items.byte-evidence"]))
    write("6.6/data/profiles/engine-profiles.json", profiles)
    for version in ["6.5", "6.6"]:
        semantic_structure(version, observations)
    update_existing()
    link_consumable_evidence(observations)
    print("item_semantics=2 accessory_cases=5 consumable_samples=" + str(len(observations["sample65"]["consumableCases"])))


if __name__ == "__main__":
    main()
