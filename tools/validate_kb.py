from __future__ import annotations

import hashlib
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
ALLOWED_TOP = {"00-共性知识", "6.5", "6.5pl", "6.6", "90-来源归档", "tools"}
ALLOWED_ROOT_FILES = {".gitattributes", ".gitignore", "README.md", "llms.txt", "CONTRIBUTING.md", "NOTICE.md", "index.json"}
FORBIDDEN_EXTENSIONS = {".exe", ".dll", ".pdb", ".bin", ".obj", ".rar", ".zip", ".7z", ".doc", ".docx", ".xlsx", ".htm", ".html", ".log", ".tmp", ".bak"}
FORBIDDEN_PARTS = {"bin", "obj", "publish", "release", "_buildcheck", ".git-checkout", "__pycache__"}
SECTIONS = ["结论速览", "适用版本", "已确认事实", "实现/使用方法", "风险与边界", "证据来源", "待验证项"]
SPECIAL_FILES = {"README.md", "CONTRIBUTING.md", "NOTICE.md", "05-知识条目模板.md", "llms.txt"}


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def read_text(path: Path) -> str:
    data = read_bytes(path)
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return data.decode("utf-8", errors="replace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def markdown_links(text: str):
    pattern = re.compile(r"(!?)\[([^\]]+)\]\(([^)]+)\)")
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in pattern.finditer(line):
            if line[: match.start()].count("`") % 2 == 1:
                continue
            yield match.groups()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    errors: list[str] = []
    files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        parts = rel.split("/")
        if len(parts) == 1 and path.name not in ALLOWED_ROOT_FILES:
            fail(errors, f"unexpected root file: {rel}")
        if len(parts) > 1 and parts[0] not in ALLOWED_TOP:
            fail(errors, f"unexpected top-level path: {rel}")
        if path.suffix.lower() in FORBIDDEN_EXTENSIONS or any(part.lower() in FORBIDDEN_PARTS for part in parts):
            fail(errors, f"forbidden artifact: {rel}")
        if path.suffix.lower() in {".md", ".txt", ".csv"} and not read_bytes(path).startswith(b"\xef\xbb\xbf"):
            fail(errors, f"missing UTF-8 BOM: {rel}")
        if path.suffix.lower() in {".md", ".txt", ".csv", ".json"}:
            text = read_text(path)
            if re.search(r"(?:[A-Z]:[\\/]|/Users/|/home/|C:/Users/|F:/|D:\\Downloads)", text):
                fail(errors, f"local absolute path: {rel}")
            if re.search(r"(?i)(?:BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY|ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9]+)", text):
                fail(errors, f"secret-like value: {rel}")
            if path.suffix.lower() == ".md" and path.name not in SPECIAL_FILES and parts[0] not in {"90-来源归档"} and not ("资料与模板" in parts):
                missing = [section for section in SECTIONS if f"## {section}" not in text]
                if missing:
                    fail(errors, f"missing standard sections ({','.join(missing)}): {rel}")
            if path.suffix.lower() == ".md":
                for _, label, raw_target in markdown_links(text):
                    target = raw_target.strip().strip("<>")
                    if re.match(r"^(?:https?://|mailto:|#)", target, re.IGNORECASE):
                        continue
                    target_path = unquote(target.partition("#")[0]).replace("\\", "/")
                    if target_path and not (path.parent / target_path).exists():
                        fail(errors, f"broken local link in {rel}: {label} -> {raw_target}")
    manifest_path = ROOT / "90-来源归档" / "source-manifest.csv"
    if not manifest_path.exists():
        fail(errors, "source-manifest.csv is missing")
    else:
        with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        required = {"sourcePath", "destinationPath", "version", "topic", "evidenceLevel", "status", "sha256", "sourceType", "correctionNote"}
        if not rows or not required.issubset(rows[0]):
            fail(errors, "source-manifest.csv schema is invalid")
        seen_sources = set()
        canonical_destinations = set()
        for row in rows:
            source = row.get("sourcePath", "")
            destination = row.get("destinationPath", "")
            status = row.get("status", "")
            if source in seen_sources:
                fail(errors, f"duplicate manifest source: {source}")
            seen_sources.add(source)
            if status not in {"canonical", "source-only", "unverified", "deprecated", "excluded"}:
                fail(errors, f"invalid manifest status for {source}: {status}")
            if not re.fullmatch(r"[0-9A-F]{64}", row.get("sha256", "")):
                fail(errors, f"invalid manifest hash: {source}")
            if status in {"canonical", "unverified"}:
                if not destination or not (ROOT / destination).exists():
                    fail(errors, f"manifest destination missing: {source} -> {destination}")
                if destination in canonical_destinations:
                    fail(errors, f"duplicate canonical destination: {destination}")
                canonical_destinations.add(destination)
            elif destination:
                fail(errors, f"non-published manifest row has destination: {source}")
    index_path = ROOT / "index.json"
    if not index_path.exists():
        fail(errors, "index.json is missing")
    else:
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
            if index.get("schemaVersion") != 1 or not isinstance(index.get("entries"), list):
                fail(errors, "index.json schema is invalid")
            else:
                seen_paths = set()
                for entry in index["entries"]:
                    rel = entry.get("path", "")
                    if rel in seen_paths:
                        fail(errors, f"duplicate index path: {rel}")
                    seen_paths.add(rel)
                    target = ROOT / Path(rel)
                    if not target.exists():
                        fail(errors, f"index target missing: {rel}")
                    elif entry.get("sha256") != sha256(target):
                        fail(errors, f"index hash mismatch: {rel}")
                    if entry.get("version") == ["6.5"] and ("6.6" in rel.lower() or "6.5pl" in rel.lower()):
                        fail(errors, f"version leakage into 6.5: {rel}")
                public_paths = {
                    path.relative_to(ROOT).as_posix()
                    for path in files
                    if path.suffix.lower() in {".md", ".txt", ".json", ".csv"}
                    and path.name not in {"index.json", "source-manifest.csv"}
                }
                missing_index = sorted(public_paths - seen_paths)
                if missing_index:
                    fail(errors, "public files missing from index: " + " | ".join(missing_index))
        except (OSError, json.JSONDecodeError) as exc:
            fail(errors, f"index.json cannot be read: {exc}")
    normalized: dict[str, list[str]] = defaultdict(list)
    for path in files:
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        text = re.sub(r"<!--.*?-->", "", read_text(path), flags=re.DOTALL)
        text = re.sub(r"\s+", " ", text).strip().lower()
        if text:
            normalized[hashlib.sha256(text.encode("utf-8")).hexdigest()].append(path.relative_to(ROOT).as_posix())
    for group in normalized.values():
        if len(group) > 1:
            fail(errors, "duplicate normalized documents: " + " | ".join(group))
    titles: dict[str, list[str]] = defaultdict(list)
    line_sets: list[tuple[str, set[str]]] = []
    for path in files:
        if path.suffix.lower() != ".md" or path.name == "README.md":
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = re.sub(r"<!--.*?-->", "", read_text(path), flags=re.DOTALL)
        title_match = re.search(r"(?m)^#\s+(.+)$", text)
        if title_match:
            titles[title_match.group(1).strip()].append(rel)
        meaningful = {
            re.sub(r"\s+", " ", line).strip().lower()
            for line in text.splitlines()
            if len(line.strip()) >= 30 and not line.startswith("## ") and "来源文件未随公开知识库发布" not in line
        }
        if len(meaningful) >= 8:
            line_sets.append((rel, meaningful))
    for title, paths in titles.items():
        if len(paths) > 1:
            fail(errors, f"duplicate document title '{title}': " + " | ".join(paths))
    for index, (left_path, left_lines) in enumerate(line_sets):
        for right_path, right_lines in line_sets[index + 1 :]:
            size_ratio = min(len(left_lines), len(right_lines)) / max(len(left_lines), len(right_lines))
            if size_ratio < 0.9:
                continue
            similarity = len(left_lines & right_lines) / len(left_lines | right_lines)
            if similarity >= 0.92:
                fail(errors, f"near-duplicate documents ({similarity:.2f}): {left_path} | {right_path}")
    if errors:
        print("validation_failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"validation_ok files={len(files)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
