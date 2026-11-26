# Vegas2 — Las Vegas trip planner (Feb 15 – Mar 23, 2027)

Live site (GitHub Pages, served from `docs/`): **https://kanlerxz87-cyber.github.io/Vegas2/**

## Published pages (what each URL is)

| URL path | What it is | Built by |
|---|---|---|
| `/` (`docs/index.html`) | **Verified landing page** and dashboard: executive summary, hotels, Michelin, activities, booking, questions, suggestions, Flagged for Review, repo review, sources | `scripts/build_site.py` |
| `/session-36cc5108/` | Parallel site from PR #6, unchanged (its own data in `data/*.json`) | `site/build.py` (output moved to this folder during integration) |
| `/planner-v1/` | First single-page dashboard from PRs #2/#3, unchanged | copied static files |
| `/session-d33551df/` | Supplemental source-first hotel, Michelin, activity and review dashboard | `site/publish-supplement.py` |

## Verified site (this session, a52047d7)

| Path | What it is |
|---|---|
| `data/verified/*.json` | Source data for every table: hotels, Michelin, activities, booking, questions, suggestions, flagged, repo review, sources. Every row has a source; unverified values are blank and flagged |
| `scripts/build_site.py` | Builds `docs/*.html` and `docs/assets/style.css` from `data/verified/` (Python 3 standard library) |
| `scripts/check_site.py` | Verification gate: JSON validity, a source on every row, official-domain allowlist, Michelin counts (4 starred / 3 Bib / 17 Recommended = 24), internal links, placeholder text |
| `assets/style.css` | Source stylesheet (copied into `docs/assets/`) |

Rebuild and check (run in this order; both must pass):

```bash
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 site/build.py      # rebuilds /session-36cc5108/ only
```

Verification rule: a value is **Verified** only when an official source confirmed it. **Partial** means an official source covers only part of the claim. Everything else is left blank and marked **Unverified**. Nothing is inferred.

## Integration notes

- `main` gained a second site (`docs/`, `site/build.py`) from PR #6 while this branch was open. Both builds are kept. Their output moved from `docs/` to `docs/session-36cc5108/` so the two builds cannot delete each other's pages.
- The Pages workflow (`.github/workflows/pages.yml`) deploys `docs/` and is unchanged.
- Root-level `index.html`, `styles.css`, `app.js`, `data.js` are the v1 dashboard source, kept unchanged. Their copy for publishing is `docs/planner-v1/`.

---

## Readme from the other session (session 36cc5108), kept verbatim

# Vegas2 — Las Vegas trip planner (Feb 15 – Mar 23, 2027)

Live site (GitHub Pages): https://kanlerxz87-cyber.github.io/Vegas2/

## What is here

| Path | Purpose |
|------|---------|
| `docs/` | Generated static site served by GitHub Pages (do not edit by hand) |
| `site/build.py` | Builds `docs/` from `data/` (standard library only) and fails on missing sources, undefined flags or broken links |
| `data/hotels.json` | Hotel shortlist, in-resort Michelin ranking, resort fee (verified only where official), blanks for anything unverified |
| `data/restaurants.json` | All 24 Las Vegas listings in the 2026 MICHELIN Guide Southwest, with official addresses |
| `data/activities.json` | Activities checked against official pages |
| `data/sources.json` | Source registry (every row cites one or more of these IDs) |
| `data/flags.json` | Irregularities, conflicts and unverified items (published on "Flagged for Review") |
| `data/questions.json` | Questions and information gaps, with known / missing / how-to-find |
| `data/suggestions.json` | Proposed site and data changes. Nothing is implemented until approved |
| `data/repo_review.json` | Line-by-line repository review |
| `COORDINATION.md` | Shared task board, claims, logs and handoffs |

## Rebuild

```bash
python3 site/build.py
```

Exit code 0 means every row has a source, every flag resolves and every internal link works.

## Verification rule

A value appears only when an official source confirmed it. Anything else is left blank and marked **Unverified**, with a flag ID linking to the review list. Third-party sources are used only to flag conflicts.

## Other dashboard in this repository

The earlier dashboard from another session now lives in `legacy-dashboard/` (moved with `git mv`, nothing deleted). The root `index.html` redirects to `docs/`, which is the published site (see F27). Their README, preserved verbatim, follows:

---

# Las Vegas Trip Planner

A source-first, mobile-friendly planning dashboard for a two-adult Las Vegas trip (Feb 15–Mar 23, 2027). Open `index.html` locally or publish this repository with GitHub Pages.

## Verification and limits

The dashboard separates published facts from unknowns. Dynamic hotel rates and total tax-inclusive prices for Feb 15–22, 2027, restaurant menu totals, transit journey times and future opening hours are not represented as verified unless a cited official source provides them. Blank values are deliberately flagged rather than estimated. Recheck all information before booking.

The 2026 MICHELIN Guide search identified several Las Vegas listings, including three starred restaurants. Individual current Guide listings are linked. Guide presence and star status are explicitly distinguished.

## Deploy

GitHub repository Settings → Pages → Deploy from a branch → `main` / `/ (root)`, or use the included Pages workflow on pushes to `main`.

## Files

- `index.html`: single-page dashboard with category navigation.
- `styles.css`: responsive styling.
- `app.js`: interactive navigation and filtering.
- `COORDINATION.md`: task board, sources, verification notes and flagged gaps.

## Supplemental source-first dashboard (session `d33551df`)

This session's separately labeled comparison dashboard is published at [`/session-d33551df/`](docs/session-d33551df/index.html) (and, after the Pages deployment completes, `https://kanlerxz87-cyber.github.io/Vegas2/session-d33551df/`). It preserves this repository's existing `docs/` landing page and other session sub-sites.

Source files and the publication copy are `site/*.html`, `site/assets/`, and `docs/session-d33551df/`. Recreate only this supplemental subdirectory with `python3 site/publish-supplement.py`; it does not overwrite `docs/index.html` or other session paths. Validate with `node site/verify.cjs`.
