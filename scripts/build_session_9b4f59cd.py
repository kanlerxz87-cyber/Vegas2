#!/usr/bin/env python3
"""Build the session 9b4f59cd Las Vegas planner into docs/session-9b4f59cd/.

Reads data/session-9b4f59cd/*.json and writes a self-contained, mobile-first
static site. Standard library only. Every table cell that has no verified value
is rendered as "Unverified" with a link to the flag that explains it.
"""
from __future__ import annotations

import html
import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "session-9b4f59cd"
OUT = ROOT / "docs" / "session-9b4f59cd"


def load(name: str):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


SRC = load("sources.json")
SRC_BY_ID = {s["id"]: s for s in SRC["items"]}
HOTELS = load("hotels.json")
MICHELIN = load("michelin.json")
ACTIVITIES = load("activities.json")
BOOKING = load("booking.json")
FLAGS = load("flags.json")
QUESTIONS = load("questions.json")
SUGGESTIONS = load("suggestions.json")
SUMMARY = load("summary.json")
REVIEW = load("repo-review.json")

E = lambda s: html.escape("" if s is None else str(s))

PAGES = [
    ("index.html", "Home"),
    ("hotels.html", "Hotels"),
    ("michelin.html", "Michelin"),
    ("activities.html", "Activities"),
    ("booking.html", "Booking &amp; cost"),
    ("questions.html", "Questions"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged for review"),
    ("repo-review.html", "Repo review"),
    ("sources.html", "Sources"),
]

CSS = """
:root{--bg:#0d1117;--panel:#161b22;--panel2:#1c2330;--line:#2a3341;--ink:#e6edf3;--dim:#9aa7b4;
--accent:#58c4dc;--ok:#3fb950;--warn:#d29922;--bad:#f85149;--gold:#e3b341;--radius:14px}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
header.top{position:sticky;top:0;z-index:20;background:rgba(13,17,23,.94);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;gap:12px;padding:12px 0}
.brand{font-weight:700;font-size:1.05rem;color:var(--ink);text-decoration:none;white-space:nowrap}
.brand span{color:var(--accent)}
nav.main{margin-left:auto;display:flex;gap:2px;flex-wrap:wrap;justify-content:flex-end}
nav.main a{color:var(--dim);text-decoration:none;font-size:.83rem;padding:6px 9px;border-radius:9px;white-space:nowrap}
nav.main a:hover{background:var(--panel2);color:var(--ink)}
nav.main a[aria-current="page"]{background:var(--accent);color:#04141a;font-weight:700}
.navbtn{display:none;background:var(--panel2);border:1px solid var(--line);color:var(--ink);border-radius:9px;padding:7px 12px;font-size:.95rem;cursor:pointer;margin-left:auto}
@media(max-width:1000px){
 .navbtn{display:block}
 nav.main{display:none;position:absolute;left:0;right:0;top:100%;background:#11161d;border-bottom:1px solid var(--line);padding:10px 16px;flex-direction:column;align-items:stretch}
 nav.main.open{display:flex}
 nav.main a{padding:11px 10px;font-size:.95rem;border-radius:9px}
}
main{padding:26px 0 60px}
h1{font-size:1.75rem;line-height:1.25;margin:.2em 0 .35em;letter-spacing:-.01em}
h2{font-size:1.22rem;margin:2em 0 .6em;padding-bottom:.35em;border-bottom:1px solid var(--line)}
h3{font-size:1rem;margin:1.4em 0 .4em}
p.lead{color:var(--dim);font-size:1.02rem;max-width:74ch}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:18px 0 8px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:14px}
.kpi b{display:block;font-size:1.5rem;line-height:1.15}
.kpi small{color:var(--dim);font-size:.79rem;display:block;margin-top:4px}
.kpi.ok b{color:var(--ok)}.kpi.warn b{color:var(--warn)}.kpi.bad b{color:var(--bad)}.kpi.gold b{color:var(--gold)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;margin:14px 0}
.card h2,.card h3{margin-top:.2em;border:0;padding:0}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-top:12px}
.tile{display:block;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:15px 16px;text-decoration:none;color:var(--ink);transition:border-color .15s,transform .15s}
.tile:hover{border-color:var(--accent);transform:translateY(-1px)}
.tile strong{display:block;color:var(--accent);margin-bottom:4px;font-size:.98rem}
.tile span{color:var(--dim);font-size:.85rem;line-height:1.45}
ul.sum,ul.plain{padding-left:20px;margin:.4em 0}
ul.sum li,ul.plain li{margin:.5em 0}
.tablewrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);border-radius:var(--radius);margin:12px 0;background:var(--panel)}
table{border-collapse:collapse;width:100%;min-width:720px;font-size:.86rem}
caption{caption-side:top;text-align:left;padding:12px 14px 0;color:var(--dim);font-size:.82rem}
th,td{padding:10px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
th{background:var(--panel2);font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:var(--dim);position:sticky;top:0}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:#182030}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.b{display:inline-block;padding:2px 8px;border-radius:999px;font-size:.71rem;font-weight:700;white-space:nowrap;letter-spacing:.02em}
.bv{background:rgba(63,185,80,.16);color:#56d364;border:1px solid rgba(63,185,80,.4)}
.bu{background:rgba(154,167,180,.13);color:var(--dim);border:1px solid var(--line)}
.bp{background:rgba(210,153,34,.16);color:#e3b341;border:1px solid rgba(210,153,34,.4)}
.bx{background:rgba(248,81,73,.14);color:#ff7b72;border:1px solid rgba(248,81,73,.4)}
.bstar2{background:rgba(227,179,65,.18);color:#f2cc60;border:1px solid rgba(227,179,65,.55)}
.bstar1{background:rgba(227,179,65,.12);color:#e3b341;border:1px solid rgba(227,179,65,.35)}
.bbib{background:rgba(88,196,220,.14);color:var(--accent);border:1px solid rgba(88,196,220,.4)}
.brec{background:rgba(154,167,180,.12);color:var(--dim);border:1px solid var(--line)}
.src{font-size:.74rem}
.src a{margin-right:6px;color:var(--accent);text-decoration:none;border-bottom:1px dotted var(--accent)}
.flaglink{font-size:.74rem;color:var(--bad);text-decoration:none;border-bottom:1px dotted var(--bad)}
.muted{color:var(--dim);font-size:.83rem}
.note{background:rgba(88,196,220,.07);border-left:3px solid var(--accent);padding:10px 14px;border-radius:0 8px 8px 0;margin:12px 0;font-size:.87rem;color:#c9d4de}
.warn{background:rgba(210,153,34,.08);border-left:3px solid var(--warn);padding:10px 14px;border-radius:0 8px 8px 0;margin:12px 0;font-size:.87rem}
.bad{background:rgba(248,81,73,.08);border-left:3px solid var(--bad);padding:10px 14px;border-radius:0 8px 8px 0;margin:12px 0;font-size:.87rem}
footer.foot{border-top:1px solid var(--line);padding:22px 0 40px;color:var(--dim);font-size:.8rem}
footer.foot a{color:var(--accent)}
details{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:8px 0}
summary{cursor:pointer;font-weight:600;font-size:.9rem}
details p,details ul{font-size:.86rem;color:#c9d4de}
.pill{display:inline-block;background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:3px 10px;font-size:.75rem;color:var(--dim);margin:2px 4px 2px 0}
@media(max-width:640px){
 h1{font-size:1.42rem}h2{font-size:1.1rem}
 body{font-size:15px}
 .wrap{padding:0 12px}
 .card{padding:14px}
 table{min-width:640px;font-size:.8rem}
 th,td{padding:8px 9px}
}
"""

NAV_JS = """
document.addEventListener('click',function(e){
  var b=document.getElementById('navbtn'),n=document.getElementById('nav');
  if(b&&b.contains(e.target)){n.classList.toggle('open');return}
  if(n&&n.contains(e.target)){n.classList.remove('open')}
});
"""


def page(filename: str, title: str, body: str, subtitle: str = "") -> str:
    links = []
    for href, label in PAGES:
        cur = ' aria-current="page"' if href == filename else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)} · Las Vegas Trip Planner</title>
