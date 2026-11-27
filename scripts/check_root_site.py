#!/usr/bin/env python3
"""Offline checker for the Vegas2 ROOT site only (session c88d116c).

Scope: index.html, restaurants.html, hotels.html, activities.html,
booking.html, questions.html, suggestions.html, flagged-for-review.html,
sources.html, assets/css/style.css, data/session-c88d116c/verification.json.

Does NOT touch docs/**, site/**, field-notes/**, legacy-dashboard/**,
data/verified/**, data/trip/**, or other data/*.json files.

Checks (all offline, no network):
  1. Required files exist.
  2. Each page: viewport meta, stylesheet link, nav toggle ids, exactly one
     active nav link pointing at itself, footer disclaimer.
  3. Internal .html links resolve to a file in the repo root.
  4. Forbidden (wrong/parked) domains are absent from href attributes
     (prose may document them as fixed irregularities, never as links).
  5. Forbidden inference phrases (unverified travel-time estimates) absent.
  6. Every <tbody> table row on DATA pages contains at least one http(s)
     link (every data row sourced to an official site). The suggestions
     reviewer sign-off log is exempt (meta table, not data).
  7. No TODO/FIXME placeholders; verification.json parses with required keys.
  8. Mobile basics: viewport meta + .table-wrap styles + media query in CSS.
  9. Row-count sanity: restaurants >= 24 body rows, activities >= 12.

Exit 0 on PASS, 1 on any FAIL.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    "index.html",
    "restaurants.html",
    "hotels.html",
    "activities.html",
    "booking.html",
    "questions.html",
    "suggestions.html",
    "flagged-for-review.html",
    "sources.html",
]

REQUIRED = PAGES + [
    "assets/css/style.css",
    "data/session-c88d116c/verification.json",
]

FORBIDDEN_DOMAINS = [
    "vegasmonorail.com",      # parked; use lvmonorail.com
    "highroller.com",         # unrelated content; use Caesars page
    "kameomakase.com",        # redirects; use sushikame.com
    "fremontexperience.com",  # use fremontstreetexperience.com
]

FORBIDDEN_PHRASES = [
    "15–20 min", "15-20 min", "15–20 minutes", "15-20 minutes",
    "20–25 min", "20-25 min", "~15", "~20",
    "roughly 15", "roughly 20", "within roughly",
]

failures: list[str] = []
passes: list[str] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    (passes if ok else failures).append(label if ok else f"{label} :: {detail}")


def main() -> int:
    # 1. required files
    for rel in REQUIRED:
        check((ROOT / rel).is_file(), f"exists:{rel}", f"missing {rel}")

    texts: dict[str, str] = {}
    for page in PAGES:
        p = ROOT / page
        if p.is_file():
            texts[page] = p.read_text(encoding="utf-8")

    # 2. per-page structure
    for page, html in texts.items():
        check('name="viewport"' in html, f"viewport:{page}", "no viewport meta")
        check('href="assets/css/style.css"' in html, f"css:{page}", "stylesheet link missing")
        check('id="navToggle"' in html and 'id="navLinks"' in html,
              f"navtoggle:{page}", "nav toggle ids missing")
        active = re.findall(r'<a href="([^"]+)" class="active">', html)
        check(len(active) == 1 and active[0] == page, f"navactive:{page}",
              f"expected exactly one active link to {page}, found {active}")
        check("Unverified items are flagged" in html, f"disclaimer:{page}",
              "footer disclaimer missing")
        check("TODO" not in html and "FIXME" not in html, f"no-todo:{page}",
              "TODO/FIXME placeholder present")

    # 3. internal links resolve
    hrefs = set()
    for page, html in texts.items():
        for m in re.finditer(r'href="([^"#]+?)(?:#[^"]*)?"', html):
            hrefs.add((page, m.group(1)))
    for page, href in sorted(hrefs):
        if href.startswith(("http://", "https://", "data:", "mailto:", "tel:")):
            continue
        target = (ROOT / href).resolve()
        ok = str(target).startswith(str(ROOT)) and target.is_file()
        check(ok, f"link:{page}->{href}", f"broken internal link from {page} to {href}")

    # 4. forbidden domains (href attributes only; prose may document
    # fixed irregularities but must never link these hosts)
    http_hrefs: list[tuple[str, str]] = []
    for page, html in texts.items():
        for m in re.finditer(r'href="(https?://[^"]+)"', html):
            http_hrefs.append((page, m.group(1)))
    for page in texts:
        page_hrefs = " ".join(h for p, h in http_hrefs if p == page)
        for dom in FORBIDDEN_DOMAINS:
            check(dom not in page_hrefs, f"domain:{page}:{dom}",
                  f"forbidden domain {dom} linked from {page}")

    # 5. forbidden inference phrases
    for page, html in texts.items():
        for phrase in FORBIDDEN_PHRASES:
            check(phrase not in html, f"no-inference:{page}:{phrase}",
                  f"unverified estimate phrase {phrase!r} in {page}")

    # 6. every tbody row on DATA pages has an http(s) link
    DATA_PAGES = {"restaurants.html", "hotels.html", "activities.html",
                  "booking.html", "sources.html", "flagged-for-review.html"}
    for page, html in texts.items():
        if page not in DATA_PAGES:
            continue
        bodies = re.findall(r"<tbody>(.*?)</tbody>", html, re.S)
        rows = []
        for b in bodies:
            rows += re.findall(r"<tr>(.*?)</tr>", b, re.S)
        if not rows:
            continue
        bad = [i for i, r in enumerate(rows)
               if "http://" not in r and "https://" not in r]
        check(not bad, f"rows-sourced:{page}({len(rows)} rows)",
              f"rows without an http link: {bad}")
        # flagging present on table pages
        if page in ("restaurants.html", "hotels.html", "activities.html",
                    "booking.html", "flagged-for-review.html"):
            check("badge-unverified" in html, f"flags:{page}",
                  "no unverified badges on a table page")

    # 7. verification.json
    vpath = ROOT / "data/session-c88d116c/verification.json"
    if vpath.is_file():
        try:
            v = json.loads(vpath.read_text(encoding="utf-8"))
            for key in ("session", "as_of", "hotels", "restaurants",
                        "activities", "transit", "irregularities"):
                check(key in v, f"verify-key:{key}", f"missing key {key}")
            check(isinstance(v.get("restaurants"), list) and len(v["restaurants"]) == 24,
                  "verify:24-restaurants",
                  f"expected 24, got {len(v.get('restaurants', []))}")
            check(isinstance(v.get("activities"), list) and len(v["activities"]) == 12,
                  "verify:12-activities",
                  f"expected 12, got {len(v.get('activities', []))}")
            check(isinstance(v.get("hotels"), list) and len(v["hotels"]) == 8,
                  "verify:8-hotels",
                  f"expected 8, got {len(v.get('hotels', []))}")
        except json.JSONDecodeError as e:
            check(False, "verify:json", f"invalid JSON: {e}")

    # 8. mobile CSS basics
    css = (ROOT / "assets/css/style.css").read_text(encoding="utf-8") \
        if (ROOT / "assets/css/style.css").is_file() else ""
    check(".table-wrap" in css and "overflow-x" in css, "css:table-wrap",
          ".table-wrap scroll styles missing")
    check("@media" in css and "nav-toggle" in css, "css:mobile-nav",
          "mobile nav media query missing")

    # 9. row counts on pages
    def body_rows(page: str) -> int:
        n = 0
        for b in re.findall(r"<tbody>(.*?)</tbody>", texts.get(page, ""), re.S):
            n += len(re.findall(r"<tr>", b))
        return n

    check(body_rows("restaurants.html") >= 24, "rows:restaurants>=24",
          f"found {body_rows('restaurants.html')}")
    check(body_rows("activities.html") >= 12, "rows:activities>=12",
          f"found {body_rows('activities.html')}")
    check(body_rows("hotels.html") >= 11, "rows:hotels>=11",
          f"found {body_rows('hotels.html')}")

    print(f"PASS {len(passes)} checks")
    for f in failures:
        print(f"FAIL {f}")
    print("RESULT:", "PASS" if not failures else f"FAIL ({len(failures)})")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
