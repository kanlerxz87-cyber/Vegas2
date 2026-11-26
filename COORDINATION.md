# COORDINATION — Las Vegas Trip Planning (Vegas2)

> **Integration note (a52047d7).** `main` gained PRs #2 and #3 from earlier sessions (`arena/f0943026-vegas2`, `arena/e94404fc-vegas2`) while this branch was open. Their live dashboard is preserved unchanged as `planner-v1.html` with its `styles.css`, `app.js` and `data.js`. This branch's verified site now owns `index.html` (landing) and the subpages. Their task rows are kept below as P1 and P2, and their log is kept verbatim in the section *Prior session records*.

Shared task board. Every row needs a status, an owning session, and the files it touches.

**Statuses:** `unclaimed` · `in progress` · `done` · `needs review` (published on the *Flagged for Review* page; does not block)

**Branch note:** This session runs on one branch only, `arena/a52047d7-vegas2` (base `c97c82a` on `main`). Per the session rules, no other branches are created or pushed. The `session-<id>/<task>` naming from the original brief is therefore not used; every task below is claimed on this branch under session ID `a52047d7`.

**Verification standard:** Every table row carries a source link. Values that cannot be confirmed from an official source are left blank and marked **Unverified**. Nothing is inferred or filled in.

| # | Task | Status | Owner (session) | Files in scope | Notes |
|---|------|--------|-----------------|----------------|-------|
| T1 | Repo review (line by line) | done | a52047d7 | `README.md` (read only), `data/repo_review.json`, `repo-review.html` | See log entry 2026-11-26-A |
| T2 | Hotel research (8 Strip-area hotels, rooms, Michelin proximity) | done | a52047d7 | `data/hotels.json` | Room claims verified against official pages where retrievable; prices not retrievable |
| T3 | Michelin restaurants, Las Vegas 2026 (24 entries) | done | a52047d7 | `data/michelin.json` | Official Michelin press release is the status source |
| T4 | Activities (4 verified attractions) | done | a52047d7 | `data/activities.json` | Official agency/operator pages |
| T5 | Booking, pricing & timing | done | a52047d7 | `data/booking.json` | No 2027 rate verified; timing not determined |
| T6 | Questions & information gaps | done | a52047d7 | `data/questions.json` | |
| T7 | Suggestions for site & decision-making (review only, not implemented) | done | a52047d7 | `data/suggestions.json` | Awaiting user choice |
| T8 | Flagged for Review (irregularities & unverified items) | needs review | a52047d7 | `data/flagged.json` | Published; does not block merge |
| T9 | Site build (landing, subpages, CSS, build + check scripts) | done | a52047d7 | `scripts/*.py`, `assets/style.css`, generated `*.html`, `.nojekyll`, `README.md` | Static site served from repo root via GitHub Pages |
| T10 | Integration: re-verify combined data, build, link check, PR, merge, Pages check | in progress (build & gate passed; PR/merge pending) | a52047d7 | `COORDINATION.md` | Final step |

| P1 | Initial Vegas trip planner and GitHub Pages site (base implementation) | done | arena/f0943026-vegas2 | COORDINATION.md, README.md, index.html, styles.css, data.js, .github/workflows/pages.yml | Merged to main via PR #2 (`58dd7c3`). Now kept as `planner-v1.html` |
| P2 | Expanded planner: mobile summaries, hotel shortlist, dining, activities, questions, review flags | done | arena/e94404fc-vegas2 | index.html, styles.css, app.js, README.md, .nojekyll, COORDINATION.md | Merged to main via PR #3 (`dce4548`). `styles.css`, `app.js`, `data.js` still serve `planner-v1.html` |

---

## Session log

### 2026-11-26-A — a52047d7 — claim
- Claimed T1–T10 on branch `arena/a52047d7-vegas2`. Only this session is active; no conflicts with other sessions were seen (the repo had a single commit and no other branches on `origin`).
- Baseline: `README.md` only (`# Vegas2`), no LICENSE, no `.gitignore`, no `COORDINATION.md` (created in this session), GitHub Pages enabled (legacy, `main` `/`, public, status `built`) per `gh api repos/kanlerxz87-cyber/Vegas2/pages`.

