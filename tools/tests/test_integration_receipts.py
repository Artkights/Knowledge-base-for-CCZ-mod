from __future__ import annotations

import copy
from contextlib import redirect_stderr
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_integration_receipt import (current_entities, entities_at_commit, entity_hash, main,
                                       incremental_receipt, observation, refresh_current)
from validate_kb import (validate_incremental_receipt, validate_incremental_receipt_files,
                         validate_integration_receipt)


COMMIT = 'a' * 40
REVIEW_PATH = 'sources/data-manager-review-20261102.json'


def entity(entity_id: str, title: str = 'fact', status: str = 'candidate') -> dict:
    return {'entry': {'id': entity_id, 'title': title, 'status': status},
            'path': '6.5/data/structures/example.json'}


class IntegrationReceipts(unittest.TestCase):
    def setUp(self):
        self.baseline = {'struct.65.changed': entity('struct.65.changed'),
                         'struct.65.retained': entity('struct.65.retained')}
        self.final = copy.deepcopy(self.baseline)
        self.final['struct.65.changed']['entry']['title'] = 'reviewed fact'
        self.final['struct.65.added'] = entity('struct.65.added')
        self.review = {'schemaVersion': 1, 'reviewDate': '2026-11-02', 'baselineCommit': COMMIT,
                       'entries': [{'path': 'data-manager/source.json', 'sha256': 'B' * 64,
                                    'disposition': 'updated-entities',
                                    'targetIds': ['struct.65.changed', 'struct.65.added'],
                                    'reason': 'Review the current codec and its independent consumer.'}]}
        self.review_bytes = (json.dumps(self.review, ensure_ascii=False, indent=2) + '\n').encode()

    def make_receipt(self):
        return incremental_receipt(self.baseline, self.final, COMMIT, '2026-11-02', REVIEW_PATH, self.review_bytes)

    def validate(self, receipt, entities=None, review=None, review_bytes=None):
        errors = []
        validate_incremental_receipt(errors, receipt, self.final if entities is None else entities,
                                     review_document=self.review if review is None else review,
                                     review_bytes=self.review_bytes if review_bytes is None else review_bytes)
        return errors

    def test_incremental_receipt_classifies_full_union_and_is_deterministic(self):
        first = self.make_receipt()
        self.assertEqual({'added': 1, 'updated': 1, 'retained': 1}, first['actionCounts'])
        self.assertEqual(set(self.final), {item['id'] for item in first['records']})
        self.assertEqual(set(self.baseline), {item['id'] for item in first['baselineEntities']})
        self.assertEqual(first, self.make_receipt())
        self.assertEqual([], self.validate(first))
        self.assertEqual('Review the current codec and its independent consumer.', first['records'][0]['reason'])

    def test_historical_refresh_preserves_all_observations_and_is_idempotent(self):
        entity_id = 'struct.65.changed'
        historical = {'schemaVersion': 1, 'date': '2026-10-28',
                      'inputCounts': {'historical-main': 1}, 'inputUnionCount': 1,
                      'finalEntityCount': 2, 'newEntityIds': ['struct.65.retained'], 'missingIds': [],
                      'records': [{'id': entity_id, 'inputs': [{'input': 'historical-main', 'commit': 'c' * 40,
                                   'entitySha256': entity_hash(self.baseline[entity_id]['entry'])}],
                                   'targetId': entity_id, 'targetPath': self.baseline[entity_id]['path'],
                                   'targetStatus': 'candidate', 'targetEntitySha256': entity_hash(self.baseline[entity_id]['entry']),
                                   'action': 'retained-and-reviewed', 'reason': 'Historical reason.'}]}
        original = copy.deepcopy(historical)
        refreshed = refresh_current(historical, self.final)
        self.assertEqual(original, historical)
        for key in ('date', 'inputCounts', 'inputUnionCount'):
            self.assertEqual(original[key], refreshed[key])
        self.assertEqual(original['records'][0]['inputs'], refreshed['records'][0]['inputs'])
        self.assertEqual('Historical reason.', refreshed['records'][0]['reason'])
        self.assertEqual(3, refreshed['finalEntityCount'])
        self.assertEqual(entity_hash(self.final[entity_id]['entry']), refreshed['records'][0]['targetEntitySha256'])
        self.assertEqual(refreshed, refresh_current(refreshed, self.final))
        errors = []
        validate_integration_receipt(errors, refreshed, self.final)
        self.assertEqual([], errors)
        for entity_id in self.baseline:
            deleted = copy.deepcopy(self.final)
            del deleted[entity_id]
            with self.assertRaisesRegex(ValueError, 'disappeared'):
                refresh_current(historical, deleted)
        invalid = copy.deepcopy(historical)
        invalid['inputCounts']['historical-main'] = 2
        with self.assertRaisesRegex(ValueError, 'inputCounts'):
            refresh_current(invalid, self.final)

    def test_generation_and_validation_reject_disappearing_baseline_entity(self):
        receipt = self.make_receipt()
        del self.final['struct.65.changed']
        with self.assertRaisesRegex(ValueError, 'disappeared'):
            self.make_receipt()
        self.assertTrue(any('disappeared' in message for message in self.validate(receipt)))

    def test_before_after_action_and_union_tampering_are_detected(self):
        receipt = self.make_receipt()
        changed = next(record for record in receipt['records'] if record['action'] == 'updated')
        for field, value, expected in (
            ('before', None, 'before observation'), ('after', observation(self.baseline['struct.65.changed']), 'after observation'),
            ('action', 'retained', 'action differs'), ('reason', '', 'reason missing'),
        ):
            with self.subTest(field=field):
                tampered = copy.deepcopy(receipt)
                record = next(record for record in tampered['records'] if record['id'] == changed['id'])
                record[field] = value
                self.assertTrue(any(expected in message for message in self.validate(tampered)))
        for field in ('path', 'status', 'entitySha256'):
            with self.subTest(after_field=field):
                tampered = copy.deepcopy(receipt)
                tampered['records'][0]['after'][field] = 'tampered'
                self.assertTrue(any('after observation' in message for message in self.validate(tampered)))
        removed = copy.deepcopy(receipt)
        removed['records'].pop()
        self.assertTrue(any('union' in message for message in self.validate(removed)))
        duplicated = copy.deepcopy(receipt)
        duplicated['records'].append(copy.deepcopy(duplicated['records'][0]))
        self.assertTrue(any('duplicate' in message for message in self.validate(duplicated)))
        tampered = copy.deepcopy(receipt)
        tampered['baselineEntities'][0]['entitySha256'] = 'F' * 64
        self.assertTrue(any('baseline observation hash differs' in message for message in self.validate(tampered)))

    def test_changed_entities_require_document_review_and_safe_metadata(self):
        incomplete = copy.deepcopy(self.review)
        incomplete['entries'][0]['targetIds'] = ['struct.65.changed']
        payload = (json.dumps(incomplete) + '\n').encode()
        with self.assertRaisesRegex(ValueError, 'lack source/document review'):
            incremental_receipt(self.baseline, self.final, COMMIT, '2026-11-02', REVIEW_PATH, payload)
        receipt = self.make_receipt()
        self.assertTrue(any('hash differs' in message for message in self.validate(receipt, review_bytes=b'altered')))
        wrong_meta = copy.deepcopy(self.review)
        wrong_meta['baselineCommit'] = 'b' * 40
        self.assertTrue(any('metadata differs' in message for message in self.validate(receipt, review=wrong_meta)))
        wrong_target = copy.deepcopy(self.review)
        wrong_target['entries'][0]['targetIds'].append('struct.65.missing')
        self.assertTrue(any('target entity missing' in message for message in self.validate(receipt, review=wrong_target)))
        with self.assertRaisesRegex(ValueError, 'safe repository-relative'):
            incremental_receipt(self.baseline, self.final, COMMIT, '2026-11-02', '../review.json', self.review_bytes)

    def test_review_can_be_loaded_offline_and_survives_crlf_checkout(self):
        receipt = self.make_receipt()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / REVIEW_PATH
            path.parent.mkdir(parents=True)
            path.write_bytes(self.review_bytes.replace(b'\n', b'\r\n'))
            errors = []
            validate_incremental_receipt(errors, receipt, self.final, root=root)
            self.assertEqual([], errors)
            path.write_bytes(b'corrupt')
            errors = []
            validate_incremental_receipt(errors, receipt, self.final, root=root)
            self.assertTrue(any('invalid incremental document review' in message for message in errors))

    def test_baseline_is_read_from_exact_git_objects_without_workspace_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / '6.5/data/structures/example.json'
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({'entries': [self.final['struct.65.changed']['entry']]}), encoding='utf-8')
            baseline_bytes = json.dumps({'entries': [self.baseline['struct.65.changed']['entry']]}).encode()
            # Freeze the Git transport responses independently from the changed
            # workspace file; all reads after ref resolution must use that SHA.
            with patch('build_integration_receipt.subprocess.check_output',
                       side_effect=[(COMMIT + '\n').encode(), b'6.5/data/structures/example.json\0', baseline_bytes]) as git:
                commit, baseline = entities_at_commit(root, 'HEAD')
                self.assertEqual(['git', 'show', COMMIT + ':6.5/data/structures/example.json'], git.call_args_list[-1].args[0])
            self.assertEqual(COMMIT, commit)
            self.assertEqual({'struct.65.changed': self.baseline['struct.65.changed']}, baseline)
            self.assertEqual(self.final['struct.65.changed'], current_entities(root)['struct.65.changed'])

    def test_incremental_historical_date_is_rejected_before_reads_or_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'sources/integration-20261028.json'
            path.parent.mkdir(parents=True)
            original = b'{"historical": "must stay frozen"}\n'
            path.write_bytes(original)
            argv = ['build_integration_receipt.py', '--refresh-current', '--incremental-from', COMMIT,
                    '--date', '2026-10-28', '--document-review', REVIEW_PATH]
            with patch('build_integration_receipt.ROOT', root), patch.object(sys, 'argv', argv), \
                    patch('build_integration_receipt.current_entities') as reader, redirect_stderr(io.StringIO()) as stderr:
                with self.assertRaises(SystemExit) as failure:
                    main()
                self.assertEqual(2, failure.exception.code)
                self.assertIn('overwrite the frozen historical receipt', stderr.getvalue())
                reader.assert_not_called()
            self.assertEqual(original, path.read_bytes())
            self.assertEqual([path], list((root / 'sources').iterdir()))

    def test_dated_receipts_cannot_hide_behind_missing_wrong_type_or_date(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'sources/integration-20261102.json'
            path.parent.mkdir(parents=True)
            for value in ({'date': '2026-11-02'}, {'receiptType': 'incremetal', 'date': '2026-11-02'}, []):
                with self.subTest(value=value):
                    path.write_text(json.dumps(value), encoding='utf-8')
                    errors = []
                    validate_incremental_receipt_files(errors, self.final, root)
                    self.assertTrue(any('must declare receiptType incremental' in message for message in errors))
            path.write_text(json.dumps({'receiptType': 'incremental', 'date': '2026-11-03'}), encoding='utf-8')
            errors = []
            validate_incremental_receipt_files(errors, self.final, root)
            self.assertTrue(any('date differs from filename' in message for message in errors))
            review = root / REVIEW_PATH
            review.write_bytes(self.review_bytes)
            path.write_text(json.dumps(self.make_receipt()), encoding='utf-8')
            errors = []
            validate_incremental_receipt_files(errors, self.final, root)
            self.assertEqual([], errors)


if __name__ == '__main__':
    unittest.main()
