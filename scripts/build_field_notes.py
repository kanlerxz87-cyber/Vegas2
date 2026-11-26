#!/usr/bin/env python3
"""Copy the standalone Field Notes source into its isolated Pages subdirectory."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "field-notes"
TARGET = ROOT / "docs" / "session-2e5e3452"
FILES = [
    ".nojekyll",
    "index.html",
    "restaurants.html",
    "hotels.html",
    "experiences.html",
    "itinerary.html",
    "getting-around.html",
    "review.html",
]
DIRECTORIES = ["assets", "data"]


def main() -> None:
    if TARGET.resolve() == ROOT.resolve() or ROOT.resolve() not in TARGET.resolve().parents:
        raise SystemExit("Refusing to build outside docs/session-2e5e3452")
    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.mkdir(parents=True)
    for relative in FILES:
        source = SOURCE / relative
        if not source.is_file():
            raise SystemExit(f"Missing Field Notes source file: {source.relative_to(ROOT)}")
        shutil.copy2(source, TARGET / relative)
    for relative in DIRECTORIES:
        source = SOURCE / relative
        if not source.is_dir():
            raise SystemExit(f"Missing Field Notes source directory: {source.relative_to(ROOT)}")
        shutil.copytree(source, TARGET / relative)
    print(f"Published {len(FILES)} root files and {len(DIRECTORIES)} asset/data folders to {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
