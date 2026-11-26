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
