#!/usr/bin/env python3
"""Entrypoint: hand entry.png to the grader's output directory.

The grader mounts this program read-only and gives it exactly one
writable place: the directory named by MAKEFUN_OUTPUT_DIR. This script
therefore never writes next to itself. Without the variable (a local
run) it uses an output/ folder beside this file instead.

The image itself is NOT regenerated here: entry.png was drawn once,
reviewed, and committed in this repository. Regenerating it would need
Pillow and the DejaVu fonts, which the grader's pinned python3.13
image does not ship — that is exactly why round 1 failed
run_completes with exit code 1. Copying the committed file is fully
deterministic (same bytes every run, byte-identical to the reviewed
image) and needs only the standard library, so it runs anywhere the
grader runs it.

After copying it checks the delivered file: it must be a 1024x1024 PNG
whose sha256 matches the hash pinned below (the hash of the entry.png
committed in this repository) and it must fit inside 1 MiB.
Any mismatch exits non-zero.
"""

import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

PINNED_SHA256 = "aaa85c01a101d687ad4e1b866a5df7da7c8d2f6f3381f45c3e143c195431cee3"
PINNED_W = 1024
PINNED_H = 1024
MAX_BYTES = 1024 * 1024

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def pick_output_dir():
    """Grader-provided writable directory, else a local output/ folder."""
    given = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if given:
        return Path(given)
    return HERE / "output"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError("delivered file is not a PNG")
    return struct.unpack(">II", head[16:24])


def deliver():
    if not SOURCE.is_file():
        print("MISSING: source image not found:", SOURCE, file=sys.stderr)
        return 2
    size = SOURCE.stat().st_size
    if size > MAX_BYTES:
        print(f"TOO BIG: source is {size} bytes, limit is 1 MiB",
              file=sys.stderr)
        return 5
    try:
        sw, sh = png_size(SOURCE)
    except (OSError, ValueError) as exc:
        print("BAD SOURCE:", exc, file=sys.stderr)
        return 6
    if (sw, sh) != (PINNED_W, PINNED_H):
        print(f"BAD SOURCE SIZE: {sw}x{sh}, want "
              f"{PINNED_W}x{PINNED_H}", file=sys.stderr)
        return 3
    target_dir = pick_output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    w, h = png_size(target)
    if (w, h) != (PINNED_W, PINNED_H):
        print(f"BAD SIZE: delivered {w}x{h}, want "
              f"{PINNED_W}x{PINNED_H}", file=sys.stderr)
        return 3
    got = sha256_file(target)
    if got != PINNED_SHA256:
        print("BAD HASH: delivered", got, "want", PINNED_SHA256,
              file=sys.stderr)
        return 4
    print("delivered", target, f"{w}x{h}", f"{size} bytes", got)
    return 0


if __name__ == "__main__":
    sys.exit(deliver())
