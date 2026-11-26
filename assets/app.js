/* Vegas2 trip planner — vanilla JS, no build step. Renders tables from data/*.json */
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function yt(q){return 'https://www.youtube.com/results?search_query='+encodeURIComponent(q)}
function tt(q){return 'https://www.tiktok.com/search?q='+encodeURIComponent(q)}
function ig(q){return 'https://www.instagram.com/explore/search/keyword/?q='+encodeURIComponent(q)}
function social(name){
  return '<span class="social"><a href="'+yt(name+' Las Vegas')+'" target="_blank" rel="noopener">▶ YouTube</a><a href="'+tt(name+' Las Vegas')+'" target="_blank" rel="noopener">♪ TikTok</a><a href="'+ig(name+' Las Vegas')+'" target="_blank" rel="noopener">◎ Instagram</a></span>';
}
function badge(v){
  if(v==='verified') return '<span class="badge b-green">✓ Verified</span>';
  if(v==='partial') return '<span class="badge b-amber">◐ Partial — see flag</span>';
  return '<span class="badge b-red">Unverified</span>';
}
function distBadge(d){
  if(d.includes('2 Stars')) return '<span class="badge b-gold">★★ 2 Stars</span>';
  if(d.includes('1 Star')) return '<span class="badge b-gold">★ 1 Star</span>';
  if(d.includes('Bib')) return '<span class="badge b-blue">Bib Gourmand</span>';
  return '<span class="badge b-blue">Selected</span>';
}
async function loadJSON(url){const r=await fetch(url);if(!r.ok)throw new Error(url);return r.json()}

async function renderHotels(){
  const el=document.getElementById('hotels-table'); if(!el) return;
  const data=await loadJSON('data/hotels.json');
  const q=(document.getElementById('q')?.value||'').toLowerCase();
  const sort=document.getElementById('sort')?.value||'rank';
  let rows=data.hotels.filter(h=>!q||JSON.stringify(h).toLowerCase().includes(q));
  if(sort==='rank') rows.sort((a,b)=>a.rank-b.rank);
  if(sort==='michelin') rows.sort((a,b)=>(b.michelin_within_60min_bus||0)-(a.michelin_within_60min_bus||0)||a.rank-b.rank);
  if(sort==='walk') rows.sort((a,b)=>(b.michelin_within_15min_walk||0)-(a.michelin_within_15min_walk||0)||a.rank-b.rank);
  el.innerHTML='<thead><tr><th>#</th><th>Hotel (official)</th><th>Area / Room</th><th>7-night total (2 adults)</th><th>Michelin ≤1 hr (bus/walk)</th><th>Why / Amenities</th><th>Verification</th></tr></thead><tbody>'+
  rows.map(h=>'<tr><td><strong>'+h.rank+'</strong></td><td><a href="'+esc(h.official_url)+'" target="_blank" rel="noopener"><strong>'+esc(h.name)+'</strong></a><br><span class="small">Official site ↗</span>'+(h.flag?'<br><span class="small">⚠ '+esc(h.flag)+'</span>':'')+'</td><td>'+esc(h.area)+'<br><span class="small">'+esc(h.room_example)+'</span></td><td><strong>'+esc(h.seven_night_total)+'</strong><br><span class="small">Resort fee: '+esc(h.resort_fee_per_night)+'<br><a href="'+esc(h.booking_url)+'" target="_blank" rel="noopener">Book / check live total ↗</a></span></td><td><span class="small">On-site: '+esc(h.michelin_on_site)+'</span><br>15-min walk: <strong>'+h.michelin_within_15min_walk+'</strong> · 30-min: <strong>'+h.michelin_within_30min+'</strong> · 60-min bus: <strong>'+h.michelin_within_60min_bus+'</strong>/24</td><td><span class="small">'+esc(h.why)+'<br><br><strong>Amenities:</strong> '+esc(h.amenities)+'</span></td><td>'+badge(h.verified)+'</td></tr>').join('')+'</tbody>';
  document.getElementById('hotels-count').textContent=rows.length+' hotels shown';
}

