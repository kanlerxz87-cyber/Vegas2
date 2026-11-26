#!/usr/bin/env python3
"""Verification gate for the Las Vegas trip-planning site.

Checks (exit code 1 on any failure):
  1. Every data file parses as JSON.
  2. Every table row (hotels, Michelin, activities) has at least one https source link.
  3. Row sources use an official-domain allowlist (secondary sources are only allowed
     in the flagged/sources pages, where they are labelled as conflict checks).
  4. Every verification cell has a valid state (v / p / u).
  5. Michelin counts match the official 2026 release (24 total: 4 starred, 3 Bib, 17 Recommended).
  6. Every internal link and asset in the generated HTML points to a file that exists.
  7. No placeholder strings ("None", "undefined", "TODO") leaked into the HTML.
Run after scripts/build_site.py.
"""
import json
import pathlib
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

OFFICIAL_DOMAINS = {
    "michelin.com", "michelinmedia.com", "agngnconpm.cloudimg.io", "opm.gov",
    "mgmresorts.com", "cosmopolitanlasvegas.mgmresorts.com", "bellagio.mgmresorts.com",
    "aria.mgmresorts.com", "mgmgrand.com", "caesars.com", "ebyjoseandres.com",
    "reservations.wynnlasvegas.com", "wynnlasvegas.com", "venetian.com", "rwlasvegas.com",
    "usbr.gov", "facebook.com", "youtube.com", "instagram.com", "blm.gov", "x.com",
    "recreation.gov", "parks.nv.gov", "neonmuseum.org", "api.github.com", "github.com",
    "stocktitan.net",  # republished MGM Resorts press release (labelled in data)
}
SECONDARY_DOMAINS = {
    "memesita.com", "lasvegasmagazine.com", "smartervegas.com", "luminafrontier.ai",
    "opentable.com", "hooverdam-tours.co", "thelasvegastravelguide.com", "usmenuguide.com",
    "lasvegasadvisor.com", "lasvegaswonders.com", "timeout.com", "vegasnearme.com",
    "theadventuristmagazine.com", "yahoo.com", "sincityvip.com", "visitlasvegas.com",
    "thedailyscout.com", "utahbusiness.com", "web.archive.org", "translate.google.com",
    "vegas.com", "smartvegasdeals.com", "wedreamoftravel.com", "vicerealtygroup.com",
    "trip.com", "vacatia.com", "wheeltheworld.com", "momondo.com", "lasvegashotels.com",
    "justsimplywander.com", "adventuresoflilnicki.com", "discovernevada.info", "leavenotracy.com",
    "comedybustours.com", "fandom.com", "lasvegas.fandom.com", "h-rez.com", "us-lasvegas.com",
    "bookstaygo.com", "eater.com", "axios.com", "azcentral.com", "phoenixnewtimes.com",
    "arizonarepublic.com", "mgmresorts.com.au", "investors.mgmresorts.com",
}

failures = []
warnings = []


def fail(msg):
    failures.append(msg)
    print("FAIL:", msg)


def warn(msg):
    warnings.append(msg)
    print("WARN:", msg)


def load(name):
    p = DATA / f"{name}.json"
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:  # noqa: BLE001
        fail(f"{p.name} does not parse: {exc}")
        return None


def domain_of(url):
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def in_domains(host, domains):
    return any(host == d or host.endswith("." + d) for d in domains)


def check_sources(where, items, allow_secondary=False):
    if not items:
        fail(f"{where}: no source links")
        return
    for it in items:
        url = it.get("url", "")
        if not url.startswith("https://"):
            fail(f"{where}: source is not https: {url!r}")
            continue
        host = domain_of(url)
        if in_domains(host, OFFICIAL_DOMAINS):
            continue
        if allow_secondary and in_domains(host, SECONDARY_DOMAINS):
            continue
        fail(f"{where}: source domain not on official allowlist: {host} ({url})")


STATES = {"v", "p", "u"}


def check_cells(where, row, fields):
    for f in fields:
        v = row.get(f)
        if isinstance(v, dict):
            if v.get("s") not in STATES:
                fail(f"{where}.{f}: invalid state {v.get('s')!r}")
            if v.get("s") in ("v", "p") and not str(v.get("t", "")).strip():
                fail(f"{where}.{f}: verified/partial cell has no text")


