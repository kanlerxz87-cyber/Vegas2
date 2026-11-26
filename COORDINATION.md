# Coordination board — Las Vegas trip-planning site

**Last updated:** 2026-11-26  
**Current branch:** `arena/b29fc34e-vegas2` (active; based on `main` at `c97c82a`)  
**Owner:** this session

## Active work

| Task | Status | Owner/session | File scope | Notes |
|---|---|---|---|---|
| End-to-end planning research, evidence-backed static site, verification, and GitHub Pages integration | in progress | `arena/b29fc34e-vegas2` | `COORDINATION.md`, `README.md`, `index.html`, `*.html`, `assets/*`, `data/*`, `.github/workflows/*` | Single active session observed; keep all work on this branch. No separate task branches. |

## Handoff / coordination log

- 2026-11-26 — Initial repository contained only an 8-byte `README.md`; created this board, claimed the end-to-end scope, committed `dca2d1d` (`docs: claim Las Vegas trip planning site task`), and pushed the current branch. No other session claims were present.
- 2026-11-26 — Official-source research now covers a verified South Point date quote, comparative room specifications, RTC/Monorail service, Bellagio seasonal attractions, Michelin distinctions, restaurant menus/hours, and activity hours/prices. No site files have been created yet. Next: finish rate/date sampling and journey-time verification, build the static multi-page site, run local checks, then open/merge a PR and verify Pages deployment.

## Working requirements

- Two adults; private bathroom; queen bed or larger. Planning window Feb 15–Mar 23, 2027; Feb 15–18 preferred. Show seven-night price, exact stay dates, room type, fees/taxes inclusion, and booking/source link. Never substitute estimates for official quotes. Leave unavailable/unverified rate cells blank and flag them.
- Restaurant meal budgets are for two people and are menu-based only where current official prices are available. Clearly distinguish MICHELIN Stars, Bib Gourmand, and Guide Recommended/Selected. Don't conflate a chef's star with a restaurant distinction.
- Link every data table row to an official venue/source page. Add official social accounts when identified from a venue/MICHELIN page; don't guess handles. Identify schedules as current checks, not guarantees for 2027.
- Include landing/summary, category pages, public-transit details only when timed and supported, decision questions, ways to resolve unknowns, recommendations, and a clearly labeled Flagged for Review page.

## Verification / source log

All rates and operating details below are official first-party pages or booking engine outputs unless explicitly identified as Michelin Guide entries. Snapshots were checked on 2026-11-26; schedules and prices can change before travel.

### Hotels and room fit

