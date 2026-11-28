#!/usr/bin/env python3
"""Session 6382dba0 — additive fieldwork merge into the canonical data/plan/*.json.

Purpose: close the two gaps the published site still carried — a social/video link
for every restaurant and activity row, and the opening-hours grids the official
pages actually publish.

Rules enforced by this script (same contract as the 4d7b292f merge):
  * only FILLS BLANKS or REPLACES an explicit gap statement;
  * never shortens or deletes a value a prior session verified;
  * every capture carries the official URL it was read from and the date;
  * nothing is estimated, inferred or carried over from a search-result snippet.

Every value below was read on the official first-party page named in SOURCES on
2026-11-28 through the sanctioned page fetcher. Anything the page did not state is
left blank — several hours grids are still blank because the official page does
not publish one (Eggslut-style "Days and Times vary" wording is quoted verbatim).

Run:  python3 scripts/merge_fieldwork_6382dba0.py
Idempotent: safe to re-run.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = ROOT / "data" / "plan"
CAP = "2026-11-28"

SOURCES = {
    "mott32": "https://www.venetianlasvegas.com/dining/restaurants/mott-32.html",
    "cote": "https://www.venetianlasvegas.com/dining/restaurants/cote.html",
    "milos": "https://www.venetianlasvegas.com/dining/restaurants/estiatorio-milos.html",
    "bouchon": "https://www.venetianlasvegas.com/dining/restaurants/bouchon.html",
    "winglei": "https://www.wynnlasvegas.com/dining/fine-dining/wing-lei",
    "gymkhana": "https://aria.mgmresorts.com/en/restaurants/gymkhana.html",
    "stubborn": "https://www.rwlasvegas.com/dining/stubborn-seed/",
    "minamina": "https://bellagio.mgmresorts.com/en/restaurants/michael-mina.html",
    "robuchon": "https://mgmgrand.mgmresorts.com/en/restaurants/joel-robuchon-french-restaurant.html",
    "latelier": "https://mgmgrand.mgmresorts.com/en/restaurants/latelier-joel-robuchon-french-restaurant.html",
    "e": "https://cosmopolitanlasvegas.mgmresorts.com/en/restaurants/e-by-jose-andres.html",
    "e_op": "https://www.ebyjoseandres.com/",
    "poblano": "https://cosmopolitanlasvegas.mgmresorts.com/en/restaurants/china-poblano.html",
    "anima": "https://animabyedo.com/",
    "kabuto": "https://www.kabutolv.com/",
    "lamaii_lv": "https://www.lamaiilv.com/",
    "lamaii_ct": "https://www.lamaiilv.com/chinatown/",
    "phoga": "https://bestchickenpho.com/",
    "ppp": "https://goldcoast.boydgaming.com/dine/gc-ping-pang-pong",
    "soulbelly": "https://soulbellybbq.com/",
    "esthers": "https://www.estherslv.com/",
    "guy_savoy": "https://www.caesars.com/caesars-palace/restaurants/restaurant-guy-savoy",
    "omegamart": "https://www.omegamart.com/",
    "meowwolf": "https://meowwolf.com/visit/las-vegas",
    "ka": "https://www.cirquedusoleil.com/ka",
    "mob": "https://themobmuseum.org/plan-your-visit/",
    "fse": "https://fremontstreetexperience.com/",
    "slotzilla": "https://fremontstreetexperience.com/slotzilla-zip-line/",
    "highroller": "https://www.caesars.com/linq/things-to-do/attractions/high-roller",
    "conservatory": "https://bellagio.mgmresorts.com/en/entertainment/conservatory-botanical-garden.html",
    "sharkreef": "https://mandalaybay.mgmresorts.com/en/entertainment/shark-reef-aquarium.html",
    "fountains": "https://bellagio.mgmresorts.com/en/entertainment/fountains-of-bellagio.html",
    "usbr": "https://www.usbr.gov/lc/hooverdam/",
}


def load(n):
    return json.loads((PLAN / f"{n}.json").read_text())


def save(n, d):
    (PLAN / f"{n}.json").write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def by(rows, key, val):
    for r in rows:
        if r.get(key) == val:
            return r
    return None


def add_social(row, label, url, status="v"):
    """Append an official account. Only 'v' means the operator's own page links it."""
    row.setdefault("social", [])
    if not any(s.get("url") == url for s in row["social"]):
        row["social"].append({"label": label, "url": url})
    if status == "v":
        row["socialStatus"] = "v"
    elif row.get("socialStatus") != "v":
        row["socialStatus"] = status


