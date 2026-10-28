"""Import reviewed storage facts from a local DataManager source checkout.

Usage: python tools/import_data_manager_facts.py --workspace <source-workspace>
The source checkout is evidence, not a runtime dependency of this knowledge base.
This importer resolves inheritance exactly as ProfileRegistry does, retains every
field, and never upgrades unavailable/inherited layouts into writable facts.
Special binary formats remain manually reviewed JSON beside the imported tables.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROFILE_IDS = {
    "64-xisui-v1": "profile.ccz64.xisui.9112",
    "65-standard-v1": "profile.ccz65.unencrypted.f9a",
    "66-standard-v1": "profile.ccz66.data-manager.standard",
    "66-legacy-data-v1": "profile.ccz66.data-manager.17byte",
    "66-shanzhai-legacy": "profile.ccz66.data-manager.old-shanzhai",
}
SOURCES = {
    "profile64": "data管理器/config/profiles/ccz-6.4.json",
    "profile64-before-configuration": "data管理器/config/profiles/ccz-6.4.before-configuration.json",
    "configuration64": "data管理器/src/DataManager.Core/Profiles/Ccz64ConfigurationProbe.cs",
    "test64-compatibility": "data管理器/src/DataManager.Tests/Ccz64CompatibilityTests.cs",
    "test64-configuration": "data管理器/src/DataManager.Tests/Ccz64ConfigurationTests.cs",
    "test64-field-writeback": "data管理器/src/DataManager.Tests/FieldWritebackMatrixTests.cs",
    "guide64": "data管理器/文档/6.4洗隋兼容适配.md",
    "consumers64": "data管理器/验证/6.4修正-20261022/data64消费者.md",
    "report64-final": "data管理器/验证/6.4配置与装备类型修正-20261022/验收摘要.md",
    "profile65": "data管理器/config/profiles/ccz-6.5.json",
    "profile66": "data管理器/config/profiles/ccz-6.6.json",
    "registry": "data管理器/src/DataManager.Core/Profiles/ProfileRegistry.cs",
    "augmentation": "data管理器/src/DataManager.Core/Profiles/ProfileAugmentationService.cs",
    "embedded-probe": "data管理器/src/DataManager.Core/Profiles/EmbeddedEngineLayoutProbe.cs",
    "codecs": "data管理器/src/DataManager.Core/Binary/RecordCodecs.cs",
    "values": "data管理器/src/DataManager.Core/Binary/BinaryValueCodec.cs",
    "quotes": "data管理器/src/DataManager.Core/Domain/PersonQuoteService.cs",
    "groups": "data管理器/src/DataManager.Core/Domain/AccessoryJobGroupService.cs",
    "name-pool": "data管理器/src/DataManager.Core/Domain/EffectNamePoolService.cs",
    "item-types": "data管理器/src/DataManager.Core/Domain/ItemTypeService.cs",
    "studio-item-layout": "工具整合包/CCZModStudio/Core/Ccz66ItemLayoutService.cs",
    "studio-icon-mapping": "工具整合包/CCZModStudio/Core/ItemIconMappingService.cs",
    "attribute-reader": "data管理器/src/DataManager.Core/Binary/BinaryTableReader.cs",
    "csv": "data管理器/src/DataManager.Core/Csv/CsvService.cs",
    "csv-labels": "data管理器/src/DataManager.Core/Csv/CsvDisplayNameRegistry.cs",
    "business": "data管理器/src/DataManager.Core/Domain/BusinessDataService.cs",
    "unified-history": "data管理器/src/DataManager.App/UnifiedHistoryService.cs",
    "resource-history": "data管理器/src/DataManager.Images/ResourceHistoryAdapter.cs",
    "data-history": "data管理器/src/DataManager.Core/History/HistoryStore.cs",
    "image-history": "形象管理器/src/ImageManager.Core/HistoryService.cs",
    "transaction": "data管理器/src/DataManager.Core/Editing/WorkspaceBinaryTransaction.cs",
    "workspace": "data管理器/src/DataManager.Core/Editing/ProjectWorkspace.cs",
    "migration": "data管理器/src/DataManager.Core/Migration/MigrationService.cs",
    "item-migration": "data管理器/src/DataManager.Core/Migration/ItemMigrationMapper.cs",
    "effect-migration": "data管理器/src/DataManager.Core/Migration/ClassEffectMigrationMapper.cs",
    "native-migration": "data管理器/src/DataManager.Core/Migration/SpecialStructureMigrationDiagnostics.cs",
    "migration-models": "data管理器/src/DataManager.Core/Migration/MigrationModels.cs",
    "migration-commit": "data管理器/src/DataManager.Core/Migration/MigrationCommitCoordinator.cs",
    "migration-path-safety": "data管理器/src/DataManager.Core/Migration/MigrationPathSafety.cs",
    "migration-field-isolation": "data管理器/src/DataManager.Core/Migration/MigrationFieldIsolation.cs",
    "migration-resource-converter": "data管理器/src/DataManager.Core/Migration/IMigrationResourceConverter.cs",
    "atomic-item-migration": "data管理器/src/DataManager.Core/Migration/AtomicItemMigrationMapper.cs",
    "extended-item-migration": "data管理器/src/DataManager.Core/Migration/ExtendedItemMigrationMapper.cs",
    "migration-review-ui": "data管理器/src/DataManager.App/MigrationReviewDialog.cs",
    "migration-progress-ui": "data管理器/src/DataManager.App/MigrationProgressDialog.cs",
    "main-form": "data管理器/src/DataManager.App/MainForm.cs",
    "byte-chunk-merger": "data管理器/src/DataManager.Core/Binary/ByteChunkMerger.cs",
    "table-writer": "data管理器/src/DataManager.Core/Binary/BinaryTableWriter.cs",
    "history-models": "data管理器/src/DataManager.Core/Models/HistoryModels.cs",
    "image-migration-converter": "data管理器/src/DataManager.Images/ImageMigrationResourceConverter.cs",
    "image-adapter": "data管理器/src/DataManager.Images/ResourceCatalogAdapter.cs",
    "image-bindings": "data管理器/src/DataManager.Images/ResourceCatalogAdapter.Bindings.cs",
    "image-codecs": "形象管理器/src/ImageManager.Core/ResourceCodecs.cs",
    "image-e5": "形象管理器/src/ImageManager.Core/E5Archive.cs",
    "image-s-map": "形象管理器/src/ImageManager.Core/SPhysicalMappingService.cs",
    "image-animation": "形象管理器/src/ImageManager.Core/StrategyAnimationCodec.cs",
    "image-mutation": "形象管理器/src/ImageManager.Core/ImageMutationService.cs",
    "image-rs-import": "形象管理器/src/ImageManager.Core/RsImportService.cs",
    "image-pixel-editor": "形象管理器/src/ImageManager.App/PixelEditorDialog.cs",
    "image-preview-layout": "形象管理器/src/ImageManager.App/PreviewImageLayout.cs",
    "image-grid": "形象管理器/src/ImageManager.App/ImageGridPage.cs",
    "image-profile": "形象管理器/src/ImageManager.Core/ProjectProfileService.cs",
    "image-catalog": "形象管理器/src/ImageManager.Core/ImageCatalogService.cs",
    "image-dll-archive": "形象管理器/src/ImageManager.Core/DllBitmapArchive.cs",
    "image-dll-codec": "形象管理器/src/ImageManager.Core/DllBitmapResourceCodec.cs",
    "image-rendering": "形象管理器/src/ImageManager.Core/ImageRendering.cs",
    "image-bmp-payload": "形象管理器/src/ImageManager.Core/BmpPayloadService.cs",
    "image-face-payload": "形象管理器/src/ImageManager.Core/FacePayloadService.cs",
    "image-item-icon-derivation": "形象管理器/src/ImageManager.Core/ItemIconDerivationService.cs",
    "image-palette": "形象管理器/src/ImageManager.Core/PaletteService.cs",
    "image-special-codecs": "形象管理器/src/ImageManager.Core/SpecialResourceCodecs.cs",
    "image-weather-evidence": "data管理器/验证/图片协议修复/weather-consumer-evidence.json",
    "image-strip-exchange": "形象管理器/src/ImageManager.Core/RsStripExchangeService.cs",
    "image-reference-context": "形象管理器/src/ImageManager.Core/ReferenceAtlasContext.cs",
    "image-reference-atlas": "形象管理器/src/ImageManager.Core/ReferenceAtlasService.cs",
    "image-reference-layout": "形象管理器/src/ImageManager.Core/ReferenceAtlasLayoutPlanner.cs",
    "image-atlas-normalizer": "形象管理器/src/ImageManager.Core/AiAtlasNormalizer.cs",
    "image-atlas-models": "形象管理器/src/ImageManager.Core/Models.cs",
    "image-selection-appearance": "形象管理器/src/ImageManager.App/SelectionAppearance.cs",
    "image-built-in-help": "形象管理器/src/ImageManager.App/BuiltInDocumentation.cs",
    "image-atlas-import-dialog": "形象管理器/src/ImageManager.App/AiAtlasImportDialog.cs",
    "image-animation-dialog": "形象管理器/src/ImageManager.App/PreviewDialogs.cs",
    "image-animation-preview-ui-tests": "data管理器/src/DataManager.Tests/AnimationPreviewUiTests.cs",
    "image-atlas-import-ui-tests": "data管理器/src/DataManager.Tests/AtlasImportDialogTests.cs",
    "image-help-document": "形象管理器/docs/一体化管理器使用说明.md",
    "image-source-labels": "data管理器/src/DataManager.Images/ResourceDisplayNames.cs",
    "image-integrated-panel": "data管理器/src/DataManager.Images/IntegratedResourcePanel.cs",
    "publish-single-file": "data管理器/src/DataManager.App/Properties/PublishProfiles/SingleFileWinX64.pubxml",
    "bundle-verification": "data管理器/src/DataManager.App/BundleVerification.cs",
    "image-exchange-tests": "形象管理器/src/ImageManager.Tests/RsExchangeAndAtlasTests.cs",
    "image-test-runner": "形象管理器/src/ImageManager.Tests/Program.cs",
    "test-ui-presentation": "data管理器/src/DataManager.Tests/UiPresentationTests.cs",
    "image-codec-tests": "形象管理器/src/ImageManager.CodecTests/Program.cs",
    "image-codec-diagnostics": "data管理器/验证/图片交换与单文件验收-20261018/图片编解码-专项诊断.log",
    "image-codec-report": "data管理器/验证/图片交换与单文件验收-20261018/BMP-天气-动画核心专项报告.md",
    "image-acceptance-summary": "data管理器/验证/图片交换与单文件验收-20261018/图片协议验收摘要.json",
    "hybrid-icon-evidence": "data管理器/验证/图片交换与单文件验收-20261018/混合版RAW图标证据.json",
    "image-animation-consumer-evidence": "data管理器/验证/图片交换与单文件验收-20261018/6.5-动画消费者-402537-402e50.txt",
    "image-animation-mixer-evidence": "data管理器/验证/图片交换与单文件验收-20261018/6.5-动画混合-417024-417380.txt",
    "image-animation-thread-evidence": "data管理器/验证/图片交换与单文件验收-20261018/6.5-动画线程-41295c-412a30.txt",
    "image-pixel-mix-evidence": "data管理器/验证/图片交换与单文件验收-20261018/6.5-像素混合-40690c-406d20.txt",
    "image-color-mix-evidence": "data管理器/验证/图片交换与单文件验收-20261018/6.5-颜色混合-415a64-415bed.txt",
    "image-animation-ui65-log": "data管理器/验证/图片交换与单文件验收-20261018/动画界面-6.5专项.log",
    "image-animation-ui66-log": "data管理器/验证/图片交换与单文件验收-20261018/动画界面-6.6专项.log",
    "image-atlas-dialog-log": "data管理器/验证/图片交换与单文件验收-20261018/参考图后台取消UI.log",
    "hybrid-icon-log": "data管理器/验证/图片交换与单文件验收-20261018/混合版图标与版本-专项诊断.log",
    "bundle-final-report": "data管理器/验证/图片交换与单文件验收-20261018/单EXE最终隔离验收.json",
    "old-hex-tables": "工具整合包/CCZModStudio/Assets/ConfigTable/HexTable.xml",
    "test-profile-write": "data管理器/src/DataManager.Tests/ProfileWriteTests.cs",
    "test-business-write": "data管理器/src/DataManager.Tests/BusinessTableWriteTests.cs",
    "test-assignment": "data管理器/src/DataManager.Tests/AssignmentEvidenceTests.cs",
    "test-csv": "data管理器/src/DataManager.Tests/CsvTests.cs",
    "test-quotes": "data管理器/src/DataManager.Tests/PersonQuoteTests.cs",
    "test-runner": "data管理器/src/DataManager.Tests/Program.cs",
    "layout-evidence": "data管理器/验证/本轮逆向/66-layout-scan.json",
    "layout-collector": "data管理器/验证/本轮逆向/inspect_66_layouts.py",
    "offline-checker": "data管理器/验证/check-layout-knowledge.py",
    "test-item-migration": "data管理器/src/DataManager.Tests/ItemMigrationTests.cs",
    "test-native-migration": "data管理器/src/DataManager.Tests/NativeStructureMigrationTests.cs",
    "test-resource-bindings": "data管理器/src/DataManager.Tests/ResourceBindingMappingTests.cs",
    "test-item-icon-append": "data管理器/src/DataManager.Tests/ItemIconAppendTests.cs",
    "test-migration-ui": "data管理器/src/DataManager.Tests/MigrationUiTests.cs",
    "test-image-migration": "data管理器/src/DataManager.Tests/ImageMigrationConversionTests.cs",
    "test-real-migration": "data管理器/src/DataManager.Tests/RealProjectMigrationTests.cs",
    "test-migration-selection": "data管理器/src/DataManager.Tests/MigrationSelectionContractTests.cs",
    "test-migration-field-isolation": "data管理器/src/DataManager.Tests/MigrationFieldIsolationPerformanceTests.cs",
    "test-save-bulk": "data管理器/src/DataManager.Tests/SaveBulkPerformanceTests.cs",
    "test-resource-migration": "data管理器/src/DataManager.Tests/MigrationResourceTests.cs",
    "test-migration-isolation": "data管理器/src/DataManager.Tests/MigrationIsolationTests.cs",
    "test-migration-readonly": "data管理器/src/DataManager.Tests/ReadonlyResourceRollbackTests.cs",
}
OWNED_SOURCES = {
    "user-attribute-enums": "sources/data-manager-user-confirmed-enums.md",
}
JOB_ATTRIBUTE_ROWS = [
    (0, "移动声音", ["马蹄", "车轮", "脚步", "无声", "引擎", "预设1", "预设2"]),
    (1, "移动速度", ["快速", "慢速"]),
    (2, "攻击声音", ["剑", "其他", "爆炸1", "爆炸2", "火箭筒", "枪声（连射）", "枪声（点射）", "火焰喷射", "毒气喷射"]),
    (3, "远程兵种", None), (4, "攻击延迟", None),
    (5, "兵种类型", ["全能", "文官", "武将"]),
    (6, "策略伤害", None), (7, "参与围攻", None),
]


def write_json(relative: str, value: dict) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


ACTIVE_SOURCE_PREFIX = "src.data-manager."


def source_id(key: str) -> str:
    """Return the source namespace for the active import.

    The 6.4 evidence was collected from a different source snapshot than the
    existing 6.5/6.6 records. Keep that namespace separate so a changed local
    hash can never silently replace an older source record with the same label.
    """
    return ACTIVE_SOURCE_PREFIX + key


def register_sources(workspace: Path, destination: Path | None = None, only64: bool = False) -> None:
    destination = destination or ROOT / "sources/source-manifest.json"
    registry = read_json(destination) if destination.exists() else {"schemaVersion": 1, "entries": []}
    current = {item["id"]: item for item in registry["entries"]}
    keys64 = {"profile64", "profile64-before-configuration", "configuration64", "test64-compatibility",
              "test64-configuration", "test64-field-writeback", "guide64", "consumers64", "report64-final",
              "profile65", "registry", "augmentation", "embedded-probe", "codecs", "values", "quotes",
              "test-quotes", "test-profile-write", "studio-item-layout", "studio-icon-mapping",
              "attribute-reader", "name-pool", "csv", "transaction", "migration", "test-runner"}
    for key, relative in SOURCES.items():
        if only64 and key not in keys64:
            continue
        path = workspace / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        identifier = source_id(key)
        value = {
            "id": identifier, "path": relative,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper(),
            "sourceType": ("static-audit" if key in {"image-weather-evidence", "image-animation-consumer-evidence", "image-animation-mixer-evidence", "image-animation-thread-evidence", "image-pixel-mix-evidence", "image-color-mix-evidence", "hybrid-icon-evidence"}
                           else "test-report" if key in {"image-codec-diagnostics", "image-codec-report", "image-acceptance-summary", "image-animation-ui65-log", "image-animation-ui66-log", "image-atlas-dialog-log", "hybrid-icon-log", "bundle-final-report"} else "first-party-source"), "published": False,
            "usedFor": "6.4/6.5/6.6 一体化编辑器的物理布局、专用编解码和可复现写入门禁",
            "verification": {"kind": "external-local", "reason": "原始源码/证据位于输入工作区，不随知识库分发；保留精确SHA，发布前可补固定Git提交或仓库内证据快照。"},
        }
        previous = current.get(identifier)
        if previous and previous.get("sha256") == value["sha256"]:
            # Keep published snapshot and repository provenance added by the audit.
            continue
        if previous:
            value["historicalRevisions"] = [previous]
        current[identifier] = value
    for key, relative in OWNED_SOURCES.items():
        current[source_id(key)] = {
            "id": source_id(key), "path": relative,
            "sha256": hashlib.sha256((ROOT / relative).read_bytes()).hexdigest().upper(),
            "sourceType": "user-confirmation", "published": True,
            "usedFor": "用户确认的兵种系属性枚举名称；不是逆向或引擎运行时验证证据",
            "verification": {"kind": "repository-file"},
        }
    registry["entries"] = sorted(current.values(), key=lambda item: item["id"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def merge_collection(relative: str, entity_type: str, entries: list[dict], refresh: bool = False) -> None:
    """Retain reviewed IDs unless an explicit refresh was requested.

    Importers are acquisition tools, not authority for deleting manually reviewed
    additions. A normal repeat import adds missing IDs and is otherwise stable.
    """
    path = ROOT / relative
    existing = read_json(path)["entries"] if path.exists() else []
    current = {item["id"]: item for item in existing}
    for entry in entries:
        if refresh or entry["id"] not in current:
            current[entry["id"]] = entry
    write_json(relative, {"schemaVersion": 1, "entityType": entity_type,
                          "entries": sorted(current.values(), key=lambda item: item["id"])})


def resolve(base: dict, child: dict | None, variant: dict) -> list[dict]:
    tables = {}
    for layer in [base] + ([child] if child else []):
        for table in layer.get("tables", []):
            existing = tables.get(table["key"], {})
            tables[table["key"]] = {**copy.deepcopy(existing), **copy.deepcopy(table)}
    for table in variant.get("tableOverrides", []):
        tables[table["key"]].update(copy.deepcopy(table))
    return list(tables.values())


def expand_fields(table: dict) -> list[dict]:
    result = []
    for field in table["fields"]:
        names = field.get("names")
        if not names:
            count = field.get("count", 1)
            pattern = field.get("namePattern", field.get("name", ""))
            names = [pattern.replace("{0:D2}", f"{index:02d}").replace("{0}", str(index))
                     for index in range(count)]
        for index, name in enumerate(names):
            offset = field["offset"] + index * field.get("stride", field["size"])
            policy = field.get("policy", "Editable")
            kind = {"UInt8": "uint8", "UInt16": "uint16le", "UInt32": "uint32le",
                    "FixedString": "fixed-string", "RawBytes": "bytes"}[field["kind"]]
            meaning = name + "；字段策略 " + policy
            if field.get("referenceTable"):
                meaning += "；引用 " + field["referenceTable"]
            if kind == "fixed-string":
                meaning += "；GBK，零终止或固定宽度填充，不允许截断多字节字符"
            value = {"name": name, "offset": f"0x{offset:X}", "width": field["size"],
                     "type": kind, "meaning": meaning, "writePolicy": policy}
            for key in ("minimum", "maximum", "referenceTable", "csvName"):
                if key in field:
                    value[key] = field[key]
            result.append(value)
    # A few Profiles retain a Preserve alias beside a newly named editable
    # field at exactly the same physical byte. Preserve both source names and
    # declare their shared storage instead of inventing a second independent byte.
    ranges = {}
    for field in result:
        ranges.setdefault((field["offset"], field["width"]), []).append(field)
    for (offset, width), aliases in ranges.items():
        if len(aliases) > 1:
            for field in aliases:
                field["overlay"] = f"physical-alias-{offset}-{width}"
    return result


def create_profiles(config66: dict, refresh: bool = False) -> None:
    entries = []
    for variant in config66["variants"]:
        samples = variant.get("fingerprints", [])
        complete = [sample for sample in samples if sample.get("sha256", {}).get("Ekd5.exe")]
        candidate = not complete
        first = complete[0] if complete else None
        entry = {
            "id": PROFILE_IDS[variant["id"]], "title": variant["displayName"] + " 数据编辑画像",
            "versions": ["6.6"], "aliases": ["ccz-6.6", variant["id"], variant["layoutId"]],
            "status": "candidate" if candidate else "canonical",
            "evidence": "length-only-source-record" if candidate else "source-reviewed-sample-fingerprints",
            "imageBase": "0x00400000", "machine": "x86-pe32",
            "sample": None if not first else {"file": "Ekd5.exe", "size": first["fileLengths"]["Ekd5.exe"],
                                              "sha256": first["sha256"]["Ekd5.exe"]},
            "sampleFingerprints": samples,
            "addressPolicy": "画像识别与字段证据分开：匹配样本不能自动证明继承表；每张表仍检查 capability、文件边界、消费签名及字段策略。VA 必须按目标 PE 节映射为 fileOffset。",
            "writePolicy": "不得自动写入；取得完整原样样本和独立布局证据前仅作手动布局候选。" if candidate else "仅支持匹配样本或通过逐项布局门禁的衍生项目；不把 6.5 偏移无条件套入 6.6。",
            "sourceRefs": [source_id("profile66"), source_id("registry"), source_id("augmentation")],
        }
        entries.append(entry)
    merge_collection("6.6/data/profiles/data-manager-layouts.json", "engine-profile", entries, refresh)


def table_entry(table: dict, version: str, variant: dict, fingerprint65: dict) -> dict:
    variant_id = variant["id"]
    profile = PROFILE_IDS[variant_id]
    capability = table.get("capability", "Editable")
    verification = table.get("verificationLevel", "InheritedUnverified")
    excluded = table["key"] in {"job-series-accessory-groups", "item-acquisition-low", "item-acquisition-high"}
    inherited66 = version == "6.6" and verification == "InheritedUnverified"
    candidate = capability == "Unavailable" or excluded or inherited66 or variant_id == "66-shanzhai-legacy"
    stride = table["rowSize"]
    start = table["offset"]
    count = table["rows"]
    begin = table.get("beginId", 0)
    end = start + stride * count
    samples = variant.get("fingerprints", []) or [fingerprint65]
    bounds = []
    for sample in samples:
        size = sample.get("fileLengths", {}).get(table["file"])
        bounds.append({"sampleId": sample["sampleId"], "fileLength": size,
                       "fits": None if size is None else end <= size,
                       "sha256": sample.get("sha256", {}).get(table["file"])})
    if table["key"] == "job-series-accessory-groups":
        address = None
        formula = "不解析占位 offset=0；实际地址由 VA 0x0044C341 经目标 PE 节表映射；参见 format.65.accessory-job-groups"
    else:
        address = {"kind": "fileOffset", "value": f"0x{start:X}", "profile": profile,
                   "evidence": "candidate-source-layout" if candidate else "source-reviewed"}
        formula = f"{table['file']} + 0x{start:X} + (ID - {begin}) * 0x{stride:X} + field_offset; ID={begin}..{begin+count-1}"
    gates = ["文件长度必须覆盖 endExclusive；编码、数值边界、字段策略及 Profile/Variant 必须匹配。",
             "仅修改被编辑字段的补丁；完整原始行、未拆字节、Preserve/ReadOnly 字段及槽尾保持原样。",
             "提交前核对加载时 SHA-256；跨表草稿统一提交、写后按当前 Codec 复读；失败回滚。"]
    if candidate:
        gates.insert(0, "不得自动写入：本条为候选/不可用/继承未验证结构，须先取得独立证据；不能因文件足够长而开放写入。")
    dynamic66 = version == "6.6" and table["key"] in {"person-r-assign", "person-s-assign", "strategy-terrain-availability"}
    if table.get("capabilityEvidence") and not dynamic66:
        gates.append(table["capabilityEvidence"])
    if excluded and table["key"].startswith("item-acquisition"):
        gates.append("旧 HexTable.xml 的 Enable=false；6.5 文件边界不足，6.6 旧区域与宝物说明/撤退区域冲突且未确认消费引用，禁止读取或写入。")
    if table["key"] == "person-retreat-quotes" and version == "6.6":
        gates.append("只使用 +491600 的 49×200 区；+440200 仅用于旧区冲突诊断。450000 字节 Imsg 样本不满足边界，必须 unavailable。")
    if table["key"] in {"person-r-assign", "person-s-assign", "strategy-terrain-availability"}:
        gates.append("静态配置之外还必须执行 ProfileAugmentationService 的实际 PE 消费者/INI/资源和样本数值门禁；不能仅凭本条几何开放写入。")
        if version == "6.6":
            gates.append("静态配置 Unavailable 是未探测默认值；EmbeddedEngineLayoutProbe 唯一消费者签名和 PE 目标区映射通过时，运行时将几何替换为探测结果并升级 Editable。此处不是所有 6.6 一律不可用。")
    entry = {
        "id": f"struct.{version.replace('.', '')}.disk.{variant_id}.{table['key']}",
        "title": f"{variant_id} {table['displayName']}（{table['key']} 物理表）",
        "versions": [version], "profile": profile, "variant": variant_id,
        "status": "candidate" if candidate else "canonical",
        "evidence": "inherited-or-unavailable-source-layout" if candidate else "source-reviewed",
        "fileName": table["file"], "address": address, "recordCount": count, "stride": stride,
        "beginId": begin, "primaryKey": "ID", "endianness": "little", "encoding": "GBK for strings",
        "indexFormula": formula, "endOffsetExclusive": f"0x{end:X}",
        "recordCodec": table.get("recordCodecKey", "fixed-record-v1"),
        "capability": "Unavailable" if excluded else capability,
        "verificationLevel": verification, "sampleBoundaries": bounds,
        "fields": expand_fields(table), "writeGates": gates,
        "notes": ["物理文件布局和运行时内存记录是不同实体。",
                  "canonical 仅表示本条来源/几何可复现，不会绕过运行时门禁，未知数值语义不得扩大为引擎已验证语义。"],
        "sourceRefs": [source_id("profile65")] + ([source_id("profile66")] if version == "6.6" else []) +
                      [source_id("registry"), source_id("codecs"), source_id("values"), source_id("test-profile-write")],
    }
    if table["key"] in {"items-high", "item-description-high"}:
        entry["title"] = entry["title"].replace("104-255", "104-254")
    if table["key"] in {"items-low", "items-high", "items-extended"}:
        entry["relations"] = ["format.item.split-data-star", "format.data-manager.item-codecs",
                              f"struct.{version.replace('.', '')}.item-category-semantics",
                              "mechanism.shared.consumable-effect-namespace"]
        meanings = {
            "初始能力": "物理 CSV 列名保留；普通装备为初始属性，辅助装备为特殊效果值，消耗品为效果参数低字节。",
            "装备特效值": "物理 CSV 列名保留；普通装备为特殊效果值，辅助装备为空/保留，消耗品为效果参数高字节。",
            "能力成长": "物理 CSV 列名保留；普通装备为能力成长，辅助装备为适用兵种系 ID（255=所有兵种），消耗品为空/保留。",
            "价格（/100）": "价格单位100；255表示不可买卖；不得将辅助 +0x17 的适用兵种当作价格。",
            "宝物图鉴": "图鉴标记；业务页为勾选框，主动修改写入0/1，未修改的原始值保留。",
        }
        for field in entry["fields"]:
            if field["name"] in meanings:
                field["meaning"] += "；" + meanings[field["name"]]
            if field["name"] in {"宝物类型", "装备特效号"}:
                field["meaning"] += "；此为逻辑字段，6.6 15 字节 Codec 仅当原始 +0x11>=26 且 +0x12 为2或3时交换实际写入位置；普通类型0..25优先按武器/防具解释，见专用 Codec 契约"
                field["meaning"] += "；消耗品实际特效使用独立0x1A..0x3D目录，不能把物理referenceTable或类别2/3当作装备特效名称。"
        entry["sourceRefs"] += [source_id("studio-item-layout"), source_id("studio-icon-mapping")]
        icon_offset = next(field["offset"] for field in table["fields"] if field.get("name") == "图标")
        for field in entry["fields"]:
            if field["name"] == "图标":
                field["meaning"] += f"；本 Variant 使用 +0x{icon_offset:02X} UInt8 图标号，允许字段级编辑；E5/Item.e5 中逻辑图标 N 对应小图 #2N+1、大图 #2N+2，N 从 0 开始"
        entry["notes"].append("15 字节名称布局中的 +0x10、+0x14 是保留字节；17 字节名称布局图标在 +0x14。跨布局迁移只映射图标逻辑字段，不能复制源偏移。")
    if table["key"] == "job-series-attributes":
        entry["rowSemantics"] = [
            {"rowId": row, "name": name,
             "evidence": "user-confirmed-semantics" if values is not None else "source-reviewed-row-label",
             **({"values": [{"id": index, "name": value} for index, value in enumerate(values)]}
                if values is not None else {})}
            for row, name, values in JOB_ATTRIBUTE_ROWS
        ]
        entry["sourceRefs"] += [source_id("attribute-reader"), source_id("user-attribute-enums")]
        entry["notes"].append("行号和 UInt8 几何来自读取器与 Profile；移动声音、移动速度、攻击声音、兵种类型的枚举名称由用户确认，未冒充逆向或引擎运行时验证。未列出的数值保留数字并允许按字段边界编辑。")
    if dynamic66:
        entry["configuredCapability"] = capability
        entry["capability"] = "RuntimeProbeRequired"
        entry["sourceRefs"] += [source_id("augmentation"), source_id("embedded-probe"), source_id("layout-evidence")]
    return entry


def special_quote_entry(version: str, variant: dict) -> dict:
    profile = PROFILE_IDS[variant["id"]]
    return {
        "id": f"struct.{version.replace('.', '')}.disk.{variant['id']}.person-critical-special-map",
        "title": f"{variant['id']} 特殊暴击人物分配（动态物理表）",
        "versions": [version], "profile": profile, "variant": variant["id"],
        "status": "candidate" if variant["id"] == "66-shanzhai-legacy" else "canonical",
        "evidence": "source-reviewed-pe-reference-gated", "fileName": "Ekd5.exe",
        "address": {"kind": "fileOffset", "value": "0x89C30", "profile": profile, "evidence": "pe-reference-gated"},
        "recordCount": 21, "stride": 4, "beginId": 0, "primaryKey": "ID",
        "indexFormula": "Ekd5.exe + 0x89C30 + specialSlot * 4; specialSlot=0..20; Imsg.e5 quoteOffset=140000 + specialSlot*200",
        "endOffsetExclusive": "0x89C84", "recordCodec": "fixed-record-v1", "capability": "RuntimeProbeRequired",
        "endianness": "little", "encoding": "not applicable",
        "fields": [{"name": "人物ID", "offset": "0x0", "width": 4, "type": "uint32le",
                    "meaning": "绑定人物 ID 0..1023，1024 为空槽；数值不是 Imsg 行号，记录主键 ID/槽号才对应特殊台词行。", "maximum": 1024}],
        "writeGates": ["需验证目标 PE 可执行区对该区域的引用、21 个 UInt32 值和文件边界；不能只检查原始固定偏移。",
                       "普通模式清空此人物所有特殊槽到 1024，再写普通类型 0..25 和三句共享台词。",
                       "特殊模式保持普通类型作为回退；绑定所选槽并清除本人物其它特殊槽；被其它人物占用时先预览并显式覆盖。",
                       "模式、绑定、人物字段和 Imsg 文本一次跨表事务提交；任何校验失败不产生部分草稿。"],
        "sourceRefs": [source_id("augmentation"), source_id("quotes"), source_id("test-quotes")],
    }


def table_entry64(table: dict, variant: dict, fingerprint: dict, reviewed_keys: set[str]) -> dict:
    table = copy.deepcopy(table)
    if table["key"] == "effect-names":
        table["capabilityEvidence"] = "洗隋两处唯一名称消费者和目标PE映射确认180×16只读槽；失败回退数字ID，不套用6.5的255槽。"
    entry = table_entry(table, "6.4", variant, fingerprint)
    key = table["key"]
    independent = key in {"persons", "detailed-job-growth", "effect-names", "person-retreat-quotes",
                          "person-r-assign", "person-s-assign", "strategy-terrain-availability"}
    entry["layoutOrigin"] = "ccz-6.4 override" if key in reviewed_keys else "ccz-6.5 inherited geometry only"
    entry["sourceRefs"] = list(dict.fromkeys(entry["sourceRefs"] + [source_id("profile64"),
        source_id("configuration64"), source_id("consumers64"), source_id("test64-compatibility")]))
    entry["configuredCapability"] = table.get("capability", "Editable")
    entry["relations"] = [value for value in entry.get("relations", [])
                          if value not in {"struct.64.item-category-semantics", "mechanism.shared.consumable-effect-namespace"}]
    entry["notes"].append("本实体是磁盘 Profile 几何；6.4 父清单继承不构成独立消费者或玩法验证。洗隋完整消费者和逐表能力是不同维度。")
    if not independent:
        entry["status"] = "candidate"
        entry["evidence"] = "inherited-source-layout"
        entry["writeGates"].insert(0, "不得仅按父清单自动写入；须核对6.4目标文件、逐表消费者/Codec、样本边界与本条字段策略。")
    else:
        entry["status"] = "canonical"
        entry["evidence"] = "source-reviewed-consumer-chain"
        if isinstance(entry.get("address"), dict):
            entry["address"]["evidence"] = "source-reviewed-consumer-chain"
    if key in {"person-r-assign", "person-s-assign", "strategy-terrain-availability", "person-retreat-quotes"}:
        entry["capability"] = "RuntimeProbeRequired"
        entry["sourceRefs"].append(source_id("augmentation"))
        entry["writeGates"].insert(0, "完整PE消费者、合法节映射和唯一性通过后才开放；探测失败关闭本表，不从6.5猜测地址。")
    if key == "person-retreat-quotes":
        entry["notes"] += ["消息索引为650+原生人物ID，人物ID只允许0..48；不是人物记录+15所指的独立行。",
                           "200字节为读取记录宽度；缓冲区在[200]补NUL。字符串实际编辑容量仍遵循严格GBK及当前文本消费者策略。"]
    if key == "effect-names":
        entry["capability"] = "ReadOnly"
        entry["notes"].append("180×16共享名称槽位于文件0xD0D60；与180×8活动特效表0xDA198不是同一结构。槽内严格GBK/NUL；探测失败回退数字ID。")
        entry["writeGates"].insert(0, "两处唯一名称消费者与PE映射通过才读取180槽；名称表只读，不升级为Editable。")
        for field in entry["fields"]:
            field["writePolicy"] = "ReadOnly"
    if key in {"item-acquisition-low", "item-acquisition-high"}:
        entry["writeGates"] = [value for value in entry["writeGates"] if not value.startswith("旧 HexTable.xml")]
        entry["writeGates"].append("旧定义Enable=false且未获洗隋独立读取证据；保持Unavailable，不读取猜测区。")
    if key in {"persons", "detailed-job-growth"}:
        cutoff = 27 if key == "persons" else 9
        chain = "PersonDefaults" if key == "persons" else "EquipmentPermissions"
        entry["fieldCapabilityGates"] = {"consumer": "Ccz64ConfigurationProbe." + chain,
            "offsetFrom": f"0x{cutoff:X}", "onVerified": "Editable", "onFailure": "Preserve"}
        entry["writeGates"].insert(0, "完整消费者不匹配时只保留受保护尾字段；普通人物/成长数值继续按原策略可用。")
        for field in entry["fields"]:
            if int(field["offset"], 16) >= cutoff:
                field["writePolicy"] = "Editable"
                field["writePrecondition"] = "Ccz64ConfigurationProbe." + chain
                field["onFailurePolicy"] = "Preserve"
                field["meaning"] += "；完整" + chain + "消费链通过才可编辑，失败按Preserve原字节保留"
        if key == "persons":
            entry["notes"] += ["级别+27的原值0在引擎加载时转为1；经验+28与默认装备+29..31均被消费者读取。",
                               "默认装备按原生类型0..19武器、20..25防具、其余类别标记分类；255仅此装备ID字段表示未装备。"]
        else:
            entry["notes"].append("许可读取row+9+物品类型，0..25共26类；UInt8非零即允许，不能强制将历史非零值归一为1。")
    return entry


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--versions", nargs="+", choices=("6.4", "6.5", "6.6"), default=["6.5", "6.6"],
                        help="Default retains the existing 6.5/6.6 import; select --versions 6.4 for Xisui only.")
    parser.add_argument("--refresh-existing", action="store_true",
                        help="Explicitly replace generated IDs; otherwise reviewed existing entities are retained.")
    parser.add_argument("--source-manifest", type=Path,
                        help="Optional separate source collection for review before merging into the manifest.")
    args = parser.parse_args()
    global ACTIVE_SOURCE_PREFIX
    ACTIVE_SOURCE_PREFIX = "src.data-manager64." if set(args.versions) == {"6.4"} else "src.data-manager."
    workspace = args.workspace.resolve()
    base = read_json(workspace / SOURCES["profile65"])
    child = read_json(workspace / SOURCES["profile66"]) if "6.6" in args.versions else None
    register_sources(workspace, args.source_manifest, only64=set(args.versions) == {"6.4"})
    if child:
        create_profiles(child, args.refresh_existing)
    fingerprint65 = base["variants"][0]["fingerprints"][0]
    configurations = {"6.5": base, "6.6": child}
    if "6.4" in args.versions:
        configurations["6.4"] = read_json(workspace / SOURCES["profile64"])
    for version in args.versions:
        config = configurations[version]
        entries = []
        for variant in config["variants"]:
            tables = resolve(base, config if version in {"6.4", "6.6"} else None, variant)
            if version == "6.4":
                reviewed = {table["key"] for table in config.get("tables", [])}
                entries.extend(table_entry64(table, variant, variant["fingerprints"][0], reviewed) for table in tables)
                special = special_quote_entry(version, variant)
                special["sourceRefs"] += [source_id("configuration64"), source_id("consumers64"), source_id("test64-configuration")]
                special["notes"] = ["洗隋完整特殊暴击消费者验证21项上限、VA0x48B230到文件0x89C30映射及200字节消息读取；失败禁用。"]
                entries.append(special)
            else:
                entries.extend(table_entry(table, version, variant, fingerprint65) for table in tables)
                entries.append(special_quote_entry(version, variant))
        merge_collection(f"{version}/data/structures/data-manager-physical-tables.json", "data-structure", entries,
                         refresh=args.refresh_existing)
        print(f"{version}: tables={len(entries)} fields={sum(len(item['fields']) for item in entries)}")


if __name__ == "__main__":
    main()
