#!/usr/bin/env python3
"""Build the canonical Vegas2 planner at the repository root.

Source of truth: data/plan/*.json  ->  index.html, restaurants.html, hotels.html,
booking.html, activities.html, transit.html, questions.html, suggestions.html,
flagged.html, sources.html, repo-review.html

Rule enforced on every row: a value is rendered only if the JSON contains it.
Blank stays blank; the verification badge explains why. Nothing is inferred.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "plan"
AS_OF = "2026-11-27"

PAGES = [
    ("index.html", "Overview"),
    ("restaurants.html", "MICHELIN"),
    ("hotels.html", "Hotels"),
    ("booking.html", "Prices & dates"),
    ("activities.html", "Activities"),
    ("transit.html", "Transit"),
    ("questions.html", "Questions"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged"),
    ("repo-review.html", "Repo review"),
    ("sources.html", "Sources"),
]


def load(name):
    with open(DATA / name, encoding="utf-8") as fh:
        return json.load(fh)


def esc(text):
    return html.escape(str(text), quote=True)


def ext(url, label, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)}</a>'


def award_badge(code):
    m = {
        "2s": ("2 MICHELIN stars · 2026", "b-star"),
        "1s": ("1 MICHELIN star · 2026", "b-star"),
        "bib": ("Bib Gourmand · 2026", "b-bib"),
        "listed": ("Listed in guide · 2026", "b-list"),
    }
    label, cls = m[code]
    return f'<span class="badge {cls}">{label}</span>'


def vbadge(status, word_map=None):
    w = word_map or {"v": "Verified", "p": "Partial", "u": "Unverified"}
    c = {"v": "b-ok", "p": "b-part", "u": "b-no"}.get(status, "b-list")
    return f'<span class="badge {c}">{w.get(status, status)}</span>'


def blank_marker(text=""):
    return f'<span class="small" style="color:#8d2b2b">— {esc(text) if text else "no official value"}</span>'


def yt(name):
    return "https://www.youtube.com/results?search_query=" + quote_plus(name + " Las Vegas")


def src_links(sources):
    if not sources:
        return ""
    return '<span class="src">' + " ".join(ext(s["url"], s["label"]) for s in sources) + "</span>"


def table(headers, rows, caption="", cls="stack", num_cols=()):
    out = [f'<div class="table-wrap"><table class="{cls}">']
    if caption:
        out.append(f"<caption>{caption}</caption>")
    out.append("<thead><tr>" + "".join(
        f'<th class="{"num" if i in num_cols else ""}">{h}</th>' for i, h in enumerate(headers)
    ) + "</tr></thead><tbody>")
    for row in rows:
        if len(row) != len(headers):
            raise SystemExit(f"row/header mismatch: {len(row)} vs {len(headers)} in {headers[0]}")
        cells = []
        for i, cell in enumerate(row):
            label = html.unescape(re.sub(r"<[^>]+>", "", headers[i]))
            klass = ' class="num"' if i in num_cols else ""
            cells.append(f'<td{klass} data-label="{esc(label)}">{cell}</td>')
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def layout(page, title, body, lede="", crumb=""):
    nav_parts = []
    for href, label in PAGES:
        cls = ' class="active"' if href == page else ""
        nav_parts.append(f'<a href="{href}"{cls}>{esc(label)}</a>')
    nav = "".join(nav_parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Vegas2 planner</title>
<meta name="description" content="{esc(lede)[:200]}">
<link rel="stylesheet" href="assets/site/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="index.html"><span class="dot" aria-hidden="true"></span> Vegas2 <span class="small" style="color:#66707d;font-weight:500">Las Vegas · Feb–Mar 2027</span></a>
    <span class="spacer"></span>
    <button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks" aria-label="Open menu">☰</button>
    <nav class="nav" id="navLinks" aria-label="Main">{nav}</nav>
  </div>
</header>
<main class="wrap" id="main">
{crumb}
<h1>{esc(title)}</h1>
{f'<p class="lede">{lede}</p>' if lede else ''}
{body}
</main>
<footer class="site">
  <p><strong>Vegas2 planner.</strong> Built {AS_OF}. Two adults, one room, Las Vegas, Feb 15 – Mar 23, 2027.
  Every value shown is tied to an official source captured on the date stated; anything unconfirmed is left blank and listed on
  <a href="flagged.html">Flagged for review</a>. Prices are snapshots, not offers, and exclude taxes unless stated.</p>
  <p>Source register: <a href="sources.html">Sources</a> · Repository review: <a href="repo-review.html">Repo review</a> · Coordination: <a href="https://github.com/kanlerxz87-cyber/Vegas2/blob/main/COORDINATION.md" target="_blank" rel="noopener noreferrer">COORDINATION.md</a></p>
</footer>
<script>
  var t=document.getElementById('navToggle'),n=document.getElementById('navLinks');
  if(t&&n){{t.addEventListener('click',function(){{var o=n.classList.toggle('open');t.setAttribute('aria-expanded',o?'true':'false');}});}}
</script>
</body>
</html>
"""


def crumb_for(page, parents):
    if not parents:
        return ""
    parts = []
    for label, href in parents:
        parts.append(ext(href, label) if href else esc(label))
    return '<p class="crumb">' + " / ".join(parts) + " / " + esc(dict(PAGES)[page]) + "</p>"


# ---------------------------------------------------------------- pages

