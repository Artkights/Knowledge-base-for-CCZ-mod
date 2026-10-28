from __future__ import annotations

import argparse
import hashlib
import sys
sys.dont_write_bytecode = True
import json
from pathlib import Path


from generated_artifacts import differences, update
from version_config import DATA_VERSIONS, REFERENCE_FILES, ROOT, data_paths

DATA_PATTERNS = [version + "/data/**/*.json" for version in DATA_VERSIONS]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def first_address(entry: dict) -> dict | None:
    if isinstance(entry.get("address"), dict):
        return entry["address"]
    sites = entry.get("sites", [])
    if sites and isinstance(sites[0].get("address"), dict):
        return sites[0]["address"]
    return None


def collect_search_terms(entry: dict) -> list[str]:
    values: list[str] = [entry["id"], entry["title"], *entry.get("aliases", [])]
    for key in ("semantics", "indexFormula", "callingConvention", "inputs", "returns", "callerSemantics"):
        value = entry.get(key)
        if isinstance(value, str):
            values.append(value)
    for _, value in walk(entry):
        if isinstance(value, dict) and value.get("kind") in {"va", "rva", "fileOffset", "pointerSlot", "resolvedRuntimeAddress"}:
            values.append(str(value.get("value", "")))
    for field in entry.get("fields", []):
        values.extend(str(field.get(key, "")) for key in ("name", "meaning", "offset"))
    excluded = {"replacementBytes", "expectedBytes", "bytes", "sha256", "sourceRefs"}
    for trail, value in walk(entry):
        parts = {part.split("[", 1)[0] for part in trail.split(".")}
        if (
            isinstance(value, str)
            and trail not in {"id", "title", "status", "evidence"}
            and not (parts & excluded)
            and len(value) <= 240
        ):
            values.append(value)
    return list(dict.fromkeys(value for value in values if value))


def walk(value: object, trail: str = ""):
    yield trail, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{trail}.{key}" if trail else key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{trail}[{index}]")


def build_payload() -> dict:
    entries = []
    for path in data_paths(ROOT):
        document = json.loads(path.read_text(encoding="utf-8"))
        entity_type = document["entityType"]
        rel = path.relative_to(ROOT).as_posix()
        version_dir = rel.split("/", 1)[0]
        reference = f"{version_dir}/reference/{REFERENCE_FILES[entity_type]}"
        for item in document["entries"]:
            addr = first_address(item)
            entries.append({
                "id": item["id"], "entityType": entity_type, "title": item["title"],
                "versions": item.get("versions", []), "profile": item.get("profile"),
                "status": item["status"], "evidence": item["evidence"], "address": addr,
                "searchTerms": collect_search_terms(item),
                "structuredDataPath": rel, "referencePath": reference,
                "sourceRefs": item.get("sourceRefs", []),
            })
    entries.sort(key=lambda item: item["id"])
    files = sorted({item["structuredDataPath"] for item in entries})
    payload = {
        "schemaVersion": 3, "structuredAuthority": "version-data-json",
        "generatedBy": "tools/build_index.py", "entityCount": len(entries),
        "statusCounts": {
            status: sum(1 for entry in entries if entry["status"] == status)
            for status in sorted({entry["status"] for entry in entries})
        },
        "structuredFiles": [{"path": rel, "sha256": sha256(ROOT / rel)} for rel in files],
        "entries": entries,
    }
    return payload


def generated_documents() -> dict[Path, str]:
    return {ROOT / "index.json": json.dumps(build_payload(), ensure_ascii=False, indent=2) + "\n"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the structured knowledge index.")
    parser.add_argument("--check", action="store_true", help="Report stale output without editing files")
    args = parser.parse_args()
    expected = generated_documents()
    changed = differences(expected)
    if args.check:
        for path in changed:
            print("stale: " + path.relative_to(ROOT).as_posix())
        return int(bool(changed))
    update(expected)
    print(f"indexed_entities={build_payload()['entityCount']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
