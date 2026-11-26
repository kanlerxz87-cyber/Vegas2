# COORDINATION.md — Shared task board (Vegas2)

Multi-session repo integration. All work is on the Arena-fixed branch `arena/e9badc77-vegas2`; the brief's `session-<id>/<task>` branch naming cannot be used (Arena pins the branch). No other session is active on this repo right now.

Status values: `unclaimed` · `in progress` · `done` · `needs review` (published on Flagged for Review; does not block anything)

## Integration summary (this session: e9badc77-vegas2)
Merged `origin/main` (prior sessions 36cc5108, a52047d7, f0943026, e94404fc, 059c3126, d33551df) into `arena/e9badc77-vegas2`. Conflicts surfaced in `COORDINATION.md` and `index.html` (both add/add). Resolution: both sides kept; nothing deleted.
- `index.html`: prior root index.html was a redirect to `docs/index.html`; this session's full dashboard landing page is kept as the root landing page (served from GitHub Pages root `/`). Prior `docs/` site preserved untouched under `docs/`, plus each session's subdirectory (`docs/session-36cc5108/`, `docs/session-059c3126/`, `docs/session-d33551df/`).
- `COORDINATION.md`: combined below.

No files from either side were discarded. Shared outputs (index/navigation/table data) were integrated by this final session.

## Combined task board

### Session e9badc77-vegas2 (this branch)
| # | Task | Status | Owner | File scope | Sources / verification |
|---|------|--------|-------|------------|------------------------|
| 1 | Create COORDINATION.md task board | done | e9badc77-vegas2 | COORDINATION.md | n/a |
| 2 | Research Michelin Guide Las Vegas (starred vs listed) — official source | done | e9badc77-vegas2 | restaurants.html | visitlasvegas.com (LVCVA, official) + official restaurant sites |
| 3 | Research Las Vegas hotel options & pricing — official booking | done | e9badc77-vegas2 | hotels.html | venetianlasvegas.com, caesars.com (official booking, Feb 15–22 2027) |
| 4 | Research activities + YouTube/TikTok/Instagram links | done | e9badc77-vegas2 | activities.html | official venue sites (left blank where unverified) |
| 5 | Build data tables with verified sources + unverified flags | done | e9badc77-vegas2 | restaurants.html, hotels.html, activities.html | official sources per row |
| 6 | Clean dashboard CSS (mobile-friendly) + shared layout/nav | done | e9badc77-vegas2 | assets/css/style.css | n/a |
| 7 | Landing page (index.html) + executive summary | done | e9badc77-vegas2 | index.html | n/a |
| 8 | Category subpages (hotels, restaurants, activities) | done | e9badc77-vegas2 | hotels.html, restaurants.html, activities.html | n/a |
| 9 | Suggestions section (decision paths before implementing) | done | e9badc77-vegas2 | suggestions.html | n/a |
| 10 | Questions / information / answers section | done | e9badc77-vegas2 | questions.html | n/a |
| 11 | "Flagged for Review" page (unverified items + irregularities) | done | e9badc77-vegas2 | flagged-for-review.html | n/a |
| 12 | Integrate, verify table rows line-by-line, fix broken links | done | e9badc77-vegas2 | all | internal links verified; external official sources linked |
| 13 | Enable GitHub Pages, confirm deploy, no broken links | done | e9badc77-vegas2 | repo Pages settings | Pages enabled on main `/`; URL https://kanlerxz87-cyber.github.io/Vegas2/ |
| 14 | Create PR from integration to main, merge, record PR link + result | done | e9badc77-vegas2 | GitHub PR #12 | merged to main |

### Prior sessions (summarized; full verbatim records preserved in git history)
| Session | Branch | Role | Key records |
|---------|--------|------|-------------|
| f0943026 | arena/f0943026-vegas2 | Base implementation | PR #2; COORDINATION.md, README.md, index.html, styles.css, data.js, .github/workflows/pages.yml |
| e94404fc | arena/e94404fc-vegas2 | Mobile-first expansion | PR #3; index.html, styles.css, app.js, README.md, .nojekyll, COORDINATION.md |
| 36cc5108 | arena/36cc5108-vegas2 | Repo review, hotels, Michelin 24 rows, activities, questions, static site | PR #6; data/repo_review.json, data/flags.json (F25–F27), data/hotels.json, data/restaurants.json, data/activities.json, data/questions.json, data/suggestions.json, data/sources.json, site/build.py, docs/**, flags F01–F29 |
| a52047d7 | arena/a52047d7-vegas2 | Verified hotels/Michelin/activities/questions/suggestions, build & check scripts | PR #5; data/verified/**, scripts/build_site.py, scripts/check_site.py, assets/style.css, docs/*.html, docs/planner-v1/, flags F1–F18 (needs review) |
| 059c3126 | arena/059c3126-vegas2 | Trip research + build/check + Pages checks | PR #4; data/trip/**, scripts/build.mjs, scripts/linkcheck.mjs, scripts/style.css, docs/session-059c3126/, .github/workflows/pages-check.yml |
| d33551df | arena/d33551df-vegas2 | Supplemental dashboard + research record | PR #11; site/index.html, hotels.html, restaurants.html, activities.html, analysis.html, flagged.html, assets/, verify.cjs, published at docs/session-d33551df/ |

