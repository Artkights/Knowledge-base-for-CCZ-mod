"""Record stable-ID coverage for historical imports and incremental reviews.

This is a historical import command, not a network or source-workspace CI step.
CI can validate the recorded final hashes without fetching historical branches.
"""
from __future__ import annotations

import argparse
import copy
from datetime import date
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORICAL_RECEIPT = 'sources/integration-20261028.json'
INPUTS = {
    'main': 'b2c60c6b1f2b0e565fb69ababc19fd4aa924e86b',
    'codex/item-consumable-knowledge-20261020': '76da41a3f5e406a8ad70ff27e7ddbf37c3547d24',
    'dsh/6.6-item-restore-chain': 'a6347d5f39034c56f5e98399d3b0fef267cf9e05',
    'dsh/6.6-20261027-batch': '2559999830ac84fc2454cd9c1cac0afbb66b162a',
}


def entity_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest().upper()


def current_entities(root: Path) -> dict:
    result = {}
    for version in ('6.4', '6.5', '6.6', 'legacy'):
        for path in sorted((root / version / 'data').rglob('*.json')):
            doc = json.loads(path.read_text(encoding='utf-8-sig'))
            for entry in doc['entries']:
                if entry['id'] in result:
                    raise ValueError('duplicate input ID: ' + entry['id'])
                result[entry['id']] = {'entry': entry, 'path': path.relative_to(root).as_posix()}
    return result


def refresh_current(receipt: dict, final: dict) -> dict:
    """Refresh final targets, without rewriting any frozen input observation."""
    result = copy.deepcopy(receipt)
    records = result['records']
    input_ids = {record['id'] for record in records}
    previous_ids = input_ids | set(result['newEntityIds'])
    missing = sorted(previous_ids - set(final))
    if missing:
        raise ValueError('previous integration entities disappeared: ' + ', '.join(missing))
    if len(input_ids) != len(records) or result['inputUnionCount'] != len(input_ids):
        raise ValueError('historical input coverage is inconsistent')
    observed_counts: dict[str, int] = {}
    for record in records:
        observations = record.get('inputs', [])
        if not observations or len({item['input'] for item in observations}) != len(observations):
            raise ValueError('historical input observations are inconsistent: ' + record['id'])
        for observation in observations:
            name = observation['input']
            observed_counts[name] = observed_counts.get(name, 0) + 1
        target_id = record.get('targetId', record['id'])
        if target_id not in final:
            raise ValueError('previous integration target disappeared: ' + target_id)
        item = final[target_id]
        record['targetPath'] = item['path']
        record['targetStatus'] = item['entry']['status']
        record['targetEntitySha256'] = entity_hash(item['entry'])
    if observed_counts != result['inputCounts']:
        raise ValueError('historical inputCounts differs from frozen observations')
    result['finalEntityCount'] = len(final)
    result['newEntityIds'] = sorted(set(final) - input_ids)
    result['missingIds'] = []
    return result


def entities_at_commit(root: Path, revision: str) -> tuple[str, dict]:
    """Read exact Git objects; the incremental operation never fetches history."""
    commit = subprocess.check_output(['git', 'rev-parse', '--verify', revision + '^{commit}'], cwd=root).decode().strip()
    paths = subprocess.check_output(['git', 'ls-tree', '-rz', '--name-only', commit], cwd=root).decode('utf-8').split('\0')
    result = {}
    for path in paths:
        parts = path.split('/')
        if len(parts) < 3 or parts[0] not in ('6.4', '6.5', '6.6', 'legacy') or parts[1] != 'data' or not path.endswith('.json'):
            continue
        raw = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=root)
        for entry in json.loads(raw.decode('utf-8-sig'))['entries']:
            if entry['id'] in result:
                raise ValueError('duplicate baseline ID: ' + entry['id'])
            result[entry['id']] = {'entry': entry, 'path': path}
    return commit, result


def observation(item: dict) -> dict:
    return {'path': item['path'], 'status': item['entry']['status'], 'entitySha256': entity_hash(item['entry'])}


