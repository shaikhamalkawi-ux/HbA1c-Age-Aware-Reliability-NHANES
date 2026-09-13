"""Verify SHA-256 content and complete file coverage for this scaffold."""
from pathlib import Path, PurePosixPath
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", ".local", ".venv", "__pycache__"}


def included_files():
    return {
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*")
        if p.is_file()
        and not any(part in IGNORED_DIRS for part in p.relative_to(ROOT).parts)
        and p.name != "SHA256SUMS.txt"
        and p.suffix not in {".pyc", ".pyo"}
    }


def main():
    manifest = ROOT / "SHA256SUMS.txt"
    if not manifest.is_file():
        print("FAIL: SHA256SUMS.txt is missing")
        return 1
    listed = set()
    errors = []
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        try:
            expected, name = line.split("  ", 1)
            relative = PurePosixPath(name)
            path = ROOT.joinpath(*relative.parts)
            if relative.is_absolute() or ".." in relative.parts or "\\" in name or ":" in name:
                raise ValueError("invalid relative path")
            if not path.resolve().is_relative_to(ROOT) or path.is_symlink():
                raise ValueError("path escapes package or is a symlink")
            if name in listed:
                raise ValueError("duplicate manifest entry")
            listed.add(name)
            if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
                raise ValueError("invalid SHA-256")
            observed = hashlib.sha256(path.read_bytes()).hexdigest()
            if observed != expected:
                errors.append(f"hash mismatch: {name}")
        except (OSError, ValueError) as exc:
            errors.append(f"manifest error: {line}: {exc}")
    actual = included_files()
    errors.extend(f"unlisted file: {name}" for name in sorted(actual - listed))
    errors.extend(f"missing file: {name}" for name in sorted(listed - actual))
    if not listed:
        errors.append("empty manifest")
    if errors:
        print("FAIL\n" + "\n".join(errors))
        return 1
    print(f"PASS: {len(listed)} file hashes and complete scaffold coverage verified.")
    print("This is package integrity only; no scientific reproduction was performed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
