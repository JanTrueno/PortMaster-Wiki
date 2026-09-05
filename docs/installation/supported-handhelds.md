# Supported Handhelds

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

Every device below runs PortMaster on at least one custom firmware.

<div class="filters-container">
  <div class="filters-left">
    <div class="games-search-wrapper">
      <i class="bi bi-search games-search-icon"></i>
      <input type="text" id="handheld-search" class="games-search-input" placeholder="Search devices...">
    </div>
    <div class="view-toggle-wrapper" id="viewToggleWrapper">
      <button class="view-toggle-btn" id="gridViewBtn" title="Grid view" aria-label="Grid view">
        <i class="bi bi-grid-3x3-gap-fill"></i>
      </button>
      <button class="view-toggle-btn active" id="listViewBtn" title="List view" aria-label="List view">
        <i class="bi bi-list-ul"></i>
      </button>
    </div>
    <button class="filter-toggle-btn" id="handheld-filter-toggle" aria-label="Filters">
      <span></span>
      <span></span>
      <span></span>
    </button>
  </div>
  <div class="filters-right">
    <p id="portsCounter">Showing <span id="visible-handheld-count">{{ devices|length }}</span> of {{ devices|length }} devices</p>
  </div>
</div>

<!-- Filter drawer. Uses the same components as the games page filter panel
     (accordion + checkbox list + reset link) rather than the .filter-pill
     class the page used to use, which had no CSS anywhere in the project
     and so rendered as plain running text. -->
<div class="filter-overlay" id="handheld-filter-overlay"></div>
<div class="filter-panel" id="handheld-filter-panel">
  <div class="filter-panel-header">
    <h2>Filters <span class="filter-count-badge" id="handheldFilterCount" style="display:none">(0)</span></h2>
    <div class="filter-panel-header-actions">
      <button type="button" class="filter-reset-link" id="clear-handheld-filters">Reset</button>
      <button class="close-panel-btn" id="close-handheld-panel">&times;</button>
    </div>
  </div>

  <div class="filter-accordion open">
    <div class="filter-accordion-summary" role="button" tabindex="0">
      <span>Manufacturer</span>
      <i class="bi bi-chevron-down accordion-chevron"></i>
    </div>
    <div class="filter-accordion-body">
      <div class="filter-radio-list">
        {% for mfr in manufacturers %}
        <label class="filter-checkbox-item">
          <input type="checkbox" data-filter="manufacturer" value="{{ mfr }}">
          <span>{{ mfr }}</span>
        </label>
        {% endfor %}
      </div>
    </div>
  </div>

  <div class="filter-accordion">
    <div class="filter-accordion-summary" role="button" tabindex="0">
      <span>Custom Firmware</span>
      <i class="bi bi-chevron-down accordion-chevron"></i>
    </div>
    <div class="filter-accordion-body">
      <div class="filter-radio-list">
        {% for cfw in all_cfw %}
        <label class="filter-checkbox-item">
          <input type="checkbox" data-filter="cfw" value="{{ cfw }}">
          <span>{{ cfw }}</span>
        </label>
        {% endfor %}
      </div>
    </div>
  </div>
</div>

<div class="game-grid handhelds-grid list-view" id="handheldsGrid">
{% for device_name, device in devices.items() %}
  <div class="handheld-card"
       data-manufacturer="{{ device.manufacturer }}"
       data-cfw="{{ device.cfw_list|join(',') }}"
       data-search="{{ device.name|lower }} {{ device.manufacturer|lower }} {{ device.cpu|lower }}">

    <div class="handheld-info">
    <h3>{{ device.name.replace(device.manufacturer, '').strip() }}</h3>
    <span class="handheld-brand">{{ device.manufacturer }}</span>

    <div class="handheld-specs">
      <span class="handheld-spec" title="Resolution">
        <i class="bi bi-display"></i>{{ device.resolution }}
      </span>
      <span class="handheld-spec" title="Chipset">
        <i class="bi bi-cpu"></i>{{ device.cpu|upper }}
      </span>
      <span class="handheld-spec" title="Memory">
        <i class="bi bi-memory"></i>{% if device.ram_gb %}{{ device.ram_gb }}GB{% else %}{{ device.ram_mb }}MB{% endif %}
      </span>
      <span class="handheld-spec" title="Analog sticks">
        <i class="bi bi-joystick"></i>{{ device.analogsticks }}
      </span>
    </div>

    <div class="handheld-cfw">
      {% for cfw in device.cfw_list %}
      <span class="cfw-pill">{{ cfw }}</span>
      {% endfor %}
    </div>
    </div>
  </div>
{% endfor %}
</div>

