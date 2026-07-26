---
hide:
  - navigation
  - toc
  - path

search:
  exclude: true
---

<div style="display:none">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
</div>
<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.1.0/dist/fuse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>.md-path { display: none; }</style>

{% macro port_card(port_key) %}
{% set port = ports.ports[port_key] %}
{% if port %}
{% set port_id = port_key.replace('.zip', '') %}
{% set attr = port.attr or {} %}
{% set title = attr.title or port_id %}
{% set screenshot = attr.image.screenshot if attr.image else '' %}
{% set downloads = port_stats.ports[port_key] | default(0) %}
{% set source = port.source or {} %}
{% set date_added = source.date_added or '' %}
{% set is_mv = 'PortMaster-MV' in (source.url or '') or 'MV-New' in (source.url or '') %}
{% set repo_owner = 'PortsMaster-MV' if is_mv else 'PortsMaster' %}
{% set repo_name = 'PortMaster-MV-New' if is_mv else 'PortMaster-New' %}
  <div class="pm-card" data-port-id="{{ port_id }}" onclick="window.location.href='../port/#{{ port_id }}'">
    {% if attr.rtr %}<span class="pm-rtr-badge"><i class="bi bi-check-lg"></i> RTR</span>{% endif %}
    {% if screenshot %}
    <img src="https://raw.githubusercontent.com/{{ repo_owner }}/{{ repo_name }}/refs/heads/main/ports/{{ port_id }}/{{ screenshot }}"
         alt="{{ title }}"
         loading="lazy"
         onerror="this.style.display='none'">
    {% endif %}
    <h3>{{ title }}</h3>
    <div class="card-stats">
      <span class="card-stat">
        <i class="bi bi-download"></i>
        {% if downloads > 0 %}{{ "{:,}".format(downloads) }}{% else %}—{% endif %}
      </span>
      <span class="card-stat">
        <i class="bi bi-calendar-plus"></i>
        {{ date_added or '—' }}
      </span>
    </div>
  </div>
{% endif %}
{% endmacro %}

