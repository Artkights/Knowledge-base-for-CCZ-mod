from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMMIT = "9b8abf5"
PROFILE_65 = "profile.ccz65.unencrypted.f9a"
PROFILE_66_LEGACY = "profile.ccz66x.legacy-patch-family"

SCRIPT_PATHS = [
    "6.5/05-剧本与战场/01-00-13结构流程.md",
    "6.5/05-剧本与战场/02-14-24文本音画.md",
    "6.5/05-剧本与战场/03-25-35触发与R场景.md",
    "6.5/05-剧本与战场/04-36-4B变量部署.md",
    "6.5/05-剧本与战场/05-4C-5E战场操作.md",
    "6.5/05-剧本与战场/06-5F-6F单挑与扩展.md",
    "6.5/05-剧本与战场/07-70-7B高级变量与系统.md",
]
SCRIPT_72_PATH = "6.5/05-剧本与战场/08-72信息传送子功能.md"
STUB_PATH = "6.5/01-核心引擎/桩函数.md"
DISPATCH_PATH = "6.5/01-核心引擎/调度函数.md"
CORE_PATH = "6.5/01-核心引擎/核心引擎.md"
INJECTION_INDEX_PATH = "6.5/03-机制与特效/6.5特效注入索引.md"

WORKFLOW_PATHS = {
    "automation": "6.5/06-工具与验证/自动化MOD制作.md",
    "validation": "6.5/06-工具与验证/验证与烟测.md",
    "effect": "6.5/06-工具与验证/本地Agent生成可注入特效代码指南.md",
    "workbench": "6.5/06-工具与验证/特效工作台复盘与验收.md",
    "battle": "6.5/05-教程指南/战场操作自动化与调试流程.md",
    "scenario": "6.5/05-剧本与战场/R剧本模板克隆复用规范.md",
    "sprites": "6.5/04-数据表与资源/人物R-S像素形象制作链路.md",
    "liu-bei": "6.5/07-制作案例/刘备6.4-RS模板学习.md",
    "composite-effect": "6.5/03-机制与特效/模块化复合特效制作.md",
}


def git_bytes(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{COMMIT}:{path}"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def git_text(path: str) -> str:
    return git_bytes(path).decode("utf-8-sig")


def git_paths(prefix: str, suffix: str) -> list[str]:
    result = subprocess.run(
        ["git", "-c", "core.quotePath=false", "ls-tree", "-r", "--name-only", COMMIT],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        check=True,
    )
    paths = result.stdout.decode("utf-8").splitlines()
    return sorted(path for path in paths if path.startswith(prefix) and path.endswith(suffix))


def write_json(rel: str, payload: dict) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def source_id(path: str) -> str:
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:16]
    return f"src.history.{COMMIT}.{digest}"


def add_source(sources: dict[str, dict], path: str, used_for: str) -> str:
    sid = source_id(path)
    data = git_bytes(path)
    sources[sid] = {
        "id": sid,
        "path": f"history/{COMMIT}/{path}",
        "sha256": hashlib.sha256(data).hexdigest().upper(),
        "sourceType": "historical-knowledge-record",
        "usedFor": used_for,
        "published": False,
        "gitCommit": COMMIT,
        "gitPath": path,
    }
    return sid


def clean_cell(value: str) -> str:
    return re.sub(r"[*`]", "", value).strip()


def parse_table_row(line: str) -> list[str]:
    return [clean_cell(value) for value in line.strip().strip("|").split("|")]


def parse_parameter_table(section: str) -> list[dict]:
    parameters = []
    for line in section.splitlines():
        cells = parse_table_row(line) if line.lstrip().startswith("|") else []
        if len(cells) < 5 or not re.fullmatch(r"P\d+", cells[0]):
            continue
        parameters.append(
            {
                "slot": cells[0],
                "name": cells[1],
                "type": cells[2],
                "meaning": cells[3],
                "risk": cells[4],
                "confidence": "candidate",
            }
        )
    return parameters


def extract_notes(section: str) -> list[str]:
    notes = []
    for line in section.splitlines():
        value = line.strip()
        if not value or value.startswith(("#", "|", "<!--", "```", "- 本条目", "- 具体结论")):
            continue
        if value not in notes:
            notes.append(value)
    return notes[:8]


