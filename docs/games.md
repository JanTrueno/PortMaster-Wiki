---
hide:
  - navigation
  - toc

search:
  exclude: true
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.1.0/dist/fuse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<div class="filters-container">
  <div class="search-wrapper">
    <input type="text" id="searchInput" placeholder="Search ports..." class="search-bar">
    
    <!-- Sort Dropdown -->
    <div class="sort-dropdown-wrapper">
      <button class="sort-toggle-btn" id="sortToggleBtn">
        <i class="bi bi-sort-down"></i>
      </button>
      <div class="sort-dropdown" id="sortDropdown">
        <div class="sort-option" data-sort="az">A-Z</div>
        <div class="sort-option" data-sort="za">Z-A</div>
        <div class="sort-option" data-sort="downloads">Most Downloads</div>
        <div class="sort-option selected" data-sort="date-added">Date Added (Newest)</div>
        <div class="sort-option" data-sort="date-updated">Date Updated (Newest)</div>
      </div>
    </div>
    
    <button class="filter-toggle-btn" id="filterToggleBtn">
      <span></span>
      <span></span>
      <span></span>
    </button>
  </div>
  <p id="portsCounter">Showing: {{ total_port_count }} ports</p>
</div>

<!-- Filter Overlay -->
<div class="filter-overlay" id="filterOverlay"></div>

<!-- Back to Top Button -->
<button class="back-to-top" id="backToTop">
  <i class="bi bi-arrow-up"></i>
</button>

<!-- Filter Panel -->
<div class="filter-panel" id="filterPanel">
  <div class="filter-panel-header">
    <h2>Filters</h2>
    <button class="close-panel-btn" id="closePanelBtn">&times;</button>
  </div>

  <div class="filter-group">
    <label for="deviceSelect">Device</label>
    <select id="deviceSelect" class="filter-dropdown">
      <option value="">Select your device...</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="osSelect">Operating System</label>
    <select id="osSelect" class="filter-dropdown" disabled>
      <option value="">Select OS...</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="genreSelect">Genre</label>
    <select id="genreSelect" class="filter-dropdown">
      <option value="">All Genres</option>
    </select>
  </div>

  <div class="filter-group">
    <label>Options</label>
    <div class="toggle-group">
      <div class="toggle-item">
        <span>Ready to Run Only</span>
        <label class="toggle-switch">
          <input type="checkbox" id="readyToggle">
          <span class="toggle-slider"></span>
        </label>
      </div>
      <div class="toggle-item">
        <span>Hide Incompatible</span>
        <label class="toggle-switch">
          <input type="checkbox" id="hideIncompatibleToggle">
          <span class="toggle-slider"></span>
        </label>
      </div>
    </div>
  </div>

  <button class="clear-all-filters-btn" onclick="clearAllFilters()">
    <i class="bi bi-x-circle"></i> Clear All Filters
  </button>

  <div class="filter-group advanced-filters">
    <label class="advanced-label" onclick="toggleAdvancedFilters()">
      Advanced <i class="bi bi-chevron-down" id="advancedArrow"></i>
    </label>
    <div class="advanced-filters-content" id="advancedFiltersContent">
      <div class="filter-subgroup">
        <label>Runtime</label>
        <div class="filter-pills" id="runtimePills"></div>
      </div>

      <div class="filter-subgroup">
        <label>Architecture</label>
        <div class="filter-pills" id="archPills"></div>
      </div>

      <div class="filter-subgroup">
        <label>Requirements</label>
        <div class="filter-pills" id="reqPills"></div>
      </div>

      <button class="clear-filters-btn" onclick="clearAdvancedFilters()">
        <i class="bi bi-x-circle"></i> Clear All
      </button>
    </div>
  </div>
</div>

<!-- Single Reusable Modal -->
<div id="portModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="closeModal()">&times;</span>

    <div class="modal-header-section">
      <h1 class="modal-main-title" id="modal-title"></h1>
      
      <div class="modal-screenshot-container" id="modal-screenshot-container">
        <img src="" alt="" class="modal-screenshot" id="modal-screenshot">
      </div>

      <div class="modal-description">
        <div class="desc-md" id="modal-desc"></div>
      </div>

      <div class="modal-button-container">
        <div class="download-warning" id="downloadWarning" style="display: none;">
          <i class="bi bi-exclamation-triangle"></i>
          <span>No device selected. This port may not be compatible with your device.</span>
        </div>
        <div class="download-actions">
          <a href="#" class="modal-download-btn" id="modal-download-btn" onclick="handleDownload(event)">
            Download
          </a>
          <button class="device-filter-btn" onclick="openDeviceFilter(event)" title="Change device">
            <i class="bi bi-controller"></i>
          </button>
          <button class="share-btn" id="modal-share-btn" onclick="sharePort(event)" title="Share port">
            <i class="bi bi-share"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="modal-details-section">
      <h2 class="modal-section-title">Port Details</h2>
      
      <div class="modal-info-grid">
        <div class="info-item">
          <i class="info-icon bi bi-dpad"></i>
          <div class="info-content">
            <h3 class="info-heading">Genres</h3>
            <div class="info-value" id="modal-genres">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-card-checklist"></i>
          <div class="info-content">
            <h3 class="info-heading">Requirements</h3>
            <div class="info-value" id="modal-reqs">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-person-workspace"></i>
          <div class="info-content">
            <h3 class="info-heading">Porter</h3>
            <div class="info-value" id="modal-porter">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-download"></i>
          <div class="info-content">
            <h3 class="info-heading">Downloads</h3>
            <div class="info-value" id="modal-downloads">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-cpu"></i>
          <div class="info-content">
            <h3 class="info-heading">Runtimes</h3>
            <div class="info-value" id="modal-runtimes">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-motherboard"></i>
          <div class="info-content">
            <h3 class="info-heading">Architecture</h3>
            <div class="info-value" id="modal-arch">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-calendar-plus"></i>
          <div class="info-content">
            <h3 class="info-heading">Date Added</h3>
            <div class="info-value" id="modal-date-added">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-calendar-check"></i>
          <div class="info-content">
            <h3 class="info-heading">Last Updated</h3>
            <div class="info-value" id="modal-date-updated">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-boxes"></i>
          <div class="info-content">
            <h3 class="info-heading">Miscellaneous</h3>
            <div class="info-value" id="modal-misc">—</div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal-text-section" id="modal-inst-section" style="display: none;">
      <h2 class="modal-section-title">Instructions</h2>
      <div class="modal-text-content" id="modal-inst"></div>
    </div>

    <div class="modal-text-section">
      <h2 class="modal-section-title">Additional Information</h2>
      <div class="modal-text-content" id="modal-readme">
        <div class="loading-spinner">Loading...</div>
      </div>
    </div>
  </div>
