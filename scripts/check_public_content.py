"""Bounded screening of the exact text-only checkpoint allowlist."""
import json
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", ".local", ".venv", "__pycache__"}
RULES = {
    "absolute_home_path": re.compile(r"[A-Za-z]:" + r"[\\/]" + r"(?:Users|home)[\\/]", re.I),
    "absolute_analysis_path": re.compile("/" + "mnt/" + "data(?:/|\\b)"),
    "github_token": re.compile("gh" + r"[pousr]_[A-Za-z0-9]{30,}"),
    "github_pat": re.compile("github" + r"_pat_[A-Za-z0-9_]{30,}"),
    "openai_style_key": re.compile("sk" + r"-[A-Za-z0-9_-]{24,}"),
    "aws_access_key": re.compile("AK" + r"IA[A-Z0-9]{16}"),
    "slack_style_token": re.compile("xox" + r"[abpor]-[A-Za-z0-9-]{16,}"),
    "private_key": re.compile("-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "internal_version_label": re.compile(r"\bR" + r"4[._]6\b"),
    "email_address": re.compile(r"[A-Za-z0-9._%+-]+@" + r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
}


def main():
    allowlist = set(json.loads((ROOT / "verification/public_allowlist.json").read_text(encoding="utf-8")))
    actual = {}
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for name in files:
            p = Path(folder) / name
            if p.suffix not in {".pyc", ".pyo"}:
                actual[p.relative_to(ROOT).as_posix()] = p
    findings = []
    for name in sorted(set(actual) - allowlist):
        findings.append({"path": name, "rule": "not_allowlisted"})
    for name in sorted(allowlist - set(actual)):
        findings.append({"path": name, "rule": "missing_allowlisted_file"})
    for name, path in sorted(actual.items()):
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            findings.append({"path": name, "rule": "symlink_or_path_escape"})
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError:
            findings.append({"path": name, "rule": "non_text_file"})
            continue
        for label, pattern in RULES.items():
            if pattern.search(content):
                findings.append({"path": name, "rule": label})
    report = {
        "scope": "Exact public text allowlist and specified lexical checks only; history, numerical and license verification are separate",
        "files_scanned": len(actual),
        "status": "PASS" if not findings else "FAIL",
        "findings": findings,
    }
    print(json.dumps(report, indent=2))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