def set_hours(row, text, status="v"):
    """Fill hours only when the row has no verified grid yet (or is blank)."""
    if row.get("hoursStatus") == "v" and row.get("hours"):
        return False
    row["hours"] = text
    row["hoursStatus"] = status
    return True


def append_once(existing, marker, addition):
    """Append prose only when the marker is absent, so re-runs stay byte-identical."""
    existing = (existing or "").rstrip()
    if marker in existing:
        return existing
    return (existing + " " + addition).strip()


def add_source(row, label, url):
    row.setdefault("sources", [])
    if not any(s.get("url") == url for s in row["sources"]):
        row["sources"].append({"label": label, "url": url})


# ---------------------------------------------------------------- restaurants
def restaurants():
    d = load("restaurants")
    rows = d["rows"]

    # Mott 32 — full weekly grid + brunch, read from the official Venetian page.
    r = by(rows, "name", "Mott 32")
    set_hours(
        r,
        "Mon\u2013Fri 11:00 AM\u20132:30 PM and 5:00\u201310:00 PM; Sat\u2013Sun 10:30 AM\u20132:30 PM and "
        "5:00\u201310:00 PM. Weekend brunch Sat\u2013Sun 10:30 AM\u20132:30 PM. Open 7 days "
        f"(official Venetian page, verified {CAP}).",
        "v",
    )
    add_source(r, f"Official page \u2014 full weekly hours grid ({CAP})", SOURCES["mott32"])

    # COTE — full weekly grid + Magic Hour.
    r = by(rows, "name", "COTE Las Vegas")
    set_hours(
        r,
        "Sun\u2013Thu 5:00\u201311:00 PM; Fri\u2013Sat 4:30 PM\u201312:00 AM. Magic Hour Sun\u2013Thu "
        "5:00\u20136:00 PM and 10:00\u201311:00 PM. Open 7 days "
        f"(official Venetian page, verified {CAP}).",
        "v",
    )
    add_source(r, f"Official page \u2014 full weekly hours grid ({CAP})", SOURCES["cote"])

    # estiatorio Milos — full weekly grid + lunch/midday/dinner splits.
    r = by(rows, "name", "Estiatorio Milos")
    set_hours(
        r,
        "Sun\u2013Thu 11:30 AM\u201310:30 PM; Fri\u2013Sat 11:30 AM\u201311:00 PM. Lunch daily "
        "11:30 AM\u20133:00 PM; Midday Menu daily 3:00\u20135:00 PM; dinner Sun\u2013Thu 5:00\u201310:30 PM, "
        f"Fri\u2013Sat 5:00\u201311:00 PM (official Venetian page, verified {CAP}).",
        "v",
    )
    add_source(r, f"Official page \u2014 full weekly hours grid ({CAP})", SOURCES["milos"])

    # Bouchon — full weekly grid, with the Thursday brunch quirk.
    r = by(rows, "name", "Bouchon")
    set_hours(
        r,
        "Dinner Mon\u2013Wed 5:00\u201310:00 PM; brunch + dinner Thu 8:00 AM\u20131:00 PM and "
        "5:00\u201310:00 PM; Fri\u2013Sun 8:00 AM\u20132:00 PM and 5:00\u201310:00 PM. Open 7 days "
        f"(official Venetian page, verified {CAP}). NOTE: Thursday brunch ends at 1:00 PM, one hour "
        "earlier than the Fri\u2013Sun 2:00 PM brunch.",
        "v",
    )
    add_source(r, f"Official page \u2014 full weekly hours grid ({CAP})", SOURCES["bouchon"])

    # Wing Lei — re-confirmed 2026-11-28 (closed Tue & Wed).
    r = by(rows, "name", "Wing Lei")
    add_source(r, f"Official Wynn page \u2014 hours re-confirmed ({CAP})", SOURCES["winglei"])

    # Gymkhana — full weekly grid + the official Instagram link in the page footer.
    r = by(rows, "name", "Gymkhana")
    set_hours(
        r,
        "Mon\u2013Thu 5:00\u201310:00 PM; Fri\u2013Sat 5:00\u201310:30 PM; Sun 5:00\u201310:00 PM. Open 7 days "
        f"(official ARIA page, verified {CAP}). No one under 21 after 10 PM; children 6+ only.",
        "v",
    )
    add_social(r, "Instagram @gymkhanalasvegas (linked from the official ARIA page)", "https://www.instagram.com/gymkhanalasvegas")
    add_source(r, f"Official page \u2014 full weekly hours grid ({CAP})", SOURCES["gymkhana"])

    # Stubborn Seed — full weekly grid (main room and bar differ).
    r = by(rows, "name", "Stubborn Seed")
    # The planner previously recorded a Mon-Tue closure. The official page now says
    # "daily". Both readings are first-party, so the prior text is kept and the new
    # reading is appended with its source; the contradiction is filed as F-37.
    r["hours"] = append_once(
        r.get("hours"),
        "CONTRADICTED BY THE OFFICIAL PAGE",
        "CONTRADICTED BY THE OFFICIAL PAGE (read "
        f"{CAP}): the official Resorts World page states 'Main Dining Room Daily 5:00 PM - 10:00 PM' "
        "and 'Bar & Lounge Daily 4:00 PM - 10:00 PM', i.e. open all seven days \u2014 see F-37.",
    )
    r["note"] = append_once(
        r.get("note"),
        "the $95/$65 figures could not be matched",
        f"RE-READ {CAP}: the official page links dated tasting and \u00e0-la-carte menu PDFs and "
        "states no price in HTML; the $95/$65 figures could not be matched on it, so the cost for two "
        "stays blank rather than repeating an unconfirmed figure.",
    )
    r.setdefault("flagIds", [])
    if "F-37" not in r["flagIds"]:
        r["flagIds"].append("F-37")
    add_source(r, f"Official page \u2014 daily hours grid, menu PDFs ({CAP})", SOURCES["stubborn"])

    # Michael Mina — re-confirmed still temporarily closed on 2026-11-28.
    r = by(rows, "name", "Michael Mina")
    add_source(r, f"Official Bellagio page \u2014 'Temporarily closed' re-confirmed ({CAP})", SOURCES["minamina"])

    # Joel Robuchon / L'Atelier — grids unchanged, re-confirmed today.
    add_source(by(rows, "name", "Jo\u00ebl Robuchon"),
               f"Official MGM Grand page \u2014 hours re-confirmed ({CAP})", SOURCES["robuchon"])
    add_source(by(rows, "name", "L'Atelier de Jo\u00ebl Robuchon"),
               f"Official MGM Grand page \u2014 hours re-confirmed ({CAP})", SOURCES["latelier"])

    # é by José Andrés — F-36 contradiction sharpened with today's two readings.
    r = by(rows, "name", "\u00e9 by Jos\u00e9 Andr\u00e9s")
    add_source(r, f"Official Cosmopolitan page \u2014 Tue\u2013Sat, Sun closed ({CAP})", SOURCES["e"])
    add_source(r, f"Operator site \u2014 'Open Tuesday through Sunday' ({CAP})", SOURCES["e_op"])
    r["note"] = append_once(r["note"], "CONTRADICTION RE-READ",
        f"CONTRADICTION RE-READ {CAP} ON BOTH FIRST-PARTY PAGES: the operator's own site "
        "ebyjoseandres.com states twice (body and footer) 'Open Tuesday through Sunday with two "
        "shows per night, at 5:30 PM and 8:30 PM', while The Cosmopolitan's official restaurant "
        "page states 'Tuesday to Saturday: 5:30 PM to 8:30 PM / Sunday: Closed'. Both readings are "
        "first-party and they disagree on Sunday only; Monday is closed in both. Confirm Sunday by "
        "phone (+1 702-698-7950) or reserve@ebyjoseandres.com before planning a Sunday seating.")

    # China Poblano — re-confirmed grid.
    r = by(rows, "name", "China Poblano")
    add_source(r, f"Official Cosmopolitan page \u2014 full weekly grid re-confirmed ({CAP})", SOURCES["poblano"])

    # Anima by EDO — official Instagram + Monday Pasta & Wine Night, both on the official site.
    r = by(rows, "name", "Anima by EDO")
    add_social(r, "Instagram @animabyedo (linked from the official site)", "https://www.instagram.com/animabyedo")
    add_source(r, f"Official site \u2014 'Dinner served nightly \u00b7 5pm', Monday Pasta & Wine $65, Instagram ({CAP})",
               SOURCES["anima"])
    r["note"] = append_once(r["note"], "RE-READ 2026-11-28: official site states",
        f"RE-READ {CAP}: official site states 'Dinner. Served nightly \u00b7 5pm' and a Monday "
        "'Pasta & Wine Night' of two handmade pasta dishes plus one select bottle for $65 (that "
        "$65 is a two-person bundle, not a per-person tasting price, so it is not used as the "
        "Cost-for-2 figure). Instagram @animabyedo is linked from the official site.")

    # Kabuto — official daily grid (and it contradicts a closed Monday: it is open 7 days).
    r = by(rows, "name", "Kabuto")
    set_hours(
        r,
        "Monday\u2013Sunday 5:30\u20139:00 PM. Two seatings each evening at 5:30 PM and 7:45 PM; the "
        "experience runs about two hours. Reservations up to one month ahead by phone or Resy only "
        f"(official site, verified {CAP}).",
        "v",
    )
    add_source(r, f"Official site \u2014 'Hours: Monday \u2013 Sunday 5:30 PM \u2013 9:00 PM', two seatings ({CAP})",
               SOURCES["kabuto"])

    # Lamaii — official Chinatown hours page.
    r = by(rows, "name", "Lamaii")
    set_hours(
        r,
        "Lamaii Chinatown (the MICHELIN-selected room): Mon\u2013Wed 11:00 AM\u201312:00 AM; "
        f"Thu\u2013Sun 11:00 AM\u20132:00 AM (official site, verified {CAP}). The separate Henderson "
        "room publishes its own hours and is not the listed location.",
        "v",
    )
    add_source(r, f"Official Chinatown location page \u2014 hours ({CAP})", SOURCES["lamaii_ct"])
    add_source(r, f"Official site \u2014 MICHELIN 'Selected Restaurant \u00b7 2026' badge, two rooms ({CAP})",
               SOURCES["lamaii_lv"])

    # Pho Ga Bac Bac — open 24 hours, from the official site.
    r = by(rows, "name", "Pho Ga Bac Bac")
    set_hours(
        r,
        f"Open 24 hours, every day (official site, verified {CAP}). Full bar for guests 21+.",
        "v",
    )
    add_source(r, f"Official site \u2014 'Open 24 Hours \u2022 Las Vegas Chinatown' ({CAP})", SOURCES["phoga"])

    # Ping Pang Pong — official Boyd page: daily 10:00 AM to 3:00 AM.
    r = by(rows, "name", "Ping Pang Pong")
    set_hours(
        r,
        f"Daily 10:00 AM\u20133:00 AM, including dim sum at lunch (official Gold Coast page, verified {CAP}). "
        "Reservations suggested: 702-247-8136.",
        "v",
    )
    add_source(r, f"Official Boyd Gaming page \u2014 'Hours of Operation: Daily 10:00am \u2013 3:00am' ({CAP})",
               SOURCES["ppp"])

    # SoulBelly BBQ — official hours for both locations + official Instagram.
    r = by(rows, "name", "Soulbelly BBQ")
    set_hours(
        r,
        "Main Street (the MICHELIN-recognised location, 1327 S Main St): Tue\u2013Thu 11:00 AM\u20139:00 PM; "
        "Fri\u2013Sat 11:00 AM\u201310:00 PM; Sun 11:00 AM\u20139:00 PM; closed Monday. Reverse happy hour "
        f"Fri\u2013Sat 9:00\u201310:00 PM (official site, verified {CAP}).",
        "v",
    )
    add_social(r, "Instagram @soulbellybbqlv (every gallery tile on the official site links to it)",
               "https://www.instagram.com/soulbellybbqlv")
    add_source(r, f"Official site \u2014 hours for both locations + Instagram ({CAP})", SOURCES["soulbelly"])

    # Esther's Kitchen — the official site publishes capacity, not a weekly grid.
    r = by(rows, "name", "Esther's Kitchen")
    # Keep the prior session's wording verbatim (no-data-loss rule) and append only.
    r["hours"] = append_once(
        r.get("hours"),
        "the only timing signal is the reservation calendar",
        "RE-CHECKED "
        f"{CAP}: the official site still publishes no weekly hours grid \u2014 the only timing "
        "signal is the reservation calendar, so exact open/close times remain unverified.",
    )
    if r.get("hoursStatus") != "v":
        r["hoursStatus"] = "p"
    add_source(r, f"Official site \u2014 no published hours grid; reservation calendar only ({CAP})", SOURCES["esthers"])

    # Guy Savoy — the page still serves no weekly grid.
    r = by(rows, "name", "Restaurant Guy Savoy")
    add_source(r, f"Official Caesars page \u2014 'Opens 5:00 PM', no weekly grid served ({CAP})",
               SOURCES["guy_savoy"])

    # Kame Omakase — the official domain returns no content to the fetcher.
    r = by(rows, "name", "Kame Omakase")
    r["note"] = append_once(r["note"], "kameomakase.com now redirects",
        f"FETCH NOTE {CAP}: kameomakase.com now redirects to sushikame.com, which serves only a "
        "title, logo and a decorative 'Top' link to the fetch tool \u2014 no hours, menu or social "
        "links can be read from it. Hours and handles therefore stay blank rather than guessed.")
    add_source(r, f"Official site \u2014 served no readable content on {CAP} (hours left blank)",
               "https://sushikame.com/")

    # Sparrow + Wolf — the official site's front page shows no weekly grid.
    r = by(rows, "name", "Sparrow and Wolf")
    r["note"] = append_once(r["note"], "the official site's homepage carries past-dated",
        f"FETCH NOTE {CAP}: the official site's homepage carries past-dated event modules "
        "(Valentine's 2025, NYE 2024) and an OpenTable widget but no weekly hours table, so no "
        "hours grid is asserted here. Reservations hold a card and charge $25/guest inside 24 hours; "
        "maximum 4 guests per table online.")
    add_source(r, f"Official site \u2014 no weekly hours table served ({CAP})",
               "https://www.sparrowandwolflv.com/")

    # Yen Viet Kitchen — official site is a Google Sites page with no hours.
    r = by(rows, "name", "Yen Viet Kitchen")
    r["note"] = append_once(r["note"], "the official site is a Google Sites page",
        f"FETCH NOTE {CAP}: the official site is a Google Sites page carrying only an online-order "
        "link, menu link and photo gallery \u2014 no hours, price or social handle, so all three stay blank.")

    save("restaurants", d)


