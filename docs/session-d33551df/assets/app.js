(() => {
  'use strict';

  const D = window.TRIP;
  if (!D) return;

  const page = document.body.dataset.page || 'home';
  const nav = [
    ['home', 'Overview', 'index.html'],
    ['hotels', 'Hotels', 'hotels.html'],
    ['restaurants', 'Restaurants', 'restaurants.html'],
    ['activities', 'Activities', 'activities.html'],
    ['analysis', 'Analysis & answers', 'analysis.html'],
    ['flagged', 'Flagged for Review', 'flagged.html']
  ];
  const pageInfo = {
    home: ['Evidence-first trip planning', 'A practical Las Vegas short list, with the knowns, gaps, and source links kept visible.'],
    hotels: ['Hotel comparison', 'King-bed rooms with private bathrooms; same-date prices and MICHELIN transit reach remain separate questions.'],
    restaurants: ['MICHELIN-recognized restaurants', 'All 24 entries from the 2026 Las Vegas list, with distinctions clearly separated and official venue pages linked.'],
    activities: ['Things to do & get around', 'Official schedules, current price anchors, service caveats, and direct ticket or transit sources.'],
    analysis: ['What the evidence says', 'Planning assumptions, known information, unanswered questions, and practical ways to close the gaps.'],
    flagged: ['Flagged for Review', 'Unconfirmed values stay blank. These are the issues to resolve before booking or locking the itinerary.']
  };

  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (ch) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[ch]));

  const safeUrl = (url) => {
    if (!url) return '';
    try {
      const parsed = new URL(url, window.location.href);
      return ['https:', 'http:'].includes(parsed.protocol) ? esc(url) : '';
    } catch (_) { return ''; }
  };

  const link = (url, label, className = '') => {
    const href = safeUrl(url);
    if (!href) return '';
    return `<a${className ? ` class="${esc(className)}"` : ''} href="${href}" target="_blank" rel="noopener noreferrer">${esc(label)}<span class="sr-only"> (opens in a new tab)</span></a>`;
  };

  const missing = (note = 'Unverified; intentionally left blank') =>
    `<span class="blank">—<small>${esc(note)}</small></span>`;

  const sourceStack = (item, opts = {}) => {
    const parts = [];
    if (item.officialUrl) parts.push(link(item.officialUrl, opts.primaryLabel || 'Official venue'));
    if (item.menuUrl && item.menuUrl !== item.officialUrl) parts.push(link(item.menuUrl, 'Official menu'));
    if (opts.guide) parts.push(link(D.meta.michelinSource, '2026 list source'));
    if (item.bookingUrl && item.bookingUrl !== item.sourceUrl && item.bookingUrl !== item.officialUrl) parts.push(link(item.bookingUrl, 'Rate / availability'));
    return `<div class="source-links">${parts.join('') || missing('Source not confirmed')}</div>`;
  };

  const table = (labels, rows, renderRow, className = '') => {
    const head = labels.map((label) => `<th scope="col">${esc(label)}</th>`).join('');
    const body = rows.map((row, i) => {
      const cells = renderRow(row, i);
      return `<tr>${cells.map((cell, ci) => `<td data-label="${esc(labels[ci])}">${cell}</td>`).join('')}</tr>`;
    }).join('');
    return `<div class="table-wrap ${className}"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
  };

  const badge = (text, type = 'neutral') => `<span class="badge ${type}">${esc(text)}</span>`;
  const sourceNote = (text, url, label = 'Official source') => `<p class="note">${esc(text)} ${url ? link(url, label) : '<span class="small">(from the requested trip dates)</span>'}</p>`;

  function drawHeader() {
    const header = document.getElementById('site-header');
    header.innerHTML = `
      <header class="site-header">
        <div class="header-inner">
          <div class="brand-row">
            <a class="brand" href="index.html" aria-label="Las Vegas trip dashboard home">
              <span class="brand-mark" aria-hidden="true">LV</span>
              <span><span class="brand-name">Vegas, planned with receipts</span><span class="brand-tag">Two adults · February–March 2027</span></span>
            </a>
            <span class="stamp"><span class="stamp-dot" aria-hidden="true"></span><span>Research snapshot<br>${esc(D.meta.researchedAt)}</span></span>
          </div>
          <nav class="primary-nav" aria-label="Main navigation">
            ${nav.map(([id, label, href]) => `<a href="${href}"${page === id ? ' aria-current="page"' : ''}>${esc(label)}</a>`).join('')}
          </nav>
        </div>
      </header>`;
  }

  function drawFooter() {
    const footer = document.getElementById('site-footer');
    footer.innerHTML = `
      <footer class="site-footer">
        <div class="footer-inner">
          <div class="footer-copy">
            <p><strong>Research snapshot: ${esc(D.meta.researchedAt)}.</strong> Not a booking, reservation, or guarantee of future hours, prices, room inventory, or transit service.</p>
            <p>Only official source links are presented for venue facts. A dash means the value is unverified or not published in the reviewed source; see <a href="flagged.html">Flagged for Review</a>.</p>
          </div>
          <nav class="footer-nav" aria-label="Footer navigation">
            <a href="analysis.html">Method & Q&amp;A</a><a href="flagged.html">Review gaps</a><a href="${safeUrl(D.meta.michelinSource)}" target="_blank" rel="noopener noreferrer">2026 MICHELIN list ↗</a>
          </nav>
        </div>
      </footer>`;
  }

  function pageHeading(eyebrow, title, lede, mark = '') {
    return `<div class="page-head"><div><p class="eyebrow">${esc(eyebrow)}</p><h1>${esc(title)}</h1><p class="lede">${esc(lede)}</p></div>${mark ? `<span class="head-mark" aria-hidden="true">${esc(mark)}</span>` : ''}</div>`;
  }

  function renderHome() {
    const target = document.getElementById('main');
    const verifiedMenus = D.restaurants.filter((r) => r.mealForTwo).length;
    target.innerHTML = `
      <section class="hero" aria-labelledby="hero-title">
        <p class="eyebrow">${esc(pageInfo.home[0])}</p>
        <h1 id="hero-title">Las Vegas, planned with receipts.</h1>
        <p class="lede">A source-linked trip dashboard for two adults, covering ${esc(D.meta.travelWindow)}. Real findings are separated from estimates, and unconfirmed details stay blank instead of being guessed.</p>
        <div class="hero-meta"><span class="pill">24 restaurants · 2026 Guide</span><span class="pill">Room fit: king + private bath</span><span class="pill">Researched ${esc(D.meta.researchedAt)}</span></div>
      </section>

      <section class="section" aria-label="Top findings">
        <div class="callout alert">
          <strong>Dates need two scenarios.</strong> Your preferred ${esc(D.meta.preferredWindow)} is ${D.meta.preferredNights} nights, while the trip request is 1–2 weeks. The ${esc(D.meta.comparisonStay)} check is shown only as a comparable seven-night price search—not as a replacement itinerary.
        </div>
        <div class="metric-grid">
          <article class="metric-card"><div class="metric-kicker">MICHELIN 2026</div><div class="metric-value">24</div><div class="metric-label">4 starred · 3 Bib Gourmand · 17 Recommended / Selected</div></article>
          <article class="metric-card"><div class="metric-kicker">ROOM FIT</div><div class="metric-value">5</div><div class="metric-label">Candidate hotel rooms with a king bed and private bathroom described by the official page</div></article>
          <article class="metric-card"><div class="metric-kicker">DATED RATE</div><div class="metric-value">$201</div><div class="metric-label">Latest Julius King nightly display for Feb 15–22; an earlier capture showed $226 and the total remains unresolved</div></article>
          <article class="metric-card"><div class="metric-kicker">TRANSIT RANK</div><div class="metric-value">Pending</div><div class="metric-label">Hotel-to-restaurant journey times were not verified consistently; blank is not zero</div></article>
        </div>
      </section>

      <section class="section two-up" aria-labelledby="summary-heading">
        <article class="panel">
          <div class="panel-heading"><div><p class="eyebrow">Executive summary</p><h2 id="summary-heading">What is ready to use</h2></div></div>
          <ul class="link-list">
            <li><strong>Hotel shortlist:</strong> five official room pages confirm a king and a private bathroom; room size ranges from 350 to 1,280 sq. ft. <a href="hotels.html">Compare rooms ↗</a></li>
            <li><strong>Food:</strong> the 2026 local MICHELIN list has four starred restaurants, three Bib Gourmand, and 17 Recommended/Selected. These labels are not interchangeable. <a href="restaurants.html">Browse all 24 ↗</a></li>
            <li><strong>Price anchors:</strong> named two-person menus are published for China Poblano ($120), Anima by EDO ($170), and Partage ($260–$420, depending on menu); these are pre-tax/tip.</li>
            <li><strong>Activities:</strong> several current attraction schedules and ticket prices are official; future changes are flagged. Bellagio’s Lunar New Year display is scheduled through Mar 6, 2027.</li>
          </ul>
        </article>
        <article class="panel">
          <p class="eyebrow">Price signal, not a winner</p>
          <h2>Cheapest verified date window?</h2>
          <p>The lowest Caesars seven-night calendar sum observed was <strong>$1,580 for Feb 15–22, 2027</strong>. On a later official recheck, the exact-date page displayed Julius Deluxe King at $201/night ($146 room rate + $55 resort fee, taxes excluded); an earlier capture showed $226/night. The latest page also displayed $196/night for a room-type-assigned option and a technical-difficulties notice. Because the rate displays conflict, the seven-night total remains unverified and this is not proven cheapest across the market or full travel window.</p>
          <p class="note">A separate Caesars offer advertises up to 30% off for stays booked 30+ days ahead; eligibility and an actual Feb 2027 total were not confirmed. <a href="analysis.html#booking-dates">See booking timing notes</a>.</p>
          <a class="link-arrow" href="hotels.html">Open hotel comparison</a>
        </article>
      </section>

      <section class="section" aria-labelledby="next-heading">
        <div class="section-head"><div><p class="eyebrow">Explore the dashboard</p><h2 id="next-heading">Start with the category you care about</h2></div><p>Every finding links directly to an official venue, hotel, operator, or tourism source.</p></div>
        <div class="finding-grid">
          <article class="finding-card"><span class="badge ok">5 candidates</span><h3>Hotels & rooms</h3><p>Bed, bathroom, room size, location, dated-rate evidence and the intentionally blank transit score.</p><a class="link-arrow" href="hotels.html">Compare hotels</a></article>
          <article class="finding-card"><span class="badge neutral">24 venues</span><h3>MICHELIN restaurants</h3><p>Stars, Bib Gourmand and Selected/Recommended are clearly separated; hours and meal-price gaps are visible.</p><a class="link-arrow" href="restaurants.html">Browse restaurants</a></article>
          <article class="finding-card"><span class="badge ok">8 options</span><h3>Activities & transit</h3><p>Official hours, two-adult ticket anchors, weather/service caveats and social links where confirmed.</p><a class="link-arrow" href="activities.html">Plan activities</a></article>
          <article class="finding-card"><span class="badge warn">Method</span><h3>Analysis & answers</h3><p>Knowns, missing information, practical Q&amp;A, price-basis notes and suggested next improvements.</p><a class="link-arrow" href="analysis.html">Read the analysis</a></article>
          <article class="finding-card"><span class="badge flag">Open items</span><h3>Flagged for Review</h3><p>Rate discrepancy, unverified fares and hours, temporary closures, social links, and a route matrix still to build.</p><a class="link-arrow" href="flagged.html">Review open items</a></article>
        </div>
      </section>

      <section class="section" aria-labelledby="meal-heading">
        <div class="section-head"><div><p class="eyebrow">Comparable only when the menu says so</p><h2 id="meal-heading">Published two-person menu anchors</h2></div><p>${verifiedMenus} venues have an explicit named menu/tasting-menu price for two in the current source snapshot. They are not a full ranking of value.</p></div>
        ${table(['Restaurant', 'MICHELIN distinction', 'Menu price for two', 'Price basis / caveat', 'Official source'], D.restaurants.filter((r) => r.mealForTwo), (r) => [
          `<span class="cell-title">${esc(r.name)}</span><span class="cell-note">${esc(r.area)}</span>`,
          badge(r.distinction, r.distinction.includes('Star') ? 'ok' : 'neutral'),
          `<strong>${esc(r.mealForTwo)}</strong>`,
          esc(r.mealNote),
          sourceStack(r, { guide: true })
        ])}
        <p class="table-footnote">Food prices are menu-only amounts before applicable tax, gratuity and optional beverages unless the linked official menu says otherwise. Future menus may change.</p>
      </section>

      <section class="section callout info" aria-labelledby="action-heading">
        <p class="eyebrow">Next decision (not requested from you)</p>
        <h2 id="action-heading">Keep the preferred dates and 1–2-week trip as separate plans.</h2>
        <p>This dashboard does not ask you to choose. It preserves the mismatch, provides the exact three-night preference, and uses a seven-night date range only where a verified date query was available. Check the review page before making bookings.</p>
        <a class="link-arrow" href="flagged.html">See the open checks</a>
      </section>`;
  }

  function renderHotels() {
    const target = document.getElementById('main');
    target.innerHTML = `${pageHeading('Stay · room fit · rate evidence', 'Hotel shortlist', pageInfo.hotels[1], 'STAY')}
      <div class="callout alert"><strong>No responsible transit ranking yet.</strong> All five options have an unmeasured reachability count, not a score of zero. RTC recommends a date/time-specific planner that returns transit routes, walking directions and travel times; the 5 × 24 hotel-to-restaurant matrix was not recorded, so no ranking is fabricated. <a href="${safeUrl(D.meta.rtcTripPlanner)}" target="_blank" rel="noopener noreferrer">Open RTC Trip Planner ↗</a></div>
      <section class="section">
        <div class="section-head"><div><p class="eyebrow">Two adults · actual-date test</p><h2>${esc(D.meta.comparisonStay)}</h2></div><p>Seven-night totals are shown only when a reliable, dated official quote exists. Unknown values remain blank and are flagged.</p></div>
        ${table(['Hotel / area', 'Room · bed · size', 'Private bathroom & amenities', 'Dated nightly result / 7-night total', 'MICHELIN restaurants ≤60 min by bus (verified)', 'Official sources'], D.hotels, (h) => [
          `<span class="cell-title">${esc(h.name)}</span><span class="cell-note">${esc(h.area)}</span>`,
          `<strong>${esc(h.room)}</strong><span class="cell-note">${esc(h.bed)} · ${esc(h.size)}</span>`,
          `${esc(h.bath)}<span class="cell-note">${esc(h.features)}</span>`,
          `${h.rate ? `<strong>${esc(h.rate)}</strong>` : missing('No reliable dated quote')}<span class="cell-note">${esc(h.totalNote)}</span>${h.rateStatus === 'flagged' ? badge('Total flagged', 'flag') : badge('Rate unverified', 'warn')}`,
          `${missing('Transit journey matrix not captured')}<span class="cell-note">${esc(h.transitNote)}</span>`,
          `<div class="source-links">${link(h.sourceUrl, 'Official room details')}${link(h.bookingUrl, h.id === 'caesars' ? 'Exact-date room list' : 'Check official availability')}</div>`
        ])}
        <p class="table-footnote">Private in-room bathroom and king bed are stated on the linked official room pages. Hotel location labels describe the Strip area, not a transit-time guarantee. A blank total is not $0.</p>
      </section>
      <section class="section grid-2">
        <article class="panel"><p class="eyebrow">Cheapest dates checked</p><h2>Caesars: Feb 15–22 is a lead, not a conclusion</h2><p>The flexible calendar showed a $1,580 seven-night sum for these dates. An earlier exact-date capture showed $226/night; a later recheck displayed $201/night for the Julius Deluxe King ($146 room rate + $55 resort fee, tax excluded) and $196/night for a room assigned on arrival. The later page also showed a technical-difficulties notice. The actual total is unresolved. No like-for-like comparison exists for the other four properties or all seven-night windows through Mar 23.</p>${sourceNote('Official exact-date booking result', D.hotels[0].bookingUrl, 'Reopen room list')}</article>
        <article class="panel"><p class="eyebrow">Room-quality comparison</p><h2>Largest spaces in the verified set</h2><p>Wynn Tower Suite Parlor (1,280 sq. ft.) and Venetian Skyline Grand Suite (1,170 sq. ft.) lead on published floor area; MGM King and Cosmopolitan City King are 446 and 460 sq. ft. Caesars’ room page and exact-date listing disagree (350 sq. ft. vs. 360+ sq. ft.), so its size is left blank pending room-type verification. Size is not value—dated rates and fee totals are still needed.</p><a class="link-arrow" href="analysis.html#known-missing">Read the comparison limits</a></article>
      </section>
      <section class="section callout"><strong>What would make the rank valid?</strong><p>Pick a consistent hotel origin point and a restaurant destination point, then query the RTC planner on the same representative 2027 date and dinner departure time for each of the 24 venues. Count end-to-end routes at or under 60 minutes, including the planner’s walk segments, and recheck service alerts. Until then, each hotel’s count remains blank.</p></section>`;
  }

  function renderRestaurants() {
    const target = document.getElementById('main');
    const starred = D.restaurants.filter((r) => r.distinction.includes('Star')).length;
    const bib = D.restaurants.filter((r) => r.distinction.includes('Bib')).length;
    const selected = D.restaurants.length - starred - bib;
    target.innerHTML = `${pageHeading('Eat · 2026 recognition · hours', 'MICHELIN-recognized restaurants', pageInfo.restaurants[1], '24')}
      <div class="callout info"><strong>Recognition labels are distinct.</strong> This source snapshot lists ${starred} starred restaurants (one two-star and three one-star), ${bib} Bib Gourmand restaurants, and ${selected} Recommended/Selected restaurants. Bib Gourmand and Recommended/Selected are not MICHELIN stars. The 2026 tourism list is linked on every row for cross-checking.</div>
      <div class="toolbar"><label class="search-box"><span aria-hidden="true">⌕</span><span class="sr-only">Filter restaurants</span><input id="restaurant-search" type="search" placeholder="Search name, area, distinction, or hours" autocomplete="off"></label><span id="restaurant-count" class="small" aria-live="polite">${D.restaurants.length} restaurants</span></div>
      ${table(['Restaurant', '2026 MICHELIN distinction', 'Area / property', 'Days & hours', 'Exceptions / access notes', 'Published meal price for two', 'Social', 'Official source links'], D.restaurants, (r) => [
        `<span class="cell-title">${esc(r.name)}</span><span class="cell-note">${esc(r.status)}</span>`,
        badge(r.distinction, r.distinction.includes('Star') ? 'ok' : (r.distinction.includes('Bib') ? 'warn' : 'neutral')),
        esc(r.area),
        r.hours ? esc(r.hours) : missing('Hours not verified'),
        esc(r.exceptions),
        `${r.mealForTwo ? `<strong>${esc(r.mealForTwo)}</strong>` : missing('No complete total confirmed')}<span class="cell-note">${esc(r.mealNote)}</span>`,
        r.socialUrl ? `<div class="source-links">${link(r.socialUrl, 'Instagram')}${r.socialAltUrl ? link(r.socialAltUrl, 'TikTok') : ''}</div>` : missing('No official social link confirmed'),
        sourceStack(r, { guide: true })
      ])}
      <p class="table-footnote">Hours are the official schedules found at the research snapshot, not confirmed 2027 bookings. Empty price cells intentionally avoid inferring a full meal from selected dishes. Prices shown are menu anchors before tax/tip; see the linked official menu.</p>
      <section class="section grid-2">
        <article class="panel"><p class="eyebrow">Starred</p><h2>Reserve far ahead where seating is limited</h2><p>Joël Robuchon, L’Atelier and é publish limited dinner schedules; é’s official page says reservations open up to three months ahead. Guy Savoy’s weekly hours and complete two-person cost still need confirmation.</p><a class="link-arrow" href="${safeUrl(D.meta.michelinSource)}" target="_blank" rel="noopener noreferrer">Review the 2026 list</a></article>
        <article class="panel"><p class="eyebrow">Potential bookable issue</p><h2>Michael Mina currently shows “Temporarily closed”</h2><p>The official Bellagio page displayed a $295++ tasting-menu price per person but was closed on Nov 26, 2026. The price is a menu snapshot, not proof the restaurant will be serving during the 2027 trip.</p>${link('https://bellagio.mgmresorts.com/en/restaurants/michael-mina.html', 'Recheck Michael Mina official page', 'link-arrow')}</article>
      </section>`;

    const input = document.getElementById('restaurant-search');
    const count = document.getElementById('restaurant-count');
    const rows = Array.from(target.querySelectorAll('tbody tr'));
    input.addEventListener('input', () => {
      const query = input.value.trim().toLocaleLowerCase();
      let shown = 0;
      rows.forEach((row) => {
        const matches = row.textContent.toLocaleLowerCase().includes(query);
        row.hidden = !matches;
        if (matches) shown += 1;
      });
      count.textContent = `${shown} of ${rows.length} restaurants`;
    });
  }

  function renderActivities() {
    const target = document.getElementById('main');
    target.innerHTML = `${pageHeading('See · explore · ride', 'Activities & getting around', pageInfo.activities[1], 'DO')}
      <div class="callout info"><strong>Ticket prices are current official page values, not 2027 guarantees.</strong> Pair totals below are simple multiplication for two adults. Future taxes, ticketing fees, inventory, special events and service interruptions must be checked at purchase time.</div>
      <section class="section">
        ${table(['Experience', 'Official schedule / hours', 'Exceptions & planning notes', 'Cost for two adults', 'Social', 'Official source / tickets'], D.activities, (a) => [
          `<span class="cell-title">${esc(a.name)}</span><span class="cell-note">${esc(a.details)}</span>`,
          a.hours ? esc(a.hours) : missing('Hours not stated in reviewed source'),
          esc(a.exceptions),
          `${a.priceForTwo ? `<strong>${esc(a.priceForTwo)}</strong>` : missing('Price not confirmed')}<span class="cell-note">${esc(a.priceNote)}</span>`,
          a.socialUrl ? `<div class="source-links">${link(a.socialUrl, 'Instagram')}${a.socialAltUrl ? link(a.socialAltUrl, 'TikTok') : ''}</div>` : missing('No official social link confirmed'),
          `<div class="source-links">${link(a.officialUrl, 'Official details')}${a.ticketUrl && a.ticketUrl !== a.officialUrl ? link(a.ticketUrl, 'Tickets / fare') : ''}</div>`
        ])}
        <p class="table-footnote">Bellagio Conservatory entry price and separate daily hours were not stated on the official page reviewed. Bellagio Gallery of Fine Art is listed as temporarily closed. Both remain flagged.</p>
      </section>
      <section class="section grid-2">
        <article class="panel"><p class="eyebrow">Best seasonal overlap</p><h2>Lunar New Year at Bellagio</h2><p>The official Conservatory calendar lists the Lunar New Year installation from Jan 9 through Mar 6, 2027—covering the preferred Feb 15–18 visit and the seven-night comparison dates. Dark dates Mar 7–12 fall inside the wider trip window.</p>${link('https://bellagio.mgmresorts.com/en/entertainment/conservatory-botanical-garden.html', 'Check the official installation calendar', 'link-arrow')}</article>
        <article class="panel"><p class="eyebrow">Transit planning</p><h2>Use a trip-time search, not just a route map</h2><p>The RTC planner accepts an origin, destination, date and time and supplies route choices, walk directions and travel times. Use it to validate the requested one-hour restaurant reach before choosing a hotel; bus frequency, Strip traffic and walking inside resorts can all change the result.</p>${link(D.meta.rtcTripPlanner, 'Open RTC Trip Planner', 'link-arrow')}</article>
      </section>`;
  }

  function renderAnalysis() {
    const target = document.getElementById('main');
    const costRows = D.restaurants.filter((r) => r.mealForTwo);
    target.innerHTML = `${pageHeading('Method · knowns · next steps', 'Analysis & answers', pageInfo.analysis[1], 'WHY')}
      <section class="section" id="known-missing">
        <div class="section-head"><div><p class="eyebrow">Evidence at a glance</p><h2>Known vs. still missing</h2></div><p>“Blank” means unverified in the sources reviewed—not a zero, a closure, or an estimate.</p></div>
        <div class="grid-2">
          <article class="panel"><span class="badge ok">Known</span><h3>What the official sources support</h3><ul class="link-list">
            <li>2026 Las Vegas MICHELIN selection: 24 venues—one two-star, three one-star, three Bib Gourmand, and 17 Recommended/Selected. ${link(D.meta.michelinSource, 'List source')}</li>
            <li>Five selected hotel room pages describe a king bed and private bathroom; only Caesars returned date-specific rate displays, which conflict ($201/night for Julius King on recheck vs. an earlier $226/night capture). ${link(D.hotels[0].sourceUrl, 'Room source')}</li>
            <li>Current official menus give named two-person anchors at China Poblano, Anima by EDO and Partage. ${link('https://www.chinapoblano.com/menus/', 'Example official menu')}</li>
            <li>RTC provides a date/time-specific transit planner and current visitor fares. ${link(D.meta.rtcTripPlanner, 'Trip planner')}</li>
            <li>Bellagio lists Lunar New Year from Jan 9–Mar 6, 2027 and dark dates Mar 7–12. ${link('https://bellagio.mgmresorts.com/en/entertainment/conservatory-botanical-garden.html', 'Installation calendar')}</li>
          </ul></article>
          <article class="panel"><span class="badge flag">Missing / not verified</span><h3>What is not ready to compare</h3><ul class="link-list">
            <li>A like-for-like seven-night all-in hotel total for all five candidates and all potential dates.</li>
            <li>A reconciled Caesars total: same-date displays varied ($196, $201 and earlier $226 per night), the calendar sums $1,580, and the latest room-list page showed a technical-difficulties notice.</li>
            <li>The count/rank of restaurants reachable within 60 minutes by RTC bus from each hotel.</li>
            <li>A complete two-person meal cost for most restaurants; future menus, tax, tip, drinks and availability vary.</li>
            <li>Several weekly hours, Yen Viet’s conflicting schedule, and 2027 holiday/special-event exceptions.</li>
            <li>Michael Mina reopening and Bellagio Gallery of Fine Art reopening dates.</li>
          </ul><a class="link-arrow" href="flagged.html">Open the full issue register</a></article>
        </div>
      </section>

      <section class="section" id="booking-dates">
        <div class="section-head"><div><p class="eyebrow">Actual-date check</p><h2>Cheapest upcoming booking dates</h2></div></div>
        <div class="grid-2">
          <article class="panel"><span class="badge warn">Provisional date lead</span><h3>Feb 15–22, 2027 · Caesars Palace · two adults</h3><p>Lowest Caesars seven-night flexible-calendar sum observed: <strong>$1,580</strong>. The earlier exact-date capture showed $226/night; a later recheck displayed Julius Deluxe King at <strong>$201/night</strong> ($146 room rate + $55 daily resort fee, taxes excluded), and a separate assigned-room rate at $196/night. The later page also showed a technical-difficulties notice. The earlier $226 × 7 implies $1,582; $201 × 7 is $1,407 by arithmetic, but neither product is a checkout total. There is no reconciled seven-night bill.</p>${link(D.hotels[0].bookingUrl, 'Open exact-date room list', 'link-arrow')}<p class="note">This is not a demonstrated market-wide cheapest date. The other hotel booking flows did not produce reliable dated rates, and other seven-night windows through Mar 23 were not compared like-for-like.</p></article>
          <article class="panel"><span class="badge neutral">Booking lead time</span><h3>Discount windows are not a substitute for a dated quote</h3><p>Caesars’ official page lists up to 30% off for stays booked 30+ days in advance (additional terms apply). MGM Grand’s page showed a limited-time Black Friday offer up to 30% plus $100 F&amp;B credit, and up to 45% for Rewards members. Neither source verifies the requested room’s final Feb/Mar 2027 total.</p><div class="source-links">${link('https://www.caesars.com/caesars-palace/hotel', 'Caesars offer terms')}${link('https://mgmgrand.mgmresorts.com/en/offers/wifi.html', 'MGM Grand offer')}</div></article>
        </div>
      </section>

      <section class="section">
        <div class="section-head"><div><p class="eyebrow">Explicit menu prices</p><h2>Two-person food price anchors</h2></div><p>These are selected set/tasting menus, not equivalent meal baskets or full-trip restaurant budgets.</p></div>
        ${table(['Restaurant', 'Published price for 2', 'What the price covers', 'Official menu/source'], costRows, (r) => [
          `<span class="cell-title">${esc(r.name)}</span><span class="cell-note">${esc(r.distinction)}</span>`,
          `<strong>${esc(r.mealForTwo)}</strong>`, esc(r.mealNote), sourceStack(r, { guide: true })
        ])}
        <p class="table-footnote">Michael Mina is flagged temporarily closed; its listed $590++ two-person menu price is conditional on future reopening and availability.</p>
      </section>

      <section class="section" aria-labelledby="method-heading">
        <div class="section-head"><div><p class="eyebrow">Decision logic</p><h2 id="method-heading">Method and definitions</h2></div></div>
        <div class="grid-3">
          <article class="panel"><h3>Stay length</h3><p>The preferred Feb 15–18 span equals three nights. The requested duration is 7–14 nights. The Feb 15–22 seven-night check is presented as a separate comparison scenario only; no itinerary length was silently chosen.</p></article>
          <article class="panel"><h3>Hotel comparison</h3><p>Room fit is confirmed only where an official page names a king (or larger) bed and private bathroom. Price comparison requires the same dates, two adults, comparable cancellation terms, resort fee and tax treatment.</p></article>
          <article class="panel"><h3>Transit ranking</h3><p>A restaurant counts only if a consistent RTC route planner search for the trip date/time shows an end-to-end bus journey of 60 minutes or less. No route matrix was verified, so counts and ranking stay blank.</p></article>
          <article class="panel"><h3>MICHELIN labels</h3><p>Stars, Bib Gourmand and Recommended/Selected are different Guide distinctions. The 2026 source list is not a guarantee that a restaurant remains open or retains a distinction in 2027.</p></article>
          <article class="panel"><h3>Meal-cost basis</h3><p>Only explicit named menu prices are shown. They do not automatically include taxes, gratuity, drinks, upgrades, service charges or future menu changes unless the source says so.</p></article>
          <article class="panel"><h3>Snapshot discipline</h3><p>Findings were checked on ${esc(D.meta.researchedAt)}. A fresh check is needed before booking and again before travel; public transport and holiday hours can change.</p></article>
        </div>
      </section>

      <section class="section" aria-labelledby="qa-heading">
        <div class="section-head"><div><p class="eyebrow">Questions & answers</p><h2 id="qa-heading">Quick answers</h2></div></div>
        <details class="qa-card"><summary>Which hotel is cheapest?</summary><div class="qa-answer"><p>Not established. Caesars is the only property with a usable dated rate display, but the same-date captures varied: $226/night in an earlier result, then $201/night for Julius King and $196/night for room assigned on arrival on a later page that also showed a technical-difficulties notice. The flexible calendar summed to $1,580. Four other date-rate checks were unusable. The hotel page keeps the total blank until the room/rate and final checkout amount are reconciled.</p>${link(D.hotels[0].bookingUrl, 'Review the official rate result')}</div></details>
        <details class="qa-card"><summary>Which hotel has the most MICHELIN restaurants within an hour by bus?</summary><div class="qa-answer"><p>Unknown. No verified hotel-to-restaurant transit matrix exists yet. RTC’s official planner takes the travel date and time; each of five hotel origins needs to be checked against all 24 restaurant destinations. The blank score is not a zero.</p>${link(D.meta.rtcTripPlanner, 'Open RTC Trip Planner')}</div></details>
        <details class="qa-card"><summary>Are Bib Gourmand and Recommended restaurants starred?</summary><div class="qa-answer"><p>No. They are separate MICHELIN Guide distinctions. The current 2026 list has four starred venues (one two-star and three one-star), three Bib Gourmand, and 17 Recommended/Selected. The distinction is printed in each restaurant row.</p>${link(D.meta.michelinSource, 'Review the 2026 list')}</div></details>
        <details class="qa-card"><summary>Why are most restaurant meal prices blank?</summary><div class="qa-answer"><p>A menu item price is not a complete two-person meal. Without an official prix-fixe or clearly defined basket, producing a total would be an unsupported estimate. The few named set/tasting-menu amounts are labeled and shown before tax/tip.</p><a href="restaurants.html" class="link-arrow">Browse the restaurant table</a></div></details>
        <details class="qa-card"><summary>What is the best booking date or day of week?</summary><div class="qa-answer"><p>No cheapest book-on date or market-wide cheapest stay date was verified. The Feb 15–22 Caesars figure is a provisional calendar lead, not an all-hotel comparison. Re-run the official booking engines across the exact travel window and compare complete totals.</p><a href="#booking-dates" class="link-arrow">See the rate discrepancy</a></div></details>
      </section>

      <section class="section" aria-labelledby="improvements-heading">
        <div class="section-head"><div><p class="eyebrow">Product ideas</p><h2 id="improvements-heading">Suggestions for improving this site</h2></div><p>These are future enhancements—not features already implemented.</p></div>
        <div class="grid-3">
          <article class="suggestion-card"><span class="suggestion-number">01</span><h3>Comparable hotel quote snapshots</h3><p>Add a date-range picker that stores two-adult quote, room type, taxes, resort fee, cancellation rule, timestamp and source for each property.</p></article>
          <article class="suggestion-card"><span class="suggestion-number">02</span><h3>Transit reachability matrix</h3><p>Record RTC planner time, route, transfers and walking time for every hotel/restaurant pair on a common departure date; sort hotels by verified count under 60 minutes.</p></article>
          <article class="suggestion-card"><span class="suggestion-number">03</span><h3>Meal basket estimator</h3><p>Let a planner define courses and drinks from current official menus; separate food subtotal, tax, service charge and optional tip instead of using vague averages.</p></article>
          <article class="suggestion-card"><span class="suggestion-number">04</span><h3>Trip-date closure alerts</h3><p>Track restaurants and attractions with hours, reservation windows, temporary closures and date exceptions, with a recheck queue at 30 and 7 days before travel.</p></article>
          <article class="suggestion-card"><span class="suggestion-number">05</span><h3>Printable plan and exports</h3><p>Allow a visitor to make a daily itinerary, print it, or export an .ics/CSV list of stops and saved official links.</p></article>
          <article class="suggestion-card"><span class="suggestion-number">06</span><h3>Source freshness indicators</h3><p>Show when each fact was captured, mark pages that changed, and prompt review when an offer or schedule is older than its validity window.</p></article>
        </div>
      </section>`;
  }

  function renderFlagged() {
    const target = document.getElementById('main');
    const high = D.flags.filter((f) => f.priority === 'High').length;
    const cards = D.flags.map((f) => `
      <article class="flag-card" data-priority="${esc(f.priority)}">
        <div class="flag-top"><div><h3>${esc(f.title)}</h3><span class="badge ${f.priority === 'High' ? 'flag' : (f.priority === 'Low' ? 'ok' : 'warn')}">${esc(f.priority)} priority</span></div></div>
        <p>${esc(f.issue)}</p>
        <p class="flag-next"><strong>Suggested verification:</strong> ${esc(f.next)}</p>
        ${f.sourceUrl ? `<div class="source-links">${link(f.sourceUrl, f.sourceText || 'Official source')}</div>` : `<p class="note">Source: ${esc(f.sourceText || 'User-provided trip requirements')}.</p>`}
      </article>`).join('');
    target.innerHTML = `${pageHeading('Open issues · no guesses', 'Flagged for Review', pageInfo.flagged[1], 'CHECK')}
      <div class="callout alert"><strong>${high} high-priority items are unresolved.</strong> These gaps do not block browsing the dashboard, but the rate discrepancy and transit ranking must be resolved before calling a hotel or date “best.”</div>
      <section class="section"><div class="section-head"><div><p class="eyebrow">Review register</p><h2>Open questions and how to close them</h2></div><p>Priority indicates planning impact, not source credibility. All venue facts link to the official page reviewed.</p></div><div class="flag-list">${cards}</div></section>
      <section class="section grid-2">
        <article class="panel"><p class="eyebrow">Data policy</p><h2>Blanks are deliberate</h2><p>Where a rate, hours, menu total, transit duration or future opening could not be confirmed from a trusted official source, the value is left blank and called out here. No zero, ranking, “typical” meal basket or market-wide cheapest claim is inferred.</p></article>
        <article class="panel"><p class="eyebrow">Recheck cadence</p><h2>Before the booking</h2><p>Refresh hotel quotes before choosing a stay; confirm restaurant opening and reservations when dates open; check official attraction hours and RTC alerts 30 days and 7 days before the trip, then again on the day.</p>${link(D.meta.rtcHowToRide, 'RTC planning guidance', 'link-arrow')}</article>
      </section>`;
  }

  drawHeader();
  drawFooter();
  if (page === 'home') renderHome();
  else if (page === 'hotels') renderHotels();
  else if (page === 'restaurants') renderRestaurants();
  else if (page === 'activities') renderActivities();
  else if (page === 'analysis') renderAnalysis();
  else if (page === 'flagged') renderFlagged();
  else renderHome();
})();