def parse_script_commands(sources: dict[str, dict], mappings: dict[str, list[str]]) -> tuple[list[dict], list[dict]]:
    commands: list[dict] = []
    extensions: list[dict] = []
    categories = {
        "01": "structure-flow", "02": "text-audio-visual", "03": "trigger-r-scene",
        "04": "variables-deployment", "05": "battle-operations", "06": "duel-extensions",
        "07": "advanced-system",
    }
    for path in SCRIPT_PATHS:
        sid = add_source(sources, path, "6.5 剧本操作码、参数槽和风险边界")
        text = git_text(path)
        matches = list(re.finditer(r"(?m)^### `0x([0-9A-Fa-f]{2})`\s+(.+)$", text))
        ids = []
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            section = text[match.end():end]
            opcode = match.group(1).upper()
            entry_id = f"script.65.opcode-{opcode.lower()}"
            ids.append(entry_id)
            commands.append(
                {
                    "id": entry_id,
                    "title": match.group(2).strip(),
                    "aliases": [f"0x{opcode}", f"剧本指令 {opcode}"],
                    "versions": ["6.5"],
                    "status": "candidate",
                    "evidence": "legacy-structured",
                    "opcode": f"0x{opcode}",
                    "category": categories[path.split("/")[-1][:2]],
                    "parameters": parse_parameter_table(section),
                    "notes": extract_notes(section),
                    "writePolicy": "参数未由编辑器源码或样本闭环前只用于识别、反编译和模板对照。",
                    "sourceRefs": [sid],
                }
            )
        mappings[path] = ids

    path = SCRIPT_72_PATH
    sid = add_source(sources, path, "0x72 信息传送子功能和 6.6 扩展参数候选")
    text = git_text(path)
    base_ids = []
    in_index = False
    for line in text.splitlines():
        if line.startswith("## 6.5/v0.23-v0.24 子功能索引"):
            in_index = True
            continue
        if in_index and line.startswith("## "):
            break
        if not in_index or not line.startswith("|"):
            continue
        cells = parse_table_row(line)
        if len(cells) != 5 or not cells[0].isdigit():
            continue
        sub = int(cells[0])
        entry_id = f"script.65.opcode-72-sub-{sub:02d}"
        base_ids.append(entry_id)
        commands.append(
            {
                "id": entry_id,
                "title": f"信息传送 {sub}: {cells[1]}",
                "aliases": [f"72-{sub}", cells[1]],
                "versions": ["6.5"],
                "status": "candidate",
                "evidence": "legacy-structured",
                "opcode": "0x72",
                "subcommand": sub,
                "category": "information-transfer",
                "parameters": [],
                "editorV023": cells[2],
                "editorV024": cells[3],
                "risk": cells[4],
                "writePolicy": "子功能参数未闭环前只读，不生成二进制写回。",
                "sourceRefs": [sid],
            }
        )

    ext_matches = list(re.finditer(r"(?m)^### `72-(\d+)\s+([^`]+)`\s*$", text))
    ext_ids = []
    for index, match in enumerate(ext_matches):
        end = ext_matches[index + 1].start() if index + 1 < len(ext_matches) else len(text)
        section = text[match.end():end]
        sub = int(match.group(1))
        entry_id = f"script.66.opcode-72-sub-{sub:02d}"
        ext_ids.append(entry_id)
        extensions.append(
            {
                "id": entry_id,
                "title": match.group(2).strip(),
                "aliases": [f"72-{sub}", f"6.6 信息传送 {sub}"],
                "versions": ["6.6"],
                "status": "candidate",
                "evidence": "legacy-structured",
                "opcode": "0x72",
                "subcommand": sub,
                "category": "information-transfer-extension",
                "parameters": parse_parameter_table(section),
                "notes": extract_notes(section),
                "writePolicy": "6.6/6.6x 只读参数候选，必须用目标作品脚本样本复核。",
                "sourceRefs": [sid],
            }
        )
    mappings[path] = base_ids + ext_ids
    return commands, extensions


def hex_number(value: str) -> int | None:
    match = re.search(r"[0-9A-Fa-f]+", value)
    return int(match.group(0), 16) if match else None


def address(value: str, profile: str, evidence: str = "legacy-structured", kind: str = "va") -> dict:
    return {"kind": kind, "value": f"0x{int(value, 16):08X}", "profile": profile, "evidence": evidence}


