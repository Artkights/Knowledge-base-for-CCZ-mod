from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def canonical_entity(summary: dict, cache: dict[str, dict]) -> dict:
    path = summary["canonicalDataPath"]
    if path not in cache:
        cache[path] = json.loads((ROOT / path).read_text(encoding="utf-8"))
    return next(item for item in cache[path]["entries"] if item["id"] == summary["id"])


def score(summary: dict, query: str) -> int:
    needle = query.casefold()
    entity_id = summary["id"].casefold()
    title = summary["title"].casefold()
    terms = [str(value).casefold() for value in summary.get("searchTerms", [])]
    if needle == entity_id:
        return 100
    if needle == title:
        return 90
    if any(needle == value for value in terms):
        return 80
    if needle in title:
        return 70
    if any(needle in value for value in terms):
        return 50
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Query canonical CCZ engine entities.")
    parser.add_argument("query", help="Entity ID, address, title, alias, field, or semantic text")
    parser.add_argument("--version", help="Require an exact version, for example 6.5, 6.5pl, or 6.6")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--include-research", action="store_true")
    args = parser.parse_args()

    index = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
    ranked = []
    for summary in index["entries"]:
        if args.version and args.version not in summary.get("versions", []):
            continue
        value = score(summary, args.query)
        if value:
            ranked.append((value, summary))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    cache: dict[str, dict] = {}
    results = [{"score": value, "summary": summary, "entity": canonical_entity(summary, cache)} for value, summary in ranked[: max(0, args.limit)]]

    research_results = []
    if args.include_research:
        research = json.loads((ROOT / "research" / "research-gaps.json").read_text(encoding="utf-8"))
        needle = args.query.casefold()
        for item in research["entries"]:
            if args.version and args.version not in item.get("versions", []):
                continue
            haystack = json.dumps(item, ensure_ascii=False).casefold()
            if needle in haystack:
                research_results.append(item)
            if len(research_results) >= max(0, args.limit):
                break
    print(json.dumps({"query": args.query, "version": args.version, "results": results, "research": research_results}, ensure_ascii=False, indent=2))
    return 0 if results or research_results else 1


if __name__ == "__main__":
    raise SystemExit(main())
