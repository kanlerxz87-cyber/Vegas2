# Vegas2 — Las Vegas trip planner

A static dashboard for planning a 2-adult trip to Las Vegas (Feb 15–22, 2027, with a Feb 15–18 option).
It is published with GitHub Pages from the repo root:
**https://kanlerxz87-cyber.github.io/Vegas2/**

## What is here

| Path | What it is |
|---|---|
| `index.html`, `hotels.html`, `michelin.html`, `activities.html`, `booking.html`, `questions.html`, `suggestions.html`, `flagged.html`, `repo-review.html`, `sources.html` | Generated site pages (do not edit by hand) |
| `data/*.json` | The source data for every table, with verification status and source links |
| `scripts/build_site.py` | Builds the HTML pages from `data/*.json` (Python 3, no dependencies) |
| `scripts/check_site.py` | Verification gate: JSON validity, source links on every row, official-domain allowlist, Michelin counts, internal links |
| `assets/style.css` | Styles (mobile-first) |
| `COORDINATION.md` | Shared task board, sources, verification log, irregularities and PR/merge record |

## Verification rule

A value is shown as **Verified** only when an official source confirmed it. A **Partial** value is covered
only in part by an official source. Anything else is left blank and marked **Unverified**. Nothing is inferred.

## Rebuild and check

```bash
python3 scripts/build_site.py
python3 scripts/check_site.py
```

The check must print `OK` before a change is merged.

## Status

Prices for the 2027 dates, transit times and most social links are **unverified** and are listed on the
*Flagged for Review* page. See *Questions* and *Suggestions* for what is needed next.
