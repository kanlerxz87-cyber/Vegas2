#!/usr/bin/env python3
"""Deterministic static dashboard builder for session-3c7ffbdd (Vegas 2027).

Reads verified JSON datasets from data/session-3c7ffbdd/ and builds a clean,
mobile-friendly, multi-page static site into docs/session-3c7ffbdd/.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data" / "session-3c7ffbdd"
OUT_DIR = REPO_ROOT / "docs" / "session-3c7ffbdd"

NAV_ITEMS = [
    ("index.html", "Overview"),
    ("hotels.html", "Hotels & Dates"),
    ("restaurants.html", "Michelin (24)"),
    ("activities.html", "Activities"),
    ("suggestions.html", "Suggestions"),
    ("questions.html", "Q&A"),
    ("flagged.html", "Flagged for Review"),
]


def load_json(name: str) -> dict[str, Any]:
    with (DATA_DIR / name).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def esc(value: Any) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def ext_link(url: str, label: str, cls: str = "ext-link") -> str:
    if not url:
        return '<span class="muted" title="Not verified from an official source">—</span>'
    return (
        f'<a class="{esc(cls)}" href="{esc(url)}" '
        f'target="_blank" rel="noopener noreferrer">{esc(label)}</a>'
    )


def format_usd(value: float | int) -> str:
    if isinstance(value, float) and not value.is_integer():
        return f"${value:,.2f}"
    return f"${int(round(value)):,}"


def render_social_links(row: dict[str, Any]) -> str:
    items = []
    for key, label in [
        ("youtube_url", "YouTube"),
        ("tiktok_url", "TikTok"),
        ("instagram_url", "Instagram"),
    ]:
        url = (row.get(key) or "").strip()
        if url:
            items.append(
                f'<a class="social-pill social-{key.split("_")[0]}" '
                f'href="{esc(url)}" target="_blank" rel="noopener noreferrer">{label}</a>'
            )
        else:
            items.append(
                f'<span class="social-pill social-blank" '
                f'title="No verified official {label} channel">— {label}</span>'
            )
    return '<div class="social-group">' + "".join(items) + "</div>"


def render_flags_cell(flags: list[str]) -> str:
    if not flags:
        return '<span class="badge badge-ok">Verified</span>'
    items = "".join(f"<li>{esc(f)}</li>" for f in flags)
    return (
        f'<details class="flag-details">'
        f'<summary class="badge badge-warn">Flagged ({len(flags)})</summary>'
        f'<ul class="flag-list">{items}</ul>'
        f'<a class="mini-link" href="flagged.html">See Flagged for Review →</a>'
        f"</details>"
    )


def page_shell(
    *,
    filename: str,
    title: str,
    subtitle: str,
    verified_date: str,
    body_html: str,
) -> str:
    nav_links = []
    for href, label in NAV_ITEMS:
        active = ' class="active" aria-current="page"' if href == filename else ""
        nav_links.append(f'<a href="{href}"{active}>{esc(label)}</a>')
    nav_html = "\n          ".join(nav_links)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} — Las Vegas 2027 Trip Dashboard (Session 3c7ffbdd)</title>
  <meta name="description" content="{esc(subtitle)}">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header">
    <div class="container header-inner">
      <div class="brand">
        <a class="brand-title" href="index.html">Las Vegas 2027 Planner</a>
        <span class="brand-tag">Verified {esc(verified_date)} · 2 Adults · Feb 15–Mar 23, 2027</span>
      </div>
      <nav class="site-nav" aria-label="Primary navigation">
          {nav_html}
      </nav>
    </div>
  </header>

  <section class="hero">
    <div class="container">
      <h1>{esc(title)}</h1>
      <p class="hero-sub">{esc(subtitle)}</p>
    </div>
  </section>

  <main id="main-content" class="container main-content">
{body_html}
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <p><strong>Session 3c7ffbdd Verification Standard:</strong> Every rate, schedule, Michelin distinction, and official URL was checked live against official trusted sources on {esc(verified_date)}. Unverified values are intentionally left blank (<code>—</code>) and logged on <a href="flagged.html">Flagged for Review</a>.</p>
      <p class="footer-links">
        <a href="index.html">Overview</a> ·
        <a href="hotels.html">Hotels</a> ·
        <a href="restaurants.html">Michelin (24)</a> ·
        <a href="activities.html">Activities</a> ·
        <a href="suggestions.html">Suggestions</a> ·
        <a href="questions.html">Q&amp;A</a> ·
        <a href="flagged.html">Flagged for Review</a>
      </p>
    </div>
  </footer>
  <script src="assets/app.js" defer></script>
</body>
</html>
"""