<meta name="description" content="Source-verified Las Vegas trip plan for two adults, Feb 15 – Mar 23, 2027. Hotels, MICHELIN restaurants, activities and open questions, each row linked to an official source.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top"><div class="wrap"><div class="bar">
<a class="brand" href="index.html">Las Vegas <span>2027</span></a>
<button class="navbtn" id="navbtn" aria-label="Toggle navigation" aria-expanded="false">&#9776; Menu</button>
<nav class="main" id="nav" aria-label="Main">{''.join(links)}</nav>
</div></div></header>
<main class="wrap">
{body}
</main>
<footer class="foot"><div class="wrap">
<p><strong>Data captured {E(SRC['as_of'])} from official sources only.</strong> Hotel and restaurant prices are dynamic and will change. A cell is filled only when an official source confirmed it; everything else says <span class="b bu">Unverified</span> and links to the flag that explains why.</p>
<p><a href="index.html">Home</a> · <a href="flagged.html">Flagged for review</a> · <a href="sources.html">All sources</a> · <a href="https://github.com/kanlerxz87-cyber/Vegas2" target="_blank" rel="noopener">Repository</a></p>
</div></footer>
<script>{NAV_JS}</script>
</body>
</html>
"""


SHORT = {
    "ML": "MICHELIN release", "LVCVA": "Visit Las Vegas", "GMICHELIN": "MICHELIN Guide",
    "OPM": "OPM holidays", "SP_BOOK": "South Point rates", "SP_BOOK3": "South Point 3nt",
    "SP_BOOK14": "South Point 14nt", "SP_BOOK222": "South Point Feb 22",
    "SP_ROOMS": "South Point rooms",
    "CLV_BOOK": "Caesars Palace rates", "CLV_BOOK3": "Caesars 3nt", "CLV_BOOK14": "Caesars 14nt",
    "CLV_BOOK222": "Caesars Feb 22", "CLV_BOOK315": "Caesars Mar 15",
    "FLV_BOOK": "Flamingo rates", "FLV_BOOK3": "Flamingo 3nt", "FLV_BOOK14": "Flamingo 14nt",
    "FLV_BOOK222": "Flamingo Feb 22", "FLV_BOOK315": "Flamingo Mar 15",
    "PLV_BOOK": "Paris rates", "PLV_BOOK14": "Paris 14nt", "PLV_BOOK315": "Paris Mar 15",
    "RW_BOOK": "Resorts World rates", "WYNN_BOOK": "Wynn rates", "WYNN_ROOM": "Wynn room",
    "VEN_ROOM": "Venetian suite", "VEN_BOOK": "Venetian calendar", "BEL_ROOM": "Bellagio room",
    "JR": "Joel Robuchon page", "LAT": "L'Atelier page", "EBJA": "e by Jose Andres page",
    "GS": "Guy Savoy page", "GS_MENU": "Guy Savoy menu", "CP": "China Poblano page",
    "BOU": "Bouchon page", "COTE": "COTE page", "MOTT": "Mott 32 page", "WL": "Wing Lei page",
    "MM": "Michael Mina page", "SS": "Stubborn Seed page", "PPP": "Ping Pang Pong page",
    "PART": "Partage site", "PART_MENU": "Partage menus", "ESTHER": "Esther's Kitchen site",
    "YEN": "Yen Viet site", "SW": "Sparrow + Wolf site",
    "SPHERE": "Sphere shows", "HR": "High Roller page", "MOB": "Mob Museum",
    "MOB_TIX": "Mob Museum tickets", "NEON": "Neon Museum", "CONS": "Bellagio Conservatory",
    "FOUNT": "Bellagio Fountains", "RRC": "Red Rock Canyon", "RRC_HOME": "Red Rock Canyon",
    "MONO": "Monorail fares", "MONO_ST": "Monorail stations",
    "RTC_FARE": "RTC fares", "RTC": "RTC trip planner",
}



def social_cell(raw: str, note: str = "") -> str:
    """Render one or more social URLs (separated by ' · ') as clickable links."""
    if not raw:
        return unv("F-14")
    parts = []
    for url in [u.strip() for u in str(raw).split("·") if u.strip()]:
        host = url.split("//")[-1].split("/")[0].replace("www.", "")
        name = ("Instagram" if "instagram" in host else "TikTok" if "tiktok" in host
                else "YouTube" if "youtube" in host else "Facebook" if "facebook" in host else host)
        parts.append(f'<a class="src" href="{E(url)}" target="_blank" rel="noopener">{E(name)}</a>')
    out = '<span class="b bv">Official</span> ' + " · ".join(parts)
    if note:
        out += f'<br><span class="muted" style="font-size:.74rem">{E(note)}</span>'
    return out

def src_links(ids: str, sep: str = " · ") -> str:
    out = []
    for sid in [s.strip() for s in (ids or "").split(",") if s.strip()]:
        s = SRC_BY_ID.get(sid)
        if not s:
            out.append(f'<span class="b bx">{E(sid)}?</span>')
            continue
        label = SHORT.get(sid, s["label"][:26] + "…")
        out.append(f'<a href="{E(s["url"])}" target="_blank" rel="noopener" title="{E(s["label"])}">{E(label)}</a>')
    return sep.join(out)


def flag_link(fid: str, sep: str = " ") -> str:
    """Render one or more flag references (comma separated) as readable links."""
    if not fid:
        return ""
    parts = []
    for one in [x.strip() for x in str(fid).split(",") if x.strip()]:
        if one.startswith("F-"):
            parts.append(f'<a class="flaglink" href="flagged.html#{E(one)}">{E(one)}</a>')
        elif one.startswith("R-"):
            parts.append(f'<a class="flaglink" href="repo-review.html#{E(one)}">{E(one)}</a>')
    return sep.join(parts)


def unv(fid: str = "", text: str = "Unverified") -> str:
    fl = f" {flag_link(fid)}" if fid else ""
    return f'<span class="b bu">{E(text)}</span>{fl}'


def val(text, fid="", ok_label="Verified") -> str:
    if text:
        badge = f'<span class="b bv">{E(ok_label)}</span> ' if ok_label else ""
        return badge + E(text)
    return unv(fid)


def award_badge(a: str) -> str:
    cls = {"star2": "bstar2", "star1": "bstar1", "bib": "bbib", "rec": "brec"}.get(
        {"2 MICHELIN Stars": "star2", "1 MICHELIN Star": "star1",
         "Bib Gourmand": "bib"}.get(a, "rec"), "brec")
    return f'<span class="b {cls}">{E(a)}</span>'


# --------------------------------------------------------------------------- pages
def build_index() -> str:
    kpis = [
        ("gold", "24", "MICHELIN distinctions in Las Vegas (2026 Guide)"),
        ("gold", "4", "Starred restaurants · 5 stars total"),
        ("ok", "$581", "Cheapest verified 7-night stay (Flamingo, derived, excl. tax)"),
        ("ok", "$2,039", "Cheapest verified 14-night stay (South Point, hotel-issued)"),
        ("warn", "5 of 10", "Hotels that returned any verified 2027 price"),
        ("bad", "16", "Items flagged for review"),
    ]
    kpi_html = "".join(
        f'<div class="kpi {c}"><b>{v}</b><small>{E(l)}</small></div>' for c, v, l in kpis)

    head = "".join(
        f'<li><strong>{E(h["k"])}.</strong> {E(h["v"])} <span class="src">{src_links(h["src"])}</span></li>'
        for h in SUMMARY["headline"])

    gaps = "".join(f"<li>{E(g)}</li>" for g in SUMMARY["biggest_gaps"])
    path = "".join(f"<li>{E(p)}</li>" for p in SUMMARY["recommended_path"])

    tiles = [
        ("hotels.html", "Hotels", "10 candidates ranked, every verified 2027 rate, bed and bathroom checks, and the 7-night totals that are real versus derived."),
        ("michelin.html", "MICHELIN restaurants", "All 24 Las Vegas 2026 distinctions with stars vs Bib vs Recommended, clusters, hours, and prices for two."),
        ("activities.html", "Activities &amp; transport", "Nine things to do with official hours and ticket prices, plus the monorail and bus fares."),
        ("booking.html", "Booking &amp; cost", "3, 7 and 14-night prices side by side across five date windows, and the honest answer on when to book."),
        ("questions.html", "Questions", "12 questions that must be answered before a booking decision is reasonable — what we know, what is missing, how to close it."),
        ("suggestions.html", "Suggestions", "12 proposed changes, ranked by effort and impact. Nothing is implemented until you choose."),
        ("flagged.html", "Flagged for review", "16 conflicts, missing values and brief mismatches, each with its evidence and a link."),
        ("repo-review.html", "Repo review", f"{len(REVIEW['findings'])} findings from a line-by-line audit of the repository and its deployment."),
        ("sources.html", "Sources", f"{len(SRC['items'])} sources, every one linked, and the rule used to decide what counts as verified."),
    ]
    tile_html = "".join(
        f'<a class="tile" href="{h}"><strong>{t}</strong><span>{E(d)}</span></a>' for h, t, d in tiles)

    body = f"""
