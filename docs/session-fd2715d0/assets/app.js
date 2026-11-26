/* Vegas2 static pages: JSON-backed tables, no dependencies or fabricated platform search links. */
const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeUrl = (value) => /^https:\/\//i.test(String(value || '')) ? String(value) : '';
const external = (url, label) => safeUrl(url) ? `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>` : '';
const social = (items) => (Array.isArray(items) && items.length) ? items.map(s => external(s.url, s.platform)).filter(Boolean).join(' · ') : '<span class="cell-muted">No official venue account verified</span>';
const tagFor = (status) => {
  if (String(status).includes('Stars')) return `<span class="tag star">${esc(status)}</span>`;
  if (status === 'Bib Gourmand') return `<span class="tag">Bib Gourmand</span>`;
  return `<span class="tag">Selected · no star</span>`;
};
async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Could not load ${path} (${response.status})`);
  return response.json();
}
function searchText(item) { return JSON.stringify(item).toLowerCase(); }
function emptyValue(value, note='Not verified') {
  return value ? esc(value) : `<span class="blank">—</span><span class="cell-muted">${esc(note)}</span>`;
}
function sourceCell(primary, extras=[]) {
  const links = [external(primary, 'Official source'), ...extras.map((x, i) => external(x, `Source ${i+2}`))].filter(Boolean);
  return links.length ? `<div class="cell-links">${links.join('')}</div>` : '<span class="cell-muted">No source link</span>';
}

async function renderHotels() {
  const table = document.getElementById('hotels-table'); if (!table) return;
  const data = await loadJson('data/hotels.json');
  const query = (document.getElementById('q')?.value || '').toLowerCase();
  const sort = document.getElementById('sort')?.value || 'count';
  const hotels = data.hotels.filter(h => !query || searchText(h).includes(query));
  if (sort === 'count') hotels.sort((a,b) => b.on_property_count - a.on_property_count || a.name.localeCompare(b.name));
  if (sort === 'name') hotels.sort((a,b) => a.name.localeCompare(b.name));
  table.innerHTML = `<thead><tr><th>Hotel · official booking page</th><th>MICHELIN Guide restaurants on property / resort complex</th><th>7-night total (2 adults)</th><th>Official room-type evidence · date inventory unverified</th><th>Public transit ≤60 min</th><th>Official sources / status</th></tr></thead><tbody>${hotels.map(h => {
    const guideLinks = h.michelin_sources.map((url, i) => external(url, h.on_property_restaurants[i] || `Guide profile ${i+1}`)).join('<br>');
    return `<tr><td>${external(h.official_url, h.name)}<span class="cell-muted">${esc(h.area)}</span></td><td><strong>${h.on_property_count}</strong> confirmed Guide entries<span class="cell-muted">${guideLinks}</span></td><td>${emptyValue(h.seven_night_total, 'No live official quote captured')}<span class="cell-muted">Fee: ${emptyValue(h.resort_fee, 'not checked')}</span><span class="cell-muted">${external(h.booking_url, 'Check official booking page')}</span></td><td>${h.room_option ? `<strong>${esc(h.room_option)}</strong><span class="cell-muted">${esc(h.room_fit)}</span>` : emptyValue(h.room_fit, 'no room-type page captured')}<span class="cell-muted">${esc(h.room_requirement_note)}</span><span class="cell-muted">${external(h.room_url, 'Official room details')}</span></td><td>${emptyValue(h.within_60min_public_transit, 'route not verified')}</td><td>${sourceCell(h.official_url, h.michelin_sources)}<span class="cell-muted">⚑ ${esc(h.flag)}</span></td></tr>`;
  }).join('')}</tbody>`;
  const count = document.getElementById('hotels-count'); if (count) count.textContent = `${hotels.length} candidate hotels · ordered by same-property Guide count, not transit time`;
}

async function renderRestaurants() {
  const table = document.getElementById('restaurants-table'); if (!table) return;
  const data = await loadJson('data/restaurants.json');
  const query = (document.getElementById('q')?.value || '').toLowerCase();
  const filter = document.getElementById('filter')?.value || 'all';
  const restaurants = data.restaurants.filter(r => {
    if (filter === 'starred' && !r.distinction.includes('Stars') && !r.distinction.includes('Star')) return false;
    if (filter === 'bib' && r.distinction !== 'Bib Gourmand') return false;
    if (filter === 'selected' && !r.distinction.startsWith('Selected')) return false;
    return !query || searchText(r).includes(query);
  });
  const order = s => s.includes('2 MICHELIN Stars') ? 0 : s.includes('1 MICHELIN Star') ? 1 : s === 'Bib Gourmand' ? 2 : 3;
  restaurants.sort((a,b) => order(a.distinction)-order(b.distinction) || a.name.localeCompare(b.name));
  table.innerHTML = `<thead><tr><th>Restaurant · official Guide profile</th><th>2026 Guide status</th><th>Guide price tier</th><th>Cost for two</th><th>Current official profile hours</th><th>2027 exceptions / social</th><th>Sources</th></tr></thead><tbody>${restaurants.map(r => {
    const cost = r.cost_for_two ? esc(r.cost_for_two) : '<span class="blank">—</span><span class="cell-muted">No official fixed two-person total verified</span>';
    const hrs = r.current_hours ? `${esc(r.current_hours)}<span class="cell-muted">MICHELIN profile snapshot ${esc(r.hours_as_of)}; recheck for 2027.</span>` : '<span class="blank">—</span><span class="cell-muted">No complete official weekly schedule captured</span>';
    return `<tr><td>${external(r.guide_url, r.name)}<span class="cell-muted">${esc(r.cuisine)} · ${esc(r.location)}</span></td><td>${tagFor(r.distinction)}</td><td>${emptyValue(r.price_tier, 'not shown')}</td><td>${cost}</td><td>${hrs}</td><td>${r.exceptions ? esc(r.exceptions) : '<span class="cell-muted">No 2027 exception schedule verified</span>'}<span class="cell-muted">${social(r.social_urls)}</span><span class="cell-muted">⚑ ${esc(r.flag)}</span></td><td>${sourceCell(r.guide_url, [r.venue_url, r.menu_url, data.meta.official_guide_release])}</td></tr>`;
  }).join('')}</tbody>`;
  const count = document.getElementById('restaurants-count'); if (count) count.textContent = `${restaurants.length} of 24 restaurants`;
}

async function renderActivities() {
  const table = document.getElementById('activities-table'); if (!table) return;
  const data = await loadJson('data/activities.json');
  const query = (document.getElementById('q')?.value || '').toLowerCase();
  const activities = data.activities.filter(a => !query || searchText(a).includes(query));
  table.innerHTML = `<thead><tr><th>Activity · official operator</th><th>Cost for two</th><th>Days / hours / exceptions</th><th>≤60 min by public transit?</th><th>Official social links</th><th>Source / unverified items</th></tr></thead><tbody>${activities.map(a => `<tr><td>${external(a.official_url, a.name)}<span class="cell-muted">${esc(a.category)} · ${esc(a.location)}</span></td><td>${emptyValue(a.cost_for_two, 'not verified')}</td><td>${a.days_open ? `<strong>Days:</strong> ${esc(a.days_open)}` : '<strong>Days:</strong> —'}<br>${a.hours ? `<strong>Hours:</strong> ${esc(a.hours)}` : '<strong>Hours:</strong> —'}<br><span class="cell-muted"><strong>Exceptions:</strong> ${a.exceptions ? esc(a.exceptions) : 'Not verified'}</span></td><td>${emptyValue(a.transit_within_60min, 'hotel-origin route not verified')}<span class="cell-muted">${esc(a.transit_note)}</span></td><td>${social(a.social_urls)}</td><td>${sourceCell(a.official_url, [a.social_source_url])}<span class="cell-muted">⚑ ${esc(a.flag)}</span></td></tr>`).join('')}</tbody>`;
  const count = document.getElementById('activities-count'); if (count) count.textContent = `${activities.length} activity/transport candidates · none certified under the hotel-origin time rule`;
}

async function renderDates() {
  const table = document.getElementById('dates-table'); if (!table) return;
  const data = await loadJson('data/dates.json');
  const query = (document.getElementById('q')?.value || '').toLowerCase();
  const windows = data.windows.filter(w => !query || `${w.checkin} ${w.checkout}`.toLowerCase().includes(query));
  table.innerHTML = `<thead><tr><th>Check-in → check-out</th><th>Nights</th><th>Verified official hotel total</th><th>Quote / source</th></tr></thead><tbody>${windows.map(w => `<tr><td><strong>${esc(w.checkin)} → ${esc(w.checkout)}</strong><span class="cell-muted">Calculated from requested date range</span></td><td>${w.nights}</td><td><span class="blank">—</span><span class="cell-muted">No official quote captured</span></td><td>${external(w.quote_source, 'Open official hotel site')}<span class="cell-muted">No specific booking result verified for these dates.</span></td></tr>`).join('')}</tbody>`;
  const count = document.getElementById('dates-count'); if (count) count.textContent = `${windows.length} of ${data.windows.length} possible seven-night windows`;
}

document.addEventListener('DOMContentLoaded', () => {
  const run = () => Promise.allSettled([renderHotels(), renderRestaurants(), renderActivities(), renderDates()]).then(results => {
    results.filter(r => r.status === 'rejected').forEach(r => console.error(r.reason));
  });
  run();
  document.getElementById('q')?.addEventListener('input', run);
  document.getElementById('sort')?.addEventListener('change', renderHotels);
  document.getElementById('filter')?.addEventListener('change', renderRestaurants);
});
