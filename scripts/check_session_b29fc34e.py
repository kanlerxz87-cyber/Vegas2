#!/usr/bin/env python3
"""Lightweight offline checks for the static Las Vegas guide."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "site" / "session-b29fc34e"
PAGES = ["index.html", "hotels.html", "dining.html", "experiences.html", "transit.html", "review.html"]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.links: list[str] = []
        self.images_without_alt: list[str] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.h1_count = 0
        self.lang: str | None = None
        self.has_viewport = False
        self.has_main = False
        self.restaurant_cards: list[dict[str, object]] = []
        self._restaurant_stack: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        element_id = attrs_dict.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        if tag == "html":
            self.lang = attrs_dict.get("lang")
        if tag == "meta" and attrs_dict.get("name", "").lower() == "viewport":
            self.has_viewport = True
        if tag == "main":
            self.has_main = True
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"] or "")
            if self._restaurant_stack and (attrs_dict["href"] or "").startswith("https://"):
                self._restaurant_stack[-1]["external_sources"] = int(self._restaurant_stack[-1]["external_sources"]) + 1
        if tag == "img" and "alt" not in attrs_dict:
            self.images_without_alt.append(attrs_dict.get("src") or "(unknown source)")
        if tag == "article" and "data-restaurant-card" in attrs_dict:
            card: dict[str, object] = {
                "status": attrs_dict.get("data-michelin"),
                "external_sources": 0,
            }
            self.restaurant_cards.append(card)
            self._restaurant_stack.append(card)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag == "article" and self._restaurant_stack:
            self._restaurant_stack.pop()

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data.strip())


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def main() -> int:
    errors: list[str] = []
    parsed: dict[str, PageParser] = {}

    for page_name in PAGES:
        page = SOURCE / page_name
        if not page.is_file():
            errors.append(f"Missing required page: {page_name}")
            continue
        parser = parse_page(page)
        parsed[page_name] = parser
        if not parser.title_parts or not "".join(parser.title_parts).strip():
            errors.append(f"{page_name}: missing a non-empty <title>")
        if not parser.lang:
            errors.append(f"{page_name}: <html> is missing its lang attribute")
        if not parser.has_viewport:
            errors.append(f"{page_name}: missing responsive viewport metadata")
        if not parser.has_main:
            errors.append(f"{page_name}: missing a <main> landmark")
        if parser.h1_count != 1:
            errors.append(f"{page_name}: expected exactly one <h1>, found {parser.h1_count}")
        if parser.duplicate_ids:
            errors.append(f"{page_name}: duplicate id(s): {', '.join(sorted(parser.duplicate_ids))}")
        if parser.images_without_alt:
            errors.append(f"{page_name}: image(s) missing alt attribute: {', '.join(parser.images_without_alt)}")

    # Validate local files and fragment targets. External URLs are deliberately not
    # fetched here: checks must work offline and venue pages change independently.
    for page_name, parser in parsed.items():
        page_path = SOURCE / page_name
        for raw_href in parser.links:
            href = raw_href.strip()
            if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            parts = urlsplit(href)
            if parts.scheme or parts.netloc:
                continue
            decoded_path = unquote(parts.path)
            if decoded_path:
                target = (page_path.parent / decoded_path).resolve()
                if not target.is_file():
                    errors.append(f"{page_name}: local link target does not exist: {href}")
                elif parts.fragment and target.parent == SOURCE and target.name in parsed:
                    if unquote(parts.fragment) not in parsed[target.name].ids:
                        errors.append(f"{page_name}: fragment target does not exist: {href}")
            elif parts.fragment and unquote(parts.fragment) not in parser.ids:
                errors.append(f"{page_name}: fragment target does not exist: {href}")

    dining = parsed.get("dining.html")
    if dining:
        if len(dining.restaurant_cards) != 24:
            errors.append(f"dining.html: expected 24 restaurant cards, found {len(dining.restaurant_cards)}")
        allowed_statuses = {"star", "bib", "listed"}
        for index, card in enumerate(dining.restaurant_cards, start=1):
            if card["status"] not in allowed_statuses:
                errors.append(f"dining.html: restaurant card {index} has unknown MICHELIN filter status {card['status']!r}")
            if int(card["external_sources"]) < 1:
                errors.append(f"dining.html: restaurant card {index} has no external source link")

    if errors:
        print("Static site checks failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Static site checks passed: {len(parsed)} pages, 24 sourced restaurant cards, local files and fragments OK.")
    print("Note: external provider links were not fetched by this offline checker.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