<h1>Las Vegas, February–March 2027</h1>
<p class="lead">A source-verified plan for two adults. Every number below was read from an official website on {E(SRC['as_of'])} and is linked. Where no official source could confirm a value it is blank and flagged — nothing is estimated.</p>
<div class="kpis">{kpi_html}</div>

<div class="card">
<h2>Executive summary</h2>
<ul class="sum">{head}</ul>
<div class="note"><strong>How to read this site.</strong> <span class="b bv">Verified</span> means an official page confirmed it.
<span class="b bp">Derived</span> means it is the hotel's own published nightly rate multiplied by the number of nights, with the multiplication shown.
<span class="b bu">Unverified</span> means we could not confirm it and left it blank. Each blank carries a flag ID such as <a class="flaglink" href="flagged.html#F-02">F-02</a> that explains the gap.</div>
</div>

<div class="card">
<h2>The four things this plan turns on</h2>
<ol class="plain">
<li><strong>Dates.</strong> Feb 15–22, 2027 was the cheapest week tested at every hotel that quoted several windows — and it matches the 7-night cost basis in the brief. Mar 15–22 was the most expensive (Caesars $310 vs $209 a night).</li>
<li><strong>Money.</strong> Only five hotels returned a price at all. The cheapest 2-queen room verified is Flamingo at $83 a night ($581 for 7 nights, before tax). Only Resorts World gave a true all-in total: $2,434.84.</li>
<li><strong>MICHELIN.</strong> Four starred restaurants exist, and three of them sit inside MGM Grand, Caesars Palace and The Cosmopolitan. The largest cluster (4) is at The Venetian, but none of those four is starred.</li>
<li><strong>Travel.</strong> There is no subway in Las Vegas. Restaurants are reachable by bus, monorail or car, and no official source publishes door-to-door minutes — so the one-hour rule is presented as route availability, not a minute count.</li>
</ol>
</div>

