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
| 1 | Research Michelin-rated/star restaurants in Las Vegas (official Michelin guide) | unclaimed | — | data/restaurants.md | michelinman.com | |
| 2 | Research hotels (private bath, queen+ bed, 2 adults, 7-night total price, cheapest booking window) | unclaimed | — | data/hotels.md | official hotel sites | |
| 3 | Research activities within ~1 hour travel of hotel + social links | unclaimed | — | data/activities.md | official activity sites | |
| 4 | Build landing/dashboard page (index.html) + CSS/JS | unclaimed | — | index.html, assets/ | | |
| 5 | Build subpages: hotels, restaurants, activities, executive summary, suggestions, open questions, flagged-for-review | unclaimed | — | *.html | | |
| 6 | Verify every table row line by line against official sources; blank + flag unverified | unclaimed | — | all data files | | |
| 7 | Integration: merge data, check build + broken links, enable GitHub Pages, publish | unclaimed | — | all | | |
| 8 | Create PR integration -> main, merge, confirm Pages deploys, record PR link + result here | unclaimed | — | COORDINATION.md | | |

## Log
- 2026-11-26: COORDINATION.md created on branch arena/0f0e637a-vegas2. Repo contained only README.md. Starting research (tasks 1-3).

## Session claim (current session)
Session `arena/0f0e637a-vegas2` claims all tasks 1-8 on the current branch (single active session). Will split into sub-tasks and commit/push as work progresses.