def incremental_receipt(baseline: dict, final: dict, commit: str, review_date: str,
                        review_path: str, review_bytes: bytes) -> dict:
    """Create a self-contained, deterministic before/after receipt."""
    from validate_kb import safe_relative_path, validate_incremental_receipt
    if date.fromisoformat(review_date).isoformat() != review_date:
        raise ValueError('incremental date must use YYYY-MM-DD')
    if not safe_relative_path(review_path):
        raise ValueError('document review path must be a safe repository-relative path')
    missing = sorted(set(baseline) - set(final))
    if missing:
        raise ValueError('baseline entities disappeared: ' + ', '.join(missing))
    review = json.loads(review_bytes.decode('utf-8-sig'))
    reasons: dict[str, list[str]] = {}
    for entry in review.get('entries', []):
        for entity_id in entry.get('targetIds', []):
            if entry.get('reason'):
                reasons.setdefault(entity_id, []).append(entry['reason'])
    records = []
    counts = {'added': 0, 'updated': 0, 'retained': 0}
    for entity_id in sorted(final):
        before = observation(baseline[entity_id]) if entity_id in baseline else None
        after = observation(final[entity_id])
        action = 'added' if before is None else ('retained' if before == after else 'updated')
        counts[action] += 1
        reason = '；'.join(dict.fromkeys(reasons.get(entity_id, []))) if action != 'retained' else '与固定基线的实体内容、路径和状态一致。'
        records.append({'id': entity_id, 'action': action, 'before': before, 'after': after, 'reason': reason})
    baseline_entities = [{'id': entity_id, **observation(baseline[entity_id])} for entity_id in sorted(baseline)]
    result = {
        'schemaVersion': 1, 'receiptType': 'incremental', 'date': review_date,
        'baselineCommit': commit, 'baselineEntityCount': len(baseline),
        'baselineEntities': baseline_entities, 'baselineEntitiesSha256': entity_hash(baseline_entities),
        'finalEntityCount': len(final), 'actionCounts': counts, 'records': records,
        'documentReview': {'path': review_path,
                           'sha256': hashlib.sha256(review_bytes).hexdigest().upper(),
                           'normalizedSha256': hashlib.sha256(review_bytes.replace(b'\r\n', b'\n')).hexdigest().upper()},
        'limitations': ['基线观察从固定提交的Git对象读取；离线验收只核验回执内部覆盖及当前实体，不重新取得历史原始样本。',
                        '文档审阅和源码复核不等价于本轮重新执行游戏运行验收。'],
    }
    errors: list[str] = []
    validate_incremental_receipt(errors, result, final, review_document=review, review_bytes=review_bytes)
    if errors:
        raise ValueError('\n'.join(errors))
    return result


