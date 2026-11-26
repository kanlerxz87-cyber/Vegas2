# Las Vegas Trip Planner

A source-first, mobile-friendly planning site for two adults considering a Las Vegas trip within Feb 15–Mar 23, 2027. Open `index.html` locally using a static HTTP server or publish the repository with GitHub Pages.

## Pages and data

- `index.html`: dashboard and navigation hub.
- `hotels.html`: eight hotel candidates, same-property 2026 MICHELIN counts, official room-category evidence and booking links.
- `restaurants.html`: all 24 Las Vegas restaurants in the 2026 MICHELIN selection (4 starred, 3 Bib Gourmand, 17 Selected).
- `activities.html`: official activity / transit references and date-sensitive prices where captured.
- `dates.html`: 30 calculated seven-night windows within the requested outer range.
- `questions.html`, `suggestions.html`, `flagged.html`: decisions, optional enhancements and unresolved verification items.
- `data/*.json`: structured, source-linked content; `assets/app.js` renders searchable and filterable tables.
- `styles.css`: responsive shared styling.
- `COORDINATION.md`: task board, research log and deployment history.

## Verification and limits

Published facts are separated from unknowns. No exact 2027 hotel total, lowest-price stay date, advance booking lead time, selected-room availability, restaurant total for two or unverified hotel-origin transit time is claimed. The preferred Feb 15–18 window is three nights, while the requested duration is one–two weeks; no final trip length is assumed. Blank values are deliberate and flagged. Recheck schedules, prices, room terms and availability before booking.

The restaurant distinction counts reflect the 2026 MICHELIN selection, not a prediction of 2027 awards. Hotel room pages confirm candidate room types, not live date-specific inventory or every private/ensuite configuration. Current ticket fares and attraction schedules may change.

## Run locally

From the repository root, run `python3 -m http.server 8000 --bind 0.0.0.0`, then open `http://localhost:8000`. The pages require HTTP so the browser can fetch JSON files.

## Deploy

GitHub repository Settings → Pages → Deploy from a branch → `main` / `/ (root)`, or use the included Pages workflow on pushes to `main`.
