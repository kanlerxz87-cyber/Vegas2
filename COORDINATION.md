# Coordination board

| Task | Status | Owner | Files |
|---|---|---|---|
| Research-backed Vegas trip planner and GitHub Pages site (initial base implementation) | done | arena/f0943026-vegas2 | COORDINATION.md, README.md, index.html, styles.css, data.js, .github/workflows/pages.yml |
| Expand planner with mobile-first summaries, hotel shortlist, dining and activity tables, open questions and review flags | done | arena/e94404fc-vegas2 | index.html, styles.css, app.js, README.md, .nojekyll, COORDINATION.md |

## Verification log
- Initial implementation: Michelin entries and star statuses checked against official MICHELIN Guide pages linked in `data.js` (2026 selection). Future hours, transit times, prices and inventory are not asserted without confirmation. `node --check data.js` passed; HTML anchors/local references checked. No build dependencies required.
- 2026-11-26 expansion: official MGM Grand page (https://mgmgrand.mgmresorts.com/en.html) confirms room options including MGM Two Queen; official transportation page (https://mgmgrand.mgmresorts.com/en/amenities/transportation.html) lists Monorail rates, station-to-station times, and operating hours (not guaranteed for 2027). Venetian homepage and map/parking page checked (https://www.venetianlasvegas.com/ and https://www.venetianlasvegas.com/resort/maps-and-parking.html). Caesars Palace and Wynn official property pages checked (https://www.caesars.com/caesars-palace and https://www.wynnlasvegas.com/).
- MICHELIN official Guide result pages show 2026 award/listing statuses: Restaurant de Joël Robuchon, Two Stars (https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/restaurant-de-joel-robuchon); L’Atelier de Joël Robuchon, One Star (https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/l-atelier-de-joel-robuchon-las-vegas); Restaurant Guy Savoy, One Star (https://guide.michelin.com/en/nevada/las-vegas_2935077/restaurant/guy-savoy-las-vegas); Bouchon and Stubborn Seed have Guide listings but no star badge in search-result markup (https://guide.michelin.com/en/nevada/las-vegas_2935077/restaurant/bouchon-1250929 and https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/stubborn-seed-las-vegas). Direct fetch of individual Michelin pages failed; recheck linked current pages before booking.
- Local verification of expanded page: all internal anchors have targets, local stylesheet/script/log exist, and `git diff --check` passes. Static site uses no dependencies; Pages workflow is configured to deploy root on `main` or manual dispatch. No live 2027 price lookup or authenticated booking was performed.

## Irregularities / flagged for review
- Hotel date-specific total quotes (room, tax, resort fee, cancellation rules) and historical data needed to determine cheapest booking time are unavailable; price cells are blank.
- Selected-room bathroom/bed details need confirmation (MGM's Two Queen bed size is shown by its official property page); remaining hotel room details need room-level checking.
- Door-to-door transit times and 2027 schedules, restaurant totals/current menus and 2027 operating hours, plus official restaurant/activity social or video URLs remain unverified. These are blank and marked in the site's Flagged for Review section.
- Preferred Feb 15–18, 2027 dates are three nights, incompatible with the 7–14-night duration. The displayed seven-night example is Feb 15–22, 2027 and is labeled as such.
- MICHELIN awards are from the 2026 selection, not a guarantee of 2027 status, opening, or availability.

## Coordination note
The original checkout initially exposed only README.md and no coordination file. A concurrent PR had landed on `main` by the time the feature branch was rebased. Its files and data were preserved; this branch expands that implementation rather than replacing the existing data. Arena requires work on its assigned fixed branch, so the user-requested per-session branch naming is not applicable here.
