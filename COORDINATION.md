# Coordination board — Vegas2 trip planner

## Completed work by earlier sessions

| Task | Status | Owner | Files |
|---|---|---|---|
| Research-backed Vegas trip planner and GitHub Pages base implementation | Done | `arena/f0943026-vegas2` | `COORDINATION.md`, `README.md`, `index.html`, `styles.css`, `data.js`, `.github/workflows/pages.yml` |
| Expand source-first dashboard with initial shortlist, open questions, and flags | Done | `arena/e94404fc-vegas2` | `index.html`, `styles.css`, `app.js`, `README.md`, `.nojekyll`, `COORDINATION.md` |

## Current session claim

**Session:** `fd2715d0`  
**Current Arena branch:** `arena/fd2715d0-vegas2` (fixed; no branch switch)  
**Repo:** `kanlerxz87-cyber/Vegas2`  
**Base originally seen:** `c97c82a`; upstream `main` advanced during this work to include PRs #1–#3.  
**Scope claimed:** audit and correct/add mobile-first category pages and structured verified data; add standalone Questions, Suggestions, and Flagged for Review pages; integrate with the existing site; validate; open and merge PR; confirm Pages deployment.  
**Files:** `COORDINATION.md`, `README.md`, `index.html`, `styles.css` only if requested through integration, `data.js` only if necessary to integrate, `data/*.json`, `assets/*`, `hotels.html`, `restaurants.html`, `activities.html`, `dates.html`, `questions.html`, `suggestions.html`, `flagged.html`.

> This session started from a stale local checkout. The main branch already contained the prior sessions' merged dashboard and verification log; those files and claims are being preserved and extended, not removed. The claim commit is being rebased onto the latest `main`. No other active claim has been observed on the current branch after fetching upstream.

## Task board

| Task | Status | Owner | Files |
|---|---|---|---|
| Preserve prior site and audit current implementation | In progress | `fd2715d0` | existing root files, `COORDINATION.md` |
| Michelin list, award status, official profile links | In progress | `fd2715d0` | `data/restaurants.json`, `restaurants.html` |
| Hotel candidates, rates, room-fit and Michelin cluster methodology | In progress | `fd2715d0` | `data/hotels.json`, `hotels.html` |
| Activities, hours, exceptions and social links | In progress | `fd2715d0` | `data/activities.json`, `activities.html` |
| Date-window and booking analysis | In progress | `fd2715d0` | `data/dates.json`, `dates.html` |
| Mobile dashboard and navigation integration | In progress | `fd2715d0` | `index.html`, `assets/*` |
| Standalone Questions, Suggestions, Flagged for Review pages | In progress | `fd2715d0` | `questions.html`, `suggestions.html`, `flagged.html` |
| Final verification, PR, merge, live deploy | Not started | `fd2715d0` | all final deliverables |

## Verification log

### Prior sessions — retained as historical records

- Session `f0943026`: Michelin entry/status checks and static-page checks are described in the prior log and source links. No 2027 hotel quote was claimed.
- Session `e94404fc`: official MGM Grand, Venetian, Caesars Palace, Wynn and MICHELIN pages were checked; local anchors/files and Pages deployment were checked. The earlier dashboard explicitly left rates, travel times, social links and future schedules unverified. PR #2 is recorded below.

### Current session — direct official-source checks

- Official MICHELIN Guide Las Vegas index: https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurants — official listing page reports 1–24 of 24. The official 2026 Southwest release gives the starred list, addresses and Recommended list: https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s.
- Official MICHELIN profile checks returned by web search for individual entries include: Restaurant de Joël Robuchon (Two Stars), https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/restaurant-de-joel-robuchon; L'Atelier, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/l-atelier-de-joel-robuchon-las-vegas; é by José Andrés, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/e-by-jose-andres; Guy Savoy, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/guy-savoy-las-vegas; China Poblano, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/china-poblano; Esther's Kitchen, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/esther-s-kitchen; YEN Viet Kitchen, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/yen-viet-kitchen; Anima by Edo, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/anima-by-edo; Bouchon, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/bouchon-1250929; COTE Las Vegas, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/cote-las-vegas; Estiatorio Milos, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/estiatorio-milos-1250934; Gymkhana Las Vegas, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/gymkhana-las-vegas; Kabuto, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/kabuto; Kame Omakase, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/kame-omakase; Lamaii, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/lamaii; Partage, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/partage-1201408; Pho Ga Bac Bac, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/pho-ga-bac-bac; Ping Pang Pong, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/ping-pang-pong; SoulBelly BBQ, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/soulbelly-bbq; Mott 32, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/mott-32-1250930; Wing Lei, https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/wing-lei-1250924.
- Official MICHELIN page search results showed current weekly hours for some restaurants (e.g. China Poblano, YEN Viet Kitchen, Wing Lei, Kabuto, Lamaii, SoulBelly BBQ, Anima by Edo, Ping Pang Pong). These are current Guide-page hours, not guaranteed 2027 schedules; any retained hours must be labeled with an as-of date and reconfirmed for the trip.
- Official NFL 2026–27 dates confirm Super Bowl LXI on Feb 14, 2027 at SoFi Stadium, Inglewood: https://www.nfl.com/news/2026-27-national-football-league-important-dates.
- U.S. OPM official federal-holidays page confirms Washington's Birthday on Mon Feb 15, 2027: https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/.
- Exact-date hotel rates, cancellation terms, selected room private-bath/bed configuration, 2027 transit itineraries, future venue schedules and official social/video URLs are not claimed unless a direct official page verifies them. Blank and flag instead.

## Irregularities / flagged for review

- Preferred Feb 15–18, 2027 window is three nights, while stated trip duration is 7–14 days and a seven-night hotel total is requested. No single duration is silently selected.
- Feb 15 is the observed federal Washington's Birthday. Super Bowl LXI is Feb 14 in Inglewood, not Las Vegas. These are verified dates; no hotel-price impact is inferred.
- Live exact-date hotel prices and the cheapest 7-night stay/booking date cannot be determined without identical-date, identical-room official booking quotes. Any earlier draft price/demand claims are to be removed unless official evidence is added.
- Las Vegas has bus and monorail service; a transit-only, door-to-door ≤1-hour hotel-to-restaurant matrix requires route-by-route official timetable checks. No unsupported travel counts or rankings should be shown as verified.
- Social search-result URLs are not verified venue accounts. Omit social handles/URLs unless linked from a venue's official site; otherwise show blank and flag.
- Current MICHELIN selection is 2026, not a guarantee of a 2027 award, service schedule or opening.

## Coordination / conflict log

- During the initial work, local `origin/main` was stale at `c97c82a`. Fetch showed merged PRs #1–#3. The rebase stopped on an add/add conflict in `COORDINATION.md`; this resolution preserves the full upstream board and verification/deployment record, then appends this session's claim. No upstream work is intentionally discarded.
- User requested branches named `session-<id>/<task>`, but Arena fixes this session to `arena/fd2715d0-vegas2`; work remains on that branch as required by the environment.

## PR and deployment result

- Prior PR #2 (https://github.com/kanlerxz87-cyber/Vegas2/pull/2) merged to `main` at `58dd7c3d9668c982b52fa83a5afe07a0a7447f0e` on 2026-11-26.
- Prior successful Pages deployment run: https://github.com/kanlerxz87-cyber/Vegas2/actions/runs/45901451051. Existing published site: https://kanlerxz87-cyber.github.io/Vegas2/.
- Current session PR / merge / deploy: pending.
