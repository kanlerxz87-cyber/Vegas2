# COORDINATION.md — Shared task board (Vegas2)

Branch in use: `arena/36cc5108-vegas2` (fixed for this session by Arena; the `session-<id>/<task>` naming in the brief cannot be used). All tasks are on this one branch. Scopes below are disjoint; no other session is active on this repo.

Legend: `unclaimed` · `in progress` · `done` · `needs review` (published on Flagged for Review; does not block anything)

## Task board

| ID | Task | Status | Owner | Claimed (UTC) | File scope |
|----|------|--------|-------|---------------|------------|
| T0 | Repo review + irregularity flags | done | 36cc5108 | 2026-11-26 | `data/repo_review.json`, `data/flags.json` (repo flags F25–F27) |
| T1 | Hotels: shortlist, in-resort Michelin ranking, official resort fee, trip-date options | done (prices and room specs flagged as unverified) | 36cc5108 | 2026-11-26 | `data/hotels.json` |
| T2 | Michelin restaurants (official 2026 Southwest list, Las Vegas, 24 rows) | done (hours partly unverified; see F17–F19) | 36cc5108 | 2026-11-26 | `data/restaurants.json` |
| T3 | Activities within transit/drive limits, official pages | done (Hoover Dam hours unverified; see F09) | 36cc5108 | 2026-11-26 | `data/activities.json` |
| T4 | Questions, suggestions (for approval only), sources | done | 36cc5108 | 2026-11-26 | `data/questions.json`, `data/suggestions.json`, `data/sources.json` |
| T5 | Static site (landing, category pages, Flagged for Review) | done (builds with 0 errors) | 36cc5108 | 2026-11-26 | `site/build.py`, `docs/**`, `README.md` |
| T6 | Integration: combined re-check, build, link check, PR to `main`, merge, Pages | in progress | 36cc5108 | 2026-11-26 | all |

## Source and verification record (per task)

**T0 Repo review.** Sources: `api.github.com/repos/kanlerxz87-cyber/Vegas2` (S31), `api.github.com/.../pages` (S28), local git (`c97c82a`, `2cf5776`). Verified: visibility public, default branch main, Pages legacy build from main `/`. Irregular: repo holds only a 8-byte README and no LICENSE or .gitignore (F26); branch naming differs from brief (F25); Pages will move to `/docs` (F27).

**T1 Hotels.** Sources: Michelin release (S01, S02) for every hotel-to-restaurant address match; Caesars booking page (S08) for the only verified resort fee ($62.30/night incl. tax); Caesars home page (S09) and Cosmopolitan home page (S20) for booking-offer types. Not verified (left blank, flagged): 7-night totals (F06), queen-or-larger bed and private bathroom (F05), resort fees other than Caesars (F08), best time to book (F04). Third-party resort-fee reports (S22) were not used as values.

**T2 Michelin restaurants.** Sources: Michelin press release (S01) and WebWire copy (S02) for all 24 distinctions and addresses; LVCVA page (S03) for area, cuisine and official site links. Hours verified from official pages: Joël Robuchon (S04), L'Atelier (S05), é (S06); Guy Savoy (S07) phone, dress and price symbol only. Kabuto (S16) hours are partial (official captions). Not verified: hours for 20 rows (F17), price for 2 for all rows (F18), social accounts for all restaurants (F19). Conflicts flagged: F10, F11, F12, F14.

**T3 Activities.** Sources: BLM Red Rock (S13), NV State Parks Valley of Fire (S14), Las Vegas Monorail (S12), Neon Museum (S15); Hoover Dam official site could not be retrieved (S21 archive from 2010 and S27 third-party conflict) so its hours are blank (F09).

**T4 Questions, suggestions, sources.** Sources: OPM 2027 federal holidays (S10) for Feb 15, 2027. Suggestions S-01 to S-14 are proposals only and are awaiting approval.

**T5 Site.** Built by `site/build.py` (standard library). Last build: 10 pages, 0 errors (strict source checks; internal links and anchors resolved).

## Irregularities for review (summary; full text on Flagged for Review)

- Brief says "subway or bus"; official sources show RTC bus and the Strip monorail, no subway (F01).
- Red Rock Canyon has no public transit (BLM, S13); it cannot meet the bus-only one-hour test (F02).
- Trip length conflict: 3-night preferred vs 7-night cost basis vs 1–2 weeks (F03).
- Feb 15, 2027 is Washington's Birthday, a federal holiday (OPM, S10) (F13).
- Yen Viet Kitchen: Bib Gourmand confirmed by the official release (S01, S02) and Time Out (S26); no conflict (F14, resolved).
- Guy Savoy hours: official page shows none; three listings conflict (F10).
- Hoover Dam hours: current official page not retrievable; sources conflict (F09).

## Session log

- 2026-11-26 · 36cc5108 · Claimed T0–T6. Repo held only `README.md`; created this file. Pages was enabled on `main` (legacy, `/`), so the site will be served from `/docs` after merge.
- 2026-11-26 · 36cc5108 · Completed research and data for T0–T4 against official sources (retrieved this session). Built the site (T5) with 0 errors.
- 2026-11-26 · 36cc5108 · T6 integration check: re-counted Michelin listings (4 starred, 3 Bib, 17 Recommended = 24) against the release; fixed one official name ("Stubborn Seed Las Vegas"); verified every source and flag ID is defined and referenced; verified trip weekdays (Feb 15 Mon, Feb 18 Thu). Next: PR, merge, Pages source to `/docs`, deploy check.

---

## Entries from other sessions on `main` (preserved verbatim)

These entries were written by other sessions and are kept unchanged. They are not edited by session 36cc5108.

### Coordination board (verbatim from main)

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

## PR and deployment result
- PR #2 (https://github.com/kanlerxz87-cyber/Vegas2/pull/2) merged to `main` at `58dd7c3d9668c982b52fa83a5afe07a0a7447f0e` on 2026-11-26.
- GitHub Pages deployment run 45901451051 succeeded. Published dashboard: https://kanlerxz87-cyber.github.io/Vegas2/. The Pages API reported `building` briefly; fetching the public URL then returned the deployed page.
- Actions emitted a Node.js 20 deprecation advisory for upstream Actions versions; deployment succeeded.


## Integration record (session 36cc5108, T6)

- **PR #6** (https://github.com/kanlerxz87-cyber/Vegas2/pull/6): `arena/36cc5108-vegas2` → `main`. Conflict with `main` at `dce4548` (another session's root dashboard). Both sides kept; no file deleted. Merged with `gh pr merge 6 --merge` after the build passed (0 errors, 672 local links OK). Merge result: merged.
- **Pages source**: the API call to set source `main` `/docs` returned **403 (Resource not accessible by integration)**. The source is still `main` `/` and must be set in Settings → Pages by the repository owner if the `/docs` source is wanted (F27). The site works either way (see next item).
- **Root redirect**: because the root build was still serving the earlier dashboard, `index.html` at the repository root now redirects to `docs/index.html`. The earlier dashboard moved to `legacy-dashboard/` with `git mv` (nothing deleted; its COORDINATION link now points to GitHub).
- **Pages workflow**: `.github/workflows/pages.yml` now uploads `docs/` (was `.`).
- **Corrections in this integration**: removed an unsupported Caesars tax split; OPM holiday wording; Yen Viet Kitchen Time Out check resolved (no conflict, F14); other dashboard's starred-count error flagged (F29).
- **PR #7**: this change (root redirect, legacy move, record update). Its merge result is recorded in the PR and in the next COORDINATION update.