{# Unified carousel section: title (+ inline "See All") on the left, prev/next
   arrows on the right - one shared layout for every carousel, standalone or
   nested inside a category, so they all look and behave the same way. #}
{% macro carousel_block(level, title, track_id, port_keys) %}
<div class="featured-group">
  <div class="carousel-section-header">
    <div class="carousel-section-title">
      {% if level == 1 %}<h1>{{ title }}</h1>{% else %}<h2>{{ title }}</h2>{% endif %}
    </div>
    <div class="carousel-nav">
      <a href="../games/#browse" class="see-all-inline"><span class="sr-only">See All</span> <i class="bi bi-chevron-right"></i></a>
      <div class="carousel-btn-group">
        <button class="carousel-btn carousel-btn-left" onclick="scrollCarousel('{{ track_id }}', -1)">
          <i class="bi bi-chevron-left"></i>
        </button>
        <button class="carousel-btn carousel-btn-right" onclick="scrollCarousel('{{ track_id }}', 1)">
          <i class="bi bi-chevron-right"></i>
        </button>
      </div>
    </div>
  </div>
  <div class="carousel-container">
    <div class="carousel-track" id="{{ track_id }}">
      {% for port_key in port_keys %}{{ port_card(port_key) }}{% endfor %}
    </div>
  </div>
</div>
{% endmacro %}

{# One genre tile: background image is the most-downloaded port carrying
   that genre tag. Shared between the Discover "Browse by Genre" preview
   and the full grid on the Browse view, so both stay in sync. #}
{% macro genre_tile(genre) %}
{% set ns = namespace(found_key=None) %}
{% for key in sorted_orders['downloads'] %}
  {% if ns.found_key is none %}
    {% set p = ports.ports[key] %}
    {% if p.attr and p.attr.genres and genre in p.attr.genres and p.attr.image and p.attr.image.screenshot %}
      {% set ns.found_key = key %}
    {% endif %}
  {% endif %}
{% endfor %}
{% if ns.found_key %}
  {% set p = ports.ports[ns.found_key] %}
  {% set p_id = ns.found_key.replace('.zip', '') %}
  {% set p_is_mv = 'PortMaster-MV' in (p.source.url or '') if p.source else false %}
  {% set p_is_mv = p_is_mv or ('MV-New' in (p.source.url or '') if p.source else false) %}
  {% set p_owner = 'PortsMaster-MV' if p_is_mv else 'PortsMaster' %}
  {% set p_repo = 'PortMaster-MV-New' if p_is_mv else 'PortMaster-New' %}
  {% set bg_url = 'https://raw.githubusercontent.com/' ~ p_owner ~ '/' ~ p_repo ~ '/refs/heads/main/ports/' ~ p_id ~ '/' ~ p.attr.image.screenshot %}
  <div class="genre-tile" data-genre="{{ genre }}" style="background-image:url('{{ bg_url }}')"><span>{{ genre }}</span></div>
{% else %}
  <div class="genre-tile" data-genre="{{ genre }}"><span>{{ genre }}</span></div>
{% endif %}
{% endmacro %}

{% set genre_set = [] %}
{% for key, port in ports.ports.items() %}
  {% if port.attr and port.attr.genres %}
    {% for g in port.attr.genres %}
      {% if g and g not in genre_set %}{% set _ = genre_set.append(g) %}{% endif %}
    {% endfor %}
  {% endif %}
{% endfor %}
{% set genre_list = genre_set | sort %}

<div class="games-topbar">
  <div class="games-search-wrapper">
    <i class="bi bi-search games-search-icon"></i>
    <input type="text" id="gamesSearchInput" class="games-search-input" placeholder="Search ports...">
  </div>
  <div class="games-view-switcher">
    <button class="games-view-btn active" data-view="discover" id="discoverTabBtn">Discover</button>
    <button class="games-view-btn" data-view="browse" id="browseTabBtn">Browse</button>
  </div>
</div>

<div class="games-view active" id="discover-view">

{% if hero_slides %}
<div class="hero-banner" id="heroBanner">
  <div class="hero-main">
    {% for slide in hero_slides %}
    {% set hero_bg_url = slide.custom_image_url if slide.custom_image_url else ('https://raw.githubusercontent.com/' ~ slide.repo ~ '/refs/heads/main/ports/' ~ slide.port_id ~ '/' ~ slide.screenshot if slide.screenshot else '') %}
    <div class="hero-slide{% if loop.first %} active{% endif %}" data-index="{{ loop.index0 }}"{% if hero_bg_url %} style="background-image:url('{{ hero_bg_url }}')"{% endif %}>
      <div class="hero-slide-overlay">
        {% if slide.rtr %}
        <span class="hero-slide-status hero-slide-status--rtr"><i class="bi bi-check-lg"></i> Ready to Run</span>
        {% else %}
        <span class="hero-slide-status"><i class="bi bi-tools"></i> Files Required</span>
        {% endif %}
        <h1 class="hero-slide-title">{{ slide.title }}</h1>
        {% if slide.desc %}<p class="hero-slide-desc">{{ slide.desc }}</p>{% endif %}
        <div class="hero-slide-actions">
          <a href="{{ slide.url }}" class="hero-download-btn">Download</a>
          <a href="../port/#{{ slide.port_id }}" class="hero-details-link">View Details <i class="bi bi-chevron-right"></i></a>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
  <div class="hero-sidebar">
    {% for slide in hero_slides %}
    <button type="button" class="hero-pill{% if loop.first %} active{% endif %}" data-index="{{ loop.index0 }}">
      <span class="hero-pill-progress"></span>
      {% if slide.screenshot %}<img class="hero-pill-thumb off-glb" src="https://raw.githubusercontent.com/{{ slide.repo }}/refs/heads/main/ports/{{ slide.port_id }}/{{ slide.screenshot }}" alt="">{% endif %}
      <span class="hero-pill-body">
        <span class="hero-pill-title">{{ slide.title }}</span>
      </span>
    </button>
    {% endfor %}
  </div>
</div>
{% endif %}

{% set rtr_category = namespace(value=None) %}
{% set other_categories = [] %}
{% for category in featured_categories %}
  {% if category.name == 'Ready to Run' and rtr_category.value is none %}
    {% set rtr_category.value = category %}
  {% else %}
    {% set _ = other_categories.append(category) %}
  {% endif %}
{% endfor %}

{% set recent_keys = [] %}
{% set prev_month_ts = now().timestamp() - 2592000 %}
{% set thirty_days_ago_str = now().fromtimestamp(prev_month_ts).strftime('%Y-%m-%d') %}
{% for port_key in sorted_orders['date-added'] %}
  {% set port = ports['ports'][port_key] %}
  {% set source = port.source or {} %}
  {% set date_added = source.date_added or '' %}
  {% if date_added and date_added >= thirty_days_ago_str and recent_keys|length < 20 %}
    {% set _ = recent_keys.append(port_key) %}
  {% endif %}
{% endfor %}

<div class="featured-category featured-category--first">
  {{ carousel_block(1, 'Recently Added Ports', 'recentPortsCarousel', recent_keys) }}
</div>

<div class="featured-category">
  {{ carousel_block(1, 'Popular Ports', 'popularPortsCarousel', sorted_orders['downloads'][:20]) }}
</div>

{# A grid of image tiles, not another card carousel - a deliberate change
   of format partway down Discover so the page doesn't read as one long
   repeating list of the same carousel. #}
<div class="featured-category">
  <div class="carousel-section-header">
    <div class="carousel-section-title">
      <h1>Browse by Genre</h1>
      <a href="../games/#browse" class="see-all-inline"><span class="sr-only">See All</span> <i class="bi bi-chevron-right"></i></a>
    </div>
  </div>
  <div class="genre-tiles genre-tiles--preview">
    {% for genre in genre_list %}{{ genre_tile(genre) }}{% endfor %}
  </div>
</div>

{% if rtr_category.value %}
<div class="featured-category rtr-spotlight">
  <div class="featured-category-header">
    <h1><i class="bi bi-lightning-charge-fill"></i> {{ rtr_category.value.name }}</h1>
    {% if rtr_category.value.description %}<p>{{ rtr_category.value.description }}</p>{% endif %}
  </div>

  {% for group in rtr_category.value.groups %}
  {% set track_id = 'carousel-rtr-' ~ loop.index %}
  {{ carousel_block(2, group.name, track_id, group.ports) }}
  {% endfor %}
</div>
{% endif %}

{% for category in other_categories %}
{% set cat_index = loop.index %}
<div class="featured-category">
  <div class="featured-category-header">
    <h1>{{ category.name }}</h1>
    {% if category.description %}<p>{{ category.description }}</p>{% endif %}
  </div>

  {% for group in category.groups %}
  {% set track_id = 'carousel-' ~ cat_index ~ '-' ~ loop.index %}
  {{ carousel_block(2, group.name, track_id, group.ports) }}
  {% endfor %}
</div>
{% endfor %}

<div style="text-align: center; padding: 2rem; background: var(--md-code-bg-color); border-radius: 12px; margin: 2.5rem auto;">
  <h3 style="font-size: 1.5rem; margin: 0 0 1rem 0;">Looking for something specific?</h3>
  <p style="margin: 0 0 1.5rem 0;">Search, filter by device, genre, or requirements, and browse the full library of {{ total_port_count }} ports.</p>
  <button type="button" onclick="setView('browse')" class="md-button" style="display: inline-flex; align-items: center; gap: 0.5rem; border: none; cursor: pointer;">
    <i class="bi bi-search"></i> Browse All Games
  </button>
</div>

</div>

<div class="games-view" id="browse-view">

  <div class="genre-tiles" id="genreTiles">
    {% for genre in genre_list %}{{ genre_tile(genre) }}{% endfor %}
  </div>

  <div class="games-layout">
    <div class="games-main">
      <div class="filters-container">
        <div class="search-wrapper" style="justify-content: flex-end;">
          <div class="sort-dropdown-wrapper">
            <button class="sort-toggle-btn" id="sortToggleBtn">
              <i class="bi bi-sort-down"></i>
            </button>
            <div class="sort-dropdown" id="sortDropdown">
              <div class="sort-option" data-sort="az">A-Z</div>
              <div class="sort-option" data-sort="za">Z-A</div>
              <div class="sort-option selected" data-sort="downloads">Most Downloads</div>
              <div class="sort-option" data-sort="date-added">Date Added (Newest)</div>
              <div class="sort-option" data-sort="date-updated">Date Updated (Newest)</div>
            </div>
          </div>

          <div class="view-toggle-wrapper" id="viewToggleWrapper">
            <button class="view-toggle-btn active" id="gridViewBtn" title="Grid view" aria-label="Grid view">
              <i class="bi bi-grid-3x3-gap-fill"></i>
            </button>
            <button class="view-toggle-btn" id="listViewBtn" title="List view" aria-label="List view">
              <i class="bi bi-list-ul"></i>
            </button>
          </div>

          <button class="filter-toggle-btn" id="filterToggleBtn">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
        <p id="portsCounter">Showing: {{ total_port_count }} ports</p>
      </div>

      <div class="filter-overlay" id="filterOverlay"></div>

      <div class="game-grid" id="gameGrid"></div>

      <div class="pagination-container" id="paginationContainer">
        <p class="pagination-info" id="paginationInfo">Showing 1-100 of {{ total_port_count }}</p>

        <div class="pagination-controls" id="paginationControls">
          <button class="pagination-nav-btn" id="pageFirstBtn" title="First page" aria-label="First page">
            <i class="bi bi-chevron-bar-left"></i>
          </button>
          <button class="pagination-nav-btn" id="pagePrevBtn" title="Previous page" aria-label="Previous page">
            <i class="bi bi-chevron-left"></i>
          </button>
          <div class="pagination-pages" id="paginationPages"></div>
          <button class="pagination-nav-btn" id="pageNextBtn" title="Next page" aria-label="Next page">
            <i class="bi bi-chevron-right"></i>
          </button>
          <button class="pagination-nav-btn" id="pageLastBtn" title="Last page" aria-label="Last page">
            <i class="bi bi-chevron-bar-right"></i>
          </button>
        </div>

        <div class="page-size-wrapper">
          <label for="pageSizeSelect">Show</label>
          <select id="pageSizeSelect" class="page-size-select">
            <option value="50">50</option>
            <option value="100" selected>100</option>
            <option value="250">250</option>
            <option value="500">500</option>
            <option value="all">All</option>
          </select>
          <span>per page</span>
        </div>
      </div>
    </div>

    <!-- Filter Panel: static sidebar on desktop, slide-out drawer on mobile
         (same markup/JS, CSS-only repositioning - see games.css) -->
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
  </div>

</div>

<button class="back-to-top" id="backToTop">
  <i class="bi bi-arrow-up"></i>
</button>

<!-- Quick-view modal: reuses the same .port-hero / .port-stat-pills /
     .port-actions components as the standalone /port/#<id> page so the
     preview and the full page look identical. -->
<div id="portModal" class="modal">
  <div class="modal-content">
    <div class="port-hero">
      <span class="close" onclick="closeModal()">&times;</span>
      <img src="" alt="" class="port-hero-img off-glb" id="modal-screenshot">
    </div>

    <div class="port-body">
      <h1 class="port-title" id="modal-title"></h1>

      <div class="port-stat-pills">
        <div class="port-stat-pill">
          <i class="bi bi-download"></i>
          <div>
            <span class="port-stat-value" id="modal-stat-downloads">—</span>
            <span class="port-stat-label">Downloads</span>
          </div>
        </div>
        <div class="port-stat-pill">
          <i class="bi bi-person-workspace"></i>
          <div>
            <span class="port-stat-value" id="modal-stat-porter">—</span>
            <span class="port-stat-label">Porter</span>
          </div>
        </div>
        <div class="port-stat-pill" id="modal-stat-rtr-pill">
          <i class="bi bi-lightning-charge-fill" id="modal-stat-rtr-icon"></i>
          <div>
            <span class="port-stat-value" id="modal-stat-rtr">—</span>
            <span class="port-stat-label">Status</span>
          </div>
        </div>
      </div>

      <div class="port-description" id="modal-desc"></div>

      <div class="port-actions">
        <div class="download-warning" id="downloadWarning" style="display: none;">
          <i class="bi bi-exclamation-triangle"></i>
          <span>No device selected. This port may not be compatible with your device.</span>
        </div>
        <a href="#" class="modal-download-btn" id="modal-download-btn" onclick="handleDownload(event)">Download</a>
        <div class="port-store-links" id="modal-store-links" style="display:none"></div>
        <button type="button" class="device-filter-btn" id="modal-device-chip-btn" title="Check compatibility with your device">
          <span class="device-chip-dot" id="modal-device-chip-dot"></span>
          <i class="bi bi-controller"></i>
        </button>
        <button class="share-btn" id="modal-share-btn" onclick="sharePort(event)" title="Share port">
          <i class="bi bi-share"></i>
        </button>
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
  </div>
</div>

<script>
  // ===================================================================
  // Carousels (Discover view) - static markup, always in the DOM
  // ===================================================================
  // Each arrow click pages the whole row by one visible width, like the
  // Steam/Epic store carousels, rather than nudging by a single card.
  function scrollCarousel(trackId, direction) {
    const track = document.getElementById(trackId);
    if (!track) return;
    track.scrollBy({ left: direction * track.clientWidth, behavior: 'smooth' });
  }

  // ===================================================================
  // Discover hero banner: auto-rotates every HERO_DURATION ms; the active
  // pill's progress bar fill is what visually times the countdown, and
  // finishing that fill is what triggers the advance to the next slide.
  // ===================================================================
  (function initHeroBanner() {
    const banner = document.getElementById('heroBanner');
    if (!banner) return;

    const slides = banner.querySelectorAll('.hero-slide');
    const pills = banner.querySelectorAll('.hero-pill');
    if (slides.length < 2) return;

    const HERO_DURATION = 7000;
    let current = 0;
    let timer = null;

    function show(index) {
      current = index;
      slides.forEach((slide, i) => slide.classList.toggle('active', i === index));
      pills.forEach((pill, i) => {
        pill.classList.toggle('active', i === index);
        const bar = pill.querySelector('.hero-pill-progress');
        bar.style.animation = 'none';
        bar.style.width = '0';
        if (i === index) {
          // Restart the fill animation from empty every time this pill becomes active.
          void bar.offsetWidth;
          bar.style.animation = `heroPillFill ${HERO_DURATION}ms linear forwards`;
        }
      });
    }

    function goToNext() {
      show((current + 1) % slides.length);
      restart();
    }

    function restart() {
      clearTimeout(timer);
      timer = setTimeout(goToNext, HERO_DURATION);
    }

    pills.forEach((pill, i) => {
      pill.addEventListener('click', () => {
        show(i);
        restart();
      });
    });

    show(0);
    restart();
  })();

  // ===================================================================
  // Cookie helpers (shared with /port/ for device selection persistence)
  // ===================================================================
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

  function escapeHtml(value) {
    const div = document.createElement('div');
    div.textContent = value == null ? '' : value;
    return div.innerHTML;
  }

  // border-radius/overflow:hidden on <table> itself doesn't reliably clip
  // cell backgrounds across browsers, so wrap each table in a div and
  // round that instead (see .table-wrap in games.css).
  function wrapTables(container) {
    container.querySelectorAll('table').forEach(table => {
      if (table.parentElement.classList.contains('table-wrap')) return;
      const wrap = document.createElement('div');
      wrap.className = 'table-wrap';
      table.parentNode.insertBefore(wrap, table);
      wrap.appendChild(table);
    });
  }

  function storeIcon(name) {
    const n = (name || '').toLowerCase();
    if (n.includes('steam')) return 'bi-steam';
    if (n.includes('itch')) return 'bi-joystick';
    if (n.includes('gog')) return 'bi-shop-window';
    if (n.includes('epic')) return 'bi-controller';
    return 'bi-box-arrow-up-right';
  }

  function shortStoreName(name) {
    return (name || '').trim() || 'Store';
  }

  // ===================================================================
  // View switching (Discover / Browse) + search-bar routing
  // ===================================================================
  const discoverView = document.getElementById('discover-view');
  const browseView = document.getElementById('browse-view');
  const discoverTabBtn = document.getElementById('discoverTabBtn');
  const browseTabBtn = document.getElementById('browseTabBtn');
  const gamesSearchInput = document.getElementById('gamesSearchInput');

  function setView(view, opts = {}) {
    const isBrowse = view === 'browse';
    discoverView.classList.toggle('active', !isBrowse);
    browseView.classList.toggle('active', isBrowse);
    discoverTabBtn.classList.toggle('active', !isBrowse);
    browseTabBtn.classList.toggle('active', isBrowse);

    if (isBrowse) {
      if (!opts.skipHash) history.replaceState(null, '', '#browse');
      ensureBrowseData().then(() => {
        if (!opts.skipFilter) filterAndSearch();
      });
    } else if (!opts.skipHash) {
      history.replaceState(null, '', window.location.pathname);
    }
  }

  discoverTabBtn.addEventListener('click', () => setView('discover'));
  browseTabBtn.addEventListener('click', () => setView('browse'));

  let topSearchTimeout;
  gamesSearchInput.addEventListener('input', () => {
    if (!browseView.classList.contains('active')) {
      setView('browse', { skipFilter: true });
    }
    clearTimeout(topSearchTimeout);
    topSearchTimeout = setTimeout(() => ensureBrowseData().then(() => filterAndSearch()), 150);
  });

  // ===================================================================
  // Genre tiles (Browse view)
  // ===================================================================
  document.querySelectorAll('.genre-tile').forEach(tile => {
    tile.addEventListener('click', () => {
      const genre = tile.dataset.genre;
      setView('browse', { skipFilter: true });
      ensureBrowseData().then(() => {
        genreSelect.value = genre;
        if (genreSelect.updateCustomOptions) genreSelect.updateCustomOptions();
        if (genreSelect.customTrigger) genreSelect.customTrigger.textContent = genre;
        document.querySelectorAll('.genre-tile').forEach(t => t.classList.toggle('active', t === tile));
        setCookie('selectedGenre', genre);
        filterAndSearch();
        document.querySelector('.filters-container').scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  });

  // ===================================================================
  // Lazy data loading for the Browse grid
  // (port_details.json / device_info.json / runtime_archs.json are all
  // already-built static files - see main.py - so Browse never needs a
  // server-rendered 1300+ card loop at build time.)
  // ===================================================================
  let allPorts = null;
  let portsById = {};
  let devices = {};
  let runtimeAvailability = {};
  let fuse = null;
  let dataLoadPromise = null;

  function ensureBrowseData() {
    if (dataLoadPromise) return dataLoadPromise;
    dataLoadPromise = Promise.all([
      fetch('../assets/json/port_details.json').then(r => r.json()),
      fetch('../assets/json/device_info.json').then(r => r.json()).catch(() => ({})),
      fetch('../assets/json/runtime_archs.json').then(r => r.json()).catch(() => ({}))
    ]).then(([details, deviceInfo, runtimeArchs]) => {
      devices = deviceInfo;
      Object.entries(runtimeArchs).forEach(([runtime, list]) => {
        runtimeAvailability[runtime] = (list || []).map(a => a.toLowerCase());
      });
      allPorts = Object.entries(details).map(([id, p]) => ({ id, ...p }));
      allPorts.forEach(p => { portsById[p.id] = p; });
      initBrowseUI();
    });
    return dataLoadPromise;
  }

  // ===================================================================
  // Browse controls (static markup, present in the DOM from page load)
  // ===================================================================
  const deviceSelect = document.getElementById('deviceSelect');
  const osSelect = document.getElementById('osSelect');
  const genreSelect = document.getElementById('genreSelect');
  const readyToggle = document.getElementById('readyToggle');
  const hideIncompatibleToggle = document.getElementById('hideIncompatibleToggle');
  const gameGrid = document.getElementById('gameGrid');
  const gridViewBtn = document.getElementById('gridViewBtn');
  const listViewBtn = document.getElementById('listViewBtn');
  const pageSizeSelect = document.getElementById('pageSizeSelect');
  const paginationInfo = document.getElementById('paginationInfo');
  const paginationPages = document.getElementById('paginationPages');
  const pageFirstBtn = document.getElementById('pageFirstBtn');
  const pagePrevBtn = document.getElementById('pagePrevBtn');
  const pageNextBtn = document.getElementById('pageNextBtn');
  const pageLastBtn = document.getElementById('pageLastBtn');

  const filterToggleBtn = document.getElementById('filterToggleBtn');
  const filterPanel = document.getElementById('filterPanel');
  const filterOverlay = document.getElementById('filterOverlay');
  const closePanelBtn = document.getElementById('closePanelBtn');

  const sortToggleBtn = document.getElementById('sortToggleBtn');
  const sortDropdown = document.getElementById('sortDropdown');
  const sortOptions = document.querySelectorAll('.sort-option');

  let currentDevice = null;
  let currentOS = null;
  let currentSort = 'downloads';
  let currentPortId = null;
  let currentPortData = null;
  let readmeCache = {};
  let viewMode = 'grid';
  let pageSize = 100;
  let currentPage = 1;
  let selectedRuntimes = new Set();
  let selectedArchs = new Set();
  let selectedReqs = new Set();
  let sortedCache = {};
  let browseUIInitialized = false;

  function getSortedIds(mode) {
    if (sortedCache[mode]) return sortedCache[mode];
    const arr = allPorts.slice();
    if (mode === 'az') arr.sort((a, b) => a.title.localeCompare(b.title));
    else if (mode === 'za') arr.sort((a, b) => b.title.localeCompare(a.title));
    else if (mode === 'date-updated') arr.sort((a, b) => (b.dateUpdated || '').localeCompare(a.dateUpdated || ''));
    else if (mode === 'date-added') arr.sort((a, b) => (b.dateAdded || '').localeCompare(a.dateAdded || ''));
    else arr.sort((a, b) => b.downloads - a.downloads);
    sortedCache[mode] = arr.map(p => p.id);
    return sortedCache[mode];
  }

  function initBrowseUI() {
    if (browseUIInitialized) return;
    browseUIInitialized = true;

    fuse = new Fuse(allPorts, {
      keys: [{ name: 'title', weight: 0.6 }, { name: 'genres', weight: 0.1 }],
      threshold: 0.4
    });

    // Populate genre dropdown
    const allGenres = new Set(allPorts.flatMap(p => p.genres || []));
    [...allGenres].sort().forEach(g => genreSelect.appendChild(new Option(g, g)));

    // Populate advanced filter pills
    const runtimePills = document.getElementById('runtimePills');
    const archPills = document.getElementById('archPills');
    const reqPills = document.getElementById('reqPills');

    function createPill(value, container, selectedSet) {
      const pill = document.createElement('span');
      pill.className = 'filter-pill';
      pill.textContent = value;
      pill.dataset.value = value;
      pill.addEventListener('click', () => {
        pill.classList.toggle('selected');
        if (pill.classList.contains('selected')) selectedSet.add(value);
        else selectedSet.delete(value);
        filterAndSearch();
      });
      container.appendChild(pill);
    }

    [...new Set(allPorts.flatMap(p => p.runtime || []))].sort().forEach(r => createPill(r, runtimePills, selectedRuntimes));
    [...new Set(allPorts.flatMap(p => p.arch || []))].sort().forEach(a => createPill(a, archPills, selectedArchs));
    [...new Set(allPorts.flatMap(p => p.reqs || []))].sort().forEach(r => createPill(r, reqPills, selectedReqs));

    // Populate device dropdown
    Object.keys(devices).forEach(deviceName => deviceSelect.appendChild(new Option(deviceName, deviceName)));

    initializeCustomSelects();
    restoreViewAndPaging();
    restoreSavedFilters();
  }

  function toggleAdvancedFilters() {
    document.getElementById('advancedFiltersContent').classList.toggle('open');
    document.getElementById('advancedArrow').classList.toggle('open');
  }

  function clearAdvancedFilters() {
    selectedRuntimes.clear();
    selectedArchs.clear();
    selectedReqs.clear();
    document.querySelectorAll('.filter-pill.selected').forEach(pill => pill.classList.remove('selected'));
    filterAndSearch();
  }

  function clearAllFilters() {
    clearAdvancedFilters();

    deviceSelect.value = '';
    if (deviceSelect.customTrigger) deviceSelect.customTrigger.textContent = 'Select your device...';
    currentDevice = null;

    osSelect.innerHTML = '<option value="">Select OS...</option>';
    osSelect.disabled = true;
    if (osSelect.customTrigger) osSelect.customTrigger.textContent = 'Select OS...';
    if (osSelect.customWrapper) osSelect.customWrapper.querySelector('.custom-select-trigger').classList.add('disabled');
    currentOS = null;

    genreSelect.value = '';
    if (genreSelect.customTrigger) genreSelect.customTrigger.textContent = 'All Genres';
    document.querySelectorAll('.genre-tile.active').forEach(t => t.classList.remove('active'));

    readyToggle.checked = false;
    hideIncompatibleToggle.checked = false;
    gamesSearchInput.value = '';

    setCookie('selectedDevice', '', -1);
    setCookie('selectedOS', '', -1);
    setCookie('selectedGenre', '', -1);
    setCookie('readyToggle', '', -1);
    setCookie('hideIncompatible', '', -1);

    filterAndSearch();
  }

  // ===== Back to Top =====
  const backToTopBtn = document.getElementById('backToTop');
  window.addEventListener('scroll', () => backToTopBtn.classList.toggle('visible', window.scrollY > 500));
  backToTopBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // ===== Sort dropdown =====
  sortToggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    sortDropdown.classList.toggle('open');
  });
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.sort-dropdown-wrapper')) sortDropdown.classList.remove('open');
  });
  sortOptions.forEach(option => {
    option.addEventListener('click', () => {
      sortOptions.forEach(opt => opt.classList.remove('selected'));
      option.classList.add('selected');
      currentSort = option.dataset.sort;
      sortDropdown.classList.remove('open');
      filterAndSearch();
    });
  });

  // ===== View mode (grid / list) =====
  function setViewMode(mode) {
    viewMode = mode;
    gridViewBtn.classList.toggle('active', mode === 'grid');
    listViewBtn.classList.toggle('active', mode === 'list');
    setCookie('viewMode', mode);
    if (allPorts) filterAndSearch(false);
  }
  gridViewBtn.addEventListener('click', () => setViewMode('grid'));
  listViewBtn.addEventListener('click', () => setViewMode('list'));

  // ===== Page size =====
  pageSizeSelect.addEventListener('change', () => {
    pageSize = pageSizeSelect.value === 'all' ? 'all' : parseInt(pageSizeSelect.value);
    setCookie('pageSize', pageSizeSelect.value);
    filterAndSearch();
  });

  function restoreViewAndPaging() {
    const savedView = getCookie('viewMode');
    if (savedView === 'list') setViewMode('list');

    const savedPageSize = getCookie('pageSize');
    if (savedPageSize && pageSizeSelect.querySelector(`option[value="${savedPageSize}"]`)) {
      pageSizeSelect.value = savedPageSize;
      pageSize = savedPageSize === 'all' ? 'all' : parseInt(savedPageSize);
    }
  }

  // ===== Filter panel open/close (drawer on mobile, static on desktop) =====
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
    filterPanel.classList.contains('open') ? closeFilterPanel() : openFilterPanel();
  });
  closePanelBtn.addEventListener('click', closeFilterPanel);
  filterOverlay.addEventListener('click', closeFilterPanel);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && filterPanel.classList.contains('open')) closeFilterPanel();
  });

  // ===== Device / OS selects =====
  deviceSelect.addEventListener('change', e => {
    const deviceName = e.target.value;
    currentDevice = deviceName ? devices[deviceName] : null;
    setCookie('selectedDevice', deviceName || '', deviceName ? 365 : -1);

    osSelect.innerHTML = '<option value="">Select OS...</option>';
    if (currentDevice) {
      const osNames = Object.keys(currentDevice);
      osNames.forEach(osName => osSelect.appendChild(new Option(osName, osName)));
      osSelect.disabled = false;

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
      if (osSelect.updateCustomOptions) osSelect.updateCustomOptions();
      if (osSelect.customWrapper) {
        osSelect.customWrapper.querySelector('.custom-select-trigger').classList.add('disabled');
        if (osSelect.customTrigger) osSelect.customTrigger.textContent = 'Select OS...';
      }
    }
    updateModalDeviceChip();
    filterAndSearch();
  });

  osSelect.addEventListener('change', e => {
    const selectedOS = e.target.value;
    currentOS = selectedOS && currentDevice ? currentDevice[selectedOS] : null;
    setCookie('selectedOS', selectedOS || '', selectedOS ? 365 : -1);
    updateModalDeviceChip();
    filterAndSearch();
  });

  genreSelect.addEventListener('change', () => {
    setCookie('selectedGenre', genreSelect.value);
    document.querySelectorAll('.genre-tile').forEach(t => t.classList.toggle('active', t.dataset.genre === genreSelect.value));
    filterAndSearch();
  });

  readyToggle.addEventListener('change', () => {
    setCookie('readyToggle', readyToggle.checked ? 'true' : '');
    filterAndSearch();
  });
  hideIncompatibleToggle.addEventListener('change', () => {
    setCookie('hideIncompatible', hideIncompatibleToggle.checked ? 'true' : '');
    filterAndSearch();
  });

  function restoreSavedFilters() {
    const savedGenre = getCookie('selectedGenre');
    if (savedGenre) {
      genreSelect.value = savedGenre;
      if (genreSelect.customTrigger) genreSelect.customTrigger.textContent = genreSelect.options[genreSelect.selectedIndex]?.text || 'All Genres';
      document.querySelectorAll('.genre-tile').forEach(t => t.classList.toggle('active', t.dataset.genre === savedGenre));
    }

    if (getCookie('readyToggle') === 'true') readyToggle.checked = true;
    if (getCookie('hideIncompatible') === 'true') hideIncompatibleToggle.checked = true;

    const savedDevice = getCookie('selectedDevice');
    if (savedDevice && devices[savedDevice]) {
      deviceSelect.value = savedDevice;
      if (deviceSelect.customTrigger) deviceSelect.customTrigger.textContent = savedDevice;
      deviceSelect.dispatchEvent(new Event('change'));
    }
  }

  // ===== Compatibility check =====
  function checkCompatibility(port) {
    if (!currentDevice || !currentOS) return true;

    const capabilities = new Set((currentOS.capabilities || []).map(c => c.toLowerCase()));
    const primaryArch = (currentOS.primary_arch || '').toLowerCase();

    if (!port.arch || port.arch.length === 0) {
      if (port.runtime && port.runtime.length > 0) {
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
      if (!hasArch) hasArch = requiredArches.some(arch => capabilities.has(arch));
      if (!hasArch) return false;
    }

    for (const req of (port.reqs || [])) {
      const reqLower = req.toLowerCase();
      if (reqLower.startsWith('!')) {
        if (capabilities.has(reqLower.slice(1))) return false;
      } else if (reqLower.startsWith('power:')) {
        continue;
      } else if (reqLower.includes('|')) {
        if (!reqLower.split('|').map(o => o.trim()).some(opt => capabilities.has(opt))) return false;
      } else if (!capabilities.has(reqLower)) {
        return false;
      }
    }
    return true;
  }

  // ===== Filter + search + render =====
  function filterAndSearch(resetPage = true) {
    if (!allPorts) return;

    const query = gamesSearchInput.value.trim();
    const selectedGenre = genreSelect.value;
    const readyOnly = readyToggle.checked;
    const hideIncompatible = hideIncompatibleToggle.checked;
    const searchMatches = query ? new Set(fuse.search(query).map(r => r.item.id)) : null;

    let supported = 0, unsupported = 0;
    const order = getSortedIds(currentSort);
    const matchedIds = [];

    order.forEach(id => {
      const port = portsById[id];
      if (!port) return;

      const matchSearch = !searchMatches || searchMatches.has(id);
      const genreMatch = !selectedGenre || (port.genres || []).includes(selectedGenre);
      const rtrMatch = !readyOnly || port.rtr;
      const compatible = checkCompatibility(port);
      const runtimeMatch = selectedRuntimes.size === 0 || (port.runtime || []).some(r => selectedRuntimes.has(r));
      const archMatch = selectedArchs.size === 0 || (port.arch || []).some(a => selectedArchs.has(a));
      const reqMatch = selectedReqs.size === 0 || (port.reqs || []).some(r => selectedReqs.has(r));

      if (currentOS) {
        if (compatible) supported++; else unsupported++;
      }

      let shouldShow = matchSearch && genreMatch && rtrMatch && runtimeMatch && archMatch && reqMatch;
      if (currentOS && hideIncompatible) shouldShow = shouldShow && compatible;

      if (shouldShow) {
        port.incompatibleFlag = currentOS && !compatible && !hideIncompatible;
        matchedIds.push(id);
      }
    });

    if (resetPage) currentPage = 1;
    renderPage(matchedIds, supported, unsupported);
  }

  function renderCardHtml(port) {
    const rtrBadge = port.rtr ? '<span class="pm-rtr-badge"><i class="bi bi-lightning-charge-fill"></i> RTR</span>' : '';
    const img = port.screenshot
      ? `<img src="https://raw.githubusercontent.com/${port.repo}/refs/heads/main/ports/${port.id}/${port.screenshot}" alt="${escapeHtml(port.title)}" loading="lazy" onerror="this.style.display='none'">`
      : '';
    const downloadsText = port.downloads > 0 ? port.downloads.toLocaleString() : '—';
    const cls = 'pm-card' + (port.incompatibleFlag ? ' incompatible' : '');
    return `<div class="${cls}" data-port-id="${port.id}">${rtrBadge}${img}<h3>${escapeHtml(port.title)}</h3><div class="card-stats"><span class="card-stat"><i class="bi bi-download"></i> ${downloadsText}</span><span class="card-stat"><i class="bi bi-calendar-plus"></i> ${port.dateAdded || '—'}</span></div></div>`;
  }

  function renderPage(matchedIds, supported = 0, unsupported = 0) {
    const total = matchedIds.length;
    const effectivePageSize = pageSize === 'all' ? Math.max(total, 1) : pageSize;
    const totalPages = Math.max(1, Math.ceil(total / effectivePageSize));

    if (currentPage > totalPages) currentPage = totalPages;
    if (currentPage < 1) currentPage = 1;

    const startIdx = (currentPage - 1) * effectivePageSize;
    const endIdx = Math.min(startIdx + effectivePageSize, total);
    const pageIds = matchedIds.slice(startIdx, endIdx);

    gameGrid.classList.toggle('list-view', viewMode === 'list');
    gameGrid.innerHTML = pageIds.map(id => renderCardHtml(portsById[id])).join('');

    const counterEl = document.getElementById('portsCounter');
    counterEl.textContent = currentOS
      ? `Supported: ${supported} | Unsupported: ${unsupported} | Showing: ${total}`
      : `Showing: ${total} of ${allPorts.length} ports`;

    paginationInfo.textContent = total === 0 ? 'No ports match your filters' : `Showing ${startIdx + 1}-${endIdx} of ${total}`;
    renderPaginationControls(totalPages);
  }

  function goToPage(page) {
    currentPage = page;
    filterAndSearch(false);
    document.querySelector('.filters-container').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function getPageNumberList(current, total) {
    if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);
    const pages = new Set([1, total, current, current - 1, current + 1, current - 2, current + 2]);
    const sorted = [...pages].filter(p => p >= 1 && p <= total).sort((a, b) => a - b);
    const result = [];
    let prev = null;
    sorted.forEach(p => {
      if (prev !== null && p - prev > 1) result.push('...');
      result.push(p);
      prev = p;
    });
    return result;
  }

  function renderPaginationControls(totalPages) {
    pageFirstBtn.disabled = currentPage <= 1;
    pagePrevBtn.disabled = currentPage <= 1;
    pageNextBtn.disabled = currentPage >= totalPages;
    pageLastBtn.disabled = currentPage >= totalPages;

    paginationPages.innerHTML = '';
    getPageNumberList(currentPage, totalPages).forEach(p => {
      if (p === '...') {
        const span = document.createElement('span');
        span.className = 'pagination-ellipsis';
        span.textContent = '…';
        paginationPages.appendChild(span);
        return;
      }
      const btn = document.createElement('button');
      btn.className = 'pagination-page-btn' + (p === currentPage ? ' active' : '');
      btn.textContent = p;
      btn.addEventListener('click', () => goToPage(p));
      paginationPages.appendChild(btn);
    });
  }

  pageFirstBtn.addEventListener('click', () => goToPage(1));
  pagePrevBtn.addEventListener('click', () => goToPage(Math.max(1, currentPage - 1)));
  pageNextBtn.addEventListener('click', () => goToPage(currentPage + 1));
  pageLastBtn.addEventListener('click', () => goToPage(Number.MAX_SAFE_INTEGER));

  // ===== Grid click delegation: left-click = quick-view modal,
  // right-click / middle-click = jump to the full /port/ page =====
  gameGrid.addEventListener('click', (e) => {
    const card = e.target.closest('.pm-card');
    if (!card) return;
    openModal(card.dataset.portId);
  });
  gameGrid.addEventListener('contextmenu', (e) => {
    const card = e.target.closest('.pm-card');
    if (!card) return;
    e.preventDefault();
    window.location.href = `../port/#${card.dataset.portId}`;
  });
  gameGrid.addEventListener('auxclick', (e) => {
    if (e.button !== 1) return;
    const card = e.target.closest('.pm-card');
    if (!card) return;
    e.preventDefault();
    window.open(`../port/#${card.dataset.portId}`, '_blank');
  });

  // ===================================================================
  // Quick-view modal
  // ===================================================================
  function renderModal(portId) {
    const port = portsById[portId];
    if (!port) return;

    currentPortId = portId;
    currentPortData = port;

    document.getElementById('modal-title').textContent = port.title;

    const screenshotImg = document.getElementById('modal-screenshot');
    const heroWrap = screenshotImg.closest('.port-hero');
    if (port.screenshot) {
      screenshotImg.src = `https://raw.githubusercontent.com/${port.repo}/refs/heads/main/ports/${portId}/${port.screenshot}`;
      screenshotImg.alt = port.title;
      heroWrap.style.display = '';
    } else {
      heroWrap.style.display = 'none';
    }

    const descEl = document.getElementById('modal-desc');
    descEl.innerHTML = port.descHtml || '';
    wrapTables(descEl);

    document.getElementById('modal-stat-downloads').textContent = port.downloads > 0 ? port.downloads.toLocaleString() : 'N/A';
    document.getElementById('modal-stat-porter').textContent = port.porter && port.porter.length
      ? (port.porter.length > 1 ? `${port.porter[0]} +${port.porter.length - 1}` : port.porter[0])
      : 'Unknown';
    document.getElementById('modal-stat-rtr').textContent = port.rtr ? 'Ready to Run' : 'Setup Required';
    const rtrPill = document.getElementById('modal-stat-rtr-pill');
    const rtrIcon = document.getElementById('modal-stat-rtr-icon');
    rtrPill.classList.toggle('port-stat-pill--warn', !port.rtr);
    rtrIcon.className = port.rtr ? 'bi bi-lightning-charge-fill' : 'bi bi-tools';

    const storeWrap = document.getElementById('modal-store-links');
    if (port.store && port.store.length) {
      storeWrap.innerHTML = port.store
        .map(s => `<a href="${s.url}" target="_blank" rel="noopener" class="port-store-link" title="${escapeHtml(shortStoreName(s.name))}"><i class="bi ${storeIcon(s.name)}"></i> <span class="port-store-label">${escapeHtml(shortStoreName(s.name))}</span></a>`)
        .join('');
      storeWrap.style.display = '';
    } else {
      storeWrap.innerHTML = '';
      storeWrap.style.display = 'none';
    }

    const downloadBtn = document.getElementById('modal-download-btn');
    downloadBtn.href = port.url || '#';
    updateDownloadButton();

    const makeBadges = arr => arr && arr.length > 0 ? arr.map(v => `<span class="info-badge">${escapeHtml(v)}</span>`).join('') : '—';
    const makePorterLinks = arr => arr && arr.length > 0
      ? arr.map(v => `<a href="../porters/#porter-${encodeURIComponent(v)}" class="porter-link-badge" onclick="event.stopPropagation()">${escapeHtml(v)} <i class="bi bi-box-arrow-up-right"></i></a>`).join(' ')
      : '—';

    document.getElementById('modal-genres').innerHTML = makeBadges(port.genres);
    document.getElementById('modal-reqs').innerHTML = makeBadges(port.reqs);
    document.getElementById('modal-porter').innerHTML = makePorterLinks(port.porter);
    document.getElementById('modal-downloads').textContent = port.downloads > 0 ? port.downloads.toLocaleString() : 'N/A';
    document.getElementById('modal-runtimes').innerHTML = makeBadges(port.runtime);
    document.getElementById('modal-arch').innerHTML = makeBadges(port.arch);
    document.getElementById('modal-date-added').textContent = port.dateAdded || 'N/A';
    document.getElementById('modal-date-updated').textContent = port.dateUpdated || 'N/A';
    document.getElementById('modal-misc').innerHTML = port.rtr
      ? '<span class="info-badge">Ready to Run</span>'
      : '<span class="info-badge">Setup Required</span>';

    const instSection = document.getElementById('modal-inst-section');
    const instEl = document.getElementById('modal-inst');
    if (port.instHtml) {
      instEl.innerHTML = port.instHtml;
      wrapTables(instEl);
      instSection.style.display = '';
    } else {
      instSection.style.display = 'none';
    }

    loadReadme(portId, port.repo);
    updateModalDeviceChip();

    const modal = document.getElementById('portModal');
    modal.style.display = 'block';
    modal.offsetHeight;
    modal.classList.add('show');
  }

  function openModal(portId) {
    renderModal(portId);
    if (currentPortId) history.pushState({ modal: portId }, '', '#modal-' + portId);
  }

  function openModalDirect(portId) {
    renderModal(portId);
  }

  function closeModal(updateHistory = true) {
    const modal = document.getElementById('portModal');
    modal.classList.remove('show');
    setTimeout(() => { modal.style.display = 'none'; }, 300);
    currentPortId = null;
    currentPortData = null;

    if (updateHistory && window.location.hash.startsWith('#modal-')) {
      history.pushState({ modal: null }, '', '#browse');
    }
  }

  window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) closeModal();
  });

  window.addEventListener('popstate', () => {
    const hash = window.location.hash;
    if (hash.startsWith('#modal-')) {
      const portId = decodeURIComponent(hash.replace('#modal-', ''));
      setView('browse', { skipHash: true, skipFilter: true });
      ensureBrowseData().then(() => { if (portsById[portId]) openModalDirect(portId); });
    } else {
      closeModal(false);
      setView(hash === '#browse' ? 'browse' : 'discover', { skipHash: true });
    }
  });

  // ===== Download button =====
  function getSelectedDeviceName() {
    return deviceSelect.value || null;
  }

  function updateDownloadButton() {
    const downloadBtn = document.getElementById('modal-download-btn');
    const deviceName = getSelectedDeviceName();
    if (downloadBtn) downloadBtn.textContent = deviceName ? `Download for ${deviceName}` : 'Download';
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
        if (warningText) warningText.textContent = `This port is not compatible with ${deviceName}. Download blocked.`;
        if (warningIcon) warningIcon.className = 'bi bi-x-circle';
        warningDiv.classList.add('error');
        warningDiv.classList.remove('fade-out');
        warningDiv.style.display = 'flex';
        setTimeout(() => {
          warningDiv.classList.add('fade-out');
          setTimeout(() => {
            warningDiv.style.display = 'none';
            warningDiv.classList.remove('fade-out', 'error');
            if (warningText) warningText.textContent = 'No device selected. This port may not be compatible with your device.';
            if (warningIcon) warningIcon.className = 'bi bi-exclamation-triangle';
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

  // ===== Modal device-compatibility chip: opens the shared filter panel
  // (sidebar/drawer) rather than duplicating its own device/OS selects. =====
  const modalDeviceChipBtn = document.getElementById('modal-device-chip-btn');
  const modalDeviceChipDot = document.getElementById('modal-device-chip-dot');

  function updateModalDeviceChip() {
    if (!currentPortData) return;
    if (!currentDevice || !currentOS) {
      modalDeviceChipDot.className = 'device-chip-dot';
      modalDeviceChipBtn.title = 'Check compatibility with your device';
      return;
    }
    const compatible = checkCompatibility(currentPortData);
    modalDeviceChipDot.className = 'device-chip-dot ' + (compatible ? 'is-compatible' : 'is-incompatible');
    modalDeviceChipBtn.title = compatible ? 'Compatible with your device' : 'May not be compatible with your device';
  }

  modalDeviceChipBtn.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    openFilterPanel();
  });

  // ===== Share =====
  async function sharePort(event) {
    event.preventDefault();
    event.stopPropagation();
    if (!currentPortId || !currentPortData) return;

    const shareUrl = `${window.location.origin}${window.location.pathname}#modal-${currentPortId}`;
    const shareData = {
      title: currentPortData.title,
      text: `Check out ${currentPortData.title} on PortMaster!`,
      url: shareUrl
    };

    if (navigator.share) {
      try {
        await navigator.share(shareData);
      } catch (err) {
        if (err.name !== 'AbortError') console.error('Share failed:', err);
      }
      return;
    }

    try {
      await navigator.clipboard.writeText(shareUrl);
      showShareConfirmation(event.target);
    } catch (err) {
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

  // ===== README (live-fetched + client-parsed; desc/inst are pre-rendered
  // server-side already, in port_details.json) =====
  async function loadReadme(portId, repo) {
    const readmeEl = document.getElementById('modal-readme');
    if (readmeCache[portId]) {
      readmeEl.innerHTML = readmeCache[portId];
      wrapTables(readmeEl);
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
        wrapTables(readmeEl);
      }
    } catch (err) {
      const fallback = '<p>No additional information available.</p>';
      readmeCache[portId] = fallback;
      if (currentPortId === portId) readmeEl.innerHTML = fallback;
    }
  }

  // ===== Custom select styling (device / OS / genre dropdowns) =====
  function initializeCustomSelects() {
    [deviceSelect, osSelect, genreSelect].forEach(select => {
      if (select.customWrapper) return;

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
        document.querySelectorAll('.custom-select-wrapper.open').forEach(w => { if (w !== wrapper) w.classList.remove('open'); });
        wrapper.classList.toggle('open');
      });

      document.addEventListener('click', (e) => {
        if (!wrapper.contains(e.target)) wrapper.classList.remove('open');
      });

      select.customWrapper = wrapper;
      select.customTrigger = triggerText;
      select.updateCustomOptions = updateOptions;
    });
  }

  // ===================================================================
  // Initial route: #browse -> Browse view, #modal-<id> -> Browse + modal,
  // anything else -> Discover (default, matches the static HTML classes).
  // ===================================================================
  (function initFromHash() {
    const hash = window.location.hash;
    if (hash === '#browse') {
      setView('browse', { skipHash: true });
    } else if (hash.startsWith('#modal-')) {
      const portId = decodeURIComponent(hash.replace('#modal-', ''));
      setView('browse', { skipHash: true, skipFilter: true });
      ensureBrowseData().then(() => { if (portsById[portId]) openModalDirect(portId); });
    }
  })();
</script>
