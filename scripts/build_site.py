#!/usr/bin/env python3
"""Build the static Las Vegas trip-planning site from data/*.json.

Output: HTML pages written to docs/ (GitHub Pages serves docs/ from main via
.github/workflows/pages.yml). Data is read from data/verified/. The assets are
copied from assets/style.css. No third-party dependencies.

Usage:  python3 scripts/build_site.py
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "verified"
OUT = ROOT / "docs"
ASSETS = ROOT / "assets"
AS_OF = "2026-11-26"


def load(name):
    with open(DATA / f"{name}.json", encoding="utf-8") as fh:
        return json.load(fh)


def esc(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- cells ----
BADGE = {
    "v": ('<span class="b bv">Verified</span>', "Verified"),
    "p": ('<span class="b bp">Partial</span>', "Partial"),
    "u": ('<span class="b bu">Unverified</span>', "Unverified"),
}


def strip_unverified_prefix(text):
    for prefix in ("Unverified — ", "Unverified - ", "Unverified"):
        if text.startswith(prefix):
            return text[len(prefix):].lstrip(" —-")
    return text


def cell(value):
    """Render a verification cell: {'s': 'v'|'p'|'u', 't': text} or plain text."""
    if isinstance(value, dict):
        s = value.get("s", "u")
        text = value.get("t", "")
        if s == "u":
            rest = strip_unverified_prefix(text)
            return BADGE["u"][0] + (f'<div class="sub">{esc(rest)}</div>' if rest else "")
        return BADGE.get(s, BADGE["u"])[0] + f'<div class="sub">{esc(text)}</div>'
    if value is None or value == "":
        return BADGE["u"][0]
    return esc(value)


def sources_html(items):
    if not items:
        return '<span class="b bu">No source</span>'
    links = []
    for it in items:
        links.append(
            f'<li><a href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["label"])}</a></li>'
        )
    return '<ul class="srcs">' + "".join(links) + "</ul>"


def count_states(obj_list, fields):
    counts = {"v": 0, "p": 0, "u": 0}
    for row in obj_list:
        for f in fields:
            v = row.get(f)
            if isinstance(v, dict):
                counts[v.get("s", "u")] = counts.get(v.get("s", "u"), 0) + 1
    return counts


# --------------------------------------------------------------- layout ----
NAV = [
    ("index.html", "Home"),
    ("hotels.html", "Hotels"),
    ("michelin.html", "Michelin"),
    ("activities.html", "Activities"),
    ("booking.html", "Booking & price"),
    ("questions.html", "Questions"),
    ("suggestions.html", "Suggestions"),
    ("flagged.html", "Flagged for Review"),
    ("repo-review.html", "Repo review"),
    ("sources.html", "Sources"),
]
OTHER_BUILDS = [
    ("session-fd2715d0/index.html", "Source-first category audit (session fd2715d0)"),
    ("session-36cc5108/index.html", "Second build (session 36cc5108)"),
    ("planner-v1/index.html", "Earlier dashboard (v1)"),
]


def page(filename, title, body, active):
    links = []
    for href, label in NAV:
        cls = ' class="on"' if href == active else ""
        links.append(f'<a href="{href}"{cls}>{esc(label)}</a>')
    nav_links = "".join(links)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Las Vegas Trip Planner</title>
<meta name="description" content="Las Vegas trip planning dashboard: hotels, Michelin restaurants, activities and verification status. Verified from official sources; unverified values are left blank.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="brand" href="index.html">Las Vegas Trip Planner</a>
    <nav class="nav" aria-label="Main">{nav_links}</nav>
  </div>
</header>
<main class="wrap">
{body}
</main>
<footer class="foot">
  <div class="wrap">
    Data as of {AS_OF}. Only values confirmed on official sources are shown as verified.
    Blank cells are marked <span class="b bu">Unverified</span>.
    Other builds in this repository:
    {" · ".join(f'<a href="{esc(h)}">{esc(l)}</a>' for h, l in OTHER_BUILDS)}.
    Source code: <a href="https://github.com/kanlerxz87-cyber/Vegas2" target="_blank" rel="noopener">github.com/kanlerxz87-cyber/Vegas2</a>.
  </div>
</footer>
</body>
</html>
"""
    (OUT / filename).write_text(doc, encoding="utf-8")
    print("wrote", filename)


