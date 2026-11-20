from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BOM_EXTENSIONS = {".md", ".txt", ".csv"}
PLAIN_UTF8_EXTENSIONS = {".json", ".py"}


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in BOM_EXTENSIONS | PLAIN_UTF8_EXTENSIONS:
            continue
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            data = data[3:]
        text = data.decode("utf-8")
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        normalized = re.sub(r"[ \t]+$", "", normalized, flags=re.MULTILINE).rstrip() + "\n"
        output = normalized.encode("utf-8")
        if path.suffix.lower() in BOM_EXTENSIONS:
            output = b"\xef\xbb\xbf" + output
        if output != path.read_bytes():
            path.write_bytes(output)
            changed += 1
    print(f"formatted={changed}")


if __name__ == "__main__":
    main()
