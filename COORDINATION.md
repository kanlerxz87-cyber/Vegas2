# COORDINATION.md — Shared task board (Vegas2)

Multi-session repo integration. All work is on the Arena-fixed branch `arena/e9badc77-vegas2`; the brief's `session-<id>/<task>` branch naming cannot be used (Arena pins the branch). No other session is active on this repo right now.

Status values: `unclaimed` · `in progress` · `done` · `needs review` (published on Flagged for Review; does not block anything)

## Integration summary (this session: e9badc77-vegas2)
Merged `origin/main` (prior sessions 36cc5108, a52047d7, f0943026, e94404fc) into `arena/e9badc77-vegas2`. Two add/add conflicts surfaced:
- `index.html`: prior root index.html was a redirect to `docs/index.html`; this session's full dashboard landing page is kept as the root landing page (served from GitHub Pages root `/`). Prior `docs/` site preserved untouched under `docs/`.
- `COORDINATION.md`: combined below; nothing deleted.

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
| 13 | Enable GitHub Pages, confirm deploy, no broken links | done | e9badc77-vegas2 | repo Pages settings | Pages already enabled on main `/`; URL https://kanlerxz87-cyber.github.io/Vegas2/ |
| 14 | Create PR from integration to main, merge, record PR link + result | done | e9badc77-vegas2 | GitHub PR #12 | merged to main |

### Prior sessions (preserved verbatim from origin/main)
| ID | Task | Status | Owner | File scope | Notes |
|----|------|--------|-------|------------|-------|
| (f0943026) | Research-backed Vegas trip planner + GitHub Pages site (base) | done | f0943026 | COORDINATION.md, README.md, index.html, styles.css, data.js, .github/workflows/pages.yml | initial base implementation |
| (e94404fc) | Mobile-first summaries, hotel shortlist, dining/activity tables, questions, review flags | done | e94404fc | index.html, styles.css, app.js, README.md, .nojekyll, COORDINATION.md | expansion |
| T0 (36cc5108) | Repo review + irregularity flags | done | 36cc5108 | data/repo_review.json, data/flags.json (F25–F27) | |
| T1 (36cc5108) | Hotels: shortlist, Michelin ranking, resort fee, trip-date options | done (prices/room specs flagged unverified) | 36cc5108 | data/hotels.json | 7-night totals, queen/private bath unverified (F05, F06) |
| T2 (36cc5108) | Michelin restaurants (2026 Southwest, Las Vegas, 24 rows) | done (hours partly unverified F17–F19) | 36cc5108 | data/restaurants.json | hours/price/social unverified for most rows |
| T3 (36cc5108) | Activities within transit/drive limits, official pages | done (Hoover Dam hours unverified F09) | 36cc5108 | data/activities.json | |
| T4 (36cc5108) | Questions, suggestions, sources | done | 36cc5108 | data/questions.json, data/suggestions.json, data/sources.json | suggestions S-01–S-14 awaiting approval |
| T5 (36cc5108) | Static site (landing, category pages, Flagged for Review) | done (builds 0 errors) | 36cc5108 | site/build.py, docs/**, README.md | |
| T6 (36cc5108) | Integration: re-check, build, link check, PR, merge, Pages | done | 36cc5108 | all | PR #6 merged; /docs source 403, stayed main `/` |
| T1–T10 (a52047d7) | Repo review, hotels, Michelin, activities, booking, questions, suggestions, flags, site build, integration | done / needs review | a52047d7 | data/verified/**, docs/*.html, scripts/** | flags F1–F18 published, needs review |

## Claims log
- e9badc77-vegas2: claimed tasks 1–14; completed and committed all; merged origin/main and resolved conflicts; created PR #12 and merged to main.
- Prior session claims are preserved above verbatim.

## Handoffs / conflicts
- 2026-11-26 · e9badc77-vegas2 · Merge conflict: `index.html` (add/add) and `COORDINATION.md` (add/add) when merging `origin/main` into `arena/e9badc77-vegas2`. Resolution: both sides kept; nothing deleted. Root index.html = this session's dashboard; prior redirect-to-docs index.html superseded at root but `docs/` site preserved intact. COORDINATION.md combined above.
- No other session is active; no outstanding handoffs.

## Irregularities & unverified items (combined; full detail on site's Flagged for Review page)
From prior sessions (preserved): F01–F29 — includes: no subway in Las Vegas (RTC bus + Strip monorail only); Red Rock Canyon no public transit; trip-length conflict (3-night preferred vs 7-night cost basis vs 1–2 weeks); Feb 15 2027 = Washington's Birthday (federal holiday); queen-or-larger bed and private bathroom unverified for most hotels; 7-night totals / best time to book unverified; most restaurant hours, per-couple prices, and social links unverified; Hoover Dam hours not retrievable from current official page; MICHELIN awards are 2026 selection, not a guarantee of 2027 status.

From this session (e9badc77-vegas2): only The Venetian Resort ($6,170.43 all-in, 7 nts, Feb 15–22 2027) and Caesars Palace ($226/nt + tax, Feb 15–22 2027) have verified hotel pricing; all other hotel prices unverified. Activity hours/prices/social links blank and unverified. Most restaurant hours/prices/social links blank and unverified (verified hours: Joël Robuchon, é by José Andrés, L'Atelier, China Poblano, Bouchon, Wing Lei). Social-media leads (e.g., @joelrobuchon.lasvegas, @ebyjoseandres, @wynnlasvegas) found via search, not confirmed on official sites — flagged unverified.

Rule applied everywhere: every table row carries a source link to an official site; values not confirmable from an official source are left blank and flagged `unverified`; nothing is inferred or filled in manually.

## PR and deployment result
- PR #12: https://github.com/kanlerxz87-cyber/Vegas2/pull/12 (`arena/e9badc77-vegas2` → `main`)
- Merge result: merged (this session)
- GitHub Pages: enabled on `main`, source `/`, public URL https://kanlerxz87-cyber.github.io/Vegas2/ (root landing page = this session's dashboard). Prior sessions' `docs/` artifact preserved in repo but not the root home page.

## Source and verification record (this session)
- Michelin: Visit Las Vegas / LVCVA official guide page (24 distinctions: 4 starred, 3 Bib Gourmand, 17 Recommended), awarded Aug 26 2026. Official restaurant pages: MGM Grand (Joël Robuchon, L'Atelier), Cosmopolitan (é by José Andrés, China Poblano), Caesars (Guy Savoy), Wynn (Wing Lei), Venetian (Bouchon, COTE, Milos, Mott 32), ARIA (Gymkhana), and others linked per row.
- Hotels: The Venetian official booking (Feb 15–22 2027, 7 nts, $6,170.43 all-in incl. taxes), Caesars Palace official booking ($226/nt incl. $55 resort fee, excl. taxes). Hours/amenities verified from those official pages.
- Attempted but blocked: MGM Grand / Bellagio official booking pages (fetch errors); Caesars Pages API PUT returned 403 (integration token lacks Pages write); guide.michelin.com direct fetch failed.