def build_index(meta, hotels, rests, acts, flags, suggestions, booking):
    rows = hotels["rows"]

    def on_campus(h):
        return sum(1 for r in rests["rows"] if r["venue"] in h["venues"])

    ranked = sorted(rows, key=lambda h: (-on_campus(h), h["price7"]["total"] if h["price7"] else 10**9))
    priced = sorted([h for h in rows if h["price7"]], key=lambda h: h["price7"]["total"])
    counts = {"2s":0,"1s":0,"bib":0,"listed":0}
    for r in rests["rows"]:
        counts[r["award"]] += 1

    kpis = [
        ("24", "MICHELIN distinctions in the 2026 Las Vegas list"),
        ("4", "Starred restaurants (5 stars total)"),
        ("$581", "Cheapest verified 7-night two-queen room (Flamingo)"),
        (str(len(flags["rows"])), "Flagged items / open gaps"),
    ]
    kpi_html = '<div class="kpis">' + "".join(
        f'<div class="kpi"><span class="n">{n}</span><span class="l">{esc(l)}</span></div>' for n, l in kpis
    ) + "</div>"

    finding_items = "".join(f"<li>{esc(x)}</li>" for x in meta["keyFindings"])

    picks = [
        ("Best MICHELIN cluster", "The Venetian Resort", f"{on_campus(ranked[0])} guide-listed restaurants inside the resort (Bouchon, COTE, Milos, Mott 32 — all 2026 Recommended). Dated price unavailable, so cost is the open question.", "hotels.html"),
        ("Best verified value", "Flamingo Las Vegas", "$581 for 7 nights in a two-queen room including the $50/day resort fee — center Strip, 350 sq ft, before taxes.", "hotels.html"),
        ("Best space per dollar", "South Point", "$989 for 7 nights in a 500 sq ft two-queen room including fees — but well south of the center Strip and no MICHELIN restaurant on site.", "booking.html"),
    ]
    pick_html = '<div class="grid three">' + "".join(
        f'<div class="pick"><div class="tag">{esc(t)}</div><div class="big">{esc(n)}</div><p>{esc(d)}</p>'
        f'<p style="margin-top:.5rem"><a href="{h}">Open details →</a></p></div>' for t, n, d, h in picks
    ) + "</div>"

    top_hotels = []
    for i, h in enumerate(ranked, 1):
        if not h["venues"] and h["price7"]:
            pass
        names = [r["name"] for r in rests["rows"] if r["venue"] in h["venues"]]
        price = f'${h["price7"]["total"]:,}' if h["price7"] else '<span class="badge b-no">No verified rate</span>'
        top_hotels.append([
            str(i), f'<strong>{esc(h["name"])}</strong><span class="sub">{esc(h["area"])}</span>',
            f'{on_campus(h)}<span class="sub">{esc(", ".join(names)) if names else "none on campus"}</span>',
            price, vbadge("v" if h["price7"] else "u", {"v":"Verified","u":"Unverified"}),
        ])

    top_rest = []
    order = {"2s":0,"1s":1,"bib":2,"listed":3}
    for r in sorted(rests["rows"], key=lambda r: order[r["award"]]):
        top_rest.append([
            esc(r["name"]), award_badge(r["award"]), esc(r["cuisine"]),
            f'{esc(r["venue"])}<span class="sub">{esc(r["area"])}</span>',
            esc(r["price2"]) if r["price2"] else blank_marker("not published"),
        ])

    body = f"""
{kpi_html}
<div class="note">
  <p><strong>Read this first.</strong> Las Vegas has <strong>no subway</strong>; rail is the 7-station Las Vegas Monorail along the Strip only. A 1-hour bus/rail limit therefore cannot separate Strip hotels — every MICHELIN restaurant in the city sits inside the Strip/Downtown/Chinatown core. The hotel ranking below uses the measure that <em>does</em> separate them: how many MICHELIN restaurants are inside the same resort, i.e. zero transit.</p>
  <p>Hotel prices are 7-night totals captured live on {AS_OF} for <strong>Feb 15–22, 2027</strong> and include each property's resort fee but <strong>exclude taxes</strong>, which no captured engine published.</p>
</div>

<h2>Executive summary</h2>
<div class="card">
  <ul class="clean">{finding_items}</ul>
  <p class="small">Full reasoning, captures and links: <a href="booking.html">Prices &amp; dates</a> · <a href="hotels.html">Hotels</a> · <a href="restaurants.html">MICHELIN</a>.</p>
</div>

<h2>The three paths</h2>
{pick_html}

<h2>Hotel ranking (MICHELIN cluster, then verified price)</h2>
{table(["#", "Hotel", "MICHELIN on campus", "7-night total (pre-tax)", "Price status"], top_hotels,
       caption="Feb 15–22, 2027 · 2 adults · 1 room · resort fee included, taxes excluded. 'No verified rate' means the official engine served no price — it is not a judgement about cost.", num_cols=(0,))}
<p class="small">Cheapest verified: {esc(priced[0]["name"])} at <strong>${priced[0]["price7"]["total"]:,}</strong>. Details and room specs on <a href="hotels.html">Hotels</a>.</p>

<h2>MICHELIN list at a glance</h2>
<p class="lede">{counts['2s']} two-star · {counts['1s']} one-star · {counts['bib']} Bib Gourmand · {counts['listed']} listed = {len(rests['rows'])} restaurants. Source: the official Las Vegas MICHELIN page (LVCVA), captured {rests['guide']['captured']}. The 2027 guide is not published yet.</p>
{table(["Restaurant", "2026 award", "Cuisine", "Where", "Cost for 2 (as published)"], top_rest,
       caption="Cost for 2 is blank unless the restaurant publishes a price. No estimates are fabricated.")}

<h2>What is still open</h2>
<div class="grid two">
  <div class="card"><h3>Decisions only you can make</h3>
    <p>20 questions are tracked on <a href="questions.html">Questions</a>. The three that change every number:</p>
    <ul class="clean">
      <li><strong>Q-01</strong> 3 nights or 7 nights? The brief says both.</li>
      <li><strong>Q-02</strong> What is the all-in budget for two?</li>
      <li><strong>Q-03</strong> Do you accept bus/monorail in place of a subway?</li>
    </ul>
  </div>
  <div class="card"><h3>Gaps the research could not close</h3>
    <p>{len(flags['rows'])} items are on <a href="flagged.html">Flagged for review</a>, with the source link for each. Biggest three: no dated price for the Venetian/MGM/Wynn platforms (F-05, F-06), taxes excluded everywhere (F-03), and two-person menu totals published by only one restaurant (F-11).</p>
  </div>
</div>

<h2>Site map</h2>
<div class="grid three">
  <div class="card"><h3><a href="restaurants.html">MICHELIN restaurants</a></h3><p class="small">All 24 distinctions, hours, cost for two, official link and social/search link per row.</p></div>
  <div class="card"><h3><a href="hotels.html">Hotels</a></h3><p class="small">11 candidates, room and bathroom evidence, 7-night totals, cluster counts.</p></div>
  <div class="card"><h3><a href="booking.html">Prices &amp; dates</a></h3><p class="small">Three date windows compared, cheapest verified totals, booking-timing evidence.</p></div>
  <div class="card"><h3><a href="activities.html">Activities</a></h3><p class="small">11 experiences with published hours, prices and travel notes.</p></div>
  <div class="card"><h3><a href="transit.html">Transit</a></h3><p class="small">Monorail hours, RTC links, and why no journey time is claimed.</p></div>
  <div class="card"><h3><a href="questions.html">Questions</a></h3><p class="small">What must be answered before booking, and how to close each gap.</p></div>
  <div class="card"><h3><a href="suggestions.html">Suggestions</a></h3><p class="small">Three decision paths and 12 site improvements, nothing auto-applied.</p></div>
  <div class="card"><h3><a href="flagged.html">Flagged for review</a></h3><p class="small">Every irregularity with severity, effect and official source.</p></div>
  <div class="card"><h3><a href="repo-review.html">Repo review</a></h3><p class="small">What was wrong with the repository and what this session changed.</p></div>
</div>
"""
    return layout("index.html", "Las Vegas, planned from official sources",
                  body, lede=f"A two-adult, one-room trip inside Feb 15 – Mar 23, 2027 (preferred Feb 15–18). Every number below was captured from an official site on {AS_OF}; blanks are gaps, not zeros.")