</div>

<div class="game-grid">

{% for key in sorted_orders["date-added"] %}
  {% set port = ports.ports[key] %}
  {% set is_mv = port.source and port.source.url and ('PortMaster-MV' in port.source.url or 'MV-New' in port.source.url) %}
  {% set repo_owner = 'PortsMaster-MV' if is_mv else 'PortsMaster' %}
  {% set repo_name = 'PortMaster-MV-New' if is_mv else 'PortMaster-New' %}
  {% set port_id = key | replace('.zip','') %}
  {% set download_count = port_stats.ports[key] | default(0) %}
  
  {% set runtime_arch_list = [] %}
  {% if port.attr and port.attr.runtime %}
    {% for rt in port.attr.runtime %}
      {% if runtime_archs[rt] is defined %}
        {% for arch in runtime_archs[rt] %}
          {% if arch not in runtime_arch_list %}
            {% set _ = runtime_arch_list.append(arch) %}
          {% endif %}
        {% endfor %}
      {% endif %}
    {% endfor %}
  {% endif %}
  
  <div class="game-card" onclick="openModal('{{ port_id }}')"
       data-title="{{ port.attr.title | default('') if port.attr else '' }}"
       data-genres="{{ port.attr.genres | default([]) | join(',') if port.attr and port.attr.genres else '' }}"
       data-reqs="{{ port.attr.reqs | default([]) | join(',') if port.attr and port.attr.reqs else '' }}"
       data-arch="{{ port.attr.arch | default([]) | join(',') if port.attr and port.attr.arch else '' }}"
       data-runtime="{{ port.attr.runtime | default([]) | join(',') if port.attr and port.attr.runtime else '' }}"
       data-runtime-archs="{{ runtime_arch_list | join(',') }}"
       data-rtr="{{ port.attr.rtr | default(false) | string | lower }}"
       data-repo="{{ repo_owner }}/{{ repo_name }}"
       data-key="{{ key }}"
       data-port-id="{{ port_id }}"
       data-downloads="{{ download_count }}"
       data-date-added="{{ port.source.date_added if port.source and port.source.date_added else '' }}"
       data-date-updated="{{ port.source.date_updated if port.source and port.source.date_updated else '' }}"
       data-porter="{{ port.attr.porter | default([]) | join(',') if port.attr and port.attr.porter else '' }}"
       data-screenshot="{{ port.attr.image.screenshot | default('') if port.attr and port.attr.image else '' }}"
       data-url="{{ port.source.url | default('') if port.source else '' }}"
       data-desc="{{ port.attr.desc | default('') if port.attr and port.attr.desc else '' }}"
       data-desc-md="{{ port.attr.desc_md | default('') if port.attr and port.attr.desc_md else '' }}"
       data-inst="{{ port.attr.inst | default('') if port.attr and port.attr.inst else '' }}"
       data-inst-md="{{ port.attr.inst_md | default('') if port.attr and port.attr.inst_md else '' }}">
    
    {% if port.attr and port.attr.image and port.attr.image.screenshot %}
    <img src="https://raw.githubusercontent.com/{{ repo_owner }}/{{ repo_name }}/refs/heads/main/ports/{{ port_id }}/{{ port.attr.image.screenshot }}" 
         alt="{{ port.attr.title if port.attr and port.attr.title else '' }}" 
         loading="lazy"
         onerror="this.style.display='none'">
    {% endif %}

    <h3>{{ port.attr.title if port.attr and port.attr.title else '' }}</h3>
    
    <div class="card-stats">
      <span class="card-stat">
        <i class="bi bi-download"></i>
        {% if download_count > 0 %}{{ "{:,}".format(download_count) }}{% else %}—{% endif %}
      </span>
      <span class="card-stat">
        <i class="bi bi-calendar-plus"></i>
        {{ port.source.date_added if port.source and port.source.date_added else '—' }}
      </span>
    </div>
  </div>
{% endfor %}

</div>

