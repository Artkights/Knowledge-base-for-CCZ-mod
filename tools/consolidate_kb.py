"""Audit and apply deterministic knowledge-base consolidation edits.

The auditor is read-only. ``--apply`` consumes an explicit plan file so every
removed alias, retitled entity or deleted evidence snapshot stays reviewable.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from version_config import ROOT, data_paths

REVIEW_DATE = "2026-11-15"
BASELINE_COMMIT = "b75eb158c944a4ebdf32b47814e5505df952cee4"
PLAN_PATH = "sources/consolidation-plan-20261115.json"
REPORT_PATH = "sources/consolidation-report-20261115.json"
HEX_ALIAS = re.compile(r"^0x[0-9A-Fa-f]+$")
PLACEHOLDER = re.compile(r"TODO|待补|待定|占位|placeholder|暂无")
VERIFIED_CLAIMS = [
    {
        "claim": "6.6 股票策略伤害的诱惑判定为策略类型 0x05，复刻版山贼变体为 0x14",
        "evidence": "sources/evidence/strategy-job-specific-damage-modifiers-20261115.json",
        "fileOffset": "0x3B5F0",
        "bytes": {
            "6.4": "80 7D 10 14",
            "6.5": "80 7D 10 14",
            "6.6-v716": "80 7D DC 05",
            "6.6-shanzhai": "80 7D DC 14",
        },
        "conclusion": "条目现有写法正确，不得按版本号统一改成 0x05 或 0x14。",
    },
    {
        "claim": "6.6 股票策略命中桩为 8B 45 F8 3C 05；山贼变体为 8B 45 F8 3C 14",
        "evidence": "sources/evidence/strategy-job-specific-damage-modifiers-20261115.json",
        "fileOffset": "0x3B5F0",
        "bytes": {
            "6.4": "8B 45 10 3C 14",
            "6.5": "8B 45 10 3C 14",
            "6.6-v716": "8B 45 F8 3C 05",
            "6.6-shanzhai": "8B 45 F8 3C 14",
        },
        "conclusion": "命中判定与伤害判定的局部偏移均为 [ebp-8]（6.6），不是 [ebp+0x10]。",
    },
]


def json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_documents(root: Path) -> list[tuple[str, dict]]:
    documents = []
    for path in data_paths(root):
        documents.append((relative(path, root), json.loads(path.read_text(encoding="utf-8"))))
    return documents


def entity_rows(root: Path):
    for rel, document in load_documents(root):
        version = rel.split("/", 1)[0]
        for entry in document["entries"]:
            yield rel, version, document["entityType"], entry


def load_manifest(root: Path) -> list[dict]:
    path = root / "sources" / "source-manifest.json"
    if not path.is_file():
        return []
    return json.loads(path.read_text(encoding="utf-8")).get("entries", [])


def referenced_evidence(manifest: list[dict]) -> set[str]:
    referenced = set()
    for record in manifest:
        for key in ("path", "snapshotPath"):
            value = record.get(key)
            if isinstance(value, str) and value.startswith("sources/evidence/"):
                referenced.add(value.replace("\\", "/"))
    return referenced


def evidence_groups(root: Path, referenced: set[str], deleting: set[str] | None = None) -> tuple[list[dict], list[str]]:
    deleting = deleting or set()
    directory = root / "sources" / "evidence"
    groups: dict[str, list[str]] = {}
    if directory.is_dir():
        for path in sorted(directory.iterdir()):
            if path.is_file():
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                groups.setdefault(digest, []).append(relative(path, root))
    duplicates = []
    for digest, paths in sorted(groups.items()):
        if len(paths) < 2:
            continue
        kept = [path for path in paths if path in referenced]
        keep = kept[0] if kept else paths[0]
        remove = [path for path in paths if path != keep and path not in referenced and path not in deleting]
        duplicates.append({
            "sha256": digest.upper(),
            "files": paths,
            "keep": keep,
            "remove": remove,
            "referenced": sorted(kept),
        })
    orphans = sorted(path for paths in groups.values() for path in paths if path not in referenced)
    return duplicates, orphans


def build_report(root: Path = ROOT) -> dict:
    manifest = load_manifest(root)
    referenced = referenced_evidence(manifest)
    rows = list(entity_rows(root))

    ids: dict[str, list[str]] = {}
    addresses: dict[tuple[str, str, str, str], list[dict]] = {}
    titles: dict[tuple[str, str], list[str]] = {}
    aliases: dict[tuple[str, str], list[str]] = {}
    summaries: dict[str, list[str]] = {}
    placeholders = []
    for rel, version, entity_type, entry in rows:
        entity_id = entry["id"]
        ids.setdefault(entity_id, []).append(rel)
        address = entry.get("address")
        if isinstance(address, dict) and address.get("value") and address["value"] != "0x0" and entry.get("profile"):
            key = (version, entity_type, entry["profile"], address["value"])
            addresses.setdefault(key, []).append({"id": entity_id, "title": entry["title"], "width": entry.get("width")})
        titles.setdefault((version, re.sub(r"\s+", "", entry["title"])), []).append(entity_id)
        for alias in entry.get("aliases", []):
            aliases.setdefault((version, alias), []).append(entity_id)
        summary = entry.get("summary")
        if isinstance(summary, str) and len(summary.strip()) >= 20:
            summaries.setdefault(summary.strip(), []).append(entity_id)
        text = json.dumps(entry, ensure_ascii=False)
        for match in PLACEHOLDER.finditer(text):
            start = max(0, match.start() - 24)
            context = text[start:match.end() + 24].replace("\n", " ")
            placeholders.append({"id": entity_id, "token": match.group(0), "context": context})

    duplicate_ids = [entity_id for entity_id, files in sorted(ids.items()) if len(files) > 1]
    address_groups = [
        {"version": key[0], "entityType": key[1], "profile": key[2], "address": key[3],
         "entries": sorted(values, key=lambda item: item["id"])}
        for key, values in sorted(addresses.items()) if len(values) > 1
    ]
    title_groups = [
        {"version": key[0], "title": key[1], "ids": sorted(values)}
        for key, values in sorted(titles.items()) if len(values) > 1
    ]
    alias_groups = [
        {"version": key[0], "alias": key[1], "kind": "address-alias" if HEX_ALIAS.fullmatch(key[1]) else "generic-alias",
         "ids": sorted(values)}
        for key, values in sorted(aliases.items()) if len(values) > 1
    ]
    summary_groups = [
        {"summary": key, "ids": sorted(values)}
        for key, values in sorted(summaries.items()) if len(values) > 1
    ]

    source_paths: dict[str, list[str]] = {}
    for record in manifest:
        path = record.get("path")
        if isinstance(path, str):
            source_paths.setdefault(path, []).append(record.get("id", ""))
    duplicate_source_paths = [
        {"path": path, "ids": sorted(ids_list)}
        for path, ids_list in sorted(source_paths.items()) if len(ids_list) > 1
    ]

    duplicate_evidence, orphan_evidence = evidence_groups(root, referenced)
    plan_file = root / PLAN_PATH
    report = {
        "schemaVersion": 1,
        "generatedBy": "tools/consolidate_kb.py",
        "reviewDate": REVIEW_DATE,
        "baselineCommit": BASELINE_COMMIT,
        "counts": {
            "entities": len(rows),
            "structuredFiles": len(load_documents(root)),
            "duplicateIds": len(duplicate_ids),
            "sameProfileAddressGroups": len(address_groups),
            "duplicateTitleGroups": len(title_groups),
            "sharedAliasGroups": len(alias_groups),
            "templateSummaryGroups": len(summary_groups),
            "duplicateEvidenceGroups": len(duplicate_evidence),
            "orphanEvidence": len(orphan_evidence),
            "duplicateSourcePaths": len(duplicate_source_paths),
            "placeholderTerms": len(placeholders),
        },
        "plan": {
            "path": PLAN_PATH,
            "sha256": hashlib.sha256(plan_file.read_bytes()).hexdigest().upper() if plan_file.is_file() else None,
        },
        "duplicateIds": duplicate_ids,
        "sameProfileAddressGroups": address_groups,
        "duplicateTitleGroups": title_groups,
        "sharedAliasGroups": alias_groups,
        "templateSummaryGroups": summary_groups,
        "duplicateEvidence": duplicate_evidence,
        "orphanEvidence": orphan_evidence,
        "duplicateSourcePaths": duplicate_source_paths,
        "placeholderTerms": placeholders,
        "verifiedClaims": VERIFIED_CLAIMS,
        "notMerged": [
            {"reason": "跨画像同地址是不同样本的合法并存", "rule": "同一 value 但 profile 不同不合并"},
            {"reason": "来源 path 同名记录属于不同日期/用途的快照", "rule": "只报告，不合并 sourceRefs"},
            {"reason": "0x410A38 的四个实体分别是物理分派表、签名、模式、行为画像", "rule": "保留视图，补 120/126 边界"},
        ],
    }
    return report


def write_report(root: Path = ROOT) -> Path:
    path = root / REPORT_PATH
    path.write_text(json_text(build_report(root)), encoding="utf-8", newline="\n")
    return path


def check_report(root: Path = ROOT) -> int:
    path = root / REPORT_PATH
    expected = json_text(build_report(root)).encode("utf-8")
    if not path.is_file() or path.read_bytes() != expected:
        print("stale: " + REPORT_PATH)
        return 1
    print("consolidation_report_ok")
    return 0


def index_entities(root: Path):
    index: dict[str, tuple[Path, str, dict, dict]] = {}
    for rel, document in load_documents(root):
        for entry in document["entries"]:
            entity_id = entry["id"]
            if entity_id in index:
                raise ValueError(f"duplicate entity id: {entity_id}")
            index[entity_id] = (root / rel, rel, document, entry)
    return index


def apply_edit(entry: dict, edit: dict) -> None:
    for key, value in edit.get("set", {}).items():
        entry[key] = value
    if isinstance(edit.get("address"), dict):
        entry["address"] = edit["address"]
    for key in edit.get("removeFields", []):
        entry.pop(key, None)
    if edit.get("removeAliases"):
        remove = set(edit["removeAliases"])
        entry["aliases"] = [alias for alias in entry.get("aliases", []) if alias not in remove]
    if edit.get("addAliases"):
        aliases = entry.setdefault("aliases", [])
        for alias in edit["addAliases"]:
            if alias not in aliases:
                aliases.append(alias)
    if edit.get("addRelations"):
        relations = entry.setdefault("relations", [])
        for relation in edit["addRelations"]:
            if relation not in relations:
                relations.append(relation)
    if edit.get("addNotes"):
        notes = entry.setdefault("notes", [])
        for note in edit["addNotes"]:
            if note not in notes:
                notes.append(note)


def apply_plan(root: Path, plan_path: Path) -> list[str]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("schemaVersion") != 1 or plan.get("reviewDate") != REVIEW_DATE:
        raise ValueError("invalid consolidation plan envelope")
    if plan.get("baselineCommit") != BASELINE_COMMIT:
        raise ValueError("consolidation plan baseline differs")
    index = index_entities(root)
    changed: dict[Path, dict] = {}
    targets: list[str] = []
    for edit in plan.get("entityEdits", []):
        entity_id = edit.get("id")
        if entity_id not in index:
            raise ValueError(f"unknown entity id: {entity_id}")
        path, _, document, entry = index[entity_id]
        apply_edit(entry, edit)
        changed[path] = document
        targets.append(entity_id)
    for path, document in sorted(changed.items()):
        path.write_text(json_text(document), encoding="utf-8", newline="\n")

    referenced = referenced_evidence(load_manifest(root))
    pending = {path.replace("\\", "/") for path in plan.get("deleteFiles", [])}
    _, _ = evidence_groups(root, referenced, pending)
    for relative_path in sorted(pending):
        if not relative_path.startswith("sources/evidence/"):
            raise ValueError(f"refusing to delete outside evidence: {relative_path}")
        target = root / relative_path
        if not target.is_file():
            raise ValueError(f"missing evidence file: {relative_path}")
        if relative_path in referenced:
            raise ValueError(f"refusing to delete referenced evidence: {relative_path}")
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        twin = any(
            path.is_file() and path != target and hashlib.sha256(path.read_bytes()).hexdigest() == digest
            for path in (root / "sources" / "evidence").iterdir()
        )
        if not twin:
            raise ValueError(f"refusing to delete non-duplicate evidence: {relative_path}")
        target.unlink()
    write_report(root)
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audit", action="store_true", help="write the consolidation report")
    group.add_argument("--check", action="store_true", help="compare the committed report without writing")
    group.add_argument("--apply", type=Path, help="apply an explicit consolidation plan")
    args = parser.parse_args()
    if args.check:
        return check_report()
    if args.apply:
        targets = apply_plan(ROOT, args.apply)
        print(f"consolidation_applied entities={len(targets)}")
        return 0
    path = write_report()
    print(f"consolidation_audit {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
