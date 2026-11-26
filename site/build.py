#!/usr/bin/env python3
"""Build the static GitHub Pages site from data/*.json.

Output: docs/*.html (served by GitHub Pages from /docs).
Standard library only. Fails (exit 1) when:
  - a data row has no source ID, or a source ID is not in data/sources.json
  - a flag ID is referenced but not defined in data/flags.json
  - an internal link points to a page or anchor that does not exist
"""
import datetime
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "docs"
ERRORS = []


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SOURCES_DOC = load("sources.json")
SOURCES = {s["id"]: s for s in SOURCES_DOC["sources"]}
FLAGS = {f["id"]: f for f in load("flags.json")["flags"]}
HOTELS = load("hotels.json")
RESTAURANTS = load("restaurants.json")["restaurants"]
ACTIVITIES = load("activities.json")["activities"]
QUESTIONS = load("questions.json")["questions"]
SUGGESTIONS = load("suggestions.json")["suggestions"]
REPO = load("repo_review.json")["findings"]
REST_BY_ID = {r["id"]: r for r in RESTAURANTS}
AS_OF = "2026-11-26"


def esc(v):
    return "" if v is None else html.escape(str(v), quote=True)


def check_sources(row_id, ids):
    if not ids:
        ERRORS.append(f"{row_id}: no source IDs")
    for i in ids:
        if i not in SOURCES:
            ERRORS.append(f"{row_id}: unknown source {i}")


def check_flags(row_id, ids):
    for f in ids:
        if f not in FLAGS:
            ERRORS.append(f"{row_id}: unknown flag {f}")


def src_links(ids):
    out = []
    for i in ids:
        s = SOURCES.get(i)
        if not s:
            continue
        out.append(f'<a class="src" href="{esc(s["url"])}" target="_blank" rel="noopener" title="{esc(s["publisher"])}">{esc(i)}</a>')
    return " ".join(out)


def flag_links(ids):
    out = []
    for f in ids:
        if f in FLAGS:
            out.append(f'<a class="flag" href="flagged.html#{esc(f)}">{esc(f)}</a>')
    return " ".join(out)


def val(v, flag=None):
    """Blank values are shown as UNVERIFIED with a link to the flag; never filled in."""
    if v is None or v == "":
        f = f' <a class="flag" href="flagged.html#{esc(flag)}">{esc(flag)}</a>' if flag else ""
        return f'<span class="unv">Unverified</span>{f}'
    return esc(v)


