#!/usr/bin/env python3
"""Assemble the hand-authored static pages into a clean GitHub Pages artifact."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "hotels.html", "dining.html", "experiences.html", "transit.html", "review.html"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="_site", help="output directory, relative to the repository root")
    args = parser.parse_args()
    output = (ROOT / args.output).resolve()
    if output == ROOT or ROOT not in output.parents:
        parser.error("output must be a child directory of the repository root")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    for name in PAGES:
        source = ROOT / name
        if not source.is_file():
            raise SystemExit(f"Required page is missing: {name}")
        shutil.copy2(source, output / name)
    shutil.copytree(ROOT / "assets", output / "assets")
    print(f"Built {len(PAGES)} static pages and assets into {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