<div class="card">
<h2>Recommended path</h2>
<ul class="sum">{path}</ul>
</div>

<div class="card">
<h2>What is still missing</h2>
<ul class="sum">{gaps}</ul>
<p class="muted">All of it is tracked on the <a href="flagged.html">Flagged for review</a> page with sources, and turned into answerable questions on the <a href="questions.html">Questions</a> page.</p>
</div>

<h2>Go to a section</h2>
<div class="tiles">{tile_html}</div>

<div class="card">
<h2>Scope and rule</h2>
<p class="muted">Trip window Feb 15 – Mar 23, 2027. Preferred dates Feb 15–18, 2027 (3 nights). Five hotels quoted exact 2027 dates; MGM Grand, The Cosmopolitan and Bellagio returned errors and are flagged, not guessed. Restaurant prices are shown only where the venue publishes them, multiplied by two diners and labelled as such.</p>
<p class="muted">This site is isolated at <code>/session-9b4f59cd/</code> and does not modify any other session's pages or the shared landing page.</p>
</div>
"""
    return page("index.html", "Home", body)


def build_hotels() -> str:
    rows = []
    for h in HOTELS["rows"]:
        price_cell = ""
        if h["rate_7n_2queen"] and h["total_7n_2queen"]:
            price_cell = (f'<span class="b bv">Verified</span> {E(h["rate_7n_2queen"])}<br>'
                          f'<strong>{E(h["total_7n_2queen"])}</strong>')
        elif h["rate_7n_2queen"]:
            price_cell = f'<span class="b bp">Partial</span> {E(h["rate_7n_2queen"])} {flag_link(h["flag"])}'
        else:
            price_cell = unv(h["flag"], "No verified price")
        rows.append(f"""<tr>
<td class="num">{h['rank']}</td>
<td><strong>{E(h['name'])}</strong><br><span class="muted">{E(h['area'])}</span><br>
<a class="src" href="{E(h['link'])}" target="_blank" rel="noopener">official site</a></td>
<td class="num"><strong>{h['michelin_in_resort']}</strong><br><span class="muted">{h['michelin_stars_in_resort']} ★</span><br><span class="muted" style="font-size:.74rem">{E(h['michelin_list'])}</span></td>
<td>{val(h['queen_or_bigger'], h['flag'])}</td>
<td>{val(h['private_bath'], h['flag'])}</td>
<td>{price_cell}<br><span class="src">{src_links(h['price_src'])}</span></td>
<td>{('<span class="b bv">Verified</span> ' + E(h['amenities']) + ' <span class="src">' + src_links(h['amenities_src']) + '</span>') if h['amenities'] else unv(h['flag'])}</td>
<td>{('<span class="b bp">Group account only</span> ' + E(h['social'])) if h['social'] else unv('F-14')}</td>
<td>{E(h['note'])}<br><span class="muted">{E(h['rate_7n_note'])}</span></td>
</tr>""")

    body = f"""
<h1>Hotels</h1>
<p class="lead">Ten candidates, ranked by the number of MICHELIN restaurants inside the same resort, then by verified price. Bed and bathroom requirements are checked against each hotel's own room description — not assumed.</p>

<div class="note"><strong>Ranking rule.</strong> Rank = MICHELIN restaurants on the same property per the official MICHELIN addresses. The one-hour transit test could not be applied because no official source publishes travel times (<a class="flaglink" href="flagged.html#F-16">F-16</a>), so it is not used to rank. Price is a tiebreaker, never an assumption.</div>

<h2>Comparison table</h2>
<div class="tablewrap">
<table>
<caption>All ten hotels, 2 adults, one room. Prices are for Feb 15–22, 2027 (7 nights) unless the notes say otherwise. Captured {E(SRC['as_of'])}.</caption>
<thead><tr>
<th>#</th><th>Hotel</th><th>MICHELIN on site</th><th>Queen or larger</th><th>Private bathroom</th><th>7-night price</th><th>Amenities</th><th>Social</th><th>Notes</th>
</tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</div>

<h2>What the price column really means</h2>
<ul class="sum">
<li><strong>Hotel-issued totals</strong> (South Point $989, Resorts World $2,434.84) come from the hotel's own engine as a multi-night sum. Resorts World's is fully itemised including tax.</li>
<li><strong>Derived totals</strong> (Caesars $1,463, Paris $1,421, Flamingo $581) are the hotel's published nightly rate × 7. They exclude tax and resort-fee tax. The arithmetic is shown so it can be checked.</li>
<li><strong>No total at all</strong> (Wynn, Venetian, MGM Grand, Cosmopolitan, Bellagio) because the rate basis or the rate itself could not be confirmed. <a class="flaglink" href="flagged.html#F-04">F-04</a> <a class="flaglink" href="flagged.html#F-01">F-01</a> <a class="flaglink" href="flagged.html#F-02">F-02</a></li>
</ul>

<h2>Meeting the two room requirements</h2>
<div class="tablewrap">
<table>
<caption>Requirement: queen-sized bed or larger, and a private bathroom. Verified from the hotel's own room description.</caption>
<thead><tr><th>Hotel</th><th>Room verified</th><th>Bed</th><th>Bathroom evidence</th><th>Source</th></tr></thead>
<tbody>
{''.join(f'<tr><td><strong>{E(h["name"])}</strong></td><td>{E((h["queen_or_bigger"] or "—"))}</td><td>{("2 queen beds" if "Queen" in (h["queen_or_bigger"] or "") or "queen" in (h["queen_or_bigger"] or "") else ("1 king" if "King" in (h["queen_or_bigger"] or "") else unv(h["flag"])))}</td><td>{E((h["private_bath"] or "Not confirmed"))}</td><td class="src">{src_links((h["queen_src"]+","+h["private_bath_src"]).strip(",")) if (h["queen_src"] or h["private_bath_src"]) else unv(h["flag"])}</td></tr>' for h in HOTELS["rows"])}
</tbody></table>
</div>
<p class="muted">Resorts World's Hilton Deluxe room page described the bed configuration but not a private bathroom; that single cell is flagged rather than filled (<a class="flaglink" href="flagged.html#F-06">F-06</a> covers the pricing gap for the same property).</p>