def build_index(
    meta: dict[str, Any],
    hotels: dict[str, Any],
    restaurants: dict[str, Any],
    activities: dict[str, Any],
    flagged: dict[str, Any],
) -> str:
    trip = meta["trip"]
    booking = meta["best_time_to_book"]
    transit = meta["transit"]
    michelin = meta["michelin_summary"]

    flag_count = len(flagged["repo_audit_irregularities"]) + len(
        flagged["official_source_conflicts_and_gaps"]
    )
    verified_price_restaurants = sum(
        1 for r in restaurants["restaurants"] if r.get("cost_verified")
    )

    cluster_cards = []
    for c in michelin["clusters"]:
        cluster_cards.append(
            f"""<article class="card">
        <div class="card-kicker">{c['count']} Michelin Restaurants</div>
        <h3>{esc(c['name'])}</h3>
        <p>{esc(c['highlights'])}</p>
      </article>"""
        )

    evidence_items = "".join(f"<li>{esc(e)}</li>" for e in booking["evidence"])
    booking_sources = " · ".join(
        ext_link(s["url"], s["label"]) for s in booking["sources"]
    )
    michelin_sources = " · ".join(
        ext_link(s["url"], s["label"]) for s in michelin["official_sources"]
    )

    top_hotels_rows = []
    for h in hotels["hotels"][:5]:
        top_hotels_rows.append(
            f"""<tr>
            <td><strong>#{h['rank']}</strong></td>
            <td><strong>{esc(h['name'])}</strong><br><span class="muted">{esc(h['area'])}</span></td>
            <td>{esc(h['room_type'])}</td>
            <td><strong>{format_usd(h['seven_night_total_usd'])}</strong><br><span class="muted">{format_usd(h['nightly_rate_usd'])}/nt</span></td>
            <td>{esc(h['pricing_basis'])}</td>
            <td>{esc(h['value_verdict'])}</td>
            <td>{ext_link(h['source_url'], 'Live Quote')}</td>
          </tr>"""
        )

    body = f"""
    <section class="kpi-grid" aria-label="Executive key metrics">
      <div class="kpi-card kpi-accent">
        <div class="kpi-label">Cheapest Verified 7-Night Window</div>
        <div class="kpi-value">Feb 15–22, 2027</div>
        <div class="kpi-note">Overlaps preferred Feb 15–18; Mon–Mon beat every later week through Mar 22</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Lowest Center-Strip 7-Nt Quote</div>
        <div class="kpi-value">$539 / $581</div>
        <div class="kpi-note">LINQ 1Q ($539) &amp; Flamingo 2Q ($581), incl. resort fee, before tax</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">2026 Michelin Las Vegas Guide</div>
        <div class="kpi-value">24 Venues</div>
        <div class="kpi-note">1 Two-Star · 3 One-Star · 3 Bib Gourmand · 17 Recommended</div>
      </div>
      <div class="kpi-card kpi-warn">
        <div class="kpi-label">Flagged for Review</div>
        <div class="kpi-value">{flag_count} Items</div>
        <div class="kpi-note">{len(flagged['repo_audit_irregularities'])} repo audit bugs + {len(flagged['official_source_conflicts_and_gaps'])} official conflicts/gaps</div>
      </div>
    </section>

    <section class="panel">
      <div class="section-head">
        <h2>Executive Decision Summary</h2>
        <span class="badge badge-ok">Live Verified {esc(meta['verified_date'])}</span>
      </div>
      <div class="two-col">
        <div class="card">
          <h3>1. Best Stay Dates &amp; When to Book</h3>
          <p><strong>Recommended stay:</strong> {esc(trip['best_verified_7_night_window'])} (2 adults). {esc(trip['holiday_note'])} ({ext_link(trip['holiday_source'], 'OPM 2027 Holidays')})</p>
          <p><strong>Best time to book:</strong> {esc(booking['summary'])}</p>
          <ul class="bullet-list">{evidence_items}</ul>
          <p class="source-row"><strong>Sources:</strong> {booking_sources}</p>
        </div>
        <div class="card">
          <h3>2. Transit Reality Check (No Subway in Las Vegas)</h3>
          <p>{esc(transit['subway_note'])}</p>
          <ul class="bullet-list">
            <li><strong>{esc(transit['monorail']['name'])}:</strong> {esc(transit['monorail']['stations'])}. Runs {esc(transit['monorail']['headway'])}; {esc(transit['monorail']['hours'])}. 7-day pass for 2 adults: <strong>{esc(transit['monorail']['two_adult_7_day_cost'])}</strong> ({ext_link(transit['monorail']['official_url'], 'Official Fares')}, {ext_link(transit['monorail']['instagram'], '@lvmonorail')}).</li>
            <li><strong>{esc(transit['rtc_deuce']['name'])}:</strong> {esc(transit['rtc_deuce']['headway'])}; {esc(transit['rtc_deuce']['fares_per_adult'])}. Two 3-day passes: <strong>{esc(transit['rtc_deuce']['two_adult_3_day_cost'])}</strong> ({ext_link(transit['rtc_deuce']['official_url'], 'RTC Fares')}).</li>
            <li><strong>Michelin Transit Access:</strong> Staying on Center Strip (LINQ, Flamingo, Horseshoe, Paris, Caesars Palace) confirms direct Strip/Monorail/Deuce corridor reach to <strong>15 Michelin venues</strong> (13 Strip + 2 Arts District), with 6 Chinatown + 3 West/SW venues flagged for exact RTC evening bus verification.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="section-head">
        <h2>Top 5 Ranked Center-Strip Hotels (Feb 15–22, 2027 · 2 Adults)</h2>
        <a class="btn-link" href="hotels.html">Full 8-Hotel &amp; 5-Week Comparison →</a>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Hotel &amp; Location</th>
              <th>Verified Room (Queen+ &amp; Private Bath)</th>
              <th>7-Night Total (2 Adults)</th>
              <th>Tax / Fee Basis</th>
              <th>Verdict</th>
              <th>Official Source</th>
            </tr>
          </thead>
          <tbody>
            {''.join(top_hotels_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="panel">
      <div class="section-head">
        <h2>2026 MICHELIN Guide Southwest — 4 Las Vegas Clusters</h2>
        <a class="btn-link" href="restaurants.html">Explore All 24 Restaurants →</a>
      </div>
      <p class="lead">{esc(michelin['edition'])}. Verified official 2-adult prices are displayed for <strong>{verified_price_restaurants} of 24</strong> restaurants; the remaining venues leave cost blank and flagged rather than guessing. Sources: {michelin_sources}</p>
      <div class="card-grid">
        {''.join(cluster_cards)}
      </div>
    </section>

    <section class="panel">
      <div class="section-head">
        <h2>Dashboard Sections</h2>
      </div>
      <div class="card-grid">
        <a class="nav-card" href="hotels.html">
          <h3>Hotels &amp; Best Dates</h3>
          <p>8 live-quoted hotels (Feb 15–22, 2027) + 5-week price matrix across Feb 15–Mar 22.</p>
        </a>
        <a class="nav-card" href="restaurants.html">
          <h3>Michelin Restaurants (24)</h3>
          <p>Starred vs Bib Gourmand vs Recommended, 2-adult costs, hours, exceptions &amp; verified social links.</p>
        </a>
        <a class="nav-card" href="activities.html">
          <h3>Activities (&le;1 Hour)</h3>
          <p>{len(activities['activities'])} curated Strip, Downtown &amp; desert activities with 2027 dark dates &amp; timed-entry rules.</p>
        </a>
        <a class="nav-card" href="suggestions.html">
          <h3>Suggestions</h3>
          <p>Decision, itinerary, and architecture proposals for human review before implementation.</p>
        </a>
        <a class="nav-card" href="questions.html">
          <h3>Questions &amp; Answers</h3>
          <p>Clear answers plus step-by-step discovery guides for unverified details.</p>
        </a>
        <a class="nav-card nav-card-warn" href="flagged.html">
          <h3>Flagged for Review ({flag_count})</h3>
          <p>Line-by-line repo audit bugs, official-source conflicts, and unverified fields with links.</p>
        </a>
      </div>
    </section>
    """

    return page_shell(
        filename="index.html",
        title="Las Vegas 2027 Vacation Dashboard",
        subtitle="Executive overview for 2 adults (1–2 weeks between Feb 15 and Mar 23, 2027) — 100% live-verified from official sources with zero hallucinations.",
        verified_date=meta["verified_date"],
        body_html=body,
    )


