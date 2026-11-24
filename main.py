"""Entry-point for the news-image program.

Copies the rendered front page (entry.png, produced by tools/draw.py)
into the directory the grader reads, then proves the copy is exact by
comparing SHA-256 digests. The output directory comes from the
MAKEFUN_OUTPUT_DIR environment variable and falls back to /output.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEFAULT_OUT = "/output"


def sha256_of(path):
    """SHA-256 hex digest of a file, read in chunks."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def out_dir():
    """Output directory from the environment, defaulting to /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT) or DEFAULT_OUT

def main():
    dest_dir = out_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    src_hash = sha256_of(SOURCE)
    dst_hash = sha256_of(dest)
    if src_hash != dst_hash:
        print("MISMATCH: copied entry.png differs from the source",
              file=sys.stderr)
        print("source:", src_hash, file=sys.stderr)
        print("copy:  ", dst_hash, file=sys.stderr)
        return 1
    print("copied entry.png to", dest)
    print("sha256:", dst_hash)
    print("verified: copy is byte-identical to the source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
