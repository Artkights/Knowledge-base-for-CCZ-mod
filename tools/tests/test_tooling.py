from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_index
import build_reference
from generated_artifacts import differences
from validate_kb import entity_sha256, safe_relative_path, validate_sources, validate_integration_receipt
from version_config import DATA_VERSIONS, VERSIONS, data_paths


class ToolingContracts(unittest.TestCase):
    def test_versions_include_64_and_preserve_65pl_research_only(self):
        self.assertIn("6.4", DATA_VERSIONS)
        self.assertIn("6.5pl", VERSIONS)
        self.assertNotIn("6.5pl", DATA_VERSIONS)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for version in ("6.4", "6.5pl"):
                target = root / version / "data/test.json"
                target.parent.mkdir(parents=True)
                target.write_text("{}", encoding="utf-8")
            self.assertEqual(["6.4"], [path.relative_to(root).parts[0] for path in data_paths(root)])

    def test_snapshot_hash_and_path_are_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            snapshot = root / "evidence.json"
            snapshot.write_bytes(b"reviewed bytes")
            digest = hashlib.sha256(snapshot.read_bytes()).hexdigest().upper()
            source = {"id": "src.fixture", "path": "external/evidence.json", "sha256": digest,
                      "verification": {"kind": "repository-snapshot", "snapshotPath": "evidence.json", "sha256": digest}}
            errors = []
            validate_sources(errors, {"entries": [source]}, root)
            self.assertEqual([], errors)
            snapshot.write_bytes(b"corrupted")
            validate_sources(errors, {"entries": [source]}, root)
            self.assertTrue(any("hash mismatch" in message for message in errors))
            source["verification"]["snapshotPath"] = "../outside.json"
            errors = []
            validate_sources(errors, {"entries": [source]}, root)
            self.assertTrue(any("unsafe" in message for message in errors))

    def test_source_availability_cannot_be_implicit_or_duplicate(self):
        source = {"id": "src.fixture", "path": "unpublished.txt", "sha256": "A" * 64}
        errors = []
        validate_sources(errors, {"entries": [source, source]})
        self.assertTrue(any("duplicate" in message for message in errors))
        self.assertTrue(any("no explicit verification" in message for message in errors))
        source["verification"] = {"kind": "external-local", "reason": "Original bytes not included; identity only."}
        errors = []
        validate_sources(errors, {"entries": [source]})
        self.assertEqual([], errors)

    def test_absolute_and_traversal_paths_fail_on_all_platforms(self):
        for text in ("../secret", "safe/../../secret", "D" + ":" + "/secret", "/secret", "safe" + chr(92) + "file", "//host/share"):
            self.assertFalse(safe_relative_path(text), text)
        self.assertTrue(safe_relative_path("sources/证据.json"))

    def test_stale_generated_output_is_reported_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "output.md"
            target.write_bytes(b"old\n")
            self.assertEqual([target], differences({target: "new\n"}))
            self.assertEqual(b"old\n", target.read_bytes())
            self.assertEqual([], differences({target: "old\n"}))

    def test_generators_are_deterministic_and_do_not_write_during_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "6.4/data/profiles/example.json"
            target.parent.mkdir(parents=True)
            target.write_text(json.dumps({"schemaVersion": 1, "entityType": "engine-profile", "entries": [{
                "id": "profile.64.fixture", "title": "精确样本", "versions": ["6.4"], "status": "candidate", "evidence": "fixture", "sourceRefs": []
            }]}), encoding="utf-8")
            with patch.object(build_index, "ROOT", root), patch.object(build_reference, "ROOT", root), patch.object(build_reference, "DATA_ROOTS", [root / "6.4/data"]):
                first = build_index.generated_documents()
                self.assertEqual(first, build_index.generated_documents())
                reference, stale = build_reference.generated_documents()
                self.assertEqual((reference, stale), build_reference.generated_documents())
                self.assertEqual(1, len(json.loads(first[root / "index.json"])["entries"]))
                self.assertIn(root / "6.4/reference/profiles.md", reference)
                self.assertFalse((root / "index.json").exists())
                self.assertFalse((root / "6.4/reference").exists())

    def test_integration_receipt_detects_hash_status_path_and_coverage_tampering(self):
        entry = {"id": "profile.64.fixture", "status": "candidate", "title": "精确样本"}
        entities = {entry["id"]: {"entry": entry, "path": "6.4/data/profiles/fixture.json"}}
        record = {
            "id": entry["id"], "inputs": [{"input": "fixture-main", "entitySha256": entity_sha256(entry)}],
            "targetId": entry["id"], "targetPath": entities[entry["id"]]["path"],
            "targetStatus": entry["status"], "targetEntitySha256": entity_sha256(entry),
        }
        receipt = {"schemaVersion": 1, "records": [record], "inputUnionCount": 1,
                   "inputCounts": {"fixture-main": 1}, "finalEntityCount": 1,
                   "missingIds": [], "newEntityIds": []}
        errors = []
        validate_integration_receipt(errors, receipt, entities)
        self.assertEqual([], errors)
        for key, changed, expected in (
            ("targetEntitySha256", "F" * 64, "hash differs"),
            ("targetStatus", "canonical", "status differs"),
            ("targetPath", "6.5/data/profiles/fixture.json", "path differs"),
        ):
            with self.subTest(key=key):
                tampered = copy.deepcopy(receipt)
                tampered["records"][0][key] = changed
                errors = []
                validate_integration_receipt(errors, tampered, entities)
                self.assertTrue(any(expected in error for error in errors), errors)
        missing_record = copy.deepcopy(receipt)
        missing_record["records"] = []
        errors = []
        validate_integration_receipt(errors, missing_record, entities)
        self.assertTrue(any("inputUnionCount" in error for error in errors))
        errors = []
        validate_integration_receipt(errors, receipt, {})
        self.assertTrue(any("target entity missing" in error for error in errors))

    def test_integration_receipt_accounts_for_genuinely_new_entities(self):
        entry = {"id": "profile.64.new", "status": "candidate"}
        entities = {entry["id"]: {"entry": entry, "path": "6.4/data/profiles/new.json"}}
        receipt = {"schemaVersion": 1, "records": [], "inputUnionCount": 0, "inputCounts": {},
                   "finalEntityCount": 1, "missingIds": [], "newEntityIds": [entry["id"]]}
        errors = []
        validate_integration_receipt(errors, receipt, entities)
        self.assertEqual([], errors)
        receipt["newEntityIds"] = []
        validate_integration_receipt(errors, receipt, entities)
        self.assertTrue(any("newEntityIds" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
