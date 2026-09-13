"""Regenerate the exact public allowlist, current-content report, and SHA-256 manifest.

This script is repository bookkeeping only. It does not read private scientific inputs or
change any scientific result.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {'.git', '.local', '.venv', '__pycache__'}
IGNORED_SUFFIXES = {'.pyc', '.pyo'}


def files(include_manifest=True):
    out = []
    for p in ROOT.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if any(part in IGNORED_DIRS for part in rel.parts):
            continue
        if p.suffix in IGNORED_SUFFIXES:
            continue
        if not include_manifest and rel.as_posix() == 'SHA256SUMS.txt':
            continue
        out.append(p)
    return sorted(out, key=lambda p: p.relative_to(ROOT).as_posix())


def main():
    allowlist_path = ROOT / 'verification' / 'public_allowlist.json'
    report_path = ROOT / 'verification' / 'public_content_report.json'
    manifest_path = ROOT / 'SHA256SUMS.txt'

    # The allowlist represents the complete public snapshot, including the manifest/report.
    allowlist = [p.relative_to(ROOT).as_posix() for p in files(include_manifest=True)]
    allowlist_path.write_text(json.dumps(allowlist, indent=2) + '\n', encoding='utf-8', newline='\n')

    proc = subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'check_public_content.py')],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    report_path.write_text(proc.stdout.rstrip() + '\n', encoding='utf-8', newline='\n')

    lines = []
    for p in files(include_manifest=False):
        rel = p.relative_to(ROOT).as_posix()
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f'{digest}  {rel}')
    manifest_path.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')

    if proc.returncode:
        sys.stderr.write(proc.stderr)
        return proc.returncode
    print(f'PASS: regenerated allowlist ({len(allowlist)} files), public-content report, and manifest ({len(lines)} entries).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
