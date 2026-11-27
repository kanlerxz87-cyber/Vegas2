# Vegas2 — Las Vegas trip planner (Feb 15 – Mar 23, 2027)

**Live site:** https://kanlerxz87-cyber.github.io/Vegas2/
**Canonical build:** the repository root (`/index.html` + 10 subpages), generated from `data/plan/*.json` by `scripts/build_plan.py`.

Two adults, one room, Las Vegas. Preferred dates Feb 15–18, 2027; allowed range Feb 15 – Mar 23, 2027. Hotel costs are shown on a 7-night basis (Feb 15–22, 2027).

## What is here

| Path | Purpose |
|---|---|
| `index.html` + 10 subpages | Canonical mobile-first planner: overview, MICHELIN restaurants, hotels, prices & dates, activities, transit, questions, suggestions, flagged for review, repo review, sources |
| `data/plan/*.json` | The only source of truth for the site. Every value carries its official source; unverified values are blank |
| `scripts/build_plan.py` | Renders the 11 root pages from `data/plan/` (Python 3 standard library only) |
| `scripts/check_plan.py` | Verification gate: JSON integrity, MICHELIN counts (4 starred / 3 Bib / 17 listed), a source on every row, hotel arithmetic, internal links, table/header consistency, placeholder scan |
| `assets/site/style.css` | The site stylesheet (tables stack into labelled cards under 640 px) |
| `docs/` | All seven earlier session sites, preserved unchanged (plus `docs/session-legacy-root/`, the archive of the previous root pages) |
| `COORDINATION.md` | Shared task board, claims, handoffs and results across sessions |

## Build and verify

```bash
python3 scripts/build_plan.py
python3 scripts/check_plan.py     # exit 0 = passed
```

CI: `.github/workflows/validate-plan.yml` rebuilds and checks on every push/PR, and fails if the committed pages are out of date.

## Verification rule

A value is shown only when an official first-party source states it, and the row links to that source. Anything that could not be confirmed is **left blank** and listed on `flagged.html` with a severity, its effect on the decision and the source used. No price, travel time, opening hour or social handle is ever inferred. Hotel totals are room + resort fee and **exclude taxes**, because no booking engine captured here published the tax amount.

Key captures (2026-11-27): the official Las Vegas MICHELIN page (24 distinctions), Caesars Entertainment dated rate pages for Feb 15–22, 2027 (Flamingo, Paris, Caesars Palace), the South Point booking engine for three date windows, and official venue pages for hours and prices.

## Earlier versions

Seven prior sessions published their own planners. They remain in `docs/` and in git history and are not edited by this build:

- `docs/index.html` and `docs/*.html` — verified dashboard (session a52047d7)
- `docs/session-059c3126/` — planner build (session 059c3126)
- `docs/session-36cc5108/` — source-first site (session 36cc5108)
- `docs/session-d33551df/` — supplemental dashboard (session d33551df)
- `docs/session-b29fc34e/` — field guide (session b29fc34e)
- `docs/session-2e5e3452/` — field notes (session 2e5e3452)
- `docs/planner-v1/` — first single-page dashboard
- `docs/session-legacy-root/` — archive of the root pages this build replaced

`field-notes/`, `site/`, `legacy-dashboard/`, `data/`, `data/verified/` and `data/trip/` are the source trees for those older builds. They are kept as provenance.
