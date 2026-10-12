#!/usr/bin/env python3
"""Create the repository SHA-256 manifest, excluding Git state and the manifest itself."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "MANIFEST_SHA256.tsv"
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "node_modules", "generated_v1_5"}
TEXT_SUFFIXES = {
    ".cff",
    ".csv",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".svg",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
}
TEXT_FILENAMES = {".gitignore", ".gitattributes", "LICENSE"}


def canonical_bytes(path: Path) -> bytes:
    """Return platform-stable bytes for manifest verification.

    Git normalizes line endings for text files.  Hashing canonical LF bytes keeps
    the manifest identical on Windows and Linux while preserving binary files
    byte-for-byte.
    """
    payload = path.read_bytes()
    if path.suffix.casefold() in TEXT_SUFFIXES or path.name in TEXT_FILENAMES:
        payload = payload.replace(b"\r\n", b"\n")
    return payload


def main() -> None:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path == OUTPUT:
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if path.suffix.casefold() == ".pyc":
            continue
        files.append(path)
    files.sort(key=lambda p: p.relative_to(ROOT).as_posix().casefold())
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["relative_path", "size_bytes", "sha256"])
        for path in files:
            payload = canonical_bytes(path)
            writer.writerow(
                [
                    path.relative_to(ROOT).as_posix(),
                    len(payload),
                    hashlib.sha256(payload).hexdigest(),
                ]
            )
    print(f"wrote {len(files)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