def write_receipt(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def incremental_output_path(root: Path, review_date: str) -> Path:
    if date.fromisoformat(review_date).isoformat() != review_date:
        raise ValueError('incremental date must use YYYY-MM-DD')
    path = root / ('sources/integration-' + review_date.replace('-', '') + '.json')
    if path.resolve() == (root / HISTORICAL_RECEIPT).resolve():
        raise ValueError('incremental date would overwrite the frozen historical receipt')
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-draft', type=Path, help='Reconstruct the historical 2026-10-28 import only.')
    parser.add_argument('--refresh-current', action='store_true', help='Refresh final targets, retaining all historical inputs and their date.')
    parser.add_argument('--incremental-from', help='Record current entities against this local Git commit/ref; never fetches.')
    parser.add_argument('--date', help='Incremental review date in YYYY-MM-DD form.')
    parser.add_argument('--document-review', help='Repository-relative document review JSON for incremental coverage.')
    args = parser.parse_args()
    if args.local_draft and (args.refresh_current or args.incremental_from):
        parser.error('--local-draft cannot be combined with incremental/refresh mode')
    if not args.local_draft and not args.refresh_current and not args.incremental_from:
        parser.error('choose --local-draft, --refresh-current, or --incremental-from')
    if bool(args.incremental_from) != bool(args.date) or bool(args.incremental_from) != bool(args.document_review):
        parser.error('--incremental-from, --date and --document-review must be supplied together')
    incremental_path = None
    if args.incremental_from:
        try:
            incremental_path = incremental_output_path(ROOT, args.date)
        except ValueError as exc:
            parser.error(str(exc))
    final = current_entities(ROOT)
    if args.refresh_current or args.incremental_from:
        # Prepare every result before writing either receipt, so failed coverage
        # cannot partially refresh the historical record.
        refreshed = None
        incremental = None
        if args.refresh_current:
            refreshed = refresh_current(json.loads((ROOT / HISTORICAL_RECEIPT).read_text(encoding='utf-8')), final)
        if args.incremental_from:
            commit, baseline = entities_at_commit(ROOT, args.incremental_from)
            from validate_kb import safe_relative_path
            if not safe_relative_path(args.document_review):
                parser.error('--document-review must be a safe repository-relative path')
            review_bytes = (ROOT / args.document_review).read_bytes()
            incremental = incremental_receipt(baseline, final, commit, args.date, args.document_review, review_bytes)
        if refreshed is not None:
            write_receipt(ROOT / HISTORICAL_RECEIPT, refreshed)
            print(f'historical_targets_refreshed final={len(final)} input_union={refreshed["inputUnionCount"]}')
        if incremental is not None:
            write_receipt(incremental_path, incremental)
            print(f'incremental_receipt={incremental_path.relative_to(ROOT).as_posix()} counts={incremental["actionCounts"]}')
        return
    observed: dict[str, list] = {}
    input_counts = {}
    for name, commit in INPUTS.items():
        paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', commit], cwd=ROOT).decode('utf-8').splitlines()
        # Git quotes non-ASCII paths by default; data paths in these commits are ASCII.
        count = 0
        for path in paths:
            if '/data/' not in path or not path.endswith('.json'):
                continue
            raw = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=ROOT)
            doc = json.loads(raw.decode('utf-8-sig'))
            for entry in doc.get('entries', []):
                observed.setdefault(entry['id'], []).append({'input': name, 'commit': commit, 'path': path,
                    'status': entry.get('status'), 'entitySha256': entity_hash(entry)})
                count += 1
        input_counts[name] = count
    local = current_entities(args.local_draft)
    input_counts['preserved-local-draft'] = len(local)
    for eid, item in local.items():
        observed.setdefault(eid, []).append({'input': 'preserved-local-draft', 'path': item['path'],
            'status': item['entry']['status'], 'entitySha256': entity_hash(item['entry'])})
    missing = sorted(set(observed) - set(final))
    if missing:
        raise ValueError('unaccounted input entities: ' + ', '.join(missing))
    records = []
    for eid in sorted(observed):
        item = final[eid]
        status = item['entry']['status']
        action = 'retained-and-reviewed'
        reason = '稳定ID保留；按画像、来源修订和字段权限审阅，生成页和索引统一重建。'
        if any(v['status'] == 'canonical' for v in observed[eid]) and status == 'candidate':
            action = 'downgraded'
            reason = '保留结构化结论，原始证据无法在本轮复核或存在未解决消费者/磁盘视图边界，候选不授权写回。'
        records.append({'id': eid, 'inputs': observed[eid], 'action': action, 'targetId': eid,
                        'targetPath': item['path'], 'targetStatus': status,
                        'targetEntitySha256': entity_hash(item['entry']), 'reason': reason})
    payload = {'schemaVersion': 1, 'date': '2026-10-28', 'inputCounts': input_counts,
               'inputUnionCount': len(observed), 'finalEntityCount': len(final), 'missingIds': missing,
               'newEntityIds': sorted(set(final) - set(observed)), 'records': records,
               'limitations': ['本地原稿原始文件与ZIP快照由工作区保留，不作为仓库运行依赖。',
                              '输入实体哈希记录结论来源，不等价于重新验证其EXE或执行其历史游戏测试。']}
    path = ROOT / 'sources/integration-20261028.json'
    write_receipt(path, payload)
    print(f'input_union={len(observed)} final={len(final)} missing={len(missing)} new={len(payload["newEntityIds"])}')


if __name__ == '__main__':
    main()
