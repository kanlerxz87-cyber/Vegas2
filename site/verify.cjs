const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

global.window = {};
require(path.join(__dirname, 'assets', 'data.js'));
const data = global.window.TRIP;
const problems = [];
const requireCheck = (condition, message) => { if (!condition) problems.push(message); };
const isOfficialHttps = (url) => typeof url === 'string' && url.startsWith('https://');

requireCheck(data && data.meta && data.restaurants && data.hotels && data.activities, 'Trip data did not load.');
requireCheck(data.restaurants.length === 24, `Expected 24 restaurants, found ${data.restaurants.length}.`);
requireCheck(data.hotels.length === 5, `Expected 5 hotel candidates, found ${data.hotels.length}.`);
requireCheck(data.activities.length >= 7, `Expected at least 7 activity/transit rows, found ${data.activities.length}.`);

const starCount = data.restaurants.filter((item) => item.distinction.includes('Star')).length;
const bibCount = data.restaurants.filter((item) => item.distinction.includes('Bib')).length;
const otherCount = data.restaurants.length - starCount - bibCount;
requireCheck(starCount === 4, `Expected 4 starred restaurants, found ${starCount}.`);
requireCheck(bibCount === 3, `Expected 3 Bib Gourmand restaurants, found ${bibCount}.`);
requireCheck(otherCount === 17, `Expected 17 Recommended/Selected restaurants, found ${otherCount}.`);

for (const restaurant of data.restaurants) {
  requireCheck(isOfficialHttps(restaurant.officialUrl), `${restaurant.name}: missing HTTPS official venue source.`);
  requireCheck(Boolean(restaurant.distinction), `${restaurant.name}: missing MICHELIN distinction.`);
  requireCheck(typeof restaurant.hours === 'string', `${restaurant.name}: missing hours field (blank is allowed).`);
  requireCheck(Boolean(restaurant.exceptions), `${restaurant.name}: missing exception / verification note.`);
  if (restaurant.menuUrl) requireCheck(isOfficialHttps(restaurant.menuUrl), `${restaurant.name}: menu URL is not HTTPS.`);
  if (restaurant.socialUrl) requireCheck(isOfficialHttps(restaurant.socialUrl), `${restaurant.name}: social URL is not HTTPS.`);
}
for (const hotel of data.hotels) {
  requireCheck(isOfficialHttps(hotel.sourceUrl), `${hotel.name}: missing HTTPS official room source.`);
  requireCheck(isOfficialHttps(hotel.bookingUrl), `${hotel.name}: missing official room/rate link.`);
  requireCheck(/king|queen/i.test(hotel.bed), `${hotel.name}: bed size not stated.`);
  requireCheck(/private|bathroom/i.test(hotel.bath), `${hotel.name}: bathroom evidence not stated.`);
  requireCheck(typeof hotel.total === 'string', `${hotel.name}: seven-night total field missing; use blank if unverified.`);
  requireCheck(Boolean(hotel.transitNote), `${hotel.name}: transit verification status missing.`);
}
for (const activity of data.activities) {
  requireCheck(isOfficialHttps(activity.officialUrl), `${activity.name}: missing HTTPS official source.`);
  requireCheck(typeof activity.hours === 'string', `${activity.name}: missing hours field (blank is allowed).`);
  requireCheck(Boolean(activity.exceptions), `${activity.name}: missing exception note.`);
}
for (const issue of data.flags) {
  requireCheck(Boolean(issue.title && issue.issue && issue.next), 'Flagged issue missing title, explanation, or verification step.');
  if (issue.sourceUrl) requireCheck(isOfficialHttps(issue.sourceUrl), `${issue.title}: source URL is not HTTPS.`);
}