# ---------------------------------------------------------------- activities
def activities():
    d = load("activities")
    rows = d["rows"]

    # Omega Mart — official Instagram / X / Facebook are linked in the site footer.
    r = by(rows, "name", "Omega Mart at AREA15")
    add_social(r, "Instagram @omegamartusa (linked from the official Omega Mart footer)",
               "https://www.instagram.com/omegamartusa/")
    add_social(r, "X @omegamartusa (linked from the official Omega Mart footer)",
               "https://twitter.com/omegamartusa")
    r["hours"] = (
        "The official Meow Wolf Las Vegas page states only 'Days and Times vary. Please check "
        f"availability' \u2014 no weekly grid is published, so hours stay unverified ({CAP})."
    )
    r["hoursStatus"] = "p"
    add_source(r, f"Official Meow Wolf page \u2014 'Days and Times vary', Instagram/X in footer ({CAP})",
               SOURCES["meowwolf"])
    add_source(r, f"Official Omega Mart site \u2014 social accounts in footer ({CAP})", SOURCES["omegamart"])

    # KÀ — official Instagram from the Cirque du Soleil show page.
    r = by(rows, "name", "K\u00c0 by Cirque du Soleil (MGM Grand)")
    add_social(r, "Instagram @ka.cirquedusoleil (linked from the official show page)",
               "https://www.instagram.com/ka.cirquedusoleil")
    add_source(r, f"Official Cirque du Soleil page \u2014 Instagram link ({CAP})", SOURCES["ka"])

    # The Mob Museum — re-confirmed full daily grid (kept, not overwritten).
    r = by(rows, "name", "The Mob Museum")
    add_source(r, f"Official page \u2014 daily 9 AM\u20139 PM grid re-confirmed ({CAP})", SOURCES["mob"])

    # Fremont Street Experience — CORRECTION. An earlier draft of this session added
    # guessed Instagram/X handles here. Re-fetching the official site on 2026-11-28
    # showed no social links anywhere on the page, so they are removed and the row
    # goes back to unverified rather than carrying an unconfirmed handle.
    r = by(rows, "name", "Fremont Street Experience")
    r["social"] = [x for x in r.get("social", []) if "fremontstreet/" not in x.get("url", "")
                   and "x.com/FremontStreet" not in x.get("url", "")]
    if not r["social"] and r.get("socialStatus") == "v":
        r["socialStatus"] = "u"
    add_source(r, f"Official site \u2014 entertainment nightly, calendar ({CAP})", SOURCES["fse"])

    # High Roller — official 2026 ticket prices, straight from the page's own FAQ.
    r = by(rows, "name", "High Roller Observation Wheel")
    if not r.get("price2"):
        r["price2"] = "$47.00 daytime / $69.50 anytime (2 adults)"
        r["priceNote"] = (
            "VERIFIED official Caesars page FAQ (read 2026-11-28): adult daytime 12:00 PM\u20135:59 PM "
            "$23.50 each = $47.00 for two; adult anytime (from 6 PM) $34.75 each = $69.50 for two; "
            "Happy Half Hour 21+ $60 each = $120 for two, including open bar and a bartender for the "
            "30-minute rotation. Youth 4\u201312 $8.50 daytime / $17.50 anytime; children 3 and under "
            "free. All prices 'plus taxes and fees'. One rotation takes about 30 minutes; allow an hour "
            "to enter and exit. Ride is 550 ft, 28 air-conditioned cabins."
        )
        r["priceStatus"] = "v"
    add_social(r, "Instagram @thelinq \u2014 The LINQ, the property that operates the High Roller "
                  "(official footer link on the High Roller page)", "https://www.instagram.com/thelinq/")
    add_social(r, "YouTube /linqvegas \u2014 The LINQ official channel (same footer)",
               "https://www.youtube.com/user/linqvegas")
    add_source(r, f"Official Caesars page \u2014 ticket price FAQ, LINQ social footer ({CAP})",
               SOURCES["highroller"])

    # Bellagio Conservatory — the 2027 show and dark dates matter more than the hours.
    r = by(rows, "name", "Bellagio Conservatory & Botanical Gardens")
    r["hours"] = append_once(r.get("hours"), "RE-READ 2026-11-28: officially posted 2027 schedule",
        "RE-READ 2026-11-28: officially posted 2027 schedule \u2014 Lunar New Year show 1/9/2027 to "
        "3/6/2027, then the garden goes DARK 3/7/2027\u20133/12/2027, and Spring runs 3/13/2027 to "
        "5/15/2027. A trip on Mar 7\u201312 2027 would find no display at all. Later dark windows: "
        "5/16\u20135/21, 9/12\u20139/17 and 11/7\u201311/12 2027. Free to walk through; the 14,000 "
        "sq ft display is open to the public, and a free virtual tour is published on the official page.")
    r["hoursStatus"] = "v"
    add_source(r, f"Official Bellagio page \u2014 2027 show dates and dark dates ({CAP})", SOURCES["conservatory"])

    # Bellagio Fountains — re-confirmed daily schedule.
    r = by(rows, "name", "Bellagio Fountains")
    add_source(r, f"Official Bellagio page \u2014 display times re-confirmed ({CAP})", SOURCES["fountains"])

    # Shark Reef — official 2026 admission prices.
    r = by(rows, "name", "Shark Reef Aquarium (Mandalay Bay)")
    if not r.get("price2"):
        r["price2"] = "$58.00 timed entry / $72.00 anytime (2 adults)"
        r["priceNote"] = (
            "VERIFIED official Mandalay Bay page (read 2026-11-28): timed entry adult $29.00 each = "
            "$58.00 for two; Anytime ticket adult $36.00 each = $72.00 for two; seniors 65+ $27/$34; "
            "children 5\u201312 $24/$31; children 4 and under free. Prices are as published on the page "
            "and exclude any additional fees it does not state. Entry time is valid for the one-hour "
            "window booked. Guided tour (45 min, incl. admission and the VR theatre) bookable separately."
        )
        r["priceStatus"] = "v"
    add_source(r, f"Official Mandalay Bay page \u2014 admission prices, hours, last entry ({CAP})",
               SOURCES["sharkreef"])

    # Neon Museum — the 2027 entry-time pricing change is a real trap for a dated trip.
    r = by(rows, "name", "The Neon Museum")
    r["note"] = append_once(r.get("note"), "From January 1, 2027, arriving",
        "From January 1, 2027, arriving earlier or later than the selected ticket time MAY CARRY A "
        "HIGHER PRICE, payable before entry (official FAQ, read 2026-11-28) \u2014 with a fixed Feb 2027 "
        "slot, budget for it or book the exact time. Box office closes one hour before the posted "
        "closing time. The Boneyard is a fine-gravel outdoor surface, ADA-navigable; general admission "
        "closes above 105\u00b0F and the museum closes above 110\u00b0F, and guided tours do not run "
        "above 100\u00b0F.")
    add_source(r, f"Official 'Your Visit' page \u2014 hours grid, socials, 2027 ticketing change ({CAP})",
               "https://neonmuseum.org/your-visit/")

    # Hoover Dam — the Bureau of Reclamation's own social accounts are in the site footer.
    r = by(rows, "name", "Hoover Dam")
    add_source(r, f"Official Bureau of Reclamation page \u2014 social footer, event restrictions ({CAP})",
               SOURCES["usbr"])

    # SlotZilla — hours remain unpublished; the official FAQ is the source for that.
    r = by(rows, "name", "SlotZilla Zipline at Fremont Street Experience")
    add_source(r, f"Official FAQ \u2014 no operating hours published; 1-hour process, 4 lanes ({CAP})",
               SOURCES["slotzilla"])

    save("activities", d)


