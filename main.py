#!/usr/bin/env python3
"""news-image-20261124 entrypoint.

Copies the repository's front-page image to /output/entry.png.
Standard library only, no network, deterministic: the bytes written are
exactly the bytes of entry.png in this repository. After copying, the
program reads the copy back and checks it is byte-for-byte the same file,
so a half-written or truncated copy can never pass as a valid hand-in.
The output is also left world-readable (mode 0644), since the grader
collects it as another user.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    with open(SRC, "rb") as f:
        expected = f.read()
    with open(dst, "rb") as f:
        actual = f.read()
    if actual != expected:
        raise SystemExit("entry.png copy mismatch: output differs from source")
    os.chmod(dst, 0o644)


if __name__ == "__main__":
    main()
