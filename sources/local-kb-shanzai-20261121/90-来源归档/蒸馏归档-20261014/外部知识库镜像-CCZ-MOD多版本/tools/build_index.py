from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKIP_NAMES = {"index.json", "source-manifest.csv"}
SKIP_PARTS = {".git", ".git-checkout", "__pycache__"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def read_text(path: Path) -> str:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    return data.decode("utf-8", errors="replace")


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def metadata(text: str, key: str, default: str) -> str:
    match = re.search(rf"<!--\s*{re.escape(key)}:\s*(.*?)\s*-->", text, re.IGNORECASE)
    return match.group(1).strip() if match else default


def main() -> None:
    entries = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.name in SKIP_NAMES or any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".txt", ".json", ".csv"}:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path) if path.suffix.lower() in {".md", ".txt"} else ""
        parts = rel.split("/")
        if parts[0] in {"6.5", "6.5pl", "6.6"}:
            version = parts[0]
        elif parts[0] == "00-共性知识":
            version = "shared"
        elif parts[0] == "90-来源归档":
            version = "archive"
        else:
            version = "shared"
        title = first_heading(text, path.stem)
        topic = metadata(text, "topic", "general")
        status = metadata(text, "status", "canonical")
        evidence = metadata(text, "evidence", "source-reviewed")
        source = metadata(text, "source", "")
        entry_id = re.sub(r"[^a-z0-9]+", ".", f"{version}.{rel[:-len(path.suffix)]}".lower()).strip(".")
        entries.append(
            {
                "id": entry_id,
                "path": rel,
                "version": [version],
                "topic": topic,
                "title": title,
                "status": status,
                "evidenceLevel": evidence,
                "sourceRefs": [source] if source else [],
                "related": [],
                "sha256": sha256(path),
            }
        )
    payload = {"schemaVersion": 1, "generatedBy": "tools/build_index.py", "entries": entries}
    (ROOT / "index.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"indexed={len(entries)}")


if __name__ == "__main__":
    main()
