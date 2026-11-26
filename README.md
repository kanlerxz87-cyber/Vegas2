# Vegas2 — Las Vegas trip planning dashboard

A mobile-friendly, source-linked planning dashboard for two adults considering Las Vegas dates from **February 15 through March 23, 2027**.

## Open the dashboard

- [Overview](site/index.html)
- [Hotels & room comparison](site/hotels.html)
- [2026 MICHELIN restaurants](site/restaurants.html)
- [Activities & transit](site/activities.html)
- [Analysis, knowns, Q&A & improvement ideas](site/analysis.html)
- [Flagged for Review](site/flagged.html)

After GitHub Pages is enabled and the Actions workflow succeeds, the same pages are published from the `site/` directory.

## Important planning caveats

- Preferred dates **Feb 15–18, 2027** are three nights, while the requested trip length is one to two weeks. The separate seven-night **Feb 15–22** rate check is a comparison scenario, not a substitute itinerary.
- Caesars Palace produced inconsistent dated displays for Feb 15–22: an earlier capture showed **$226/night**, while a later official recheck displayed the Julius Deluxe King at **$201/night** ($146 room rate + $55 resort fee, taxes excluded) and a room-assigned option at **$196/night**. The flexible calendar summed to **$1,580**; the later booking page also showed a technical-difficulties notice. The seven-night total is intentionally left unconfirmed.
- The other hotel date-price checks were not reliable enough for a like-for-like comparison. No market-wide cheapest stay is claimed.
- The hotel ranking by MICHELIN restaurants reachable within one hour by bus is pending RTC date/time route checks. Blank reach counts mean **unmeasured**, not zero.
- Unconfirmed prices, hours, exceptions and social accounts remain blank and are listed on the review page. Restaurant MICHELIN distinctions are explicitly separated.

## Local preview and validation

From the repository root:

```sh
python3 -m http.server 8000 --directory site
```

Then open `http://localhost:8000`. The site is static HTML/CSS/JavaScript and has no package install step. Validate the source data with:

```sh
node site/verify.cjs
```

GitHub Actions runs the same validation before deploying `site/` to GitHub Pages.

Research snapshot: **November 26, 2026**. Rates, inventory, hours, transit schedules and ticket prices may change before travel; always recheck the linked official source before paying or booking.