def parse_effect_stubs(sources: dict[str, dict], mappings: dict[str, list[str]]) -> tuple[list[dict], list[dict]]:
    sid = add_source(sources, STUB_PATH, "6.5 标准桩、内联桩和四参数特效判定契约")
    core_sid = add_source(sources, CORE_PATH, "6.5 双渠道特效判定语义")
    text = git_text(STUB_PATH)
    stubs: list[dict] = []
    ids: list[str] = []
    dispatchers = {"4210D0": "0x006002C6", "421106": "0x0060002A", "421175": "0x00600819"}

    standard = re.search(r"#### 已知桩函数表(.*?)(?:#### 内联桩函数)", text, re.S)
    if standard:
        for line in standard.group(1).splitlines():
            cells = parse_table_row(line) if line.startswith("|") else []
            if len(cells) != 6 or not re.fullmatch(r"[0-9A-Fa-f]{6,8}", cells[0]):
                continue
            raw = cells[0].upper()
            entry_id = f"stub.65.standard-{raw.lower()}"
            ids.append(entry_id)
            stubs.append(
                {
                    "id": entry_id,
                    "title": f"{cells[1]}标准特效桩",
                    "aliases": [cells[1], raw],
                    "versions": ["6.5"],
                    "profile": PROFILE_65,
                    "status": "candidate",
                    "evidence": "legacy-structured",
                    "address": address(raw, PROFILE_65),
                    "stubStyle": "standard-dispatch",
                    "contract": {
                        "registers": {"ECX": "单位上下文"},
                        "pushOrder": ["effectValueFlag", "stackingFlag", "equipmentEffectId", "personalEffectId"],
                        "effectValueMode": "value" if cells[2] == "是" else "boolean",
                        "stacking": cells[3] == "是",
                        "equipmentEffectId": hex_number(cells[4]),
                        "personalEffectId": hex_number(cells[5]),
                        "dispatcher": dispatchers.get(raw),
                        "coreFunction": "fn.65.core-effect-engine",
                    },
                    "writePolicy": "候选桩契约；写入前复核目标样本原字节、调度目标和调用约定。",
                    "relations": ["fn.65.core-effect-engine"],
                    "sourceRefs": [sid, core_sid],
                }
            )

    inline = re.search(r"##### 已知内联桩实例(.*?)(?:##### 特殊判定样本)", text, re.S)
    if inline:
        for line in inline.group(1).splitlines():
            cells = parse_table_row(line) if line.startswith("|") else []
            if len(cells) != 6 or not re.fullmatch(r"[0-9A-Fa-f]{6,8}", cells[0]):
                continue
            raw = cells[0].upper()
            entry_id = f"stub.65.inline-{raw.lower()}"
            ids.append(entry_id)
            stubs.append(
                {
                    "id": entry_id,
                    "title": f"{cells[1].lstrip('★ ').strip()}内联特效桩",
                    "aliases": [cells[1], raw],
                    "versions": ["6.5"],
                    "profile": PROFILE_65,
                    "status": "candidate",
                    "evidence": "legacy-structured",
                    "address": address(raw, PROFILE_65),
                    "stubStyle": "inline-core-call",
                    "contract": {
                        "registers": {"ECX": "单位指针"},
                        "pushOrder": ["effectValueFlag", "stackingFlag", "equipmentEffectId", "personalEffectId"],
                        "effectValueMode": "value" if cells[2] == "是" else "boolean",
                        "stacking": cells[3] == "是",
                        "equipmentEffectId": hex_number(cells[4]),
                        "personalEffectId": hex_number(cells[5]),
                        "coreFunction": "fn.65.core-effect-engine",
                    },
                    "writePolicy": "地址表示历史补丁中的桩位置，不等于未修改基底的可写代码洞。",
                    "relations": ["fn.65.core-effect-engine"],
                    "sourceRefs": [sid, core_sid],
                }
            )

    special = re.search(r"##### 特殊判定样本(.*?)(?:#### 相关文档)", text, re.S)
    if special:
        for line in special.group(1).splitlines():
            cells = parse_table_row(line) if line.startswith("|") else []
            if len(cells) != 5 or not re.fullmatch(r"[0-9A-Fa-f]{6,8}", cells[0]):
                continue
            raw = cells[0].upper()
            entry_id = f"stub.65.special-{raw.lower()}"
            ids.append(entry_id)
            stubs.append(
                {
                    "id": entry_id,
                    "title": f"{cells[1]}特殊判定桩",
                    "aliases": [cells[1], raw],
                    "versions": ["6.5"],
                    "profile": PROFILE_65,
                    "status": "candidate",
                    "evidence": "legacy-structured",
                    "address": address(raw, PROFILE_65),
                    "stubStyle": "special-wrapper",
                    "semantics": cells[2],
                    "contract": {
                        "equipmentEffectId": hex_number(cells[3]),
                        "personalEffectId": hex_number(cells[4]),
                    },
                    "writePolicy": "不是通用四参数内联桩，必须按完整函数上下文处理。",
                    "relations": [],
                    "sourceRefs": [sid],
                }
            )
    mappings[STUB_PATH] = ids
    mappings[CORE_PATH] = [entry["id"] for entry in stubs]

    dispatch_sid = add_source(sources, DISPATCH_PATH, "6.5 特效调度函数、AL 分支和 EDX 表偏移")
    dispatch_text = git_text(DISPATCH_PATH)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for line in dispatch_text.splitlines():
        cells = parse_table_row(line) if line.startswith("|") else []
        if len(cells) < 3 or not re.fullmatch(r"[0-9A-Fa-f]{6,8}", cells[0]):
            continue
        raw = cells[0].upper()
        if cells[1].lower().startswith("al=") and len(cells) >= 4:
            grouped[raw].append({"al": cells[1].split("=", 1)[1], "edx": cells[2], "meaning": cells[3]})
        elif re.fullmatch(r"[0-9A-Fa-f]{4}", cells[1]):
            grouped[raw].append({"al": None, "edx": cells[1], "meaning": cells[-1]})

    functions = []
    function_ids = []
    for raw, branches in sorted(grouped.items()):
        known = next((value["meaning"] for value in branches if value["meaning"]), "")
        entry_id = f"fn.65.effect-dispatch-{raw.lower()}"
        function_ids.append(entry_id)
        functions.append(
            {
                "id": entry_id,
                "title": known or f"特效调度函数 {raw}",
                "aliases": [raw, f"调度函数 {raw}"],
                "versions": ["6.5"],
                "profile": PROFILE_65,
                "status": "candidate",
                "evidence": "legacy-structured",
                "address": address(raw, PROFILE_65),
                "callingConvention": "unknown",
                "inputs": "AL 可选子类型；单位上下文和四参数桩契约来自调用者",
                "returns": "EAX=核心特效判定结果（历史文档口径）",
                "semantics": "按固定 EDX 行偏移或 AL 分支选择特效数据，再进入核心特效判定。",
                "dispatchBranches": branches,
                "relations": ["fn.65.core-effect-engine"],
                "sourceRefs": [dispatch_sid, core_sid],
            }
        )
    mappings[DISPATCH_PATH] = function_ids
    return stubs, functions


