#!/usr/bin/env python3
"""Entry point for news-image-20261124.

The entry image is pre-rendered and shipped in this repository as
news.png; this program only copies it to /output/entry.png.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "news.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
    sys.exit(0)
