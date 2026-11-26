# COORDINATION — Las Vegas Trip Planning (Vegas2)

Shared task board. Every row needs a status, an owning session, and the files it touches.

**Statuses:** `unclaimed` · `in progress` · `done` · `needs review` (published on the *Flagged for Review* page; does not block)

**Branch note:** This session runs on one branch only, `arena/a52047d7-vegas2` (base `c97c82a` on `main`). Per the session rules, no other branches are created or pushed. The `session-<id>/<task>` naming from the original brief is therefore not used; every task below is claimed on this branch under session ID `a52047d7`.

**Verification standard:** Every table row carries a source link. Values that cannot be confirmed from an official source are left blank and marked **Unverified**. Nothing is inferred or filled in.

| # | Task | Status | Owner (session) | Files in scope | Notes |
|---|------|--------|-----------------|----------------|-------|
| T1 | Repo review (line by line) | done | a52047d7 | `README.md` (read only), `data/repo_review.json`, `repo-review.html` | See log entry 2026-11-26-A |
| T2 | Hotel research (8 Strip-area hotels, rooms, Michelin proximity) | done | a52047d7 | `data/hotels.json` | Room claims verified against official pages where retrievable; prices not retrievable |
| T3 | Michelin restaurants, Las Vegas 2026 (24 entries) | done | a52047d7 | `data/michelin.json` | Official Michelin press release is the status source |
| T4 | Activities (4 verified attractions) | done | a52047d7 | `data/activities.json` | Official agency/operator pages |
| T5 | Booking, pricing & timing | done | a52047d7 | `data/booking.json` | No 2027 rate verified; timing not determined |
| T6 | Questions & information gaps | done | a52047d7 | `data/questions.json` | |
| T7 | Suggestions for site & decision-making (review only, not implemented) | done | a52047d7 | `data/suggestions.json` | Awaiting user choice |
| T8 | Flagged for Review (irregularities & unverified items) | needs review | a52047d7 | `data/flagged.json` | Published; does not block merge |
| T9 | Site build (landing, subpages, CSS, build + check scripts) | done | a52047d7 | `scripts/*.py`, `assets/style.css`, generated `*.html`, `.nojekyll`, `README.md` | Static site served from repo root via GitHub Pages |
| T10 | Integration: re-verify combined data, build, link check, PR, merge, Pages check | in progress (build & gate passed; PR/merge pending) | a52047d7 | `COORDINATION.md` | Final step |

---

## Session log

### 2026-11-26-A — a52047d7 — claim
- Claimed T1–T10 on branch `arena/a52047d7-vegas2`. Only this session is active; no conflicts with other sessions were seen (the repo had a single commit and no other branches on `origin`).
- Baseline: `README.md` only (`# Vegas2`), no LICENSE, no `.gitignore`, no `COORDINATION.md` (created in this session), GitHub Pages enabled (legacy, `main` `/`, public, status `built`) per `gh api repos/kanlerxz87-cyber/Vegas2/pages`.

### 2026-11-26-B — a52047d7 — research & verification (sources)
Official sources retrieved on 2026-11-26 (all links are the pages actually read):
- Michelin 2026 Southwest selection (official press release, Aug 26/31 2026): https://www.michelin.com/en/publications/products-and-services/michelin-guide-reveals-first-ever-southwest-restaurant-selection-in-the-u-s — full star, Bib and Recommended lists with addresses. Also the Michelin Media copy https://michelinmedia.com/pages/blog/detail/article/c0/a1480/ and the PDF attached to the release.
- OPM federal holidays 2027 (Washington's Birthday = Mon Feb 15, 2027): https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/
- Bureau of Reclamation, Hoover Dam: https://www.usbr.gov/lc/hooverdam/ and https://www.usbr.gov/lc/hooverdam/service/index.html
- BLM, Red Rock Canyon NCA: https://www.blm.gov/visit/red-rock-canyon-national-conservation-area
- Recreation.gov, Red Rock Scenic Drive timed entry: https://www.recreation.gov/timed-entry/10075177
- Nevada State Parks, Valley of Fire: https://parks.nv.gov/parks/valley-of-fire
- Neon Museum (official site): https://neonmuseum.org/ and https://neonmuseum.org/tickets-and-experiences/
- Hotel official pages: Cosmopolitan https://cosmopolitanlasvegas.mgmresorts.com/en.html · Bellagio https://bellagio.mgmresorts.com/en/hotel.html · Caesars Palace https://www.caesars.com/caesars-palace · ARIA https://aria.mgmresorts.com/en/hotel/center-suite.html · Wynn booking engine https://reservations.wynnlasvegas.com/ibe/details.aspx?hotelID=13763&langID=1&access=&corp=&voucher=&rcID=324634&currID=0 · Resorts World (Conrad) https://www.rwlasvegas.com/stay/conrad-las-vegas/premium-room/
- Restaurant official pages: é by José Andrés https://www.ebyjoseandres.com/ · Guy Savoy https://www.caesars.com/caesars-palace/restaurants/restaurant-guy-savoy · Gymkhana hours via MGM Resorts press release (republished) https://www.stocktitan.net/news/MGM/aria-resort-casino-and-jks-restaurants-unveil-gymkhana-bringing-pus2edgb10tf.html
- Repo/Pages config: https://api.github.com/repos/kanlerxz87-cyber/Vegas2/pages

### 2026-11-26-C — a52047d7 — build & verification gate
- Built 10 pages with `python3 scripts/build_site.py`; re-running it produces no diff (reproducible).
- `python3 scripts/check_site.py`: OK — all data files parse; every hotel, Michelin and activity row has at least one https source; every row source is on the official-domain allowlist; Michelin counts 4 starred / 3 Bib / 17 Recommended = 24; 130 internal links resolve across 10 pages; no placeholder text leaked into HTML.
- Verification totals (cells across hotels, Michelin and activities): see the Home page KPIs.
- Commit: `c8d3d9b` (site build) on `arena/a52047d7-vegas2`.

### Verification gaps (see Flagged for Review)
- Official MGM Grand, Venetian, Restaurant de Joël Robuchon and L'Atelier pages could not be retrieved (fetch errors). Their rows are marked partial/unverified.
- No hotel rate for 7 nights (Feb 15–22, 2027) or 3 nights (Feb 15–18, 2027) was retrieved from an official source.
- No official transit-time source for "within 1 hour by bus/subway" was retrieved.

### Irregularities found
See `flagged.html` (Flagged for Review) for the full list and links. Key items: conflicting Michelin status claims in secondary press; Feb 15, 2027 is a federal holiday (Washington's Birthday); conflicting restaurant hours across third-party sites.

---

## Integration (T10) — checklist
- [x] All task data files present and valid JSON (checked by `scripts/check_site.py`)
- [x] Site builds from `scripts/build_site.py` with no errors
- [x] Internal links resolve (checked by `scripts/check_site.py`)
- [x] Every table row has at least one source link (checked by `scripts/check_site.py`)
- [ ] Pull request from `arena/a52047d7-vegas2` into `main`
- [ ] Merge result recorded below
- [ ] GitHub Pages deploy confirmed live

### PR & merge record
_(to be filled after the PR is created and merged)_
