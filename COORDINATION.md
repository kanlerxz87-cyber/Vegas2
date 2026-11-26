# Coordination Board

No prior task board existed at kickoff. This session is the only active worker visible in this checkout. Arena requires all work to remain on the assigned branch `arena/d33551df-vegas2`; the requested per-session worktree naming convention is not being used because the Arena branch is fixed.

| Task | Status | Owner / session | File scope | Notes |
|---|---|---|---|---|
| End-to-end Las Vegas trip research, sourced planning dashboard, verification, and GitHub Pages deployment | implementation complete; PR/deployment pending | `arena/d33551df-vegas2` (current session) | Entire repository; no other task claimed | Static mobile dashboard and route/data checks are ready. Continue only on this branch. |

## Verification and handoff log

- Kickoff: read the repository root and checked `git status`; repository initially contained only `README.md`, with no `COORDINATION.md` and no other task claim.
- Claim recorded and pushed before implementation as `dd200d4 docs: claim Vegas trip planning task`. The initial `git pull --rebase origin arena/d33551df-vegas2` failed because the remote branch did not exist; the branch was then pushed to origin successfully.
- Implementation is in `site/` with static HTML/CSS/JS, a data verifier, mobile card-style tables, source links, and a GitHub Pages Actions workflow. There are no other file-scope claims.
- As of Nov 26, 2026, `node --check` passed for the dashboard scripts and `node site/verify.cjs` passed: 5 hotels, 24 restaurants (4 starred / 3 Bib Gourmand / 17 Recommended/Selected), 8 activity/transit rows, and 13 review flags; every rendered findings-table row has an official source link.
- `git diff --check` passed. The local HTTP smoke check returned 200 for the landing page, all five category pages, CSS and JavaScript assets.
- No PR has yet been created or merged and no GitHub Pages deployment has yet been confirmed. Update this log after creating/merging the PR and checking the deployment run and public Pages URL.

## Verified source ledger and captured findings

All individual row sources are embedded in `site/assets/data.js` and linked in the dashboard. This ledger preserves the evidence and known irregularities so the research does not depend on browser history.

### MICHELIN restaurants