<script>
  // ===== Cookie Helper Functions =====
  function setCookie(name, value, days = 365) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
  }

  function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }

  // ===== Global Variables =====
  let devices = {};
  let currentDevice = null;
  let currentOS = null;
  let currentSort = 'date-added';
  let currentPortId = null;
  let currentPortData = null;
  let readmeCache = {};

  const deviceSelect = document.getElementById('deviceSelect');
  const osSelect = document.getElementById('osSelect');
  const genreSelect = document.getElementById('genreSelect');
  const searchInput = document.getElementById('searchInput');
  const readyToggle = document.getElementById('readyToggle');
  const hideIncompatibleToggle = document.getElementById('hideIncompatibleToggle');
  const allCards = document.querySelectorAll('.game-card');
  const gameGrid = document.querySelector('.game-grid');

  // Filter panel elements
  const filterToggleBtn = document.getElementById('filterToggleBtn');
  const filterPanel = document.getElementById('filterPanel');
  const filterOverlay = document.getElementById('filterOverlay');
  const closePanelBtn = document.getElementById('closePanelBtn');

  // Sort elements
  const sortToggleBtn = document.getElementById('sortToggleBtn');
  const sortDropdown = document.getElementById('sortDropdown');
  const sortOptions = document.querySelectorAll('.sort-option');

  // ===== Runtime availability lookup =====
  const runtimeArchs = {{ ports.utils | default({}) | tojson | safe }};
  
  // Build a map of runtime -> available architectures
  const runtimeAvailability = {};
  Object.values(runtimeArchs).forEach(util => {
    if (util.runtime_name && util.runtime_arch) {
      if (!runtimeAvailability[util.runtime_name]) {
        runtimeAvailability[util.runtime_name] = [];
      }
      runtimeAvailability[util.runtime_name].push(util.runtime_arch.toLowerCase());
    }
  });

  // ===== Pre-sorted orders (from Python) =====
  const sortedOrders = {{ sorted_orders | tojson | safe }};

  // ===== Ports Data =====
  const portsByKey = {};
  const portsByPortId = {};
  const portsData = Array.from(allCards).map(card => {
    const key = card.dataset.key;
    const portId = card.dataset.portId;
    const title = card.querySelector('h3')?.textContent.trim() || '';
    const genres = card.dataset.genres ? card.dataset.genres.split(',').map(g => g.trim()).filter(Boolean) : [];
    const reqs = card.dataset.reqs ? card.dataset.reqs.split(',').map(r => r.trim()).filter(Boolean) : [];
    const arch = card.dataset.arch ? card.dataset.arch.split(',').map(a => a.trim()).filter(Boolean) : [];
    const runtime = card.dataset.runtime ? card.dataset.runtime.split(',').map(r => r.trim()).filter(Boolean) : [];
    const rtr = card.dataset.rtr === "true";
    const downloads = parseInt(card.dataset.downloads) || 0;
    const dateAdded = card.dataset.dateAdded || '';
    const dateUpdated = card.dataset.dateUpdated || '';

    const port = { key, portId, card, title, genres, reqs, arch, runtime, rtr, downloads, dateAdded, dateUpdated };
    portsByKey[key] = port;
    portsByPortId[portId] = port;
    return port;
  });

  // Fuse.js for fuzzy search
  const fuse = new Fuse(portsData, {
    keys: [{ name: 'title', weight: 0.6 }, { name: 'genres', weight: 0.1 }],
    threshold: 0.4
  });

  // Populate Genre Dropdown
  const allGenres = new Set(portsData.flatMap(p => p.genres));
  [...allGenres].sort().forEach(g => genreSelect.appendChild(new Option(g, g)));

  // ===== Advanced Filters (Pills) =====
  const runtimePills = document.getElementById('runtimePills');
  const archPills = document.getElementById('archPills');
  const reqPills = document.getElementById('reqPills');

  // Track selected pills
  let selectedRuntimes = new Set();
  let selectedArchs = new Set();
  let selectedReqs = new Set();

  // Create pill element
  function createPill(value, container, selectedSet) {
    const pill = document.createElement('span');
    pill.className = 'filter-pill';
    pill.textContent = value;
    pill.dataset.value = value;
    pill.addEventListener('click', () => {
      pill.classList.toggle('selected');
      if (pill.classList.contains('selected')) {
        selectedSet.add(value);
      } else {
        selectedSet.delete(value);
      }
      filterAndSearch();
    });
    container.appendChild(pill);
  }

  // Populate pills
  const allRuntimes = new Set(portsData.flatMap(p => p.runtime));
  [...allRuntimes].sort().forEach(r => createPill(r, runtimePills, selectedRuntimes));

  const allArchs = new Set(portsData.flatMap(p => p.arch));
  [...allArchs].sort().forEach(a => createPill(a, archPills, selectedArchs));

  const allReqs = new Set(portsData.flatMap(p => p.reqs));
  [...allReqs].sort().forEach(r => createPill(r, reqPills, selectedReqs));

  // Toggle Advanced Filters
  function toggleAdvancedFilters() {
    const content = document.getElementById('advancedFiltersContent');
    const arrow = document.getElementById('advancedArrow');
    content.classList.toggle('open');
    arrow.classList.toggle('open');
  }

  // Clear all advanced filters
  function clearAdvancedFilters() {
    selectedRuntimes.clear();
    selectedArchs.clear();
    selectedReqs.clear();
    
    document.querySelectorAll('.filter-pill.selected').forEach(pill => {
      pill.classList.remove('selected');
    });
    
    filterAndSearch();
  }

  // Clear ALL filters (for main clear button)
  function clearAllFilters() {
    // Clear advanced pills
    clearAdvancedFilters();
    
    // Clear device
    deviceSelect.value = '';
    if (deviceSelect.customTrigger) {
      deviceSelect.customTrigger.textContent = 'Select your device...';
    }
    currentDevice = null;
    
    // Clear OS
    osSelect.innerHTML = '<option value="">Select OS...</option>';
    osSelect.disabled = true;
    if (osSelect.customTrigger) {
      osSelect.customTrigger.textContent = 'Select OS...';
    }
    if (osSelect.customWrapper) {
      osSelect.customWrapper.querySelector('.custom-select-trigger').classList.add('disabled');
    }
    currentOS = null;
    
    // Clear genre
    genreSelect.value = '';
    if (genreSelect.customTrigger) {
      genreSelect.customTrigger.textContent = 'All Genres';
    }
    
    // Clear toggles
    readyToggle.checked = false;
    hideIncompatibleToggle.checked = false;
    
    // Clear search
    searchInput.value = '';
    
    // Clear cookies
    setCookie('selectedDevice', '', -1);
    setCookie('selectedOS', '', -1);
    setCookie('selectedGenre', '', -1);
    setCookie('readyToggle', '', -1);
    setCookie('hideIncompatible', '', -1);
    
    filterAndSearch();
  }

  // ===== Back to Top Button =====
  const backToTopBtn = document.getElementById('backToTop');
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
      backToTopBtn.classList.add('visible');
    } else {
      backToTopBtn.classList.remove('visible');
    }
  });

  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // ===== Sort Dropdown Toggle =====
  sortToggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    sortDropdown.classList.toggle('open');
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.sort-dropdown-wrapper')) {
      sortDropdown.classList.remove('open');
    }
  });

  sortOptions.forEach(option => {
    option.addEventListener('click', () => {
      sortOptions.forEach(opt => opt.classList.remove('selected'));
      option.classList.add('selected');
      currentSort = option.dataset.sort;
      sortDropdown.classList.remove('open');
      sortCards();
    });
  });

  // ===== Sort Cards Function =====
  function sortCards() {
    const order = sortedOrders[currentSort] || sortedOrders['az'];
    
    // Use CSS order property instead of moving DOM elements
    order.forEach((key, index) => {
      const port = portsByKey[key];
      if (port) {
        port.card.style.order = index;
      }
    });
  }

  // ===== Filter Panel Toggle =====
  function openFilterPanel() {
    filterPanel.classList.add('open');
    filterOverlay.classList.add('active');
    filterToggleBtn.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeFilterPanel() {
    filterPanel.classList.remove('open');
    filterOverlay.classList.remove('active');
    filterToggleBtn.classList.remove('active');
    document.body.style.overflow = '';
  }

  filterToggleBtn.addEventListener('click', () => {
    if (filterPanel.classList.contains('open')) {
      closeFilterPanel();
    } else {
      openFilterPanel();
    }
  });

  closePanelBtn.addEventListener('click', closeFilterPanel);
  filterOverlay.addEventListener('click', closeFilterPanel);

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && filterPanel.classList.contains('open')) {
      closeFilterPanel();
    }
  });

  // ===== Device Data Loading =====
  devices = {{ device_info | tojson | safe }};
  
  // Populate device dropdown
  Object.keys(devices).forEach(deviceName => deviceSelect.appendChild(new Option(deviceName, deviceName)));

  deviceSelect.addEventListener('change', e => {
    const deviceName = e.target.value;
    currentDevice = deviceName ? devices[deviceName] : null;
    
    // Save device to cookie
    if (deviceName) {
      setCookie('selectedDevice', deviceName);
    } else {
      setCookie('selectedDevice', '', -1);
    }

    osSelect.innerHTML = '<option value="">Select OS...</option>';
    if (currentDevice) {
      const osNames = Object.keys(currentDevice);
      osNames.forEach(osName => osSelect.appendChild(new Option(osName, osName)));
      osSelect.disabled = false;

      // Try to load saved OS from cookie
      const savedOS = getCookie('selectedOS');
      if (savedOS && osNames.includes(savedOS)) {
        osSelect.value = savedOS;
        currentOS = currentDevice[savedOS];
      } else if (osNames.length > 0) {
        osSelect.value = osNames[0];
        currentOS = currentDevice[osNames[0]];
      }
      
      if (osSelect.updateCustomOptions) {
        osSelect.updateCustomOptions();
        osSelect.customTrigger.textContent = osSelect.options[osSelect.selectedIndex].text;
        osSelect.customWrapper.querySelector('.custom-select-trigger').classList.remove('disabled');
      }
    } else {
      osSelect.disabled = true;
      currentOS = null;
      if (osSelect.updateCustomOptions) {
        osSelect.updateCustomOptions();
      }
      if (osSelect.customWrapper) {
        osSelect.customWrapper.querySelector('.custom-select-trigger').classList.add('disabled');
        if (osSelect.customTrigger) {
          osSelect.customTrigger.textContent = 'Select OS...';
        }
      }
    }
    filterAndSearch();
  });

  osSelect.addEventListener('change', e => {
    const selectedOS = e.target.value;
    currentOS = selectedOS && currentDevice ? currentDevice[selectedOS] : null;
    
    // Save OS to cookie
    if (selectedOS) {
      setCookie('selectedOS', selectedOS);
    } else {
      setCookie('selectedOS', '', -1);
    }
    
    filterAndSearch();
  });

  genreSelect.addEventListener('change', () => {
    setCookie('selectedGenre', genreSelect.value);
    filterAndSearch();
  });
  
  // Debounce for search to prevent lag on mobile
  let searchTimeout;
  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(filterAndSearch, 150);
  });
  
  readyToggle.addEventListener('change', () => {
    setCookie('readyToggle', readyToggle.checked ? 'true' : '');
    filterAndSearch();
  });
  
  hideIncompatibleToggle.addEventListener('change', () => {
    setCookie('hideIncompatible', hideIncompatibleToggle.checked ? 'true' : '');
    filterAndSearch();
  });

  // ===== Restore Saved Filters =====
  function restoreSavedFilters() {
    // Restore genre
    const savedGenre = getCookie('selectedGenre');
    if (savedGenre) {
      genreSelect.value = savedGenre;
      if (genreSelect.customTrigger) {
        genreSelect.customTrigger.textContent = genreSelect.options[genreSelect.selectedIndex]?.text || 'All Genres';
      }
    }
    
    // Restore toggles
    const savedRTR = getCookie('readyToggle');
    if (savedRTR === 'true') {
      readyToggle.checked = true;
    }
    
    const savedHideIncompat = getCookie('hideIncompatible');
    if (savedHideIncompat === 'true') {
      hideIncompatibleToggle.checked = true;
    }
    
    // Restore device (triggers change event which loads OS)
    const savedDevice = getCookie('selectedDevice');
    if (savedDevice && devices[savedDevice]) {
      deviceSelect.value = savedDevice;
      if (deviceSelect.customTrigger) {
        deviceSelect.customTrigger.textContent = savedDevice;
      }
      deviceSelect.dispatchEvent(new Event('change'));
    }
  }

  // ===== Compatibility Check =====
  function checkCompatibility(port) {
    if (!currentDevice || !currentOS) {
      return true;
    }

    const capabilities = new Set(
      (currentOS.capabilities || []).map(c => c.toLowerCase())
    );

    const primaryArch = (currentOS.primary_arch || '').toLowerCase();

    if (port.arch.length === 0) {
      if (port.runtime.length > 0) {
        let hasCompatibleRuntime = false;
        
        for (const runtime of port.runtime) {
          const availableArchs = runtimeAvailability[runtime] || [];
          if (availableArchs.includes(primaryArch) || availableArchs.some(arch => capabilities.has(arch))) {
            hasCompatibleRuntime = true;
            break;
          }
        }
        
        if (!hasCompatibleRuntime) return false;
      }
    } else {
      const requiredArches = port.arch.map(a => a.toLowerCase());
      let hasArch = requiredArches.includes(primaryArch) || requiredArches.includes('all');
      
      if (!hasArch) {
        hasArch = requiredArches.some(arch => capabilities.has(arch));
      }
      if (!hasArch) return false;
    }

    for (const req of port.reqs) {
      const reqLower = req.toLowerCase();
      if (reqLower.startsWith("!")) {
        // Negative requirement - device must NOT have this
        const negReq = reqLower.slice(1);
        if (capabilities.has(negReq)) {
          return false;
        }
      } else if (reqLower.startsWith("power:")) {
        // Power requirements - skip for now
        continue;
      } else if (reqLower.includes("|")) {
        // OR requirement - device needs at least one of these
        const options = reqLower.split("|").map(o => o.trim());
        const hasAny = options.some(opt => capabilities.has(opt));
        if (!hasAny) {
          return false;
        }
      } else {
        // Standard requirement - device must have this
        if (!capabilities.has(reqLower)) {
          return false;
        }
      }
    }

    return true;
  }

  // ===== Filter + Search + Counter =====
  function filterAndSearch() {
    const query = searchInput.value.trim();
    const selectedGenre = genreSelect.value;
    const readyOnly = readyToggle.checked;
    const hideIncompatible = hideIncompatibleToggle.checked;
    const searchSet = query ? new Set(fuse.search(query).map(r => r.item)) : null;

    let supported = 0, unsupported = 0, visible = 0;
    
    // Collect all changes first, then apply in batch
    const changes = [];

    portsData.forEach(port => {
      const matchSearch = !searchSet || searchSet.has(port);
      const genreMatch = !selectedGenre || port.genres.includes(selectedGenre);
      const rtrMatch = !readyOnly || port.rtr;
      const compatible = checkCompatibility(port);

      // Advanced filters (pills)
      const runtimeMatch = selectedRuntimes.size === 0 || port.runtime.some(r => selectedRuntimes.has(r));
      const archMatch = selectedArchs.size === 0 || port.arch.some(a => selectedArchs.has(a));
      const reqMatch = selectedReqs.size === 0 || port.reqs.some(r => selectedReqs.has(r));

      if (currentOS) {
        if (compatible) {
          supported++;
        } else {
          unsupported++;
        }
      }

      let shouldShow = matchSearch && genreMatch && rtrMatch && runtimeMatch && archMatch && reqMatch;
      if (currentOS && hideIncompatible) {
        shouldShow = shouldShow && compatible;
      }
      
      if (shouldShow) {
        visible++;
      }

      const shouldBeIncompatible = currentOS && !compatible && !hideIncompatible && shouldShow;
      
      changes.push({
        card: port.card,
        display: shouldShow ? "flex" : "none",
        incompatible: shouldBeIncompatible
      });
    });

    // Apply all DOM changes in one batch
    requestAnimationFrame(() => {
      changes.forEach(({ card, display, incompatible }) => {
        card.style.display = display;
        if (incompatible) {
          card.classList.add('incompatible');
        } else {
          card.classList.remove('incompatible');
        }
      });
    });

    const counterEl = document.getElementById('portsCounter');
    if (currentOS) {
      counterEl.textContent = `Supported: ${supported} | Unsupported: ${unsupported} | Showing: ${visible}`;
    } else {
      counterEl.textContent = `Showing: ${visible} of ${portsData.length} ports`;
    }
    
    // Update URL with current filter state
    updateURLState();
  }

  // ===== URL State for Shareable Filters =====
  function updateURLState() {
    const params = new URLSearchParams();
    
    const query = searchInput.value.trim();
    if (query) params.set('search', query);
    
    const genre = genreSelect.value;
    if (genre) params.set('genre', genre);
    
    if (readyToggle.checked) params.set('rtr', '1');
    if (hideIncompatibleToggle.checked) params.set('hideIncompat', '1');
    
    if (selectedRuntimes.size > 0) params.set('runtime', [...selectedRuntimes].join(','));
    if (selectedArchs.size > 0) params.set('arch', [...selectedArchs].join(','));
    if (selectedReqs.size > 0) params.set('reqs', [...selectedReqs].join(','));
    
    const device = deviceSelect.value;
    if (device) params.set('device', device);
    const os = osSelect.value;
    if (os) params.set('os', os);
    
    const newUrl = params.toString() 
      ? `${window.location.pathname}?${params.toString()}${window.location.hash}`
      : `${window.location.pathname}${window.location.hash}`;
    
    history.replaceState(null, '', newUrl);
  }

  function loadURLState() {
    const params = new URLSearchParams(window.location.search);
    
    const query = params.get('search');
    if (query) searchInput.value = query;
    
    const genre = params.get('genre');
    if (genre && genreSelect.querySelector(`option[value="${genre}"]`)) {
      genreSelect.value = genre;
    }
    
    if (params.get('rtr') === '1') readyToggle.checked = true;
    if (params.get('hideIncompat') === '1') hideIncompatibleToggle.checked = true;
    
    const runtimeParam = params.get('runtime');
    if (runtimeParam) {
      runtimeParam.split(',').forEach(r => {
        selectedRuntimes.add(r);
        const pill = document.querySelector(`#runtimePills .filter-pill[data-value="${r}"]`);
        if (pill) pill.classList.add('selected');
      });
    }
    
    const archParam = params.get('arch');
    if (archParam) {
      archParam.split(',').forEach(a => {
        selectedArchs.add(a);
        const pill = document.querySelector(`#archPills .filter-pill[data-value="${a}"]`);
        if (pill) pill.classList.add('selected');
      });
    }
    
    const reqsParam = params.get('reqs');
    if (reqsParam) {
      reqsParam.split(',').forEach(r => {
        selectedReqs.add(r);
        const pill = document.querySelector(`#reqPills .filter-pill[data-value="${r}"]`);
        if (pill) pill.classList.add('selected');
      });
    }
    
    if (runtimeParam || archParam || reqsParam) {
      document.getElementById('advancedFiltersContent').classList.add('open');
      document.getElementById('advancedArrow').classList.add('open');
    }
  }

  // ===== Modal Functions =====
  function openModal(portId) {
    const card = document.querySelector(`[data-port-id="${portId}"]`);
    if (!card) return;
    
    currentPortId = portId;
    currentPortData = portsByPortId[portId];
    
    const modal = document.getElementById('portModal');
    
    // Get data from card attributes
    const title = card.dataset.title || '';
    const repo = card.dataset.repo || '';
    const screenshot = card.dataset.screenshot || '';
    const genres = card.dataset.genres ? card.dataset.genres.split(',').filter(Boolean) : [];
    const reqs = card.dataset.reqs ? card.dataset.reqs.split(',').filter(Boolean) : [];
    const porter = card.dataset.porter ? card.dataset.porter.split(',').filter(Boolean) : [];
    const runtime = card.dataset.runtime ? card.dataset.runtime.split(',').filter(Boolean) : [];
    const arch = card.dataset.arch ? card.dataset.arch.split(',').filter(Boolean) : [];
    const rtr = card.dataset.rtr === 'true';
    const downloads = parseInt(card.dataset.downloads) || 0;
    const dateAdded = card.dataset.dateAdded || '';
    const dateUpdated = card.dataset.dateUpdated || '';
    const url = card.dataset.url || '';
    const desc = card.dataset.desc || '';
    const descMd = card.dataset.descMd || '';
    const inst = card.dataset.inst || '';
    const instMd = card.dataset.instMd || '';
    
    // Populate modal
    document.getElementById('modal-title').textContent = title;
    
    // Screenshot
    const screenshotContainer = document.getElementById('modal-screenshot-container');
    const screenshotImg = document.getElementById('modal-screenshot');
    if (screenshot) {
      screenshotImg.src = `https://raw.githubusercontent.com/${repo}/refs/heads/main/ports/${portId}/${screenshot}`;
      screenshotImg.alt = title;
      screenshotContainer.style.display = '';
    } else {
      screenshotContainer.style.display = 'none';
    }
    
    // Description - prefer markdown version if available
    const descEl = document.getElementById('modal-desc');
    const descContent = descMd || desc;
    if (descContent && descContent.trim() && descContent.trim() !== 'None') {
      descEl.innerHTML = marked.parse(descContent);
    } else {
      descEl.innerHTML = '';
    }
    
    // Download button
    const downloadBtn = document.getElementById('modal-download-btn');
    downloadBtn.href = url || '#';
    updateDownloadButton();
    
    // Helper for badges
    const makeBadges = arr => arr.length > 0 
      ? arr.map(v => `<span class="info-badge">${v}</span>`).join('') 
      : '—';
    
    // Helper for porter links
		const makePorterLinks = arr => arr.length > 0
	  ? arr.map(v => `<a href="../porters/#porter-${encodeURIComponent(v)}" class="porter-link-badge" onclick="event.stopPropagation()">${v} <i class="bi bi-box-arrow-up-right"></i></a>`).join(' ')
	  : '—';
    
    // Info grid
    document.getElementById('modal-genres').innerHTML = makeBadges(genres);
    document.getElementById('modal-reqs').innerHTML = makeBadges(reqs);
    document.getElementById('modal-porter').innerHTML = makePorterLinks(porter);
    document.getElementById('modal-downloads').textContent = downloads > 0 ? downloads.toLocaleString() : 'N/A';
    document.getElementById('modal-runtimes').innerHTML = makeBadges(runtime);
    document.getElementById('modal-arch').innerHTML = makeBadges(arch);
    document.getElementById('modal-date-added').textContent = dateAdded || 'N/A';
    document.getElementById('modal-date-updated').textContent = dateUpdated || 'N/A';
    document.getElementById('modal-misc').innerHTML = rtr 
      ? '<span class="info-badge">Ready to Run</span>' 
      : '<span class="info-badge">Setup Required</span>';
    
    // Instructions
    const instSection = document.getElementById('modal-inst-section');
    const instEl = document.getElementById('modal-inst');
    const instContent = instMd || inst;
    if (instContent && instContent.trim() && instContent.trim() !== 'None') {
      instEl.innerHTML = marked.parse(instContent);
      instSection.style.display = '';
    } else {
      instSection.style.display = 'none';
    }
    
    // README
    loadReadme(portId, repo);
    
    // Show modal with animation
    modal.style.display = 'block';
    modal.offsetHeight; // Trigger reflow for animation
    modal.classList.add('show');
    history.pushState({ modal: portId }, '', '#modal-' + portId);
  }

  function closeModal(updateHistory = true) {
    const modal = document.getElementById('portModal');
    modal.classList.remove('show');
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300);
    currentPortId = null;
    currentPortData = null;
    
    if (updateHistory && window.location.hash.startsWith('#modal-')) {
      history.pushState({ modal: null }, '', window.location.pathname + window.location.search);
    }
  }

  // Handle back/forward button
  window.addEventListener('popstate', (e) => {
    const hash = window.location.hash;
    
    if (hash.startsWith('#modal-')) {
      const portId = hash.replace('#modal-', '');
      if (portsByPortId[portId]) {
        openModalDirect(portId);
      }
    } else {
      closeModal(false);
    }
  });

  // Direct modal open without history push (for popstate)
  function openModalDirect(portId) {
    const card = document.querySelector(`[data-port-id="${portId}"]`);
    if (!card) return;
    
    currentPortId = portId;
    currentPortData = portsByPortId[portId];
    
    const modal = document.getElementById('portModal');
    
    const title = card.dataset.title || '';
    const repo = card.dataset.repo || '';
    const screenshot = card.dataset.screenshot || '';
    const genres = card.dataset.genres ? card.dataset.genres.split(',').filter(Boolean) : [];
    const reqs = card.dataset.reqs ? card.dataset.reqs.split(',').filter(Boolean) : [];
    const porter = card.dataset.porter ? card.dataset.porter.split(',').filter(Boolean) : [];
    const runtime = card.dataset.runtime ? card.dataset.runtime.split(',').filter(Boolean) : [];
    const arch = card.dataset.arch ? card.dataset.arch.split(',').filter(Boolean) : [];
    const rtr = card.dataset.rtr === 'true';
    const downloads = parseInt(card.dataset.downloads) || 0;
    const dateAdded = card.dataset.dateAdded || '';
    const dateUpdated = card.dataset.dateUpdated || '';
    const url = card.dataset.url || '';
    const desc = card.dataset.desc || '';
    const descMd = card.dataset.descMd || '';
    const inst = card.dataset.inst || '';
    const instMd = card.dataset.instMd || '';
    
    document.getElementById('modal-title').textContent = title;
    
    const screenshotContainer = document.getElementById('modal-screenshot-container');
    const screenshotImg = document.getElementById('modal-screenshot');
    if (screenshot) {
      screenshotImg.src = `https://raw.githubusercontent.com/${repo}/refs/heads/main/ports/${portId}/${screenshot}`;
      screenshotImg.alt = title;
      screenshotContainer.style.display = '';
    } else {
      screenshotContainer.style.display = 'none';
    }
    
    const descEl = document.getElementById('modal-desc');
    const descContent = descMd || desc;
    if (descContent && descContent.trim() && descContent.trim() !== 'None') {
      descEl.innerHTML = marked.parse(descContent);
    } else {
      descEl.innerHTML = '';
    }
    
    const downloadBtn = document.getElementById('modal-download-btn');
    downloadBtn.href = url || '#';
    updateDownloadButton();
    
    const makeBadges = arr => arr.length > 0 
      ? arr.map(v => `<span class="info-badge">${v}</span>`).join('') 
      : '—';
    
    const makePorterLinks = arr => arr.length > 0
      ? arr.map(v => `<a href="../porters/#porter-${encodeURIComponent(v)}" class="porter-link-badge" onclick="event.stopPropagation()">${v} <i class="bi bi-box-arrow-up-right"></i></a>`).join(' ')
      : '—';
    
    document.getElementById('modal-genres').innerHTML = makeBadges(genres);
    document.getElementById('modal-reqs').innerHTML = makeBadges(reqs);
    document.getElementById('modal-porter').innerHTML = makePorterLinks(porter);
    document.getElementById('modal-downloads').textContent = downloads > 0 ? downloads.toLocaleString() : 'N/A';
    document.getElementById('modal-runtimes').innerHTML = makeBadges(runtime);
    document.getElementById('modal-arch').innerHTML = makeBadges(arch);
    document.getElementById('modal-date-added').textContent = dateAdded || 'N/A';
    document.getElementById('modal-date-updated').textContent = dateUpdated || 'N/A';
    document.getElementById('modal-misc').innerHTML = rtr 
      ? '<span class="info-badge">Ready to Run</span>' 
      : '<span class="info-badge">Setup Required</span>';
    
    const instSection = document.getElementById('modal-inst-section');
    const instEl = document.getElementById('modal-inst');
    const instContent = instMd || inst;
    if (instContent && instContent.trim() && instContent.trim() !== 'None') {
      instEl.innerHTML = marked.parse(instContent);
      instSection.style.display = '';
    } else {
      instSection.style.display = 'none';
    }
    
    loadReadme(portId, repo);
    
    modal.style.display = 'block';
    modal.offsetHeight;
    modal.classList.add('show');
  }

  // Close modal when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
      closeModal();
    }
  });

  // ===== Download Button =====
  function getSelectedDeviceName() {
    return deviceSelect.value || null;
  }

  function updateDownloadButton() {
    const downloadBtn = document.getElementById('modal-download-btn');
    const deviceName = getSelectedDeviceName();

    if (downloadBtn) {
      if (deviceName) {
        downloadBtn.textContent = `Download for ${deviceName}`;
      } else {
        downloadBtn.textContent = 'Download';
      }
    }
  }

  function handleDownload(event) {
    const deviceName = getSelectedDeviceName();
    const warningDiv = document.getElementById('downloadWarning');
    
    if (!currentPortData) return;
    
    if (deviceName && currentOS) {
      const compatible = checkCompatibility(currentPortData);
      
      if (!compatible) {
        event.preventDefault();
        
        const warningText = warningDiv.querySelector('span');
        const warningIcon = warningDiv.querySelector('i');
        
        if (warningText) {
          warningText.textContent = `This port is not compatible with ${deviceName}. Download blocked.`;
        }
        if (warningIcon) {
          warningIcon.className = 'bi bi-x-circle';
        }
        
        warningDiv.classList.add('error');
        warningDiv.classList.remove('fade-out');
        warningDiv.style.display = 'flex';
        
        setTimeout(() => {
          warningDiv.classList.add('fade-out');
          setTimeout(() => {
            warningDiv.style.display = 'none';
            warningDiv.classList.remove('fade-out', 'error');
            if (warningText) {
              warningText.textContent = 'No device selected. This port may not be compatible with your device.';
            }
            if (warningIcon) {
              warningIcon.className = 'bi bi-exclamation-triangle';
            }
          }, 300);
        }, 3000);
        
        return false;
      }
    }
    
    if (!deviceName && warningDiv) {
      warningDiv.classList.remove('fade-out', 'error');
      warningDiv.style.display = 'flex';
      
      setTimeout(() => {
        warningDiv.classList.add('fade-out');
        setTimeout(() => {
          warningDiv.style.display = 'none';
          warningDiv.classList.remove('fade-out');
        }, 300);
      }, 2700);
    }
  }

  function openDeviceFilter(event) {
    event.preventDefault();
    event.stopPropagation();
    openFilterPanel();
  }

  // ===== Share Port =====
  async function sharePort(event) {
    event.preventDefault();
    event.stopPropagation();
    
    if (!currentPortId) return;
    
    const card = document.querySelector(`[data-port-id="${currentPortId}"]`);
    const portTitle = card ? card.dataset.title : '';
    
    const shareUrl = `${window.location.origin}${window.location.pathname}#modal-${currentPortId}`;
    const shareData = {
      title: portTitle,
      text: `Check out ${portTitle} on PortMaster!`,
      url: shareUrl
    };
    
    // Try native Web Share API first (mobile)
    if (navigator.share) {
      try {
        await navigator.share(shareData);
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.error('Share failed:', err);
        }
      }
    } else {
      // Fallback: Copy to clipboard
      try {
        await navigator.clipboard.writeText(shareUrl);
        showShareConfirmation(event.target);
      } catch (err) {
        // Final fallback
        const textArea = document.createElement('textarea');
        textArea.value = shareUrl;
        textArea.style.position = 'fixed';
        textArea.style.left = '-9999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
          document.execCommand('copy');
          showShareConfirmation(event.target);
        } catch (e) {
          console.error('Copy failed:', e);
        }
        document.body.removeChild(textArea);
      }
    }
  }

  function showShareConfirmation(buttonElement) {
    const button = buttonElement.closest('.share-btn');
    if (!button) return;
    
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="bi bi-check2"></i>';
    button.style.backgroundColor = '#28a745';
    
    setTimeout(() => {
      button.innerHTML = originalHTML;
      button.style.backgroundColor = '';
    }, 2000);
  }

  // ===== Load README =====
  async function loadReadme(portId, repo) {
    const readmeEl = document.getElementById('modal-readme');
    
    if (readmeCache[portId]) {
      readmeEl.innerHTML = readmeCache[portId];
      return;
    }
    
    readmeEl.innerHTML = '<div class="loading-spinner">Loading...</div>';
    
    const readmeUrl = `https://raw.githubusercontent.com/${repo}/refs/heads/main/ports/${portId}/README.md`;
    
    try {
      const res = await fetch(readmeUrl);
      if (!res.ok) throw new Error('Not found');
      const md = await res.text();
      const html = marked.parse(md);
      readmeCache[portId] = html;
      if (currentPortId === portId) {
        readmeEl.innerHTML = html;
      }
    } catch (err) {
      const fallback = '<p>No additional information available.</p>';
      readmeCache[portId] = fallback;
      if (currentPortId === portId) {
        readmeEl.innerHTML = fallback;
      }
    }
  }

  // ===== Custom Select Styling =====
  function initializeCustomSelects() {
    const selects = [deviceSelect, osSelect, genreSelect];
    
    selects.forEach(select => {
      if (select.customWrapper) return; // Already initialized
      
      const wrapper = document.createElement('div');
      wrapper.className = 'custom-select-wrapper';
      select.parentNode.insertBefore(wrapper, select);
      wrapper.appendChild(select);
      
      const trigger = document.createElement('div');
      trigger.className = 'custom-select-trigger';
      if (select.disabled) trigger.classList.add('disabled');
      
      const triggerText = document.createElement('span');
      triggerText.textContent = select.options[select.selectedIndex].text;
      
      const arrow = document.createElement('div');
      arrow.className = 'custom-select-arrow';
      arrow.innerHTML = '<i class="bi bi-chevron-down"></i>';
      
      trigger.appendChild(triggerText);
      trigger.appendChild(arrow);
      wrapper.appendChild(trigger);
      
      const optionsContainer = document.createElement('div');
      optionsContainer.className = 'custom-select-options';
      
      function updateOptions() {
        optionsContainer.innerHTML = '';
        Array.from(select.options).forEach((option, index) => {
          const customOption = document.createElement('div');
          customOption.className = 'custom-select-option';
          if (index === select.selectedIndex) customOption.classList.add('selected');
          customOption.textContent = option.text;
          customOption.addEventListener('click', () => {
            select.selectedIndex = index;
            select.dispatchEvent(new Event('change'));
            triggerText.textContent = option.text;
            wrapper.classList.remove('open');
            optionsContainer.querySelectorAll('.custom-select-option').forEach(o => o.classList.remove('selected'));
            customOption.classList.add('selected');
          });
          optionsContainer.appendChild(customOption);
        });
      }
      updateOptions();
      wrapper.appendChild(optionsContainer);
      
      trigger.addEventListener('click', () => {
        if (select.disabled) return;
        document.querySelectorAll('.custom-select-wrapper.open').forEach(w => {
          if (w !== wrapper) w.classList.remove('open');
        });
        wrapper.classList.toggle('open');
      });
      
      document.addEventListener('click', (e) => {
        if (!wrapper.contains(e.target)) {
          wrapper.classList.remove('open');
        }
      });
      
      select.customWrapper = wrapper;
      select.customTrigger = triggerText;
      select.updateCustomOptions = updateOptions;
    });
  }

  // ===== Initialize =====
  // Use requestIdleCallback to avoid blocking MkDocs Material initialization
  function initializePage() {
    initializeCustomSelects();
    loadURLState();
    restoreSavedFilters();
    sortCards();
    filterAndSearch();

    const hash = window.location.hash.substring(1);
    if (hash && hash.startsWith('modal-')) {
      const portId = hash.replace('modal-', '');
      if (portsByPortId[portId]) {
        openModal(portId);
      }
    }
  }

  if ('requestIdleCallback' in window) {
    requestIdleCallback(initializePage, { timeout: 1000 });
  } else {
    setTimeout(initializePage, 100);
  }

</script>