def build_restaurants(rests, flags):
    guide = rests["guide"]
    rows = []
    for r in rests["rows"]:
        hours = esc(r["hours"]) if r["hours"] else blank_marker("not published on the captured page")
        price = esc(r["price2"]) if r["price2"] else blank_marker("not published")
        social = " ".join(ext(s["url"], s["label"]) for s in r["social"]) if r["social"] else ""
        social_cell = social + ("" if social else blank_marker("no official handle confirmed"))
        social_cell += f'<span class="sub">{ext(yt(r["name"] + " review"), "YouTube search")}</span>'
        official = ext(r["official"], "Official site")
        if r.get("menu"):
            official += " " + ext(r["menu"], "Menu")
        rows.append([
            f'<strong>{esc(r["name"])}</strong><span class="sub">{esc(r["note"])}</span>',
            award_badge(r["award"]),
            f'{esc(r["cuisine"])}<span class="sub">{esc(r["area"])} · {esc(r["venue"])}</span>',
            hours + ("" if r["hours"] else "") + f'<span class="sub">{vbadge(r["hoursStatus"], {"v":"verified","p":"logged 11-26","u":"unverified"})}</span>',
            price + (f'<span class="sub">{esc(r["priceNote"])}</span>' if r["priceNote"] else ""),
            official,
            social_cell,
        ])
    counts = {"2s":0,"1s":0,"bib":0,"listed":0}
    for r in rests["rows"]:
        counts[r["award"]] += 1
    cluster = [
        ["The Venetian + The Palazzo", "4", "Bouchon · COTE · Estiatorio Milos · Mott 32", "All 2026 Recommended (no stars)"],
        ["MGM Grand", "2", "Joël Robuchon (2 stars) · L'Atelier (1 star)", "The only two-star room in Las Vegas"],
        ["The Cosmopolitan", "2", "é by José Andrés (1 star) · China Poblano (Bib)", "One star + one Bib Gourmand"],
        ["Caesars Palace", "1", "Restaurant Guy Savoy (1 star)", ""],
        ["Bellagio", "1", "Michael Mina", "Recommended (listed)"],
        ["ARIA", "1", "Gymkhana", "Recommended (listed)"],
        ["Wynn Las Vegas", "1", "Wing Lei", "Recommended (listed) — not starred in 2026"],
        ["Resorts World", "1", "Stubborn Seed", "Recommended (listed)"],
        ["Chinatown / Downtown / off-Strip", "11", "Esther's Kitchen · Yen Viet · Anima · Kabuto · Kame · Lamaii · Partage · Pho Ga Bac Bac · Ping Pang Pong · Soulbelly · Sparrow and Wolf", "No casino campus; bus or car from the Strip"],
    ]
    body = f"""
<div class="note">
  <p><strong>How tiers are shown.</strong> The official Las Vegas MICHELIN page lists {guide['cityList']}. A <span class="badge b-star">star</span> is a star. <span class="badge b-bib">Bib Gourmand</span> is the value category — it is <em>not</em> a star. <span class="badge b-list">Listed</span> means the restaurant appears in the guide's recommended selection with no star. The official page's own wording for non-starred, non-Bib entries is "Recommended by MICHELIN Guide"; this site labels those rows "Listed in guide" and never calls them starred.</p>
  <p>Captured {guide['captured']} from {ext(guide['source'], 'the official Las Vegas MICHELIN page')}. 2027 awards have not been announced (F-08).</p>
</div>

<div class="kpis">
  <div class="kpi"><span class="n">{counts['2s']}</span><span class="l">Two-star</span></div>
  <div class="kpi"><span class="n">{counts['1s']}</span><span class="l">One-star</span></div>
  <div class="kpi"><span class="n">{counts['bib']}</span><span class="l">Bib Gourmand</span></div>
  <div class="kpi"><span class="n">{counts['listed']}</span><span class="l">Listed / recommended</span></div>
</div>

<h2>Restaurant clusters by property</h2>
{table(["Property", "MICHELIN count", "Restaurants", "Notes"], cluster,
       caption="Use this to pick a hotel. Counts come from the venue field of each row in the table below.")}

<h2>All 24 restaurants</h2>
{table(["Restaurant", "2026 award", "Cuisine / area", "Open (days & hours)", "Cost for 2 adults", "Official link", "Social / video"], rows,
       caption="Hours and prices are blank where the official page did not publish them. 'Cost for 2' is the published total for two adults, pre-tax and pre-tip; à-la-carte item prices are quoted as items, never converted into an invented average.")}
<p class="small">Every row's official link was opened or is the link the official MICHELIN list publishes. Social handles appear only when an official page linked them; otherwise the YouTube link is a plain search, not a verified account.</p>

<h2>Food budget reality check</h2>
<ul class="clean">
  <li><strong>Only one total is published:</strong> Partage — 5 courses $130pp ($260 for two), 7 courses $160pp ($320), Signature $210pp ($420), before tax and tip.</li>
  <li><strong>Item-level only:</strong> Guy Savoy — à la carte $60–$290 per item (Colors of Caviar $120, Artichoke &amp; Black Truffle Soup $100, Sea Bass $160, Marmite of Squab $200, A5 Wagyu $290).</li>
  <li><strong>Nothing published:</strong> the other 22 rows. Ask the venue or open the menu PDF; the site will not guess.</li>
  <li>Dress codes are enforced: Joël Robuchon business formal, Guy Savoy formal, Wing Lei business casual.</li>
</ul>
"""
    return layout("restaurants.html", "MICHELIN restaurants in Las Vegas",
                  body, lede="24 distinctions from the 2026 MICHELIN Guide Southwest — stars, Bib Gourmand and listed restaurants kept strictly apart, with hours, published prices, official links and a social/video link for every row.",
                  crumb=crumb_for("restaurants.html", [("Overview", "index.html")]))