def table(headers, rows_html, cls="tbl"):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    return f'<div class="tblwrap"><table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{"".join(rows_html)}</tbody></table></div>'


def row(cells, labels):
    tds = "".join(f'<td data-label="{esc(l)}">{c}</td>' for c, l in zip(cells, labels))
    return f"<tr>{tds}</tr>"


def legend():
    return """<div class="legend">
<span class="b bv">Verified</span> confirmed on an official page ·
<span class="b bp">Partial</span> official page covers part of the claim ·
<span class="b bu">Unverified</span> not confirmed — left blank by rule
</div>"""


# ----------------------------------------------------------------- pages ---
def build_hotels():
    d = load("hotels")
    rows = d["rows"]
    fields = ["queen", "private_bath", "transit_1hr", "price_7n", "price_3n", "book_timing", "social"]
    counts = count_states(rows, fields)
    labels = ["Rank", "Hotel", "Michelin on same campus", "2 queen beds", "Private bath",
              "7-night total (Feb 15–22, 2027)", "3-night total (Feb 15–18, 2027)",
              "Within 1 hr by bus/subway", "Cheapest booking time", "Social (YouTube/TikTok/IG)", "Sources"]
    rows_html = []
    for r in rows:
        hotel = (f'<strong>{esc(r["name"])}</strong><div class="sub">{esc(r["cluster"])}</div>'
                 f'<div class="sub">{esc(r["address"])}</div>')
        mich = (f'<strong>{r["michelin_on_campus"]}</strong><div class="sub">{esc(r["michelin_on_campus_list"])}</div>')
        cells = [
            f'<strong>{r["rank"]}</strong>',
            hotel,
            mich,
            cell(r["queen"]),
            cell(r["private_bath"]),
            cell(r["price_7n"]),
            cell(r["price_3n"]),
            cell(r["transit_1hr"]),
            cell(r["book_timing"]),
            cell(r["social"]),
            sources_html(r["src"]),
        ]
        rows_html.append(row(cells, labels))
    body = f"""
<h1>Hotels — Strip candidates</h1>
<p class="lead">Eight Strip resorts that host at least one restaurant on the official 2026 Michelin Southwest list.
Ranked by the number of Michelin restaurants on the same resort campus (official addresses).
Room, price and transit fields are verified only where an official page confirmed them.</p>
<div class="callout"><strong>Stay options:</strong> {esc(d['stay']['preferred'])}; {esc(d['stay']['seven_night'])}.
<br><strong>Holiday:</strong> {esc(d['stay']['holiday_note'])}</div>
<div class="kpis">
  <div class="kpi"><span>{len(rows)}</span>hotels reviewed</div>
  <div class="kpi ok"><span>{counts['v']}</span>verified cells</div>
  <div class="kpi warn"><span>{counts['p']}</span>partial cells</div>
  <div class="kpi bad"><span>{counts['u']}</span>unverified cells</div>
</div>
{legend()}
<p class="note"><strong>Method:</strong> {esc(d['method'])}</p>
<h2>Ranking</h2>
{table(labels, rows_html)}
"""
    page("hotels.html", "Hotels", body, "hotels.html")


