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

**T1 Hotels.** Sources: Michelin release (S01, S02) for every hotel-to-restaurant address match; Caesars booking page (S08) for the only verified resort fee ($62.30/night incl. $7.35 tax); Caesars home page (S09) and Cosmopolitan home page (S20) for booking-offer types. Not verified (left blank, flagged): 7-night totals (F06), queen-or-larger bed and private bathroom (F05), resort fees other than Caesars (F08), best time to book (F04). Third-party resort-fee reports (S22) were not used as values.

**T2 Michelin restaurants.** Sources: Michelin press release (S01) and WebWire copy (S02) for all 24 distinctions and addresses; LVCVA page (S03) for area, cuisine and official site links. Hours verified from official pages: Joël Robuchon (S04), L'Atelier (S05), é (S06); Guy Savoy (S07) phone, dress and price symbol only. Kabuto (S16) hours are partial (official captions). Not verified: hours for 20 rows (F17), price for 2 for all rows (F18), social accounts for all restaurants (F19). Conflicts flagged: F10, F11, F12, F14.

**T3 Activities.** Sources: BLM Red Rock (S13), NV State Parks Valley of Fire (S14), Las Vegas Monorail (S12), Neon Museum (S15); Hoover Dam official site could not be retrieved (S21 archive from 2010 and S27 third-party conflict) so its hours are blank (F09).

**T4 Questions, suggestions, sources.** Sources: OPM 2027 federal holidays (S10) for Feb 15, 2027. Suggestions S-01 to S-14 are proposals only and are awaiting approval.

**T5 Site.** Built by `site/build.py` (standard library). Last build: 10 pages, 0 errors (strict source checks; internal links and anchors resolved).

## Irregularities for review (summary; full text on Flagged for Review)

- Brief says "subway or bus"; official sources show RTC bus and the Strip monorail, no subway (F01).
- Red Rock Canyon has no public transit (BLM, S13); it cannot meet the bus-only one-hour test (F02).
- Trip length conflict: 3-night preferred vs 7-night cost basis vs 1–2 weeks (F03).
- Feb 15, 2027 is Presidents' Day (OPM, S10) (F13).
- Yen Viet Kitchen: Bib Gourmand (official release) vs Recommended (Time Out) (F14).
- Guy Savoy hours: official page shows none; three listings conflict (F10).
- Hoover Dam hours: current official page not retrievable; sources conflict (F09).

## Session log

- 2026-11-26 · 36cc5108 · Claimed T0–T6. Repo held only `README.md`; created this file. Pages was enabled on `main` (legacy, `/`), so the site will be served from `/docs` after merge.
- 2026-11-26 · 36cc5108 · Completed research and data for T0–T4 against official sources (retrieved this session). Built the site (T5) with 0 errors.
- 2026-11-26 · 36cc5108 · T6 integration check: re-counted Michelin listings (4 starred, 3 Bib, 17 Recommended = 24) against the release; fixed one official name ("Stubborn Seed Las Vegas"); verified every source and flag ID is defined and referenced; verified trip weekdays (Feb 15 Mon, Feb 18 Thu). Next: PR, merge, Pages source to `/docs`, deploy check.