<h2>Where each hotel sits relative to the MICHELIN clusters</h2>
<div class="tablewrap">
<table>
<thead><tr><th>Cluster</th><th>Restaurants</th><th>Starred</th><th>Hotel(s) in cluster</th><th>Why it matters</th></tr></thead>
<tbody>{''.join(f'<tr><td><strong>{E(c["cluster"])}</strong></td><td class="num">{c["count"]}</td><td class="num">{c["starred"]}</td><td>{E(c["hotels"])}</td><td class="muted">{E(c["note"])}</td></tr>' for c in MICHELIN["clusters"])}</tbody>
</table>
</div>
"""
    return page("hotels.html", "Hotels", body)


def build_michelin() -> str:
    star_rows, bib_rows, rec_rows = [], [], []
    for r in MICHELIN["rows"]:
        cell = f"""<tr>
<td><strong>{E(r['name'])}</strong><br><a class="src" href="{E(r['official_link'])}" target="_blank" rel="noopener">official page</a></td>
<td>{award_badge(r['award'])}</td>
<td>{E(r['cuisine'])}</td>
<td>{E(r['cluster'])}<br><span class="muted" style="font-size:.74rem">{E(r['address'].split(',')[0])}</span></td>
<td>{('<span class="b bv">Confirmed</span> ' + E(r['days_hours'])) if r['days_hours'] else unv(r['flag'], 'Hours not published')}<br><span class="muted">{E(r['hours_note'])}</span></td>
<td>{('<strong>' + E(r['price_2_adults']) + '</strong><br><span class="muted" style="font-size:.74rem">' + E(r['price_basis']) + '</span>') if r['price_2_adults'] else unv(r['flag'], 'Price not published')}</td>
<td>{social_cell(r['social'], r.get('social_note',''))}</td>
<td class="src">{src_links(r['src'])}</td>
</tr>"""
        if r["award"] in ("2 MICHELIN Stars", "1 MICHELIN Star"):
            star_rows.append(cell)
        elif r["award"] == "Bib Gourmand":
            bib_rows.append(cell)
        else:
            rec_rows.append(cell)

    tot = MICHELIN["totals"]
    body = f"""
<h1>MICHELIN restaurants</h1>
<p class="lead">All {tot['las_vegas_distinctions']} Las Vegas entries in the {E(MICHELIN['edition'])}. Star status, Bib Gourmand and plain Recommended listings are kept strictly separate — they are not the same award.</p>

<div class="kpis">
<div class="kpi gold"><b>{tot['starred']}</b><small>Starred restaurants</small></div>
<div class="kpi gold"><b>{tot['stars_total']}</b><small>Stars in total (one has two)</small></div>
<div class="kpi"><b>{tot['bib']}</b><small>Bib Gourmand</small></div>
<div class="kpi"><b>{tot['recommended']}</b><small>Recommended (listed, no star)</small></div>
<div class="kpi ok"><b>{tot['las_vegas_distinctions']}</b><small>Total distinctions</small></div>
</div>

<div class="warn"><strong>Two official sources disagree.</strong> The MICHELIN press release names three Las Vegas Bib Gourmands; the Visit Las Vegas guide page describes four. The star count is identical in both. This site follows the MICHELIN release for award class and uses the DMO list only for discovery. See <a class="flaglink" href="flagged.html#F-03">F-03</a>.</div>

<h2>Starred restaurants</h2>
<div class="tablewrap"><table>
<caption>Four restaurants hold MICHELIN stars. Restaurant de Joël Robuchon holds two.</caption>
<thead><tr><th>Restaurant</th><th>Award</th><th>Cuisine</th><th>Cluster / address</th><th>Open days &amp; hours</th><th>Typical cost, 2 adults</th><th>YouTube / TikTok / Instagram</th><th>Source</th></tr></thead>
<tbody>{''.join(star_rows)}</tbody></table></div>

<h2>Bib Gourmand — great food at moderate price</h2>
<div class="tablewrap"><table>
<caption>Bib Gourmand is a value award, not a star.</caption>
<thead><tr><th>Restaurant</th><th>Award</th><th>Cuisine</th><th>Cluster</th><th>Open days &amp; hours</th><th>Cost, 2 adults</th><th>Social</th><th>Source</th></tr></thead>
<tbody>{''.join(bib_rows)}</tbody></table></div>

<h2>Recommended — listed in the Guide, no star</h2>
<p class="muted">These restaurants appear in the MICHELIN Guide selection but do <strong>not</strong> hold a star and are not Bib Gourmand. They are listed separately so the distinction is never blurred.</p>
<div class="tablewrap"><table>
<thead><tr><th>Restaurant</th><th>Status</th><th>Cuisine</th><th>Cluster</th><th>Open days &amp; hours</th><th>Cost, 2 adults</th><th>Social</th><th>Source</th></tr></thead>
<tbody>{''.join(rec_rows)}</tbody></table></div>

<h2>Clusters — where the restaurants are grouped</h2>
<div class="tablewrap"><table>
<thead><tr><th>Cluster</th><th>Restaurants</th><th>Starred</th><th>Hotel(s) in cluster</th><th>Reading</th></tr></thead>
<tbody>{''.join(f'<tr><td><strong>{E(c["cluster"])}</strong></td><td class="num">{c["count"]}</td><td class="num">{c["starred"]}</td><td>{E(c["hotels"])}</td><td class="muted">{E(c["note"])}</td></tr>' for c in MICHELIN["clusters"])}</tbody></table></div>

<div class="note"><strong>Cost column rule.</strong> A price appears only when the restaurant publishes one. Starred tasting menus are usually per person; the totals here are that price × 2 diners and exclude tax, tip and wine. Where only à-la-carte dish prices exist (Guy Savoy), the range shows what different dish choices would cost rather than pretending there is one set menu.</div>
"""
    return page("michelin.html", "MICHELIN", body)


def build_activities() -> str:
    rows = []
    for a in ACTIVITIES["rows"]:
        rows.append(f"""<tr>
