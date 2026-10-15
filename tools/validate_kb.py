from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ALLOWED_TOP = {"6.5", "6.5pl", "6.6", "legacy", "research", "schema", "sources", "tools"}
ALLOWED_ROOT = {".gitattributes", ".gitignore", "README.md", "llms.txt", "CONTRIBUTING.md", "NOTICE.md", "index.json"}
FORBIDDEN_EXTENSIONS = {".exe", ".dll", ".pdb", ".bin", ".obj", ".rar", ".zip", ".7z", ".doc", ".docx", ".xls", ".xlsx", ".log", ".bak", ".tmp"}
FORBIDDEN_PARTS = {"bin", "obj", "build", "publish", "release", "__pycache__"}
ADDRESS_KINDS = {"va", "rva", "fileOffset", "pointerSlot", "resolvedRuntimeAddress"}
ENTITY_TYPES = {
    "engine-profile", "function", "global", "data-structure", "file-format",
    "patch-recipe", "mechanism", "effect-stub", "script-command", "workflow",
    "test-contract", "case-study",
}
STATUSES = {"canonical", "candidate", "legacy-reference"}
HEX_ADDRESS = re.compile(r"^0x[0-9A-Fa-f]{1,16}$")
HEX_TOKEN = re.compile(r"^(?:[0-9A-Fa-f]{2}|\?\?)$")


