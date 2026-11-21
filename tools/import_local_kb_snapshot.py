"""Import a local knowledge-base tree as a sanitized, hashed source snapshot.

The tool is deliberately split from the manifest so every import stays auditable:
``--audit`` is read-only, ``--apply`` writes the snapshot/receipt/coverage/fragment,
and ``--check`` verifies an already generated snapshot against its fragment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parent.parent
TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".htm", ".html", ".json", ".py"}
FORBIDDEN_EXTENSIONS = {
    ".doc", ".docx", ".xls", ".xlsx", ".rar", ".zip", ".7z",
    ".exe", ".dll", ".pdb", ".bin", ".obj", ".log", ".bak", ".tmp",
}
ARTIFACT_NAMES = {".gitattributes"}
ARTIFACT_SUFFIXES = {".pyc"}

DRIVE_RE = re.compile(r"\b([A-Za-z]):([\\/])")
USER_RE = re.compile(r"(?<![A-Za-z0-9])/(Users|home)(?=/|[\\])")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sanitize_text(text: str) -> tuple[str, int, int]:
    drive_count = 0
    user_count = 0

    def repl_drive(match: re.Match) -> str:
        nonlocal drive_count
        drive_count += 1
        return "[本地盘]" + match.group(2)

    def repl_user(match: re.Match) -> str:
        nonlocal user_count
        user_count += 1
        return "[用户目录]"

    text = DRIVE_RE.sub(repl_drive, text)
    text = USER_RE.sub(repl_user, text)
    text = normalize_newlines(text)
    text = "\n".join(line.rstrip(" \t") for line in text.split("\n"))
    return text, drive_count, user_count


def decode_text(data: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", data, 0, len(data), "not UTF-8 or GB18030")


def classify(rel: Path) -> str:
    name = rel.name
    lower = name.lower()
    if name in ARTIFACT_NAMES or lower.endswith(tuple(ARTIFACT_SUFFIXES)):
        return "artifact"
    if ".bak_" in lower:
        base_suffix = Path(lower.split(".bak_", 1)[0]).suffix
        if base_suffix in TEXT_EXTENSIONS:
            return "text"
    suffix = Path(lower).suffix
    if suffix in TEXT_EXTENSIONS:
        return "text"
    if suffix in FORBIDDEN_EXTENSIONS:
        return "binary"
    return "other"


def stable_id(prefix: str, key: str, used: set[str]) -> str:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest().upper()
    for length in (8, 12, 16, 24):
        candidate = f"{prefix}.{digest[:length]}"
        if candidate not in used:
            used.add(candidate)
            return candidate
    raise RuntimeError("stable id collision")


def manifest_entries(manifest_path: Path) -> list[dict]:
    if not manifest_path.is_file():
        return []
    document = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    return document.get("entries", [])


def existing_snapshot_hashes(entries: list[dict], prefix: str) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for entry in entries:
        verification = entry.get("verification", {})
        if verification.get("kind") != "repository-snapshot":
            continue
        snapshot_path = str(verification.get("snapshotPath", ""))
        if not snapshot_path.startswith(prefix + "/"):
            continue
        digest = str(verification.get("sha256", ""))
        if digest:
            hashes[digest] = snapshot_path
    return hashes


def read_excluded_receipt(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    document = json.loads(path.read_text(encoding="utf-8-sig"))
    excluded = document.get("excluded", [])
    return excluded if isinstance(excluded, list) else []


def resolve_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    for base in (REPO, REPO.parent):
        candidate = base / path
        if candidate.exists():
            return candidate
    return REPO / path


def build_plan(args: argparse.Namespace) -> dict:
    source_root = resolve_path(args.source)
    snapshot_root = REPO / args.snapshot_prefix
    existing_root = REPO / args.existing_snapshot
    manifest_path = REPO / args.manifest
    receipt_path = REPO / args.existing_snapshot_receipt

    if not source_root.is_dir():
        raise SystemExit(f"source root not found: {source_root}")

    manifest = manifest_entries(manifest_path)
    manifest_by_path = {entry.get("path"): entry for entry in manifest if entry.get("path")}
    snapshot_hashes = existing_snapshot_hashes(manifest, args.existing_snapshot)
    existing_snapshot_paths = {
        path.relative_to(existing_root).as_posix()
        for path in existing_root.rglob("*")
        if path.is_file()
    } if existing_root.is_dir() else set()
    local_paths = {
        path.relative_to(source_root).as_posix()
        for path in source_root.rglob("*")
        if path.is_file()
    }

    new_text: list[dict] = []
    binaries: dict[str, dict] = {}
    artifacts: list[dict] = []
    other: list[dict] = []
    deduped: list[dict] = []
    already_snapshot: list[str] = []
    already_manifest: list[str] = []

    for rel_text in sorted(local_paths):
        rel = Path(rel_text)
        kind = classify(rel)
        manifest_key = f"{args.source.rstrip('/')}/{rel_text}"
        if kind == "artifact":
            artifacts.append({
                "path": rel_text,
                "reason": "非知识产物，不进入来源清单。",
            })
            continue
        if kind == "other":
            other.append({
                "path": rel_text,
                "reason": "未知扩展名，未纳入快照。",
                "sha256": sha256_bytes((source_root / rel).read_bytes()),
            })
            continue

        data = (source_root / rel).read_bytes()
        original_hash = sha256_bytes(data)

        if kind == "binary":
            if manifest_key in manifest_by_path:
                already_manifest.append(rel_text)
                continue
            binaries.setdefault(original_hash, {
                "path": rel_text,
                "sha256": original_hash,
                "size": len(data),
            })
            continue

        if rel_text in existing_snapshot_paths:
            already_snapshot.append(rel_text)
            continue
        existing = manifest_by_path.get(manifest_key)
        refresh_id = None
        if existing is not None:
            existing_snapshot = str(existing.get("verification", {}).get("snapshotPath", ""))
            if existing_snapshot.startswith(args.snapshot_prefix + "/"):
                refresh_id = existing["id"]
            else:
                already_manifest.append(rel_text)
                continue

        text, encoding = decode_text(data)
        sanitized, drive_count, user_count = sanitize_text(text)
        sanitized_bytes = sanitized.encode("utf-8")
        sanitized_hash = sha256_bytes(sanitized_bytes)
        if sanitized_hash in snapshot_hashes:
            deduped.append({
                "path": rel_text,
                "matchingSnapshotPath": snapshot_hashes[sanitized_hash],
                "sanitizedSha256": sanitized_hash,
            })
            continue

        new_text.append({
            "path": rel_text,
            "refresh_id": refresh_id,
            "encoding": encoding,
            "originalSha256": original_hash,
            "sanitizedSha256": sanitized_hash,
            "normalizedSha256": sha256_bytes(sanitized_bytes.replace(b"\r\n", b"\n")),
            "replacements": {"drivePrefix": drive_count, "userDirectory": user_count},
        })

    excluded_receipt = read_excluded_receipt(receipt_path)
    identity_only: dict[str, dict] = {}
    for item in excluded_receipt:
        digest = str(item.get("sha256", ""))
        if not digest:
            continue
        identity_only.setdefault(digest, {
            "path": str(item.get("path", "")),
            "sha256": digest,
            "reason": str(item.get("reason", "禁扩展名，不随仓库发布；仅登记身份与哈希。")),
        })

    used_ids: set[str] = {entry.get("id") for entry in manifest if entry.get("id")}
    fragment_entries: list[dict] = []
    text_entries: list[dict] = []

    for item in new_text:
        rel = item["path"]
        source_id = item.get("refresh_id") or stable_id(f"src.local-kb-workspace-{args.date}", rel, used_ids)
        verification = {
            "kind": "repository-snapshot",
            "snapshotPath": f"{args.snapshot_prefix}/{rel}",
            "sha256": item["sanitizedSha256"],
            "normalizedSha256": item["normalizedSha256"],
        }
        if item["originalSha256"] != item["sanitizedSha256"]:
            verification["reason"] = "快照已掩去本机盘符/用户目录特征并统一 LF；item.sha256 保留原件哈希。"
        entry = {
            "id": source_id,
            "path": f"{args.source.rstrip('/')}/{rel}",
            "sha256": item["originalSha256"],
            "sourceType": "local-knowledge-document",
            "usedFor": "本地工作区知识库文本快照（已净化本机路径并统一 LF）",
            "published": True,
            "verification": verification,
        }
        fragment_entries.append(entry)
        text_entries.append({"id": source_id, **item})

    for digest, item in sorted(binaries.items()):
        if digest in identity_only:
            identity_only[digest]["reason"] += f" 同一内容亦见于本地文件 {args.source.rstrip('/')}/{item['path']}。"
            continue
        existing = manifest_by_path.get(f"{args.source.rstrip('/')}/{item['path']}")
        if existing is not None and existing.get("verification", {}).get("kind") == "external-local":
            source_id = existing["id"]
        else:
            source_id = stable_id(f"src.local-kb-workspace-binary-{args.date}", item["path"], used_ids)
        fragment_entries.append({
            "id": source_id,
            "path": f"{args.source.rstrip('/')}/{item['path']}",
            "sha256": item["sha256"],
            "sourceType": "technical-document",
            "usedFor": "本地工作区原始文档（禁扩展名，不随仓库发布；仅登记哈希）",
            "published": False,
            "verification": {
                "kind": "external-local",
                "reason": "仓库禁扩展名（doc/docx/xlsx/rar 等），原件仅存于贡献者本地；登记 SHA256 供复核。",
            },
        })

    for digest, item in sorted(identity_only.items()):
        existing = manifest_by_path.get(item["path"])
        if existing is not None and existing.get("verification", {}).get("kind") == "identity-only":
            source_id = existing["id"]
        else:
            source_id = stable_id(f"src.local-kb-snapshot-excluded-{args.date}", item["path"], used_ids)
        fragment_entries.append({
            "id": source_id,
            "path": item["path"],
            "sha256": item["sha256"],
            "sourceType": "technical-document",
            "usedFor": "2026-11-21 快照排除的原始文档（禁扩展名；仅登记身份与哈希）",
            "published": False,
            "verification": {
                "kind": "identity-only",
                "reason": item["reason"],
            },
        })

    fragment = {
        "schemaVersion": 1,
        "generatedBy": "tools/import_local_kb_snapshot.py",
        "date": args.date,
        "sourceRoot": args.source,
        "snapshotPrefix": args.snapshot_prefix,
        "entries": sorted(fragment_entries, key=lambda entry: entry["id"]),
    }
    coverage = {
        "schemaVersion": 1,
        "date": args.date,
        "sourceRoot": args.source,
        "snapshotPrefix": args.snapshot_prefix,
        "localFileCount": len(local_paths),
        "inExistingSnapshotByPath": len(already_snapshot),
        "inManifestByPath": len(already_manifest),
        "newTextFiles": len(text_entries),
        "newTextFilePaths": [item["path"] for item in text_entries],
        "dedupedBySha256": len(deduped),
        "deduped": deduped,
        "forbiddenBinaries": len(binaries),
        "forbiddenBinaryPaths": [item["path"] for _, item in sorted(binaries.items())],
        "excludedArtifacts": artifacts,
        "excludedOther": other,
        "snapshotOnlyFiles": len(existing_snapshot_paths - local_paths),
        "snapshotExcludedBinaries": len(identity_only),
        "existingSnapshotReceipt": args.existing_snapshot_receipt,
    }
    receipt = {
        "schemaVersion": 1,
        "receiptType": "local-kb-workspace-snapshot",
        "date": args.date,
        "sourceRoot": args.source,
        "snapshotPrefix": args.snapshot_prefix,
        "documentCount": len(local_paths),
        "publishedTextCount": len(text_entries),
        "excludedBinaryCount": len(binaries),
        "excludedArtifactCount": len(artifacts),
        "alreadyCoveredBySnapshot": len(already_snapshot),
        "alreadyCoveredByEvidence": len(already_manifest),
        "dedupedBySha256": len(deduped),
        "sanitizedTextCount": sum(
            1 for item in text_entries
            if item["replacements"]["drivePrefix"]
            or item["replacements"]["userDirectory"]
            or item["encoding"] != "utf-8-sig"
        ),
        "encodingConverted": [item["path"] for item in text_entries if item["encoding"] != "utf-8-sig"],
        "excluded": [
            {"path": item["path"], "reason": item["reason"]} for item in artifacts + other
        ] + [
            {"path": f"{args.source.rstrip('/')}/{item['path']}", "reason": "仓库禁扩展名，原件不随仓库发布。", "sha256": item["sha256"]}
            for _, item in sorted(binaries.items())
        ],
        "entries": text_entries,
        "stripTrailingWhitespace": True,
        "note": "不修改历史快照回执；本回执只记录本轮工作区快照。",
    }
    return {
        "source_root": source_root,
        "snapshot_root": snapshot_root,
        "fragment": fragment,
        "coverage": coverage,
        "receipt": receipt,
        "new_text": new_text,
    }


def write_outputs(args: argparse.Namespace, plan: dict) -> None:
    snapshot_root: Path = plan["snapshot_root"]
    source_root: Path = plan["source_root"]
    for item in plan["new_text"]:
        text, _ = decode_text((source_root / item["path"]).read_bytes())
        sanitized, _, _ = sanitize_text(text)
        destination = snapshot_root / item["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(sanitized.encode("utf-8"))

    outputs = [
        (REPO / args.output_manifest_fragment, plan["fragment"]),
        (REPO / args.output_coverage, plan["coverage"]),
        (REPO / args.output_receipt, plan["receipt"]),
    ]
    for path, document in outputs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print("wrote", path.relative_to(REPO).as_posix())


def check_outputs(args: argparse.Namespace) -> int:
    fragment_path = REPO / args.output_manifest_fragment
    if not fragment_path.is_file():
        print("missing fragment:", fragment_path)
        return 1
    fragment = json.loads(fragment_path.read_text(encoding="utf-8"))
    manifest = manifest_entries(REPO / args.manifest)
    by_id = {entry.get("id"): entry for entry in manifest}
    errors = 0
    for entry in fragment.get("entries", []):
        source_id = entry.get("id")
        if source_id not in by_id:
            print("manifest entry missing:", source_id)
            errors += 1
            continue
        verification = entry.get("verification", {})
        if verification.get("kind") != "repository-snapshot":
            continue
        target = REPO / verification["snapshotPath"]
        if not target.is_file():
            print("snapshot missing:", target)
            errors += 1
            continue
        data = target.read_bytes()
        if sha256_bytes(data) != verification.get("sha256"):
            print("snapshot hash mismatch:", target)
            errors += 1
    print("check_errors=", errors)
    return int(bool(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="工具整合包/本地知识库")
    parser.add_argument("--snapshot-prefix", default="sources/local-kb-workspace-20261121")
    parser.add_argument("--date", default="2026-11-21")
    parser.add_argument("--existing-snapshot", default="sources/local-kb-shanzai-20261121")
    parser.add_argument("--existing-snapshot-receipt", default="sources/local-kb-snapshot-receipt-2026-11-21.json")
    parser.add_argument("--manifest", default="sources/source-manifest.json")
    parser.add_argument("--output-manifest-fragment", default="sources/local-kb-workspace-manifest-20261121.json")
    parser.add_argument("--output-coverage", default="sources/local-kb-coverage-20261121.json")
    parser.add_argument("--output-receipt", default="sources/local-kb-workspace-snapshot-receipt-2026-11-21.json")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        return check_outputs(args)

    plan = build_plan(args)
    if args.audit:
        print(json.dumps(plan["coverage"], ensure_ascii=False, indent=2))
        return int(plan["coverage"]["newTextFiles"] > 0)

    if args.apply:
        write_outputs(args, plan)
        print(json.dumps({
            "newTextFiles": plan["coverage"]["newTextFiles"],
            "forbiddenBinaries": plan["coverage"]["forbiddenBinaries"],
            "excludedArtifacts": len(plan["coverage"]["excludedArtifacts"]),
            "dedupedBySha256": plan["coverage"]["dedupedBySha256"],
            "snapshotExcludedBinaries": plan["coverage"]["snapshotExcludedBinaries"],
        }, ensure_ascii=False, indent=2))
        return 0

    parser.error("choose --audit, --apply or --check")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
