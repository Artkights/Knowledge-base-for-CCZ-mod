from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_PATTERNS = ["6.5/data/**/*.json", "6.6/data/**/*.json", "legacy/data/**/*.json"]
REFERENCE_FILES = {
    "engine-profile": "profiles.md", "function": "functions.md", "global": "globals.md",
    "data-structure": "structures.md", "file-format": "file-formats.md",
    "patch-recipe": "patches.md", "mechanism": "mechanisms.md",
}


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
    return list(dict.fromkeys(value for value in values if value))


def walk(value: object, trail: str = ""):
    yield trail, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, f"{trail}.{key}" if trail else key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{trail}[{index}]")


def main() -> None:
    entries = []
    paths: list[Path] = []
    for pattern in DATA_PATTERNS:
        paths.extend(ROOT.glob(pattern))
    for path in sorted(set(paths)):
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
                "canonicalDataPath": rel, "referencePath": reference,
                "sourceRefs": item.get("sourceRefs", []),
            })
    entries.sort(key=lambda item: item["id"])
    files = sorted({item["canonicalDataPath"] for item in entries})
    payload = {
        "schemaVersion": 2, "canonicalAuthority": "structured-json",
        "generatedBy": "tools/build_index.py", "entityCount": len(entries),
        "canonicalFiles": [{"path": rel, "sha256": sha256(ROOT / rel)} for rel in files],
        "entries": entries,
    }
    (ROOT / "index.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(f"indexed_entities={len(entries)} canonical_files={len(files)}")


if __name__ == "__main__":
    main()
