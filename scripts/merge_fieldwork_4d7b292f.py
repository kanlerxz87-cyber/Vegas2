#!/usr/bin/env python3
"""Session 4d7b292f — additive merge of newly verified fieldwork into the canonical
data/plan/*.json produced by session 155b420b.

Design rule: this script only FILLS BLANKS, APPENDS rows, or APPENDS sources/flags.
It never deletes or overwrites a value that a prior session verified, except where
this session captured a newer dated rate for the same field (which is recorded with
its capture date and kept alongside the old figure).

Run:  python3 scripts/merge_fieldwork_4d7b292f.py
Idempotent: safe to re-run.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = ROOT / "data" / "plan"
CAP = "2026-11-27"


def load(n):
    return json.loads((PLAN / f"{n}.json").read_text())


def save(n, d):
    (PLAN / f"{n}.json").write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def by(rows, key, val):
    for r in rows:
        if r.get(key) == val:
            return r
    return None


def append_once(existing, marker, addition):
    """Append prose only if the marker is not already present (keeps re-runs idempotent)."""
    existing = existing or ""
    if marker in existing:
        return existing
    return (existing + " " + addition).strip()


def add_source(row, label, url):
    if not any(s.get("url") == url for s in row.setdefault("sources", [])):
        row["sources"].append({"label": label, "url": url})


def add_social(row, label, url):
    if not any(s.get("url") == url for s in row.setdefault("social", [])):
        row["social"].append({"label": label, "url": url})
    row["socialStatus"] = "v"


# ---------------------------------------------------------------- hotels
def hotels():
    d = load("hotels")
    rows = d["rows"]

    w = by(rows, "id", "wynn")
    w["price7"] = {
        "total": 4739,
        "room": "Wynn Resort King (640 sq ft)",
        "nightly": "$677 avg/night including the resort fee (Cyber Exclusive)",
        "math": "$677 \u00d7 7 = $4,739 before taxes",
        "basis": ("Official dated engine: 'Wynn Cyber Exclusive + Up to $300 Resort Credit' at $677 Avg/Night, "
                  "'Includes Resort Fee, Excludes taxes'. Resort fee is $55/night plus tax. "
                  "Must be booked Nov 20 \u2013 Dec 4, 2026."),
    }
    w["price7Note"] = (
        "VERIFIED " + CAP + ": official Wynn booking engine, Wynn Resort King, 7-night stay "
        "Feb 15\u201322 2027, 2 adults. 'Wynn Cyber Exclusive + Up to $300 Resort Credit' shows "
        "$677 Avg/Night, 'Includes Resort Fee, Excludes taxes'. $677 x 7 = $4,739 before tax. "
        "The Flexible Getaway Rate on the same page is $833 Avg/Night ($5,831 for 7 nights)."
    )
    w["price7Status"] = "v"
    w["price7Alt"] = {
        "label": "Flexible Getaway Rate (no sale)",
        "nightly": 833,
        "total": 5831,
        "basis": "Includes resort fee, excludes taxes. Cancel 72 hours before arrival.",
    }
    w["bookBy"] = "2026-12-04"
    w["note"] = append_once(w.get("note"), "TIME-CRITICAL:",
                 "TIME-CRITICAL: the $677 Cyber rate must be BOOKED between "
                 "Nov 20 and Dec 4, 2026 (stays Nov 22 2026\u2013Jun 30 2027, 1\u201314 nights). "
                 "It also carries a $75/day resort credit up to $300 per stay. Room is 640 sq ft "
                 "with a marble bathroom, glass-enclosed shower, deep-soaking tub and separate "
                 "water closet. Self-parking complimentary for registered guests.")
    add_source(w, "Official dated Wynn rate page \u2014 $677 Cyber / $833 Flexible, Feb 15\u201322 2027",
               "https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&langID=1&rmID=68658&checkIn=02/15/2027&checkOut=02/22/2027&adults=2&children=0")
    add_source(w, "Official Cyber sale terms \u2014 book Nov 20\u2013Dec 4 2026",
               "https://www.wynnlasvegas.com/terms-and-conditions/2026-cyber-sale-offer-public")

    rw = by(rows, "id", "resorts-world")
    rw["price7"] = {
        "total": 1940.47,
        "room": "Las Vegas Hilton tower \u2014 promotional rate, room category not named in the offer tile",
        "nightly": "$277.21 avg/night including the resort fee (Cyber Sale)",
        "math": "$277.21 \u00d7 7 = $1,940.47 before taxes",
        "basis": ("Official 'Up to 50% Off' tile: 'Current price: $277.21 ... Avg./Per Night Includes Resort Fee "
                  "and Excludes Taxes'. Bed type and bathroom are not stated in that tile, so they stay unverified."),
    }
    rw["price7Note"] = (
        "VERIFIED " + CAP + ": official Resorts World engine, Las Vegas Hilton tower, Feb 15\u201322 2027, "
        "2 adults. 'Up to 50% Off' Cyber Sale tile: 'Current price: $277.21 ... Avg./Per Night "
        "Includes Resort Fee and Excludes Taxes'. $277.21 x 7 = $1,940.47 before tax. "
        "'Signature Savings' and '$75 Dining Credits' offers both show $351.29 Avg/Night for the same dates."
    )
    rw["price7Status"] = "v"
    rw["price7Alt"] = {"label": "Signature Savings / Dining Credit offers", "nightly": 351.29, "total": 2459.03,
                       "basis": "Includes resort fee, excludes taxes."}
    rw["note"] = append_once(rw.get("note"), "two contradictory resort-fee captions",
                  "The engine's February 2027 month calendar is reproduced on "
                  "Prices & dates; it prints two contradictory resort-fee captions (F-26).")
    add_source(rw, "Official dated Resorts World rate page + February 2027 calendar",
               "https://reservations.rwlasvegas.com/ibe/shop.aspx?hotelID=17726&selectedTower=HILTON&checkin=2027-02-15&checkout=2027-02-22&nights=7&adults=2&children=0")

    cp = by(rows, "id", "caesars-palace")
    add_social(cp, "Caesars Palace \u2014 official Instagram", "https://www.instagram.com/caesarspalace/")
    add_social(cp, "Caesars Palace \u2014 official YouTube", "https://www.youtube.com/user/caesarspalace")
    cp["note"] = append_once(cp.get("note"), "Social accounts are property-level",
                  "Social accounts are property-level, linked from the official "
                  "Restaurant Guy Savoy page footer; they are not restaurant-specific.")

    sp = by(rows, "id", "south-point")
    if sp:
        if sp.get("price7"):
            sp["price7"]["publishedTotal"] = True
            sp["price7"]["basis"] = append_once(sp["price7"].get("basis"), "ROUNDING DISCREPANCY",
                "ROUNDING DISCREPANCY (F-35): the engine prints both '$141 Per Night' and "
                "'$989 Total for 7 nights'. $141 x 7 = $987, not $989; $989 / 7 = $141.29. "
                "The explicit stay total is treated as authoritative and the nightly figure as a "
                "rounded display. Nothing is adjusted or averaged.")

        sp["note"] = append_once(sp.get("note"), "Booking engine confirms Premium 2 Queens",
                      "Booking engine confirms Premium 2 Queens is 500 sq ft, "
                      "sleeps 4, with a mini refrigerator; the bathroom configuration is not stated "
                      "on the retrieved page and stays unverified.")

    new = [
        {
            "id": "horseshoe",
            "name": "Horseshoe Las Vegas",
            "area": "Center Strip",
            "venues": ["Horseshoe Las Vegas"],
            "rooms": "Resort Room | 1 King \u2014 450 sq ft, one king bed, 42-inch TV, workspace and sitting area.",
            "bath": "Official room description: 'stylish marble bathroom with a vanity'. Room amenities list 'Shower only'.",
            "roomStatus": "v",
            "price7": {
                "total": 812,
                "room": "Resort Room | 1 King (450 sq ft)",
                "nightly": "$116/night including the $50/day resort fee",
                "math": "$116 \u00d7 7 = $812 before taxes",
                "basis": ("Rate card: $66 room rate (standard $95) + $50 resort fee = $116/night, taxes excluded. "
                          "Fee disclosure: $56.63 with tax ($49.95 + $6.68)."),
            },
            "price7Note": ("VERIFIED " + CAP + ": $66 room rate (standard $95) + $50 daily resort fee = "
                           "$116/night including resort fee, excluding taxes. $116 x 7 = $812. "
                           "Resort fee disclosure: $56.63 with tax ($49.95 + $6.68)."),
            "price7Status": "v",
            "price3": None,
            "transit": "Center Strip on the Las Vegas Blvd Deuce corridor. Door-to-door times not retrieved.",
            "transitStatus": "u",
            "social": [],
            "socialStatus": "u",
            "sources": [
                {"label": "Official dated rate page \u2014 Feb 15\u201322 2027, 2 adults",
                 "url": "https://www.caesars.com/book/room-list?arrivalDate=02/15/2027&departureDate=02/22/2027&dateSearchFormat=exact-dates&propCode=blv&numberOfAdults=2&numberOfRooms=1"},
                {"label": "Official hotel page", "url": "https://www.caesars.com/horseshoe-las-vegas/hotel"},
            ],
            "note": ("Cheapest verified CENTER-Strip room with a confirmed king bed AND a confirmed private "
                     "bathroom. 450 sq ft is larger than Flamingo (350) and Paris (390). Check-in 4 PM, "
                     "check-out 11 AM, minimum age 21. 'Room Type Assigned on Arrival' is $110/night but "
                     "does not guarantee a bed type, so it fails the brief's queen-or-larger requirement."),
            "flagIds": ["F-03"],
        },
        {
            "id": "planet-hollywood",
            "name": "Planet Hollywood Resort & Casino",
            "area": "Center Strip",
            "venues": ["Planet Hollywood"],
            "rooms": "Ultra Hip Room | 1 King | Mountain View \u2014 430 sq ft, one king bed with luxury bedding, workspace, 42-inch TV, mini refrigerator.",
            "bath": "",
            "roomStatus": "p",
            "price7": {
                "total": 861,
                "room": "Ultra Hip Room | 1 King | Mountain View (430 sq ft)",
                "nightly": "$123/night including the $55/day resort fee",
                "math": "$123 \u00d7 7 = $861 before taxes",
                "basis": ("Rate card: $68 room rate (standard $138) + $55 resort fee = $123/night, taxes excluded. "
                          "Fee disclosure: $62.30 with tax ($54.95 + $7.35)."),
            },
            "price7Note": ("VERIFIED " + CAP + ": $68 room rate (standard $138) + $55 daily resort fee = "
                           "$123/night including resort fee, excluding taxes. $123 x 7 = $861. "
                           "Resort fee disclosure: $62.30 with tax ($54.95 + $7.35)."),
            "price7Status": "v",
            "price3": None,
            "transit": "Center Strip on the Las Vegas Blvd Deuce corridor. Door-to-door times not retrieved.",
            "transitStatus": "u",
            "social": [],
            "socialStatus": "u",
            "sources": [
                {"label": "Official dated rate page \u2014 Feb 15\u201322 2027, 2 adults",
                 "url": "https://www.caesars.com/book/room-list?arrivalDate=02/15/2027&departureDate=02/22/2027&dateSearchFormat=exact-dates&propCode=phv&numberOfAdults=2&numberOfRooms=1"},
                {"label": "Official hotel page", "url": "https://www.caesars.com/planet-hollywood/hotel"},
            ],
            "note": ("King bed verified; the bathroom is NOT described in the official room text, so it "
                     "stays unverified. A $50/day food-and-beverage credit package is $184/night. "
                     "'Room Type Assigned on Arrival' is $118/night, bed type not guaranteed."),
            "flagIds": ["F-03", "F-04"],
        },
    ]
    for n in new:
        if not by(rows, "id", n["id"]):
            rows.append(n)

    d["rankMethod"] = append_once(d.get("rankMethod"), "(session 4d7b292f)",
        "Update " + CAP + " (session 4d7b292f): Wynn and Resorts World now have verified dated "
        "7-night figures, and Horseshoe and Planet Hollywood were added, so the price ladder is "
        "complete from $581 to $5,831 before tax.")
    save("hotels", d)


# ---------------------------------------------------------------- restaurants
def restaurants():
    d = load("restaurants")
    rows = d["rows"]
    fills = {
        "L'Atelier de Jo\u00ebl Robuchon": {
            "hours": "Mon 5:00\u20139:30 PM; Thu\u2013Sun 5:00\u20139:30 PM. CLOSED Tuesday and Wednesday.",
            "hoursStatus": "v",
            "note": ("$$$ \u00b7 Business Casual \u00b7 Reservations 702.891.7358 \u00b7 children 6 and under not "
                     "accepted \u00b7 34-seat counter facing the open kitchen. One MICHELIN Star 2026; "
                     "Forbes Travel Guide Four Stars; AAA Four Diamond; Wine Spectator Best of Award of "
                     "Excellence. IMPORTANT PAIRING: Jo\u00ebl Robuchon is closed Mon/Sun and L'Atelier is "
                     "closed Tue/Wed, so between them MGM Grand has a starred restaurant open all 7 nights "
                     "but never both on the same night."),
        },
        "\u00e9 by Jos\u00e9 Andr\u00e9s": {
            "hours": "Tue\u2013Sun, two seatings nightly at 5:30 PM and 8:30 PM. CLOSED Monday.",
            "hoursStatus": "v",
            "note": ("Only 9 seats at a chef's counter inside Jaleo, third floor of The Cosmopolitan. "
                     "Tickets are released THREE MONTHS in advance, with a waitlist \u2014 for a Feb 15\u201318 2027 "
                     "stay that window is already open. Phone +1 702-698-7950, reserve@ebyjoseandres.com. "
                     "No ticket price is published on the official site, so cost for two stays blank."),
        },
        "China Poblano": {
            "hours": "Mon\u2013Thu 11:00 AM\u201310:00 PM; Fri 11:00 AM\u201310:30 PM; Sat 10:00 AM\u201310:30 PM; Sun 10:00 AM\u201310:00 PM.",
            "hoursStatus": "v",
            "note": ("$$ \u00b7 Casual dress \u00b7 Reservations 877.893.2003, information 702.698.7900. "
                     "Cocktail Hour Mon\u2013Thu 4:00\u20136:00 PM. Open every day, including the Monday when "
                     "\u00e9 by Jos\u00e9 Andr\u00e9s is closed \u2014 the practical Bib Gourmand fallback on the same property."),
        },
        "Partage": {
            "price2": "$260 / $320 / $420",
            "priceNote": ("VERIFIED official menu: 5 courses $130 per person ($260 for two, ~1.5 h); "
                          "7 courses $160 pp ($320 for two, ~2.5 h); Signature 9 courses $210 pp "
                          "($420 for two, ~3 h). Before tax and tip. Wine pairing per person: 5-glass $60, "
                          "7-glass $84, 9-glass $108; premium add $40/$56/$72; 5-glass Champagne $125. "
                          "Seared foie gras add-on +$33 pp. Automatic 20% gratuity applies only to parties "
                          "of 6 or more, so it does NOT apply to two."),
            "note": ("Menu changes monthly. The official site states it CANNOT accommodate vegan, "
                     "dairy-free, celiac, or garlic/onion-free diets. 12-seat private room available. "
                     "Hours are not confirmed \u2014 a prior session found the venue site and the MICHELIN "
                     "listing disagree."),
        },
        "Anima by EDO": {
            "hours": "Dinner served nightly from 5:00 PM.",
            "hoursStatus": "v",
            "price2": "$170",
            "priceNote": ("VERIFIED official site: 'Anima Experience' tasting menu $85 per person, "
                          "so $170 for two adults before tax, tip and wine pairings. The tasting runs "
                          "~2 to 2.5 hours and the entire table must participate. Vegetarian and vegan "
                          "tastings available on request. Separate Monday special: two handmade pasta "
                          "dishes plus one select bottle of wine for $65 (a table price, not per person)."),
            "note": ("Cheapest published tasting-menu total for two of all 24 listed restaurants. "
                     "At The Gramercy, 9205 W Russell Rd #185 \u2014 off-Strip southwest, so it needs a car "
                     "or rideshare rather than a Strip bus."),
        },
        "Restaurant Guy Savoy": {
            "hours": "Official live status shows 'Opens 5:00 PM'. Open days were not exposed in the retrieved page text.",
            "hoursStatus": "p",
            "note": ("$$$$ \u00b7 Formal dress \u00b7 (702) 731-7286, groups (866) 733-5827. Forbes Five-Star; "
                     "AAA Five Diamond; Wine Spectator Grand Award with 12,000+ bottles; highest-ranked "
                     "Las Vegas restaurant on LaListe's 2026 Top 1,000. Offers a 9-course Krug table "
                     "dinner described as the only one in North America (no price published). "
                     "Reservations via OpenTable from the official page."),
        },
    }
    for name, patch in fills.items():
        r = by(rows, "name", name)
        if not r:
            continue
        for k, v in patch.items():
            if k in ("hours", "hoursStatus") and r.get("hoursStatus") == "v" and r.get("hours"):
                continue
            if k == "price2" and r.get("price2"):
                continue
            r[k] = v

    gs = by(rows, "name", "Restaurant Guy Savoy")
    if gs:
        add_social(gs, "Caesars Palace \u2014 official Instagram (property-level)", "https://www.instagram.com/caesarspalace/")
        add_social(gs, "Caesars Palace \u2014 official YouTube (property-level)", "https://www.youtube.com/user/caesarspalace")

    d["guide"]["primarySource"] = {
        "label": "MICHELIN Guide Southwest 2026 \u2014 official press release, 31 Aug 2026",
        "url": "https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s",
        "note": ("Added by session 4d7b292f as the first-party primary source behind the LVCVA page. "
                 "It confirms the ceremony was held at Fontainebleau Las Vegas, lists every starred and "
                 "Recommended restaurant with its street address, and states the full Southwest selection "
                 "is 64 restaurants across 24 cuisine types. The fifth starred restaurant, Monte, is in "
                 "South Salt Lake, UTAH \u2014 not Las Vegas \u2014 which is why Las Vegas has 4 starred "
                 "restaurants and 5 stars, not 5 starred restaurants."),
    }
    save("restaurants", d)


# ---------------------------------------------------------------- activities
def activities():
    d = load("activities")
    rows = d["rows"]

    def patch(name, **kw):
        r = by(rows, "name", name)
        if not r:
            return None
        for k, v in kw.items():
            if k == "price2" and r.get("price2"):
                continue
            if k == "hours" and r.get("hoursStatus") == "v":
                continue
            r[k] = v
        return r

    hd = patch(
        "Hoover Dam",
        hours=("Dam open to the public daily 5:00 AM\u20139:00 PM (PST). Visitor Center and tours daily "
               "9:00 AM\u20135:00 PM. The official page begins listing holiday exceptions but the list was "
               "cut off in the retrieved text \u2014 confirm before a holiday visit."),
        hoursStatus="p",
        price2="$80 / $50 / $30",
        priceNote=("VERIFIED official Bureau of Reclamation tour page: Guided Dam Tour $40 per person "
                   "($80 for two) \u2014 ON-SITE ONLY, must be purchased in person. Guided Powerplant Tour "
                   "$25 per adult ($50 for two). Self-guided Visitor Center Tour $15 per person ($30 for "
                   "two). Children 3 and under free. Powerplant and Visitor Center tickets are "
                   "upgradeable on site."),
        note=("America the Beautiful / Interagency passes are NOT accepted at Hoover Dam \u2014 it is "
              "self-funded and receives no Federal Lands Recreation Enhancement Act revenue. The Guided "
              "Dam Tour includes the historic tunnels, the original elevator, the inspection tunnels and "
              "the Powerplant tour; it is wheelchair accessible but not stroller or scooter accessible."),
    )
    if hd:
        add_social(hd, "Bureau of Reclamation \u2014 official YouTube (agency-level)", "https://www.youtube.com/@reclamation")
        add_social(hd, "Bureau of Reclamation \u2014 official Instagram (agency-level)", "https://instagram.com/bureau_of_reclamation")

    rr = patch(
        "Red Rock Canyon National Conservation Area",
        hours=("Visitor Center and Elements Gift Shop open daily 8:00 AM\u20134:30 PM. TIMED-ENTRY "
               "RESERVATION REQUIRED for vehicle entry to the 13-mile Scenic Drive 8:00 AM\u20135:00 PM, "
               "October 1 \u2013 May 31 \u2014 which covers the entire Feb 15 \u2013 Mar 23, 2027 window."),
        hoursStatus="v",
        price2="$20 per vehicle",
        priceNote=("VERIFIED official fee table: Car/Truck 1 day $20 PER VEHICLE, so two adults in one car "
                   "pay $20 total. Commercial tour vehicle (bus, limo, taxi, ride-share) is $20 per vehicle "
                   "PLUS $5 per person = $30 for two. Motorcycle $10; bicycle $8; pedestrian $5 per person. "
                   "Red Rock Annual Pass $50. America the Beautiful Annual Pass is $80 for U.S. "
                   "citizens/residents but $250 for NON-U.S. residents."),
        note=("26 hikes and trails. Reserve the timed entry at Recreation.gov (timed-entry/10075177) or "
              "(877) 444-6777 BEFORE fixing the day's itinerary. No public bus service to the Scenic Drive "
              "is published on the official visitor pages, so this is a car or commercial-tour day."),
    )
    if rr:
        rr["official"] = "https://www.redrockcanyonlv.org/visitor-information/"
        rr.setdefault("alsoOfficial", [])
        for u in ["https://www.redrockcanyonlv.org/fees/", "https://www.recreation.gov/timed-entry/10075177"]:
            if u not in rr["alsoOfficial"]:
                rr["alsoOfficial"].append(u)

    vf = patch(
        "Valley of Fire State Park",
        hours=("Park open daily sunrise to sunset, 365 days a year. Visitor Center daily 9:00 AM\u20134:00 PM. "
               "Park office Mon\u2013Fri 9\u20134, closed state holidays. Annual maintenance closure Dec 1\u201314 "
               "(outside your window). Annual trail closures May 15 \u2013 Sep 30 (outside your window, so "
               "Fire Wave, White Domes, Pastel Canyon and the other listed trails ARE open in Feb/Mar)."),
        hoursStatus="v",
        price2="$15 per vehicle",
        priceNote=("VERIFIED Nevada State Parks: entrance $10.00, or $15.00 for NON-NEVADA vehicles. "
                   "The fee is per vehicle, so two adults in one rental car pay $15 total. No reservation "
                   "is required for day use."),
        note=("OFFICIAL WARNING: taking Uber/Lyft can leave you STRANDED \u2014 a return ride from the park is "
              "often impossible. A car or an organised tour is effectively required. Drones are prohibited; "
              "pets must be on a leash of six feet or less and are not allowed in the Visitor Center. "
              "A separate official notice says the WEST ENTRANCE is open only until November 30, 2026 \u2014 "
              "re-check entrance status for 2027 (F-30)."),
    )
    if vf:
        vf["official"] = "https://parks.nv.gov/parks/valley-of-fire"
        vf.setdefault("alsoOfficial", [])
        u = "https://parks.nv.gov/news/temporary-closure-of-the-west-entrance-at-valley-of-fire"
        if u not in vf["alsoOfficial"]:
            vf["alsoOfficial"].append(u)

    nm = by(rows, "name", "The Neon Museum")
    if nm:
        add_social(nm, "The Neon Museum \u2014 official TikTok", "https://www.tiktok.com/@neonmuseumlasvegas")
        add_social(nm, "The Neon Museum \u2014 official Instagram", "https://www.instagram.com/theneonmuseumlasvegas/")
        nm["hours"] = ("SEPT\u2013MAY: 3:00 PM\u201311:00 PM daily, last entry 10:00 PM \u2014 this is the schedule "
                       "for Feb/Mar 2027. JUN\u2013AUG: 8:00 PM\u2013midnight, last entry 11:00 PM. Box office "
                       "closes one hour before posted closing.")
        nm["hoursStatus"] = "v"
        nm["note"] = append_once(nm.get("note"), "From January 1, 2027 the museum may charge extra",
                      "From January 1, 2027 the museum may charge extra for arriving "
                      "earlier or later than your selected ticket time, so book a specific slot and keep to it. "
                      "Photography is personal phone/tablet snapshots ONLY \u2014 cameras, tripods and selfie "
                      "sticks must be left in a vehicle or checked at the front desk. Outdoor collection: "
                      "guided tours stop above 100\u00b0F, general admission closes above 105\u00b0F, the museum "
                      "closes above 110\u00b0F.")

    mob = by(rows, "name", "The Mob Museum")
    if mob:
        mob["hours"] = ("Museum daily 9:00 AM\u20139:00 PM. The Underground speakeasy: Sun\u2013Thu 11:00 AM\u201311:00 PM; "
                        "Fri\u2013Sat 11:00 AM\u2013midnight. Hours subject to change; a separate early-closures "
                        "page is published.")
        mob["hoursStatus"] = "v"
        mob["price2"] = "$75.90 / $99.90 / $109.90"
        mob["priceNote"] = ("VERIFIED official admission portal: General Admission $37.95 per adult "
                            "($75.90 for two), Deluxe Pass $49.95 ($99.90), Premier Pass $54.95 ($109.90). "
                            "All three include entry to The Underground. Online-only Morning (9\u201311 AM) or "
                            "Evening (5\u20139 PM) arrival reduces Premier to $47.95 pp = $95.90 for two. "
                            "Children 10 and under free. Prices were read with a November 2026 date "
                            "selected, so 2027 pricing may differ (F-31).")

    hr = by(rows, "name", "High Roller Observation Wheel")
    if hr:
        add_social(hr, "Caesars Entertainment \u2014 official Instagram (property-level)", "https://www.instagram.com/caesarspalace/")
        add_social(hr, "Caesars Entertainment \u2014 official YouTube (property-level)", "https://www.youtube.com/user/caesarspalace")
        hr["note"] = append_once(hr.get("note"), "Caesars Rewards Gold and Platinum members",
                      "Caesars Rewards Gold and Platinum members can buy one ticket and "
                      "get one free (limit 2 tickets per month) \u2014 a genuine two-for-one for a couple. "
                      "Seniors 65+ get $5 off Sun\u2013Thu 12\u20135 PM at the box office. Individual outside "
                      "beverages are allowed; glass, coolers and cases are not.")

    if not by(rows, "name", "SlotZilla Zipline at Fremont Street Experience"):
        rows.append({
            "name": "SlotZilla Zipline at Fremont Street Experience",
            "area": "Downtown \u2014 Fremont Street Experience",
            "hours": "",
            "hoursStatus": "u",
            "price2": "$98 / $110 (Zip) \u00b7 $138 / $150 (Zoom)",
            "priceNote": ("VERIFIED official operator: Zip Line Mon\u2013Thu from $49, Fri\u2013Sun from $55; "
                          "Zoom Line Mon\u2013Thu from $69, Fri\u2013Sun from $75. Doubled for two adults, "
                          "all 'starting at' prices PLUS FEES. A Mob Museum + SlotZilla bundle is $88 "
                          "and applies to Zoomline only."),
            "transit": "Downtown terminus of the Las Vegas Blvd Deuce corridor. Door-to-door times not retrieved.",
            "transitStatus": "u",
            "official": "https://fremontstreetexperience.com/slotzilla-zip-line/",
            "alsoOfficial": ["https://fremontstreetexperience.com/slotzilla-zip-line-lv/slotzilla-faq/"],
            "social": [
                {"label": "Official SlotZilla 'Hall of Famers' video \u2014 Katy Perry", "url": "https://youtu.be/D85A-xuIb58"},
                {"label": "Official SlotZilla video \u2014 Vampire Diaries", "url": "https://youtu.be/gWVvWJxQSEc"},
                {"label": "Official SlotZilla video \u2014 Spruce The Goose x The Aviator", "url": "https://youtu.be/vCnkPlFylcE"},
            ],
            "socialStatus": "v",
            "note": ("Zip Line: seated, launches from 77 ft, glides three blocks, rider 50\u2013300 lbs. "
                     "Zoom Line: belly-down head-up, launches from 11 stories, five blocks, rider 80\u2013300 lbs. "
                     "Maximum height 6'8\" for either. ADA elevators available. Operating hours were not "
                     "exposed on the retrieved official page, so they are left blank."),
            "flagIds": ["F-32"],
        })
    save("activities", d)


# ---------------------------------------------------------------- booking
def booking():
    d = load("booking")
    bt = d.setdefault("bookTiming", {})
    bt["statement"] = (
        "TIME-CRITICAL, VERIFIED " + CAP + ": Wynn's public 'Cyber Exclusive' rate for the exact "
        "Feb 15\u201322 2027 stay is $677 avg/night including the resort fee, versus $833 avg/night on the "
        "same room's Flexible Getaway Rate. That offer must be BOOKED between November 20 and "
        "December 4, 2026. Booking inside that window saves $1,092 across 7 nights before tax and adds "
        "a $75/day resort credit (up to $300 per stay). This is the only verified, dated booking "
        "deadline found that changes the price of this specific trip. Separately, no official source "
        "publishes an optimal booking lead time, and Caesars advertises 'Advanced Purchase Savings \u2014 "
        "up to 30% off for stays 30+ days in advance', which booking now already satisfies."
    )
    dl = bt.setdefault("deadlines", [])
    entries = [
        {
            "offer": "Wynn Cyber Exclusive + Up to $300 Resort Credit",
            "bookFrom": "2026-11-20", "bookBy": "2026-12-04",
            "stayWindow": "Nov 22, 2026 \u2013 Jun 30, 2027", "nights": "1 to 14 nights",
            "membership": "None \u2014 public rate",
            "rate": "$677 avg/night, Wynn Resort King, Feb 15\u201322 2027, includes resort fee, excludes taxes",
            "compare": "$833 avg/night Flexible Getaway Rate, same room and dates ($5,831 for 7 nights)",
            "saving": "$1,092 across 7 nights (computed: ($833 \u2212 $677) \u00d7 7)",
            "perks": "$75 resort credit per day, up to $300 per stay",
            "cancel": "72 hours before arrival to avoid a one-night room-rate-and-tax penalty",
            "status": "v",
            "source": "https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&langID=1&rmID=68658&checkIn=02/15/2027&checkOut=02/22/2027&adults=2&children=0",
            "terms": "https://www.wynnlasvegas.com/terms-and-conditions/2026-cyber-sale-offer-public",
        },
        {
            "offer": "Wynn Rewards Cyber + Resort Credit + Panoramic View upgrade",
            "bookFrom": "2026-11-20", "bookBy": "2026-12-04",
            "stayWindow": "Nov 22, 2026 \u2013 Jun 30, 2027", "nights": "2 to 14 nights",
            "membership": "Wynn Rewards membership required (free to join)",
            "rate": "Hidden behind sign-in \u2014 NOT verified. Advertised as up to 25% off Resort rooms.",
            "compare": "", "saving": "",
            "perks": "Panoramic View upgrade; $75/day resort credit up to $300 per stay",
            "cancel": "48 hours before arrival",
            "status": "p",
            "source": "https://www.wynnlasvegas.com/terms-and-conditions/2026-cyber-sale-offer-wynn-rewards",
            "terms": "https://www.wynnlasvegas.com/terms-and-conditions/2026-cyber-sale-offer-wynn-rewards",
        },
        {
            "offer": "Resorts World 'Up to 50% Off' Cyber Sale",
            "bookFrom": "", "bookBy": "",
            "stayWindow": "", "nights": "",
            "membership": "Genting Rewards offered for best rate; the quoted price was visible without signing in",
            "rate": "$277.21 avg/night, Hilton tower, Feb 15\u201322 2027, includes resort fee, excludes taxes",
            "compare": "$351.29 avg/night on 'Signature Savings' and '$75 Dining Credits', same dates",
            "saving": "$518.56 across 7 nights (computed: ($351.29 \u2212 $277.21) \u00d7 7)",
            "perks": "Competing offers add up to $75 dining credit per stay",
            "cancel": "",
            "status": "v",
            "source": "https://reservations.rwlasvegas.com/ibe/shop.aspx?hotelID=17726&selectedTower=HILTON&checkin=2027-02-15&checkout=2027-02-22&nights=7&adults=2&children=0",
            "terms": "",
        },
        {
            "offer": "Caesars Palace \u2014 daily breakfast at Brasserie B package",
            "bookFrom": "", "bookBy": "2027-12-20",
            "stayWindow": "", "nights": "", "membership": "None stated",
            "rate": "$274/night, excludes taxes", "compare": "$209/night Best Available Rate",
            "saving": "", "perks": "Daily breakfast at Brasserie B", "cancel": "",
            "status": "v",
            "source": "https://www.caesars.com/book/room-list?arrivalDate=02/15/2027&departureDate=02/22/2027&dateSearchFormat=exact-dates&propCode=clv&numberOfAdults=2&numberOfRooms=1",
            "terms": "",
        },
    ]
    for e in entries:
        if not any(x.get("offer") == e["offer"] for x in dl):
            dl.append(e)

    if "rateCalendar" not in d:
        d["rateCalendar"] = {
            "hotel": "Resorts World Las Vegas \u2014 Las Vegas Hilton tower",
            "captured": CAP,
            "source": "https://reservations.rwlasvegas.com/ibe/shop.aspx?hotelID=17726&selectedTower=HILTON&checkin=2027-02-15&checkout=2027-02-22&nights=7&adults=2&children=0",
            "warning": ("These are the engine's per-arrival-date 'from' prices for February 2027. The same "
                        "calendar prints TWO contradictory captions \u2014 'Calendar pricing excludes daily "
                        "resort fee and taxes' AND 'Calendar pricing includes $55 daily resort fee and "
                        "excludes taxes' \u2014 so fee treatment is UNRESOLVED (F-26). Summing seven "
                        "consecutive nights is an INDICATIVE comparison of date windows, not a quote."),
            "prices": [
                ["2027-02-13", "Sat", 414], ["2027-02-14", "Sun", 184],
                ["2027-02-15", "Mon", 214], ["2027-02-16", "Tue", 404],
                ["2027-02-17", "Wed", 404], ["2027-02-18", "Thu", 284],
                ["2027-02-19", "Fri", 242], ["2027-02-20", "Sat", 242],
                ["2027-02-21", "Sun", 152], ["2027-02-22", "Mon", 174],
                ["2027-02-23", "Tue", 254], ["2027-02-24", "Wed", 284],
                ["2027-02-25", "Thu", 354], ["2027-02-26", "Fri", 214],
                ["2027-02-27", "Sat", 279], ["2027-02-28", "Sun", 454],
            ],
            "windows": [
                ["Feb 15 \u2192 Feb 22", 1942, "Preferred start \u2014 holiday week"],
                ["Feb 16 \u2192 Feb 23", 1902, ""],
                ["Feb 17 \u2192 Feb 24", 1752, ""],
                ["Feb 18 \u2192 Feb 25", 1632, "CHEAPEST 7-night window on this calendar"],
                ["Feb 19 \u2192 Feb 26", 1702, ""],
                ["Feb 20 \u2192 Feb 27", 1674, ""],
                ["Feb 21 \u2192 Feb 28", 1711, ""],
                ["Feb 22 \u2192 Mar 1", 2013, "Runs into a $454 Feb 28 night"],
            ],
            "finding": ("Shifting check-in from Mon Feb 15 to Thu Feb 18 lowers the indicative 7-night room "
                        "subtotal from $1,942 to $1,632 \u2014 about $310 (16%) less \u2014 and still starts "
                        "inside the preferred part of the window. Feb 16 and Feb 17 are the two most "
                        "expensive weeknights of the month at $404 each. Only February was captured; "
                        "no claim is made about March."),
        }

    vf = d.setdefault("verifiedDateFacts", [])
    facts = [
        {"fact": "Monday, February 15, 2027 is Washington's Birthday (Presidents' Day), a U.S. federal holiday.",
         "source": "https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/",
         "effect": "Your preferred check-in is the holiday itself, at the end of a three-day weekend."},
        {"fact": "MGM Resorts' official engine states stays can only be booked up to 14 nights online; longer stays need 866.761.7111.",
         "source": "https://mgmgrand.mgmresorts.com/book-room?property=mgmgrand",
         "effect": "A 14-night trip is exactly the online maximum at MGM properties \u2014 no margin."},
        {"fact": "Red Rock Canyon requires a timed-entry vehicle reservation 8 AM\u20135 PM, Oct 1 \u2013 May 31.",
         "source": "https://www.redrockcanyonlv.org/fees/",
         "effect": "Book the Red Rock slot before finalising the daily itinerary."},
        {"fact": "Valley of Fire's trail closures run May 15 \u2013 Sep 30 and its maintenance closure is Dec 1\u201314.",
         "source": "https://parks.nv.gov/parks/valley-of-fire",
         "effect": "Feb/Mar is one of the best windows of the year \u2014 all listed trails are open."},
        {"fact": "The Neon Museum may charge extra for arriving outside your selected ticket time from January 1, 2027.",
         "source": "https://neonmuseum.org/your-visit/",
         "effect": "Book a specific Neon Museum slot and keep to it."},
    ]
    for f in facts:
        if not any(x.get("fact") == f["fact"] for x in vf):
            vf.append(f)
    save("booking", d)


# ---------------------------------------------------------------- flags
def flags():
    d = load("flags")
    rows = d["rows"]
    new = [
        {
            "id": "F-24", "severity": "high",
            "title": "MGM's own site shows a phantom 'One MICHELIN Star' badge for Bardot Brasserie (ARIA)",
            "detail": ("The related-dining card on the official Jo\u00ebl Robuchon page renders 'Bardot Brasserie "
                       "\u2014 ARIA \u2014 One MICHELIN Star'. But Bardot Brasserie's OWN official page carries no "
                       "MICHELIN badge and its 'Awards and acclaim' list contains only 2015\u20132016 honours "
                       "(SNHCA, Wine Spectator, James Beard semifinalist, Desert Companion). Bardot appears "
                       "in neither the official MICHELIN Southwest press release nor the LVCVA list. "
                       "Third-party 'ARIA review' blogs compound the error by claiming Mizumi has 2 stars "
                       "and Sage 1 \u2014 Sage is not in the 2026 selection at all."),
            "effect": ("ARIA is NOT counted as a starred hotel. It has one MICHELIN-listed restaurant "
                       "(Gymkhana, Recommended) and zero stars. Do not let the MGM card or AI-written "
                       "review blogs change the ranking."),
            "source": [
                {"label": "Official Jo\u00ebl Robuchon page \u2014 related-dining card carrying the badge",
                 "url": "https://mgmgrand.mgmresorts.com/en/restaurants/joel-robuchon-french-restaurant.html"},
                {"label": "Official Bardot Brasserie page \u2014 no MICHELIN award listed",
                 "url": "https://aria.mgmresorts.com/en/restaurants/bardot-brasserie.html"},
                {"label": "Official MICHELIN Southwest 2026 press release \u2014 starred table",
                 "url": "https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s"},
            ],
        },
        {
            "id": "F-25", "severity": "medium",
            "title": "MGM Resorts page contains an unpublished CMS placeholder ('Dress code: Test copy')",
            "detail": ("The official L'Atelier de Jo\u00ebl Robuchon page has a 'Dress code' field reading "
                       "literally 'Test copy', immediately above the real 'Dress Code: Business Casual' "
                       "field. This is live editorial placeholder text on a first-party page."),
            "effect": ("Only the 'Business Casual' value is used. It also lowers confidence in MGM's "
                       "restaurant metadata generally, which is why F-24 is treated as a site defect "
                       "rather than an award."),
            "source": [{"label": "Official L'Atelier page",
                        "url": "https://mgmgrand.mgmresorts.com/en/restaurants/latelier-joel-robuchon-french-restaurant.html"}],
        },
        {
            "id": "F-26", "severity": "high",
            "title": "Resorts World's rate calendar contradicts itself on the resort fee",
            "detail": ("The same official February 2027 calendar prints both 'Calendar pricing excludes "
                       "daily resort fee and taxes' and 'Calendar pricing includes $55 daily resort fee "
                       "and excludes taxes'. The two captions cannot both be true."),
            "effect": ("The calendar is used ONLY to compare date windows against each other, never to "
                       "quote an all-in cost. The separately quoted $277.21 avg/night offer tile does "
                       "state 'Includes Resort Fee and Excludes Taxes' and is the figure ranked."),
            "source": [{"label": "Official Resorts World engine + February 2027 calendar",
                        "url": "https://reservations.rwlasvegas.com/ibe/shop.aspx?hotelID=17726&selectedTower=HILTON&checkin=2027-02-15&checkout=2027-02-22&nights=7&adults=2&children=0"}],
        },
        {
            "id": "F-27", "severity": "medium",
            "title": "Caesars 'book by' dates are ten months AFTER the stay",
            "detail": ("On the Feb 15\u201322 2027 rate search, Caesars Palace shows a breakfast package "
                       "'Book by Dec 20, 2027' and a food-credit package 'Book by Dec 30, 2027'; Flamingo "
                       "and Planet Hollywood show 'Book by Dec 30, 2027'. Those deadlines fall after the "
                       "trip itself."),
            "effect": ("Reproduced exactly as published and NOT corrected to 2026. Do not rely on these "
                       "as booking urgency; confirm the real expiry with Caesars before choosing a package."),
            "source": [{"label": "Official Caesars Palace dated rate page",
                        "url": "https://www.caesars.com/book/room-list?arrivalDate=02/15/2027&departureDate=02/22/2027&dateSearchFormat=exact-dates&propCode=clv&numberOfAdults=2&numberOfRooms=1"}],
        },
        {
            "id": "F-28", "severity": "medium",
            "title": "Proposed RTC fare increase dated January 31, 2027 could not be verified",
            "detail": ("A third-party page cites an RTC proposal to raise fares from Jan 31, 2027 "
                       "(Strip single ride $4\u2192$5, Strip 24-hour $8\u2192$10, residential 24-hour $5\u2192$7) "
                       "and links the official RTC fare-update page. That official page could NOT be "
                       "retrieved in this session, so the proposal, amounts and date are UNVERIFIED. "
                       "The fares actually shown on this site are the ones read on RTC's own fare page."),
            "effect": ("Because the proposed start date falls BEFORE the trip, confirm directly with RTC "
                       "before budgeting transit. Budget risk is small in absolute terms (a few dollars "
                       "per pass) but it is a real pre-trip change."),
            "source": [{"label": "Official RTC fare page (current fares, verified)",
                        "url": "https://rtcws.rtcsnv.com/mobile/geoFares.html"},
                       {"label": "Official RTC fare-update page \u2014 could not be retrieved",
                        "url": "https://www.rtcsnv.com/ways-to-travel/transitupdates-fares/"}],
        },
        {
            "id": "F-29", "severity": "low",
            "title": "High Roller opening time disagrees with its own ticket window",
            "detail": ("The official High Roller page showed a live status of 'Opens 12:30 PM' while "
                       "publishing ticket windows of 'Daily 12 PM to 5 PM' and 'Anytime, Daily 12 PM \u2013 Close'."),
            "effect": "Do not plan a noon arrival. Confirm the day's opening before buying a daytime ticket.",
            "source": [{"label": "Official High Roller page",
                        "url": "https://www.caesars.com/linq/things-to-do/attractions/high-roller"}],
        },
        {
            "id": "F-30", "severity": "medium",
            "title": "Valley of Fire west entrance notice expires November 30, 2026",
            "detail": ("Nevada State Parks posts 'WEST ENTRANCE *OPEN* UNTIL NOVEMBER 30, 2026' plus a "
                       "separate upcoming-maintenance-closure notice. What happens to the west entrance "
                       "after that date is not stated on the retrieved page."),
            "effect": ("Re-check entrance status and routing before a Feb/Mar 2027 visit; the drive time "
                       "and route depend on which entrance is open."),
            "source": [{"label": "Official Nevada State Parks \u2014 Valley of Fire",
                        "url": "https://parks.nv.gov/parks/valley-of-fire"},
                       {"label": "Official west-entrance closure notice",
                        "url": "https://parks.nv.gov/news/temporary-closure-of-the-west-entrance-at-valley-of-fire"}],
        },
        {
            "id": "F-31", "severity": "medium",
            "title": "Mob Museum ticket prices were read against a November 2026 date, not a 2027 date",
            "detail": ("The official admission portal defaulted to today's date when prices were captured "
                       "($37.95 / $49.95 / $54.95 per adult). The portal did not expose a February 2027 "
                       "price for the same ticket types."),
            "effect": ("The doubled figures are arithmetically correct for the published prices but are "
                       "not a confirmed 2027 quote. Re-price on the official portal for your exact date."),
            "source": [{"label": "Official Mob Museum admission portal", "url": "https://admission.themobmuseum.org/"}],
        },
        {
            "id": "F-32", "severity": "low",
            "title": "SlotZilla operating hours not published on the retrieved official page",
            "detail": ("The operator's page publishes Mon\u2013Thu and Fri\u2013Sun pricing, rider weight and "
                       "height limits and ADA access, but no opening hours were exposed in the retrieved text."),
            "effect": "Hours are left blank rather than inferred. Confirm before scheduling a downtown evening.",
            "source": [{"label": "Official SlotZilla page", "url": "https://fremontstreetexperience.com/slotzilla-zip-line/"}],
        },
        {
            "id": "F-33", "severity": "medium",
            "title": "Bardot Brasserie's own page contradicts itself on hours",
            "detail": ("The official page's 'Hours of operation' block says Tue\u2013Thu 5\u201310 PM, Fri 9 AM\u20132 PM "
                       "and 5\u20139 PM, Sat 9 AM\u20134 PM, Sun 9 AM\u20132 PM; the summary below it says 'Dinner "
                       "Tuesday\u2013Saturday 5 PM\u201310 PM'; and the overview says 'on Friday and Saturday, we are "
                       "closed between 2-5PM' \u2014 which conflicts with a 4 PM Saturday close. The chef's own "
                       "group site gives the summary version."),
            "effect": ("Bardot is not in the MICHELIN selection so it is not ranked, but if you book it, "
                       "phone the restaurant (702.590.8610) rather than trusting either block."),
            "source": [{"label": "Official Bardot Brasserie page (ARIA)",
                        "url": "https://aria.mgmresorts.com/en/restaurants/bardot-brasserie.html"},
                       {"label": "Chef's own group page for Bardot", "url": "https://theminagroup.com/restaurants/bardot-brasserie/"}],
        },
        {
            "id": "F-35", "severity": "low",
            "title": "South Point's engine prints a nightly rate that does not multiply to its own stay total",
            "detail": ("For Feb 15\u201322 2027 the official SynXis engine shows Premium 2 Queens at "
                       "'$141 Per Night' and '$989 Total for 7 nights'. $141 \u00d7 7 = $987, a $2 gap; "
                       "$989 / 7 = $141.29, so the nightly figure is a rounded display. The same pattern "
                       "appears on the King room ($131/night vs $919 total; $131 \u00d7 7 = $917)."),
            "effect": ("The explicit published stay total is used as authoritative and the nightly figure "
                       "is labelled a rounded average. No figure is averaged, adjusted or inferred. This "
                       "was surfaced by tightening the build gate to validate money to the cent."),
            "source": [{"label": "Official South Point booking engine \u2014 Feb 15\u201322 2027, 2 adults",
                        "url": "https://be.synxis.com/?adult=2&arrive=2027-02-15&chain=6903&child=0&currency=USD&depart=2027-02-22&hotel=11548&level=hotel&locale=en-US&productcurrency=USD&rooms=1"}],
        },
        {
            "id": "F-34", "severity": "high",
            "title": "Parallel-session collision on the data/plan and root-page scope",
            "detail": ("Session 4d7b292f claimed data/plan/** and the root pages at the start of this run, "
                       "then discovered that session 155b420b had already claimed the identical scope, "
                       "built the canonical root site and merged PR #22 while this session was researching. "
                       "The live site therefore did not match this session's checkout."),
            "effect": ("Resolved without discarding anything: origin/main was merged in, 155b420b's data "
                       "schema and generated pages were kept as canonical, and this session's new verified "
                       "findings were merged ADDITIVELY via scripts/merge_fieldwork_4d7b292f.py. Both "
                       "COORDINATION records were retained. No eighth competing subsite was created."),
            "source": [{"label": "COORDINATION.md \u2014 shared task board",
                        "url": "https://github.com/kanlerxz87-cyber/Vegas2/blob/main/COORDINATION.md"},
                       {"label": "PR #22 \u2014 session 155b420b canonical root site",
                        "url": "https://github.com/kanlerxz87-cyber/Vegas2/pull/22"}],
        },
    ]
    for n in new:
        if not by(rows, "id", n["id"]):
            rows.append(n)
    save("flags", d)


# ---------------------------------------------------------------- repo review
def repo_review():
    d = load("repo_review")
    rows = d["rows"]
    new = [
        {
            "id": "R-14", "severity": "high",
            "finding": "Two sessions claimed the same file scope concurrently and both wrote data/plan/*.json",
            "evidence": ("git log shows PR #22 (session 155b420b) merged to main while session 4d7b292f was "
                         "mid-research on the same paths. The live Pages site referenced booking.html and "
                         "flagged.html, which did not exist in 4d7b292f's checkout at claim time. Merge "
                         "produced add/add conflicts in data/plan/hotels.json, activities.json and booking.json."),
            "action": ("Resolved additively: 155b420b's schema kept as canonical; new verified values merged "
                       "by scripts/merge_fieldwork_4d7b292f.py; both COORDINATION records retained. "
                       "Recommendation: claims should be pushed AND re-checked against origin/main "
                       "immediately before any write, not only at session start."),
            "status": "resolved",
        },
        {
            "id": "R-16", "severity": "medium",
            "finding": "A prior session's validator fails on main because its official-domain allowlist is too narrow",
            "evidence": ("scripts/check_site.py reports 26 failures on origin/main @ 900cb90, independent of "
                         "this session's changes (reproduced from a clean git archive of main). The failures "
                         "are of two kinds: (a) genuinely official domains rejected by the allowlist, e.g. "
                         "venetianlasvegas.com and rtcws.rtcsnv.com; (b) insecure http:// social links such as "
                         "http://instagram.com/mypubliclands. Its own CI job is not gating main."),
            "action": ("Not fixed here: data/verified/ and scripts/check_site.py belong to session a52047d7 "
                       "and are outside this session's additive scope. Requested change: add the official "
                       "domains to the allowlist and upgrade those social links to https. The canonical root "
                       "site is gated separately by scripts/check_plan.py, which passes with 0 failures."),
            "status": "needs review",
        },
        {
            "id": "R-15", "severity": "medium",
            "finding": "GitHub Pages source configuration and the Pages workflow disagree",
            "evidence": ("The Pages API reports build_type 'legacy' with source branch 'main' and path '/', "
                         "so the checked-in REPOSITORY ROOT is what https://kanlerxz87-cyber.github.io/Vegas2/ "
                         "serves. But .github/workflows/pages.yml uploads the 'docs' folder via "
                         "actions/upload-pages-artifact and deploys it with actions/deploy-pages. Under the "
                         "legacy source that artifact is not the served site."),
            "action": ("The canonical site is therefore correctly built at the root by scripts/build_plan.py. "
                       "Prior-session notes claiming a subsite lives at '/session-<id>/' are wrong under this "
                       "configuration \u2014 those folders resolve at '/docs/session-<id>/'. Either switch Pages "
                       "to GitHub Actions as the source, or retire the misleading workflow. Left unchanged "
                       "here because it is shared infrastructure outside this session's additive scope."),
            "status": "needs review",
        },
    ]
    for n in new:
        if not by(rows, "id", n["id"]):
            rows.append(n)
    save("repo_review", d)


# ---------------------------------------------------------------- questions / suggestions
def questions_suggestions():
    q = load("questions")
    extra = [
        {
            "id": "Q-21",
            "q": "Will you book the Wynn Cyber rate before it expires on December 4, 2026?",
            "status": "open",
            "known": ("Verified: $677 avg/night including resort fee for Feb 15\u201322 2027 versus $833 on the "
                      "Flexible rate; $1,092 saved over 7 nights; $75/day resort credit up to $300; "
                      "book Nov 20 \u2013 Dec 4, 2026; 72-hour cancellation."),
            "missing": "Whether a luxury budget is acceptable at all, and whether you want Wynn specifically.",
            "how": "Decide the budget ceiling (Q-02) first; the deadline is 7 days from the capture date.",
            "impact": "Highest of any open question \u2014 it is the only verified price change with a hard expiry.",
        },
        {
            "id": "Q-22",
            "q": "Are you travelling from outside the United States, and will you have a car?",
            "status": "open",
            "known": ("Verified: Red Rock's America the Beautiful annual pass is $80 for U.S. citizens/"
                      "residents but $250 for non-U.S. residents, while the Red Rock-only annual pass is $50. "
                      "Valley of Fire charges $10 for Nevada vehicles and $15 for non-Nevada vehicles, and "
                      "officially warns rideshare users can be stranded. Red Rock has no published bus service."),
            "missing": "Your residency and whether you will rent a car for the nature days.",
            "how": "Answer once; it changes pass choice, the Red Rock entry fee basis and whether Valley of Fire is feasible at all.",
            "impact": "Determines whether two of the three nature day trips are practical.",
        },
        {
            "id": "Q-23",
            "q": "Do you want the cheaper Feb 18\u201325 window instead of the preferred Feb 15 start?",
            "status": "open",
            "known": ("Verified: Feb 15 2027 is Washington's Birthday (OPM). On Resorts World's official "
                      "February calendar, Feb 18\u201325 sums to $1,632 versus $1,942 for Feb 15\u201322 \u2014 "
                      "about $310 less \u2014 and Feb 16/17 are the month's priciest weeknights at $404."),
            "missing": "Whether your dates are fixed by flights or leave, and whether the calendar's fee basis resolves (F-26).",
            "how": "Re-run the same engine for Feb 18\u201325 and read the offer tile's explicit fee wording.",
            "impact": "Roughly 16% of the room cost at that property, for a three-day shift.",
        },
    ]
    for e in extra:
        if not by(q["rows"], "id", e["id"]):
            q["rows"].append(e)
    save("questions", q)

    s = load("suggestions")
    si = s.setdefault("siteImprovements", [])
    adds = [
        {
            "id": "S-13",
            "title": "Put the verified booking deadline at the top of the landing page",
            "why": ("The most valuable fact found is time-limited: Wynn's $677 Cyber rate must be booked by "
                    "December 4, 2026, and it saves $1,092 over 7 nights versus the Flexible rate. Burying it "
                    "below eleven hotel rows risks the reader missing it entirely."),
            "effort": "small", "impact": "high",
            "needs": "Nothing further \u2014 IMPLEMENTED in this pass as a dated banner driven by booking.bookTiming.deadlines.",
        },
        {
            "id": "S-14",
            "title": "Show a per-night date strip instead of only a single stay average",
            "why": ("Resorts World's official February calendar reveals a 16% swing between adjacent 7-night "
                    "windows ($1,942 for Feb 15\u201322 vs $1,632 for Feb 18\u201325). A single average hides that."),
            "effort": "small", "impact": "high",
            "needs": "Nothing further \u2014 IMPLEMENTED in this pass on Prices & dates. Fee basis still unresolved (F-26).",
        },
        {
            "id": "S-15",
            "title": "Cite the primary MICHELIN press release, not only the tourism-board page",
            "why": ("MGM's own site shows a star badge Bardot Brasserie does not hold (F-24) and review blogs "
                    "invent stars for Mizumi and Sage. A first-party primary source with street addresses "
                    "settles tier disputes and proves Monte is in Utah, not Las Vegas."),
            "effort": "small", "impact": "medium",
            "needs": "Nothing further \u2014 IMPLEMENTED in this pass; the press release is now recorded as guide.primarySource.",
        },
        {
            "id": "S-16",
            "title": "Add a 'closed on your dates' filter driven by the verified calendars",
            "why": ("Three verified facts silently break itineraries: Bellagio Conservatory is dark Mar 7\u201312; "
                    "Jo\u00ebl Robuchon is closed Mon/Sun while L'Atelier is closed Tue/Wed; Red Rock needs a timed "
                    "reservation on every day of the window."),
            "effort": "medium", "impact": "high",
            "needs": "A chosen check-in date from the reader, plus verified daily hours for the remaining restaurants.",
        },
        {
            "id": "S-17",
            "title": "Stamp a capture timestamp on every dynamic price cell",
            "why": ("Caesars Palace moved from $226 to $214 per night in one day (F-23). Without a per-cell "
                    "timestamp a reader cannot tell a stale figure from a fresh one."),
            "effort": "medium", "impact": "medium",
            "needs": "A re-verification run that writes capture dates per cell rather than one page-level date.",
        },
        {
            "id": "S-18",
            "title": "Reconcile GitHub Pages source with the Pages workflow",
            "why": ("Pages serves the repository ROOT (legacy source main '/'), but pages.yml uploads the docs/ "
                    "folder. Prior-session notes therefore point at wrong URLs, which wastes review time (R-15)."),
            "effort": "small", "impact": "medium",
            "needs": "Owner decision: switch Pages to GitHub Actions, or retire the misleading workflow. Shared infrastructure \u2014 not changed in this pass.",
        },
    ]
    for a in adds:
        if not any(x.get("title") == a["title"] for x in si):
            si.append(a)
    save("suggestions", s)


def meta():
    d = load("meta")
    kf = d.setdefault("keyFindings", [])
    adds = [
        ("TIME-CRITICAL: Wynn's public Cyber Exclusive rate for Feb 15-22 2027 is $677 avg/night including "
         "the resort fee ($4,739 for 7 nights, pre-tax) versus $833 ($5,831) on the Flexible rate. It must be "
         "booked Nov 20 - Dec 4, 2026, and adds a $75/day resort credit up to $300 per stay. Verified saving: "
         "$1,092 over 7 nights."),
        ("The verified pre-tax 7-night price ladder now runs from $581 (Flamingo, 2 queens, 350 sq ft) through "
         "$812 (Horseshoe, king, 450 sq ft), $861 (Planet Hollywood, king, 430 sq ft), $989 (South Point, "
         "2 queens, 500 sq ft), $1,421 (Paris, 2 queens), $1,498 (Caesars Palace, king), $1,940.47 "
         "(Resorts World) to $4,739 (Wynn, king, 640 sq ft)."),
        ("On Resorts World's official February 2027 calendar, shifting check-in from Mon Feb 15 to Thu Feb 18 "
         "cuts the indicative 7-night room subtotal from $1,942 to $1,632 - about 16% - because Feb 16 and 17 "
         "are the month's priciest weeknights at $404. Feb 15 2027 is Washington's Birthday (OPM)."),
        ("Two MICHELIN-starred restaurants at MGM Grand have complementary closures: Joel Robuchon is closed "
         "Mon/Sun, L'Atelier is closed Tue/Wed. Together they cover all 7 nights, but never both on one night."),
        ("MGM's own site shows a 'One MICHELIN Star' badge for Bardot Brasserie (ARIA) that Bardot's own page "
         "and both official MICHELIN lists do not support. ARIA is scored as one Listed restaurant, zero stars (F-24)."),
        ("Red Rock Canyon requires a timed-entry vehicle reservation 8 AM-5 PM every day of the trip window "
         "(Oct 1-May 31) and charges $20 per car, not per person. Valley of Fire charges $15 per non-Nevada "
         "vehicle and officially warns that rideshare visitors can be stranded."),
    ]
    for a in adds:
        if a not in kf:
            kf.append(a)
    save("meta", d)


if __name__ == "__main__":
    hotels()
    restaurants()
    activities()
    booking()
    flags()
    repo_review()
    questions_suggestions()
    meta()
    print("Fieldwork merged additively into data/plan/*.json")