def main():
    data = {}
    for name in ["hotels", "michelin", "activities", "booking", "questions", "suggestions",
                 "flagged", "repo_review", "sources"]:
        data[name] = load(name)
    if any(v is None for v in data.values()):
        return

    # 2 & 3 & 4: hotels
    for i, r in enumerate(data["hotels"]["rows"]):
        where = f"hotels[{r.get('name', i)}]"
        check_sources(where, r.get("src"))
        check_cells(where, r, ["queen", "private_bath", "transit_1hr", "price_7n", "price_3n", "book_timing", "social"])
        if not isinstance(r.get("michelin_on_campus"), int):
            fail(f"{where}: michelin_on_campus must be an integer")

    # Michelin
    mrows = data["michelin"]["rows"]
    for r in mrows:
        where = f"michelin[{r.get('name')}]"
        check_sources(where, r.get("src"))
        check_cells(where, r, ["hours", "price_2adults", "reservations", "social"])
    counts = {}
    for r in mrows:
        counts[r["status_group"]] = counts.get(r["status_group"], 0) + 1
    expected = {"Starred": 4, "Bib Gourmand": 3, "Recommended": 17}
    if len(mrows) != 24:
        fail(f"michelin: expected 24 Las Vegas rows, found {len(mrows)}")
    for k, v in expected.items():
        if counts.get(k) != v:
            fail(f"michelin: expected {v} in group {k}, found {counts.get(k)}")
    stars = {r["name"]: r["status"] for r in mrows if r["status_group"] == "Starred"}
    if stars.get("Restaurant de Joël Robuchon") != "2 MICHELIN Stars":
        fail("michelin: Restaurant de Joël Robuchon must be 2 MICHELIN Stars (official release)")

    # Activities
    for r in data["activities"]["rows"]:
        where = f"activities[{r.get('name')}]"
        check_sources(where, r.get("src"))
        check_cells(where, r, ["distance", "hours", "fees", "exceptions", "reservation", "social"])

    # Booking facts & dates
    for f in data["booking"]["timing"]["verified_booking_facts"]:
        check_sources("booking.timing", [{"label": "fact", "url": f["url"]}])
    check_sources("booking.sources_dates", data["booking"]["sources_dates"])

    # Questions, flagged, repo, sources
    for q in data["questions"]["answered"]:
        check_sources(f"questions[{q['q'][:30]}]", [{"label": "src", "url": q["src"]}], allow_secondary=True)
    for f in data["flagged"]["items"]:
        check_sources(f"flagged[{f['id']}]", f["src"], allow_secondary=True)
    for i in data["repo_review"]["items"]:
        check_sources(f"repo_review[{i['item']}]", i["src"])
    for s in data["sources"]["items"]:
        if s["type"].startswith("Official") and not in_domains(domain_of(s["url"]), OFFICIAL_DOMAINS):
            fail(f"sources: official-labelled source is not on the official allowlist: {s['url']}")

    # 6 & 7: generated HTML
    html_files = sorted(ROOT.glob("*.html"))
    if not html_files:
        fail("no HTML pages found; run scripts/build_site.py first")
    pages = {p.name for p in html_files}
    expected_pages = {"index.html", "hotels.html", "michelin.html", "activities.html", "booking.html",
                      "questions.html", "suggestions.html", "flagged.html", "repo-review.html", "sources.html"}
    for missing in sorted(expected_pages - pages):
        fail(f"missing page: {missing}")

    class LinkParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = []

        def handle_starttag(self, tag, attrs):
            for k, v in attrs:
                if k in ("href", "src") and v:
                    self.links.append((tag, v))

    internal_checked = 0
    for page_path in html_files:
        text = page_path.read_text(encoding="utf-8")
        for bad in ("None", "undefined", "TODO", "NaN"):
            if re.search(r"(?<![A-Za-z])" + bad + r"(?![A-Za-z])", text):
                fail(f"{page_path.name}: placeholder text '{bad}' found")
        parser = LinkParser()
        parser.feed(text)
        for tag, link in parser.links:
            parsed = urlparse(link)
            if parsed.scheme in ("http", "https", "mailto", "tel"):
                if parsed.scheme == "http":
                    fail(f"{page_path.name}: insecure link {link}")
                continue
            if link.startswith("#"):
                continue
            target = (ROOT / parsed.path).resolve() if parsed.path else page_path
            internal_checked += 1
            if not target.exists():
                fail(f"{page_path.name}: broken internal link -> {link}")
    print(f"checked {internal_checked} internal links across {len(html_files)} pages")

    if failures:
        print(f"\n{len(failures)} failure(s). Fix before publishing.")
        sys.exit(1)
    print(f"\nOK — all checks passed ({len(warnings)} warning(s)).")


if __name__ == "__main__":
    main()