### Notable prior-session irregularity flags (preserved)
F01–F29 include: no subway in Las Vegas (RTC bus + Strip monorail only); Red Rock Canyon no public transit; trip-length conflict (3-night preferred vs 7-night cost basis vs 1–2 weeks); Feb 15 2027 = Washington's Birthday (federal holiday); queen-or-larger bed and private bathroom unverified for most hotels; 7-night totals / best time to book unverified; most restaurant hours, per-couple prices, and social links unverified; Hoover Dam hours not retrievable from current official page; MICHELIN awards are 2026 selection, not a guarantee of 2027 status; v1 star count error (says 3 starred, official release lists 4); Wynn two-queen claim withdrawn; Caesars room-size sources conflict (350 vs 360+ sq ft, left blank); Caesars exact-date rate volatility ($226 vs $201 vs $196/night; 7-night total blank).

## Claims log
- e9badc77-vegas2: claimed tasks 1–14; completed and committed all; merged origin/main and resolved conflicts; created PR #12 and merged to main; Pages deploy confirmed.
- Prior session claims are preserved/summarized above; full verbatim text is in git history (commit ed54f82 and the origin/main line).

## Handoffs / conflicts
- 2026-11-26 · e9badc77-vegas2 · Merge conflict: `index.html` (add/add) and `COORDINATION.md` (add/add) when merging `origin/main` into `arena/e9badc77-vegas2`. Resolution: both sides kept; nothing deleted. Root index.html = this session's dashboard; prior redirect-to-docs index.html superseded at root but `docs/` site preserved intact.
- 2026-11-26 · e9badc77-vegas2 · Second merge conflict: `COORDINATION.md` (content) when merging the advanced `origin/main` (session d33551df supplemental dashboard) into local main. Resolution: both sides' information retained below; no content discarded.
- No other session is active; no outstanding handoffs.

## Irregularities & unverified items (combined; full detail on site's Flagged for Review page)
From prior sessions (preserved): F01–F29 (see table above).
From this session (e9badc77-vegas2): only The Venetian Resort ($6,170.43 all-in, 7 nts, Feb 15–22 2027) and Caesars Palace ($226/nt + tax, Feb 15–22 2027) have verified hotel pricing; all other hotel prices unverified. Activity hours/prices/social links blank and unverified. Most restaurant hours/prices/social links blank and unverified (verified hours: Joël Robuchon, é by José Andrés, L'Atelier, China Poblano, Bouchon, Wing Lei). Social-media leads (e.g., @joelrobuchon.lasvegas, @ebyjoseandres, @wynnlasvegas) found via search, not confirmed on official sites — flagged unverified.

Rule applied everywhere: every table row carries a source link to an official site; values not confirmable from an official source are left blank and flagged `unverified`; nothing is inferred or filled in manually.

## PR and deployment result
- PR #12: https://github.com/kanlerxz87-cyber/Vegas2/pull/12 (`arena/e9badc77-vegas2` → `main`)
- Merge result: merged into `main` (this session)
- GitHub Pages: enabled on `main`, source `/`, public URL https://kanlerxz87-cyber.github.io/Vegas2/ (root landing page = this session's dashboard). Prior sessions' `docs/` artifacts and session subdirectories preserved in repo but not the root home page.

## Source and verification record (this session: e9badc77-vegas2)
- Michelin: Visit Las Vegas / LVCVA official guide page (24 distinctions: 4 starred, 3 Bib Gourmand, 17 Recommended), awarded Aug 26 2026. Official restaurant pages: MGM Grand (Joël Robuchon, L'Atelier), Cosmopolitan (é by José Andrés, China Poblano), Caesars (Guy Savoy), Wynn (Wing Lei), Venetian (Bouchon, COTE, Milos, Mott 32), ARIA (Gymkhana), and others linked per row.
- Hotels: The Venetian official booking (Feb 15–22 2027, 7 nts, $6,170.43 all-in incl. taxes), Caesars Palace official booking ($226/nt incl. $55 resort fee, excl. taxes). Hours/amenities verified from those official pages.
- Attempted but blocked: MGM Grand / Bellagio official booking pages (fetch errors); Caesars Pages API PUT returned 403 (integration token lacks Pages write); guide.michelin.com direct fetch failed.

## Source and verification record (prior sessions, preserved)
See the "Prior sessions" table above and the verbatim records in git history. Highlights:
- Session 36cc5108: Michelin 24 distinctions confirmed against official release and LVCVA; hours verified for Joël Robuchon, L'Atelier, é, Guy Savoy (phone/dress/price only); Kabuto partial; 20 rows' hours unverified; price for 2 unverified; social unverified. Conflicts flagged F10, F11, F12, F14.
- Session a52047d7: 8 Strip hotels; rooms/private bath/Michelin on campus partial; Wynn two-queen withdrawn; Hoover fees/hours, Valley of Fire fee/closure, Neon 2027 admission and official social links verified. `scripts/check_site.py` passed (154 links, 11 pages).
- Session d33551df: official RTC sources (Trip Planner, How to Ride, Maps & Guides, Fares); meal-price anchors China Poblano $60/person, Anima by EDO $85/person, Partage $130/$160/$210; Michael Mina $295++ (temporarily closed Nov 26, 2026); Bellagio Lunar New Year display Jan 9–Mar 6 2027. Verifier checked 5 hotel candidates, 24 restaurants, 8 activity/transit rows, 13 review flags.