def error(errors: list[str], message: str) -> None:
    errors.append(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        error(errors, f"invalid JSON {path.relative_to(ROOT).as_posix()}: {exc}")
        return None


def iter_addresses(value: object, trail: str = ""):
    if isinstance(value, dict):
        if {"kind", "value", "profile", "evidence"}.issubset(value):
            yield trail, value
        for key, child in value.items():
            yield from iter_addresses(child, f"{trail}.{key}" if trail else key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_addresses(child, f"{trail}[{index}]")


def validate_address(errors: list[str], owner: str, trail: str, value: dict, profiles: set[str]) -> None:
    if value.get("kind") not in ADDRESS_KINDS:
        error(errors, f"{owner}:{trail} invalid address kind {value.get('kind')}")
    if not HEX_ADDRESS.fullmatch(str(value.get("value", ""))):
        error(errors, f"{owner}:{trail} invalid hexadecimal address {value.get('value')}")
    profile = value.get("profile")
    if not profile or profile not in profiles:
        error(errors, f"{owner}:{trail} address is not bound to a known profile: {profile}")
    if value.get("kind") == "resolvedRuntimeAddress" and value.get("evidence") == "version-constant":
        error(errors, f"{owner}:{trail} runtime observation cannot be a version constant")


def validate_fields(errors: list[str], entry: dict) -> None:
    stride = entry.get("stride")
    if not isinstance(stride, int) or stride <= 0:
        error(errors, f"{entry['id']} has invalid stride")
        return
    occupied: dict[int, tuple[str, str | None]] = {}
    names = set()
    for item in entry.get("fields", []):
        name = item.get("name")
        if not name or name in names:
            error(errors, f"{entry['id']} has duplicate/empty field name {name}")
        names.add(name)
        try:
            offset = int(str(item.get("offset")), 16)
        except ValueError:
            error(errors, f"{entry['id']}.{name} has invalid offset")
            continue
        width = item.get("width")
        if not isinstance(width, int) or width <= 0 or offset < 0 or offset + width > stride:
            error(errors, f"{entry['id']}.{name} exceeds stride 0x{stride:X}")
            continue
        overlay = item.get("overlay")
        for byte in range(offset, offset + width):
            if byte in occupied and not overlay:
                error(errors, f"{entry['id']}.{name} overlaps {occupied[byte][0]} at 0x{byte:X} without overlay")
            elif byte in occupied and occupied[byte][1] != overlay:
                error(errors, f"{entry['id']}.{name} overlay group differs from {occupied[byte][0]}")
            else:
                occupied[byte] = (name, overlay)


def validate_patch(errors: list[str], entry: dict) -> None:
    kind = entry.get("kind")
    if kind == "semantic-locator":
        for required in ("signature", "extraction", "scanScope", "matchPolicy"):
            if not entry.get(required):
                error(errors, f"{entry['id']} semantic locator missing {required}")
        if entry.get("sites"):
            error(errors, f"{entry['id']} semantic locator must not invent a fixed patch site")
        return

    for required in ("kind", "sites"):
        if required not in entry:
            error(errors, f"{entry['id']} patch missing {required}")
    if not entry.get("sites"):
        error(errors, f"{entry['id']} patch has no sites")
    for index, site in enumerate(entry.get("sites", [])):
        length = site.get("overwriteLength")
        expected = site.get("expectedBytes")
        status = entry.get("status")
        if not isinstance(length, int) or length <= 0:
            error(errors, f"{entry['id']} patch site {index} has invalid overwrite length")
            continue
        if status == "canonical":
            if not expected:
                error(errors, f"{entry['id']} canonical patch site {index} is incomplete")
                continue
            tokens = str(expected).split()
            if len(tokens) != length or any(not HEX_TOKEN.fullmatch(token) for token in tokens):
                error(errors, f"{entry['id']} site {index} expected bytes do not match overwrite length")
            replacements = []
            if site.get("replacementBytes"):
                replacements.append(site["replacementBytes"])
            replacements.extend(value.get("bytes") for value in site.get("replacementVariants", []))
            if not replacements and kind not in {"hook", "call-retarget"}:
                error(errors, f"{entry['id']} site {index} has no replacement bytes or variants")
            for replacement in replacements:
                replacement_tokens = str(replacement).split()
                if len(replacement_tokens) != length or any(not HEX_TOKEN.fullmatch(token) for token in replacement_tokens):
                    error(errors, f"{entry['id']} site {index} replacement bytes do not match overwrite length")
            if site.get("instructionBoundary") is False:
                if site.get("writeMode") not in {
                    "function-entry-prefix", "immediate-operand-only",
                    "instruction-prefix-terminal-transfer", "function-entry-terminal-transfer",
                } or not site.get("executionEffect"):
                    error(errors, f"{entry['id']} site {index} has an unexplained partial-instruction write")
        elif status == "candidate":
            if expected:
                tokens = str(expected).split()
                if len(tokens) != length or any(not HEX_TOKEN.fullmatch(token) for token in tokens):
                    error(errors, f"{entry['id']} candidate site {index} expected bytes do not match overwrite length")
            replacements = []
            if site.get("replacementBytes"):
                replacements.append(site["replacementBytes"])
            replacements.extend(value.get("bytes") for value in site.get("replacementVariants", []))
            if not replacements:
                error(errors, f"{entry['id']} candidate site {index} has no historical replacement bytes")
            for replacement in replacements:
                tokens = str(replacement).split()
                if len(tokens) != length or any(not HEX_TOKEN.fullmatch(token) for token in tokens):
                    error(errors, f"{entry['id']} candidate site {index} replacement bytes do not match overwrite length")
            if not expected and "不得自动" not in str(entry.get("writePolicy", "")):
                error(errors, f"{entry['id']} candidate without expected bytes must explicitly forbid automatic writes")
    if kind in {"hook", "call-retarget", "entry-jump"}:
        stub = entry.get("stub", {})
        if not isinstance(stub, dict) or not {"entry", "return", "relocations"}.issubset(stub):
            error(errors, f"{entry['id']} has incomplete stub contract")


def validate_script_command(errors: list[str], entry: dict, keys: set[tuple[str, str, object]]) -> None:
    opcode = str(entry.get("opcode", ""))
    if not re.fullmatch(r"0x[0-9A-Fa-f]{2}", opcode):
        error(errors, f"{entry['id']} has invalid script opcode {opcode}")
    subcommand = entry.get("subcommand")
    if subcommand is not None and (not isinstance(subcommand, int) or subcommand < 0):
        error(errors, f"{entry['id']} has invalid subcommand {subcommand}")
    for version in entry.get("versions", []):
        key = (str(version), opcode.upper(), subcommand)
        if key in keys:
            error(errors, f"duplicate script command key: {key}")
        keys.add(key)
    slots: list[int] = []
    for parameter in entry.get("parameters", []):
        match = re.fullmatch(r"P([1-9][0-9]*)", str(parameter.get("slot", "")))
        if not match:
            error(errors, f"{entry['id']} has invalid parameter slot {parameter.get('slot')}")
            continue
        slots.append(int(match.group(1)))
        for required in ("name", "type", "meaning"):
            if not parameter.get(required):
                error(errors, f"{entry['id']}.{parameter.get('slot')} missing {required}")
    if slots != sorted(set(slots)):
        error(errors, f"{entry['id']} parameter slots are duplicated or out of order")


def validate_effect_stub(errors: list[str], entry: dict) -> None:
    if not isinstance(entry.get("address"), dict) or not entry.get("profile"):
        error(errors, f"{entry['id']} effect stub must bind an address and profile")
    if entry.get("stubStyle") in {"standard-dispatch", "inline-core-call"}:
        expected = ["effectValueFlag", "stackingFlag", "equipmentEffectId", "personalEffectId"]
        if entry.get("contract", {}).get("pushOrder") != expected:
            error(errors, f"{entry['id']} has an invalid four-argument push order")


def validate_workflow(errors: list[str], entry: dict) -> None:
    orders = [step.get("order") for step in entry.get("steps", [])]
    if orders != list(range(1, len(orders) + 1)):
        error(errors, f"{entry['id']} workflow steps are not contiguous from 1")
    for required in ("goal", "inputs", "steps", "gates", "outputs", "rollback"):
        if not entry.get(required):
            error(errors, f"{entry['id']} workflow missing {required}")


def validate_test_contract(errors: list[str], entry: dict) -> None:
    command = str(entry.get("command", ""))
    if not command or re.search(r"(?:[A-Z]:[\\/]|/Users/|/home/)", command):
        error(errors, f"{entry['id']} test command is empty or contains an absolute path")
    for required in ("target", "mutationScope", "assertions", "requiredArtifacts", "failureMeaning"):
        if not entry.get(required):
            error(errors, f"{entry['id']} test contract missing {required}")


def validate_case_study(errors: list[str], entry: dict) -> None:
    for required in ("objective", "inputs", "procedure", "outcome", "reusableLessons"):
        if not entry.get(required):
            error(errors, f"{entry['id']} case study missing {required}")


def validate_generated(errors: list[str]) -> None:
    watched = [ROOT / "index.json", *sorted(ROOT.glob("*/reference/*.md"))]
    before = {path: path.read_bytes() for path in watched if path.exists()}
    for script in ("build_reference.py", "build_index.py"):
        result = subprocess.run([sys.executable, str(ROOT / "tools" / script)], cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            error(errors, f"{script} failed: {result.stderr.strip() or result.stdout.strip()}")
            return
    after_paths = [ROOT / "index.json", *sorted(ROOT.glob("*/reference/*.md"))]
    after = {path: path.read_bytes() for path in after_paths if path.exists()}
    if before != after:
        changed = sorted(path.relative_to(ROOT).as_posix() for path in set(before) | set(after) if before.get(path) != after.get(path))
        error(errors, "generated artifacts were stale: " + " | ".join(changed))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    errors: list[str] = []
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        parts = rel.split("/")
        if len(parts) == 1 and path.name not in ALLOWED_ROOT:
            error(errors, f"unexpected root file: {rel}")
        if len(parts) > 1 and parts[0] not in ALLOWED_TOP:
            error(errors, f"unexpected top-level path: {rel}")
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS or any(part.lower() in FORBIDDEN_PARTS for part in parts):
            error(errors, f"forbidden artifact: {rel}")
        if path.suffix.lower() in {".md", ".txt", ".json", ".py"}:
            try:
                text = path.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError as exc:
                error(errors, f"not UTF-8: {rel}: {exc}")
                continue
            if path.name != "validate_kb.py" and re.search(r"(?:[A-Z]:[\\/]|/Users/|/home/)", text):
                error(errors, f"local absolute path: {rel}")
            if re.search(r"(?i)(?:BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY|ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9]+)", text):
                error(errors, f"secret-like value: {rel}")

    data_paths = sorted([*ROOT.glob("6.5/data/**/*.json"), *ROOT.glob("6.6/data/**/*.json"), *ROOT.glob("legacy/data/**/*.json")])
    documents: list[tuple[Path, dict]] = []
    ids: dict[str, str] = {}
    profiles: set[str] = set()
    source_ids: set[str] = set()
    script_keys: set[tuple[str, str, object]] = set()

    for entity_type in ENTITY_TYPES:
        schema_path = ROOT / "schema" / f"{entity_type}.schema.json"
        schema = load_json(schema_path, errors)
        if not isinstance(schema, dict) or schema.get("properties", {}).get("entityType", {}).get("const") != entity_type:
            error(errors, f"missing or mismatched schema for {entity_type}")

    source_document = load_json(ROOT / "sources" / "source-manifest.json", errors)
    if isinstance(source_document, dict):
        for item in source_document.get("entries", []):
            source_id = item.get("id")
            if not source_id or source_id in source_ids:
                error(errors, f"duplicate/empty source id: {source_id}")
            source_ids.add(source_id)
            if not re.fullmatch(r"[0-9A-F]{64}", str(item.get("sha256", ""))):
                error(errors, f"invalid source hash: {source_id}")
            if Path(str(item.get("path", ""))).is_absolute():
                error(errors, f"source path must be relative: {source_id}")

    for path in data_paths:
        value = load_json(path, errors)
        if not isinstance(value, dict):
            continue
        entity_type = value.get("entityType")
        if value.get("schemaVersion") != 1 or entity_type not in ENTITY_TYPES or not isinstance(value.get("entries"), list):
            error(errors, f"invalid collection envelope: {path.relative_to(ROOT).as_posix()}")
            continue
        documents.append((path, value))
        for item in value["entries"]:
            entry_id = item.get("id")
            if not entry_id or entry_id in ids:
                error(errors, f"duplicate/empty entity id: {entry_id}")
            else:
                ids[entry_id] = path.relative_to(ROOT).as_posix()
            for required in ("title", "status", "evidence", "sourceRefs"):
                if required not in item:
                    error(errors, f"{entry_id} missing {required}")
            if item.get("status") not in STATUSES:
                error(errors, f"{entry_id} has unsupported status {item.get('status')}")
            if entity_type == "engine-profile":
                profiles.add(entry_id)

    for path, document in documents:
        entity_type = document["entityType"]
        for item in document["entries"]:
            owner = item.get("id", path.name)
            version_root = path.relative_to(ROOT).parts[0]
            if version_root in {"6.5", "6.6"} and item.get("status") == "legacy-reference":
                error(errors, f"{owner} legacy-reference status must live under legacy/data")
            if version_root == "legacy" and item.get("status") != "legacy-reference":
                error(errors, f"{owner} in legacy/data must use legacy-reference status")
            item_profile = item.get("profile")
            if entity_type != "engine-profile" and item_profile and item_profile not in profiles:
                error(errors, f"{owner} references unknown profile {item_profile}")
            for trail, value in iter_addresses(item):
                validate_address(errors, owner, trail, value, profiles)
            for source_ref in item.get("sourceRefs", []):
                if source_ref not in source_ids:
                    error(errors, f"{owner} references unknown source {source_ref}")
            relations = list(item.get("relations", []))
            relations.extend(step.get("entity") for step in item.get("steps", []) if step.get("entity"))
            relations.extend(item.get("pierceBranch", []))
            relations.extend(item.get("state", []))
            if item.get("locatorRef"):
                relations.append(item["locatorRef"])
            for relation in relations:
                if relation not in ids:
                    error(errors, f"{owner} references unknown entity {relation}")
            if entity_type == "data-structure":
                validate_fields(errors, item)
            if entity_type == "patch-recipe":
                validate_patch(errors, item)
            if entity_type == "script-command":
                validate_script_command(errors, item, script_keys)
            if entity_type == "effect-stub":
                validate_effect_stub(errors, item)
            if entity_type == "workflow":
                validate_workflow(errors, item)
            if entity_type == "test-contract":
                validate_test_contract(errors, item)
            if entity_type == "case-study":
                validate_case_study(errors, item)

    if list((ROOT / "6.5pl").rglob("*.json")):
        error(errors, "6.5pl must not contain canonical data until an independent profile is verified")

    cleanup = load_json(ROOT / "sources" / "cleanup-report.json", errors)
    if not isinstance(cleanup, dict) or cleanup.get("oldIndexedEntryCount") != len(cleanup.get("records", [])):
        error(errors, "cleanup report does not cover every old indexed entry")
    elif isinstance(cleanup, dict):
        counts: dict[str, int] = {}
        for record in cleanup.get("records", []):
            action = record.get("action")
            counts[action] = counts.get(action, 0) + 1
            mapped = record.get("mappedEntities", [])
            if action in {"merge-into-entity", "structured-candidate"} and not mapped:
                error(errors, f"cleanup merge has no mapped entity: {record.get('oldPath')}")
            for entity_id in mapped:
                if entity_id not in ids:
                    error(errors, f"cleanup maps to unknown entity {entity_id}: {record.get('oldPath')}")
        if cleanup.get("decisionCounts") != dict(sorted(counts.items())):
            error(errors, "cleanup decisionCounts does not match records")

    research = load_json(ROOT / "research" / "research-gaps.json", errors)
    research_ids = {item.get("id") for item in research.get("entries", [])} if isinstance(research, dict) else set()

    index = load_json(ROOT / "index.json", errors)
    if isinstance(index, dict):
        if index.get("schemaVersion") != 3 or index.get("structuredAuthority") != "version-data-json":
            error(errors, "index.json is not the structured schema v3 index")
        index_ids = [item.get("id") for item in index.get("entries", [])]
        if set(index_ids) != set(ids) or len(index_ids) != len(ids):
            error(errors, "index entity set differs from structured data")
        if research_ids & set(index_ids):
            error(errors, "research entries leaked into the default index")
        actual_status_counts = {
            status: sum(1 for path, document in documents for entry in document["entries"] if entry.get("status") == status)
            for status in sorted({entry.get("status") for path, document in documents for entry in document["entries"]})
        }
        if index.get("statusCounts") != actual_status_counts:
            error(errors, "index statusCounts differs from structured data")
        indexed_files = {item.get("path") for item in index.get("structuredFiles", [])}
        actual_files = {path.relative_to(ROOT).as_posix() for path, _ in documents}
        if indexed_files != actual_files:
            error(errors, "index structuredFiles differs from structured data files")
        for item in index.get("structuredFiles", []):
            target = ROOT / item.get("path", "")
            if not target.exists() or item.get("sha256") != sha256(target):
                error(errors, f"index structured file hash mismatch: {item.get('path')}")
        for item in index.get("entries", []):
            target = ROOT / item.get("structuredDataPath", item.get("canonicalDataPath", ""))
            reference = ROOT / item.get("referencePath", "")
            if not target.exists() or not reference.exists():
                error(errors, f"index target/reference missing for {item.get('id')}")
            if item.get("versions") == ["6.5pl"]:
                error(errors, f"6.5pl canonical entry is not allowed yet: {item.get('id')}")

    validate_generated(errors)

    required_queries = {
        "0x004837C2": "fn.65.item-id-to-record",
        "攻击函数": "mechanism.65.physical-attack-targeting",
        "E5 格式": "format.e5.indexed-archive",
        "小暗 S 加速": "mechanism.66.xiaoan.super-s",
        "0x004210D0": "stub.65.standard-4210d0",
        "0x14": "script.65.opcode-14",
        "ModPackage 自动化交付": "workflow.65.mod-package-delivery",
        "--rs-write-smoke": "test.65.smoke-rs-write-smoke",
    }
    searchable = json.dumps(index, ensure_ascii=False) if isinstance(index, dict) else ""
    for query, expected in required_queries.items():
        if query not in searchable or expected not in searchable:
            error(errors, f"required query coverage missing: {query} -> {expected}")
    structures_text = (ROOT / "6.5" / "reference" / "structures.md").read_text(encoding="utf-8") if (ROOT / "6.5" / "reference" / "structures.md").exists() else ""
    if "0x004A7B20 + battlefield_id * 0x30 + field_offset" not in structures_text or "`hp` | `0x10`" not in structures_text:
        error(errors, "tactical HP address formula is not present in the human reference")

    if errors:
        print("validation_failed")
        for item in errors:
            print("- " + item)
        return 1
    print(f"validation_ok files={len(files)} entities={len(ids)} sources={len(source_ids)} research={len(research_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
