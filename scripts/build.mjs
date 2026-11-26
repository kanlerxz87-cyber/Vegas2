#!/usr/bin/env node
// Builds this session's trip-planner pages into docs/ (root) from data/trip/*.json.
// Output goes to docs/session-059c3126/ only. Other sessions own their own docs/ folders.
// No dependencies. Run: node scripts/build.mjs
// Exits non-zero if any verification rule fails (see checkData below).

import { readFileSync, writeFileSync, mkdirSync, rmSync, readdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const DATA = join(ROOT, "data", "trip");
const OUT = join(ROOT, "docs", "session-059c3126");

const load = (f) => JSON.parse(readFileSync(join(DATA, f), "utf8"));
const michelin = load("michelin.json");
const hotels = load("hotels.json");
const activities = load("activities.json");
const transit = load("transit-calendar.json");
const questions = load("questions.json");
const suggestions = load("suggestions.json");
const flagged = load("flagged.json");
const repo = load("repo-review.json");
const summary = load("summary.json");

// Domains that official sources may come from (sources must be https and on this list).
const OFFICIAL_DOMAINS = [
  "michelin.com", "guide.michelin.com", "michelinmedia.com", "visitlasvegas.com",
  "mgmresorts.com", "mgmgrand.mgmresorts.com", "cosmopolitanlasvegas.mgmresorts.com",
  "bellagio.mgmresorts.com", "aria.mgmresorts.com", "caesars.com", "www.caesars.com",
  "venetianlasvegas.com", "www.venetianlasvegas.com", "wynnlasvegas.com", "www.wynnlasvegas.com",
  "rwlasvegas.com", "www.rwlasvegas.com", "goldcoast.boydgaming.com",
  "opm.gov", "www.opm.gov", "rtcsnv.com", "www.rtcsnv.com", "lvmonorail.com", "www.lvmonorail.com",
  "redrockcanyonlv.org", "www.redrockcanyonlv.org", "recreation.gov", "www.recreation.gov",
  "parks.nv.gov", "reservenevada.com", "www.reservenevada.com", "usbr.gov", "www.usbr.gov",
  "hooverdam.ticketure.co", "neonmuseum.org", "www.neonmuseum.org",
  "tiktok.com", "www.tiktok.com", "instagram.com", "www.instagram.com", "facebook.com", "www.facebook.com",
  "github.com", "docs.github.com", "opentable.com", "www.opentable.com",
  "animabyedo.com", "kabutolv.com", "partage.vegas", "sevenrooms.com"
];

const problems = [];
const warnings = [];
const fail = (msg) => problems.push(msg);

function domainOk(url) {
  try {
    const h = new URL(url).hostname.toLowerCase();
    return OFFICIAL_DOMAINS.some((d) => h === d || h.endsWith("." + d));
  } catch { return false; }
}

// Venue links come from LVCVA's official list (or the venue's own page); they must be https.
function checkLink(url, where) {
  if (url == null) return;
  if (!/^https:\/\//.test(url)) fail(`${where}: link must be https: ${url}`);
}

function checkSources(sources, where) {
  if (!Array.isArray(sources) || sources.length === 0) {
    // Allowed only for user-brief or intentionally blank rows, which must say so.
    fail(`${where}: no sources listed`);
    return;
  }
  for (const s of sources) {
    if (s.url == null) continue; // user brief item (not an external source)
    if (!/^https:\/\//.test(s.url) || !domainOk(s.url)) fail(`${where}: source not on official domain list: ${s.url}`);
  }
}

// ---------- Verification rules ----------
function checkData() {
  // Michelin counts must match the official release totals.
  const tierCount = {};
  for (const r of michelin.restaurants) {
    tierCount[r.tier] = (tierCount[r.tier] || 0) + 1;
    checkSources(r.sources, `Michelin ${r.name}`);
    checkLink(r.link, `Michelin ${r.name}`);
    if (!r.address) fail(`Michelin ${r.name}: address missing`);
  }
  const exp = michelin.meta.expectedCounts;
  for (const k of Object.keys(exp)) {
    if (k === "total") continue;
    if ((tierCount[k] || 0) !== exp[k]) fail(`Michelin tier count mismatch for ${k}: found ${tierCount[k] || 0}, expected ${exp[k]}`);
  }
  if (michelin.restaurants.length !== exp.total) fail(`Michelin total ${michelin.restaurants.length} != ${exp.total}`);

  // Hotels: count must equal listed restaurants; ranking must be sorted by count then stars.
  let prev = null;
  for (const h of hotels.hotels) {
    checkSources(h.sources, `Hotel ${h.name}`);
    checkLink(h.link, `Hotel ${h.name}`);
    if (h.michelinInResort.length !== h.michelinCount) fail(`Hotel ${h.name}: michelinCount ${h.michelinCount} != list length ${h.michelinInResort.length}`);
    if (prev && (prev.michelinCount < h.michelinCount || (prev.michelinCount === h.michelinCount && prev.michelinStarCount < h.michelinStarCount))) {
      fail(`Hotel ranking order wrong at ${h.name}`);
    }
    prev = h;
  }

  for (const a of activities.activities) {
    checkSources(a.sources, `Activity ${a.name}`);
    checkLink(a.link, `Activity ${a.name}`);
  }
  for (const t of transit.transit) checkSources(t.sources, `Transit ${t.name}`);
  for (const c of transit.calendar) checkSources(c.sources, `Calendar ${c.dates}`);
  for (const b of transit.bookingTiming) {
    if (b.fact !== null) checkSources(b.sources, `Booking ${b.item}`);
    else if (b.sources.length) fail(`Booking ${b.item}: blank fact should have no source`);
  }

  // Dates: arithmetic checks for calendar claims.
  const d = (s) => new Date(s + "T00:00:00Z");
  const weekday = (s) => d(s).toLocaleDateString("en-US", { weekday: "long", timeZone: "UTC" });
  if (weekday("2027-02-15") !== "Monday") fail("Feb 15, 2027 is not a Monday");
  if (weekday("2027-02-18") !== "Thursday") fail("Feb 18, 2027 is not a Thursday");
  if (weekday("2027-03-23") !== "Tuesday") fail("Mar 23, 2027 is not a Tuesday");

  // Internal consistency: no empty required strings.
  for (const q of [...questions.fromYou, ...questions.research]) if (!q.question) fail(`Question ${q.id} empty`);
  for (const s of suggestions.items) if (!s.title) fail(`Suggestion ${s.id} empty`);
  for (const f of flagged.irregularities) {
    if (!f.sources.length) fail(`Flag ${f.id} has no source link`);
    for (const u of f.sources) if (!domainOk(u)) fail(`Flag ${f.id} source not official: ${u}`);
  }
  for (const c of repo.checks) {
    for (const u of c.sources) if (!domainOk(u)) fail(`Repo check ${c.id} source not official: ${u}`);
  }
}

// ---------- Helpers ----------
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const UNV = '<span class="unv">Unverified</span>';

// Render text, turning URLs into links.
function rich(text) {
  return esc(text).replace(/(https:\/\/[^\s;,)]+)/g, (u) => `<a href="${u}" rel="noopener" target="_blank">${u.replace(/^https:\/\//, "")}</a>`);
}

function cell(v) {
  if (v === null || v === undefined || v === "") return UNV;
  if (Array.isArray(v)) return v.length ? `<ul class="cl">${v.map((x) => `<li>${rich(x)}</li>`).join("")}</ul>` : UNV;
  if (typeof v === "object") return `<a href="${esc(v.url)}" target="_blank" rel="noopener">${esc(v.label)}</a>`;
  return rich(v);
}

function sourcesCell(sources) {
  if (!sources || !sources.length) return "—";
  return `<ul class="cl src">${sources
    .map((s) => (s.url ? `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.label)}</a></li>` : `<li>${esc(s.label)}</li>`))
    .join("")}</ul>`;
}

