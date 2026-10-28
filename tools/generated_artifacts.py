"""Compare generated UTF-8/LF output without mutating stale files."""
from pathlib import Path


def differences(expected: dict[Path, str], stale: set[Path] | None = None) -> list[Path]:
    changed = [path for path, content in expected.items()
               if not path.is_file() or path.read_bytes() != content.encode("utf-8")]
    return sorted(set(changed) | (stale or set()))


def update(expected: dict[Path, str], stale: set[Path] | None = None) -> None:
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
    for path in stale or set():
        path.unlink()
