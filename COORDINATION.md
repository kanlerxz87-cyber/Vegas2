# Shared Task Board — Las Vegas Trip Planning

Last updated: 2026-11-26 (UTC)

## Working agreement
- Arena fixes this session to one branch: `arena/059c3126-vegas2` (base `c97c82a` on `main`). All work for this session is committed and pushed only to that branch.
- Other branches already exist on the remote with their own claims of the same overall scope (see Overlap below). This session did not switch to or push to them. The final integration step must reconcile those branches before anything is merged to `main`.
- Shared outputs (`data/`, `scripts/`, `docs/`, `index`/navigation) are owned by this branch's session for this run.

## Tasks

| Task | Status | Owner / session | Branch | File scope |
|---|---|---|---|---|
| Las Vegas trip research: hotels, Michelin restaurants, activities, transit, dates, booking timing | in progress | `059c3126` | `arena/059c3126-vegas2` | `data/**`, `scripts/**`, `docs/**`, `README.md`, `COORDINATION.md`, `.github/workflows/**` |
| Repo review (line-by-line of repo state, branches, brief) | in progress | `059c3126` | `arena/059c3126-vegas2` | `data/repo-review.json` |
| GitHub Pages site build, checks, flagged-for-review page | in progress | `059c3126` | `arena/059c3126-vegas2` | `scripts/**`, `docs/**`, `.github/workflows/**` |

## Overlap with other session branches (logged, not resolved here)
- `origin/arena/2e5e3452-vegas2` (commit `d84919a`) claims "Las Vegas trip-planning research, accessible multi-page site, review flags, build/deploy verification, and final integration" with file scope `COORDINATION.md`, `README.md`, `index.html`, `assets/**`, `data/**`, `pages/**`, `scripts/**`, `styles/**`, `.github/workflows/**`, `package.json`.
- `origin/arena/e94404fc-vegas2` (commit `1ae27b1`) claims "Build initial Las Vegas trip-planning dashboard, source policy, and flagged items" with scope "all project files".
- Both overlap with this branch's scope. Integration must pick one site build (this branch uses `docs/` from `scripts/build.mjs`), merge the verified data, and avoid duplicate pages. Flagged for the integration session.

## Verification policy (applied on this branch)
- A value is published only if it was read on an official source page this session. The source URL is stored with the row.
- Anything not confirmed is left blank (`null`) and is rendered as **Unverified**. Unverified fields are listed automatically on the Flagged for Review page.
- Michelin awards: taken from the official MICHELIN Guide press release (michelin.com), cross-checked against the LVCVA (visitlasvegas.com) list. Third-party reprints were not used as the basis for any award.
- Hotel prices, 7-night totals, price-per-couple restaurant costs, and "cheapest time to book" were NOT found on official sources for the requested dates. They are blank and flagged.

## Log
- 2026-11-26 — Read repo: only `README.md` (`# Vegas2`) on `main`. No COORDINATION.md on this branch; it was created here.
- 2026-11-26 — Claimed the task on this branch (see table). Read-only review of the other two session branches' COORDINATION.md files (no edits made to them).
- 2026-11-26 — Verified Michelin Southwest 2026 Las Vegas list from michelin.com press release (4 Stars, 3 Bib Gourmand, 17 Recommended = 24 Las Vegas entries). Visit Las Vegas (LVCVA) page used for cuisine labels and venue links.
- 2026-11-26 — Verified federal holiday on Mon Feb 15, 2027 (Washington's Birthday) from opm.gov.
- 2026-11-26 — Note on fetch limits: `guide.michelin.com` and several hotel room pages (Venetian `/hotel/rooms.html`, Bellagio `/hotel/rooms.html`) and the Bellagio fountains page did not load through the fetch tool. Those items are left unverified.