- South Point room specifications: [Premium rooms](https://southpointcasino.com/hotel/guest-rooms) — Premium King and Premium Two Queen rooms are 500 sq. ft.; two queens sleep four. Fits the stated bed/occupancy needs; verify private-bathroom details on the booking page before booking.
- South Point [official rate calendar](https://southpointcasino.com/hotel/room-rate-calendar) — rates include the daily resort fee and exclude tax.
- South Point [two-adult booking engine, Feb 15–22, 2027, 7 nights](https://be.synxis.com/?chain=6903&hotel=11548&arrive=02%2F15%2F2027&nights=7&adult=2&child=0&rooms=1): Premium King Non-Smoking **$919**; Premium 2 Queens Non-Smoking **$989**. Booking page states $29.20/day resort fee included in prevailing rate; tax excluded; deposit required.
- South Point [Feb 22–Mar 1, 2027, 7 nights](https://be.synxis.com/?chain=6903&hotel=11548&arrive=02%2F22%2F2027&nights=7&adult=2&child=0&rooms=1): King **$979**; 2 Queens **$1,049**.
- South Point [preferred Feb 15–18, 2027, 3 nights](https://be.synxis.com/?chain=6903&hotel=11548&arrive=02%2F15%2F2027&nights=3&adult=2&child=0&rooms=1): King **$313**; 2 Queens **$343**. Not a 7-night quote.
- South Point sampled additional March check-in dates (Mar 1, 8, 15, 16) returned unavailable/mismatched availability notices. No cheapest-in-window claim is supported yet.
- Official comparator room pages: [MGM Grand Two Queen](https://mgmgrand.mgmresorts.com/en/hotel/mgm-two-queen.html) — 446 sq. ft.; [Cosmopolitan City Room](https://cosmopolitanlasvegas.mgmresorts.com/en/hotel/city-room.html) — 460 sq. ft., two queens; [Venetian Luxury Two Queen Suite](https://www.venetianlasvegas.com/hotel/the-venetian/luxury-two-queen-suite.html) — 750 sq. ft., bathroom 130 sq. ft.; [Caesars Palace hotel](https://www.caesars.com/caesars-palace/hotel) — Colosseum Strip View two-queen 475 sq. ft. No verified comparative date-specific rates yet.

### Transit and attractions

- RTC official [schedules/maps](https://www.rtcsnv.com/ways-to-travel/schedules-maps/); [Route 117 timetable](https://rtcws.rtcsnv.com/routepdf/117.pdf); [Deuce timetable](https://rtcws.rtcsnv.com/routepdf/deuce.pdf). Current schedules posted Aug. 23, 2026. South Point connects on Route 117 to SSTT; Deuce serves the Strip from SSTT. Door-to-door journey time still needs to be computed from actual dated trips; do not describe as a verified under-one-hour connection until done.
- Official [Las Vegas Monorail](https://www.lvmonorail.com/) — seven stations; 4–8 minute frequency; Mon 7 a.m.–midnight, Tue–Thu to 2 a.m., Fri–Sun to 3 a.m. It does not serve South Point.
- [Bellagio Fountains](https://bellagio.mgmresorts.com/en/entertainment/fountains-of-bellagio.html) — free; Mon–Fri every 30 minutes 3–7:30 p.m., every 15 minutes 8 p.m.–midnight; Sat/Sun/holidays from noon; weather/schedule exceptions.
- [Bellagio Conservatory](https://bellagio.mgmresorts.com/en/entertainment/conservatory-botanical-garden.html) — 2027 Lunar New Year display Jan. 9–Mar. 6; dark Mar. 7–12; Spring display Mar. 13–May 15. Dates subject to change.
- [Neon Museum tickets/experiences](https://neonmuseum.org/tickets-and-experiences/) — 2027 admission listing daily 3–11 p.m. from $21; advance booking advised.
- [AREA15 / Omega Mart](https://www.area15.com/experiences/meow-wolf) — official page lists daily 10 a.m.–11 p.m.; visit duration around 120 minutes.
- [Fremont Street Experience](https://vegasexperience.com/) — free nightly entertainment on three stages; specific Feb–Mar 2027 lineup not published/verified.
- [High Roller](https://www.caesars.com/linq/things-to-do/attractions/high-roller) — 30-minute ride; official FAQ adult prices $23.50 daytime / $34.75 anytime before tax/fees.
- [KÀ](https://mgmgrand.mgmresorts.com/en/entertainment/ka-cirque-du-soleil-show.html) — schedule lists Mon–Wed 6/8:30 p.m., Sat/Sun 4:30/7 p.m.; dark Thu/Fri and posted special dates; from $69 before tax.

### MICHELIN and dining

- [Visit Las Vegas Michelin overview](https://www.visitlasvegas.com/michelin-guide-restaurants/) reports 24 Las Vegas distinctions in the 2026 Southwest Guide. Use the individual [MICHELIN Guide entry](https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/restaurant-de-joel-robuchon) (not chef biography or an aggregator) to substantiate each restaurant's current distinction. Verified individual star pages include [Joel Robuchon (Two Stars)](https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/restaurant-de-joel-robuchon), [L'Atelier](https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/l-atelier-de-joel-robuchon-las-vegas), [Guy Savoy](https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/guy-savoy-las-vegas), and [é by José Andrés](https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/e-by-jose-andres).
- Bib Gourmand entries verified: [China Poblano](https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/china-poblano), [Esther's Kitchen](https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/esther-s-kitchen), [YEN Viet Kitchen](https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/yen-viet-kitchen). In particular, China Poblano official [venue page](https://cosmopolitanlasvegas.mgmresorts.com/en/restaurants/china-poblano.html) shows hours Mon–Thu 11 a.m.–10 p.m.; Fri 11 a.m.–10:30 p.m.; Sat 10 a.m.–10:30 p.m.; Sun 10 a.m.–10 p.m.; cocktail hour Mon–Thu 4–6 p.m. Venue page lists $60 tasting menu.
- First-party menu/hours pages retrieved: [Joël Robuchon](https://mgmgrand.mgmresorts.com/en/restaurants/joel-robuchon-french-restaurant.html), [L'Atelier](https://mgmgrand.mgmresorts.com/en/restaurants/latelier-joel-robuchon.html), [é](https://www.cosmopolitanlasvegas.com/restaurants/e-by-jose-andres), [Guy Savoy](https://www.caesars.com/caesars-palace/restaurants/restaurant-guy-savoy), [Bouchon](https://www.venetianlasvegas.com/dining/restaurants/bouchon.html), [COTE](https://www.venetianlasvegas.com/dining/restaurants/cote.html), [Milos](https://www.venetianlasvegas.com/dining/restaurants/estiatorio-milos.html), [Mott 32](https://www.venetianlasvegas.com/dining/restaurants/mott-32.html), [Gymkhana](https://aria.mgmresorts.com/en/restaurants/gymkhana.html), [Wing Lei](https://www.wynnlasvegas.com/dining/fine-dining/wing-lei), [Partage menu](https://partage.vegas/menu), [Lamaii menu/hours](https://www.lamaiilv.com/chinatown/), [Kabuto](https://www.kabutolv.com/), [Kame Omakase](https://sushikame.com/contact-us/), [Esther's Kitchen hours](https://www.estherslv.com/location/esthers-kitchen/), [SoulBelly menu](https://soulbellybbq.com/menu), and [Sparrow + Wolf menu/hours](https://sparrowandwolflv.com/menu/).
- Confirmed menu prices usable for two-person estimates: Partage tasting menus $130/$160/$210 per person; Stubborn Seed official 2026 tasting menu $160/person; China Poblano $60 tasting menu; SoulBelly combos from $18/person; Sparrow + Wolf tasting $149/person (menu says automatic gratuity applies); Lamaii menu has entrée prices; Kabuto omakase $48/$80/$120/person on official menu; Kame Omakase $350 or $500/person (high-cost, reservation-only); Bouchon menu dishes and Milos market menu have item prices; Mott 32 has dishes/feasts; COTE official menu lists the Feast of USDA Prime at $95/person. Taxes, tip, drinks and add-ons are not included unless explicitly stated.
- [Wing Lei hours](https://www.wynnlasvegas.com/dining/fine-dining/wing-lei): Thu/Sun/Mon 5:30–9:30 p.m.; Fri/Sat to 10 p.m.; closed Tue/Wed; under-5s not permitted.
- [Partage menu](https://partage.vegas/menu): Tue–Sat 5–9 p.m. (last reservation 8:30 p.m.); closed Sun/Mon.
- [Lamaii Chinatown](https://www.lamaiilv.com/chinatown/): Mon–Wed 11 a.m.–midnight; Thu–Sun 11 a.m.–2 a.m.
- [Esther's Kitchen](https://www.estherslv.com/location/esthers-kitchen/): weekday lunch 11 a.m.–3 p.m.; weekend brunch 10 a.m.–3 p.m.; dinner daily 5–11 p.m.
- [SoulBelly BBQ](https://soulbellybbq.com/): Tue–Thu/Sun 11 a.m.–9 p.m.; Fri/Sat to 10 p.m.; live music Fri/Sat, event-specific.
- [Sparrow + Wolf](https://sparrowandwolflv.com/): open daily 5–10 p.m. Menu pages are seasonal and may change.
- [Ping Pang Pong](https://goldcoast.boydgaming.com/dine/gc-ping-pang-pong): official page lists daily 10 a.m.–3 a.m.

## Known limitations / irregularities to flag

- Only South Point dated prices are verified; the comparable hotels have room fit but no verified rates. Do not rank hotels by made-up prices. Cheapest 7-night South Point start date across the complete Feb 15–Mar 23 arrival window is not yet established.
- RTC PDFs provide timetables but not a verified end-to-end arrival time in current findings. Recompute from selected departure/arrival times and allow transfer/wait time; recheck 2027 service before promising <=60 minutes.
- Restaurant page schedules are current snapshots, not 2027 guarantees. Yen Viet's venue hours were inconsistent across sources; leave its exact weekly hours blank and flag for direct verification. Some restaurants have reservation-only formats or unpublished menus/prices. No price estimate should be made where official price data is missing.
- Social handles must be linked only when discoverable from official venue/attraction pages; mark other profiles as not verified rather than guessing.
- Show the Bellagio Conservatory Mar. 7–12 closure prominently. Fremont events and attraction schedules for 2027 require another check close to the travel dates.

## Delivery status

- [x] Scope claimed, branch pushed
- [x] Initial official-source research recorded
- [ ] Complete rate-window scan and transit journey verification where supported
- [ ] Build mobile-friendly site and individual category pages, including Flagged for Review
- [ ] Run validation/build/accessibility/responsive checks
- [ ] Open PR from this branch to `main`
- [ ] Merge PR immediately (no review wait)
- [ ] Verify GitHub Pages deployment and record URL/status here