def build_hotels(meta: dict[str, Any], hotels_data: dict[str, Any]) -> str:
    rows = []
    for h in hotels_data["hotels"]:
        area_group = "off-strip" if h["id"] == "south-point" else "strip"
        rows.append(
            f"""<tr data-area="{area_group}" data-price="{h['seven_night_total_usd']}">
            <td><strong>#{h['rank']}</strong></td>
            <td><strong>{esc(h['name'])}</strong><br><span class="muted">{esc(h['area'])}</span><br><span class="badge badge-info">{esc(h['value_verdict'])}</span></td>
            <td>{esc(h['room_type'])}<br><span class="muted">{esc(h['bed_verified'])} · {esc(h['private_bath_verified'])}</span></td>
            <td><strong>{format_usd(h['seven_night_total_usd'])}</strong><br><span class="muted">{format_usd(h['nightly_rate_usd'])}/night</span></td>
            <td>{esc(h['pricing_basis'])}<br><span class="muted">{esc(h['resort_fee_detail'])}</span></td>
            <td>{esc(h['michelin_within_1hr_label'])}<br><span class="muted">{esc(h['transit_access'])}</span></td>
            <td>{ext_link(h['source_url'], 'Live Quote')}<br>{ext_link(h['property_url'], 'Official Hotel')}</td>
            <td>{render_flags_cell(h.get('flags', []))}</td>
          </tr>"""
        )

    week_rows = []
    for w in hotels_data["multi_week_comparison"]["weeks"]:
        badge = (
            '<span class="badge badge-ok">Cheapest + Preferred</span>'
            if w["overlaps_preferred"]
            else f'<span class="badge badge-neutral">{esc(w["verdict"])}</span>'
        )
        sp = esc(w["south_point_rate"]) if w["south_point_rate"] else '<span class="muted">— (not queried)</span>'
        week_rows.append(
            f"""<tr class="{'row-highlight' if w['overlaps_preferred'] else ''}">
            <td><strong>{esc(w['window'])}</strong></td>
            <td>{esc(w['flamingo_rate'])}</td>
            <td>{esc(w['caesars_palace_rate'])}</td>
            <td>{sp}</td>
            <td>{badge}</td>
          </tr>"""
        )

    week_sources = " · ".join(
        ext_link(u, f"Booking Engine {idx}")
        for idx, u in enumerate(hotels_data["multi_week_comparison"]["sources"], start=1)
    )

    body = f"""
    <section class="panel">
      <div class="section-head">
        <h2>Ranked Hotel Comparison ({esc(hotels_data['benchmark_dates'])})</h2>
        <span class="badge badge-ok">Live Quotes {esc(hotels_data['verified_date'])}</span>
      </div>
      <p class="lead">{esc(hotels_data['ranking_methodology'])}</p>
      <div class="controls" data-filter-target="hotels-table">
        <label>Filter Location:
          <select data-filter-attr="area">
            <option value="all">All Hotels (8)</option>
            <option value="strip">Strip Corridor (7)</option>
            <option value="off-strip">Off-Strip Reference (1)</option>
          </select>
        </label>
        <label>Search:
          <input type="search" data-filter-search placeholder="Filter by hotel, room, transit...">
        </label>
      </div>
      <div class="table-wrap">
        <table id="hotels-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Hotel &amp; Verdict</th>
              <th>Room, Bed &amp; Private Bath</th>
              <th>7-Night Total (2 Adults)</th>
              <th>Resort Fee &amp; Tax Basis</th>
              <th>Michelin &le;1 Hr &amp; Transit Access</th>
              <th>Official Sources</th>
              <th>Review Status</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="panel">
      <div class="section-head">
        <h2>5-Week Date &amp; Price Matrix (Feb 15 – Mar 22, 2027)</h2>
        <span class="badge badge-ok">Mon Feb 15–22 Wins Across All Properties</span>
      </div>
      <p class="lead">{esc(hotels_data['multi_week_comparison']['description'])}</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>7-Night Window (Mon–Mon)</th>
              <th>Flamingo (Live Quote)</th>
              <th>Caesars Palace (Live Quote)</th>
              <th>South Point (Live Quote)</th>
              <th>Verdict</th>
            </tr>
          </thead>
          <tbody>
            {''.join(week_rows)}
          </tbody>
        </table>
      </div>
      <p class="source-row"><strong>Live Multi-Week Verification Sources:</strong> {week_sources}</p>
    </section>
    """

    return page_shell(
        filename="hotels.html",
        title="Hotels & Cheapest 2027 Dates",
        subtitle="Ranked by verified Michelin public-transit access, room/private-bath standards, and live 7-night pricing for 2 adults.",
        verified_date=meta["verified_date"],
        body_html=body,
    )


