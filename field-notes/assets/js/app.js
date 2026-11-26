(() => {
  'use strict';

  const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[character]);

  const externalLink = (url, label, className = '') => {
    if (!url) return '';
    return `<a${className ? ` class="${escapeHtml(className)}"` : ''} href="${escapeHtml(url)}">${escapeHtml(label)}</a>`;
  };

  const navToggle = document.querySelector('.nav-toggle');
  const siteNav = document.querySelector('#primary-nav');
  if (navToggle && siteNav) {
    navToggle.addEventListener('click', () => {
      const expanded = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!expanded));
      siteNav.classList.toggle('is-open', !expanded);
    });
  }

  const renderRestaurants = async () => {
    const grid = document.querySelector('#restaurants-grid');
    if (!grid) return;
    const count = document.querySelector('#restaurant-count');
    const search = document.querySelector('#restaurant-search');
    const awardFilter = document.querySelector('#award-filter');
    const areaFilter = document.querySelector('#area-filter');
    const status = document.querySelector('#restaurant-status');
    try {
      const response = await fetch('data/restaurants.json');
      if (!response.ok) throw new Error('Could not load the restaurant research file.');
      const data = await response.json();
      const guideNote = document.querySelector('#guide-note');
      if (guideNote) guideNote.textContent = data.guideNote;

      grid.innerHTML = data.restaurants.map((restaurant) => {
        const badgeClass = restaurant.awardType === 'starred' ? 'badge--star' : restaurant.awardType === 'bib' ? 'badge--bib' : 'badge--recommended';
        const statusLine = restaurant.status ? `<p class="status-line">${escapeHtml(restaurant.status)}</p>` : '';
        const price = restaurant.price || 'No verified two-person meal total captured.';
        const priceNote = restaurant.priceNote ? `<p class="small-note">${escapeHtml(restaurant.priceNote)}</p>` : '';
        const hours = restaurant.hours || 'Not confirmed in this research snapshot.';
        const menuLink = restaurant.menu ? externalLink(restaurant.menu, 'Official menu') : '';
        const reservationLink = restaurant.reservation ? externalLink(restaurant.reservation, 'Venue / reservation page') : '';
        return `<article class="restaurant-card" data-award="${escapeHtml(restaurant.awardType)}" data-area="${escapeHtml(restaurant.area)}" data-search="${escapeHtml(`${restaurant.name} ${restaurant.cuisine} ${restaurant.area} ${restaurant.award}`.toLowerCase())}">
          <span class="badge ${badgeClass}">${escapeHtml(restaurant.award)}</span>
          <h3>${escapeHtml(restaurant.name)}</h3>
          <p class="card-deck">${escapeHtml(restaurant.cuisine)} · ${escapeHtml(restaurant.area)}</p>
          ${statusLine}
          <div class="card-copy"><p>${escapeHtml(restaurant.description)}</p></div>
          <ul class="card-facts">
            <li><strong>Hours</strong>${escapeHtml(hours)}</li>
            <li><strong>Published price signal</strong>${escapeHtml(price)}${priceNote}</li>
          </ul>
          <div class="card-actions">${externalLink(restaurant.source, restaurant.sourceLabel || 'Official venue source')}${menuLink}${reservationLink}</div>
        </article>`;
      }).join('');
      grid.setAttribute('aria-busy', 'false');

      const cards = Array.from(grid.querySelectorAll('.restaurant-card'));
      const applyFilters = () => {
        const needle = search.value.trim().toLowerCase();
        const award = awardFilter.value;
        const area = areaFilter.value;
        let visible = 0;
        for (const card of cards) {
          const searchMatches = !needle || card.dataset.search.includes(needle);
          const awardMatches = award === 'all' || card.dataset.award === award;
          const areaMatches = area === 'all' || card.dataset.area === area;
          const show = searchMatches && awardMatches && areaMatches;
          card.hidden = !show;
          if (show) visible += 1;
        }
        count.textContent = `${visible} of ${cards.length} restaurants shown`;
        status.textContent = visible ? '' : 'No restaurants match those filters. Try a broader search.';
      };
      [search, awardFilter, areaFilter].forEach((control) => control.addEventListener(control === search ? 'input' : 'change', applyFilters));
      applyFilters();
    } catch (error) {
      grid.innerHTML = '<p class="callout callout--warn">Restaurant details could not be loaded. Please refresh, or see the checked-source and review notes below.</p>';
      grid.setAttribute('aria-busy', 'false');
      if (status) status.textContent = error.message;
    }
  };

  const renderHotels = async () => {
    const grid = document.querySelector('#hotel-grid');
    if (!grid) return;
    const buttons = Array.from(document.querySelectorAll('[data-rate-scenario]'));
    const heading = document.querySelector('#hotel-scenario-heading');
    const note = document.querySelector('#hotel-scenario-note');
    const status = document.querySelector('#hotel-status');
    try {
      const response = await fetch('data/hotels.json');
      if (!response.ok) throw new Error('Could not load the hotel-rate research file.');
      const data = await response.json();
      const renderScenario = (scenarioKey) => {
        const scenario = data.scenarios[scenarioKey];
        if (!scenario) return;
        heading.textContent = `${scenario.label} · ${scenario.dates}`;
        note.textContent = scenario.note;
        grid.innerHTML = scenario.hotels.map((hotel) => {
          const rateItems = hotel.rates.map((rate) => {
            const statusBadge = rate.status ? `<span class="badge badge--warning">${escapeHtml(rate.status)}</span>` : '';
            return `<div class="rate-option">
              <strong>${escapeHtml(rate.room)}</strong>
              ${statusBadge}
              <div class="rate-price"><b>${escapeHtml(rate.nightly)}</b><span>${escapeHtml(rate.total)}</span></div>
              <p>${escapeHtml(rate.basis)}</p>
            </div>`;
          }).join('');
          return `<article class="hotel-card">
            <div><span class="badge">${escapeHtml(hotel.area)}</span></div>
            <h3>${escapeHtml(hotel.name)}</h3>
            <p class="card-copy">${escapeHtml(hotel.profile)}</p>
            <div class="rate-list">${rateItems}</div>
            <div class="hotel-links">${externalLink(hotel.roomLink, 'Room details')}${externalLink(hotel.bookingLink, 'Open live date search')}</div>
          </article>`;
        }).join('');
        grid.setAttribute('aria-busy', 'false');
        buttons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.rateScenario === scenarioKey)));
        status.textContent = `${scenario.hotels.length} hotel quotes shown. Snapshot checked ${data.asOf}; booking sites may now show different prices.`;
      };
      buttons.forEach((button) => button.addEventListener('click', () => renderScenario(button.dataset.rateScenario)));
      renderScenario('threeNight');
    } catch (error) {
      grid.innerHTML = '<p class="callout callout--warn">Hotel details could not be loaded. Please refresh, or use the official booking links listed in the page notes.</p>';
      grid.setAttribute('aria-busy', 'false');
      if (status) status.textContent = error.message;
    }
  };

  const renderExperiences = async () => {
    const grid = document.querySelector('#experience-grid');
    if (!grid) return;
    const status = document.querySelector('#experience-status');
    try {
      const response = await fetch('data/experiences.json');
      if (!response.ok) throw new Error('Could not load the experience research file.');
      const data = await response.json();
      grid.innerHTML = data.experiences.map((experience) => `<article class="experience-card">
        <span class="badge">${escapeHtml(experience.category)}</span>
        <h3>${escapeHtml(experience.name)}</h3>
        <p class="card-deck">${escapeHtml(experience.area)}</p>
        <div class="card-copy"><p>${escapeHtml(experience.summary)}</p></div>
        <ul class="card-facts">
          <li><strong>Hours / timing</strong>${escapeHtml(experience.hours)}</li>
          <li><strong>Published price</strong>${escapeHtml(experience.price)}</li>
          <li><strong>For two</strong>${escapeHtml(experience.forTwo)}</li>
        </ul>
        <p class="small-note">${escapeHtml(experience.note)}</p>
        <div class="card-actions">${externalLink(experience.source, experience.sourceLabel)}${externalLink(experience.booking, 'Check live details / tickets')}</div>
      </article>`).join('');
      grid.setAttribute('aria-busy', 'false');
      status.textContent = `${data.experiences.length} experiences shown. Prices and event calendars were checked ${data.asOf}.`;
    } catch (error) {
      grid.innerHTML = '<p class="callout callout--warn">Experience details could not be loaded. Please refresh, or open the official links from this page.</p>';
      grid.setAttribute('aria-busy', 'false');
      if (status) status.textContent = error.message;
    }
  };

  const setupRoutePlanner = () => {
    const form = document.querySelector('#route-form');
    const result = document.querySelector('#route-result');
    const link = document.querySelector('#route-link');
    if (!form || !result || !link) return;
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const origin = document.querySelector('#route-origin').value.trim();
      const destination = document.querySelector('#route-destination').value.trim();
      const mode = document.querySelector('#route-mode').value;
      const url = new URL('https://www.google.com/maps/dir/');
      url.searchParams.set('api', '1');
      url.searchParams.set('origin', origin);
      url.searchParams.set('destination', destination);
      url.searchParams.set('travelmode', mode);
      link.href = url.toString();
      link.textContent = `Open ${mode === 'transit' ? 'transit' : mode} directions from ${origin} to ${destination}`;
      result.hidden = false;
      link.focus();
    });
  };

  const page = document.body.dataset.page;
  if (page === 'restaurants') renderRestaurants();
  if (page === 'hotels') renderHotels();
  if (page === 'experiences') renderExperiences();
  if (page === 'getting-around') setupRoutePlanner();
})();
