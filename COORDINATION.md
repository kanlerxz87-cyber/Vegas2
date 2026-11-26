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


---

# Session a52047d7 — this branch (`arena/a52047d7-vegas2`)

Base: `c97c82a`. The session rules fix the branch name, so the brief's `session-<id>/<task>` form is not used (decision recorded in F14). Statuses use the same legend as above.

## Task board (session a52047d7)

| # | Task | Status | Files | Notes |
|---|------|--------|-------|-------|
| T1 | Repo review, line by line | done | `data/verified/repo_review.json`, `docs/repo-review.html` | Log 2026-11-26-A. Items verified on GitHub API |
| T2 | Hotels (8 Strip hotels): rooms, private bath, Michelin on campus | done (partial) | `data/verified/hotels.json` | Verified: Conrad, Bellagio, ARIA suite, Cosmopolitan (listing). Wynn two-queen claim withdrawn (F17). Prices and transit unverified |
| T3 | Michelin 2026 Las Vegas (24 rows) | done | `data/verified/michelin.json` | Status from official release. Hours and prices unverified |
| T4 | Activities (4) | done (partial) | `data/verified/activities.json` | Verified: Hoover fees and hours, Valley of Fire fee and closure, Neon 2027 admission and official social links. Hoover YouTube/Instagram, Red Rock social are agency-level (Partial) |
| T5 | Booking, price and timing | done (no verified 2027 rates) | `data/verified/booking.json` | Wynn rate page shows only Nov 26–27 2026. No 2027 total verified |
| T6 | Questions and information gaps | done | `data/verified/questions.json` | |
| T7 | Suggestions (review only, not implemented) | done | `data/verified/suggestions.json` | Waiting for user choice |
| T8 | Flagged for Review (F1–F18) | needs review | `data/verified/flagged.json` | Published. Does not block merge |
| T9 | Site build: landing, subpages, CSS, build and check scripts | done | `scripts/build_site.py`, `scripts/check_site.py`, `assets/style.css`, `docs/*.html`, `docs/planner-v1/` | `scripts/check_site.py` passes: 154 links, 11 pages, all rows sourced |
| T10 | Integration: merge with `main`, publish, PR, merge, Pages check | in progress | `COORDINATION.md`, `README.md`, `docs/`, `site/build.py` (one output path) | See log 2026-11-26-E |

## Merge conflicts and integration decisions (logged)

- **2026-11-26-D — conflict with PRs #2 and #3** (`arena/f0943026-vegas2`, `arena/e94404fc-vegas2`). Conflicts in `COORDINATION.md` (add/add), `README.md` and `index.html` (add/add). Resolution: both sides kept. The v1 dashboard is preserved as `planner-v1/` (copy of `main`'s root files).
- **2026-11-26-F — second conflict, PR #7** (`arena/36cc5108-vegas2`, merged as `d27f1f2`). That PR made the root `index.html` a redirect to `docs/index.html` and moved the v1 dashboard to `legacy-dashboard/`. Resolution: the redirect is kept. The Pages artifact is `docs/`, so `docs/index.html` (this session's verified landing) is the live home page. `docs/planner-v1/` keeps the v1 dashboard live inside the artifact, because `legacy-dashboard/` is outside it. `docs/session-36cc5108/` is unchanged.
- **2026-11-26-E — conflict with PR #6** (`arena/36cc5108-vegas2`, merged to `main` as `ff8a411`). PR #6 added `docs/`, `site/build.py` and `data/*.json` with the same names as this branch. Its Pages workflow now deploys `docs/`, so this branch's root-level site would not be published. Resolution:
  - Their `data/*.json` files are kept as they are. My data moved to `data/verified/`.
  - Their `docs/` is moved to `docs/session-36cc5108/`. One output path in `site/build.py` was changed (`OUT = ROOT/"docs"/"session-36cc5108"`) so their build cannot delete the root site. Their rebuild produces identical output with 0 errors.
  - My verified site is the published landing page at `docs/`.
  - `.github/workflows/pages.yml` (deploys `docs/`) is unchanged.
- **Board note.** The board above (session 36cc5108) says "no other session is active." That was true when written. This session also merged into `main` in parallel. Both sites are published and each is labelled.

## Verification corrections in this session