def build_michelin():
    d = load("michelin")
    rows = d["rows"]
    fields = ["hours", "price_2adults", "reservations", "social"]
    counts = count_states(rows, fields)
    groups = [("Starred", "Starred (4)"), ("Bib Gourmand", "Bib Gourmand (3)"), ("Recommended", "Michelin Recommended (17)")]
    labels = ["Restaurant", "Michelin status", "Cuisine", "Address & area", "Days & hours",
              "Cost for 2 adults (total)", "Reservations", "Social (YouTube/TikTok/IG)", "Sources"]
    sections = []
    for key, heading in groups:
        grp = [r for r in rows if r["status_group"] == key]
        rows_html = []
        for r in grp:
            cells = [
                f'<strong>{esc(r["name"])}</strong>',
                f'<span class="pill">{esc(r["status"])}</span>',
                esc(r["cuisine"]),
                f'{esc(r["address"])}<div class="sub">Area: {esc(r["cluster"])}</div>',
                cell(r["hours"]),
                cell(r["price_2adults"]),
                cell(r["reservations"]),
                cell(r["social"]),
                sources_html(r["src"]),
            ]
            rows_html.append(row(cells, labels))
        sections.append(f"<h2>{esc(heading)}</h2>{table(labels, rows_html)}")
    body = f"""
<h1>Michelin restaurants — Las Vegas 2026</h1>
<p class="lead">All 24 Las Vegas entries in the official 2026 Michelin Guide Southwest selection (announced Aug 26, 2026).
Status is taken from the official Michelin release. Hours, prices and social links appear only when an official page confirmed them.</p>
<div class="callout"><strong>Official summary:</strong> {esc(d['summary'])}</div>
<div class="kpis">
  <div class="kpi"><span>24</span>Las Vegas restaurants</div>
  <div class="kpi ok"><span>{counts['v']}</span>verified cells</div>
  <div class="kpi warn"><span>{counts['p']}</span>partial cells</div>
  <div class="kpi bad"><span>{counts['u']}</span>unverified cells</div>
</div>
{legend()}
<p class="note"><strong>Price note:</strong> {esc(d['price_note'])}</p>
{''.join(sections)}
<p class="note">Michelin link: <a href="{esc(d['source_status'])}" target="_blank" rel="noopener">{esc(d['source_status_label'])}</a></p>
"""
    page("michelin.html", "Michelin restaurants", body, "michelin.html")


def build_activities():
    d = load("activities")
    rows = d["rows"]
    fields = ["distance", "hours", "fees", "exceptions", "reservation", "social"]
    counts = count_states(rows, fields)
    labels = ["Place", "Type", "Distance from Strip", "Days open & hours", "Cost",
              "Exceptions", "Reservation", "Social (YouTube/TikTok/IG)", "Sources"]
    rows_html = []
    for r in rows:
        cells = [
            f'<strong>{esc(r["name"])}</strong>',
            esc(r["type"]),
            cell(r["distance"]),
            cell(r["hours"]),
            cell(r["fees"]),
            cell(r["exceptions"]),
            cell(r["reservation"]),
            cell(r["social"]),
            sources_html(r["src"]),
        ]
        rows_html.append(row(cells, labels))
    body = f"""
<h1>Activities</h1>
<p class="lead">{esc(d['note'])}</p>
<div class="kpis">
  <div class="kpi"><span>{len(rows)}</span>activities</div>
  <div class="kpi ok"><span>{counts['v']}</span>verified cells</div>
  <div class="kpi warn"><span>{counts['p']}</span>partial cells</div>
  <div class="kpi bad"><span>{counts['u']}</span>unverified cells</div>
</div>
{legend()}
<h2>Attractions</h2>
{table(labels, rows_html)}
"""
    page("activities.html", "Activities", body, "activities.html")