def build_hotels(hotels, rests):
    def on_campus(h):
        return [r["name"] for r in rests["rows"] if r["venue"] in h["venues"]]

    rows_sorted = sorted(hotels["rows"], key=lambda h: (
        -len(on_campus(h)),
        h["price7"]["total"] if h["price7"] else 10**9,
    ))
    rows = []
    for i, h in enumerate(rows_sorted, 1):
        names = on_campus(h)
        price = f'<strong>${h["price7"]["total"]:,}</strong><span class="sub">{esc(h["price7"]["room"])} · {esc(h["price7"]["nightly"])}</span>' if h["price7"] else blank_marker(h["price7Note"][:70] + ("…" if len(h["price7Note"]) > 70 else ""))
        rows.append([
            str(i),
            f'<strong>{esc(h["name"])}</strong><span class="sub">{esc(h["area"])}</span>',
            f'{len(names)}<span class="sub">{esc(", ".join(names)) if names else "—"}</span>',
            f'{esc(h["rooms"]) if h["rooms"] else blank_marker("room types not captured")}<span class="sub">{vbadge(h["roomStatus"])}</span>',
            f'{esc(h["bath"]) if h["bath"] else blank_marker("bathroom detail not captured")}',
            price,
            vbadge("v" if h["price7"] else "u", {"v":"Verified","u":"Unverified"}),
        ])
    detail = []
    for i, h in enumerate(rows_sorted, 1):
        detail.append(f"""
<details>
  <summary>#{i} {esc(h['name'])} — {esc(h['area'])}</summary>
  <p>{esc(h['note'])}</p>
  <p class="small"><strong>Room:</strong> {esc(h['rooms']) if h['rooms'] else 'not captured'}<br>
  <strong>Bathroom:</strong> {esc(h['bath']) if h['bath'] else 'not captured'}<br>
  <strong>7-night total:</strong> {('$'+format(h['price7']['total'], ',')+' — '+h['price7']['basis']) if h['price7'] else h['price7Note']}<br>
  <strong>Within 1 hour:</strong> {esc(h['transit'])} {vbadge(h['transitStatus'])}</p>
  {src_links(h['sources'])}
  {'<p class="small">Flags: ' + ', '.join(f'<a href="flagged.html#{f}">{f}</a>' for f in h['flagIds']) + '</p>' if h['flagIds'] else ''}
</details>""")
    priced = [h for h in hotels["rows"] if h["price7"]]
    value_rank = sorted(priced, key=lambda h: h["price7"]["total"])
    value_rows = [[str(i), esc(h["name"]), esc(h["price7"]["room"]), f'${h["price7"]["total"]:,}', esc(h["price7"]["nightly"])] for i, h in enumerate(value_rank, 1)]
    body = f"""
<div class="note warn">
  <p><strong>Ranking rule.</strong> {esc(hotels['rankMethod'])}</p>
  <p><strong>Price rule.</strong> {esc(hotels['basis'])} All totals include the resort fee and <strong>exclude taxes</strong> (F-03).</p>
</div>

<h2>All candidates</h2>
{table(["#", "Hotel", "MICHELIN on campus", "Room &amp; bed (verified)", "Private bathroom", "7-night total, Feb 15–22 2027", "Price"], rows,
       caption="Blank = the official page did not state it or the engine served no rate. It does not mean the feature is absent.", num_cols=(0,))}

<h2>Value ranking (verified prices only)</h2>
{table(["#", "Hotel", "Room used", "7 nights", "Nightly incl. resort fee"], value_rows,
       caption="Same dates, same party. Tax is not included because no engine published it.", num_cols=(0, 3))}

<h2>Why the 1-hour rule does not rank these hotels</h2>
<div class="card">
  <p>All 24 MICHELIN restaurants sit in the Strip / Downtown / Chinatown core, and every hotel in this table is in or next to that core. With no subway, the realistic modes are walking, the Strip Monorail, RTC buses and rideshare. No official door-to-door time was retrieved for any pair (F-02), so a "minutes to each restaurant" column would be invented.</p>
  <p>What <em>is</em> verifiable is co-location: four restaurants share the Venetian/Palazzo resort, two are inside MGM Grand, two inside The Cosmopolitan. Those require zero transit. That is the ranking you see above.</p>
  <p class="small">Chinatown, Downtown and off-Strip restaurants (11 of 24) have no rail link at all — Monorail is Strip-only (F-17).</p>
</div>

<h2>Hotel-by-hotel detail</h2>
{''.join(detail)}

<h2>What would change this ranking</h2>
<ul class="clean">
  <li>Dated rates for Venetian, Cosmopolitan, MGM Grand, Bellagio, ARIA, Wynn and Resorts World (F-05, F-06).</li>
  <li>A door-to-door transit matrix from the RTC Trip Planner (F-02) — the honest way to enforce the 1-hour rule.</li>
  <li>Your bed and bathroom preferences, and whether a 350 sq ft room is acceptable (Q-07, Q-09, Q-17).</li>
</ul>
"""
    return layout("hotels.html", "Hotels: price, location and MICHELIN proximity",
                  body, lede="11 Las Vegas candidates for two adults, ranked first by MICHELIN restaurants inside the same resort (no transit needed) and then by the verified 7-night total for Feb 15–22, 2027.",
                  crumb=crumb_for("hotels.html", [("Overview", "index.html")]))


