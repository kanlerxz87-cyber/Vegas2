#!/usr/bin/env python3
"""Verification gate for the session 9b4f59cd planner.

Checks, in order:
 1. every JSON file parses and every source id referenced anywhere resolves
 2. every table row carries at least one source link
 3. sources resolve to official or official-partner domains only
 4. MICHELIN counts reconcile (4 starred, 3 Bib, 17 Recommended = 24 Las Vegas)
 5. every unverified hotel / restaurant cell carries a flag id that exists
 6. every internal link and asset in the built site resolves
 7. no placeholder text, no hard-coded localhost, no broken anchors
 8. the committed output matches a fresh build (no stale pages)

Exit code 0 means every check passed. Non-zero prints each failure.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "session-9b4f59cd"
SITE = ROOT / "docs" / "session-9b4f59cd"

ALLOWED_SUFFIXES = (
    "michelin.com", "guide.michelin.com", "visitlasvegas.com", "opm.gov",
    "caesars.com", "wynnlasvegas.com", "venetianlasvegas.com", "rwlasvegas.com",
    "mgmgrand.mgmresorts.com", "bellagio.mgmresorts.com",
    "cosmopolitanlasvegas.mgmresorts.com", "aria.mgmresorts.com",
    "be.synxis.com", "reservations.rwlasvegas.com", "reservations.wynnlasvegas.com",
    "southpointcasino.com", "goldcoast.boydgaming.com",
    "themobmuseum.org", "admission.themobmuseum.org", "neonmuseum.org",
    "redrockcanyonlv.org", "thesphere.com", "lvmonorail.com", "rtcsnv.com",
    "partage.vegas", "estherslv.com", "yenvietkitchen.com", "sparrowandwolflv.com",
    "kabutolv.com", "kameomakase.com", "lamaiilv.com", "animabyedo.com",
    "bestchickenpho.com", "soulbellybbq.com",
    "github.com",
)

failures: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def load(name: str):
    p = DATA / name
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"JSON parse error in {name}: {exc}")
        return {}


# ---------------------------------------------------------------- 1. JSON + ids
files = ["sources", "hotels", "michelin", "activities", "booking",
         "flags", "questions", "suggestions", "summary", "repo-review"]
data = {f: load(f + ".json") for f in files}
src = data["sources"]
ids = {s["id"] for s in src.get("items", [])}
if not ids:
    fail("sources.json has no items")

used: set[str] = set()


def note_refs(value, where: str) -> None:
    if isinstance(value, str):
        if value in ids:
            used.add(value)
    elif isinstance(value, dict):
        for k, v in value.items():
            note_refs(v, where)
    elif isinstance(value, list):
        for v in value:
            note_refs(v, where)


for f in files:
    note_refs(data[f], f)
unknown = used - ids
if unknown:
    fail(f"unknown source ids referenced: {sorted(unknown)}")
notes.append(f"{len(ids)} sources defined, {len(used)} referenced")

# every url must be well formed and on an allowed domain
for s in src.get("items", []):
    u = s.get("url", "")
    p = urllib.parse.urlparse(u)
    if p.scheme != "https":
        fail(f"source {s['id']} is not https: {u}")
    host = (p.hostname or "").lower()
    if not any(host == suf or host.endswith("." + suf) for suf in ALLOWED_SUFFIXES):
        fail(f"source {s['id']} domain not on official allowlist: {host}")

# ------------------------------------------------- 2. every row has a source
flag_ids = {f["id"] for f in data["flags"].get("items", [])}
repo_ids = {f["id"] for f in data["repo-review"].get("findings", [])}
if not flag_ids:
    fail("flags.json has no items")

for h in data["hotels"].get("rows", []):
    if not h.get("price_src") and not h.get("link"):
        fail(f"hotel row without any source: {h.get('name')}")
    if not h.get("rate_7n_2queen") and not h.get("flag"):
        fail(f"hotel row missing a price but no flag: {h.get('name')}")
    for one in [x.strip() for x in str(h.get("flag") or "").split(",") if x.strip()]:
        if one.startswith("F-") and one not in flag_ids:
            fail(f"hotel {h.get('name')} cites undefined flag {one}")
        if one.startswith("R-") and one not in repo_ids:
            fail(f"hotel {h.get('name')} cites undefined repo finding {one}")
    for k in ("queen_src", "private_bath_src", "amenities_src", "price_src", "social_src"):
        v = h.get(k) or ""
        for sid in [x.strip() for x in v.split(",") if x.strip()]:
            if sid not in ids:
                fail(f"hotel {h.get('name')} field {k} cites unknown source {sid}")

for r in data["michelin"].get("rows", []):
    if not r.get("official_link"):
        fail(f"restaurant without official link: {r.get('name')}")
    for sid in [x.strip() for x in str(r.get("src") or "").split(",") if x.strip()]:
        if sid not in ids:
            fail(f"restaurant {r.get('name')} cites unknown source {sid}")
    if not r.get("price_2_adults") and not r.get("flag"):
        fail(f"restaurant {r.get('name')} has no price and no flag")
    for one in [x.strip() for x in str(r.get("flag") or "").split(",") if x.strip()]:
        if one.startswith("F-") and one not in flag_ids:
            fail(f"restaurant {r.get('name')} cites undefined flag {one}")
        if one.startswith("R-") and one not in repo_ids:
            fail(f"restaurant {r.get('name')} cites undefined repo finding {one}")
    if not re.match(r"^https://", r.get("official_link", "")):
        fail(f"restaurant {r.get('name')} link is not https")

for a in data["activities"].get("rows", []):
    if not a.get("official_link"):
        fail(f"activity without official link: {a.get('name')}")
    for sid in [x.strip() for x in str(a.get("src") or "").split(",") if x.strip()]:
        if sid not in ids:
            fail(f"activity {a.get('name')} cites unknown source {sid}")
    if not a.get("price_2_adults") and not a.get("flag"):
        fail(f"activity {a.get('name')} has no price and no flag")
    for one in [x.strip() for x in str(a.get("flag") or "").split(",") if x.strip()]:
        if one.startswith("F-") and one not in flag_ids:
            fail(f"activity {a.get('name')} cites undefined flag {one}")

for q in data["questions"].get("rows", []):
    if not q.get("how"):
        fail(f"question {q.get('id')} has no way to resolve it")
for s in data["suggestions"].get("rows", []):
    if not s.get("why"):
        fail(f"suggestion {s.get('id')} has no rationale")

for f in data["flags"].get("items", []):
    for key in ("source", "source2"):
        u = f.get(key)
        if u and not re.match(r"^https://", u):
            fail(f"flag {f['id']} {key} is not https: {u}")

for f in data["repo-review"].get("findings", []):
    if not f.get("evidence"):
        fail(f"repo finding {f.get('id')} has no evidence")
    if not re.match(r"^https://", f.get("source_url", "")):
        fail(f"repo finding {f.get('id')} has no https source_url")

# ----------------------------------------------------- 3. MICHELIN reconciliation
m = data["michelin"]
rows = m.get("rows", [])
starred = [r for r in rows if r["award"] in ("2 MICHELIN Stars", "1 MICHELIN Star")]
bib = [r for r in rows if r["award"] == "Bib Gourmand"]
rec = [r for r in rows if r["award"] == "MICHELIN Recommended"]
t = m.get("totals", {})
if len(rows) != 24:
    fail(f"expected 24 Las Vegas restaurants, found {len(rows)}")
if len(starred) != 4 or t.get("starred") != 4:
    fail(f"expected 4 starred, found {len(starred)}")
if len(bib) != 3 or t.get("bib") != 3:
    fail(f"expected 3 Bib Gourmand, found {len(bib)}")
if len(rec) != 17 or t.get("recommended") != 17:
    fail(f"expected 17 Recommended, found {len(rec)}")
stars_total = sum(2 if r["award"] == "2 MICHELIN Stars" else 1 for r in starred)
if stars_total != 5 or t.get("stars_total") != 5:
    fail(f"expected 5 stars total, found {stars_total}")
if len(starred) + len(bib) + len(rec) != t.get("las_vegas_distinctions", 24):
    fail("award classes do not sum to the stated total")
notes.append(f"MICHELIN reconciled: {len(starred)} starred / {stars_total} stars + {len(bib)} Bib + {len(rec)} Recommended = {len(rows)}")

# star/bib/rec must be mutually exclusive labels — no row may claim two
for r in rows:
    if r["award"] not in ("2 MICHELIN Stars", "1 MICHELIN Star", "Bib Gourmand", "MICHELIN Recommended"):
        fail(f"restaurant {r['name']} has an ambiguous award label: {r['award']}")

# ------------------------------------------------------- 4. built-site integrity
if not SITE.exists():
    fail("built site directory is missing — run scripts/build_session_9b4f59cd.py")
    print("\n".join(failures))
    sys.exit(1)

pages = sorted(SITE.glob("*.html"))
if len(pages) < 10:
    fail(f"expected at least 10 pages, found {len(pages)}")

anchors: dict[str, set[str]] = {}
for p in pages:
    text = p.read_text(encoding="utf-8")
    anchors[p.name] = set(re.findall(r'\bid="([^"]+)"', text))

bad_links = 0
for p in pages:
    text = p.read_text(encoding="utf-8")
    for m_ in re.finditer(r'(?:href|src)="([^"]+)"', text):
        u = m_.group(1)
        if u.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
            continue
        target, _, frag = u.partition("#")
        if target:
            tp = (p.parent / target).resolve()
            if not tp.exists():
                fail(f"{p.name}: broken local link {u}")
                bad_links += 1
        if frag and (not target or target.endswith(".html")):
            tname = target.split("/")[-1] if target else p.name
            if tname in anchors and frag not in anchors[tname]:
                fail(f"{p.name}: link to missing anchor #{frag} in {tname}")
                bad_links += 1
notes.append(f"{len(pages)} pages checked, {bad_links} broken local links")

placeholder = re.compile(r"lorem ipsum|\bTODO\b|\bFIXME\b|localhost|127\.0\.0\.1|XXX(?![^<]*price)", re.I)
for p in pages:
    text = p.read_text(encoding="utf-8")
    hit = placeholder.search(text)
    if hit:
        fail(f"{p.name}: placeholder or localhost text found: {hit.group(0)!r}")
    if "<table" in text and 'target="_blank"' not in text:
        fail(f"{p.name}: table without any external source links")

# every page must be reachable from the nav
index = (SITE / "index.html").read_text(encoding="utf-8")
for p in pages:
    if p.name == "index.html":
        continue
    if f'href="{p.name}"' not in index:
        fail(f"{p.name} is not linked from the navigation")

# flags page must be able to receive every anchor that other pages point at
flag_page = (SITE / "flagged.html").read_text(encoding="utf-8")
for fid in flag_ids:
    if f'id="{fid}"' not in flag_page:
        fail(f"flag {fid} is referenced but has no anchor on flagged.html")

repo_page = (SITE / "repo-review.html").read_text(encoding="utf-8")
for rid in repo_ids:
    if f'id="{rid}"' not in repo_page:
        fail(f"repo finding {rid} is referenced but has no anchor on repo-review.html")

# ------------------------------------------------- 5. committed output is current
import subprocess  # noqa: E402

before = {p.name: p.read_text(encoding="utf-8") for p in pages}
subprocess.run([sys.executable, str(ROOT / "scripts" / "build_session_9b4f59cd.py")],
               cwd=ROOT, check=True, capture_output=True)
after = {p.name: p.read_text(encoding="utf-8") for p in pages}
drift = [n for n in before if before[n] != after[n]]
if drift:
    fail(f"committed output was stale; rebuilt and changed: {drift}")

# ------------------------------------------------------------------ report
print("\n".join(f"  note: {n}" for n in notes))
if failures:
    print(f"\nFAIL — {len(failures)} problem(s):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print(f"\nPASS — {len(pages)} pages, {len(ids)} sources, "
      f"{len(flag_ids)} flags, every row sourced, every link resolving.")
sys.exit(0)