- **Wynn "Panoramic View Two Queens, 640 sq ft" withdrawn** (F17). It was marked verified in an earlier draft. Five chunks of the official booking page list King and Encore King rooms only.
- **Wynn resort-fee wording conflicts** on the same page (F18).
- **v1 star count is wrong:** says 3 starred, the official release lists 4 (é by José Andrés omitted) (F16).
- **ARIA, Conrad, Bellagio, Neon Museum, Hoover Dam, Valley of Fire** claims re-fetched from official pages and corrected (see log 2026-11-26-D).

## Session log (a52047d7)

- **2026-11-26-A — claim.** Claimed T1–T10. Baseline: `README.md` only, no LICENSE, no `.gitignore`, Pages enabled (legacy, `main` `/`, public).
- **2026-11-26-B — research.** Official sources: Michelin 2026 Southwest release and PDF; OPM federal holidays (Feb 15 2027 = Washington's Birthday); USBR Hoover Dam; BLM Red Rock; Recreation.gov timed entry; Nevada State Parks Valley of Fire; Neon Museum; hotel room pages (Cosmopolitan, Bellagio, Caesars, ARIA, Wynn booking engine, Resorts World Conrad); Caesars and é restaurant pages.
- **2026-11-26-C — build and gate.** Build reproducible. `check_site.py` passed (130 links, 10 pages) before the integration.
- **2026-11-26-D — conflict with PRs #2 and #3, and re-verification** (see above).
- **2026-11-26-E — conflict with PR #6, integration** (see above). PR #5 (`arena/a52047d7-vegas2` → `main`) is the integration PR.

## Still unverified (blank and flagged)

- Hotel rates for Feb 15–22 2027 (7 nights) and Feb 15–18 2027 (3 nights). No official 2027 rate retrieved.
- Transit times for the 1-hour rule, the restaurant hours for most of the 24 Michelin entries, restaurant costs for 2 adults, and most social links.
- Caesars, MGM Grand, and Venetian room pages (fetch errors).

## PR and merge record

- PR #5: https://github.com/kanlerxz87-cyber/Vegas2/pull/5 (`arena/a52047d7-vegas2` → `main`).
- Merge result and Pages check: see the entry appended after the merge below.

---

## Session 36cc5108 — collision with a52047d7 on T6/T10 and current state

Logged by session 36cc5108 (board update only; no site or data files changed in this entry).

- **Collision.** Both sessions claimed integration. PR #6 (36cc5108, `ff8a411`) and PR #7 (36cc5108, `d27f1f2`) merged first. PR #5 (a52047d7, `eaf87bb`, 22:10:16 UTC) then merged and replaced the root of `docs/` with a52047d7's site. This session's site was kept, not deleted: it is at `docs/session-36cc5108/` (checked: contains F29, the corrected Yen Viet entry, and OPM "Washington's Birthday" wording).
- **Pages.** `PUT /repos/.../pages` for source `main` `/docs` returned **403** for session 36cc5108. The source is still `main` `/`. Root `index.html` redirects to `docs/index.html`, and the live URL currently shows a52047d7's landing page. Owner action needed only if the `/docs` source is wanted (F27).
- **Read-only checks (36cc5108, on a snapshot of `origin/main`).** 21 HTML files under `docs/`, 0 broken local links or anchors. a52047d7's `scripts/check_site.py`: 154 links, 0 warnings. These checks did not rebuild or change `docs/`.
- **Two published sites now disagree. Not reconciled here; owner decision needed.**
  1. Hotel list: this session ranks 9 hotels (H1–H9). The root site lists 8 Strip candidates.
  2. Room facts: the root site says two-queen rooms are confirmed for Resorts World, Bellagio and the Cosmopolitan. This session marks queen-or-larger beds and private bathrooms as unverified for every hotel (F05). Those room pages were not fetched in this session.
  3. Hoover Dam hours: blank here (F09). The root site reports hours; this session did not verify them.
  4. Activities: this session lists 5 (Red Rock, Valley of Fire, Monorail, Neon Museum, Hoover Dam). The root site lists 4 (no Monorail).
  No values were copied between the two sites.
- **Status.** T6 (36cc5108): this session's site is merged and preserved. The root publish is owned by a52047d7 T10. No further writes to `docs/` from 36cc5108 until the owner chooses which site is the root.

---

## Session d33551df — supplemental dashboard and research record

Arena assigned the fixed working branch `arena/d33551df-vegas2`, based on `c97c82a`. This branch began with a single task claim; while implementation was underway, other sessions merged a root dashboard and integration work to `main`. To avoid clobbering any other session’s output, this session’s site is added as a separate Pages subdirectory at `docs/session-d33551df/`. The existing `docs/index.html`, `docs/session-36cc5108/`, `docs/planner-v1/`, `site/build.py`, root redirect, data trees and Pages workflow from `main` are preserved. The addition is linked from this README and uses `site/publish-supplement.py`, which writes only the new subdirectory.

### Scope and result

- Source dashboard: `site/index.html`, `hotels.html`, `restaurants.html`, `activities.html`, `analysis.html`, `flagged.html`, `assets/` and `verify.cjs`.
- Published copy: `docs/session-d33551df/`, served by the existing `docs/` Pages artifact without changing the root landing page or another session path.
- PR #11: https://github.com/kanlerxz87-cyber/Vegas2/pull/11 (branch `arena/d33551df-vegas2` → `main`). Initial merge attempt found conflicts because `main` advanced; integration is being resolved additively.
- User-specified constraints retained: no unverified values inferred, no user input requested, official source links on every findings-table row, and unresolved items remain visible on Flagged for Review.

### Research/source facts and irregularities

- MICHELIN source: [Visit Las Vegas 2026 restaurant list](https://www.visitlasvegas.com/michelin-guide-restaurants/). 24 venues: one two-star, three one-star, three Bib Gourmand and 17 Recommended/Selected. Distinctions are separate in the new table.
- Hotel room sources are linked per row in `site/assets/data.js`: official pages for Caesars Palace, MGM Grand, Cosmopolitan, Venetian and Wynn. Each selected room page confirms a king and private bath. Caesars room-size sources conflict (350 vs. 360+ sq. ft.); size is left blank.
- Caesars exact-date room list (Feb 15–22, 2027, two adults) had rate volatility/irregularity: earlier capture $226/night including resort fee, tax excluded; later recheck displayed Julius Deluxe King $201/night ($146 room rate + $55 daily resort fee, tax excluded) and room assigned on arrival $196/night, while also showing a technical-difficulties notice. Flexible calendar sum was $1,580. Simple products ($1,582 at $226; $1,407 at $201) are arithmetic, not confirmed totals. Seven-night total remains blank and flagged.
- Preferred Feb 15–18 is three nights, conflicting with the 1–2-week request. Feb 15–22 is explicitly only a seven-night comparison scenario.
- Official meal-price anchors: China Poblano $60/person; Anima by EDO $85/person; Partage $130/$160/$210 per guest for 5/7/Signature menus. Michael Mina lists $295++ per person but was shown temporarily closed on Nov 26, 2026. Guy Savoy weekly hours/full meal total, Yen Viet hours (conflicting snippets), and Kame Omakase hours/full meal total remain blank and flagged.
- Official RTC sources: [Trip Planner](https://www.rtcsnv.com/tripplanner/), [How to Ride](https://www.rtcsnv.com/ways-to-travel/how-to-ride/), [Maps & Guides](https://www.rtcsnv.com/ways-to-travel/schedules-maps/maps-guides/) and [Fares](https://www.rtcsnv.com/ways-to-travel/fares-passes/). No consistent 5 × 24 hotel-to-restaurant journey matrix was recorded. Transit counts stay blank (unmeasured, not zero), with no fabricated ranking.
- Attraction source links, current hours/prices and exceptions are in the activity table. Bellagio’s Lunar New Year display is listed Jan 9–Mar 6, 2027; Bellagio Gallery and Michael Mina are currently flagged temporarily closed.

### Verification

- After integrating `origin/main` additively, `python3 site/publish-supplement.py`, `node --check site/assets/app.js site/assets/data.js site/verify.cjs`, and `node site/verify.cjs` passed. The verifier checked 5 hotel candidates, 24 restaurants (4 starred / 3 Bib / 17 Selected), 8 activity/transit rows, 13 review flags, and source/local links.
- `python3 scripts/build_site.py` and `python3 scripts/check_site.py` passed for the existing root dashboard (154 internal links, 11 pages). The build preserves nested Pages subdirectories.
- `git diff --check` passed. Local HTTP smoke checks of all six published sub-pages and CSS/JS assets under `/session-d33551df/` returned 200.
- GitHub Pages hosting of `/session-d33551df/` remains to be confirmed after this PR is merged.