<td><strong>{E(a['name'])}</strong><br><span class="muted">{E(a['category'])}</span><br><a class="src" href="{E(a['official_link'])}" target="_blank" rel="noopener">official page</a></td>
<td><span class="b bv">Confirmed</span> {E(a['when_open'])}<br><span class="muted">{E(a['hours'])}</span></td>
<td class="muted">{E(a['exceptions'])}</td>
<td>{('<strong>' + E(a['price_2_adults']) + '</strong><br><span class="muted" style="font-size:.74rem">' + E(a['price_basis']) + '</span>') if a['price_2_adults'] else unv(a['flag'], 'Price not published')}</td>
<td class="muted">{E(a['why_it_matches'])}</td>
<td class="muted">{E(a['transit_note']) if a['transit_note'] else unv(a['flag'])}</td>
<td>{social_cell(a['social'], a['social_note'])}</td>
<td class="src">{src_links(a['src'])}</td>
</tr>""")

    body = f"""
<h1>Activities &amp; getting around</h1>
<p class="lead">Nine options that were checked against the venue's own page, plus the fares for the two public transport systems. Hours and prices are the venue's published figures captured {E(SRC['as_of'])}.</p>

<div class="tablewrap"><table>
<caption>Every row links to the operator's own website. Blank prices mean the operator does not publish one.</caption>
<thead><tr><th>Activity</th><th>Open / when it runs</th><th>Exceptions</th><th>Cost, 2 adults</th><th>Fits the dates because</th><th>Getting there</th><th>Social</th><th>Source</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>

<h2>The transport reality</h2>
<div class="bad"><strong>Las Vegas has no subway or metro.</strong> The brief asks for Michelin restaurants within an hour by subway or bus. There is no subway. Public options are the RTC bus network (including the Deuce on the Strip) and the privately operated Las Vegas Monorail. Anything not served by those two needs a car or rideshare. See <a class="flaglink" href="flagged.html#F-11">F-11</a>.</div>

<div class="tablewrap"><table>
<caption>Published fares, multiplied by two adults. These are the operator's regular fares.</caption>
<thead><tr><th>System</th><th>Where it goes</th><th>Frequency</th><th>Single</th><th>Day pass</th><th>3-day</th><th>7-day</th><th>Source</th></tr></thead>
<tbody>
<tr><td><strong>RTC Deuce bus</strong></td><td>Strip and Downtown; the only service that also reaches Chinatown/Spring Mountain by local routes</td><td>About every 15 minutes</td><td class="num">$8.00</td><td class="num">$16.00</td><td class="num">$40.00</td><td class="num">$20 per person (7-day residential pass)</td><td class="src">{src_links('RTC_FARE')}</td></tr>
<tr><td><strong>Las Vegas Monorail</strong></td><td>7 stations along the east Strip: MGM Grand, Horseshoe/Paris, Flamingo/Caesars Palace, Harrah's/The LINQ, Boingo LVCC, Westgate, SAHARA</td><td>Every 4–8 minutes</td><td class="num">$12.50</td><td class="num">$31.00</td><td class="num">$66.00</td><td class="num">$128.00</td><td class="src">{src_links('MONO')}</td></tr>
</tbody></table></div>
<p class="muted">The Monorail does not reach Downtown, Chinatown or the airport. The Deuce runs about every 15 minutes along the Strip and Downtown. Neither operator publishes a venue-to-venue journey time, so no minute figure is claimed (<a class="flaglink" href="flagged.html#F-16">F-16</a>).</p>

<h2>Things that are free</h2>
<ul class="sum">
<li><strong>Fountains of Bellagio</strong> — every 30 minutes from 3:00 PM (noon at weekends), every 15 minutes from 8:00 PM to midnight. Free. <a class="src" href="https://bellagio.mgmresorts.com/en/entertainment/fountains-of-bellagio.html" target="_blank" rel="noopener">official</a></li>
<li><strong>Bellagio Conservatory</strong> — Lunar New Year display 9 Jan – 6 Mar 2027 fits the whole preferred stay. Dark 7–12 Mar. <a class="src" href="https://bellagio.mgmresorts.com/en/entertainment/conservatory-botanical-garden.html" target="_blank" rel="noopener">official</a></li>
</ul>
"""
    return page("activities.html", "Activities", body)


def build_booking() -> str:
    hdr = ["Window"] + [h["name"] for h in HOTELS["rows"]]
    keys = ["window", "south_point", "caesars", "flamingo", "paris", "resorts_world", "wynn"]
    labels = ["South Point", "Caesars Palace", "Flamingo", "Paris", "Resorts World", "Wynn"]
    rows = []
    for w in BOOKING["windows"]:
        cells = [f'<td><strong>{E(w["window"])}</strong></td>']
        for k in keys[1:]:
            v = w.get(k, "")
            cells.append(f'<td>{E(v) if v else unv("", "No quote")}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")

    cf = BOOKING["cheapest_finding"]
    bt = BOOKING["best_time_to_book"]
    body = f"""
<h1>Booking &amp; cost</h1>
<p class="lead">What the trip actually costs, window by window, and the honest answer to "when should I book?".</p>

<div class="kpis">
<div class="kpi ok"><b>$581</b><small>Cheapest verified 7-night 2-queen stay — Flamingo (derived, before tax)</small></div>
<div class="kpi ok"><b>$989</b><small>Cheapest hotel-issued 7-night total — South Point</small></div>
<div class="kpi gold"><b>$2,039</b><small>Cheapest verified 14-night stay — South Point</small></div>
<div class="kpi warn"><b>$2,434.84</b><small>Only fully itemised all-in 7-night total — Resorts World</small></div>
<div class="kpi bad"><b>Unverified</b><small>Best time to book — no official source publishes a forecast</small></div>
</div>

<h2>Price by date window</h2>
<div class="tablewrap"><table>
<caption>Two adults, one room, exact dates, read live from each hotel's own booking engine on {E(SRC['as_of'])}. "Derived" figures are the hotel's published nightly rate × nights, before tax.</caption>
<thead><tr><th>Date window</th><th>South Point</th><th>Caesars Palace</th><th>Flamingo</th><th>Paris</th><th>Resorts World</th><th>Wynn</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>

<div class="card">
<h2>Which window is cheapest</h2>
<p>{E(cf['window_ranking'])}</p>
<ul class="sum">
<li><strong>Cheapest 7 nights, verified:</strong> {E(cf['cheapest_7n_verified'])}</li>
<li><strong>Cheapest 7 nights, hotel-issued:</strong> {E(cf['cheapest_7n_hotel_issued'])}</li>
<li><strong>Cheapest 14 nights:</strong> {E(cf['cheapest_14n_verified'])}</li>
</ul>
<p class="muted">{E(cf['note'])}</p>
</div>

