"""Record stable-ID coverage for the 2026-10-28 branch and local-draft import.

This is a historical import command, not a network or source-workspace CI step.
CI can validate the recorded final hashes without fetching historical branches.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUTS = {
    'main': 'b2c60c6b1f2b0e565fb69ababc19fd4aa924e86b',
    'codex/item-consumable-knowledge-20261020': '76da41a3f5e406a8ad70ff27e7ddbf37c3547d24',
    'dsh/6.6-item-restore-chain': 'a6347d5f39034c56f5e98399d3b0fef267cf9e05',
    'dsh/6.6-20261027-batch': '2559999830ac84fc2454cd9c1cac0afbb66b162a',
}


def entity_hash(value: dict) -> str:
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-draft', type=Path, required=True)
    args = parser.parse_args()
    final = current_entities(ROOT)
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
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(f'input_union={len(observed)} final={len(final)} missing={len(missing)} new={len(payload["newEntityIds"])}')


if __name__ == '__main__':
    main()
