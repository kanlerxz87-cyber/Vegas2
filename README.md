# Vegas2 — Las Vegas trip planner (Feb 15 – Mar 23, 2027)

Live site (GitHub Pages): https://kanlerxz87-cyber.github.io/Vegas2/

Two sites are published from `docs/`:

| Path | What it is | Built by |
|------|-----------|----------|
| `docs/` (root) | This session's planner: executive summary, hotels, Michelin restaurants, activities, transit and dates, booking timing, questions, suggestions, Flagged for Review, repo review, sources | `scripts/build.mjs` from `data/trip/*.json` |
| `docs/legacy/` | The other session's dashboard (kept unchanged for comparison; linked from the landing page) | `scripts/build-legacy.py` (wraps `site/build.py`) from `data/*.json` |

## Layout

| Path | Purpose |
|------|---------|
| `data/trip/*.json` | Source data for the planner (every value cites an official source; unverified values are blank and flagged) |
| `scripts/build.mjs` | Builds the planner into `docs/` and runs the verification rules. Exit 0 = passed |
| `scripts/build-legacy.py` | Builds the other dashboard into `docs/legacy/` without editing its code |
| `scripts/linkcheck.mjs` | Checks external links (warning-only; intended for CI) |
| `scripts/style.css` | Planner stylesheet (copied to `docs/assets/style.css`) |
| `.github/workflows/pages-check.yml` | CI: runs both builds and fails if committed `docs/` is out of date |
| `.github/workflows/pages.yml` | Deploys `docs/` to GitHub Pages on push to `main` |
| `COORDINATION.md` | Shared task board, claims, logs and handoffs |

## Rebuild

```bash
node scripts/build.mjs          # planner -> docs/
python3 scripts/build-legacy.py # other dashboard -> docs/legacy/
node scripts/linkcheck.mjs      # optional, needs outbound web access
```

## Verification rule

A value appears only when an official source confirmed it. Anything else is left blank and marked **Unverified**, with a flag ID that links to the Flagged for Review page. Third-party sources are used only to flag conflicts.

---

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
