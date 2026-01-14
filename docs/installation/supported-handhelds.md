# Supported Handhelds

<div class="filters-container">
  <div class="search-wrapper">
    <input type="text" id="handheld-search" class="search-bar" placeholder="Search devices...">
    <button class="filter-toggle-btn" id="handheld-filter-toggle">
      <span></span>
      <span></span>
      <span></span>
    </button>
  </div>
</div>

<!-- Filter Panel (Sidebar) -->
<div class="filter-overlay" id="handheld-filter-overlay"></div>
<div class="filter-panel" id="handheld-filter-panel">
  <div class="filter-panel-header">
    <h2>Filters</h2>
    <button class="close-panel-btn" id="close-handheld-panel">&times;</button>
  </div>
  
  <div class="filter-section">
    <h3>Manufacturer</h3>
    <div class="filter-pills" id="manufacturer-filters">
      {% for mfr in manufacturers %}
      <span class="filter-pill" data-filter="manufacturer" data-value="{{ mfr }}">{{ mfr }}</span>
      {% endfor %}
    </div>
  </div>
  
  <div class="filter-section">
    <h3>Custom Firmware</h3>
    <div class="filter-pills" id="cfw-filters">
      {% for cfw in all_cfw %}
      <span class="filter-pill" data-filter="cfw" data-value="{{ cfw }}">{{ cfw }}</span>
      {% endfor %}
    </div>
  </div>
  
  <button class="clear-all-filters-btn" id="clear-handheld-filters">
    <i class="fa-solid fa-rotate-left"></i> Clear All Filters
  </button>
</div>

<div id="portsCounter">
  Showing <span id="visible-handheld-count">{{ devices|length }}</span> of {{ devices|length }} devices
</div>

<div class="handhelds-grid">
{% for device_name, device in devices.items() %}
  <div class="handheld-card" 
       data-manufacturer="{{ device.manufacturer }}" 
       data-cfw="{{ device.cfw_list|join(',') }}"
       data-search="{{ device.name|lower }} {{ device.manufacturer|lower }}">
    
    <div class="handheld-header">
      <h3 class="handheld-name">{{ device.name.replace(device.manufacturer, '').strip() }}</h3>
      <span class="handheld-brand">{{ device.manufacturer }}</span>
    </div>
    
    <div class="handheld-specs">
      <div class="spec-row">
        <i class="fa-solid fa-display"></i>
        <span>{{ device.resolution }}</span>
      </div>
      <div class="spec-row">
        <i class="fa-solid fa-microchip"></i>
        <span>{{ device.cpu|upper }}</span>
      </div>
      <div class="spec-row">
        <i class="fa-solid fa-memory"></i>
        <span>{% if device.ram_gb %}{{ device.ram_gb }}GB{% else %}{{ device.ram_mb }}MB{% endif %}</span>
      </div>
      <div class="spec-row">
        <i class="fa-solid fa-gamepad"></i>
        <span>{{ device.analogsticks }} sticks</span>
      </div>
    </div>
    
    <div class="handheld-cfw">
      {% for cfw in device.cfw_list %}
      <span class="cfw-pill">{{ cfw }}</span>
      {% endfor %}
    </div>
  </div>
{% endfor %}
</div>

<div id="no-results" class="no-results" style="display: none;">
  <p>No devices found matching your filters.</p>
  <button class="clear-all-filters-btn" onclick="document.getElementById('clear-handheld-filters').click()">
    <i class="fa-solid fa-rotate-left"></i> Clear Filters
  </button>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchBar = document.getElementById('handheld-search');
  const filterToggle = document.getElementById('handheld-filter-toggle');
  const filterPanel = document.getElementById('handheld-filter-panel');
  const filterOverlay = document.getElementById('handheld-filter-overlay');
  const closePanel = document.getElementById('close-handheld-panel');
  const clearFilters = document.getElementById('clear-handheld-filters');
  const cards = document.querySelectorAll('.handheld-card');
  const visibleCount = document.getElementById('visible-handheld-count');
  const noResults = document.getElementById('no-results');
  const filterPills = document.querySelectorAll('.filter-pill');
  
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
  
  // Filter pill toggle
  filterPills.forEach(pill => {
    pill.addEventListener('click', function() {
      const filterType = this.dataset.filter;
      const value = this.dataset.value.toLowerCase();
      
      if (activeFilters[filterType].has(value)) {
        activeFilters[filterType].delete(value);
        this.classList.remove('selected');
      } else {
        activeFilters[filterType].add(value);
        this.classList.add('selected');
      }
      
      applyFilters();
    });
  });
  
  // Search
  searchBar.addEventListener('input', function() {
    applyFilters();
  });
  
  // Clear all filters
  clearFilters.addEventListener('click', function() {
    activeFilters.manufacturer.clear();
    activeFilters.cfw.clear();
    searchBar.value = '';
    
    filterPills.forEach(pill => pill.classList.remove('selected'));
    applyFilters();
  });
  
  // Apply filters
  function applyFilters() {
    const searchTerm = searchBar.value.toLowerCase();
    let visibleCards = 0;
    
    cards.forEach(card => {
      const manufacturer = card.dataset.manufacturer.toLowerCase();
      const cfwList = card.dataset.cfw.toLowerCase().split(',');
      const searchText = card.dataset.search;
      
      // Check manufacturer filter
      const matchesManufacturer = activeFilters.manufacturer.size === 0 || 
                                   activeFilters.manufacturer.has(manufacturer);
      
      // Check CFW filter (device must have at least one selected CFW)
      const matchesCFW = activeFilters.cfw.size === 0 || 
                         cfwList.some(cfw => activeFilters.cfw.has(cfw.trim()));
      
      // Check search
      const matchesSearch = !searchTerm || searchText.includes(searchTerm);
      
      if (matchesManufacturer && matchesCFW && matchesSearch) {
        card.style.display = '';
        visibleCards++;
      } else {
        card.style.display = 'none';
      }
    });
    
    visibleCount.textContent = visibleCards;
    
    if (visibleCards === 0) {
      noResults.style.display = 'block';
    } else {
      noResults.style.display = 'none';
    }
  }
});
</script>