async function renderRestaurants(){
  const el=document.getElementById('restaurants-table'); if(!el) return;
  const data=await loadJSON('data/restaurants.json');
  const q=(document.getElementById('q')?.value||'').toLowerCase();
  const f=document.getElementById('filter')?.value||'all';
  let rows=data.restaurants.filter(r=>{
    if(f==='starred'&&!r.distinction.includes('Star'))return false;
    if(f==='bib'&&!r.distinction.includes('Bib'))return false;
    if(f==='selected'&&!r.distinction.includes('Selected'))return false;
    if(q&&!JSON.stringify(r).toLowerCase().includes(q))return false;
    return true;
  });
  const order={'2 Stars':0,'1 Star':1,'Bib Gourmand':2,'Selected (Michelin Guide)':3};
  rows.sort((a,b)=>(order[a.distinction]??9)-(order[b.distinction]??9)||a.name.localeCompare(b.name));
  el.innerHTML='<thead><tr><th>Restaurant (official)</th><th>Distinction</th><th>Cost for 2 (food only)</th><th>Days / Hours / Exceptions</th><th>Social</th><th>Verification</th></tr></thead><tbody>'+
  rows.map(r=>'<tr><td><a href="'+esc(r.official_url)+'" target="_blank" rel="noopener"><strong>'+esc(r.name)+'</strong></a><br><span class="small">'+esc(r.cuisine)+' · '+esc(r.location)+'<br><a href="'+esc(r.menu_url)+'" target="_blank" rel="noopener">Official menu ↗</a></span>'+(r.flag?'<br><span class="small">⚠ '+esc(r.flag)+'</span>':'')+'</td><td>'+distBadge(r.distinction)+'<br><span class="small">'+esc(r.distinction)+'</span></td><td><strong>'+esc(r.total_for_2)+'</strong><br><span class="small">'+esc(r.price_per_person)+'</span></td><td><span class="small"><strong>Days:</strong> '+esc(r.days_open)+'<br><strong>Hours:</strong> '+esc(r.hours)+'<br><strong>Exceptions:</strong> '+esc(r.exceptions)+'</span></td><td>'+social(r.name)+'</td><td>'+badge(r.verified)+'</td></tr>').join('')+'</tbody>';
  document.getElementById('restaurants-count').textContent=rows.length+' restaurants shown';
}

async function renderActivities(){
  const el=document.getElementById('activities-table'); if(!el) return;
  const data=await loadJSON('data/activities.json');
  const q=(document.getElementById('q')?.value||'').toLowerCase();
  let rows=data.activities.filter(a=>!q||JSON.stringify(a).toLowerCase().includes(q));
  el.innerHTML='<thead><tr><th>Activity (official)</th><th>Cost for 2</th><th>Days / Hours / Exceptions</th><th>Travel ≤1 hr</th><th>Social</th><th>Verification</th></tr></thead><tbody>'+
  rows.map(a=>'<tr><td><a href="'+esc(a.official_url)+'" target="_blank" rel="noopener"><strong>'+esc(a.name)+'</strong></a><br><span class="small">'+esc(a.category)+' · '+esc(a.location)+'</span>'+(a.flag?'<br><span class="small">⚠ '+esc(a.flag)+'</span>':'')+'</td><td><strong>'+esc(a.cost_for_2)+'</strong></td><td><span class="small"><strong>Days:</strong> '+esc(a.days_open)+'<br><strong>Hours:</strong> '+esc(a.hours)+'<br><strong>Exceptions:</strong> '+esc(a.exceptions)+'</span></td><td><span class="small">'+esc(a.travel_from_center_strip)+'</span></td><td>'+social(a.name)+'</td><td>'+badge(a.verified)+'</td></tr>').join('')+'</tbody>';
  document.getElementById('activities-count').textContent=rows.length+' activities shown';
}

async function renderDates(){
  const el=document.getElementById('dates-table'); if(!el) return;
  const data=await loadJSON('data/dates.json');
  el.innerHTML='<thead><tr><th>Check-in → Check-out (7 nights)</th><th>Events in window</th><th>Demand</th><th>Note</th></tr></thead><tbody>'+
  data.windows.map(w=>{
    let b='<span class="badge b-blue">'+esc(w.demand)+'</span>';
    if(w.demand==='PEAK')b='<span class="badge b-red">PEAK</span>';
    if(w.demand.includes('least-bad'))b='<span class="badge b-green">'+esc(w.demand)+'</span>';
    return '<tr><td><strong>'+esc(w.checkin)+' → '+esc(w.checkout)+'</strong></td><td><span class="small">'+esc(w.events)+'</span></td><td>'+b+'</td><td><span class="small">'+esc(w.note)+'</span></td></tr>';
  }).join('')+'</tbody>';
}

document.addEventListener('DOMContentLoaded',()=>{
  renderHotels();renderRestaurants();renderActivities();renderDates();
  document.getElementById('q')?.addEventListener('input',()=>{renderHotels();renderRestaurants();renderActivities()});
  document.getElementById('sort')?.addEventListener('change',renderHotels);
  document.getElementById('filter')?.addEventListener('change',renderRestaurants);
});