NAV = [
    ("index.html", "Home"),
    ("hotels.html", "Hotels"),
    ("restaurants.html", "Restaurants"),
    ("activities.html", "Activities"),
    ("analysis.html", "Analysis"),
    ("questions.html", "Questions"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged for Review"),
    ("sources.html", "Sources"),
    ("repo-review.html", "Repo Review"),
]


def page(filename, title, body, active):
    nav_items = []
    for href, label in NAV:
        cls = ' class="on"' if href == active else ""
        nav_items.append(f'<a href="{href}"{cls}>{esc(label)}</a>')
    nav = "".join(nav_items)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Las Vegas Trip Planner</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="brand"><a href="index.html">Las Vegas Trip Planner</a><span class="asof">Data as of {AS_OF}</span></div>
  <nav class="nav" aria-label="Main">{nav}</nav>
</header>
<main>
<h1>{esc(title)}</h1>
{body}
</main>
<footer class="foot">
  <p>Every value links to an official source ID (see <a href="sources.html">Sources</a>). Blank cells read <span class="unv">Unverified</span> and are listed on <a href="flagged.html">Flagged for Review</a>. Nothing here is inferred.</p>
  <p>Data files: <code>data/*.json</code> · Build: <code>site/build.py</code> · Repository: <a href="https://github.com/kanlerxz87-cyber/Vegas2">kanlerxz87-cyber/Vegas2</a></p>
</footer>
</body>
</html>
"""
    (OUT / filename).write_text(doc, encoding="utf-8")


def table(headers, rows, cls=""):
    """rows: list of lists of pre-rendered HTML cells (same length as headers)."""
    thead = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = []
    for r in rows:
        tds = "".join(f'<td data-label="{esc(h)}">{c}</td>' for h, c in zip(headers, r))
        body.append(f"<tr>{tds}</tr>")
    return (f'<div class="table-wrap"><table class="{cls}"><thead><tr>{thead}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


def star_text(mc):
    parts = []
    if mc["two_star"]:
        parts.append(f'{mc["two_star"]} × 2★')
    if mc["one_star"]:
        parts.append(f'{mc["one_star"]} × 1★')
    if mc["bib_gourmand"]:
        parts.append(f'{mc["bib_gourmand"]} Bib')
    if mc["recommended"]:
        parts.append(f'{mc["recommended"]} Rec')
    return ", ".join(parts) if parts else "None"


def badge(text, kind):
    return f'<span class="badge {kind}">{esc(text)}</span>'


# ---------------------------------------------------------------- index
def page_index():
    n_rest = len(RESTAURANTS)
    n_star = sum(1 for r in RESTAURANTS if r["tier"] in ("1-star", "2-star"))
    n_hotels = len(HOTELS["hotels"])
    n_act = len(ACTIVITIES)
    n_flags = len(FLAGS)
    cards = [
        ("hotels.html", "Hotels", f"{n_hotels} shortlisted, ranked by Michelin restaurants inside the resort. Prices and bed/bath not yet verified."),
        ("restaurants.html", "Michelin restaurants", f"All {n_rest} Las Vegas listings from the 2026 MICHELIN Guide Southwest, with official addresses."),
        ("activities.html", "Activities", f"{n_act} activities checked against official park, agency and venue pages."),
        ("analysis.html", "Analysis", "Clusters, trip-date options, booking-time facts and transit limits."),
        ("questions.html", "Questions", "What must be answered before deciding, and how to find each answer."),
        ("suggestions.html", "Suggestions", "Site and data improvements. Awaiting your approval. Nothing has been applied."),
        ("flagged.html", "Flagged for Review", f"{n_flags} irregularities, conflicts and unverified items, with source links."),
        ("sources.html", "Sources", f"{len(SOURCES)} source IDs. Official sources are marked as such."),
        ("repo-review.html", "Repo review", "Line-by-line review of the repository with evidence and flags."),
    ]
    card_html = "".join(
        f'<a class="card" href="{h}"><h3>{esc(t)}</h3><p>{esc(d)}</p><span class="go">Open →</span></a>'
        for h, t, d in cards
    )
    stats = [
        (n_rest, "Michelin listings (LV)"),
        (n_star, "Starred restaurants"),
        (n_hotels, "Hotels shortlisted"),
        (sum(1 for h in HOTELS["hotels"] if h["price_7_nights_usd"] is not None), "Hotel 7-night totals verified"),
        (n_flags, "Flags for review"),
    ]
    stat_html = "".join(f'<div class="stat"><div class="n">{esc(n)}</div><div class="l">{esc(l)}</div></div>' for n, l in stats)
    summary = """
<section class="panel">
<h2>Executive summary</h2>
<ul class="bullets">
<li><strong>Dates.</strong> Preferred stay is Mon Feb 15 – Thu Feb 18, 2027 (3 nights). Feb 15 is Washington's Birthday, a federal holiday [<a href="sources.html#S10">S10</a>]. The brief also asks for 7-night totals, so both views are kept. <a href="questions.html#Q-01">Q-01</a></li>
<li><strong>Michelin.</strong> Las Vegas has 24 listings in the inaugural 2026 Southwest guide: 4 starred (Joël Robuchon 2★; L'Atelier, é by José Andrés and Guy Savoy 1★), 3 Bib Gourmand and 17 Recommended [<a href="sources.html#S01">S01</a>, <a href="sources.html#S02">S02</a>].</li>
<li><strong>Best in-resort Michelin count.</strong> The Venetian (4 Recommended), then MGM Grand (2 starred, 3 stars in total), then The Cosmopolitan (1★ + Bib) [<a href="analysis.html">Analysis</a>].</li>
<li><strong>Hotel prices.</strong> No verified 7-night total exists yet. Official booking pages returned no Feb 2027 rates [<a href="sources.html#S08">S08</a>]. The one verified fee is Caesars Palace's resort fee: $62.30 per night incl. tax [<a href="sources.html#S08">S08</a>].</li>
<li><strong>Room requirements.</strong> Queen-or-larger bed and private bathroom are unverified for every hotel [<a href="flagged.html#F05">F05</a>].</li>
<li><strong>Transit.</strong> Official transit sources show RTC buses and the Strip monorail. No subway appears in them [<a href="sources.html#S11">S11</a>, <a href="sources.html#S12">S12</a>]. Red Rock Canyon has no public transit [<a href="sources.html#S13">S13</a>], so it cannot meet the bus-only test.</li>
<li><strong>Cheapest time to book.</strong> Cannot be determined from official sources yet. Official offers exist (Caesars advance purchase up to 30%, terms apply) [<a href="sources.html#S09">S09</a>].</li>
<li><strong>Next steps.</strong> Answer Q-01 to Q-08 and approve the suggestions. Then price the chosen dates on each official booking engine.</li>
</ul>
</section>
"""
    howto = """
<section class="panel legend">
<h2>How to read this site</h2>
<p><span class="unv">Unverified</span> means no official source confirmed the value, so the cell is blank and flagged. Source IDs (S01, S02…) link to the page they came from. Flag IDs (F01…) link to the review list.</p>
</section>
"""
    body = f"""
<div class="stats">{stat_html}</div>
{summary}
<section><h2>Pages</h2><div class="cards">{card_html}</div></section>
{howto}
"""
    page("index.html", "Las Vegas Trip Planner: Feb 15 – Mar 23, 2027", body, "index.html")


# ---------------------------------------------------------------- hotels
def page_hotels():
    headers = ["Rank", "Hotel", "Area", "Michelin in resort", "Stars / Bib / Rec", "Address", "Resort fee / night",
               "Private bathroom", "Queen+ bed", "7-night total", "Best time to book", "Sources", "Flags"]
    rows = []
    for h in HOTELS["hotels"]:
        check_sources(h["id"], h["sources"])
        check_flags(h["id"], h["flags"])
        names = ", ".join(REST_BY_ID[r]["name"] for r in h["michelin_restaurants"])
        mc = h["michelin_counts"]
        counts = star_text(mc)
        rf = h["resort_fee_per_night_usd"]
        rf_cell = f"${rf:.2f} (verified, S08)" if rf is not None else val(None, "F08")
        rows.append([
            esc(h["rank"]),
            f'<strong>{esc(h["name"])}</strong><br><span class="small">{esc(names)}</span>',
            esc(h["area"]),
            esc(len(h["michelin_restaurants"])),
            esc(counts),
            esc(h["address"]),
            rf_cell,
            val(None, "F05"),
            val(None, "F05"),
            val(h["price_7_nights_usd"], "F06"),
            val(None, "F04"),
            src_links(h["sources"]),
            flag_links(h["flags"]),
        ])
    body = f"""
<p class="lede">Ranked by the number of 2026 MICHELIN Guide restaurants inside the same resort (address match). Trip window: Feb 15 – Mar 23, 2027. Preferred stay 3 nights (Feb 15–18). Cost basis requested: 7 nights for 2 adults. <a href="analysis.html">Method and trip-date options</a>.</p>
<div class="note"><strong>Not yet verified:</strong> 7-night totals, queen-or-larger bed, private bathroom, best time to book. These are blank on purpose. <a href="questions.html">Questions Q-02 to Q-05</a> explain what is needed.</div>
{table(headers, rows, "hotels")}
"""
    page("hotels.html", "Hotels", body, "hotels.html")


# ---------------------------------------------------------------- restaurants
def social_cell(r):
    parts = []
    for label, k in (("YouTube", "social_youtube"), ("TikTok", "social_tiktok"), ("Instagram", "social_instagram")):
        v = r.get(k)
        if v:
            parts.append(f'<a href="{esc(v.split(" ")[0])}" target="_blank" rel="noopener">{label}</a>')
    return " · ".join(parts) if parts else val(None, "F19")


def distinction_badge(tier, text):
    kind = {"2-star": "star2", "1-star": "star1", "bib": "bib", "recommended": "rec"}.get(tier, "rec")
    return badge(text, kind)


def page_restaurants():
    headers = ["#", "Michelin distinction", "Restaurant", "Area", "Cuisine", "Address", "Hours", "Days open",
               "Closed", "Exceptions", "Dress code", "Phone", "Price level", "Price for 2 (USD)", "Social media",
               "Official site", "Sources", "Flags"]
    rows = []
    for r in RESTAURANTS:
        check_sources(r["id"], r["sources"])
        check_flags(r["id"], r["flags"])
        site = f'<a href="{esc(r["official_site"])}" target="_blank" rel="noopener">Site</a>' if r.get("official_site") else val(None)
        rows.append([
            esc(r["id"]),
            distinction_badge(r["tier"], r["distinction"]),
            f'<strong>{esc(r["name"])}</strong>',
            esc(r["area"]),
            esc(r["cuisine"]) if r.get("cuisine") else val(None),
            esc(r["address"]),
            val(r.get("hours"), "F17" if r.get("hours") is None else None),
            val(r.get("days_open")),
            val(r.get("closed_days")) if r.get("closed_days") else "—",
            esc(r["exceptions"]) if r.get("exceptions") else "—",
            esc(r["dress_code"]) if r.get("dress_code") else val(None),
            esc(r["phone"]) if r.get("phone") else val(None),
            esc(r["price_level"]) if r.get("price_level") else val(None),
            val(r.get("price_for_two_usd"), "F18"),
            social_cell(r),
            site,
            src_links(r["sources"]),
            flag_links(r["flags"]),
        ])
    body = f"""
<p class="lede">All 24 Las Vegas restaurants in the inaugural 2026 MICHELIN Guide Southwest. Distinction and address are from the official Michelin release [<a href="sources.html#S01">S01</a>]. Area and cuisine labels are from the LVCVA [<a href="sources.html#S03">S03</a>]. Hours are shown only when an official page confirms them.</p>
<div class="note"><strong>Verified so far:</strong> hours for Joël Robuchon, L'Atelier and é; partial for Kabuto. <strong>Not verified:</strong> hours for 20 listings, price for two for all, and social links for all. Restaurant social accounts were not confirmed from official pages (F19).</div>
{table(headers, rows, "restaurants")}
"""
    page("restaurants.html", "Michelin restaurants (Las Vegas, 2026)", body, "restaurants.html")


# ---------------------------------------------------------------- activities
def page_activities():
    headers = ["Activity", "Type", "Address", "Distance from Strip", "Public transit", "Hours", "Days open",
               "Exceptions", "Fees", "Phone", "Official site", "Social media", "Sources", "Flags"]
    rows = []
    for a in ACTIVITIES:
        check_sources(a["id"], a["sources"])
        check_flags(a["id"], a["flags"])
        soc = []
        for label, k in (("YouTube", "social_youtube"), ("TikTok", "social_tiktok"), ("Instagram", "social_instagram")):
            v = a.get(k)
            if v:
                url = v.split(" ")[0]
                soc.append(f'<a href="{esc(url)}" target="_blank" rel="noopener">{label}</a>' if url.startswith("http") else f"{label}: {esc(v)}")
        rows.append([
            f'<strong>{esc(a["name"])}</strong>',
            esc(a["type"]),
            esc(a["address"]),
            esc(a["distance_from_strip"]),
            esc(a["public_transit"]),
            esc(a["hours"]),
            esc(a["days_open"]) if a.get("days_open") else val(None, "F20"),
            esc(a["exceptions"]) if a.get("exceptions") else "—",
            esc(a["fees"]) if a.get("fees") else val(None),
            esc(a["phone"]) if a.get("phone") else "—",
            f'<a href="{esc(a["official_site"])}" target="_blank" rel="noopener">Official page</a>' if a.get("official_site") else val(None),
            " · ".join(soc) if soc else val(None, "F19"),
            src_links(a["sources"]),
            flag_links(a["flags"]),
        ])
    body = f"""
<p class="lede">Only activities checked against official pages. Each row gives the official hours and the distance the official page states. Drive and transit times that no official page states are left blank.</p>
<div class="note"><strong>Conflicts:</strong> Hoover Dam hours are unverified and sources disagree (<a href="flagged.html#F09">F09</a>). Red Rock Canyon has no public transit (<a href="flagged.html#F02">F02</a>).</div>
{table(headers, rows, "activities")}
"""
    page("activities.html", "Activities", body, "activities.html")


# ---------------------------------------------------------------- analysis
def weekday(d):
    return datetime.date.fromisoformat(d).strftime("%a")


def page_analysis():
    # trip date options
    dates = [
        ("Preferred (brief)", "2027-02-15", "2027-02-18", 3, "Feb 15 is Washington's Birthday (federal holiday) [S10]. Check-in is a Monday, check-out a Thursday."),
        ("Example 7-night stay (cost basis)", "2027-02-15", "2027-02-22", 7, "Inside the window. Used for price lookups. No price has been retrieved for it."),
        ("Latest 7-night stay in window", "2027-03-16", "2027-03-23", 7, "Last permitted check-out date in the brief."),
    ]
    drows = []
    for label, ci, co, n, note in dates:
        drows.append([
            f'<strong>{esc(label)}</strong>',
            f"{esc(ci)} ({weekday(ci)})",
            f"{esc(co)} ({weekday(co)})",
            esc(n),
            esc(note),
        ])
    date_tbl = table(["Option", "Check-in", "Check-out", "Nights", "Notes"], drows, "dates")

    # clusters
    crow = []
    for c in HOTELS["michelin_clusters"]:
        names = "<br>".join(f'{esc(REST_BY_ID[r]["name"])} <span class="small">({esc(REST_BY_ID[r]["distinction"])})</span>' for r in c["restaurants"])
        crow.append([f'<strong>{esc(c["name"])}</strong>', esc(c["count"]), names, esc(c["note"])])
    cluster_tbl = table(["Cluster", "Listings", "Restaurants (official distinction)", "Note"], crow, "clusters")

    # hotel ranking summary
    hrow = []
    for h in HOTELS["hotels"]:
        mc = h["michelin_counts"]
        hrow.append([esc(h["rank"]), f'<strong>{esc(h["name"])}</strong>', esc(len(h["michelin_restaurants"])),
                     esc(star_text(mc)),
                     src_links(h["sources"])])
    rank_tbl = table(["Rank", "Hotel", "Listings in resort", "Michelin breakdown", "Sources"], hrow, "ranking")

    # transit
    trow = [
        ["Las Vegas Monorail", "Mon 7:00 am – 12:00 am; Tue–Thu 7:00 am – 2:00 am; Fri–Sun 7:00 am – 3:00 am", "Seven Strip stations; trains every 4–8 minutes", src_links(["S12"])],
        ["RTC bus", "Not verified (no trip-planner times retrieved)", "RTC states a $118.5M annual shortfall and bus changes around the Strip", src_links(["S11"])],
        ["Red Rock Canyon", "Timed entry Oct 1 – May 31, 8:00 am – 5:00 pm", "No public transit; about 30 minutes from the Strip", src_links(["S13"])],
        ["Valley of Fire", "Sunrise to sunset, daily", "Rideshare return can be unreliable; drive time not stated", src_links(["S14"])],
    ]
    transit_tbl = table(["Option", "Hours / rule", "Limit", "Sources"], trow, "transit")

    body = f"""
<section class="panel">
<h2>1. Trip-date options</h2>
{date_tbl}
<p class="small">Day names are computed from the dates. Federal-holiday status comes from OPM [<a href="sources.html#S10">S10</a>].</p>
</section>

<section class="panel">
<h2>2. Michelin clusters (2026 Southwest, Las Vegas)</h2>
<p>Clusters are grouped by address, not by travel time. Travel time is not verified (<a href="flagged.html#F20">F20</a>).</p>
{cluster_tbl}
</section>

<section class="panel">
<h2>3. Hotel ranking (in-resort Michelin count)</h2>
<p>Ranking rule: number of listings inside the same resort; tie-break by stars, then Bib Gourmand. This is not a 1-hour transit count (<a href="flagged.html#F15">F15</a>).</p>
{rank_tbl}
</section>

<section class="panel">
<h2>4. Cheapest time to book: what can and cannot be concluded</h2>
<ul class="bullets">
<li><strong>Known (official):</strong> Caesars Palace advertises 'Advanced Purchase Savings', up to 30% off for stays 30+ days ahead, terms apply [<a href="sources.html#S09">S09</a>]. The Cosmopolitan lists an 'Advance Purchase Non-Refundable' rate type [<a href="sources.html#S20">S20</a>]. Caesars lists 'FREE 48-Hour Cancellation*' with terms not read [<a href="sources.html#S09">S09</a>].</li>
<li><strong>Known (official):</strong> the official booking page for Caesars Palace did not return February 2027 rates; it showed a December 2026 calendar [<a href="sources.html#S08">S08</a>].</li>
<li><strong>Cannot conclude:</strong> a cheapest booking date, a price trend, or a 7-night total. These need dated official rate records (see <a href="suggestions.html#S-01">S-01</a>).</li>
</ul>
</section>

<section class="panel">
<h2>5. Transit and access limits</h2>
{transit_tbl}
<p class="small">Las Vegas has no subway in the official sources reviewed, so 'subway or bus' is read as bus + monorail (<a href="flagged.html#F01">F01</a>).</p>
</section>

<section class="panel">
<h2>6. Method and limits</h2>
<ul class="bullets">
<li>Michelin status: official Michelin release (Aug 26, 2026) [<a href="sources.html#S01">S01</a>]. The guide.michelin.com pages were not reachable this session (<a href="flagged.html#F16">F16</a>).</li>
<li>A value appears only when an official page confirmed it. Every other cell is blank and flagged.</li>
<li>Third-party sources are used only to flag conflicts, never to fill a value.</li>
</ul>
</section>
"""
    page("analysis.html", "Analysis", body, "analysis.html")


# ---------------------------------------------------------------- questions
def page_questions():
    rows = []
    for q in QUESTIONS:
        check_sources(q["id"], q["source_ids"])
        rows.append([
            f'<strong id="{esc(q["id"])}">{esc(q["id"])}</strong>',
            badge(q["priority"], "pri-" + q["priority"].lower()),
            esc(q["question"]),
            esc(q["known"]),
            esc(q["missing"]),
            esc(q["how_to_find"]),
            esc(q["status"]),
            src_links(q["source_ids"]),
        ])
    body = f"""
<p class="lede">What must be answered before a reasonable decision can be made. 'Known' lists what official sources already show. 'Missing' lists what is not yet known. 'How to find it' names the next step, which is listed on <a href="suggestions.html">Suggestions</a>.</p>
{table(["ID", "Priority", "Question", "Known (sourced)", "Missing", "How to find it", "Status", "Sources"], rows, "questions")}
"""
    page("questions.html", "Questions and information gaps", body, "questions.html")


# ---------------------------------------------------------------- suggestions
def page_suggestions():
    rows = []
    for s in SUGGESTIONS:
        rows.append([
            f'<strong id="{esc(s["id"])}">{esc(s["id"])}</strong>',
            esc(s["area"]),
            f'<strong>{esc(s["title"])}</strong>',
            esc(s["why"]),
            esc(s["how"]),
            esc(s["effort"]),
            esc(s["decision_needed"]),
            badge("Awaiting approval", "pending"),
        ])
    body = f"""
<p class="lede">These are proposed changes only. Nothing here is implemented until you approve it. Choose the items you want; each one lists the decision it needs.</p>
<div class="note"><strong>How to respond:</strong> reply with the IDs you approve (for example, "approve S-01, S-02, S-03, S-06") and any changes to the scope.</div>
{table(["ID", "Area", "Suggestion", "Why", "How", "Effort", "Decision needed", "Status"], rows, "suggestions")}
"""
    page("suggestions.html", "Suggestions (awaiting your approval)", body, "suggestions.html")


# ---------------------------------------------------------------- flagged
def page_flagged():
    rows = []
    anchors = []
    for f in FLAGS.values():
        check_sources(f["id"], f["source_ids"])
        rows.append([
            f'<strong id="{esc(f["id"])}">{esc(f["id"])}</strong>',
            esc(f["category"]),
            f'<strong>{esc(f["title"])}</strong>',
            esc(f["detail"]),
            src_links(f["source_ids"]),
            esc(", ".join(f["affects"])),
        ])
        anchors.append(f["id"])
    body = f"""
<p class="lede">Irregularities, conflicts and unverified items. They do not block the merge. Each one names its sources so you can check it. Items are not fixed silently.</p>
<div class="note"><strong>{len(FLAGS)} flags.</strong> The most important: trip length (F03), no verified hotel price (F06), no verified room type (F05), and the 'subway' wording (F01).</div>
{table(["ID", "Category", "Title", "Detail", "Sources", "Affects"], rows, "flags")}
"""
    page("flagged.html", "Flagged for Review", body, "flagged.html")


# ---------------------------------------------------------------- sources
def page_sources():
    rows = []
    for s in SOURCES_DOC["sources"]:
        rows.append([
            f'<strong id="{esc(s["id"])}">{esc(s["id"])}</strong>',
            badge(s["type"], "official" if s["type"].startswith("official") else ("archived" if "archived" in s["type"] else "secondary")),
            esc(s["publisher"]),
            esc(s["title"]),
            f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["url"])}</a>',
            esc(s["used_for"]),
        ])
    body = f"""
<p class="lede">Source IDs used across all tables. Each row links to the page checked. 'Official' means issued by the entity itself or a government or tourism body. 'Secondary' means media or third-party, used only to flag conflicts. Retrieved {AS_OF}.</p>
{table(["ID", "Type", "Publisher", "Title", "Link", "Used for"], rows, "sources")}
"""
    page("sources.html", "Sources", body, "sources.html")


# ---------------------------------------------------------------- repo review
def page_repo():
    rows = []
    for f in REPO:
        check_sources(f["id"], f["source_ids"])
        rows.append([
            f'<strong>{esc(f["id"])}</strong>',
            f'<strong>{esc(f["item"])}</strong>',
            esc(f["result"]),
            esc(f["evidence"]),
            src_links(f["source_ids"]),
            flag_links([f["flag"]]) if f["flag"] else "—",
            esc(f["status"]),
        ])
    body = f"""
<p class="lede">Line-by-line review of the repository and its settings, at base commit c97c82a (main) and the working branch. Evidence comes from local git and the GitHub API. Flags link to the review list.</p>
{table(["ID", "Item", "Result", "Evidence", "Sources", "Flag", "Status"], rows, "repo")}
"""
    page("repo-review.html", "Repo review", body, "repo-review.html")


CSS = """
:root{--ink:#1d2433;--muted:#5b6474;--line:#e3e7ef;--bg:#f6f8fb;--card:#fff;--brand:#1f5fbf;--warn:#b35c00;--ok:#1b7a3d;--unv:#8a4b00;--unvbg:#fff4e0}
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--brand)}
header.top{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
.brand{display:flex;justify-content:space-between;align-items:center;padding:10px 16px;gap:8px;flex-wrap:wrap}
.brand a{font-weight:700;text-decoration:none;color:var(--ink);font-size:18px}
.asof{font-size:12px;color:var(--muted)}
.nav{display:flex;gap:6px;flex-wrap:wrap;padding:0 16px 10px}
.nav a{font-size:13px;padding:5px 9px;border-radius:999px;background:#eef3fb;text-decoration:none;color:var(--brand)}
.nav a.on{background:var(--brand);color:#fff}
main{max-width:1280px;margin:0 auto;padding:16px}
h1{font-size:26px;margin:8px 0 12px}
h2{font-size:20px;margin:0 0 10px}
h3{margin:0 0 6px;font-size:17px}
.lede{color:var(--muted);max-width:900px}
.small{font-size:12px;color:var(--muted)}
.panel{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:0 0 16px}
.bullets li{margin:6px 0}
.note{background:#eef6ff;border:1px solid #cfe2ff;border-radius:10px;padding:10px 12px;margin:10px 0 14px;font-size:14px}
.legend{background:#fbfcfe}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:8px 0 16px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px}
.stat .n{font-size:26px;font-weight:700;color:var(--brand)}
.stat .l{font-size:13px;color:var(--muted)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:var(--ink)}
.card:hover{border-color:var(--brand)}
.card p{margin:0 0 8px;color:var(--muted);font-size:14px}
.card .go{color:var(--brand);font-size:14px;font-weight:600}
.table-wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px;margin:0 0 20px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#f1f4f9;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);position:sticky;top:0}
tr:last-child td{border-bottom:none}
a.src{display:inline-block;font-size:12px;background:#eef3fb;padding:1px 6px;border-radius:6px;margin:1px 2px 1px 0;text-decoration:none}
a.flag{display:inline-block;font-size:12px;background:var(--unvbg);color:var(--unv);padding:1px 6px;border-radius:6px;margin:1px 2px 1px 0;text-decoration:none;border:1px solid #f1d4a4}
.unv{color:var(--unv);background:var(--unvbg);border-radius:6px;padding:0 5px;font-size:12px;font-style:italic}
.badge{display:inline-block;font-size:12px;padding:2px 8px;border-radius:999px;font-weight:600;white-space:nowrap}
.badge.star2,.badge.star1{background:#fff1c2;color:#7a5200}
.badge.bib{background:#e4f5ea;color:#17602f}
.badge.rec{background:#eef3fb;color:#1f4f9a}
.badge.official{background:#e4f5ea;color:#17602f}
.badge.archived{background:#f0ecf9;color:#4b3a7a}
.badge.secondary{background:#f3f3f3;color:#555}
.badge.pending{background:#fff4e0;color:#8a4b00}
.badge.pri-high{background:#fde2e1;color:#8a1f1a}
.badge.pri-medium{background:#fff4e0;color:#8a4b00}
.badge.pri-low{background:#eef3fb;color:#1f4f9a}
.foot{max-width:1280px;margin:20px auto;padding:0 16px 30px;color:var(--muted);font-size:13px}
code{background:#eef1f6;padding:0 4px;border-radius:4px}
@media (max-width:760px){
  main{padding:10px}
  h1{font-size:22px}
  .table-wrap{overflow:visible;background:transparent;border:none}
  table,thead,tbody,tr,td{display:block;width:100%}
  thead{display:none}
  tr{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:0 0 12px;padding:6px 10px}
  td{border:none;padding:6px 0;border-bottom:1px dashed var(--line)}
  td:last-child{border-bottom:none}
  td::before{content:attr(data-label);display:block;font-size:11px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);font-weight:600;margin-bottom:2px}
}
"""


def write_css():
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    (OUT / "assets" / "style.css").write_text(CSS, encoding="utf-8")


def check_internal_links():
    """Every relative href must point to an existing file; anchors must exist."""
    href_re = re.compile(r'href="([^"]+)"')
    id_re = re.compile(r'id="([^"]+)"')
    ids_by_file = {p.name: set(id_re.findall(p.read_text(encoding="utf-8"))) for p in OUT.glob("*.html")}
    for p in OUT.glob("*.html"):
        for href in href_re.findall(p.read_text(encoding="utf-8")):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target, _, anchor = href.partition("#")
            if target == "":
                target = p.name
            if target.startswith("assets/"):
                if not (OUT / target).exists():
                    ERRORS.append(f"{p.name}: missing asset {target}")
                continue
            if target not in ids_by_file:
                ERRORS.append(f"{p.name}: broken link {href}")
                continue
            if anchor and anchor not in ids_by_file[target]:
                ERRORS.append(f"{p.name}: missing anchor #{anchor} in {target}")


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    write_css()
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    page_index()
    page_hotels()
    page_restaurants()
    page_activities()
    page_analysis()
    page_questions()
    page_suggestions()
    page_flagged()
    page_sources()
    page_repo()
    check_internal_links()
    if ERRORS:
        print("BUILD FAILED:")
        for e in ERRORS:
            print("  -", e)
        return 1
    print(f"Built {len(list(OUT.glob('*.html')))} pages into {OUT.relative_to(ROOT)}/ with 0 errors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
