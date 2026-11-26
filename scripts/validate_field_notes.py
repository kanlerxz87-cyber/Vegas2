#!/usr/bin/env python3
"""Dependency-free structural checks for the isolated Vegas Field Notes site."""
from __future__ import annotations

import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "field-notes"
PUBLISHED = ROOT / "docs" / "session-2e5e3452"
PAGES = [
    "index.html",
    "restaurants.html",
    "hotels.html",
    "experiences.html",
    "itinerary.html",
    "getting-around.html",
    "review.html",
]


class LinkAndIdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.local_refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if not value:
                continue
            parsed = urlsplit(value)
            if parsed.scheme or parsed.netloc or value.startswith("#"):
                continue
            local_path = unquote(parsed.path)
            if local_path:
                self.local_refs.append((attribute, local_path))


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_json() -> None:
    try:
        restaurants = json.loads((SITE / "data/restaurants.json").read_text(encoding="utf-8"))
        hotels = json.loads((SITE / "data/hotels.json").read_text(encoding="utf-8"))
        experiences = json.loads((SITE / "data/experiences.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"data JSON failed to parse: {error}")

    restaurant_rows = restaurants.get("restaurants", [])
    if len(restaurant_rows) != 24:
        fail(f"expected 24 restaurant entries, found {len(restaurant_rows)}")
    award_counts = Counter(row.get("awardType") for row in restaurant_rows)
    expected_awards = Counter({"starred": 4, "bib": 3, "recommended": 17})
    if award_counts != expected_awards:
        fail(f"unexpected restaurant distinction counts: {award_counts}")
    if any(not row.get("name") or not row.get("source") for row in restaurant_rows):
        fail("every restaurant needs a name and a direct source URL")

    scenarios = hotels.get("scenarios", {})
    if set(scenarios) != {"threeNight", "sevenNight"}:
        fail("hotel data must keep three-night and seven-night scenarios separate")
    for scenario_key, scenario in scenarios.items():
        hotel_rows = scenario.get("hotels", [])
        if len(hotel_rows) != 5:
            fail(f"{scenario_key} must contain five hotel quotes, found {len(hotel_rows)}")
        if any(not hotel.get("rates") for hotel in hotel_rows):
            fail(f"a hotel in {scenario_key} has no displayed rate entry")
    if len(experiences.get("experiences", [])) < 4:
        fail("expected the core activity research entries")


def check_html_tree(base: Path, label: str) -> None:
    for page in PAGES:
        page_path = base / page
        if not page_path.is_file():
            fail(f"required {label} page missing: {page}")
        text = page_path.read_text(encoding="utf-8")
        parser = LinkAndIdParser()
        parser.feed(text)
        if parser.duplicate_ids:
            fail(f"duplicate IDs in {label} {page}: {sorted(parser.duplicate_ids)}")
        for _attribute, local_path in parser.local_refs:
            destination = (base / local_path).resolve()
            if not destination.is_relative_to(base.resolve()):
                fail(f"local reference escapes {label} site in {page}: {local_path}")
            if not destination.exists():
                fail(f"broken local reference in {label} {page}: {local_path}")
        if '<html lang="en"' not in text:
            fail(f"language attribute missing from {label} {page}")


def main() -> None:
    check_json()
    check_html_tree(SITE, "source")
    for required in (SITE / "assets/css/site.css", SITE / "assets/js/app.js", SITE / ".nojekyll", ROOT / "scripts/build_field_notes.py"):
        if not required.exists():
            fail(f"required Field Notes asset or script missing: {required.relative_to(ROOT)}")
    app_js = (SITE / "assets/js/app.js").read_text(encoding="utf-8")
    if "localhost" in app_js or "127.0.0.1" in app_js:
        fail("browser-facing script must not depend on localhost")

    if PUBLISHED.exists():
        check_html_tree(PUBLISHED, "published")
        for relative in ("assets/css/site.css", "assets/js/app.js", "data/restaurants.json", "data/hotels.json", "data/experiences.json"):
            if not (PUBLISHED / relative).is_file():
                fail(f"published asset missing: docs/session-2e5e3452/{relative}")

    print("PASS: source pages, internal references, research JSON, and scenario counts are valid.")
    print("PASS: 24 restaurants = 4 starred + 3 Bib Gourmand + 17 Recommended.")
    print("PASS: five hotel entries in each separate three-night and seven-night scenario.")
    if PUBLISHED.exists():
        print("PASS: generated docs/session-2e5e3452/ copy matches the site structure.")


if __name__ == "__main__":
    main()