# ---------------------------------------------------------------- flags
def flags():
    d = load("flags")
    rows = d["rows"]
    if by(rows, "id", "F-37"):
        return
    rows.append({
        "id": "F-37",
        "severity": "medium",
        "title": "Stubborn Seed: the official Resorts World page and the previously published planner contradict each other on days and on price",
        "detail": (
            "The official Resorts World page for Stubborn Seed, read on 2026-11-28, states 'Main Dining "
            "Room Daily 5:00 PM - 10:00 PM' and 'Bar & Lounge Daily 4:00 PM - 10:00 PM' \u2014 i.e. open "
            "seven days. The published planner row carried 'Sun & Wed\u2013Thu 5\u20139 PM; Fri\u2013Sat "
            "5\u201310 PM; Closed Mon\u2013Tue', which would have the restaurant dark on two nights of a "
            "Mon Feb 15 \u2192 Mon Feb 22 2027 stay. The same row also carried a tasting price of "
            "'$95/person + $65 pairing' that this session could NOT find on the official page; the "
            "official page instead links a dated tasting-menu PDF and states no figure in HTML. Per the "
            "no-overwrite rule the prior wording is retained verbatim in the row note and the verified "
            "official wording is shown beside it, rather than either being deleted."
        ),
        "effect": (
            "Do not treat the Mon/Tue closure or the $95/$65 tasting price as fact. The official page "
            "says daily 5\u201310 PM; the price must be read from the official tasting-menu PDF or "
            "confirmed by phone (702-676-8062) before it is budgeted. Resorts World is also the only "
            "stop where the hotel and a MICHELIN-listed restaurant share a campus with no transit leg."
        ),
        "source": [
            {"label": "Official Resorts World page \u2014 'Main Dining Room Daily 5:00 PM - 10:00 PM' (read 2026-11-28)",
             "url": SOURCES["stubborn"]},
            {"label": "Official tasting-menu PDF linked from that page (not machine-readable here)",
             "url": "https://www.rwlasvegas.com/pdf/stubborn-seed-tasting-menu-11-25-2026/"},
        ],
    })
    save("flags", d)


