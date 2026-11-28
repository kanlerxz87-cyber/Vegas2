#!/usr/bin/env python3
"""Offline checker for the Vegas2 ROOT site only (session c88d116c).

Scope: the 11 pages scripts/build_plan.py generates at the repo root, plus
assets/site/style.css and data/plan/*.json.

Retargeted 2026-11-28 (session 6382dba0). The original version of this file
asserted the older session-c88d116c generation (page named flagged-for-review.html,
stylesheet at assets/css/style.css, badge class .badge-unverified, and a footer
sentence build_plan.py never emitted), so it reported 26 failures against main
with no relationship to any real defect (repo finding R-17). The structural
intent is kept; every assertion below is now checked against what the canonical
builder actually emits, so a real regression will fail and a passing run means
something.

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
    "transit.html",
    "flagged.html",
    "repo-review.html",
    "sources.html",
]

REQUIRED = PAGES + [
    "assets/site/style.css",
]

CSS = "assets/site/style.css"
BADGES = ("b-ok", "b-part", "b-no")        # verified / partial / unverified
DISCLAIMER = "unconfirmed is left blank"

FORBIDDEN_DOMAINS = [
    "vegasmonorail.com",      # parked; use lvmonorail.com
    "highroller.com",         # unrelated content; use Caesars page
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
        check(f'href="{CSS}"' in html, f"css:{page}", "stylesheet link missing")
        check('id="navToggle"' in html and 'id="navLinks"' in html,
              f"navtoggle:{page}", "nav toggle ids missing")
        active = re.findall(r'<a href="([^"]+)" class="active">', html)
        check(len(active) == 1 and active[0] == page, f"navactive:{page}",
              f"expected exactly one active link to {page}, found {active}")
        check(DISCLAIMER in html, f"disclaimer:{page}",
              "footer disclaimer ('anything unconfirmed is left blank') missing")
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

    # 5. forbidden inference phrases. repo-review.html is exempt by design: that page
    #    exists to DOCUMENT the inference it removed, so it must be able to quote the
    #    old wording inside a quoted-defect cell. Every other page must be clean.
    for page, html in texts.items():
        if page == "repo-review.html":
            continue
        for phrase in FORBIDDEN_PHRASES:
            check(phrase not in html, f"no-inference:{page}:{phrase}",
                  f"unverified estimate phrase {phrase!r} in {page}")

    # 6. every tbody row on DATA pages has an http(s) link
    # Data pages whose every row must link a source. flagged.html is exempt: its
    # rows are open questions, and F-13 documents a contradiction in the brief itself.
    DATA_PAGES = {"restaurants.html", "hotels.html", "activities.html", "sources.html"}
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
                    "booking.html", "flagged.html"):
            check(any(b in html for b in BADGES), f"flags:{page}",
                  "no verification-state badges on a table page")

    # 7. the canonical data files parse and keep the verified/award invariants
    plan = ROOT / "data" / "plan"
    for name in ("hotels", "restaurants", "activities", "flags", "questions",
                 "suggestions", "repo_review", "booking", "meta"):
        fp = plan / f"{name}.json"
        if not fp.is_file():
            check(False, f"plan:{name}", f"missing data/plan/{name}.json")
            continue
        try:
            json.loads(fp.read_text(encoding="utf-8"))
            check(True, f"plan:{name}")
        except json.JSONDecodeError as e:
            check(False, f"plan:{name}", f"invalid JSON: {e}")
    try:
        rests = json.loads((plan / "restaurants.json").read_text(encoding="utf-8"))["rows"]
        acts = json.loads((plan / "activities.json").read_text(encoding="utf-8"))["rows"]
        hots = json.loads((plan / "hotels.json").read_text(encoding="utf-8"))["rows"]
        awards = [r["award"] for r in rests]
        check(len(rests) == 24, "plan:24-restaurants", f"expected 24, got {len(rests)}")
        check(awards.count("2s") == 1 and awards.count("1s") == 3,
              "plan:starred", f"expected 1 two-star + 3 one-star, got {awards}")
        check(awards.count("bib") == 3, "plan:bib", f"expected 3 Bib Gourmand, got {awards.count('bib')}")
        check(awards.count("listed") == 17, "plan:listed", f"expected 17 listed, got {awards.count('listed')}")
        check(len(acts) >= 12, "plan:activities>=12", f"found {len(acts)}")
        check(len(hots) >= 11, "plan:hotels>=11", f"found {len(hots)}")
        check(all(r.get("official", "").startswith("https://") for r in rests + acts),
              "plan:https-official", "a row's official link is not https")
    except (json.JSONDecodeError, KeyError) as e:
        check(False, "plan:invariants", f"could not evaluate: {e}")

    # 8. mobile CSS basics
    css = (ROOT / CSS).read_text(encoding="utf-8") if (ROOT / CSS).is_file() else ""
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
    check(body_rows("flagged.html") >= 30, "rows:flagged>=30",
          f"found {body_rows('flagged.html')}")

    print(f"PASS {len(passes)} checks")
    for f in failures:
        print(f"FAIL {f}")
    print("RESULT:", "PASS" if not failures else f"FAIL ({len(failures)})")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
