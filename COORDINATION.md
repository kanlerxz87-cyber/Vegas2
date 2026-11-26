# COORDINATION.md — Shared task board (Vegas2)

Branch in use: `arena/36cc5108-vegas2` (fixed for this session; the `session-<id>/<task>` naming in the brief could not be used because Arena tracks this session by its branch). All sessions commit to this branch; scopes below are kept non-overlapping.

Legend: `unclaimed` · `in progress` · `done` · `needs review` (published on the Flagged for Review page; does not block anything)

## Tasks

| ID | Task | Status | Owner (session) | Claimed (UTC) | File scope |
|----|------|--------|-----------------|---------------|------------|
| T0 | Repo review + irregularity flags | in progress | 36cc5108 | 2026-11-26 | `docs-src/` repo-review data, `data/repo_review.json` |
| T1 | Hotels research (Feb 15–Mar 23 2027 window, 7-night basis, Michelin cluster ranking) | in progress | 36cc5108 | 2026-11-26 | `data/hotels.json` |
| T2 | Michelin restaurants (official Southwest 2026 list, Las Vegas) + social links | in progress | 36cc5108 | 2026-11-26 | `data/restaurants.json` |
| T3 | Activities within 1 hour of hotel clusters + social links | in progress | 36cc5108 | 2026-11-26 | `data/activities.json` |
| T4 | Questions / info gaps, suggestions (for approval only), source registry | in progress | 36cc5108 | 2026-11-26 | `data/questions.json`, `data/suggestions.json`, `data/sources.json`, `data/flags.json` |
| T5 | Static site build (landing + category subpages + Flagged for Review) | in progress | 36cc5108 | 2026-11-26 | `site/build.py`, `docs/**` (GitHub Pages source: `/docs`) |
| T6 | Integration: merge, re-verify combined data, build, link check, PR to `main`, merge, confirm Pages | pending (after T0–T5) | 36cc5108 | — | all |

## Session log

- 2026-11-26 · 36cc5108 · Claimed T0–T6. Repo found with only `README.md`; no `COORDINATION.md` existed, so it was created here. Pages is already enabled on `main` (legacy, source `/`), serving `https://kanlerxz87-cyber.github.io/Vegas2/`. Plan: change Pages source to `/docs` after merge so the generated site is served without cluttering the root.