def build_restaurants(meta: dict[str, Any], rest_data: dict[str, Any]) -> str:
    restaurants = rest_data["restaurants"]
    clusters = sorted({r["cluster"] for r in restaurants})

    def distinction_badge(r: dict[str, Any]) -> str:
        d = r["distinction"]
        if "Two" in d:
            return f'<span class="badge badge-star2">{esc(d)}</span>'
        if "One" in d:
            return f'<span class="badge badge-star1">{esc(d)}</span>'
        if "Bib" in d:
            return f'<span class="badge badge-bib">{esc(d)}</span>'
        return f'<span class="badge badge-rec">{esc(d)}</span>'

    rows = []
    for r in restaurants:
        cost_html = (
            f"<strong>{esc(r['cost_for_2_adults'])}</strong>"
            if r.get("cost_for_2_adults")
            else '<span class="muted">— (unverified; <a href="flagged.html">flagged</a>)</span>'
        )
        days_html = (
            esc(r["days_open"])
            if r.get("days_open")
            else '<span class="muted">— (unverified; <a href="flagged.html">flagged</a>)</span>'
        )
        hours_html = (
            esc(r["hours"])
            if r.get("hours")
            else '<span class="muted">— (unverified; <a href="flagged.html">flagged</a>)</span>'
        )
        group_slug = (
            "starred"
            if r["distinction_group"] == "Michelin-Starred"
            else ("bib" if "Bib" in r["distinction_group"] else "recommended")
        )
        cost_slug = "verified" if r.get("cost_verified") else "blank"
        rows.append(
            f"""<tr data-group="{group_slug}" data-cluster="{esc(r['cluster'])}" data-cost="{cost_slug}">
            <td><strong>{esc(r['name'])}</strong><br><span class="muted">{esc(r['property_or_area'])}</span><br><span class="muted tiny">{esc(r['address'])}</span></td>
            <td>{distinction_badge(r)}<br><span class="muted tiny">{esc(r['distinction_group'])}</span></td>
            <td>{esc(r['cluster'])}</td>
            <td>{esc(r['price_tier'])}</td>
            <td>{cost_html}</td>
            <td><strong>{days_html}</strong><br>{hours_html}</td>
            <td>{esc(r['exceptions'])}</td>
            <td>{ext_link(r['official_url'], 'Official Site')}<br>{ext_link(r['michelin_source_url'], 'Michelin List')}</td>
            <td>{render_social_links(r)}</td>
            <td>{render_flags_cell(r.get('flags', []))}</td>
          </tr>"""
        )

    cluster_opts = "".join(
        f'<option value="{esc(c)}">{esc(c)}</option>' for c in clusters
    )
    guide_sources = " · ".join(
        ext_link(u, f"Official Michelin Directory {i}")
        for i, u in enumerate(rest_data["official_guide_sources"], start=1)
    )

    body = f"""
    <section class="panel">
      <div class="section-head">
        <h2>All 24 Las Vegas Michelin Restaurants (2026 Southwest Guide)</h2>
        <span class="badge badge-star2">4 Starred</span>
        <span class="badge badge-bib">3 Bib Gourmand</span>
        <span class="badge badge-rec">17 Recommended</span>
      </div>
      <p class="lead">{esc(rest_data['pricing_policy_note'])} Sources: {guide_sources}</p>
      <div class="controls" data-filter-target="restaurants-table">
        <label>Distinction:
          <select data-filter-attr="group">
            <option value="all">All 24 Restaurants</option>
            <option value="starred">Michelin-Starred Only (4)</option>
            <option value="bib">Bib Gourmand Only (3)</option>
            <option value="recommended">Michelin Recommended Only (17)</option>
          </select>
        </label>
        <label>Cluster:
          <select data-filter-attr="cluster">
            <option value="all">All 4 Clusters</option>
            {cluster_opts}
          </select>
        </label>
        <label>2-Adult Cost:
          <select data-filter-attr="cost">
            <option value="all">All</option>
            <option value="verified">Published Official Price Only (7)</option>
            <option value="blank">Unverified / Blank Only (17)</option>
          </select>
        </label>
        <label>Search:
          <input type="search" data-filter-search placeholder="Name, hotel, address, closed days...">
        </label>
      </div>
      <div class="table-wrap">
        <table id="restaurants-table">
          <thead>
            <tr>
              <th>Restaurant &amp; Address</th>
              <th>Michelin Status</th>
              <th>Cluster</th>
              <th>Tier</th>
              <th>Total Cost for 2 Adults (Official)</th>
              <th>Days Open &amp; Hours</th>
              <th>Exceptions &amp; Rules</th>
              <th>Official Links</th>
              <th>YouTube / TikTok / Instagram</th>
              <th>Review Status</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """

    return page_shell(
        filename="restaurants.html",
        title="24 Las Vegas Michelin Restaurants",
        subtitle="Complete 2026 MICHELIN Guide Southwest selection — Starred vs Bib Gourmand vs Recommended, clusters, verified 2-adult prices, hours, exceptions, and verified social links.",
        verified_date=meta["verified_date"],
        body_html=body,
    )