def build_booking():
    d = load("booking")
    h = load("hotels")
    labels = ["Option", "Check-in", "Check-out", "Nights", "Note"]
    rows_html = [row([esc(x["option"]), esc(x["check_in"]), esc(x["check_out"]), str(x["nights"]), esc(x["note"])], labels)
                 for x in d["dates"]]
    rl = ["Hotel", "3-night total (Feb 15–18)", "7-night total (Feb 15–22)"]
    rate_rows = [row([f'<strong>{esc(r["name"])}</strong>', cell(r["price_3n"]), cell(r["price_7n"])], rl) for r in h["rows"]]
    fl = ["Fact", "Source"]
    fact_rows = [row([esc(f["fact"]), sources_html([{"label": "Official source", "url": f["url"]}])], fl)
                 for f in d["timing"]["verified_booking_facts"]]
    body = f"""
<h1>Booking, price &amp; timing</h1>
<p class="lead">Dates are fixed by the brief. Prices and the cheapest booking time are <strong>not verified</strong>,
so they are blank. Nothing has been estimated.</p>
<div class="callout"><strong>Rate check:</strong> {esc(d['rate_results']['text'])}<br>
<strong>Booking timing:</strong> {esc(d['timing']['text'])}</div>
<h2>Stay options</h2>
{table(labels, rows_html)}
<p class="note">Sources: {sources_html(d['sources_dates'])}</p>
<h2>Hotel totals</h2>
{legend()}
{table(rl, rate_rows)}
<h2>Verified booking facts (official pages)</h2>
<p class="note">These are policies and advertised offers. They do not show that any date is cheapest.</p>
{table(fl, fact_rows)}
"""
    page("booking.html", "Booking & price", body, "booking.html")


def build_questions():
    d = load("questions")
    al = ["Question", "Answer", "Source"]
    ans_rows = [row([esc(a["q"]), esc(a["a"]), sources_html([{"label": "Source", "url": a["src"]}])], al)
                for a in d["answered"]]
    ol = ["ID", "Question", "Why it matters", "How to answer"]
    open_rows = [row([f'<strong>{esc(o["id"])}</strong>', esc(o["question"]), esc(o["why"]), esc(o["how"])], ol)
                 for o in d["open"]]
    ml = ["Information needed", "Status", "How to find it"]
    miss_rows = [row([esc(m["item"]), f'<span class="b bu">{esc(m["status"])}</span>', esc(m["how"])], ml)
                 for m in d["missing_info"]]
    body = f"""
<h1>Questions &amp; information gaps</h1>
<p class="lead">{esc(d['intro'])}</p>
<h2>Answered (with sources)</h2>
{table(al, ans_rows)}
<h2>Open questions for you</h2>
<p class="note">Answer these so the next pass can rank hotels and finish the travel-time test.</p>
{table(ol, open_rows)}
<h2>Information still missing</h2>
{table(ml, miss_rows)}
"""
    page("questions.html", "Questions", body, "questions.html")


def build_suggestions():
    d = load("suggestions")
    cards = []
    for s in d["items"]:
        cards.append(f"""<article class="card">
  <div class="cardtop"><span class="pill">{esc(s['id'])}</span><span class="tag">{esc(s['area'])}</span><span class="tag st">{esc(s['status'])}</span></div>
  <h3>{esc(s['title'])}</h3>
  <p>{esc(s['detail'])}</p>
  <dl><dt>Benefit</dt><dd>{esc(s['benefit'])}</dd><dt>Trade-off</dt><dd>{esc(s['tradeoff'])}</dd></dl>
</article>""")
    body = f"""
<h1>Suggestions for review</h1>
<p class="lead">{esc(d['intro'])}</p>
<div class="callout"><strong>How to choose:</strong> reply with the IDs you want (for example <em>S1, S4, S6</em>).
Only those are implemented. Nothing on this page changes the data.</div>
<div class="grid">{''.join(cards)}</div>
"""
    page("suggestions.html", "Suggestions", body, "suggestions.html")


def build_flagged():
    d = load("flagged")
    cards = []
    for f in d["items"]:
        cat_cls = {"Irregularity": "bad", "Source conflict": "warn", "Unverified": "bu", "Repo": "warn"}.get(f["category"], "bu")
        cards.append(f"""<article class="card">
  <div class="cardtop"><span class="pill">{esc(f['id'])}</span><span class="tag {cat_cls}">{esc(f['category'])}</span></div>
  <h3>{esc(f['title'])}</h3>
  <p>{esc(f['detail'])}</p>
  <div class="srcwrap"><strong>Source links for manual review</strong>{sources_html(f['src'])}</div>
</article>""")
    body = f"""
<h1>Flagged for Review</h1>
<p class="lead">{esc(d['intro'])}</p>
<div class="callout bad-call"><strong>Not blocking.</strong> These items are published here so you can review them after the site is live and ask for changes.</div>
<div class="grid">{''.join(cards)}</div>
"""
    page("flagged.html", "Flagged for Review", body, "flagged.html")


