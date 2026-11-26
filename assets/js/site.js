(() => {
  const input = document.querySelector("#restaurant-search");
  const cards = [...document.querySelectorAll("[data-restaurant-card]")];
  const filterButtons = [...document.querySelectorAll("[data-restaurant-filter]")];
  const count = document.querySelector("#restaurant-result-count");
  if (!input || !cards.length || !filterButtons.length) return;

  let activeFilter = "all";
  const normalize = (value) => value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();

  function applyFilters() {
    const query = normalize(input.value.trim());
    let visible = 0;
    for (const card of cards) {
      const textMatches = !query || normalize(card.textContent).includes(query);
      const status = card.dataset.michelin || "other";
      const statusMatches = activeFilter === "all"
        || (activeFilter === "stars" && status === "star")
        || (activeFilter === "bib" && status === "bib")
        || (activeFilter === "listed" && status === "listed");
      const show = textMatches && statusMatches;
      card.hidden = !show;
      if (show) visible += 1;
    }
    if (count) count.textContent = `${visible} of ${cards.length} restaurants shown`;
  }

  input.addEventListener("input", applyFilters);
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.restaurantFilter;
      filterButtons.forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
      applyFilters();
    });
  });
  applyFilters();
})();