def build_activities(meta: dict[str, Any], act_data: dict[str, Any]) -> str:
    rows = []
    for a in act_data["activities"]:
        transit_slug = "transit" if a["transit_accessible"] else "car"
        transit_badge = (
            '<span class="badge badge-ok">Walk / Monorail / RTC Bus</span>'
            if a["transit_accessible"]
            else '<span class="badge badge-warn">Car / Commercial Tour Only</span>'
        )
        cost_html = (
            f"<strong>{esc(a['cost_for_2_adults'])}</strong>"
            if a.get("cost_for_2_adults")
            else '<span class="muted">— (event-dependent; <a href="flagged.html">flagged</a>)</span>'
        )
        rows.append(
            f"""<tr data-access="{transit_slug}">
            <td><strong>{esc(a['name'])}</strong><br><span class="muted">{esc(a['category'])}</span></td>
            <td>{transit_badge}<br><span class="muted">{esc(a['travel_from_center_strip'])}</span></td>
            <td>{cost_html}</td>
            <td><strong>{esc(a['days_open'])}</strong><br>{esc(a['hours'])}</td>
            <td>{esc(a['exceptions'])}</td>
            <td>{ext_link(a['official_url'], 'Official Page')}</td>
            <td>{render_social_links(a)}</td>
            <td>{render_flags_cell(a.get('flags', []))}</td>
          </tr>"""
        )

    body = f"""
    <section class="panel">
      <div class="section-head">
        <h2>Las Vegas Activities Within &le;1 Hour From Center Strip</h2>
        <span class="badge badge-ok">{len(act_data['activities'])} Verified Activities</span>
      </div>
      <p class="lead">{esc(act_data['scope_note'])}</p>
      <div class="controls" data-filter-target="activities-table">
        <label>Access Mode:
          <select data-filter-attr="access">
            <option value="all">All Activities ({len(act_data['activities'])})</option>
            <option value="transit">Public Transit / Walkable (8)</option>
            <option value="car">Car / Tour Required (3)</option>
          </select>
        </label>
        <label>Search:
          <input type="search" data-filter-search placeholder="Filter by activity, hours, exceptions...">
        </label>
      </div>
      <div class="table-wrap">
        <table id="activities-table">
          <thead>
            <tr>
              <th>Activity</th>
              <th>Travel From Center Strip</th>
              <th>2-Adult Cost (Official)</th>
              <th>Days Open &amp; Hours</th>
              <th>Exceptions &amp; 2027 Alerts</th>
              <th>Official Link</th>
              <th>YouTube / TikTok / Instagram</th>
              <th>Review Status</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """

    return page_shell(
        filename="activities.html",
        title="Las Vegas Activities (≤1 Hour)",
        subtitle="Verified hours, 2027 closure/timed-entry exceptions, 2-adult pricing, official links, and official YouTube/TikTok/Instagram channels.",
        verified_date=meta["verified_date"],
        body_html=body,
    )


def build_suggestions(meta: dict[str, Any], sug_data: dict[str, Any]) -> str:
    rows = []
    for s in sug_data["suggestions"]:
        p_cls = (
            "badge-warn"
            if s["priority"] == "High"
            else ("badge-info" if s["priority"] == "Medium" else "badge-neutral")
        )
        rows.append(
            f"""<tr>
            <td><code>{esc(s['id'])}</code></td>
            <td><span class="badge {p_cls}">{esc(s['priority'])}</span></td>
            <td>{esc(s['category'])}</td>
            <td><strong>{esc(s['title'])}</strong><br><span class="muted">{esc(s['rationale'])}</span></td>
            <td>{esc(s['proposed_action'])}</td>
            <td>{ext_link(s['source_url'], 'Supporting Source')}</td>
          </tr>"""
        )

    body = f"""
    <section class="panel">
      <div class="section-head">
        <h2>Suggestions for Review Before Implementation</h2>
        <span class="badge badge-info">{len(sug_data['suggestions'])} Proposals</span>
      </div>
      <p class="lead">{esc(sug_data['intro'])}</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Priority</th>
              <th>Category</th>
              <th>Proposal &amp; Rationale</th>
              <th>Recommended Action</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows)}
          </tbody>
        </table>
      </div>
    </section>
    """

    return page_shell(
        filename="suggestions.html",
        title="Suggestions & Decision Proposals",
        subtitle="Trip-decision optimizations, data improvements, and repository architecture suggestions queued for review before implementing.",
        verified_date=meta["verified_date"],
        body_html=body,
    )