const pages = ['index.html', 'hotels.html', 'restaurants.html', 'activities.html', 'analysis.html', 'flagged.html'];
for (const page of pages) {
  const pagePath = path.join(__dirname, page);
  requireCheck(fs.existsSync(pagePath), `Missing page: ${page}`);
  if (!fs.existsSync(pagePath)) continue;
  const html = fs.readFileSync(pagePath, 'utf8');
  requireCheck(html.includes('assets/styles.css'), `${page}: missing stylesheet reference.`);
  requireCheck(html.includes('assets/data.js') && html.includes('assets/app.js'), `${page}: missing application scripts.`);
  requireCheck(html.includes('<main id="main"'), `${page}: missing main landmark.`);
}
const publishedPath = path.join(__dirname, '..', 'docs', 'session-d33551df');
for (const page of pages) {
  const publishedPage = path.join(publishedPath, page);
  requireCheck(fs.existsSync(publishedPage), `Published Pages copy is missing ${page}.`);
  if (fs.existsSync(publishedPage)) {
    const html = fs.readFileSync(publishedPage, 'utf8');
    requireCheck(html.includes('assets/styles.css') && html.includes('assets/data.js') && html.includes('assets/app.js'), `Published ${page}: missing local assets.`);
  }
}
for (const asset of ['styles.css', 'data.js', 'app.js']) {
  requireCheck(fs.existsSync(path.join(publishedPath, 'assets', asset)), `Published Pages copy is missing asset ${asset}.`);
}

const appSource = fs.readFileSync(path.join(__dirname, 'assets', 'app.js'), 'utf8');
const expectedRendered = {
  home: ['Las Vegas, planned with receipts.', 'Executive summary'],
  hotels: ['Hotel shortlist', 'Caesars Palace'],
  restaurants: ['MICHELIN-recognized restaurants', 'Joël Robuchon', 'Wing Lei'],
  activities: ['Activities', 'High Roller Observation Wheel'],
  analysis: ['Analysis', 'Questions'],
  flagged: ['Flagged for Review', 'Caesars Palace seven-night total is not reconciled']
};
for (const [page, markers] of Object.entries(expectedRendered)) {
  const elements = new Map();
  const getElementById = (id) => {
    if (!elements.has(id)) elements.set(id, { innerHTML: '', addEventListener() {}, querySelectorAll() { return []; } });
    return elements.get(id);
  };
  const context = {
    window: { TRIP: data, location: { href: 'https://example.test/' } },
    document: { body: { dataset: { page } }, getElementById },
    URL,
    console
  };
  try {
    vm.runInNewContext(appSource, context, { filename: 'assets/app.js' });
    const output = getElementById('main').innerHTML;
    for (const marker of markers) requireCheck(output.includes(marker), `${page}: rendered output missing “${marker}”.`);
    const tableBodies = output.split('<tbody>').slice(1).map((part) => part.split('</tbody>')[0]);
    for (const body of tableBodies) {
      const rows = body.split('<tr>').slice(1).map((part) => part.split('</tr>')[0]);
      for (const row of rows) requireCheck(row.includes('href="https://'), `${page}: a rendered findings-table row lacks an official source link.`);
    }
    const hrefs = [...output.matchAll(/href="([^"]+)"/g)].map((match) => match[1]);
    for (const href of hrefs) {
      if (/^(https?:|mailto:|tel:|#)/i.test(href)) continue;
      const localPath = href.split(/[?#]/)[0];
      const targetPath = path.resolve(__dirname, localPath || `${page}.html`);
      requireCheck(targetPath.startsWith(`${__dirname}${path.sep}`) && fs.existsSync(targetPath), `${page}: broken or unsafe local link: ${href}`);
    }
  } catch (error) {
    problems.push(`${page}: render smoke test threw ${error.message}`);
  }
}

const exactHotel = data.hotels.find((hotel) => hotel.id === 'caesars');
requireCheck(exactHotel && exactHotel.rate.includes('$201/night') && exactHotel.rate.includes('$226/night'), 'Caesars current and earlier dated nightly displays must be recorded.');
requireCheck(exactHotel && exactHotel.total === '', 'Unreconciled Caesars seven-night total must remain blank.');
requireCheck(exactHotel && exactHotel.totalNote.includes('$1,580') && exactHotel.totalNote.includes('$1,582'), 'Caesars discrepancy must remain explicit.');
requireCheck(data.hotels.every((hotel) => hotel.transitCount === ''), 'Transit counts should remain blank until route matrix is verified.');

if (problems.length) {
  console.error(`Site verification failed (${problems.length} issue${problems.length === 1 ? '' : 's'}):`);
  for (const problem of problems) console.error(`- ${problem}`);
  process.exit(1);
}
console.log(`Site data verified: ${data.hotels.length} hotels, ${data.restaurants.length} restaurants (${starCount} starred / ${bibCount} Bib / ${otherCount} Selected), ${data.activities.length} activity/transit rows, ${data.flags.length} review flags; all findings table rows have source links.`);
