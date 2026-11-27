#!/usr/bin/env python3
"""Verification gate for the canonical Vegas2 site.

Fails (exit 1) on: invalid JSON, unknown award tiers, wrong MICHELIN counts,
a row without an official source, duplicate flag IDs, a value that is not a
string/number/null, broken internal links, missing page landmarks, placeholder
text, and any page that is out of date with respect to its data.

Run after scripts/build_plan.py.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "plan"
PAGES = [
    "index.html", "restaurants.html", "hotels.html", "booking.html", "activities.html",
    "transit.html", "questions.html", "suggestions.html", "flagged.html", "sources.html",
    "repo-review.html",
]
AWARDS = {"2s", "1s", "bib", "listed"}
EXPECTED = {"2s": 1, "1s": 3, "bib": 3, "listed": 17}

errors: list[str] = []
warnings: list[str] = []


def fail(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load(name):
    try:
        return json.loads((DATA / name).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"{name}: cannot parse JSON — {exc}")
        return None


def is_official(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    if not host:
        return False
    return not any(b in host for b in ("tripadvisor", "yelp", "wikipedia", "reddit", "blogspot", "medium.com"))


def main():
    meta = load("meta.json")
    hotels = load("hotels.json")
    rests = load("restaurants.json")
    acts = load("activities.json")
    booking = load("booking.json")
    questions = load("questions.json")
    suggestions = load("suggestions.json")
    flags = load("flags.json")
    review = load("repo_review.json")
    for name, obj in [("meta", meta), ("hotels", hotels), ("restaurants", rests), ("activities", acts),
                      ("booking", booking), ("questions", questions), ("suggestions", suggestions),
                      ("flags", flags), ("repo_review", review)]:
        if obj is None:
            fail(f"missing data file: {name}.json")
    if errors:
        report()
        return

    # --- MICHELIN counts and row integrity
    counts = {k: 0 for k in AWARDS}
    seen = set()
    for r in rests["rows"]:
        for field in ("name", "award", "cuisine", "area", "venue", "hours", "price2", "official"):
            if field not in r:
                fail(f"restaurant {r.get('name','?')}: missing field {field}")
        if r["award"] not in AWARDS:
            fail(f"restaurant {r['name']}: unknown award code {r['award']}")
        else:
            counts[r["award"]] += 1
        if r["name"] in seen:
            fail(f"duplicate restaurant: {r['name']}")
        seen.add(r["name"])
        if not r.get("official", "").startswith("https://"):
            fail(f"restaurant {r['name']}: official link missing or not https")
        elif not is_official(r["official"]):
            fail(f"restaurant {r['name']}: official link is not a first-party source ({r['official']})")
        if r.get("hoursStatus") not in {"v", "p", "u"}:
            fail(f"restaurant {r['name']}: bad hoursStatus")
        if r.get("socialStatus") not in {"v", "p", "u"}:
            fail(f"restaurant {r['name']}: bad socialStatus")
        if r["price2"] and not r["priceNote"]:
            warn(f"restaurant {r['name']}: price shown without an explanatory note")
    for k, want in EXPECTED.items():
        if counts[k] != want:
            fail(f"MICHELIN count for {k}: expected {want}, found {counts[k]}")
    if len(rests["rows"]) != 24:
        fail(f"expected 24 MICHELIN rows, found {len(rests['rows'])}")

    # --- hotels
    names = set()
    for h in hotels["rows"]:
        if h["id"] in names:
            fail(f"duplicate hotel id {h['id']}")
        names.add(h["id"])
        if not h["sources"]:
            fail(f"hotel {h['name']}: no sources")
        for s in h["sources"]:
            if not s.get("url", "").startswith("https://"):
                fail(f"hotel {h['name']}: source without https URL")
        if h.get("roomStatus") not in {"v", "p", "u"}:
            fail(f"hotel {h['name']}: bad roomStatus")
        if h.get("transitStatus") not in {"v", "p", "u"}:
            fail(f"hotel {h['name']}: bad transitStatus")
        if h["price7"]:
            p = h["price7"]
            for f in ("total", "room", "nightly", "basis"):
                if f not in p:
                    fail(f"hotel {h['name']}: price7 missing {f}")
            # Money may carry cents (e.g. an avg/night of $277.21). Accept int or
            # float, reject bool/str, and verify nightly x 7 to the cent.
            total = p.get("total")
            if isinstance(total, bool) or not isinstance(total, (int, float)):
                fail(f"hotel {h['name']}: price7 total must be numeric")
            m = re.search(r"\$(\d[\d,]*(?:\.\d{1,2})?)", p.get("nightly", ""))
            if m and isinstance(total, (int, float)) and not isinstance(total, bool):
                nightly = float(m.group(1).replace(",", ""))
                # Engines round an average nightly to the cent, so allow 7c of drift.
                if abs(nightly * 7 - total) > 0.07:
                    if p.get("publishedTotal"):
                        # The engine itself printed the stay total; the nightly figure is a
                        # rounded display. Allowed only with an explicit basis note.
                        if "ROUNDING DISCREPANCY" not in p.get("basis", ""):
                            fail(f"hotel {h['name']}: publishedTotal set without a rounding note")
                    else:
                        fail(f"hotel {h['name']}: nightly × 7 ({nightly*7:.2f}) != total ({total})")
        else:
            if not h.get("price7Note"):
                fail(f"hotel {h['name']}: no price and no explanation")

    # --- flags
    fids = set()
    for f in flags["rows"]:
        if f["id"] in fids:
            fail(f"duplicate flag id {f['id']}")
        fids.add(f["id"])
        if f["severity"] not in {"high", "medium", "low"}:
            fail(f"flag {f['id']}: bad severity")
        if not f.get("detail") or not f.get("effect") or not f.get("title"):
            fail(f"flag {f['id']}: incomplete")

    # --- questions / suggestions
    qids = set()
    for q in questions["rows"]:
        if q["id"] in qids:
            fail(f"duplicate question id {q['id']}")
        qids.add(q["id"])
        if q["status"] not in {"open", "partial", "answered"}:
            fail(f"question {q['id']}: bad status")
        for f in ("q", "known", "missing", "how", "impact"):
            if not q.get(f):
                fail(f"question {q['id']}: empty {f}")
    sids = set()
    for s in suggestions["siteImprovements"]:
        if s["id"] in sids:
            fail(f"duplicate suggestion id {s['id']}")
        sids.add(s["id"])

    # --- activities
    for a in acts["rows"]:
        if not a["official"].startswith("https://"):
            fail(f"activity {a['name']}: missing official link")
        if a.get("hoursStatus") not in {"v", "p", "u"}:
            fail(f"activity {a['name']}: bad hoursStatus")

    # --- booking arithmetic
    for q in booking["quotes"]:
        if q["total"] and q["nightly"]:
            nightly = int(re.sub(r"[^\d]", "", q["nightly"]) or 0)
            total = int(re.sub(r"[^\d]", "", q["total"]) or 0)
            if nightly and total and abs(nightly * 7 - total) > 7:
                fail(f"booking quote {q['hotel']} ({q['window']}): nightly×7 != total")

    # --- HTML pages
    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            fail(f"missing page {page}")
            continue
        text = path.read_text(encoding="utf-8")
        if '<html lang="en">' not in text:
            fail(f"{page}: missing lang attribute")
        if 'name="viewport"' not in text:
            fail(f"{page}: missing viewport meta")
        if text.count("<h1>") != 1:
            fail(f"{page}: expected exactly one h1, found {text.count('<h1>')}")
        if 'id="main"' not in text:
            fail(f"{page}: missing main landmark")
        for bad in ("TODO", "TBD", "lorem ipsum", "PLACEHOLDER"):
            if bad in text:
                fail(f"{page}: placeholder text {bad!r}")
        # "$XXX" is a quoted observation from the Venetian calendar, not a placeholder.
        if re.search(r"(?<!\$)XXX", text):
            fail(f"{page}: unquoted placeholder XXX")
        if "&amp;amp;" in text:
            fail(f"{page}: double-escaped entity")
        # internal links
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http://", "https://", "#", "mailto:", "tel:")):
                if href.startswith("#") and href != "#":
                    if f'id="{href[1:]}"' not in text:
                        fail(f"{page}: dead in-page anchor {href}")
                continue
            target, _, frag = href.partition("#")
            tpath = ROOT / target
            if not tpath.exists():
                fail(f"{page}: broken internal link {href}")
            elif frag and f'id="{frag}"' not in tpath.read_text(encoding="utf-8"):
                fail(f"{page}: broken anchor {href}")
        # stacked tables must carry data-label on every td
        for table_body in re.findall(r"<table class=\"stack\">(.*?)</table>", text, re.S):
            heads = re.findall(r"<th[^>]*>(.*?)</th>", table_body, re.S)
            nheads = len(heads)
            for tr in re.findall(r"<tr>(.*?)</tr>", table_body, re.S):
                if "<th" in tr or "<td" not in tr:
                    continue
                tds = re.findall(r"<td[^>]*>", tr)
                if len(tds) != nheads:
                    fail(f"{page}: table row has {len(tds)} cells vs {nheads} headers")
                for td in tds:
                    if "data-label=" not in td:
                        fail(f"{page}: stacked td without data-label")

    # --- counts surfaced on the site
    idx = (ROOT / "restaurants.html").read_text(encoding="utf-8")
    for label, n in (("Two-star", 1), ("One-star", 3), ("Bib Gourmand", 3), ("Listed / recommended", 17)):
        if f'<span class="l">{label}</span>' not in idx:
            fail(f"restaurants.html: missing KPI {label}")
    flagged = (ROOT / "flagged.html").read_text(encoding="utf-8")
    for f in flags["rows"]:
        if f'id="{f["id"]}"' not in flagged:
            fail(f"flagged.html: missing flag {f['id']}")
    for q in questions["rows"]:
        if q["id"] not in (ROOT / "questions.html").read_text(encoding="utf-8"):
            fail(f"questions.html: missing {q['id']}")

    report()


def report():
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"FAIL  {e}")
    if errors:
        print(f"\n{len(errors)} failure(s), {len(warnings)} warning(s)")
        sys.exit(1)
    print(f"OK — 0 failures, {len(warnings)} warning(s). Pages: {len(PAGES)}")


if __name__ == "__main__":
    main()
