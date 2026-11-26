// Vegas2 renderer: builds tables from data/*.json. Unverified fields show blank + flag.
(function () {
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const UNV = '<span class="badge badge-unverified">Unverified</span>';
  const cell = (v, fallback = UNV) => (v === undefined || v === null || v === '') ? fallback : esc(v);
  const link = (url, label) => url ? `<a class="link-btn" href="${esc(url)}" target="_blank" rel="noopener">${label}</a>` : UNV;
  const social = s => {
    const parts = [];
    const cfg = [['youtube','YT','YouTube'],['tiktok','TT','TikTok'],['instagram','IG','Instagram']];
    cfg.forEach(([k, short, full]) => { if (s && s[k]) parts.push(`<a href="${esc(s[k])}" target="_blank" rel="noopener" title="${full}">${short}</a>`); });
    return parts.length ? `<div class="social-links">${parts.join('')}</div>` : UNV;
  };
  const table = (headers, rows) => `<div class="table-wrap"><table><thead><tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`;
  const row = cells => `<tr>${cells.map(c => `<td>${c}</td>`).join('')}</tr>`;
  const badgeFor = k => ({twoStars:'badge-star2',oneStar:'badge-star1',bibGourmand:'badge-bib',recommended:'badge-rec'})[k] || 'badge-rec';
  const load = p => fetch(p).then(r => r.json());
  const out = id => document.getElementById(id);

  function restaurants(d) {
    const order = {twoStars:0,oneStar:1,bibGourmand:2,recommended:3};
    const rows = d.restaurants.slice().sort((a,b)=>order[a.distinctionKey]-order[b.distinctionKey]).map(r => row([
      `<span class="name-cell">${esc(r.name)}</span>`,
      `<span class="badge ${badgeFor(r.distinctionKey)}">${esc(r.distinction)}</span><div class="sub-note">${r.distinctionKey==='recommended'||r.distinctionKey==='bibGourmand' ? 'Listed in guide' : 'Currently holds star(s)'}</div>`,
      cell(r.address),
      `${cell(r.costForTwo)}<div class="sub-note">Total for 2 adults</div>`,
      cell(r.daysOpen) + '<div class="sub-note">Hours: ' + cell(r.hours) + '</div>',
      social(r.social),
      link(r.officialUrl, 'Official site') + ' ' + link(r.michelinUrl, 'Michelin')
    ]));
    out('content').innerHTML = `
      <div class="page-header"><h2>Michelin Restaurants — Las Vegas</h2>
      <div class="sub">Source: ${link(d.sourceUrl,'MICHELIN official press release')} (${esc(d.edition)}).</div></div>
      <div class="callout info"><span class="ct-title">Guide status</span>
        <b>Currently holds a star</b>: 2★ and 1★ rows. <b>Listed in guide</b>: Bib Gourmand and Michelin Recommended rows (no star). Cost, hours and social links are blank until verified from official sites.</div>
      ${table(['Restaurant','Michelin status','Address','Cost for 2 adults (total)','Days & hours','Social','Links'], rows)}`;
  }

  function hotels(d) {
    const rows = d.hotels.map(h => row([
      `<b>#${h.rank}</b>`,
      `<span class="name-cell">${esc(h.name)}</span><div class="sub-note">${esc(h.address)}</div>`,
      cell(h.roomType) + (h.id==='h-mgmgrand' ? '<div class="sub-note">Confirmed on mgmgrand.com</div>' : ''),
      cell(h.privateBath, UNV),
      cell(h.queenBed, UNV),
      esc(h.michelinOnSite || ''),
      `${cell(h.price7NightTotalUsd)}<div class="sub-note">7 nights Feb 15–22, 2027</div>`,
      cell(h.cheapestBookingWindow),
      link(h.officialUrl, 'Official site') + ' ' + link(h.bookingUrl, 'Book / rates')
    ]));
    out('content').innerHTML = `
      <div class="page-header"><h2>Hotels — ranked by on-site Michelin listings</h2>
      <div class="sub">Party: ${esc(d.trip.guests)} · ${esc(d.trip.roomRequirement)}</div></div>
      <div class="callout warn"><span class="ct-title">Pricing not verified</span>${esc(d.sourceNote)}</div>
      <div class="callout info"><span class="ct-title">Ranking basis</span>${esc(d.rankingBasis)}</div>
      ${table(['Rank','Hotel','Room type','Private bath','Queen+ bed','Michelin on site','7-night total','Best booking window','Links'], rows)}
      <h3 class="section-title">Notes</h3><ul class="info-card">${d.verificationNotes.map(n=>`<li>${esc(n)}</li>`).join('')}</ul>`;
  }

  function activities(d) {
    const rows = d.activities.map(a => row([
      `<span class="name-cell">${esc(a.name)}</span><div class="sub-note">${esc(a.category)}</div>`,
      esc(a.address),
      cell(a.daysOpen) + '<div class="sub-note">Hours: ' + cell(a.hours) + '</div>',
      cell(a.costEstimateUsd),
      esc(a.within1HrByBusHotel),
      social({youtube:a.youtube,tiktok:a.tiktok,instagram:a.instagram}),
      link(a.officialUrl, 'Official site')
    ]));
    out('content').innerHTML = `
      <div class="page-header"><h2>Activities</h2><div class="sub">Travel limit: ${esc(d.trip.travelLimit)}</div></div>
      <div class="callout info"><span class="ct-title">Transit</span>${esc(d.trip.note)}</div>
      ${table(['Activity','Address','Days & hours','Cost (2 adults)','Within ~1 hr of hotel','Social','Link'], rows)}
      <h3 class="section-title">Notes</h3><ul class="info-card">${d.verificationNotes.map(n=>`<li>${esc(n)}</li>`).join('')}</ul>`;
  }

  function flagged(R, H, A) {
    const items = [];
    R.restaurants.forEach(r => items.push(['Restaurant', r.name, 'Hours/days, cost for two, social links, venue & guide URLs not fetched', r.michelinUrl || r.officialUrl]));
    H.hotels.forEach(h => items.push(['Hotel', h.name, 'Feb 2027 7-night price, private bath, queen bed, booking window — ' + (h.id==='h-mgmgrand'?'room type confirmed; rest unverified':'official page not fetched'), h.officialUrl]));
    A.activities.forEach(a => items.push(['Activity', a.name, 'Hours, days, cost, social links unverified', a.officialUrl]));
    out('content').innerHTML = `
      <div class="page-header"><h2>Flagged for Review</h2><div class="sub">Items that could not be confirmed from an official source. These do not block publication. Review and request changes.</div></div>
      <div class="callout warn"><span class="ct-title">Irregularities</span>
        <ul>
          <li>Hotel live pricing for Feb 15–22, 2027 could not be retrieved (Wynn page failed; booking engines are JavaScript-rendered).</li>
          <li>Restaurant hours, cost, and social links are not in the Michelin release and were not fetched from venue sites.</li>
          <li>Michelin venue/guide links were not fetched in this session.</li>
          <li>Esther's Kitchen cuisine and Michelin link were not recorded; the row shows only the official distinction and address.</li>
          <li>Transit reach claims (Deuce, Monorail) come from secondary guides, not an RTC timetable.</li>
        </ul></div>
      ${table(['Category','Item','Issue','Source to check'], items.map(i => row([esc(i[0]), `<b>${esc(i[1])}</b>`, esc(i[2]), link(i[3], 'Open'), ])))}`;
  }

  function staticPage(html) { out('content').innerHTML = html; }

  window.VegasApp = { restaurants, hotels, activities, flagged, staticPage, load };
})();