def normalise_hex_tokens(lines: list[str]) -> list[str]:
    values = []
    for line in lines:
        for token in line.split():
            if re.fullmatch(r"[0-9A-Fa-f]{1,2}", token):
                values.append(token.upper().zfill(2))
    return values


def title_from_patch(path: str, text: str) -> str:
    for line in text.splitlines():
        value = line.strip()
        if value.startswith("#") and not value.startswith("##"):
            title = value.lstrip("# ").strip()
            if title and not title.startswith(("v3 修复", "第一行写", "第二行写")):
                return title
    return Path(path).stem


def parse_patch(path: str, version: str, profile: str, sid: str) -> dict | None:
    text = git_text(path)
    lines = text.splitlines()
    sites = []
    mode = "o"
    pending_notes: list[str] = []
    index = 0
    while index < len(lines):
        value = lines[index].strip()
        if value in {"o", "u"}:
            mode = value
            index += 1
            continue
        if value.startswith("#") and not value.startswith("##"):
            note = value.lstrip("# ").strip()
            if note:
                pending_notes.append(note)
            index += 1
            continue
        match = re.fullmatch(r"-([0-9A-Fa-f]+)", value)
        if not match:
            index += 1
            continue
        raw_address = match.group(1)
        index += 1
        byte_lines = []
        while index < len(lines):
            candidate = lines[index].strip()
            if re.fullmatch(r"-([0-9A-Fa-f]+)", candidate) or candidate in {"o", "u"} or candidate.startswith("#"):
                break
            if candidate and all(re.fullmatch(r"[0-9A-Fa-f]{1,2}", token) for token in candidate.split()):
                byte_lines.append(candidate)
            index += 1
        tokens = normalise_hex_tokens(byte_lines)
        if not tokens:
            continue
        role = pending_notes[-1] if pending_notes else "历史注入块"
        sites.append(
            {
                "address": address(raw_address, profile, kind="va" if mode == "o" else "fileOffset"),
                "replacementBytes": " ".join(tokens),
                "overwriteLength": len(tokens),
                "writeMode": "legacy-od-block" if mode == "o" else "legacy-ue-block",
                "instructionBoundary": None,
                "role": role,
            }
        )
    if not sites:
        return None
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()[:12]
    version_tag = "6.6x-kf" if "6.6xKF" in path or "6.6x KF" in path else "6.6x" if "6.6x" in path else version
    notes = []
    for line in lines:
        value = line.strip()
        if value.startswith("#") and not value.startswith("##"):
            note = value.lstrip("# ").strip()
            if note and note not in notes:
                notes.append(note)
    return {
        "id": f"patch.{version.replace('.', '')}.legacy-{digest}",
        "title": title_from_patch(path, text),
        "aliases": [Path(path).stem],
        "versions": [version],
        "profile": profile,
        "status": "candidate",
        "evidence": "legacy-patch-bytes",
        "kind": "legacy-injection",
        "versionVariant": version_tag,
        "sites": sites,
        "semantics": notes[0] if notes else Path(path).stem,
        "notes": notes[:40],
        "parameterSites": [site for site in sites if site["overwriteLength"] <= 4 and site["role"] != "历史注入块"],
        "writePolicy": "只保存历史替换字节；缺少原字节、精确样本身份或指令边界时不得自动应用。",
        "relations": [],
        "sourceRefs": [sid],
    }