function linkCell(url, text = "Official page") {
  if (!url) return UNV;
  return `<a href="${esc(url)}" target="_blank" rel="noopener">${esc(text)}</a>`;
}

// Build a responsive table: on phones each row becomes a stacked card with labels.
function table(cols, rows, id = "") {
  const head = cols.map((c) => `<th scope="col">${esc(c.label)}</th>`).join("");
  const body = rows
    .map((r) => `<tr>${cols.map((c) => `<td data-label="${esc(c.label)}">${c.render ? c.render(r) : cell(r[c.key])}</td>`).join("")}</tr>`)
    .join("\n");
  return `<div class="tw"><table class="data"${id ? ` id="${id}"` : ""}><thead><tr>${head}</tr></thead><tbody>\n${body}\n</tbody></table></div>`;
}

// Count null key fields for a row (drives the verification status shown in the UI).
function verifiedStatus(obj, keys) {
  const ok = keys.filter((k) => obj[k] !== null && obj[k] !== undefined && obj[k] !== "" && !(Array.isArray(obj[k]) && !obj[k].length)).length;
  const badge = ok === keys.length ? '<span class="ok">Verified</span>' : ok === 0 ? '<span class="unv">Unverified</span>' : `<span class="part">Partly verified (${ok}/${keys.length})</span>`;
  return badge;
}