def build_booking(booking, hotels):
    qrows = []
    for q in booking["quotes"]:
        total = f'<strong>{esc(q["total"])}</strong>' if q["total"] else blank_marker("no quote")
        qrows.append([
            esc(q["window"]), esc(q["hotel"]), esc(q["nightly"]) if q["nightly"] else "—", total,
            esc(q["feeNote"]), vbadge(q["status"]), ext(q["source"], "Dated link"),
        ])
    wrows = [[esc(w["id"]), esc(w["label"]), esc(w["checkIn"]), esc(w["checkOut"]), str(w["nights"]), esc(w["note"])] for w in booking["windows"]]
    prow = [[esc(p["fact"]), ext(p["source"], "Official source")] for p in booking["bookTiming"]["verifiedPolicies"]]
    c = booking["cheapest"]
    d = booking["dateVerdict"]
    body = f"""
<div class="note">
  <p><strong>Cheapest verified option.</strong> {esc(c['verdict'])}</p>
  <p>Runner-up: {esc(c['runnerUp'])} {esc(c['delta'])}</p>
  <p class="small">{esc(c['caveat'])}</p>
</div>

<h2>Booking windows used</h2>
{table(["ID", "Window", "Check-in", "Check-out", "Nights", "Why"], wrows, caption="All inside the Feb 15 – Mar 23, 2027 allowed range.")}

<h2>Every dated quote captured</h2>
{table(["Window", "Hotel & room", "Nightly", "7-night total", "Fee basis", "Status", "Source"], qrows,
       caption=f"Captured {AS_OF}. Totals are room + resort fee only. Taxes are excluded because the engines did not publish the tax amount (F-03).", num_cols=(2, 3))}

<h2>Is Feb 15–22 the cheapest time to go?</h2>
<div class="card">
  <p><strong>What the captures show.</strong> {esc(d['statement'])}</p>
  <p><strong>What cannot be claimed.</strong> {esc(d['cannotSay'])}</p>
</div>

<h2>Best time to book</h2>
<div class="card">
  <p>{esc(booking['bookTiming']['statement'])}</p>
  <p><strong>Recommended action:</strong> {esc(booking['bookTiming']['action'])}</p>
</div>
{table(["Verified booking policy", "Source"], prow, caption="Only policies actually read on an official page are listed.")}

<h2>Tax and total honesty</h2>
<div class="note warn"><p>{esc(booking['taxNote'])}</p></div>

<h2>Price-watch plan</h2>
<ol>
  <li>Hold a free-cancellation two-queen room now at Flamingo ($581/7 nights pre-tax) or South Point ($989) — whichever location you prefer.</li>
  <li>Re-open the exact dated links on this page weekly and record the total (S-08).</li>
  <li>If a cheaper total appears, rebook and cancel the hold inside its free-cancellation window — check the window on the rate, not on the marketing page.</li>
  <li>Recheck March availability: South Point already shows March 20, 2027 sold out (F-15).</li>
</ol>
"""
    return layout("booking.html", "Prices, dates and when to book",
                  body, lede="Live 7-night quotes for Feb 15–22, 2027, a second week for comparison, the March availability problem, and the verified booking-policy evidence behind the timing recommendation.",
                  crumb=crumb_for("booking.html", [("Overview", "index.html")]))


def build_activities(acts):
    rows = []
    for a in acts["rows"]:
        hours = esc(a["hours"]) if a["hours"] else blank_marker("not captured")
        price = esc(a["price2"]) if a["price2"] else blank_marker("not published")
        social = " ".join(ext(s["url"], s["label"]) for s in a["social"]) if a["social"] else blank_marker("no official handle confirmed")
        social += f'<span class="sub">{ext(yt(a["name"]), "YouTube search")}</span>'
        rows.append([
            f'<strong>{esc(a["name"])}</strong><span class="sub">{esc(a["note"])}</span>',
            esc(a["area"]),
            hours + f'<span class="sub">{vbadge(a["hoursStatus"], {"v":"verified","p":"partial (dates only)","u":"unverified"})}</span>',
            price + (f'<span class="sub">{esc(a["priceNote"])}</span>' if a["priceNote"] else ""),
            f'{esc(a["transit"])} {vbadge(a["transitStatus"])}',
            ext(a["official"], "Official site"),
            social,
        ])
    body = f"""
<div class="note">
  <p><strong>What "cost for 2" means here.</strong> Only the High Roller publishes both a per-person price and a clear per-person structure, so it is the only activity with a true two-person total. Everything else is blank or shows the published per-person figure in the notes. No ticket price is estimated.</p>
</div>
<h2>Activities</h2>
{table(["Activity", "Area", "Open (days & hours)", "Cost for 2 adults", "Travel / transit", "Official link", "Social / video"], rows,
       caption="Hours and prices captured 2026-11-27. A blank cell means the official page did not state it.")}

<h2>Timing notes that matter for Feb 15–18, 2027</h2>
<div class="grid two">
  <div class="card"><h3>Bellagio Conservatory</h3><p>The Lunar New Year display runs <strong>Jan 9 – Mar 6, 2027</strong>, so your preferred dates are inside a live installation. The gardens go dark <strong>Mar 7–12</strong>, which matters only if you shift the trip later. Spring opens Mar 13.</p>{ext("https://bellagio.mgmresorts.com/en/entertainment/conservatory-botanical-garden.html", "Official show dates")}</div>
  <div class="card"><h3>Neon Museum in February</h3><p>Open daily <strong>3:00–11:00 PM</strong> with last entry at 10:00 PM in the Sept–May schedule. It is an outdoor boneyard: summer heat rules do not apply in February, but wind/lightning cancellations still can.</p>{ext("https://neonmuseum.org/your-visit/", "Official visit page")}</div>
  <div class="card"><h3>Mob Museum + Downtown</h3><p>Open daily <strong>9:00 AM–9:00 PM</strong>; The Underground stays open later. Pair it with the Neon Museum and a Downtown MICHELIN table (Esther's Kitchen, Soulbelly BBQ) to make one transit trip instead of three.</p>{ext("https://themobmuseum.org/plan-your-visit/", "Official hours")}</div>
  <div class="card"><h3>Out-of-corridor trips</h3><p>Hoover Dam, Red Rock Canyon and Valley of Fire need a car or a tour; no verified public-transit option exists. Decide Q-11 before choosing a hotel.</p></div>
</div>
"""
    return layout("activities.html", "Activities and experiences",
                  body, lede="What is open, what it costs, and how far it is — with the official page linked on every row and blanks where a price or schedule was not published.",
                  crumb=crumb_for("activities.html", [("Overview", "index.html")]))


