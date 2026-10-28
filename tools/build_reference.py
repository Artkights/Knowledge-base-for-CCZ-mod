from __future__ import annotations

import argparse
import json
import sys
sys.dont_write_bytecode = True
from pathlib import Path


from generated_artifacts import differences, update
from version_config import DATA_VERSIONS, REFERENCE_FILES, ROOT

DATA_ROOTS = [ROOT / version / "data" for version in DATA_VERSIONS]
ORDER = [
    "engine-profile", "function", "global", "data-structure", "file-format",
    "effect-stub", "patch-recipe", "mechanism", "script-command", "workflow",
    "test-contract", "case-study",
]
FILENAMES = REFERENCE_FILES

TITLES = {
    "engine-profile": "引擎画像", "function": "函数与入口", "global": "全局地址",
    "data-structure": "数据结构", "file-format": "文件格式",
    "patch-recipe": "Hook、补丁与定位器", "mechanism": "机制与调用链",
    "effect-stub": "特效桩函数", "script-command": "剧本指令",
    "workflow": "自动化制作工作流", "test-contract": "自动化测试契约",
    "case-study": "制作案例",
}


def load_collections(version_dir: Path) -> dict[str, list[tuple[Path, dict]]]:
    groups: dict[str, list[tuple[Path, dict]]] = {}
    data_dir = version_dir / "data"
    if not data_dir.exists():
        return groups
    for path in sorted(data_dir.rglob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        groups.setdefault(document["entityType"], []).extend((path, entry) for entry in document["entries"])
    return groups


def fmt_address(value: object) -> str:
    if not isinstance(value, dict):
        return "-"
    return f"`{value.get('value', '?')}` ({value.get('kind', '?')})"


def md_cell(value: object) -> str:
    return str(value if value is not None else "-").replace("|", "\\|").replace("\n", " ")


def fmt_abi(item: dict) -> str:
    parts = [str(item.get("callingConvention", "unknown"))]
    abi = item.get("abi", {})
    if abi.get("registers"):
        parts.append(", ".join(f"{key}={value}" for key, value in abi["registers"].items()))
    if abi.get("stackArguments"):
        parts.append("stack: " + ", ".join(str(value) for value in abi["stackArguments"]))
    if "calleeCleanup" in abi:
        parts.append(f"callee cleanup {abi['calleeCleanup']} bytes")
    if len(parts) == 1 and item.get("inputs"):
        parts.append(str(item["inputs"]))
    return "; ".join(parts)


def render_profiles(entries: list[tuple[Path, dict]]) -> list[str]:
    lines = ["| ID | 版本 | 样本 SHA256 | 状态 | 证据 |", "|---|---|---|---|---|"]
    for _, item in entries:
        sample = item.get("sample") or {}
        lines.append(f"| `{item['id']}` | {md_cell(', '.join(item.get('versions', [])))} | `{sample.get('sha256', '-')}` | `{item['status']}` | `{item['evidence']}` |")
    return lines


def render_functions(entries: list[tuple[Path, dict]]) -> list[str]:
    lines = ["| 函数 | 地址 | 调用约定/输入 | 返回 | 含义 | 状态/证据 |", "|---|---|---|---|---|---|"]
    for _, item in entries:
        lines.append(f"| `{item['id']}` {md_cell(item['title'])} | {fmt_address(item.get('address'))} | {md_cell(fmt_abi(item))} | {md_cell(item.get('returns'))} | {md_cell(item.get('semantics'))} | `{item['status']}` / `{item['evidence']}` |")
    call_sites = [(item, site) for _, item in entries for site in item.get("callSites", [])]
    if call_sites:
        lines.extend(["", "## 已确认调用点", ""])
        for item, site in call_sites:
            lines.append(
                f"- `{item['id']}`：{fmt_address(site.get('address'))}；"
                f"指令 `{site.get('instruction', '-')}`；{site.get('meaning', '-')}"
            )
    notes = [(item, note) for _, item in entries for note in item.get("notes", [])]
    if notes:
        lines.extend(["", "## ABI与使用边界", ""])
        lines.extend(f"- `{item['id']}`（画像 `{item.get('profile', '-')}`）：{note}" for item, note in notes)
    return lines


def render_globals(entries: list[tuple[Path, dict]]) -> list[str]:
    lines = ["| 全局量 | 地址 | 宽度 | 含义 | 状态/证据 |", "|---|---|---|---|---|"]
    for _, item in entries:
        if "addresses" in item:
            lines.append(f"| `{item['id']}` {md_cell(item['title'])} | 多地址历史画像 | - | {md_cell(item.get('warning'))} | `{item['status']}` / `{item['evidence']}` |")
        else:
            lines.append(f"| `{item['id']}` {md_cell(item['title'])} | {fmt_address(item.get('address'))} | {md_cell(item.get('width'))} | {md_cell(item.get('semantics'))} | `{item['status']}` / `{item['evidence']}` |")
    return lines


def render_structures(entries: list[tuple[Path, dict]]) -> list[str]:
    lines: list[str] = []
    for _, item in entries:
        lines.extend([f"## {item['title']}", "", f"ID: `{item['id']}`；状态: `{item['status']}`；证据: `{item['evidence']}`", "", f"步长: `0x{item['stride']:X}` ({item['stride']})", "", f"索引公式: `{item.get('indexFormula', '-')}`", ""])
        if item.get("profile"):
            lines.extend([f"画像：`{item['profile']}`；记录数：`{item.get('recordCount', item.get('rowCount', '-'))}`。", ""])
        if item.get("activeAddress") or item.get("fileAddress"):
            lines.extend([f"指针槽：{fmt_address(item.get('address'))}；活动地址：{fmt_address(item.get('activeAddress'))}；文件偏移：{fmt_address(item.get('fileAddress'))}。", ""])
        if item.get("fileName"):
            lines.extend([f"存储：`{item['fileName']}`；起点：{fmt_address(item.get('address'))}；记录数：`{item.get('recordCount', '-')}`；ID 起点：`{item.get('beginId', '-')}`；结束偏移（不含）：`{item.get('endOffsetExclusive', '-')}`。", ""])
        if item.get("capability"):
            lines.extend([f"能力：`{item['capability']}`；Codec：`{item.get('recordCodec', '-')}`；字节序：`{item.get('endianness', '-')}`；编码：`{item.get('encoding', '-')}`。", ""])
        for note in item.get("notes", []):
            lines.append(f"- {note}")
        if item.get("notes"):
            lines.append("")
        if item.get("writeGates"):
            lines.extend(["写入门禁：", ""])
            lines.extend(f"- {value}" for value in item["writeGates"])
            lines.append("")
        if item.get("rowSemantics"):
            lines.extend(["| 属性行 ID | 名称 | 值语义 | 语义来源 |", "|---:|---|---|---|"])
            for row in item["rowSemantics"]:
                values = "；".join(f"{value['id']}：{value['name']}" for value in row.get("values", [])) or "未在此确认"
                lines.append(f"| {row['rowId']} | {md_cell(row['name'])} | {md_cell(values)} | `{row['evidence']}` |")
            lines.append("")
        if item.get("sampleBoundaries"):
            lines.extend(["| 样本 | 文件字节数 | 区域在边界内 | 文件 SHA256 |", "|---|---:|---|---|"])
            for sample in item["sampleBoundaries"]:
                lines.append(f"| {md_cell(sample.get('sampleId'))} | {md_cell(sample.get('fileLength'))} | {md_cell(sample.get('fits'))} | `{sample.get('sha256') or '-'}` |")
            lines.append("")
        fields = item.get("fields", [])
        if not fields:
            lines.extend(["字段尚未解析，见研究队列。", ""])
            continue
        lines.extend(["| 字段 | 偏移 | 宽度 | 类型 | 含义 |", "|---|---:|---:|---|---|"])
        for value in fields:
            lines.append(f"| `{value['name']}` | `{value['offset']}` | {value['width']} | `{value['type']}` | {md_cell(value['meaning'])} |")
        lines.append("")
    return lines


def render_formats(entries: list[tuple[Path, dict]]) -> list[str]:
    lines: list[str] = []
    for _, item in entries:
        lines.extend([f"## {item['title']}", "", f"ID: `{item['id']}`；状态: `{item['status']}`；证据: `{item['evidence']}`", "", f"字节序: `{item.get('endianness', '-')}`", ""])
        if item.get("indexFormula"):
            lines.extend([f"索引公式: `{item['indexFormula']}`", ""])
        if item.get("entrySize") is not None:
            lines.extend([f"每条解压大小: `{item['entrySize']}` 字节。", ""])
        if item.get("frameWidth") is not None:
            lines.extend([f"帧几何: `{item['frameWidth']}×{item.get('frameHeight', '?')}`；帧数: `{item.get('frameCount', '?')}`；条带: `{item.get('stripWidth', '?')}×{item.get('stripHeight', '?')}`。", ""])
        files = item.get("files", [])
        for value in files:
            if isinstance(value, str):
                lines.append(f"- 文件：`{value}`")
            elif isinstance(value, dict):
                name = value.get("name", value.get("file", "?"))
                details = []
                if value.get("width") is not None:
                    details.append(f"{value['width']}×{value.get('height', '?')}")
                if value.get("frameCount") is not None:
                    details.append(f"{value['frameCount']}帧，每帧{value.get('frameWidth', '?')}×{value.get('frameHeight', '?')}")
                if value.get("recordCount") is not None:
                    details.append(f"{value['recordCount']}条")
                if value.get("recordSize") is not None:
                    details.append(f"记录{value['recordSize']}字节")
                lines.append(f"- 文件：`{name}`" + ("；" + "；".join(details) if details else ""))
        if files:
            lines.append("")
        for label, fields in (("目录项字段", item.get("entryFields", [])),
                              ("头记录字段", item.get("headerFields", [])),
                              ("播放记录字段", item.get("recordFields", []))):
            if not fields:
                continue
            lines.extend([f"{label}：", ""])
            lines.extend(["| 字段 | 偏移 | 宽度 | 类型 | 含义 |", "|---|---:|---:|---|---|"])
            for value in fields:
                lines.append(f"| `{value['name']}` | `{value['offset']}` | {value['width']} | `{value['type']}` | {md_cell(value['meaning'])} |")
            lines.append("")
        for consumer in item.get("consumers", []):
            lines.extend([f"消费者画像：`{consumer.get('profile', '?')}`；定位：{fmt_address(consumer.get('address'))}；文件位置：{fmt_address(consumer.get('fileAddress'))}；样本SHA256：`{consumer.get('sampleSha256', '-')}`。", ""])
            for anchor in consumer.get("anchors", []):
                lines.append(f"- `{anchor.get('meaning', '-')}`：文件 `{anchor.get('fileOffset', '-')}` / VA `{anchor.get('va', '-')}`；原字节 `{anchor.get('expectedBytes', '-')}`。")
            lines.append("")
        for fact in item.get("semantics", []):
            lines.append(f"- {fact}")
        if item.get("writePolicy"):
            lines.extend(["", "写入策略：" + str(item["writePolicy"])])
        lines.append("")
    return lines


def render_patches(entries: list[tuple[Path, dict]]) -> list[str]:
    lines: list[str] = []
    for _, item in entries:
        lines.extend([f"## {item['title']}", "", f"ID: `{item['id']}`；类型: `{item['kind']}`；画像: `{item['profile']}`；状态: `{item['status']}`；证据: `{item['evidence']}`", ""])
        if item.get("status") == "candidate":
            lines.extend(["> 历史候选：用于查询、逆向和迁移设计。若站点缺少 `expectedBytes` 或完整指令边界，不得自动写入。", ""])
        if item.get("signature"):
            lines.extend([
                f"签名: `{item['signature']}`",
                "",
                f"扫描范围: {item.get('scanScope', '-')}",
                "",
                f"命中规则: {item.get('matchPolicy', '-')}",
                "",
            ])
        sites = item.get("sites", [])
        if sites:
            lines.extend(["| 地址 | 原字节 | 目标字节 | 写入方式 | 长度 | 完整指令边界 |", "|---|---|---|---|---:|---|"])
            for site in sites:
                replacement = site.get("replacementBytes")
                if not replacement and site.get("replacementVariants"):
                    replacement = "; ".join(
                        f"{value['bytes']} ({value['meaning']})" for value in site["replacementVariants"]
                    )
                lines.append(
                    f"| {fmt_address(site.get('address'))} | `{site.get('expectedBytes', '-')}` | "
                    f"`{replacement or '-'}` | {md_cell(site.get('writeMode'))} | "
                    f"{md_cell(site.get('overwriteLength'))} | {md_cell(site.get('instructionBoundary'))} |"
                )
                if site.get("executionEffect"):
                    lines.append(f"\n执行流：{site['executionEffect']}\n")
            lines.append("")
        if item.get("abi"):
            lines.extend([f"ABI: {item['abi']}", ""])
        stub = item.get("stub")
        if stub:
            lines.extend([
                f"桩入口: `{stub.get('entry', '-')}`",
                "",
                f"返回: `{stub.get('return', '-')}`",
                "",
                "重定位: " + ("；".join(f"`{value}`" for value in stub.get("relocations", [])) or "无"),
                "",
            ])
        for step in item.get("extraction", []):
            lines.append(f"- 提取：`{step}`")
        if item.get("extraction"):
            lines.append("")
    return lines


def render_mechanisms(entries: list[tuple[Path, dict]]) -> list[str]:
    lines: list[str] = []
    for _, item in entries:
        lines.extend([f"## {item['title']}", "", f"ID: `{item['id']}`；状态: `{item['status']}`；证据: `{item['evidence']}`", ""])
        if item.get("summary"):
            lines.extend([str(item["summary"]), ""])
        for step in item.get("steps", []):
            lines.append(f"{step['order']}. `{step['entity']}`：{step['role']}")
        if item.get("pierceBranch"):
            lines.extend(["", "穿透分支：" + " -> ".join(f"`{value}`" for value in item["pierceBranch"])])
        if item.get("safeReturnAddresses"):
            lines.extend(["", "S 等待白名单返回地址：", "", ", ".join(f"`{value}`" for value in item["safeReturnAddresses"]), "", item.get("callerSemantics", "")])
        if item.get("algorithm"):
            lines.extend(["", "计算规则：", ""])
            for value in item["algorithm"]:
                lines.append(f"- `{value}`")
        for composition in item.get("composition", []):
            lines.extend(["", "### " + str(composition.get("effect", "组合关系")), ""])
            for key in ("steps", "rules", "abi"):
                lines.extend(f"- {value}" for value in composition.get(key, []))
            if composition.get("result"):
                lines.extend(["", str(composition["result"])])
            if composition.get("consumerEvidence"):
                lines.extend(["", "消费者证据：", "", "```json", json.dumps(composition["consumerEvidence"], ensure_ascii=False, indent=2), "```"])
        for title, key in (("边界", "boundaries"), ("补充说明", "notes"), ("写入策略", "writePolicy"), ("界面规则", "uiPolicy")):
            value = item.get(key)
            if not value:
                continue
            lines.extend(["", title + "：", ""])
            if isinstance(value, list):
                lines.extend(f"- {child}" for child in value)
            elif isinstance(value, dict):
                lines.extend(f"- `{name}`：{child if isinstance(child, str) else json.dumps(child, ensure_ascii=False)}" for name, child in value.items())
            else:
                lines.append(str(value))
        lines.append("")
    return lines


def render_effect_stubs(entries: list[tuple[Path, dict]]) -> list[str]:
    lines = [
        "> 候选桩地址不是空闲代码洞。复用前必须核对目标样本原字节、调用约定、覆盖范围和占用冲突。",
        "",
        "| 桩函数 | 地址 | 风格 | 效果值/叠加 | 特效 ID（装备/个人） | 调度器/核心 | 状态/证据 |",
        "|---|---|---|---|---|---|---|",
    ]
    for _, item in entries:
        contract = item.get("contract", {})
        ids = f"{contract.get('equipmentEffectId', '-')} / {contract.get('personalEffectId', '-')}"
        dispatch = f"`{contract.get('dispatcher', '-')}` / `{contract.get('coreFunction', '-')}`"
        mode = f"{contract.get('effectValueMode', '-')} / {contract.get('stacking', '-')}"
        lines.append(
            f"| `{item['id']}` {md_cell(item['title'])} | {fmt_address(item.get('address'))} | "
            f"`{item.get('stubStyle', '-')}` | {md_cell(mode)} | {md_cell(ids)} | {dispatch} | "
            f"`{item['status']}` / `{item['evidence']}` |"
        )
    lines.extend(["", "标准/内联桩参数压栈顺序：`effectValueFlag -> stackingFlag -> equipmentEffectId -> personalEffectId`。"])
    return lines


def render_script_commands(entries: list[tuple[Path, dict]]) -> list[str]:
    lines = [
        "> `candidate` 指令可用于解析器设计和样本比对；参数语义未复核前不得驱动自动改写。",
        "",
        "| ID | Opcode/子命令 | 名称 | 分类 | 参数槽 | 状态/证据 |",
        "|---|---|---|---|---|---|",
    ]
    for _, item in entries:
        opcode = item.get("opcode", "-")
        if item.get("subcommand") is not None:
            opcode += f" / {item['subcommand']}"
        parameters = "; ".join(
            f"{value.get('slot', '?')}:{value.get('name', '?')}[{value.get('type', '?')}]"
            for value in item.get("parameters", [])
        ) or "-"
        lines.append(
            f"| `{item['id']}` | `{opcode}` | {md_cell(item['title'])} | `{item.get('category', '-')}` | "
            f"{md_cell(parameters)} | `{item['status']}` / `{item['evidence']}` |"
        )
    return lines


def render_workflows(entries: list[tuple[Path, dict]]) -> list[str]:
    lines: list[str] = []
    for _, item in entries:
        lines.extend([
            f"## {item['title']}", "",
            f"ID: `{item['id']}`；状态: `{item['status']}`；证据: `{item['evidence']}`", "",
            f"目标：{item.get('goal', '-')}", "", "输入：", "",
        ])
        lines.extend(f"- {value}" for value in item.get("inputs", []))
        lines.extend(["", "步骤：", ""])
        lines.extend(f"{step['order']}. {step['action']}" for step in item.get("steps", []))
        for title, key in (("门禁", "gates"), ("产物", "outputs"), ("回滚", "rollback")):
            lines.extend(["", f"{title}：", ""])
            lines.extend(f"- {value}" for value in item.get(key, []))
        lines.append("")
    return lines


def render_test_contracts(entries: list[tuple[Path, dict]]) -> list[str]:
    lines: list[str] = []
    for _, item in entries:
        lines.extend([
            f"## {item['title']}", "",
            f"ID: `{item['id']}`；状态: `{item['status']}`；证据: `{item['evidence']}`", "",
            f"命令: `{item.get('command', '-')}`", "",
            f"目标: {item.get('target', '-')}；变更范围: {item.get('mutationScope', '-')}", "",
            "断言：", "",
        ])
        lines.extend(f"- {value}" for value in item.get("assertions", []))
        lines.extend(["", "必需产物：", ""])
        lines.extend(f"- {value}" for value in item.get("requiredArtifacts", []))
        lines.extend(["", f"失败含义：{item.get('failureMeaning', '-')}" , ""])
    return lines


def render_case_studies(entries: list[tuple[Path, dict]]) -> list[str]:
    lines: list[str] = []
    for _, item in entries:
        lines.extend([
            f"## {item['title']}", "",
            f"ID: `{item['id']}`；状态: `{item['status']}`；证据: `{item['evidence']}`", "",
            f"目标：{item.get('objective', '-')}", "", "输入：", "",
        ])
        lines.extend(f"- {value}" for value in item.get("inputs", []))
        for title, key in (("过程", "procedure"), ("结果", "outcome"), ("可复用结论", "reusableLessons")):
            lines.extend(["", f"{title}：", ""])
            lines.extend(f"- {value}" for value in item.get(key, []))
        lines.append("")
    return lines


RENDERERS = {
    "engine-profile": render_profiles, "function": render_functions, "global": render_globals,
    "data-structure": render_structures, "file-format": render_formats,
    "patch-recipe": render_patches, "mechanism": render_mechanisms,
    "effect-stub": render_effect_stubs, "script-command": render_script_commands,
    "workflow": render_workflows, "test-contract": render_test_contracts,
    "case-study": render_case_studies,
}


def render_group(version_dir: Path, entity_type: str, entries: list[tuple[Path, dict]]) -> str:
    sources = sorted({path.relative_to(ROOT).as_posix() for path, _ in entries})
    lines = [f"# {version_dir.name} {TITLES[entity_type]}", "", "<!-- GENERATED: tools/build_reference.py; DO NOT EDIT -->", "", "结构化事实来源：" + "、".join(f"`{path}`" for path in sources), ""]
    lines.extend(RENDERERS[entity_type](entries))
    return "\n".join(lines).rstrip() + "\n"


def generated_documents() -> tuple[dict[Path, str], set[Path]]:
    expected: dict[Path, str] = {}
    stale: set[Path] = set()
    for data_root in DATA_ROOTS:
        version_dir = data_root.parent
        reference = version_dir / "reference"
        groups = load_collections(version_dir)
        for entity_type in ORDER:
            entries = groups.get(entity_type)
            if entries:
                expected[reference / FILENAMES[entity_type]] = render_group(version_dir, entity_type, entries)
        stale.update(path for path in reference.glob("*.md") if path not in expected)
    return expected, stale


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate human references from structured JSON.")
    parser.add_argument("--check", action="store_true", help="Report stale output without editing files")
    args = parser.parse_args()
    expected, stale = generated_documents()
    changed = differences(expected, stale)
    if args.check:
        for path in changed:
            print("stale: " + path.relative_to(ROOT).as_posix())
        return int(bool(changed))
    update(expected, stale)
    print(f"references={len(expected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