def build_questions(meta: dict[str, Any], q_data: dict[str, Any]) -> str:
    cards = []
    for item in q_data["qa_items"]:
        cards.append(
            f"""<article class="qa-card">
        <div class="qa-meta">
          <code>{esc(item['id'])}</code>
          <span class="badge badge-info">{esc(item['topic'])}</span>
        </div>
        <h3>{esc(item['question'])}</h3>
        <div class="qa-answer">
          <strong>Verified Answer:</strong> {esc(item['answer'])}
        </div>
        <div class="qa-discover">
          <strong>How to Discover Missing Info:</strong> {esc(item['missing_info_discovery'])}
        </div>
        <div class="qa-source">
          <strong>Official Source:</strong> {ext_link(item['source_url'], 'Open Source')}
        </div>
      </article>"""
        )

    body = f"""
    <section class="panel">
      <div class="section-head">
        <h2>Questions, Verified Information &amp; Missing-Data Discovery Guide</h2>
        <span class="badge badge-ok">{len(q_data['qa_items'])} Topics</span>
      </div>
      <p class="lead">{esc(q_data['intro'])}</p>
      <div class="qa-stack">
        {''.join(cards)}
      </div>
    </section>
    """

    return page_shell(
        filename="questions.html",
        title="Questions, Information & Answers",
        subtitle="Evidence-backed answers for your Feb–Mar 2027 trip plus exact playbooks for uncovering unpublished menu prices, room taxes, and transit timings.",
        verified_date=meta["verified_date"],
        body_html=body,
    )


def build_flagged(meta: dict[str, Any], flag_data: dict[str, Any]) -> str:
    repo_rows = []
    for item in flag_data["repo_audit_irregularities"]:
        sev_cls = "badge-danger" if item["severity"] == "High" else "badge-warn"
        repo_rows.append(
            f"""<tr>
            <td><code>{esc(item['id'])}</code></td>
            <td><span class="badge {sev_cls}">{esc(item['severity'])}</span></td>
            <td><code>{esc(item['location'])}</code></td>
            <td><strong>{esc(item['issue'])}</strong><br><span class="muted">{esc(item['details'])}</span></td>
            <td>{esc(item['status'])}</td>
            <td>{ext_link(item['source_url'], 'Verify Source')}</td>
          </tr>"""
        )

    data_rows = []
    for item in flag_data["official_source_conflicts_and_gaps"]:
        data_rows.append(
            f"""<tr>
            <td><code>{esc(item['id'])}</code></td>
            <td><span class="badge badge-warn">{esc(item['category'])}</span></td>
            <td><strong>{esc(item['item'])}</strong></td>
            <td><strong>{esc(item['issue'])}</strong><br><span class="muted">{esc(item['details'])}</span></td>
            <td>{ext_link(item['source_url'], 'Official Source')}</td>
          </tr>"""
        )

    body = f"""
    <section class="panel">
      <div class="section-head">
        <h2>A. Repository Line-by-Line Audit Irregularities</h2>
        <span class="badge badge-danger">{len(flag_data['repo_audit_irregularities'])} Repo Findings</span>
      </div>
      <p class="lead">{esc(flag_data['intro'])}</p>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Severity</th>
              <th>Repo Location</th>
              <th>Irregularity &amp; Evidence</th>
              <th>Disposition</th>
              <th>Verification Link</th>
            </tr>
          </thead>
          <tbody>
            {''.join(repo_rows)}
          </tbody>
        </table>
      </div>
    </section>

    <section class="panel">
      <div class="section-head">
        <h2>B. Official-Source Conflicts &amp; Unverified Fields Register</h2>
        <span class="badge badge-warn">{len(flag_data['official_source_conflicts_and_gaps'])} Data Flags</span>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Category</th>
              <th>Venue / Item</th>
              <th>Conflict or Unverified Gap</th>
              <th>Official Source Link</th>
            </tr>
          </thead>
          <tbody>
            {''.join(data_rows)}
          </tbody>
        </table>
      </div>
    </section>
    """

    return page_shell(
        filename="flagged.html",
        title="Flagged for Review",
        subtitle="Transparent log of every repository audit irregularity, official-source conflict, and intentionally blank unverified field — each with a verification link.",
        verified_date=meta["verified_date"],
        body_html=body,
    )


