# COORDINATION.md

Shared task board for the Vegas2 trip-planning site (GitHub Pages).
Branch: `arena/0f0e637a-vegas2` (branched from main `c97c82aaa0d485e60be170e2e93e64beabdb9508`)
Session: single session `arena/0f0e637a-vegas2` doing all work on the current branch (branch is fixed by Arena; no separate worktrees used).

## Claim rules
- Claim a task by writing your session ID + file scope, then commit and push immediately.
- Never start a task another session has claimed.
- If a claim is >60 min old with no commits, another session may take over (note handoff in the log).
- Shared outputs (table data, index/navigation) are changed only by the final integration session once all other tasks are done.
- Never mark anything verified without checking against an official source; link that source.
- Flagged irregularities/unverified items go on the "Flagged for Review" page; they do NOT block merge.

## Task board

| # | Task | Status | Owner | File scope | Sources / verification | Irregularities |
|---|------|--------|-------|------------|------------------------|----------------|
| 1 | Research Michelin-rated/star restaurants in Las Vegas (official Michelin guide) | done | arena/0f0e637a-vegas2 | data/restaurants.json | michelin.com official press release (Aug 26/31 2026) | None for starred/Bib/Recommended names/addresses |
| 2 | Research hotels (private bath, queen+ bed, 2 adults, 7-night total price, cheapest booking window) | in progress | arena/0f0e637a-vegas2 | data/hotels.json | official hotel sites (mgmgrand.com loaded; wynn failed JS) | Feb 2027 live pricing not retrievable (JS booking engine) → flagged unverified |
| 3 | Research activities within ~1 hour travel of hotel + social links | unclaimed | arena/0f0e637a-vegas2 | data/activities.json | official activity sites | social links/hours largely unverified → flagged |
| 4 | Build landing/dashboard page (index.html) + CSS/JS | unclaimed | arena/0f0e637a-vegas2 | index.html, assets/ | | |
| 5 | Build subpages: hotels, restaurants, activities, executive summary, suggestions, open questions, flagged-for-review | unclaimed | arena/0f0e637a-vegas2 | *.html | | |
| 6 | Verify every table row line by line against official sources; blank + flag unverified | unclaimed | arena/0f0e637a-vegas2 | all data files | | |
| 7 | Integration: merge data, check build + broken links, enable GitHub Pages, publish | unclaimed | arena/0f0e637a-vegas2 | all | | |
| 8 | Create PR integration -> main, merge, confirm Pages deploys, record PR link + result here | unclaimed | arena/0f0e637a-vegas2 | COORDINATION.md | | |

## Log
- 2026-11-26: COORDINATION.md created on branch arena/0f0e637a-vegas2. Repo contained only README.md.
- 2026-11-26: Task 1 done — official Michelin Guide Southwest 2026 selection captured from michelin.com press release (starred, Bib Gourmand, Recommended, with addresses). Verified.
- 2026-11-26: Task 2 in progress — MGM Grand official site loaded (MGM Two Queen room confirmed). Wynn site blocked (JS). Feb 2027 pricing flagged unverified.
- 2026-11-26: Transport research — confirmed Las Vegas has NO subway; RTC Deuce bus + Monorail are the public options; all Strip venues within ~1 hr by bus/monorail from central Strip hotels.

## Session claim (current session)
Session `arena/0f0e637a-vegas2` claims all tasks 1-8 on the current branch (single active session). Will split into sub-tasks and commit/push as work progresses.