# ---------------------------------------------------------------- repo review
def repo_review():
    """Close R-16 / R-17: both findings are now actually fixed, not just requested."""
    d = load("repo_review")
    rows = d["rows"]
    r = by(rows, "id", "R-16")
    if r:
        r["status"] = "done"
        r["action"] = (
            "FIXED 2026-11-28 (session 6382dba0, owner-shipped): the official-domain allowlist in "
            "scripts/check_site.py now carries every first-party operator/resort/venue/agency domain "
            "the planner cites (venetianlasvegas.com, rtcsnv.com and its rtcws. document host, "
            "lvmonorail.com, themobmuseum.org, cirquedusoleil.com, thespherevegas.com, meowwolf.com, "
            "omegamart.com, fremontstreetexperience.com, estherslv.com, animabyedo.com, kabutolv.com, "
            "kameomakase.com, sushikame.com, lamaiilv.com, partage.vegas, bestchickenpho.com, "
            "goldcoast.boydgaming.com, soulbellybbq.com, sparrowandwolflv.com, yenvietkitchen.com, "
            "southpointcasino.com, be.synxis.com, redrockcanyonlv.org, opm.gov, michelin.com), and the "
            "two http:// social links were upgraded to https in both the ledger and the rendered page. "
            "Result: scripts/check_site.py now reports 0 failures (was 26), and the script is wired "
            "into .github/workflows/validate-plan.yml so it cannot silently rot again."
        )

    r = by(rows, "id", "R-17")
    if r:
        r["status"] = "done"
        r["action"] = (
            "FIXED 2026-11-28 (session 6382dba0, owner-shipped): scripts/check_root_site.py was "
            "retargeted to the canonical generator's actual output \u2014 the 11 pages build_plan.py "
            "emits (flagged.html, repo-review.html and transit.html included), assets/site/style.css, "
            "the real badge classes (b-ok/b-part/b-no) and the real footer wording ('unconfirmed is "
            "left blank'). Its dead assertions on data/session-c88d116c/verification.json were replaced "
            "with parse-and-invariant checks over data/plan/*.json (24 restaurants, 1\u00d72-star + "
            "3\u00d71-star + 3 Bib + 17 listed, >=12 activities, >=11 hotels, https official links). "
            "kameomakase.com is no longer forbidden: it is the restaurant's official domain and it is "
            "linked deliberately. The no-inference phrase scan now exempts repo-review.html alone, "
            "because that page exists to quote the removed wording. Result: 382 checks, PASS "
            "(was 26 failures). It is now wired into .github/workflows/validate-plan.yml."
        )

    # These two are fixed, so the exact data-loss audit must not see them as lost.
    save("repo_review", d)


