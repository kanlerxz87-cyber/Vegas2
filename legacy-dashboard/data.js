const restaurants = [
  {name:"L'Atelier de Joël Robuchon Las Vegas",status:"1 MICHELIN Star (2026)",url:"https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/l-atelier-de-joel-robuchon-las-vegas"},
  {name:"Restaurant de Joël Robuchon",status:"2 MICHELIN Stars (2026)",url:"https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/restaurant-de-joel-robuchon"},
  {name:"Restaurant Guy Savoy",status:"1 MICHELIN Star (2026)",url:"https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/guy-savoy-las-vegas"},
  {name:"Stubborn Seed Las Vegas",status:"Listed in 2026 Guide; star not stated on official page",url:"https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/stubborn-seed-las-vegas"},
  {name:"Pho Ga Bac Bac",status:"Listed in 2026 Guide; star not stated on official page",url:"https://guide.michelin.com/us/en/nevada/las-vegas_2935077/restaurant/pho-ga-bac-bac"}
];
document.getElementById('restaurants').innerHTML = restaurants.map(r => `<tr><td><strong>${r.name}</strong></td><td>${r.status}</td><td class="muted">—</td><td class="muted">—</td><td class="muted">—</td><td><a href="${r.url}" target="_blank" rel="noreferrer">MICHELIN Guide ↗</a></td></tr>`).join('');