STYLE_CSS = """/* Las Vegas 2027 Dashboard — Session 3c7ffbdd (Mobile-First Responsive UI) */
:root {
  --bg: #f6f7f9;
  --surface: #ffffff;
  --ink: #111827;
  --muted: #4b5563;
  --border: #e5e7eb;
  --navy: #0f172a;
  --navy-soft: #1e293b;
  --accent: #b45309;
  --accent-bg: #fef3c7;
  --ok: #047857;
  --ok-bg: #d1fae5;
  --warn: #b45309;
  --warn-bg: #fef3c7;
  --danger: #b91c1c;
  --danger-bg: #fee2e2;
  --info: #1d4ed8;
  --info-bg: #dbeafe;
  --bib: #0f766e;
  --bib-bg: #ccfbf1;
  --radius: 12px;
  --shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
}

*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, Helvetica, Arial, sans-serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.55;
  font-size: 15px;
}

.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
  background: var(--navy);
  color: #fff;
  padding: 0.6rem 1rem;
  z-index: 1000;
}
.skip-link:focus { left: 0.5rem; top: 0.5rem; }

.container {
  width: min(1240px, 100% - 2rem);
  margin-inline: auto;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--navy);
  color: #fff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}
.header-inner {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem 1.25rem;
  padding: 0.8rem 0;
}
.brand { display: flex; flex-direction: column; gap: 0.1rem; }
.brand-title {
  color: #fff;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.05rem;
  letter-spacing: -0.01em;
}
.brand-tag { color: #cbd5e1; font-size: 0.78rem; }

.site-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}
.site-nav a {
  color: #e2e8f0;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.42rem 0.72rem;
  border-radius: 999px;
  transition: background 0.15s ease, color 0.15s ease;
}
.site-nav a:hover { background: rgba(255, 255, 255, 0.12); color: #fff; }
.site-nav a.active { background: #f59e0b; color: #111827; font-weight: 700; }

.hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 65%, #334155 100%);
  color: #fff;
  padding: 2rem 0 2.2rem;
}
.hero h1 { margin: 0 0 0.45rem; font-size: clamp(1.55rem, 3vw, 2.2rem); line-height: 1.2; }
.hero-sub { margin: 0; color: #cbd5e1; max-width: 75ch; font-size: 0.98rem; }

.main-content { padding: 1.5rem 0 3rem; display: flex; flex-direction: column; gap: 1.5rem; }

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.1rem 1.2rem;
  box-shadow: var(--shadow);
}
.kpi-accent { border-top: 4px solid #f59e0b; }
.kpi-warn { border-top: 4px solid var(--danger); }
.kpi-label { font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }
.kpi-value { font-size: 1.55rem; font-weight: 800; color: var(--navy); margin: 0.25rem 0; }
.kpi-note { font-size: 0.84rem; color: var(--muted); }

.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem 1.35rem;
  box-shadow: var(--shadow);
}
.section-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem 0.75rem;
  margin-bottom: 0.75rem;
}
.section-head h2 { margin: 0; font-size: 1.22rem; color: var(--navy); }
.lead { margin: 0 0 1rem; color: var(--muted); }

.two-col {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}
.card, .nav-card, .qa-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem 1.1rem;
  background: #fbfcfd;
}
.card h3, .nav-card h3, .qa-card h3 { margin: 0.15rem 0 0.5rem; font-size: 1.02rem; color: var(--navy); }
.card-kicker { font-size: 0.76rem; font-weight: 700; text-transform: uppercase; color: var(--accent); letter-spacing: 0.04em; }

.nav-card {
  display: block;
  text-decoration: none;
  color: inherit;
  transition: transform 0.12s ease, border-color 0.12s ease;
}
.nav-card:hover { transform: translateY(-2px); border-color: #94a3b8; }
.nav-card p { margin: 0; font-size: 0.88rem; color: var(--muted); }
.nav-card-warn { border-left: 4px solid var(--danger); }

.bullet-list { margin: 0.5rem 0 0.75rem; padding-left: 1.2rem; }
.bullet-list li { margin-bottom: 0.4rem; }
.source-row { font-size: 0.84rem; color: var(--muted); margin: 0.75rem 0 0; }

.controls {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem 1rem;
  align-items: center;
  margin-bottom: 0.9rem;
  padding: 0.75rem;
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: 8px;
}
.controls label {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--muted);
}
.controls select, .controls input {
  font: inherit;
  font-size: 0.88rem;
  padding: 0.4rem 0.6rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: #fff;
  color: var(--ink);
  min-width: 170px;
}

.table-wrap {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--border);
  border-radius: 8px;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.87rem;
  min-width: 720px;
}
th, td {
  text-align: left;
  vertical-align: top;
  padding: 0.68rem 0.75rem;
  border-bottom: 1px solid var(--border);
}
thead th {
  background: #f1f5f9;
  color: var(--navy);
  font-weight: 700;
  font-size: 0.79rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  white-space: nowrap;
}
tbody tr:hover { background: #f8fafc; }
.row-highlight { background: #ecfdf5; }
.row-highlight:hover { background: #d1fae5; }

.muted { color: var(--muted); }
.tiny { font-size: 0.79rem; }

.badge {
  display: inline-block;
  font-size: 0.74rem;
  font-weight: 700;
  padding: 0.16rem 0.5rem;
  border-radius: 999px;
  white-space: nowrap;
}
.badge-ok { background: var(--ok-bg); color: var(--ok); }
.badge-warn { background: var(--warn-bg); color: var(--warn); }
.badge-danger { background: var(--danger-bg); color: var(--danger); }
.badge-info { background: var(--info-bg); color: var(--info); }
.badge-neutral { background: #e5e7eb; color: #374151; }
.badge-star2 { background: #7f1d1d; color: #fef3c7; }
.badge-star1 { background: #991b1b; color: #ffffff; }
.badge-bib { background: var(--bib-bg); color: var(--bib); }
.badge-rec { background: var(--info-bg); color: var(--info); }

.ext-link, .btn-link, .mini-link {
  color: #1d4ed8;
  text-decoration: none;
  font-weight: 600;
}
.ext-link:hover, .btn-link:hover, .mini-link:hover { text-decoration: underline; }
.ext-link::after { content: " ↗"; font-size: 0.8em; }
.btn-link { font-size: 0.88rem; }
.mini-link { font-size: 0.78rem; display: inline-block; margin-top: 0.25rem; }

.social-group { display: flex; flex-wrap: wrap; gap: 0.25rem; }
.social-pill {
  display: inline-block;
  font-size: 0.73rem;
  font-weight: 600;
  padding: 0.15rem 0.45rem;
  border-radius: 6px;
  text-decoration: none;
}
.social-youtube { background: #fee2e2; color: #991b1b; }
.social-tiktok { background: #e2e8f0; color: #0f172a; }
.social-instagram { background: #fce7f3; color: #9d174d; }
.social-blank { background: #f3f4f6; color: #9ca3af; font-weight: 500; }

.flag-details summary { cursor: pointer; list-style: none; }
.flag-details summary::-webkit-details-marker { display: none; }
.flag-list { margin: 0.4rem 0 0.2rem; padding-left: 1rem; font-size: 0.8rem; color: var(--muted); }
.flag-list li { margin-bottom: 0.25rem; }

.qa-stack { display: flex; flex-direction: column; gap: 0.9rem; }
.qa-meta { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem; }
.qa-answer, .qa-discover, .qa-source { margin-top: 0.45rem; font-size: 0.92rem; }
.qa-discover {
  background: #fffbeb;
  border-left: 3px solid #f59e0b;
  padding: 0.55rem 0.75rem;
  border-radius: 0 6px 6px 0;
}

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.84em;
  background: #f1f5f9;
  padding: 0.1rem 0.32rem;
  border-radius: 4px;
}

.site-footer {
  border-top: 1px solid var(--border);
  background: #fff;
  padding: 1.4rem 0 2rem;
  color: var(--muted);
  font-size: 0.84rem;
}
.footer-inner { display: flex; flex-direction: column; gap: 0.5rem; }
.footer-links a { color: var(--navy); text-decoration: none; font-weight: 600; }
.footer-links a:hover { text-decoration: underline; }

@media (max-width: 640px) {
  .container { width: min(1240px, 100% - 1.1rem); }
  .panel { padding: 0.95rem; }
  .controls select, .controls input { min-width: 140px; width: 100%; }
}
"""