def parse_patches(sources: dict[str, dict], mappings: dict[str, list[str]]) -> tuple[list[dict], list[dict]]:
    index_sid = add_source(sources, INJECTION_INDEX_PATH, "6.5 注入效果语义、代码区、参数点和冲突关系")
    mappings[INJECTION_INDEX_PATH] = []
    result: dict[str, list[dict]] = {"6.5": [], "6.6": []}
    for version, prefix, profile in (
        ("6.5", "6.5/03-机制与特效/", PROFILE_65),
        ("6.6", "6.6/03-机制与特效/", PROFILE_66_LEGACY),
    ):
        for path in git_paths(prefix, ".txt"):
            sid = add_source(sources, path, f"{version} 历史引擎注入替换块、参数点和注释语义")
            entry = parse_patch(path, version, profile, sid)
            if entry:
                if version == "6.5":
                    entry["sourceRefs"].append(index_sid)
                result[version].append(entry)
                mappings[path] = [entry["id"]]
                mappings[INJECTION_INDEX_PATH].append(entry["id"])

    conflicts = {
        "回mp攻击": ["两个版本使用同一 Hook 和代码区，只能二选一。"],
        "护卫": ["6.5 护卫代码区与僵尸大法历史代码区重叠；应用前必须重排或合并。"],
        "噬心毒咒": ["与策略偷钱形成历史链式 Hook；必须复核回跳是否仍落到下一补丁入口。"],
    }
    for entry in result["6.5"]:
        values = []
        for needle, messages in conflicts.items():
            if needle.lower() in entry["title"].lower() or any(needle.lower() in alias.lower() for alias in entry["aliases"]):
                values.extend(messages)
        if values:
            entry["conflicts"] = values
    return result["6.5"], result["6.6"]


def workflow_entry(entry_id: str, title: str, sid: str, goal: str, inputs: list[str], steps: list[str], gates: list[str], outputs: list[str], rollback: list[str]) -> dict:
    return {
        "id": entry_id,
        "title": title,
        "versions": ["6.5"],
        "status": "candidate",
        "evidence": "legacy-structured",
        "goal": goal,
        "inputs": inputs,
        "steps": [{"order": index + 1, "action": value} for index, value in enumerate(steps)],
        "gates": gates,
        "outputs": outputs,
        "rollback": rollback,
        "sourceRefs": [sid],
    }


