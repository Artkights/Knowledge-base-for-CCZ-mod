"""Exercise the public query CLI, including exact version isolation."""
from __future__ import annotations
import json
import subprocess
import sys
sys.dont_write_bytecode = True
from version_config import ROOT


def query(term: str, *arguments: str, expected_code: int | tuple[int, ...] = 0) -> dict:
    result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/query_kb.py"), term, *arguments],
                            cwd=ROOT, capture_output=True, encoding="utf-8")
    allowed = expected_code if isinstance(expected_code, tuple) else (expected_code,)
    if result.returncode not in allowed:
        raise AssertionError(f"query {term!r} returned {result.returncode}: {result.stderr}")
    return json.loads(result.stdout)


def main() -> int:
    index = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
    entities = {entry["id"]: entry for entry in index["entries"]}
    cases = [
        ("profile.ccz64.xisui.9112", "6.4", "engine-profile", "profile.ccz64.xisui.9112"),
        ("0x00508998", "6.4", "data-structure", "struct.64.xisui.active-effect-assignment"),
        ("0x004837C2", "6.5", "function", "fn.65.item-id-to-record"),
        ("0x14", "6.5", "script-command", "script.65.opcode-14"),
        ("mechanism.66.xiaoan.super-s", "6.6", "mechanism", "mechanism.66.xiaoan.super-s"),
        ("mechanism.65pl.reference-scanner-coverage-and-counterexamples", "6.5pl", "mechanism", "mechanism.65pl.reference-scanner-coverage-and-counterexamples"),
    ]
    for term, version, kind, expected in cases:
        payload = query(term, "--version", version, "--entity-type", kind, "--limit", "50")
        found = {value["summary"]["id"] for value in payload["results"]}
        assert expected in found, f"missing {expected} for {term}"
        assert all(version in value["summary"]["versions"] and value["summary"]["entityType"] == kind for value in payload["results"])
    # The public title query must find the same object as its stable ID.
    profile = entities["profile.ccz64.xisui.9112"]
    title = query(profile["title"], "--version", "6.4", "--canonical-only")
    assert title["results"][0]["summary"]["id"] == profile["id"]
    isolated = query(profile["id"], "--version", "6.5", "--entity-type", "engine-profile", expected_code=(0, 1))
    assert all(value["summary"]["id"] != profile["id"] for value in isolated["results"])

    guard = query("mechanism.65pl.reference-scanner-coverage-and-counterexamples", "--version", "6.5pl", "--canonical-only", expected_code=(0, 1))
    assert all(value["summary"]["status"] != "canonical" for value in guard["results"])

    print(f"query_smoke_ok scenarios={len(cases) + 3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
