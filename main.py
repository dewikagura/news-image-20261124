#!/usr/bin/env python3
"""news-image-20261124 entrypoint: hand in the front-page image.

Copies the rendered entry.png (drawn in code with Pillow in this session)
into the output directory the grader provides. Standard library only;
reads the repo, writes only to MAKEFUN_OUTPUT_DIR (default /output).
The program runs twice and both runs must write identical bytes, so
nothing here depends on time, chance, or the network.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

ENTRY = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1_048_576


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    data = ENTRY.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(ENTRY, target)
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        print("copy mismatch: output differs from entry.png", file=sys.stderr)
        return 1
    print(f"entry.png ({len(data)} bytes, sha256 {digest[:12]}...) -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
