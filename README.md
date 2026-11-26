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
