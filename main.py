#!/usr/bin/env python3
"""Entrypoint: regenerate entry.png (deterministic) into the output dir.

The grader runs this program with a read-only repo and a writable
$MAKEFUN_OUTPUT_DIR; the image must be written there. The output is fully
deterministic: the same code always produces the same bytes, so the pinned
hash below is a hard check that the run reproduced the reviewed image.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gen import build

PINNED_SHA256 = "aaa85c01a101d687ad4e1b866a5df7da7c8d2f6f3381f45c3e143c195431cee3"


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.dirname(
        os.path.abspath(__file__)
    )
    out = os.path.join(outdir, "entry.png")
    img = build()
    assert img.size == (1024, 1024), img.size
    img.save(out, "PNG")  # PNG, 1024x1024, well under the 1 MiB cap
    data = open(out, "rb").read()
    assert len(data) <= 1024 * 1024, len(data)
    h = hashlib.sha256(data).hexdigest()
    assert h == PINNED_SHA256, h
    print("wrote", out, len(data), "bytes, sha256", h)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
