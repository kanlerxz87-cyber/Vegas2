#!/usr/bin/env python3
"""Automated quality & integrity checks for session-3c7ffbdd."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "session-3c7ffbdd"
OUT_DIR = REPO_ROOT / "docs" / "session-3c7ffbdd"

FORBIDDEN_DOMAINS = (
    "highroller.com",
    "fremontexperience.com",
    "vegasmonorail.com",
    "www.bellagio.mgmresorts.com",
)


class LinkAndTagChecker(HTMLParser):
    VOID_TAGS = {"meta", "link", "br", "hr", "img", "input", "source", "area", "base", "col", "embed", "param", "track", "wbr"}

    def __init__(self, filename: str) -> None:
        super().__init__()
        self.filename = filename
        self.stack: list[str] = []
        self.errors: list[str] = []
        self.hrefs: list[str] = []
        self.srcs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        if tag == "a" and attr_map.get("href"):
            self.hrefs.append(attr_map["href"] or "")
        if tag == "link" and attr_map.get("href"):
            self.srcs.append(attr_map["href"] or "")
        if tag == "script" and attr_map.get("src"):
            self.srcs.append(attr_map["src"] or "")
        if tag not in self.VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag in self.VOID_TAGS:
            return
        if not self.stack or self.stack[-1] != tag:
            expected = self.stack[-1] if self.stack else "<none>"
            self.errors.append(f"{self.filename}: mismatched </{tag}> (expected </{expected}>)")
            return
        self.stack.pop()


def load_json(name: str) -> dict:
    with (DATA_DIR / name).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    errors: list[str] = []

    # 1. Deterministic build check
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "build_session_3c7ffbdd.py"), "--check"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        errors.append(proc.stderr.strip() or proc.stdout.strip())

    # 2. Data integrity & Michelin count verification
    hotels = load_json("hotels.json")["hotels"]
    restaurants = load_json("restaurants.json")["restaurants"]
    activities = load_json("activities.json")["activities"]
    suggestions = load_json("suggestions.json")["suggestions"]
    qa_items = load_json("questions.json")["qa_items"]
    flagged = load_json("flagged.json")

    if len(hotels) < 8:
        errors.append(f"Expected >=8 hotels, found {len(hotels)}")
    for h in hotels:
        if not (h.get("source_url") or "").startswith("https://"):
            errors.append(f"Hotel {h.get('id')} missing https source_url")

    if len(restaurants) != 24:
        errors.append(f"Expected exactly 24 Michelin restaurants, found {len(restaurants)}")

    counts = {"Two": 0, "One": 0, "Bib": 0, "Recommended": 0}
    for r in restaurants:
        if not (r.get("official_url") or "").startswith("https://"):
            errors.append(f"Restaurant {r.get('id')} missing https official_url")
        if not (r.get("michelin_source_url") or "").startswith("https://"):
            errors.append(f"Restaurant {r.get('id')} missing https michelin_source_url")
        d = r.get("distinction", "")
        if "Two" in d:
            counts["Two"] += 1
        elif "One" in d:
            counts["One"] += 1
        elif "Bib" in d:
            counts["Bib"] += 1
        elif "Recommended" in d:
            counts["Recommended"] += 1
    if counts != {"Two": 1, "One": 3, "Bib": 3, "Recommended": 17}:
        errors.append(f"Unexpected Michelin counts: {counts}")

    if len(activities) < 10:
        errors.append(f"Expected >=10 activities, found {len(activities)}")
    for a in activities:
        if not (a.get("official_url") or "").startswith("https://"):
            errors.append(f"Activity {a.get('id')} missing https official_url")

    for s in suggestions:
        if not (s.get("source_url") or "").startswith("https://"):
            errors.append(f"Suggestion {s.get('id')} missing https source_url")

    for q in qa_items:
        if not (q.get("source_url") or "").startswith("https://"):
            errors.append(f"Q&A {q.get('id')} missing https source_url")

    for section in ("repo_audit_irregularities", "official_source_conflicts_and_gaps"):
        for item in flagged[section]:
            if not (item.get("source_url") or "").startswith("https://"):
                errors.append(f"Flagged item {item.get('id')} missing https source_url")

    # 3. HTML tag balance, local link & asset integrity, forbidden broken domains
    html_files = sorted(OUT_DIR.glob("*.html"))
    if len(html_files) != 7:
        errors.append(f"Expected 7 HTML pages in docs/session-3c7ffbdd, found {len(html_files)}")

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        for bad in FORBIDDEN_DOMAINS:
            if re.search(rf"https?://{re.escape(bad)}", text, re.IGNORECASE):
                errors.append(f"{path.name}: contains forbidden broken domain {bad}")

        parser = LinkAndTagChecker(path.name)
        parser.feed(text)
        if parser.stack:
            errors.append(f"{path.name}: unclosed tags {parser.stack}")
        errors.extend(parser.errors)

        for ref in parser.hrefs + parser.srcs:
            if ref.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            target = (path.parent / ref.split("#", 1)[0]).resolve()
            if not target.exists():
                errors.append(f"{path.name}: broken local reference '{ref}'")

    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1

    print(
        f"PASS: Verified {len(html_files)} pages, {len(hotels)} hotels, "
        f"{len(restaurants)} Michelin restaurants ({counts}), {len(activities)} activities, "
        f"{len(flagged['repo_audit_irregularities']) + len(flagged['official_source_conflicts_and_gaps'])} flagged items."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
