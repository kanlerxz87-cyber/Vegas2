"""Publish this session's static dashboard under docs/session-d33551df.

This deliberately writes only its own Pages subdirectory. It does not replace
or clean docs/index.html or any dashboard built by another session.
"""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site"
DESTINATION = ROOT / "docs" / "session-d33551df"

DESTINATION.mkdir(parents=True, exist_ok=True)
for page in SOURCE.glob("*.html"):
    shutil.copy2(page, DESTINATION / page.name)
shutil.copytree(SOURCE / "assets", DESTINATION / "assets", dirs_exist_ok=True)

print(f"Published supplemental dashboard to {DESTINATION.relative_to(ROOT)}")