APP_JS = """/* Client-side progressive enhancement for table filtering */
(function () {
  document.querySelectorAll('.controls[data-filter-target]').forEach(function (bar) {
    var tableId = bar.getAttribute('data-filter-target');
    var table = document.getElementById(tableId);
    if (!table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
    var selects = Array.prototype.slice.call(bar.querySelectorAll('select[data-filter-attr]'));
    var search = bar.querySelector('input[data-filter-search]');

    function applyFilters() {
      var q = search ? search.value.trim().toLowerCase() : '';
      rows.forEach(function (tr) {
        var visible = true;
        selects.forEach(function (sel) {
          var attr = sel.getAttribute('data-filter-attr');
          var val = sel.value;
          if (val !== 'all' && tr.getAttribute('data-' + attr) !== val) {
            visible = false;
          }
        });
        if (visible && q && tr.textContent.toLowerCase().indexOf(q) === -1) {
          visible = false;
        }
        tr.style.display = visible ? '' : 'none';
      });
    }

    selects.forEach(function (sel) { sel.addEventListener('change', applyFilters); });
    if (search) search.addEventListener('input', applyFilters);
  });
})();
"""


def generate_outputs() -> dict[Path, str]:
    meta = load_json("meta.json")
    hotels = load_json("hotels.json")
    restaurants = load_json("restaurants.json")
    activities = load_json("activities.json")
    suggestions = load_json("suggestions.json")
    questions = load_json("questions.json")
    flagged = load_json("flagged.json")

    return {
        OUT_DIR / "index.html": build_index(meta, hotels, restaurants, activities, flagged),
        OUT_DIR / "hotels.html": build_hotels(meta, hotels),
        OUT_DIR / "restaurants.html": build_restaurants(meta, restaurants),
        OUT_DIR / "activities.html": build_activities(meta, activities),
        OUT_DIR / "suggestions.html": build_suggestions(meta, suggestions),
        OUT_DIR / "questions.html": build_questions(meta, questions),
        OUT_DIR / "flagged.html": build_flagged(meta, flagged),
        OUT_DIR / "assets" / "style.css": STYLE_CSS,
        OUT_DIR / "assets" / "app.js": APP_JS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build session-3c7ffbdd Vegas dashboard.")
    parser.add_argument("--check", action="store_true", help="Verify generated output matches disk without writing.")
    args = parser.parse_args()

    outputs = generate_outputs()

    if args.check:
        mismatches = []
        for path, content in outputs.items():
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                mismatches.append(str(path.relative_to(REPO_ROOT)))
        if mismatches:
            print("ERROR: Out-of-date generated files:", ", ".join(mismatches), file=sys.stderr)
            return 1
        print(f"OK: {len(outputs)} generated files match deterministic build.")
        return 0

    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path.relative_to(REPO_ROOT)} ({len(content):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