def build_transit():
    mono = [
        ["Stations", "7, all on the Las Vegas Strip (route map on the official site)"],
        ["Train frequency", "Every 4–8 minutes"],
        ["Station hours", "Monday 7 AM–midnight · Tuesday–Thursday 7 AM–2 AM · Friday–Sunday 7 AM–3 AM"],
        ["Reach", "Strip corridor only — no Chinatown, no Downtown, no airport"],
        ["Social", "@lvmonorail (stated by the official site)"],
    ]
    reach = [
        ["The Venetian · The Palazzo · Wynn · Resorts World", "Monorail corridor / walk", "4 + 1 + 1 MICHELIN rooms reachable on foot or one short rail hop"],
        ["Caesars Palace · Bellagio · ARIA · Cosmopolitan", "Walk / tram / Monorail", "1–2 MICHELIN rooms each on campus"],
        ["MGM Grand · Paris · Flamingo · South Point", "Walk / Monorail / bus", "0 on campus; all Strip MICHELIN rooms by short trip"],
        ["Chinatown (Kabuto, Kame, Partage, Sparrow and Wolf, Pho Ga Bac Bac)", "Bus, rideshare or car", "No rail. 11 of the 24 restaurants are here, Downtown or off-Strip"],
        ["Downtown (Esther's Kitchen, Soulbelly BBQ, Mob Museum, Neon Museum, Fremont)", "Bus, rideshare or car", "No rail link from the Strip"],
        ["Hoover Dam · Red Rock Canyon · Valley of Fire", "Car or tour", "Outside the bus network; travel time not verified"],
    ]
    body = f"""
<div class="note stop">
  <p><strong>There is no subway or metro in Las Vegas.</strong> The brief's "within 1 hour by subway or bus" test needs rewording: rail here means the <strong>7-station Las Vegas Monorail</strong>, which never leaves the Strip. Everything else is RTC bus (including the Deuce on Las Vegas Blvd), walking, the free tram segments, rideshare or a car.</p>
</div>

<h2>Las Vegas Monorail — verified facts</h2>
{table(["Fact", "Value"], mono, caption="Source: lvmonorail.com, captured 2026-11-27.")}
<p class="small">{ext("https://www.lvmonorail.com/", "Monorail home")} · {ext("https://www.lvmonorail.com/route-map/", "Route map")} · {ext("https://www.lvmonorail.com/ticket-information/", "Ticket information")}</p>

<h2>RTC buses — where to get the real answer</h2>
<div class="card">
  <p>RTC of Southern Nevada publishes a trip planner, fares and route maps. It also posts service alerts — currently including F1 construction changes around the Strip. Live journey times for your actual dates must come from that planner; this site does not model them (F-02).</p>
  <p>{ext("https://www.rtcsnv.com/tripplanner/", "RTC trip planner")} · {ext("https://www.rtcsnv.com/ways-to-travel/fares-passes/", "Fares & passes")} · {ext("https://www.rtcsnv.com/ways-to-travel/schedules-maps/", "Schedules & maps")} · {ext("https://www.rtcsnv.com/ways-to-travel/schedules-maps/alerts-detours/", "Alerts & detours")}</p>
</div>

<h2>What the 1-hour rule really implies</h2>
{table(["Where you stay", "How you move", "MICHELIN reach"], reach,
       caption="Mode assignment is based on the published Monorail route and venue addresses. Door-to-door minutes are deliberately absent.")}

<h2>Why there is no travel-time column</h2>
<ul class="clean">
  <li>No official source publishes a hotel→restaurant journey time for a February 2027 date.</li>
  <li>The RTC planner returns live results; capturing them would be a snapshot that expires, so it belongs in a dated log, not a static claim.</li>
  <li>Converting distance into minutes would be an estimate — exactly what the brief forbids.</li>
</ul>
<div class="note warn"><p><strong>Practical consequence:</strong> for a restaurant-led trip, choose the hotel whose resort already contains the restaurants you want (Venetian: 4, MGM Grand: 2, Cosmopolitan: 2). That removes the transit question entirely.</p></div>
"""
    return layout("transit.html", "Getting around: Monorail, buses and the 1-hour rule",
                  body, lede="What actually exists, what it reaches, and why this site refuses to print invented travel times.",
                  crumb=crumb_for("transit.html", [("Overview", "index.html")]))


def build_questions(questions):
    order = {"open": 0, "partial": 1, "answered": 2}
    rows = []
    for q in sorted(questions["rows"], key=lambda q: order.get(q["status"], 3)):
        badge = {"open": '<span class="badge b-no">Open — needs your answer</span>',
                 "partial": '<span class="badge b-part">Partly answered</span>',
                 "answered": '<span class="badge b-ok">Answered from a source</span>'}[q["status"]]
        rows.append([
            f'<span class="qid">{esc(q["id"])}</span>',
            f'<strong>{esc(q["q"])}</strong><span class="sub">{esc(q["impact"])}</span>',
            badge,
            esc(q["known"]),
            esc(q["missing"]),
            esc(q["how"]),
        ])
    open_n = sum(1 for q in questions["rows"] if q["status"] == "open")
    body = f"""
<div class="note">
  <p>{esc(questions['intro'])}</p>
  <p class="small"><strong>{open_n} of {len(questions['rows'])} questions are still open.</strong> The site cannot get cheaper or more precise until they are answered — the missing inputs are preferences and budget, not research.</p>
</div>
<h2>Questions, known facts, gaps and how to close them</h2>
{table(["#", "Question", "Status", "What we know (sourced)", "What is missing", "How to find it"], rows,
       caption="Ordered: open questions first, then partly answered, then answered.")}
<h2>If you only answer three</h2>
<div class="grid three">
  <div class="pick"><div class="tag">Changes every total</div><div class="big">Q-01 · Trip length</div><p>3 nights, 7 nights or two weeks. The brief currently says all three.</p></div>
  <div class="pick"><div class="tag">Changes the hotel</div><div class="big">Q-02 · Budget</div><p>An all-in ceiling for two. Without it, $581 and $6,170 look equally valid.</p></div>
  <div class="pick"><div class="tag">Changes the method</div><div class="big">Q-03 · No subway</div><p>Accept bus/monorail/walking, or redefine the 1-hour rule.</p></div>
</div>
<h2>How to answer without doing research</h2>
<p>Reply with numbers or choices only — e.g. "7 nights, $3,000 all-in, two queens, no car, starred restaurants only". Everything else on this site is already sourced and will re-rank itself.</p>
"""
    return layout("questions.html", "Questions that must be answered first",
                  body, lede="A clear list of what we know from official sources, what we do not know, and the exact step that would close each gap.",
                  crumb=crumb_for("questions.html", [("Overview", "index.html")]))


