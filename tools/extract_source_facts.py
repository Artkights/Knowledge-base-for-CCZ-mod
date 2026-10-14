from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the first-party source snapshot used by the knowledge base.")
    parser.add_argument("source_root", type=Path, help="Root containing the wrench, XiaoAn, and CCZModStudio source trees")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "sources" / "source-manifest.json").read_text(encoding="utf-8"))
    failures = []
    for entry in manifest["entries"]:
        path = args.source_root / Path(entry["path"])
        if not path.is_file():
            failures.append(f"missing {entry['id']}: {entry['path']}")
            continue
        actual = sha256(path)
        if actual != entry["sha256"]:
            failures.append(f"hash mismatch {entry['id']}: expected {entry['sha256']}, actual {actual}")
    if failures:
        print("source_verification_failed")
        for failure in failures:
            print("- " + failure)
        return 1
    print(f"source_verification_ok files={len(manifest['entries'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