### 2026-11-26-B — a52047d7 — research & verification (sources)
Official sources retrieved on 2026-11-26 (all links are the pages actually read):
- Michelin 2026 Southwest selection (official press release, Aug 26/31 2026): https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s — full star, Bib and Recommended lists with addresses. Also the Michelin Media copy https://michelinmedia.com/pages/blog/detail/article/c0/a1480/ and the PDF attached to the release.
- OPM federal holidays 2027 (Washington's Birthday = Mon Feb 15, 2027): https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/
- Bureau of Reclamation, Hoover Dam: https://www.usbr.gov/lc/hooverdam/ and https://www.usbr.gov/lc/hooverdam/service/index.html
- BLM, Red Rock Canyon NCA: https://www.blm.gov/visit/red-rock-canyon-national-conservation-area
- Recreation.gov, Red Rock Scenic Drive timed entry: https://www.recreation.gov/timed-entry/10075177
- Nevada State Parks, Valley of Fire: https://parks.nv.gov/parks/valley-of-fire
- Neon Museum (official site): https://neonmuseum.org/ and https://neonmuseum.org/tickets-and-experiences/
- Hotel official pages: Cosmopolitan https://cosmopolitanlasvegas.mgmresorts.com/en.html · Bellagio https://bellagio.mgmresorts.com/en/hotel.html · Caesars Palace https://www.caesars.com/caesars-palace · ARIA https://aria.mgmresorts.com/en/hotel/center-suite.html · Wynn booking engine https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&langID=1&access=&corp=&voucher=&rcID=324634&currID=0 · Resorts World (Conrad) https://www.rwlasvegas.com/stay/conrad-las-vegas/premium-room/
- Restaurant official pages: é by José Andrés https://www.ebyjoseandres.com/ · Guy Savoy https://www.caesars.com/caesars-palace/restaurants/restaurant-guy-savoy · Gymkhana hours via MGM Resorts press release (republished) https://www.stocktitan.net/news/MGM/aria-resort-casino-and-jks-restaurants-unveil-gymkhana-bringing-pus2edgb10tf.html
- Repo/Pages config: https://api.github.com/repos/kanlerxz87-cyber/Vegas2/pages

### 2026-11-26-C — a52047d7 — build & verification gate
- Built 10 pages with `python3 scripts/build_site.py`; re-running it produces no diff (reproducible).
- `python3 scripts/check_site.py`: OK — all data files parse; every hotel, Michelin and activity row has at least one https source; every row source is on the official-domain allowlist; Michelin counts 4 starred / 3 Bib / 17 Recommended = 24; 130 internal links resolve across 10 pages; no placeholder text leaked into HTML.
- Verification totals (cells across hotels, Michelin and activities): see the Home page KPIs.
- Commit: `c8d3d9b` (site build) on `arena/a52047d7-vegas2`.

### 2026-11-26-D — a52047d7 — integration, merge conflict & re-verification
- **Merge conflict logged.** While this branch was open, `main` received PR #2 (`arena/f0943026-vegas2`, commit `58dd7c3`) and PR #3 (`arena/e94404fc-vegas2`, commit `dce4548`). The PR then reported "not mergeable". Conflicts were in `COORDINATION.md` (add/add), `README.md` (content) and `index.html` (add/add).
- **Resolution (kept both sides, no history lost):** `index.html` is now this session's verified landing page. The earlier single-page dashboard is preserved unchanged as `planner-v1.html` (its `styles.css`, `app.js` and `data.js` are kept). `README.md` was rewritten to cover both. This board keeps the prior rows as P1/P2 and the prior log verbatim.
- **Re-verification before publish (fetched 2026-11-26):**
  - ARIA Center Tower Suite — 2 Queen Beds, private water closet (suite only) → Verified.
  - Resorts World Conrad Premium Room — one king or two queens, 550 sq ft, spa bathroom → Verified.
  - Bellagio Premier Two Queen — 2 Queen Beds, 510 sq ft → Verified.
  - Wynn Las Vegas — **the "Panoramic View Two Queens 640 sq ft" claim is withdrawn.** Across five chunks, the official booking page lists only King and Encore King rooms. Queen is now Unverified (F17).
  - Wynn booking page resort fee conflicts ($55 plus tax vs "includes resort fee") → F18.
  - Neon Museum — official 2027 admission (daily 3–11 PM, from $21) and official TikTok/Instagram/Facebook links → Verified.
  - Hoover Dam — official fees ($40 guided dam tour, $25 powerplant, $15 visitor center, $10 parking), last tour 4:10 PM, Hoover Facebook → Verified. YouTube and Instagram are Bureau-level only → Partial.
  - Valley of Fire — $10 / $15 non-NV, Dec 1–14 maintenance closure → Verified.
  - Red Rock — agency-level BLM social links → Partial.
- **Found and fixed:** `planner-v1.html` says 3 starred restaurants and omits é by José Andrés. The official release lists 4 (F16).
- **Still unverified:** all 2027 hotel rates and totals, transit times, most restaurant hours and costs, Caesars/MGM/Venetian room pages, Valley of Fire social.

### Verification gaps (see Flagged for Review)
- Official MGM Grand, Venetian, Restaurant de Joël Robuchon and L'Atelier pages could not be retrieved (fetch errors). Their rows are marked partial/unverified.
- No hotel rate for 7 nights (Feb 15–22, 2027) or 3 nights (Feb 15–18, 2027) was retrieved from an official source.
- No official transit-time source for "within 1 hour by bus/subway" was retrieved.

### Irregularities found
See `flagged.html` (Flagged for Review) for the full list and links. Key items: conflicting Michelin status claims in secondary press; Feb 15, 2027 is a federal holiday (Washington's Birthday); conflicting restaurant hours across third-party sites.

---

## Integration (T10) — checklist
- [x] All task data files present and valid JSON (checked by `scripts/check_site.py`)
- [x] Site builds from `scripts/build_site.py` with no errors
- [x] Internal links resolve (checked by `scripts/check_site.py`)
- [x] Every table row has at least one source link (checked by `scripts/check_site.py`)
- [ ] Pull request from `arena/a52047d7-vegas2` into `main`
- [ ] Merge result recorded below
- [ ] GitHub Pages deploy confirmed live

### PR & merge record
- PR #5 (`arena/a52047d7-vegas2` → `main`): https://github.com/kanlerxz87-cyber/Vegas2/pull/5 — opened with summary, sources and irregularities. Its first attempt to merge reported a conflict with `main` (PRs #2/#3). Resolved on this branch (see log 2026-11-26-D) and pushed.
- Merge result and Pages deploy result: recorded in the branch's final commit after merge (see the end of this section).

---

## Prior session records (verbatim, from `main`)

### Verification log
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
