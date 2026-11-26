# Vegas Field Guide

A source-linked, mobile-friendly static guide for two adults planning a Las Vegas trip in February–March 2027. It includes dated hotel quote evidence, room-fit notes, a restaurant shortlist, attraction schedules and realistic public-transit facts. Known gaps are kept on a dedicated **Review Flags** page rather than filled with assumptions.

## Pages

- `index.html` — trip overview and planning decisions
- `hotels.html` — room comparisons and verified dated booking results
- `dining.html` — restaurant search/filter, official menus/hours and carefully labeled MICHELIN status
- `experiences.html` — attractions, ticket examples and date-sensitive schedules
- `transit.html` — RTC Route 117 / Deuce transfer facts and Monorail service
- `review.html` — unresolved fees, missing rates, schedule caveats and follow-up questions

## Run locally

This site is plain HTML, CSS and JavaScript with no package install or server-side component. From the repository root:

```bash
python3 scripts/check_site.py
node scripts/test_filters.js
python3 scripts/build_pages.py
python3 -m http.server 8080
```

Open `http://localhost:8080/` in a browser. The build command creates a clean `_site/` directory for deployment; generated output is ignored by Git.

## GitHub Pages

`.github/workflows/pages.yml` builds and deploys the static artifact when commits reach `main`. `.github/workflows/validate.yml` checks pull requests and branch pushes for required pages, local file/fragment links, page landmarks, image alt attributes and sourced restaurant cards.

## Research notes

The guide’s initial research snapshot is November 26, 2026. Hotel prices, availability, fees, restaurant menus/hours, attraction prices and transit schedules can change. Hotel prices shown are date- and occupancy-specific first-party outputs; tax treatment is called out. Menu examples are not full meal budgets. Every key listing links to an official venue, booking or MICHELIN Guide source. See `COORDINATION.md` for the detailed research log and unresolved fee comparison.
