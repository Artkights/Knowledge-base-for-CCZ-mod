from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import import_local_kb_snapshot as importer
from validate_kb import is_scanned_text


class LocalKbSnapshotContracts(unittest.TestCase):
    def test_text_scan_covers_htm_csv_and_backup_snapshots(self):
        self.assertTrue(is_scanned_text(Path("post.htm")))
        self.assertTrue(is_scanned_text(Path("post.html")))
        self.assertTrue(is_scanned_text(Path("table.csv")))
        self.assertTrue(is_scanned_text(Path("record.md.bak_20261116")))
        self.assertFalse(is_scanned_text(Path("binary.exe")))

    def test_sanitizer_masks_drive_and_user_paths_and_normalizes_lf(self):
        drive = "C" + ":\\Users\\Example\\file.txt\r\n"
        unix = "/" + "home/example/file.txt"
        text, drive_count, user_count = importer.sanitize_text(drive + unix)
        self.assertEqual(1, drive_count)
        self.assertEqual(1, user_count)
        self.assertNotIn("\r", text)
        self.assertIn("[本地盘]\\Users\\Example", text)
        self.assertIn("[用户目录]/example", text)

    def test_classify_rejects_forbidden_binaries_and_artifacts(self):
        self.assertEqual("text", importer.classify(Path("note.md")))
        self.assertEqual("text", importer.classify(Path("record.md.bak_20261116")))
        self.assertEqual("binary", importer.classify(Path("manual.docx")))
        self.assertEqual("artifact", importer.classify(Path("cache.pyc")))
        self.assertEqual("artifact", importer.classify(Path(".gitattributes")))

    def test_stable_id_is_deterministic(self):
        used: set[str] = set()
        first = importer.stable_id("src.example", "a/b.md", used)
        second = importer.stable_id("src.example", "a/b.md", set())
        self.assertEqual(first, second)
        self.assertRegex(first, r"^src\.example\.[0-9A-F]{8}$")


if __name__ == "__main__":
    unittest.main()