<div class="card">
<h2>Best time to book</h2>
<div class="bad"><span class="b bu">Unverified</span> {E(bt['why'])}</div>
<p><strong>What would answer it:</strong> {E(bt['what_would_answer_it'])}</p>
<p class="muted">This is the one question in the brief that the available official sources cannot answer. It is flagged rather than guessed. <a class="flaglink" href="flagged.html#F-16">F-16</a> and <a class="flaglink" href="flagged.html#F-12">F-12</a>.</p>
</div>

<div class="card">
<h2>Fees, deposits and the fine print</h2>
<p>{E(BOOKING['fees_note'])}</p>
</div>

<div class="card">
<h2>What to do next, in order</h2>
<ol class="plain">
<li>Confirm the number of nights — 3, 7 or 14. Only South Point quoted a 14-night stay.</li>
<li>Decide whether a car will be used; without one, Red Rock Canyon and Chinatown are not reachable.</li>
<li>Re-price the shortlisted hotel on the exact dates and use the engine's <em>Total Price</em> toggle to see tax inclusive.</li>
<li>Book starred restaurants as soon as dates are fixed — é by José Andrés seats nine and opens bookings three months ahead.</li>
</ol>
</div>
"""
    return page("booking.html", "Booking & cost", body)


def build_questions() -> str:
    rows = "".join(f"""<tr>
<td><strong>{E(q['id'])}</strong></td>
<td><strong>{E(q['question'])}</strong></td>
<td class="muted">{E(q['known'])}</td>
<td>{unv('', 'Needed') if q['missing'] else ''} <span class="muted">{E(q['missing'])}</span></td>
<td class="muted">{E(q['how'])}</td>
<td>{'<span class="b bx">Blocks decision</span>' if q['blocking'].startswith('Yes') else '<span class="b bu">No</span>'}</td>
<td class="muted">{E(q['owner'])}</td>
</tr>""" for q in QUESTIONS["rows"])

    body = f"""
<h1>Questions to answer before deciding</h1>
<p class="lead">{E(QUESTIONS['intro'])}</p>

<div class="note">Two of these block every calculation, not just a detail: the number of nights, and whether a car is available. Everything else can be refined later.</div>

<div class="tablewrap"><table>
<caption>Known facts, missing facts, and the cheapest way to close each gap.</caption>
<thead><tr><th>ID</th><th>Question</th><th>What we already know</th><th>What is missing</th><th>How to find it</th><th>Blocks the decision?</th><th>Owner</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>How to discover the missing information</h2>
<ul class="sum">
<li><strong>Ask the properties directly.</strong> Three hotels never returned a price. A single email each asking for an all-in quote for the exact dates resolves the biggest gap.</li>
<li><strong>Use the booking engine's own total.</strong> Caesars and MGM engines both have a "Total Price" toggle that includes tax — that removes the need to derive anything.</li>
<li><strong>Check the reservation widgets, not the menu pages.</strong> Most restaurants do not publish hours or prices, but their OpenTable or SevenRooms booking screen shows the service times they are actually selling.</li>
<li><strong>Re-run the same search weekly.</strong> That is the only honest way to learn whether waiting lowers the price.</li>
<li><strong>Ask RTC's trip planner for the specific pairs.</strong> It will give a door-to-door time for the actual date, which is the only thing that satisfies the one-hour rule.</li>
</ul>
"""
    return page("questions.html", "Questions", body)


def build_suggestions() -> str:
    rows = "".join(f"""<tr>
<td><strong>{E(s['id'])}</strong></td>
<td><strong>{E(s['title'])}</strong></td>
<td class="muted">{E(s['why'])}</td>
<td>{'<span class="b bv">' + E(s['effort']) + '</span>' if s['effort']=='Low' else '<span class="b bp">' + E(s['effort']) + '</span>'}</td>
<td>{'<span class="b bv">' + E(s['impact']) + '</span>' if s['impact']=='High' else '<span class="b bp">' + E(s['impact']) + '</span>'}</td>
<td class="muted">{E(s['needs'])}</td>
<td><span class="b bu">{E(s['status'])}</span></td>
</tr>""" for s in SUGGESTIONS["rows"])

    body = f"""
<h1>Suggestions for review</h1>
<p class="lead">{E(SUGGESTIONS['intro'])}</p>

<div class="note"><strong>Nothing on this page has been implemented.</strong> These are proposals. Choose the ones worth doing, and a later pass can add them to the site or the plan.</div>

<h2>Highest impact first</h2>
<div class="card">
<h3>If you only do three things</h3>
<ol class="plain">
<li><strong>S-01 — Lock the Feb 15–22, 2027 week.</strong> It is the cheapest window tested and it matches the 7-night cost basis.</li>
<li><strong>S-03 — Re-price MGM Grand, The Cosmopolitan and Bellagio.</strong> Three of the four hotels with a Michelin star on site have no verified price, which is the single biggest distortion in the ranking.</li>
<li><strong>S-02 — Get one itemised all-in quote from the top two hotels.</strong> That converts every "derived" figure into a real number.</li>
</ol>
</div>

<div class="tablewrap"><table>
<caption>Each suggestion is independent. Effort and impact are my judgement, stated plainly so they can be argued with.</caption>
<thead><tr><th>ID</th><th>Suggestion</th><th>Why it helps</th><th>Effort</th><th>Impact</th><th>Needs</th><th>Status</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Ways to improve the site itself</h2>
<ul class="sum">
<li><strong>Total-cost calculator (S-08).</strong> Readers currently add hotel + restaurants + transit by hand. One clearly-labelled sum would let a decision be made in a minute.</li>
<li><strong>Distance rings on the hotel page (S-11).</strong> A visual walking / bus / monorail ring per hotel would make the one-hour requirement obvious at a glance.</li>
<li><strong>One recheck date for every live price (S-12).</strong> A single "prices rechecked on" banner keeps the site honest as rates drift.</li>
<li><strong>Keep the current three-tier badge system.</strong> Verified / Derived / Unverified has proven the clearest way to show what is known without hiding what is not.</li>
</ul>
"""
    return page("suggestions.html", "Suggestions", body)


def build_flagged() -> str:
    items = []
    for f in FLAGS["items"]:
        extra = f'<br><span class="src">also: <a href="{E(f["source2"])}" target="_blank" rel="noopener">{E(f["source2"])}</a></span>' if f.get("source2") else ""
        sev = {"high": "bx", "medium": "bp", "low": "bu"}.get(f["severity"], "bu")
        items.append(f"""<tr id="{E(f['id'])}">