- Official 2026 list: [Visit Las Vegas — MICHELIN Guide restaurants](https://www.visitlasvegas.com/michelin-guide-restaurants/). It supports 24 entries: Joël Robuchon (two stars); L’Atelier de Joël Robuchon, Restaurant Guy Savoy and é by José Andrés (one star each); China Poblano, Esther’s Kitchen and Yen Viet Kitchen (Bib Gourmand); and 17 Recommended/Selected venues. The dashboard keeps stars, Bib Gourmand and Recommended/Selected distinct.
- Official restaurant sources, hours, page facts and price anchors are stored on each venue record and shown in the restaurant table. Notable price facts: China Poblano’s José’s Way menu is $60/person ($120 for two); Anima by EDO’s tasting menu is $85/person ($170 for two); Partage has 5/7/Signature menus at $130/$160/$210 per guest ($260/$320/$420 for two), all before taxes/tip/other add-ons.
- Michael Mina’s [official Bellagio page](https://bellagio.mgmresorts.com/en/restaurants/michael-mina.html) displayed “Temporarily closed” and daily closed status on the research date; it also listed a $295++ tasting menu per person. The conditional $590++ for two is not evidence of February/March 2027 availability.
- Yen Viet Kitchen official-site search snippets conflicted about Tuesday service; the fetched current site page did not resolve the hours. Guy Savoy weekly hours/full two-person meal price and Kame Omakase hours/full price were not established from reviewed official pages. These values remain blank and flagged.
- Social links are only shown where confirmed from a business/venue page: China Poblano, Anima by EDO, Gymkhana, Kabuto and SoulBelly. No account was guessed for other venues.

### Hotels and rates

- Official room-fit evidence: [Caesars Palace rooms](https://www.caesars.com/caesars-palace/hotel), [MGM Grand MGM King](https://mgmgrand.mgmresorts.com/en/hotel/mgm-king.html), [Cosmopolitan City Room King](https://cosmopolitanlasvegas.mgmresorts.com/en/hotel/city-room-king.html), [Venetian Skyline Grand One Bedroom Suite](https://www.venetianlasvegas.com/hotel/the-venetian/skyline-grand-one-bedroom-suite.html), [Wynn Tower Suite Parlor](https://www.wynnlasvegas.com/rooms-and-suites/wynn-tower-suites/wynn-parlor-suite). All five selected room types specify a king bed and private bath. Four room sizes are verified (446–1,280 sq. ft.); Caesars sources disagree (350 vs. 360+ sq. ft.), so its size is blank pending room-type verification. Wynn booking details showed a $55 + tax Tower Suite resort fee and a breakfast credit subject to rate terms.
- [Caesars exact-date room list](https://www.caesars.com/book/room-list?arrivalDate=02/15/2027&departureDate=02/22/2027&dateSearchFormat=exact-dates&propCode=clv): Feb 15–22, 2027, two adults; page showed 69 rooms but also a technical-difficulties notice. An earlier capture showed $226/night best available, resort fee included and taxes excluded. A later recheck displayed Julius Deluxe King at $201/night ($146 room + $55 resort fee, taxes excluded) and a room-type-assigned option at $196/night. The separate flexible calendar sums $1,580; earlier $226 × 7 is $1,582, and $201 × 7 is $1,407 arithmetic. These do not resolve to a checkout total; the total is deliberately blank.
- Other date-rate failures: MGM booking flows errored; Venetian’s dated suite query returned a capacity message rather than a rate; Wynn’s date query returned stale Nov 2026 dates. MGM’s [official offer page](https://mgmgrand.mgmresorts.com/en/offers/wifi.html) showed a Black Friday promotion (up to 30% plus $100 F&B; members up to 45%) but not a dated Feb 2027 room price. No cross-hotel cheapest stay is claimed.
- Caesars’ hotel page also advertised up to 30% off for advance purchase at least 30 days before a stay; no specific room/date checkout total or eligibility was established.

### Transit and activities

- The [RTC Trip Planner](https://www.rtcsnv.com/tripplanner/) accepts origin, destination, date and time; RTC’s [How to Ride](https://www.rtcsnv.com/ways-to-travel/how-to-ride/) and [Maps & Guides](https://www.rtcsnv.com/ways-to-travel/schedules-maps/maps-guides/) describe the planner’s route, walking-direction and travel-time outputs. The RTC [fare page](https://www.rtcsnv.com/ways-to-travel/fares-passes/) lists visitor Strip & All Access prices: $4 single, $6 two-hour, $8 24-hour, $20 three-day per rider. The August 2026 Deuce schedule is linked on the activity page.
- No consistent 5 hotel × 24 restaurant journey-time matrix was captured. Deuce service/fare information does not prove door-to-door ≤60-minute reach. Hotel reach counts are blank (unmeasured, not zero), so no ranking is asserted.
- Official activity sources and captured values appear in the activity table: High Roller ($23.50 daytime / $34.75 anytime adult); Shark Reef ($29 timed / $36 anytime adult); Neon Museum’s 2027 daily Sept–May schedule 3–11 p.m., last admission 10 p.m., adult ticket from $21 plus processing fee; Mob Museum daily 9 a.m.–9 p.m. with seasonal/early-closure caveats; Fountains’ posted schedule/free admission/weather caveat; and RTC Deuce fares. Bellagio Conservatory lists Lunar New Year Jan 9–Mar 6, 2027 and dark dates Mar 7–12. The official Bellagio Gallery page currently says temporarily closed.
- Future attraction prices, schedules, tickets, closures and bus service can change before travel. Social links on the activity page are limited to those linked from official High Roller/Neon Museum pages.

## Irregularities and remaining work

- Preferred dates **2027-02-15 to 2027-02-18** are three nights, conflicting with the requested 1–2-week trip. The dashboard preserves both and labels **2027-02-15 to 2027-02-22** as a separate seven-night comparison scenario, not an assumed itinerary.
- Caesars is the only property with date-specific rate displays, but the same-date page changed between captures ($226, then $201/night for Julius King and $196/night for room-assigned), with a technical-difficulties notice on the latest page. The calendar sum is $1,580 and taxes are excluded from the nightly values; the seven-night total is unresolved. The cheapest stay across properties/the full window remains unknown.
- Transit ranking, the flagged restaurant hours/meal totals, 2027 exception schedules, full price comparisons, and the Gallery/Michael Mina future availability remain open; unverified facts do not block the site/merge but are explicitly disclosed.
- Possible later site enhancements are described in `site/analysis.html`: comparable quote snapshots, an RTC route matrix, a menu-basket estimator, trip-date closure alerts, exports and source freshness markers.

## Files in scope

- `site/index.html`, `hotels.html`, `restaurants.html`, `activities.html`, `analysis.html`, `flagged.html` — landing page and five category subpages.
- `site/assets/data.js`, `app.js`, `styles.css` — source-linked research data, page renderer and mobile styling.
- `site/verify.cjs` — content invariants, official-source row coverage and render smoke tests.
- `.github/workflows/pages.yml` — verify and deploy the `site/` artifact to GitHub Pages on updates to `main`.
- `README.md` — project guide, preview, verification and key caveats.
- `COORDINATION.md` — this task claim, research ledger, irregularities and deployment handoff.