def build_workflows(sources: dict[str, dict], mappings: dict[str, list[str]]) -> list[dict]:
    sids = {key: add_source(sources, path, "制作工作流、验证门禁和复用案例") for key, path in WORKFLOW_PATHS.items()}
    workflows = [
        workflow_entry(
            "workflow.65.mod-package-delivery", "ModPackage 自动化交付", sids["automation"],
            "把人物、兵种、物品、资源和 R/S 设计转换为可审计的增量包。",
            ["目标项目画像", "槽位规划", "结构化表更新", "资源和剧本变更"],
            ["冻结版本画像和槽位", "生成增量包与清单", "静态预览", "写测试副本", "逐域复读", "执行相关烟测", "推广或 direct 写入", "保存报告和备份"],
            ["不自动改槽位", "资源未预览不写编号", "剧本非白名单命令必须走完整树", "失败域不得被无关烟测掩盖"],
            ["变更包", "写前/写后差异", "备份", "复读结果", "烟测结果"],
            ["恢复备份", "拒绝继续推广", "保留失败报告"],
        ),
        workflow_entry(
            "workflow.65.effect-injection", "引擎特效注入制作", sids["effect"],
            "从特效语义生成可审计的 Hook、桩函数、代码洞和回跳方案。",
            ["目标 EXE 画像", "触发语义", "单位上下文", "特效号和效果值规则"],
            ["确认目标样本和入口", "复核调用点 ABI", "选择标准桩或内联桩", "分配代码洞", "计算 CALL/JMP 重定位", "记录原字节和覆盖长度", "检查冲突", "写测试副本", "静态复读和实机验证"],
            ["地址绑定画像", "覆盖完整指令", "旧字节必须匹配", "代码洞不得重叠", "寄存器和栈必须守恒"],
            ["补丁配方", "参数点", "冲突矩阵", "回滚字节", "验证报告"],
            ["逆序恢复已写站点", "恢复页保护", "标记样本污染并停止写入"],
        ),
        workflow_entry(
            "workflow.65.effect-workbench-acceptance", "特效工作台复盘与验收", sids["workbench"],
            "把特效扫描、能力判定、预览、写入和复读组织为单一可追踪任务。",
            ["目标 EXE", "特效目录", "预期机制", "证据包"],
            ["识别画像", "扫描当前安装状态", "生成能力矩阵", "构建写入预览", "核对冲突和参数", "应用到测试目标", "复读字节和行为", "更新证据状态"],
            ["扫描相似不等于已安装", "静态能力不能自动提升为运行时能力", "任一冲突阻断写入"],
            ["扫描清单", "能力矩阵", "应用报告", "证据升级记录"],
            ["按补丁记录恢复原字节", "保留失败时样本和日志"],
        ),
        workflow_entry(
            "workflow.65.r-script-template-clone", "R 剧本模板克隆", sids["scenario"],
            "复用成熟 R 剧本的 Scene/Section/Command 布局，仅替换受控文本和人物编号。",
            ["同版本成熟模板", "目标 R 剧本", "文本槽映射", "R 人物映射"],
            ["复读模板结构", "导出可见文本槽", "建立人物映射", "执行写前断言", "完整树写测试副本", "圆程复读", "实机烟测"],
            ["Scene/Section/Command 数保持一致", "0x72 默认不改", "Section 末尾 0x00 保留", "R 人物编号同场景唯一"],
            ["目标 EEX", "逐命令结构差异", "文本与人物映射", "实机结果"],
            ["保留模板副本", "结构不一致时丢弃目标写入"],
        ),
        workflow_entry(
            "workflow.65.rs-sprite-production", "人物 R/S 像素形象制作", sids["sprites"],
            "从角色设定和样例库制作可导入的 R/S 像素资源。",
            ["角色设定", "动作和方向清单", "同类样例", "目标资源尺寸和调色板"],
            ["筛选同构样例", "制作代表帧", "人工审阅轮廓和装备", "扩展动作/方向", "校验帧条尺寸", "预览 E5 替换", "导入测试槽", "实机审阅"],
            ["先代表帧后全套", "不从异构样例拼接关键部位", "编号映射必须复读"],
            ["帧条", "样例和选择理由", "图号映射", "审阅结论"],
            ["恢复资源备份", "保留上一版通过审阅的帧条"],
        ),
        workflow_entry(
            "workflow.65.map-terrain-publish", "地图底图与 Hexzmap 同步发布", sids["automation"],
            "保持视觉地图、地形格和剧本坐标一致。",
            ["Map JPG", "Hexzmap 块", "地图槽", "部署和触发坐标"],
            ["确认地图槽和尺寸", "校验 Hexzmap 格数", "检查必经格和触发格", "同步发布底图与地形", "复读关键坐标", "运行一致性烟测", "实机寻路验证"],
            ["不得新增无 Hexzmap 绑定的地图号", "视觉道路不等于地形可通行", "部署/增援/Boss 邻接格必须可站立"],
            ["地图资源", "地形块", "坐标审计", "一致性报告"],
            ["恢复地图和 Hexzmap 两份备份，禁止只回滚其中一份"],
        ),
        workflow_entry(
            "workflow.65.automated-battle-debug", "战场自动化与调试", sids["battle"],
            "用稳定触发、快照和复读定位战场脚本或引擎行为。",
            ["可复现关卡", "触发事件", "目标单位和坐标", "预期状态变化"],
            ["冻结测试存档和随机条件", "记录写前单位状态", "执行单一触发", "采集脚本/内存结果", "对比预期字段", "缩小到命令或函数入口", "重复验证"],
            ["一次只改变一个变量", "失败必须区分脚本、资源、地形和引擎层", "自动化结果需人工画面复核"],
            ["最小复现步骤", "状态快照", "地址/命令定位", "回归用例"],
            ["恢复测试存档和测试副本"],
        ),
    ]
    by_source = defaultdict(list)
    for entry in workflows:
        by_source[entry["sourceRefs"][0]].append(entry["id"])
    for key, path in WORKFLOW_PATHS.items():
        mappings[path] = by_source.get(sids[key], [])
    return workflows


def parse_smoke_tests(sources: dict[str, dict], mappings: dict[str, list[str]]) -> list[dict]:
    path = WORKFLOW_PATHS["validation"]
    sid = source_id(path)
    text = git_text(path)
    entries = []
    for line in text.splitlines():
        if not line.startswith("|") or "SmokeTests" not in line or "--" not in line:
            continue
        cells = parse_table_row(line)
        if len(cells) < 4 or cells[0].lower().startswith("command"):
            continue
        flag_match = re.search(r"--[a-z0-9-]+", cells[0], re.I)
        if not flag_match:
            continue
        flag = flag_match.group(0).lower()
        entry_id = "test.65.smoke-" + flag[2:]
        entries.append(
            {
                "id": entry_id,
                "title": cells[1],
                "aliases": [flag, cells[1]],
                "versions": ["6.5"],
                "status": "candidate",
                "evidence": "legacy-structured",
                "command": f"dotnet <SMOKE_TESTS_DLL> {flag}",
                "target": cells[1],
                "mutationScope": cells[2],
                "assertions": [cells[3]],
                "requiredArtifacts": ["console result", "test-copy diff when mutation is enabled"],
                "failureMeaning": "该领域的读写、结构或回归契约未满足；不能用其它无关烟测通过来覆盖。",
                "sourceRefs": [sid],
            }
        )
    entries = list({entry["id"]: entry for entry in entries}.values())
    mappings[path] = sorted(set(mappings.get(path, [])) | {entry["id"] for entry in entries})
    return entries


