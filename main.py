#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261124.

Copies the pre-rendered front page (entry.png) to the output directory
the grader provides. Standard library only. It writes nothing under the
repository directory, which the grader mounts read-only, and it writes
the same bytes on every run.
"""
import hashlib
import os
import sys

MAX_BYTES = 1048576
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    # The image is shipped in the repository and copied byte for byte,
    # so two runs always produce identical output, as the grader requires.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(SRC, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        written = fh.read()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        print("output bytes differ from entry.png", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