def build_repo():
    d = load("repo_review")
    labels = ["Item", "Finding", "Status", "Source"]
    rows_html = [row([f'<strong>{esc(i["item"])}</strong>', esc(i["finding"]), f'<span class="pill">{esc(i["status"])}</span>', sources_html(i["src"])], labels)
                 for i in d["items"]]
    body = f"""
<h1>Repo review</h1>
<p class="lead">{esc(d['scope'])}</p>
{table(labels, rows_html)}
"""
    page("repo-review.html", "Repo review", body, "repo-review.html")


def build_sources():
    d = load("sources")
    labels = ["Source", "Type", "Owner", "Used for", "Result", "Link"]
    rows_html = []
    for s in d["items"]:
        rows_html.append(row([
            esc(s["label"]),
            f'<span class="pill">{esc(s["type"])}</span>',
            esc(s["owner"]),
            esc(s["used_for"]),
            esc(s["result"]),
            f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">open</a>',
        ], labels))
    body = f"""
<h1>Sources</h1>
<p class="lead">{esc(d['note'])}</p>
{table(labels, rows_html)}
"""
    page("sources.html", "Sources", body, "sources.html")


def build_index():
    hot = load("hotels")
    mic = load("michelin")
    act = load("activities")
    flg = load("flagged")
    hc = count_states(hot["rows"], ["queen", "private_bath", "transit_1hr", "price_7n", "price_3n", "book_timing", "social"])
    mc = count_states(mic["rows"], ["hours", "price_2adults", "reservations", "social"])
    ac = count_states(act["rows"], ["distance", "hours", "fees", "exceptions", "reservation", "social"])
    total = {k: hc[k] + mc[k] + ac[k] for k in ("v", "p", "u")}
    cards = [
        ("hotels.html", "Hotels", "8 Strip candidates, ranked by Michelin count on campus, with room checks and blank prices."),
        ("michelin.html", "Michelin", "All 24 Las Vegas 2026 entries: 4 starred, 3 Bib Gourmand, 17 Recommended."),
        ("activities.html", "Activities", "Hoover Dam, Red Rock Canyon, Valley of Fire and The Neon Museum: official hours, fees and rules."),
        ("booking.html", "Booking & price", "Feb 15–18 and Feb 15–22, 2027 options. No verified 2027 rates yet."),
        ("questions.html", "Questions", "What we know, what we need from you, and what is still missing."),
        ("suggestions.html", "Suggestions", "Options for improving the site and the decision. Choose before anything changes."),
        ("flagged.html", "Flagged for Review", f"{len(flg['items'])} irregularities, source conflicts and unverified items, with links."),
        ("repo-review.html", "Repo review", "Line-by-line review of the repository and GitHub Pages settings."),
        ("sources.html", "Sources", "Every official and secondary source, and what each one was used for."),
        ("session-fd2715d0/index.html", "Source-first category audit", "Mobile-friendly tables for hotels, Michelin restaurants, activities and dates; live quotes and transit times remain unverified."),
        ("planner-v1/index.html", "Earlier dashboard (v1)", "The first single-page planner from PRs #2 and #3, kept unchanged for reference."),
        ("session-36cc5108/index.html", "Second build (session 36cc5108)", "The parallel site from PR #6 on main, kept unchanged. Its data is in data/*.json."),
    ]
    card_html = "".join(
        f'<a class="tile" href="{href}"><strong>{esc(title)}</strong><span>{esc(desc)}</span></a>'
        for href, title, desc in cards
    )
    body = f"""
<section class="hero">
  <h1>Las Vegas trip, Feb 15–22 2027</h1>
  <p class="lead">A simple dashboard for planning a 2-adult trip: hotels, Michelin restaurants, activities, booking and the open questions.
  Everything is checked against official sources. Anything that cannot be confirmed is blank and marked <span class="b bu">Unverified</span>.</p>
  <div class="kpis">
    <div class="kpi ok"><span>{total['v']}</span>verified cells</div>
    <div class="kpi warn"><span>{total['p']}</span>partial cells</div>
    <div class="kpi bad"><span>{total['u']}</span>unverified cells</div>
    <div class="kpi"><span>{len(flg['items'])}</span>items flagged</div>
  </div>
</section>

<section>
  <h2>Executive summary</h2>
  <ul class="sum">
    <li><strong>Dates.</strong> Preferred stay is 3 nights, Mon Feb 15 → Thu Feb 18, 2027. The full 7-night option is Feb 15 → Feb 22. Both are inside the Feb 15–Mar 23 window.
      <strong>Feb 15, 2027 is Washington's Birthday (Presidents' Day)</strong>, a federal holiday. <span class="src">[<a href="https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/" target="_blank" rel="noopener">OPM</a>]</span></li>
    <li><strong>Michelin, Las Vegas 2026 (official).</strong> 24 restaurants: 4 starred (Restaurant de Joël Robuchon at 2 stars; é by José Andrés, Guy Savoy Las Vegas and L'Atelier de Joël Robuchon at 1 star each), 3 Bib Gourmand, 17 Recommended. <span class="src">[<a href="https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s" target="_blank" rel="noopener">Michelin</a>]</span></li>
    <li><strong>Michelin clusters.</strong> 13 of the 24 are on the Strip (Las Vegas Blvd), 6 on Spring Mountain (Chinatown), and 5 elsewhere (Downtown/S. Main, S. Decatur, W. Russell, Gold Coast). Counts use official addresses.</li>
    <li><strong>Best-placed hotels by Michelin count on campus.</strong> The Venetian (4), then The Cosmopolitan and MGM Grand (2 each). Caesars Palace, Bellagio, Wynn, ARIA and Resorts World have 1 each. This is a campus count only; the 1-hour transit test is not verified.</li>
    <li><strong>Rooms.</strong> Two queen beds are confirmed on official pages for Resorts World (Conrad, one king <em>or</em> two queens), Bellagio (Premier Two Queen) and the Cosmopolitan (two-queen listing). ARIA is confirmed for its Center Tower Suite only. Wynn's two-queen claim was <strong>withdrawn</strong> after re-checking the official booking page (see Flagged F17). Caesars Palace, MGM Grand and The Venetian remain unverified.</li>
    <li><strong>Price and booking time.</strong> <em>No 2027 rate was verified for any hotel</em>, so totals and the cheapest booking time are blank. This is the largest gap.</li>
    <li><strong>Activities.</strong> Hoover Dam, Red Rock Canyon (timed entry Oct–May), Valley of Fire ($10/$15 fee) and The Neon Museum: hours and rules from official pages. You have not yet named your activity list (see Questions).</li>
    <li><strong>Irregularities.</strong> Secondary press gives different Michelin star holders and Bib lists than the official release. The official release is used throughout. Full list on <a href="flagged.html">Flagged for Review</a>.</li>
  </ul>
</section>

<section>
  <h2>Go to a page</h2>
  <div class="tiles">{card_html}</div>
</section>
"""
    page("index.html", "Home", body, "index.html")


def copy_assets():
    import shutil
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ASSETS / "style.css", OUT / "assets" / "style.css")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


def main():
    copy_assets()
    build_index()
    build_hotels()
    build_michelin()
    build_activities()
    build_booking()
    build_questions()
    build_suggestions()
    build_flagged()
    build_repo()
    build_sources()


if __name__ == "__main__":
    main()