def build_case_studies(sources: dict[str, dict], mappings: dict[str, list[str]]) -> list[dict]:
    sids = {key: source_id(path) for key, path in WORKFLOW_PATHS.items()}
    cases = [
        {
            "id": "case.65.anxi-data-package", "title": "安西军传 Data ModPackage",
            "versions": ["6.5"], "status": "candidate", "evidence": "legacy-case-record",
            "objective": "把人物、兵种和职业设计批量写入独立基底。",
            "inputs": ["1005 个表更新", "人物 260 行", "兵种系 40 行", "详细职业 80 行"],
            "procedure": ["preview", "apply-test-copy", "表域烟测", "复读", "promote"],
            "outcome": ["表写入烟测通过", "生成 Data/Imsg/Ekd5 备份和报告"],
            "reusableLessons": ["纯 Data 包不应被无关地图烟测阻断", "基础表、特效分配和资源替换应拆包", "中文必须按目标表编码复读"],
            "sourceRefs": [sids["automation"]],
        },
        {
            "id": "case.65.anxi-quote-package", "title": "安西军传台词小包",
            "versions": ["6.5"], "status": "candidate", "evidence": "legacy-case-record",
            "objective": "只更新暴击、撤退台词和特殊暴击人物表，避免重刷全量 Data。",
            "inputs": ["撤退台词 49 行", "特殊暴击人物 21 行", "普通暴击 8 组三句"],
            "procedure": ["生成小包", "静态检查", "测试副本写入", "EffectPackage 写 EXE 表", "三项复读"],
            "outcome": ["测试副本和正式基底复读一致", "禁止读写 EXE patch 并行执行"],
            "reusableLessons": ["文本小改应独立成包", "EXE patch 必须带 expectedOldBytesHex", "读写依赖操作不能并行"],
            "sourceRefs": [sids["automation"]],
        },
        {
            "id": "case.65.anxi-r01-template-clone", "title": "安西 R_01 模板克隆迭代",
            "versions": ["6.5"], "status": "candidate", "evidence": "legacy-case-record",
            "objective": "从成熟 R_01 模板复用完整结构，并逐步修复文本、人物和 R/S 入口。",
            "inputs": ["刘备 6.4 R_01 模板", "安西目标文本", "人物映射", "出战名单"],
            "procedure": ["克隆 10 Scene/13 Section/501 Command", "修正换行和背景", "清理 0x02 内部信息", "保证 R 人物实例唯一", "同步 0x06/0x4A/0x4B"],
            "outcome": ["避免自造短结构在 Section 4 卡死", "形成 507/173 命令规模的最终 R/S 入口样板"],
            "reusableLessons": ["完整结构优先于从零拼接", "剧情露脸人物不等于已加入我军", "入口人数、名单和部署槽必须一致"],
            "sourceRefs": [sids["scenario"], sids["liu-bei"]],
        },
        {
            "id": "case.65.mp-recovery-effect-pilot", "title": "物理攻击后恢复 MP 复合特效试点",
            "versions": ["6.5"], "status": "candidate", "evidence": "legacy-case-record",
            "objective": "验证从特效蓝图到桩、参数、注入和验收的模块化路径。",
            "inputs": ["物理攻击结算点", "四参数特效判定", "伤害值", "MP 字段"],
            "procedure": ["定义触发和公式", "选择内联桩", "生成代码洞和回跳", "绑定特效号参数", "测试副本复读", "实机验证"],
            "outcome": ["形成可复用特效蓝图和写入凭据要求"],
            "reusableLessons": ["蓝图必须声明读取和写入字段", "参数位宽必须与机器码一致", "发布内容必须与验收样本一致"],
            "sourceRefs": [sids["composite-effect"]],
        },
        {
            "id": "case.65.liu-bei-rs-template", "title": "刘备 6.4 R/S 模板学习",
            "versions": ["6.4", "6.5"], "status": "candidate", "evidence": "legacy-case-record",
            "objective": "从成熟旧版关卡抽取 R 玩家切换、S 初始化和战中事件结构。",
            "inputs": ["R_01.eex", "S_01.eex", "完整树复读结果"],
            "procedure": ["统计 Scene/Section/Command", "识别 R 出战入口", "识别 S 初始化部署", "保留高风险命令原参数", "迁移前做版本复核"],
            "outcome": ["提供 R 剧本克隆和 S 战场结构的历史样板"],
            "reusableLessons": ["跨版本只复用结构，不复制裸地址", "高风险命令保留原参数", "迁移后必须圆程复读"],
            "sourceRefs": [sids["liu-bei"]],
        },
    ]
    for entry in cases:
        for sid in entry["sourceRefs"]:
            path = next((path for key, path in WORKFLOW_PATHS.items() if sids[key] == sid), None)
            if path:
                mappings[path] = sorted(set(mappings.get(path, [])) | {entry["id"]})
    return cases