<div id="no-results" class="no-results" style="display: none;">
  <p>No devices found matching your filters.</p>
  <button class="clear-all-filters-btn" onclick="document.getElementById('clear-handheld-filters').click()">
    <i class="bi bi-arrow-counterclockwise"></i> Clear Filters
  </button>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  // .filter-panel positions its top from --md-header-actual-height, which the
  // games page measures at runtime. Without it the drawer falls back to 3rem
  // and rides up over the real (taller) header.
  function updateHeaderHeightVar() {
    const header = document.querySelector('.md-header');
    if (!header) return;
    document.documentElement.style.setProperty('--md-header-actual-height', `${header.getBoundingClientRect().height}px`);
  }
  updateHeaderHeightVar();
  window.addEventListener('resize', updateHeaderHeightVar);

  const searchBar = document.getElementById('handheld-search');
  const filterToggle = document.getElementById('handheld-filter-toggle');
  const filterPanel = document.getElementById('handheld-filter-panel');
  const filterOverlay = document.getElementById('handheld-filter-overlay');
  const closePanel = document.getElementById('close-handheld-panel');
  const clearFilters = document.getElementById('clear-handheld-filters');
  const cards = document.querySelectorAll('.handheld-card');
  const visibleCount = document.getElementById('visible-handheld-count');
  const noResults = document.getElementById('no-results');
  const filterInputs = document.querySelectorAll('#handheld-filter-panel input[type="checkbox"]');
  const filterCount = document.getElementById('handheldFilterCount');

  let activeFilters = {
    manufacturer: new Set(),
    cfw: new Set()
  };

  // Toggle filter panel
  filterToggle.addEventListener('click', function() {
    filterPanel.classList.toggle('open');
    filterOverlay.classList.toggle('active');
    filterToggle.classList.toggle('active');
  });

  closePanel.addEventListener('click', function() {
    filterPanel.classList.remove('open');
    filterOverlay.classList.remove('active');
    filterToggle.classList.remove('active');
  });

  filterOverlay.addEventListener('click', function() {
    filterPanel.classList.remove('open');
    filterOverlay.classList.remove('active');
    filterToggle.classList.remove('active');
  });

  // Accordion open/close, same interaction as the games panel
  document.querySelectorAll('#handheld-filter-panel .filter-accordion-summary').forEach(sum => {
    const toggle = () => sum.parentElement.classList.toggle('open');
    sum.addEventListener('click', toggle);
    sum.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });

  filterInputs.forEach(input => {
    input.addEventListener('change', function() {
      const type = this.dataset.filter;
      const value = this.value.toLowerCase();
      if (this.checked) {
        activeFilters[type].add(value);
      } else {
        activeFilters[type].delete(value);
      }
      applyFilters();
    });
  });

  // Grid / list toggle, mirroring the games page. List is the default here
  // because these rows are specs, which read better as aligned columns.
  const grid = document.getElementById('handheldsGrid');
  const gridBtn = document.getElementById('gridViewBtn');
  const listBtn = document.getElementById('listViewBtn');

  function setView(view) {
    const isList = view === 'list';
    grid.classList.toggle('list-view', isList);
    listBtn.classList.toggle('active', isList);
    gridBtn.classList.toggle('active', !isList);
    try { localStorage.setItem('pm-handhelds-view', view); } catch (e) {}
  }

  gridBtn.addEventListener('click', () => setView('grid'));
  listBtn.addEventListener('click', () => setView('list'));

  try {
    const saved = localStorage.getItem('pm-handhelds-view');
    if (saved === 'grid') setView('grid');
  } catch (e) {}

  searchBar.addEventListener('input', applyFilters);

  clearFilters.addEventListener('click', function() {
    activeFilters.manufacturer.clear();
    activeFilters.cfw.clear();
    searchBar.value = '';

    filterInputs.forEach(input => { input.checked = false; });
    applyFilters();
  });

  function applyFilters() {
    const searchTerm = searchBar.value.toLowerCase();
    let visibleCards = 0;

    cards.forEach(card => {
      const manufacturer = card.dataset.manufacturer.toLowerCase();
      const cfwList = card.dataset.cfw.toLowerCase().split(',');
      const searchText = card.dataset.search;

      const matchesManufacturer = activeFilters.manufacturer.size === 0 ||
                                   activeFilters.manufacturer.has(manufacturer);

      const matchesCFW = activeFilters.cfw.size === 0 ||
                         cfwList.some(cfw => activeFilters.cfw.has(cfw.trim()));

      const matchesSearch = !searchTerm || searchText.includes(searchTerm);

      if (matchesManufacturer && matchesCFW && matchesSearch) {
        card.style.display = '';
        visibleCards++;
      } else {
        card.style.display = 'none';
      }
    });

    visibleCount.textContent = visibleCards;
    noResults.style.display = visibleCards === 0 ? 'block' : 'none';

    const active = activeFilters.manufacturer.size + activeFilters.cfw.size;
    filterCount.textContent = `(${active})`;
    filterCount.style.display = active ? '' : 'none';
  }
});
</script>
