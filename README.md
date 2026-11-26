# Vegas2 — Las Vegas trip planner

A static, mobile-friendly dashboard for planning a Las Vegas trip (window: Feb 15 to Mar 23, 2027).
Published with GitHub Pages from the `docs/` folder on `main`.

**Live site:** https://kanlerxz87-cyber.github.io/Vegas2/ (after the Pages source is set to `main` / `docs`)

## What is in the site
- **Home**: executive summary and headline numbers
- **Hotels**: candidates ranked by MICHELIN listings in the same resort, with bed/bath/price status
- **Michelin**: all 24 official Las Vegas listings (2026 MICHELIN Guide Southwest), clusters, hours where verified
- **Activities**: attractions with official hours, fees, reservation rules and social links where official
- **Transit & dates**: RTC bus, Las Vegas Monorail, key dates (OPM federal holidays)
- **Booking timing**: promotions and booking windows printed on official pages
- **Questions**, **Suggestions** (for review, not implemented), **Flagged for Review**, **Repo review**, **Sources**

## Rules used
- Every published row carries at least one official-source link.
- Any value not confirmed on an official source is left blank and shown as **Unverified**. These are listed automatically on the Flagged for Review page.
- Michelin awards come from the official MICHELIN press release; the Visit Las Vegas list is used for cuisine and venue links.

## How the site is built
Data lives in `data/*.json`. The generator is dependency-free Node:

```bash
node scripts/build.mjs      # verifies data rules, regenerates docs/, checks internal links
node scripts/linkcheck.mjs  # reports external links that do not return OK (run in CI; warning only)
```

`build.mjs` fails (non-zero exit) if a source is not on the official-domain list, a Michelin tier count does not match the official totals, a hotel ranking is out of order, or an internal link is broken.

CI: `.github/workflows/pages-check.yml` rebuilds the site and fails if the committed `docs/` differs from the build output.

## Coordination
See `COORDINATION.md` for the task board, claims, overlap with other session branches, and the log.
