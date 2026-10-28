"""Freeze available text evidence without redistributing game binaries.

Run with --workspace pointing at the source workspace. Existing snapshots remain
valid without that workspace; this command is an import step, not a CI dependency.
Original-byte SHA and redacted snapshot SHA are deliberately separate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BINARY = {'.exe', '.dll', '.zip', '.7z', '.rar', '.png', '.jpg', '.bmp', '.e5', '.eex', '.xlsx', '.docx', '.pdb'}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def git(repo: Path, *args: str) -> bytes | None:
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
    return result.stdout if result.returncode == 0 else None


def safe_text(data: bytes) -> bytes | None:
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        return None
    if '\x00' in text:
        return None
    # Evidence can contain command transcripts and fixture paths. Remove machine
    # prefixes while retaining the final filename and explicit derivation reason.
    text = re.sub(r'[A-Z]:[\\/][^\r\n\t"<>|]*', '<source-workspace>', text)
    text = re.sub(r'/(?:Users|home)/[^\s"<>]+', '<source-workspace>', text)
    return text.encode('utf-8')


def resolve(entry: dict, workspace: Path, repos: list[tuple[Path, str]]) -> dict:
    relative = entry['path'].replace('\\', '/')
    if relative.startswith('../'):
        entry.setdefault('originalPathNotation', relative)
        while relative.startswith('../'):
            relative = relative[3:]
    entry['path'] = relative
    expected = entry['sha256'].upper()
    entry['sha256'] = expected
    current = entry.get('verification', {})
    if current.get('kind') == 'repository-snapshot':
        snapshot = ROOT / str(current.get('snapshotPath', ''))
        if snapshot.is_file() and digest(snapshot.read_bytes()) == str(current.get('sha256', '')).upper():
            return current
    if current.get('kind') == 'remote-git':
        return current
    if current.get('kind') == 'repository-file':
        target = ROOT / relative
        if target.is_file() and digest(target.read_bytes()) == expected:
            return current
    path = ROOT / relative
    if path.is_file() and digest(path.read_bytes()) == expected:
        return {'kind': 'repository-file', 'sha256': expected}
    if entry.get('repository') and entry.get('gitCommit') and entry.get('gitPath'):
        return {'kind': 'remote-git', 'repository': entry['repository'], 'commit': entry['gitCommit'], 'path': entry['gitPath'], 'sha256': expected,
                'reason': '固定提交的已审阅JSON；该来源本身是上游结论，不替代未发布样本的运行时证据。'}
    if Path(relative).suffix.lower() in BINARY or entry.get('sourceType') == 'sample-binary':
        return {'kind': 'identity-only', 'reason': '仅保存样本或二进制身份与原始SHA256；不发布原件。必须自备完全匹配的样本才能复核字节，不能由版本名推导兼容性。'}
    for repo, url in repos:
        if git(repo, 'rev-parse', '--git-dir') is None:
            continue
        commits = git(repo, 'log', '--all', '--format=%H', '--', relative) or b''
        for commit in commits.decode().splitlines():
            raw = git(repo, 'show', commit + ':' + relative)
            if raw is not None and digest(raw) == expected:
                return {'kind': 'remote-git', 'repository': url, 'commit': commit, 'path': relative, 'sha256': expected,
                        'reason': '已从本地Git对象读取固定提交原字节并核对SHA256；CI仅离线检查固定提交元数据。'}
    candidates = [workspace / relative, workspace / '_github-data-manager-20261022' / relative,
                  workspace / '_github-kb-integrate-20261020' / relative]
    for candidate in candidates:
        if not candidate.is_file():
            continue
        raw = candidate.read_bytes()
        if digest(raw) != expected or len(raw) > 1_000_000:
            continue
        text = safe_text(raw)
        if text is None:
            continue
        name = 'sources/evidence/' + expected[:20].lower() + '.txt'
        snapshot = ROOT / name
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        snapshot.write_bytes(text)
        return {'kind': 'repository-snapshot', 'snapshotPath': name, 'sha256': digest(text),
                'reason': '读取时原件SHA256完全匹配。快照仅去除UTF-8 BOM和本机绝对路径；快照哈希独立于原件哈希，逐字节复核仍需原件。' if text != raw else '原件匹配SHA256的完整UTF-8文本快照。'}
    return {'kind': 'external-local', 'reason': '历史来源原字节未在当前工作区或已抓取Git历史中找到，原始SHA256仅保留为身份记录；本次不能复核原件，不能据此宣称重新完成静态或实机验证。'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace', type=Path, required=True)
    args = parser.parse_args()
    repos = [(ROOT, 'https://github.com/Artkights/Knowledge-base-for-CCZ-mod'),
             (args.workspace / '_github-data-manager-20261022', 'https://github.com/Artkights/CCZ-DataManager'),
             (args.workspace, 'https://github.com/Artkights/AI-For-CCZ')]
    manifest = ROOT / 'sources/source-manifest.json'
    doc = json.loads(manifest.read_text(encoding='utf-8'))
    counts: dict[str, int] = {}
    for entry in doc['entries']:
        entry['verification'] = resolve(entry, args.workspace, repos)
        key = entry['verification']['kind']
        counts[key] = counts.get(key, 0) + 1
    doc['entries'].sort(key=lambda entry: entry['id'])
    manifest.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(counts, sort_keys=True))


if __name__ == '__main__':
    main()
