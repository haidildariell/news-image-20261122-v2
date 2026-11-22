#!/usr/bin/env python3
"""Entrypoint for make.fun news-image-20261122 (v2).

The page image is pre-rendered by build_image.py and shipped as
entry.png next to this file. At run time we only copy it to the
output directory - stdlib only, no network, byte-identical output.
"""
import os
import shutil
from pathlib import Path


def main():
    src = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")
    print("entry.png ->", out_dir / "entry.png")


if __name__ == "__main__":
    main()