function page({ file, title, active, body, desc = "" }) {
  const nav = [
    ["index.html", "Home"],
    ["hotels.html", "Hotels"],
    ["michelin.html", "Michelin"],
    ["activities.html", "Activities"],
    ["transit-dates.html", "Transit & dates"],
    ["booking.html", "Booking timing"],
    ["questions.html", "Questions"],
    ["suggestions.html", "Suggestions"],
    ["flagged.html", "Flagged for Review"],
    ["repo-review.html", "Repo review"],
    ["sources.html", "Sources"],
  ]
    .map(([href, label]) => `<a href="${href}"${href === active ? ' aria-current="page"' : ""}>${label}</a>`)
    .join("");
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)} · Las Vegas Trip Planner</title>
<meta name="description" content="${esc(desc || "Las Vegas trip planning: hotels, MICHELIN restaurants, activities, transit and dates, with official sources and flagged items.")}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="brand"><a href="index.html">Las Vegas Trip Planner</a><span class="upd">Data as of 2026-11-26</span></div>
  <nav class="nav" aria-label="Main">${nav}</nav>
</header>
<main id="main">
${body}
</main>
<footer class="foot">
  <p>Every published row links to an official source. Values not confirmed on an official source are shown as <span class="unv">Unverified</span> and listed on <a href="flagged.html">Flagged for Review</a>. Prices and availability change; check the official site before booking.</p>
  <p>Built from <code>data/trip/*.json</code> by <code>scripts/build.mjs</code>. Repository: <a href="https://github.com/kanlerxz87-cyber/Vegas2">kanlerxz87-cyber/Vegas2</a>.</p>
</footer>
</body>
</html>
`;
}

// ---------- Pages ----------
const pages = [];

function buildIndex() {
  const michelinByTier = michelin.restaurants.reduce((a, r) => ((a[r.tier] = (a[r.tier] || 0) + 1), a), {});
  const unverifiedCount = countUnverified();
  const stats = summary.headlineNumbers
    .map((s) => `<div class="stat"><div class="sv">${esc(s.value)}</div><div class="sl">${esc(s.label)}</div></div>`)
    .join("");
  const cards = [
    ["hotels.html", "Hotels", `${hotels.hotels.length} candidates ranked by nearby MICHELIN listings. Prices pending.`],
    ["michelin.html", "Michelin restaurants", `${michelin.restaurants.length} official Las Vegas listings: ${michelinByTier["Two MICHELIN Stars"] + michelinByTier["One MICHELIN Star"]} starred, ${michelinByTier["Bib Gourmand"]} Bib, ${michelinByTier["Michelin Recommended"]} Recommended.`],
    ["activities.html", "Activities", `${activities.activities.length} with official hours and fees. Drive times pending.`],
    ["transit-dates.html", "Transit & dates", "Bus and Monorail (no subway found on official sites), key dates and holidays."],
    ["booking.html", "Booking timing", "Verified promotions and booking windows. Cheapest date not verified."],
    ["questions.html", "Questions", `${questions.fromYou.length} questions for you and ${questions.research.length} research items.`],
    ["suggestions.html", "Suggestions", `${suggestions.items.length} improvements to review. Nothing implemented.`],
    ["flagged.html", "Flagged for Review", `${flagged.irregularities.length} irregularities and ${unverifiedCount} unverified item groups.`],
    ["repo-review.html", "Repo review", `${repo.checks.length} repository checks and their sources.`],
    ["sources.html", "Sources", "Every official link used, and where it was used."],
    ["../session-36cc5108/index.html", "Other planner (session 36cc5108)", "The other session's planner, built by site/build.py and kept unchanged for comparison."],
  ]
    .map(([href, t, d]) => `<a class="card" href="${href}"><h3>${esc(t)}</h3><p>${esc(d)}</p></a>`)
    .join("");
  const bullets = summary.bullets.map((b) => `<li>${rich(b)}</li>`).join("");
  return page({
    file: "index.html",
    title: "Home",
    active: "index.html",
    body: `
<section class="hero">
  <h1>${esc(summary.title)}</h1>
  <p class="lede">Feb 15 to Mar 23, 2027 window. Preferred: Mon Feb 15 to Thu Feb 18. Every value below is either sourced to an official page or marked <span class="unv">Unverified</span>.</p>
  <div class="stats">${stats}</div>
</section>
<section>
  <h2>Executive summary</h2>
  <ul class="bullets">${bullets}</ul>
</section>
<section>
  <h2>Pages</h2>
  <div class="cards">${cards}</div>
</section>`,
  });
}

function countUnverified() {
  return unverifiedItems().length;
}

// Unverified items generated from the data (null key fields).
function unverifiedItems() {
  const out = [];
  const check = (group, entries, nameOf, keys) => {
    for (const e of entries) {
      const missing = keys.filter((k) => e[k] === null || e[k] === undefined || e[k] === "" || (Array.isArray(e[k]) && !e[k].length));
      if (missing.length) out.push({ group, item: nameOf(e), missing: missing.join(", ") });
    }
  };
  check("Michelin restaurant", michelin.restaurants, (r) => r.name, ["hours", "priceLevel", "reservations", "priceForCouple", "social"]);
  check("Hotel", hotels.hotels, (h) => h.name, ["bedType", "privateBathroom", "sevenNightTotal", "cheapestBookingWindow"]);
  check("Activity", activities.activities, (a) => a.name, ["prices", "driveOrTransitFromHotel", "social"]);
  check("Transit", transit.transit, (t) => t.name, ["hours"]);
  for (const b of transit.bookingTiming) if (b.fact === null) out.push({ group: "Booking timing", item: b.item, missing: "fact" });
  return out;
}

function buildMichelin() {
  const order = ["Two MICHELIN Stars", "One MICHELIN Star", "Bib Gourmand", "Michelin Recommended"];
  const areaCount = {};
  for (const r of michelin.restaurants) areaCount[r.area] = (areaCount[r.area] || 0) + 1;
  const areaRows = Object.entries(areaCount).sort((a, b) => b[1] - a[1]);
  const clusterTable = table(
    [{ key: "area", label: "Area (per official/LVCVA label)" }, { key: "n", label: "Listings" }],
    areaRows.map(([area, n]) => ({ area, n })),
  );
  const sorted = [...michelin.restaurants].sort((a, b) => order.indexOf(a.tier) - order.indexOf(b.tier));
  const cols = [
    { key: "tier", label: "Distinction" },
    { key: "name", label: "Restaurant", render: (r) => `<strong>${esc(r.name)}</strong><br><span class="muted">${esc(r.cuisine)}</span>` },
    { key: "area", label: "Area" },
    { key: "address", label: "Address (official)" },
    { key: "hours", label: "Days & hours (official)" },
    { key: "priceLevel", label: "Price level" },
    { key: "priceForCouple", label: "Cost for 2 (total)" },
    { key: "reservations", label: "Reservations" },
    { key: "social", label: "YouTube / TikTok / Instagram" },
    { key: "link", label: "Official link", render: (r) => linkCell(r.link, "Restaurant site") },
    { key: "status", label: "Verified", render: (r) => verifiedStatus(r, ["address", "hours", "priceLevel", "priceForCouple", "social"]) },
    { key: "sources", label: "Sources", render: (r) => sourcesCell(r.sources) },
  ];
  const excluded = michelin.excludedFromLasVegas
    .map((e) => `<li><strong>${esc(e.name)}</strong>: ${esc(e.reason)} <a href="${esc(e.source)}" target="_blank" rel="noopener">source</a></li>`)
    .join("");
  return page({
    file: "michelin.html",
    title: "Michelin restaurants",
    active: "michelin.html",
    body: `
<section>
  <h1>MICHELIN restaurants in Las Vegas</h1>
  <p>${esc(michelin.meta.description)}</p>
  <p class="note">Official sources: <a href="${esc(michelin.meta.primarySource.url)}" target="_blank" rel="noopener">MICHELIN press release (michelin.com)</a>; <a href="${esc(michelin.meta.secondarySource.url)}" target="_blank" rel="noopener">Visit Las Vegas MICHELIN list</a>.</p>
  <p class="note"><strong>Cost for 2:</strong> no official couple price was read for any restaurant, so these cells are blank. Hours are shown only where the official page was read.</p>
</section>
<section>
  <h2>Clusters by area</h2>
  ${clusterTable}
</section>
<section>
  <h2>All 24 Las Vegas listings</h2>
  <p class="muted">Stars first, then Bib Gourmand, then Recommended. Cost fields are blank until an official menu price is read.</p>
  ${table(cols, sorted)}
</section>
<section>
  <h2>Not counted as Las Vegas</h2>
  <ul class="bullets">${excluded}</ul>
</section>`,
  });
}

function buildHotels() {
  const cols = [
    { key: "rank", label: "Rank" },
    { key: "name", label: "Hotel", render: (h) => `<strong>${esc(h.name)}</strong><br><span class="muted">${esc(h.area)}</span><br>${linkCell(h.link, "Official site")}` },
    { key: "michelinCount", label: "MICHELIN listings in resort", render: (h) => `<strong>${h.michelinCount}</strong> (${h.michelinStarCount} star${h.michelinStarCount === 1 ? "" : "s"} total)<ul class="cl">${h.michelinInResort.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>` },
    { key: "bedType", label: "Bed (queen or larger?)" },
    { key: "privateBathroom", label: "Private bathroom" },
    { key: "sevenNightTotal", label: "7-night total (Feb 15-22, 2027)" },
    { key: "cheapestBookingWindow", label: "Cheapest booking window" },
    { key: "notes", label: "Notes" },
    { key: "status", label: "Verified", render: (h) => verifiedStatus(h, ["bedType", "privateBathroom", "sevenNightTotal"]) },
    { key: "sources", label: "Sources", render: (h) => sourcesCell(h.sources) },
  ];
  return page({
    file: "hotels.html",
    title: "Hotels",
    active: "hotels.html",
    body: `
<section>
  <h1>Hotel candidates</h1>
  <p><strong>Ranking rule:</strong> ${esc(hotels.meta.rankingRule)}</p>
  <p class="warn"><strong>Price:</strong> ${esc(hotels.meta.priceNote)}</p>
  <p class="note"><strong>Room requirement:</strong> ${esc(hotels.meta.roomRequirement)}</p>
</section>
<section>
  <h2>Ranked candidates</h2>
  ${table(cols, hotels.hotels)}
</section>`,
  });
}

function buildActivities() {
  const cols = [
    { key: "name", label: "Activity", render: (a) => `<strong>${esc(a.name)}</strong><br><span class="muted">${esc(a.category)}</span><br>${linkCell(a.link, "Official page")}` },
    { key: "hours", label: "Days & hours (official)" },
    { key: "prices", label: "Prices (official)" },
    { key: "specialRules", label: "Exceptions & reservations" },
    { key: "driveOrTransitFromHotel", label: "Drive / transit from hotel" },
    { key: "social", label: "YouTube / TikTok / Instagram" },
    { key: "tickets", label: "Tickets / reservations", render: (a) => (a.tickets ? linkCell(a.tickets, "Tickets / reservations") : UNV) },
    { key: "status", label: "Verified", render: (a) => verifiedStatus(a, ["hours", "prices", "driveOrTransitFromHotel", "social"]) },
    { key: "sources", label: "Sources", render: (a) => sourcesCell(a.sources) },
  ];
  return page({
    file: "activities.html",
    title: "Activities",
    active: "activities.html",
    body: `
<section>
  <h1>Activities</h1>
  <p class="note">${esc(activities.meta.note)}</p>
  <p class="warn">${esc(activities.meta.reservationWindow)}</p>
</section>
<section>
  <h2>Verified activities</h2>
  ${table(cols, activities.activities)}
</section>`,
  });
}

function buildTransitDates() {
  const tcols = [
    { key: "mode", label: "Mode" },
    { key: "name", label: "Service", render: (t) => `<strong>${esc(t.name)}</strong>` },
    { key: "hours", label: "Hours (official)" },
    { key: "status", label: "Status / notes", render: (t) => `${esc(t.status || "")}${t.notes ? `<br><span class="muted">${esc(t.notes)}</span>` : ""}` },
    { key: "link", label: "Official link", render: (t) => linkCell(t.link, "Official page") },
    { key: "sources", label: "Sources", render: (t) => sourcesCell(t.sources) },
  ];
  const ccols = [
    { key: "dates", label: "Dates" },
    { key: "label", label: "What" },
    { key: "effect", label: "Effect / note" },
    { key: "sources", label: "Sources", render: (c) => sourcesCell(c.sources) },
  ];
  return page({
    file: "transit-dates.html",
    title: "Transit & dates",
    active: "transit-dates.html",
    body: `
<section>
  <h1>Transit & dates</h1>
  <p class="note">The brief asks for travel by subway or bus within about 1 hour. Las Vegas has no subway listed on official sites read. Travel times from each hotel are not verified (see Flagged F13).</p>
</section>
<section>
  <h2>Transit options</h2>
  ${table(tcols, transit.transit)}
</section>
<section>
  <h2>Key dates</h2>
  ${table(ccols, transit.calendar)}
</section>`,
  });
}

function buildBooking() {
  const cols = [
    { key: "item", label: "Item" },
    { key: "fact", label: "What the official source says" },
    { key: "validFor", label: "Applies to / caveat" },
    { key: "link", label: "Official link", render: (b) => linkCell(b.link, "Official page") },
    { key: "sources", label: "Sources", render: (b) => sourcesCell(b.sources) },
  ];
  return page({
    file: "booking.html",
    title: "Booking timing",
    active: "booking.html",
    body: `
<section>
  <h1>Booking timing</h1>
  <p class="warn">The cheapest time to book was NOT verified. Only promotions and booking windows printed on official pages are listed here. A real answer needs dated price snapshots from each hotel's official booking calendar (see Suggestions S1).</p>
</section>
<section>
  <h2>What the official sources say</h2>
  ${table(cols, transit.bookingTiming)}
</section>`,
  });
}

function buildQuestions() {
  const qcols = [
    { key: "id", label: "ID" },
    { key: "question", label: "Question" },
    { key: "why", label: "Why it matters" },
    { key: "status", label: "Status" },
  ];
  const rcols = [
    { key: "id", label: "ID" },
    { key: "question", label: "Information needed" },
    { key: "missing", label: "What is missing" },
    { key: "howToDiscover", label: "How to find it (official sources first)" },
    { key: "status", label: "Status" },
  ];
  return page({
    file: "questions.html",
    title: "Questions",
    active: "questions.html",
    body: `
<section>
  <h1>Questions and information needed</h1>
  <p class="note">${esc(questions.meta.intro)}</p>
</section>
<section>
  <h2>Questions for you</h2>
  ${table(qcols, questions.fromYou)}
</section>
<section>
  <h2>Information to research</h2>
  ${table(rcols, questions.research)}
</section>`,
  });
}

function buildSuggestions() {
  const cols = [
    { key: "id", label: "ID" },
    { key: "title", label: "Suggestion" },
    { key: "benefit", label: "Benefit" },
    { key: "effort", label: "Effort" },
    { key: "risk", label: "Risk / caveat" },
    { key: "status", label: "Decision" },
  ];
  return page({
    file: "suggestions.html",
    title: "Suggestions",
    active: "suggestions.html",
    body: `
<section>
  <h1>Suggestions for review</h1>
  <p class="note">${esc(suggestions.meta.intro)}</p>
</section>
<section>
  <h2>Options</h2>
  ${table(cols, suggestions.items)}
</section>`,
  });
}

function buildFlagged() {
  const cols = [
    { key: "id", label: "ID" },
    { key: "item", label: "Item" },
    { key: "detail", label: "Detail" },
    { key: "sources", label: "Source links for manual review", render: (f) => `<ul class="cl src">${f.sources.map((u) => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(u.replace(/^https:\/\/(www\.)?/, ""))}</a></li>`).join("")}</ul>` },
  ];
  const unv = unverifiedItems();
  const ucols = [
    { key: "group", label: "Group" },
    { key: "item", label: "Entry" },
    { key: "missing", label: "Unverified fields" },
  ];
  return page({
    file: "flagged.html",
    title: "Flagged for Review",
    active: "flagged.html",
    body: `
<section>
  <h1>Flagged for Review</h1>
  <p class="note">${esc(flagged.meta.intro)} Items here do not block publication. Review them after the site is live.</p>
</section>
<section>
  <h2>Irregularities and conflicts</h2>
  ${table(cols, flagged.irregularities)}
</section>
<section>
  <h2>Unverified fields (generated from the data)</h2>
  <p class="muted">${unv.length} entries have at least one field not confirmed on an official source. Each such field is blank in the tables.</p>
  ${table(ucols, unv)}
</section>`,
  });
}

function buildRepo() {
  const cols = [
    { key: "id", label: "ID" },
    { key: "item", label: "Item checked" },
    { key: "result", label: "Result" },
    { key: "sources", label: "Sources for manual review", render: (c) => (c.sources.length ? `<ul class="cl src">${c.sources.map((u) => `<li><a href="${esc(u)}" target="_blank" rel="noopener">${esc(u.replace(/^https:\/\/(www\.)?/, ""))}</a></li>`).join("")}</ul>` : "—") },
  ];
  return page({
    file: "repo-review.html",
    title: "Repo review",
    active: "repo-review.html",
    body: `
<section>
  <h1>Repository review</h1>
  <p class="note">${esc(repo.meta.intro)}</p>
  ${table(cols, repo.checks)}
</section>`,
  });
}

function collectSources() {
  const map = new Map();
  const add = (src, where) => {
    if (!src || !src.url) return;
    if (!map.has(src.url)) map.set(src.url, { url: src.url, labels: new Set(), used: new Set() });
    map.get(src.url).labels.add(src.label);
    map.get(src.url).used.add(where);
  };
  for (const r of michelin.restaurants) r.sources.forEach((s) => add(s, "Michelin"));
  for (const h of hotels.hotels) h.sources.forEach((s) => add(s, "Hotels"));
  for (const a of activities.activities) a.sources.forEach((s) => add(s, "Activities"));
  for (const t of transit.transit) t.sources.forEach((s) => add(s, "Transit"));
  for (const c of transit.calendar) c.sources.forEach((s) => add(s, "Dates"));
  for (const b of transit.bookingTiming) b.sources.forEach((s) => add(s, "Booking timing"));
  for (const f of flagged.irregularities) f.sources.forEach((u) => add({ url: u, label: f.item }, "Flagged"));
  for (const c of repo.checks) c.sources.forEach((u) => add({ url: u, label: c.item }, "Repo review"));
  michelin.excludedFromLasVegas.forEach((e) => add({ url: e.source, label: e.name }, "Michelin"));
  const rows = [...map.values()].sort((a, b) => a.url.localeCompare(b.url));
  const cols = [
    { key: "url", label: "Official link", render: (r) => `<a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.url)}</a>` },
    { key: "labels", label: "What it supports", render: (r) => esc([...r.labels].join("; ")) },
    { key: "used", label: "Used on", render: (r) => esc([...r.used].join(", ")) },
  ];
  return page({
    file: "sources.html",
    title: "Sources",
    active: "sources.html",
    body: `
<section>
  <h1>Sources</h1>
  <p class="note">Every official link used in the data. ${rows.length} unique links. A link in this list is not a guarantee of a current value; check the date on the source page when booking.</p>
  ${table(cols, rows)}
</section>`,
  });
}

// ---------- Main ----------
checkData();
if (problems.length) {
  console.error("VERIFICATION FAILED:\n- " + problems.join("\n- "));
  process.exit(1);
}

// Only this builder's folder is cleared.
mkdirSync(OUT, { recursive: true });
for (const f of [...readdirSync(OUT).filter((f) => f.endsWith(".html")), ".nojekyll"]) rmSync(join(OUT, f), { force: true });
rmSync(join(OUT, "assets"), { recursive: true, force: true });
mkdirSync(join(OUT, "assets"), { recursive: true });
const outputs = {
  "index.html": buildIndex(),
  "michelin.html": buildMichelin(),
  "hotels.html": buildHotels(),
  "activities.html": buildActivities(),
  "transit-dates.html": buildTransitDates(),
  "booking.html": buildBooking(),
  "questions.html": buildQuestions(),
  "suggestions.html": buildSuggestions(),
  "flagged.html": buildFlagged(),
  "repo-review.html": buildRepo(),
  "sources.html": collectSources(),
};
for (const [f, html] of Object.entries(outputs)) writeFileSync(join(OUT, f), html);
writeFileSync(join(OUT, ".nojekyll"), "");
writeFileSync(join(OUT, "assets", "style.css"), readFileSync(join(ROOT, "scripts", "style.css"), "utf8"));

// Internal link check: every relative href/src must resolve to a generated file.
const pageFiles = new Set([...Object.keys(outputs), "assets/style.css"]);
const exists = (rel) => existsSync(join(OUT, rel));
const broken = [];
for (const [f, html] of Object.entries(outputs)) {
  for (const m of html.matchAll(/href="([^"#:]+)(#[^"]*)?"/g)) {
    const target = m[1];
    if (target.startsWith("http")) continue;
    if (!pageFiles.has(target) && !exists(target)) broken.push(`${f} -> ${target}`);
  }
}
if (broken.length) {
  console.error("BROKEN INTERNAL LINKS:\n- " + broken.join("\n- "));
  process.exit(1);
}
const unv = unverifiedItems().length;
console.log(`Built ${Object.keys(outputs).length} pages into docs/session-059c3126/. Unverified entry groups: ${unv}. Checks passed.`);
