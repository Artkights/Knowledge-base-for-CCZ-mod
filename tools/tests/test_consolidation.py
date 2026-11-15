from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import consolidate_kb  # noqa: E402


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ConsolidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "sources" / "evidence").mkdir(parents=True)
        dump(self.root / "sources" / "source-manifest.json", {"schemaVersion": 1, "entries": []})

    def tearDown(self) -> None:
        self.temp.cleanup()

    def add_document(self, relative: str, entity_type: str, entries: list[dict]) -> None:
        dump(self.root / relative, {"schemaVersion": 1, "entityType": entity_type, "entries": entries})

    def test_duplicate_ids_are_reported(self) -> None:
        entry = {"id": "fn.x", "title": "A", "versions": ["6.4"], "status": "candidate", "evidence": "static-verified"}
        self.add_document("6.4/data/functions/a.json", "function", [entry])
        self.add_document("6.5/data/functions/b.json", "function", [dict(entry)])
        report = consolidate_kb.build_report(self.root)
        self.assertEqual(report["duplicateIds"], ["fn.x"])

    def test_same_profile_address_groups(self) -> None:
        address = {"kind": "va", "value": "0x00400000", "profile": "p", "evidence": "static-verified"}
        base = {"versions": ["6.4"], "profile": "p", "status": "candidate", "evidence": "static-verified", "address": address}
        self.add_document("6.4/data/globals/a.json", "global", [
            dict(base, id="global.64.a", title="表 A"),
            dict(base, id="global.64.b", title="表 B"),
        ])
        report = consolidate_kb.build_report(self.root)
        self.assertEqual(len(report["sameProfileAddressGroups"]), 1)
        self.assertEqual(report["sameProfileAddressGroups"][0]["address"], "0x00400000")

    def test_apply_plan_is_idempotent_and_removes_fields(self) -> None:
        self.add_document("6.4/data/globals/a.json", "global", [{
            "id": "global.64.a", "title": "旧标题", "aliases": ["旧别名", "0x0040620A"],
            "versions": ["6.4"], "profile": "p", "status": "candidate", "evidence": "static-verified",
            "summary": "模板摘要", "address": {"kind": "va", "value": "0x00400000", "profile": "p", "evidence": "static-verified"},
        }])
        plan = {
            "schemaVersion": 1, "reviewDate": consolidate_kb.REVIEW_DATE,
            "baselineCommit": consolidate_kb.BASELINE_COMMIT,
            "entityEdits": [{
                "id": "global.64.a",
                "set": {"title": "新标题"},
                "removeFields": ["summary"],
                "removeAliases": ["0x0040620A"],
                "addAliases": ["新别名"],
                "addNotes": ["复核说明"],
                "reason": "test",
            }],
        }
        plan_path = self.root / "plan.json"
        plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        consolidate_kb.apply_plan(self.root, plan_path)
        first = (self.root / "6.4/data/globals/a.json").read_text(encoding="utf-8")
        entity = json.loads(first)["entries"][0]
        self.assertEqual(entity["title"], "新标题")
        self.assertNotIn("summary", entity)
        self.assertEqual(entity["aliases"], ["旧别名", "新别名"])
        self.assertEqual(entity["notes"], ["复核说明"])
        consolidate_kb.apply_plan(self.root, plan_path)
        self.assertEqual(first, (self.root / "6.4/data/globals/a.json").read_text(encoding="utf-8"))

    def test_refuses_to_delete_referenced_evidence(self) -> None:
        payload = b"same snapshot\n"
        keep = self.root / "sources/evidence/keep.txt"
        drop = self.root / "sources/evidence/drop.txt"
        keep.write_bytes(payload)
        drop.write_bytes(payload)
        dump(self.root / "sources" / "source-manifest.json", {
            "schemaVersion": 1,
            "entries": [{"id": "src.keep", "path": "sources/evidence/keep.txt", "sha256": "0" * 64}],
        })
        plan = {
            "schemaVersion": 1, "reviewDate": consolidate_kb.REVIEW_DATE,
            "baselineCommit": consolidate_kb.BASELINE_COMMIT,
            "entityEdits": [],
            "deleteFiles": ["sources/evidence/drop.txt", "sources/evidence/keep.txt"],
        }
        plan_path = self.root / "plan.json"
        plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        with self.assertRaises(ValueError):
            consolidate_kb.apply_plan(self.root, plan_path)


if __name__ == "__main__":
    unittest.main()