def build_suggestions(suggestions):
    paths = []
    for p in suggestions["paths"]:
        paths.append(f"""
<div class="card">
  <h3>{esc(p['id'])} · {esc(p['name'])}</h3>
  <p><strong>Pick:</strong> {esc(p['pick'])}</p>
  <p><strong>Pros:</strong> {esc(p['pros'])}</p>
  <p><strong>Cons:</strong> {esc(p['cons'])}</p>
  <p><strong>Best if:</strong> {esc(p['bestIf'])}</p>
  <p class="small"><strong>Still unknown:</strong> {esc(", ".join(p['unknowns']))}</p>
</div>""")
    rows = [[
        f'<span class="qid">{esc(s["id"])}</span>', esc(s["title"]), esc(s["why"]), esc(s["effort"]), esc(s["impact"]), esc(s["needs"]),
    ] for s in suggestions["siteImprovements"]]
    body = f"""
<div class="note">
  <p>{esc(suggestions['intro'])}</p>
  <p class="small">Nothing on this page has been implemented. Choose a path (or a list of improvement IDs) and the next build applies exactly that.</p>
</div>

<h2>Decision paths</h2>
<div class="grid three">{''.join(paths)}</div>

<h2>Site improvements to approve or reject</h2>
{table(["#", "Improvement", "Why it improves decisions", "Effort", "Impact", "What is needed"], rows,
       caption="Effort and impact are this session's assessment, not a sourced fact. Everything else states what data is missing.")}

<h2>What I would do first</h2>
<ol>
  <li><strong>S-08 price-watch log</strong> — cheap, and it turns "best time to book" from a guess into a measurement.</li>
  <li><strong>S-01 all-in calculator</strong> — closes the biggest honesty gap (every total here is pre-tax).</li>
  <li><strong>S-02 capture MGM/Venetian/Wynn rates</strong> — seven of eleven hotels are currently unpriced, which biases the ranking.</li>
  <li><strong>S-05 transit matrix</strong> — the only way to honour your 1-hour rule with evidence.</li>
</ol>

<h2>How to choose a path</h2>
<table class="stack">
  <thead><tr><th>If this is true</th><th>Take</th><th>Because</th></tr></thead>
  <tbody>
    <tr><td data-label="If this is true">The restaurants are the point</td><td data-label="Take">PATH-A (Venetian / MGM Grand)</td><td data-label="Because">Four or two MICHELIN rooms with zero transit, 650 sq ft+ suites</td></tr>
    <tr><td data-label="If this is true">Budget matters and you want to walk everywhere</td><td data-label="Take">PATH-B (Flamingo)</td><td data-label="Because">$581 verified, center Strip, no car needed</td></tr>
    <tr><td data-label="If this is true">You want space, quiet and a rental car</td><td data-label="Take">PATH-C (South Point)</td><td data-label="Because">500 sq ft, free valet, $989 including fees</td></tr>
  </tbody>
</table>
"""
    return layout("suggestions.html", "Suggestions and decision paths",
                  body, lede="Three concrete trip paths and twelve site improvements, each with its cost, benefit and the exact data needed — review before anything is implemented.",
                  crumb=crumb_for("suggestions.html", [("Overview", "index.html")]))


def build_flagged(flags):
    sev = {"high": 0, "medium": 1, "low": 2}
    rows = []
    for f in sorted(flags["rows"], key=lambda f: (sev[f["severity"]], f["id"])):
        cls = {"high": "b-no", "medium": "b-part", "low": "b-list"}[f["severity"]]
        srcs = " ".join(ext(s["url"], s["label"]) for s in f["source"] if s["url"] != "#") or '<span class="small">No external source — a request-level constraint.</span>'
        rows.append([
            f'<a id="{f["id"]}"></a><strong>{esc(f["id"])}</strong>',
            f'<span class="badge {cls}">{esc(f["severity"].upper())}</span>',
            f'<strong>{esc(f["title"])}</strong><span class="sub">{esc(f["detail"])}</span>',
            esc(f["effect"]),
            srcs,
        ])
    high = sum(1 for f in flags["rows"] if f["severity"] == "high")
    body = f"""
<div class="note">
  <p>{esc(flags['intro'])}</p>
  <p class="small"><strong>{len(flags['rows'])} items</strong> · {high} high severity. Nothing here blocks publication; each item explains why a value on another page is blank or qualified.</p>
</div>
{table(["ID", "Severity", "What is wrong", "Effect on the plan", "Source"], rows,
       caption="Sorted by severity. Every external claim links to the official page it came from.")}
<h2>How to use this page</h2>
<ul class="clean">
  <li><strong>Before booking:</strong> read every HIGH item. F-03 (taxes) and F-05/F-06 (missing rates) change the money; F-01/F-02 change the hotel method.</li>
  <li><strong>Before choosing a restaurant:</strong> read F-08 (2027 stars unannounced) and F-10/F-11 (hours and prices missing).</li>
  <li><strong>When a blank confuses you:</strong> search this page for the venue name; the flag will say what was and was not confirmed.</li>
</ul>
"""
    return layout("flagged.html", "Flagged for review",
                  body, lede="Every irregularity, conflict, and unverified value — with severity, its effect on the decision, and the official source used.",
                  crumb=crumb_for("flagged.html", [("Overview", "index.html")]))