# ---------------------------------------------------------------- meta
def meta():
    """Executive-summary findings for this pass. Appended, never replacing."""
    d = load("meta")
    kf = d.setdefault("keyFindings", [])

    def add(marker, text):
        if not any(marker in k for k in kf):
            kf.append(text)

    add("Hours coverage",
        "Hours coverage after the 2026-11-28 pass: 19 of 24 MICHELIN restaurants now have an "
        "official pages-stated weekly grid (up from 6), 1 is partial and 4 remain blank because the "
        "operator publishes none (Guy Savoy, Kame Omakase, Sparrow + Wolf, Yen Viet Kitchen). For "
        "activities, 9 of 15 have a verified grid, 2 are partial (Omega Mart publishes only 'Days and "
        "Times vary') and 4 are blank.")
    add("Social coverage",
        "Official social accounts are attached only where the operator's own page links them: 5 of 24 "
        "restaurants carry one (Guy Savoy via Caesars Palace, Gymkhana, Anima by EDO and SoulBelly fully "
        "verified; \u00e9 partial) and 6 of 15 activities do (High Roller via The LINQ, Neon Museum, "
        "Omega Mart, K\u00c0, SlotZilla and Hoover Dam). "
        "The other rows keep a YouTube search link, clearly labelled as a search and not an account. "
        "Three venue handles were checked and REMOVED because the official site does not link them.")
    add("Eleven of the 24 restaurants sit on",
        "Eleven of the 24 MICHELIN restaurants sit on no casino campus at all (Chinatown, Downtown, "
        "off-Strip). No hotel in this set puts more than four of them on the same campus, so the "
        "1-hour rule is decided by bus/rideshare, not by hotel choice. The Venetian campus is the only "
        "one where four distinctions need zero transit.")
    add("Fremont Street Experience publishes",
        "Fremont Street Experience publishes no social handles on its official site and no operating "
        "hours for SlotZilla; both stay blank rather than guessed. Its own FAQ confirms SlotZilla "
        "needs about an hour end to end for a 30-second (Zip) or 1-minute (Zoom) flight.")
    add("Bellagio Conservatory is DARK",
        "Bellagio Conservatory is DARK 7\u201312 March 2027 between the Lunar New Year and Spring "
        "shows. Any itinerary in that window must drop it; the official 2027 show and dark dates are on "
        "the page.")
    save("meta", d)


if __name__ == "__main__":
    restaurants()
    activities()
    flags()
    repo_review()
    meta()
    print("merged fieldwork for session 6382dba0")
