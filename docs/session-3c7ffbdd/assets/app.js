/* Client-side progressive enhancement for table filtering */
(function () {
  document.querySelectorAll('.controls[data-filter-target]').forEach(function (bar) {
    var tableId = bar.getAttribute('data-filter-target');
    var table = document.getElementById(tableId);
    if (!table) return;
    var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
    var selects = Array.prototype.slice.call(bar.querySelectorAll('select[data-filter-attr]'));
    var search = bar.querySelector('input[data-filter-search]');

    function applyFilters() {
      var q = search ? search.value.trim().toLowerCase() : '';
      rows.forEach(function (tr) {
        var visible = true;
        selects.forEach(function (sel) {
          var attr = sel.getAttribute('data-filter-attr');
          var val = sel.value;
          if (val !== 'all' && tr.getAttribute('data-' + attr) !== val) {
            visible = false;
          }
        });
        if (visible && q && tr.textContent.toLowerCase().indexOf(q) === -1) {
          visible = false;
        }
        tr.style.display = visible ? '' : 'none';
      });
    }

    selects.forEach(function (sel) { sel.addEventListener('change', applyFilters); });
    if (search) search.addEventListener('input', applyFilters);
  });
})();