def update_source_manifest(sources: dict[str, dict]) -> None:
    path = ROOT / "sources" / "source-manifest.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    retained = [entry for entry in document["entries"] if not entry["id"].startswith(f"src.history.{COMMIT}.")]
    document["entries"] = sorted(retained + list(sources.values()), key=lambda entry: entry["id"])
    write_json("sources/source-manifest.json", document)


def update_cleanup_and_research(mappings: dict[str, list[str]]) -> None:
    cleanup_path = ROOT / "sources" / "cleanup-report.json"
    cleanup = json.loads(cleanup_path.read_text(encoding="utf-8"))
    mapped_paths = {path for path, ids in mappings.items() if ids}
    for record in cleanup["records"]:
        old_path = record.get("oldPath")
        if old_path not in mapped_paths:
            continue
        record["action"] = "structured-candidate"
        record["reason"] = "历史技术内容已提炼为结构化候选；进入默认索引但不具备自动写回资格。"
        record["mappedEntities"] = sorted(set(mappings[old_path]))
    counts = defaultdict(int)
    for record in cleanup["records"]:
        counts[record["action"]] += 1
    cleanup["decisionCounts"] = dict(sorted(counts.items()))
    cleanup["coverageRule"] = "正式事实使用 canonical；历史技术内容可进入 structured-candidate；其余候选保留在 research。"
    write_json("sources/cleanup-report.json", cleanup)

    research_path = ROOT / "research" / "research-gaps.json"
    research = json.loads(research_path.read_text(encoding="utf-8"))
    research["entries"] = [entry for entry in research["entries"] if entry.get("legacyPath") not in mapped_paths]
    research["entries"].sort(key=lambda entry: entry["id"])
    write_json("research/research-gaps.json", research)


def main() -> None:
    sources: dict[str, dict] = {}
    mappings: dict[str, list[str]] = {}

    commands_65, commands_66 = parse_script_commands(sources, mappings)
    stubs, dispatchers = parse_effect_stubs(sources, mappings)
    patches_65, patches_66 = parse_patches(sources, mappings)
    workflows = build_workflows(sources, mappings)
    smoke_tests = parse_smoke_tests(sources, mappings)
    cases = build_case_studies(sources, mappings)

    write_json("6.5/data/scripts/script-commands.json", {"schemaVersion": 1, "entityType": "script-command", "entries": commands_65})
    write_json("6.6/data/scripts/script-command-extensions.json", {"schemaVersion": 1, "entityType": "script-command", "entries": commands_66})
    write_json("6.5/data/stubs/effect-stubs.json", {"schemaVersion": 1, "entityType": "effect-stub", "entries": stubs})
    write_json("6.5/data/functions/legacy-effect-dispatchers.json", {"schemaVersion": 1, "entityType": "function", "entries": dispatchers})
    write_json("6.5/data/patches/legacy-effect-injections.json", {"schemaVersion": 1, "entityType": "patch-recipe", "entries": patches_65})
    write_json("6.6/data/patches/legacy-effect-injections.json", {"schemaVersion": 1, "entityType": "patch-recipe", "entries": patches_66})
    write_json("6.5/data/workflows/production-workflows.json", {"schemaVersion": 1, "entityType": "workflow", "entries": workflows})
    write_json("6.5/data/tests/smoke-test-contracts.json", {"schemaVersion": 1, "entityType": "test-contract", "entries": smoke_tests})
    write_json("6.5/data/cases/production-cases.json", {"schemaVersion": 1, "entityType": "case-study", "entries": cases})
    write_json(
        "6.6/data/profiles/legacy-patch-profiles.json",
        {
            "schemaVersion": 1,
            "entityType": "engine-profile",
            "entries": [
                {
                    "id": PROFILE_66_LEGACY,
                    "title": "6.6/6.6x 历史注入补丁族",
                    "aliases": ["6.6x legacy patch family", "Star6.6x", "6.6xKF"],
                    "versions": ["6.6"],
                    "status": "candidate",
                    "evidence": "legacy-patch-bytes",
                    "imageBase": "0x00400000",
                    "machine": "x86-pe32",
                    "sample": None,
                    "addressPolicy": "仅用于保存历史补丁中的地址和值；没有精确样本 SHA 和原字节，不得自动写入。",
                    "sourceRefs": sorted({entry["sourceRefs"][0] for entry in patches_66}),
                }
            ],
        },
    )

    update_source_manifest(sources)
    update_cleanup_and_research(mappings)
    print(
        "legacy_import_ok "
        f"script65={len(commands_65)} script66={len(commands_66)} stubs={len(stubs)} "
        f"dispatchers={len(dispatchers)} patches65={len(patches_65)} patches66={len(patches_66)} "
        f"workflows={len(workflows)} tests={len(smoke_tests)} cases={len(cases)} sources={len(sources)}"
    )


if __name__ == "__main__":
    main()