<td><strong>{E(f['id'])}</strong></td>
<td><span class="b {sev}">{E(f['severity'])}</span><br><span class="muted">{E(f['kind'])}</span></td>
<td><strong>{E(f['title'])}</strong></td>
<td>{E(f['detail'])}<br><br><em>Impact:</em> {E(f['impact'])}<br><em>Next step:</em> {E(f['next'])}</td>
<td class="src"><a href="{E(f['source'])}" target="_blank" rel="noopener">source</a>{extra}</td>
</tr>""")

    body = f"""
<h1>Flagged for review</h1>
<p class="lead">{E(FLAGS['intro'])}</p>

<div class="kpis">
<div class="kpi bad"><b>{sum(1 for f in FLAGS['items'] if f['severity']=='high')}</b><small>High severity</small></div>
<div class="kpi warn"><b>{sum(1 for f in FLAGS['items'] if f['severity']=='medium')}</b><small>Medium severity</small></div>
<div class="kpi"><b>{sum(1 for f in FLAGS['items'] if f['severity']=='low')}</b><small>Low severity</small></div>
<div class="kpi gold"><b>{len(FLAGS['items'])}</b><small>Items in total</small></div>
</div>

<div class="warn">None of these items blocked publication. They are published here, with their sources, so the decision can be made with the gaps visible.</div>

<div class="tablewrap"><table>
<caption>Every item is anchored — link to it directly with #F-01 style anchors.</caption>
<thead><tr><th>ID</th><th>Severity</th><th>Item</th><th>Detail, impact and next step</th><th>Source</th></tr></thead>
<tbody>{''.join(items)}</tbody></table></div>
"""
    return page("flagged.html", "Flagged for review", body)


def build_repo_review() -> str:
    sev = {"high": "bx", "medium": "bp", "low": "bu"}
    rows = "".join(f"""<tr id="{E(f['id'])}">
<td><strong>{E(f['id'])}</strong></td>
<td><span class="b {sev.get(f['severity'],'bu')}">{E(f['severity'])}</span></td>
<td><strong>{E(f['title'])}</strong></td>
<td>{E(f['evidence'])}<br><br><em>Impact:</em> {E(f['impact'])}<br><em>Fix:</em> {E(f['how_to_fix'])}</td>
<td class="src"><a href="{E(f['source_url'])}" target="_blank" rel="noopener">{E(f['source'])}</a></td>
</tr>""" for f in REVIEW["findings"])

    clean = "".join(f"<li>{E(c)}</li>" for c in REVIEW["clean_checks"])
    body = f"""
<h1>Repository review</h1>
<p class="lead">{E(REVIEW['method'])}</p>

<div class="note"><strong>Verdict.</strong> {E(REVIEW['headline'])}</div>

<h2>Findings</h2>
<div class="tablewrap"><table>
<caption>{len(REVIEW["findings"])} findings, each with the file or command that produced it.</caption>
<thead><tr><th>ID</th><th>Severity</th><th>Finding</th><th>Evidence, impact and fix</th><th>Where</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2>Checks that passed</h2>
<ul class="sum">{clean}</ul>

<h2>How this was checked</h2>
<ul class="plain">
<li>Every HTML file under <code>docs/</code>, <code>site/</code>, <code>field-notes/</code> and the repository root was parsed and each relative <code>href</code>/<code>src</code> resolved on disk.</li>
<li>The GitHub Pages API was read directly for the deployment configuration.</li>
<li>Each session's own validation script was executed and its exit code recorded.</li>
<li>Live prices were re-read from the official booking engines on {E(SRC['as_of'])} and compared with the numbers already published.</li>
<li>No file outside this session's scope was modified. Findings are reported here instead of edited elsewhere, per the shared coordination rules.</li>
</ul>
"""
    return page("repo-review.html", "Repo review", body)


def build_sources() -> str:
    rows = "".join(f"""<tr>
<td><strong>{E(s['id'])}</strong></td>
<td><a href="{E(s['url'])}" target="_blank" rel="noopener">{E(s['label'])}</a></td>
<td class="muted">{E(s['domain'])}</td>
<td><span class="b {'bv' if 'official' in s['tier'] else 'bu'}">{E(s['tier'])}</span></td>
</tr>""" for s in SRC["items"])

    body = f"""
<h1>Sources</h1>
<p class="lead">Every source used, with a short note on what each was used for. The rule is simple: a value appears on this site only if one of these pages confirmed it.</p>

<div class="card">
<h2>The verification rule</h2>
<ul class="sum">
<li><strong>Verified</strong> — an official page (the venue, the hotel, the operator, the government agency or the awarding body) states the value. The row links to that page.</li>
<li><strong>Derived</strong> — arithmetic performed on values the official page published, with the arithmetic shown. Never presented as if the venue issued it.</li>
<li><strong>Unverified</strong> — the value is left blank and carries a flag ID. No estimate, average or "typical" figure is substituted.</li>
<li><strong>Third parties</strong> — review sites, blogs and aggregators were not used to fill cells. Where they surfaced a conflict, the conflict is recorded on the Flagged page instead.</li>
</ul>
</div>

<div class="tablewrap"><table>
<caption>{len(SRC['items'])} sources, captured {E(SRC['as_of'])}.</caption>
<thead><tr><th>ID</th><th>Source</th><th>Domain</th><th>Type</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<div class="note"><strong>Dynamic data notice.</strong> Hotel rates, restaurant menus and show schedules change. Every price on this site is a dated snapshot. Re-check the linked page before booking.</div>
"""
    return page("sources.html", "Sources", body)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "style.css").write_text(CSS, encoding="utf-8")

    builders = {
        "index.html": build_index,
        "hotels.html": build_hotels,
        "michelin.html": build_michelin,
        "activities.html": build_activities,
        "booking.html": build_booking,
        "questions.html": build_questions,
        "suggestions.html": build_suggestions,
        "flagged.html": build_flagged,
        "repo-review.html": build_repo_review,
        "sources.html": build_sources,
    }
    for name, fn in builders.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
    print(f"built {len(builders)} pages into {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
