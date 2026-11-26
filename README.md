# Las Vegas Trip Planner (Vegas2)

A source-first, mobile-friendly planning dashboard for a two-adult Las Vegas trip (Feb 15–Mar 23, 2027). Published with GitHub Pages from the repo root: **https://kanlerxz87-cyber.github.io/Vegas2/**

## Pages

| Path | What it is |
|---|---|
| `index.html` | Landing page and executive summary (generated) |
| `hotels.html`, `michelin.html`, `activities.html`, `booking.html`, `questions.html`, `suggestions.html`, `flagged.html`, `repo-review.html`, `sources.html` | Category subpages (generated) |
| `planner-v1.html` | Earlier single-page dashboard from PR #2/#3, kept unchanged (uses `styles.css`, `app.js`, `data.js`) |

## Source layout

| Path | What it is |
|---|---|
| `data/*.json` | Source data for every table, with verification status and source links |
| `scripts/build_site.py` | Builds the subpages from `data/*.json` (Python 3, no dependencies) |
| `scripts/check_site.py` | Verification gate: JSON validity, a source on every row, official-domain allowlist, Michelin counts, internal links |
| `assets/style.css` | Styles for the generated pages (mobile-first) |
| `.github/workflows/pages.yml` | Deploys the repo root to GitHub Pages on push to `main` |
| `COORDINATION.md` | Shared task board, sources, verification log, irregularities and PR/merge record |

## Verification rule

A value is **Verified** only when an official source confirmed it. **Partial** means an official source covers only part of the claim. Anything else is left blank and marked **Unverified**. Nothing is inferred.

## Rebuild and check

```bash
python3 scripts/build_site.py
python3 scripts/check_site.py
```

The check must print `OK` before a change is merged.

## Status

Prices for the 2027 dates, transit times and most social links are **Unverified** and listed on *Flagged for Review*. See *Questions* and *Suggestions* for what is still needed.