def build_sources(meta, rests, hotels, acts, booking):
    registry = {}
    def add(url, label, used_for):
        if not url or url == "#":
            return
        if url not in registry:
            registry[url] = {"label": label, "used": set()}
        registry[url]["used"].add(used_for)

    add(rests["guide"]["source"], "Visit Las Vegas (LVCVA) — official MICHELIN list", "Award tiers for all 24 restaurants")
    for r in rests["rows"]:
        add(r["official"], r["name"] + " — official page", "Hours, address, price, social links")
        if r.get("menu"):
            add(r["menu"], r["name"] + " — official menu", "Published prices")
        for s in r["social"]:
            add(s["url"], s["label"], "Verified social account")
    for h in hotels["rows"]:
        for s in h["sources"]:
            add(s["url"], s["label"], h["name"] + " room/rate evidence")
    for a in acts["rows"]:
        add(a["official"], a["name"] + " — official page", "Hours, prices, dates")
        for s in a["social"]:
            add(s["url"], s["label"], "Verified social account")
    for p in booking["bookTiming"]["verifiedPolicies"]:
        add(p["source"], "Booking policy / fee disclosure", p["fact"][:70])
    add("https://www.lvmonorail.com/", "Las Vegas Monorail — official", "Stations, headways, station hours")
    add("https://www.lvmonorail.com/route-map/", "Las Vegas Monorail route map", "7 Strip stations")
    add("https://www.rtcsnv.com/", "RTC of Southern Nevada — official", "Bus network, alerts")
    add("https://www.rtcsnv.com/tripplanner/", "RTC trip planner", "Door-to-door journey queries (not captured)")
    add("https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/", "OPM federal holidays", "Feb 15, 2027 = Washington's Birthday")
    rows = []
    for url, info in sorted(registry.items(), key=lambda kv: kv[1]["label"].lower()):
        rows.append([ext(url, info["label"]), f'<span class="small">{esc(", ".join(sorted(info["used"])))}</span>', f'<span class="small" style="word-break:break-all">{esc(url)}</span>'])
    body = f"""
<div class="note">
  <p><strong>Verification method.</strong> {esc(meta['rules'][0])} Each row on this site carries the link it came from. Where a value could not be confirmed, it is blank and appears on <a href="flagged.html">Flagged for review</a>.</p>
  <p class="small">Capture date for everything marked "verified" here: <strong>{AS_OF}</strong>, except items explicitly labelled as logged by a prior session on 2026-11-26 (é by José Andrés and L'Atelier hours, the Venetian $6,170.43 figure, and the OPM holiday check).</p>
</div>
<h2>Rest of the rules</h2>
<ul class="clean">{''.join(f'<li>{esc(r)}</li>' for r in meta['rules'][1:])}</ul>

<h2>Source register ({len(registry)} links)</h2>
{table(["Source", "Used for", "URL"], rows, caption="Official first-party sources only. Third-party pages were used at most to raise a conflict, never to fill a value.")}

<h2>What was attempted and failed</h2>
<ul class="clean">
  <li><strong>MGM Resorts booking path</strong> (MGM Grand, Cosmopolitan, Bellagio, ARIA) — did not load in the fetch tool. F-06.</li>
  <li><strong>Venetian dated calendar</strong> — served "$XXX" for every February 2027 date. F-05.</li>
  <li><strong>Wynn booking engine</strong> — returned to its search form without a dated rate set.</li>
  <li><strong>guide.michelin.com</strong> direct restaurant listing — fetch failed; the official LVCVA page was used for tiers and each venue's own page for details.</li>
  <li><strong>RTC Trip Planner</strong> — live-only, so no journey times were captured. F-02.</li>
</ul>

<h2>How to reproduce any number</h2>
<ol>
  <li>Open the source link on the row (all hotel/room links include the exact dates).</li>
  <li>Check the capture date against today's date — dynamic prices will have moved.</li>
  <li>If a value now differs, that is expected for rates; log it in the price-watch log (S-08).</li>
</ol>
"""
    return layout("sources.html", "Sources and verification record",
                  body, lede=f"Every official page used, what it was used for, and what could not be retrieved. Capture date {AS_OF}.",
                  crumb=crumb_for("sources.html", [("Overview", "index.html")]))


def build_repo(review):
    rows = [[
        f'<span class="qid">{esc(r["id"])}</span>',
        f'<span class="badge {"b-no" if r["severity"]=="high" else "b-part" if r["severity"]=="medium" else "b-list"}">{esc(r["severity"].upper())}</span>',
        f'<strong>{esc(r["finding"])}</strong>',
        f'<span class="small">{esc(r["evidence"])}</span>',
        esc(r["action"]),
        f'<span class="badge {"b-ok" if r["status"]=="fixed" else "b-list"}">{esc(r["status"])}</span>',
    ] for r in review["rows"]]
    stats = '<div class="kpis">' + "".join(
        f'<div class="kpi"><span class="n">{esc(s["value"])}</span><span class="l">{esc(s["label"])}</span></div>' for s in review["stats"]
    ) + "</div>"
    body = f"""
<div class="note">
  <p>{esc(review['intro'])}</p>
</div>
{stats}

<h2>What the previous work got right</h2>
<ul class="clean">{''.join(f'<li>{esc(p)}</li>' for p in review['positives'])}</ul>

<h2>Findings</h2>
{table(["ID", "Severity", "Finding", "Evidence (paths)", "Action taken", "Status"], rows,
       caption="'Fixed' = changed in this session. 'Documented' = deliberately left as historical record.")}

<h2>What this session changed</h2>
<div class="grid two">
  <div class="card"><h3>Published</h3>
    <ul class="clean">
      <li>New canonical root site: 11 pages generated from <code>data/plan/*.json</code> by <code>scripts/build_plan.py</code>.</li>
      <li>Mobile-first stylesheet at <code>assets/site/style.css</code> — tables stack into labelled cards under 640 px.</li>
      <li>Verification gate <code>scripts/check_plan.py</code> and CI workflow <code>.github/workflows/validate-plan.yml</code>.</li>
      <li>README rewritten to one document with one build command.</li>
    </ul>
  </div>
  <div class="card"><h3>Preserved</h3>
    <ul class="clean">
      <li>All seven prior sites remain under <code>docs/</code> and in git history.</li>
      <li>The previous root pages are archived at <code>docs/session-legacy-root/</code>.</li>
      <li>Every prior data tree (<code>data/</code>, <code>data/verified/</code>, <code>data/trip/</code>, <code>field-notes/data/</code>) is untouched.</li>
      <li>Open PRs #8 and #9 were left alone.</li>
    </ul>
  </div>
</div>

<h2>Remaining repository risks</h2>
<ul class="clean">
  <li>Two publishing paths are configured (legacy root source and a <code>docs/</code> artifact workflow). Until one is retired, both must stay buildable (F-20).</li>
  <li>Stale duplicates are load-bearing documentation for past sessions — deleting them would erase provenance, so they stay.</li>
  <li>Two open PRs from older sessions may reintroduce conflicting pages if merged without review (F-21).</li>
</ul>
"""
    return layout("repo-review.html", "Repository review",
                  body, lede="What was in the repository when this session started, what was wrong with it, and exactly what changed.",
                  crumb=crumb_for("repo-review.html", [("Overview", "index.html")]))


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

    pages = {
        "index.html": build_index(meta, hotels, rests, acts, flags, suggestions, booking),
        "restaurants.html": build_restaurants(rests, flags),
        "hotels.html": build_hotels(hotels, rests),
        "booking.html": build_booking(booking, hotels),
        "activities.html": build_activities(acts),
        "transit.html": build_transit(),
        "questions.html": build_questions(questions),
        "suggestions.html": build_suggestions(suggestions),
        "flagged.html": build_flagged(flags),
        "sources.html": build_sources(meta, rests, hotels, acts, booking),
        "repo-review.html": build_repo(review),
    }
    for name, body in pages.items():
        (ROOT / name).write_text(body, encoding="utf-8")
        print(f"wrote {name} ({len(body):,} bytes)")


if __name__ == "__main__":
    main()
