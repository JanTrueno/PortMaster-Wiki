---
hide:
  - navigation
  - toc
  - path

search:
  exclude: true

# Every card image on this page is JS-rendered client-side (not present in
# the static build-time HTML at all) and every other <img> already carries
# off-glb, so glightbox has zero images to actually wrap here - but it
# still regex-scans the entire rendered page including the large embedded
# ports_text_json data blob to check, which is pathologically slow on a
# page this size (multiple minutes, dominating the whole site build).
# Skipping the plugin outright for this page removes that cost with no
# loss of functionality.
glightbox: false
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
  <div class="pm-card" data-port-id="{{ port_id }}" onclick="window.location.href='../port/?name={{ port_id }}'">
    {% if attr.rtr %}<span class="pm-rtr-badge">RTR</span>{% endif %}
    {% if screenshot %}
    <img class="off-glb" src="https://raw.githubusercontent.com/{{ repo_owner }}/{{ repo_name }}/refs/heads/main/ports/{{ port_id }}/{{ screenshot }}"
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
          <a href="../port/?name={{ slide.port_id }}" class="hero-details-link">View Details <i class="bi bi-chevron-right"></i></a>
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
    </div>
    <div class="carousel-nav genre-carousel-nav">
      <a href="../games/#browse" class="see-all-inline"><span class="sr-only">See All</span> <i class="bi bi-chevron-right"></i></a>
      <div class="carousel-btn-group">
        <button class="carousel-btn carousel-btn-left" onclick="scrollCarousel('genreTilesPreview', -1)">
          <i class="bi bi-chevron-left"></i>
        </button>
        <button class="carousel-btn carousel-btn-right" onclick="scrollCarousel('genreTilesPreview', 1)">
          <i class="bi bi-chevron-right"></i>
        </button>
      </div>
    </div>
  </div>
  <div class="genre-tiles genre-tiles--preview" id="genreTilesPreview">
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
        <!-- Left: sort trigger + active-filter chips, Epic-style (chip
             sits right next to "Show:", not off with the counter). Right:
             the two things Epic doesn't have - the result counter and the
             grid/list view toggle - grouped together so they wrap onto a
             new line as one unit on narrow phones instead of the view
             icons getting stranded below everything else. -->
        <div class="filters-left">
          <span class="sort-label">Show:</span>
          <div class="sort-dropdown-wrapper">
            <button class="sort-toggle-btn" id="sortToggleBtn">
              <span id="sortCurrentLabel">Most Downloads</span>
              <i class="bi bi-chevron-down"></i>
            </button>
            <div class="sort-dropdown" id="sortDropdown">
              <div class="sort-option" data-sort="az">A-Z</div>
              <div class="sort-option" data-sort="za">Z-A</div>
              <div class="sort-option selected" data-sort="downloads">Most Downloads</div>
              <div class="sort-option" data-sort="date-added">Date Added (Newest)</div>
              <div class="sort-option" data-sort="date-updated">Date Updated (Newest)</div>
            </div>
          </div>
          <div class="active-filters-row" id="activeFiltersRow" style="display:none"></div>
        </div>

        <div class="filters-right">
          <p id="portsCounter">Showing: {{ total_port_count }} ports</p>
          <div class="search-wrapper">
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
        </div>
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
         (same markup/JS, CSS-only repositioning - see games-filters.css) -->
    <div class="filter-panel" id="filterPanel">
      <div class="filter-panel-header">
        <h2>Filters <span class="filter-count-badge" id="filterActiveCount" style="display:none">(0)</span></h2>
        <div class="filter-panel-header-actions">
          <button type="button" class="filter-reset-link" id="filterResetBtn" onclick="clearAllFilters()">Reset</button>
          <button class="close-panel-btn" id="closePanelBtn">&times;</button>
        </div>
      </div>

      <div class="filter-accordion open">
        <div class="filter-accordion-summary" role="button" tabindex="0">
          <span>Device</span>
          <i class="bi bi-chevron-down accordion-chevron"></i>
        </div>
        <div class="filter-accordion-body">
          <div class="filter-radio-list" id="deviceRadioList"></div>
        </div>
      </div>

      <div class="filter-accordion open">
        <div class="filter-accordion-summary" role="button" tabindex="0">
          <span>Operating System</span>
          <i class="bi bi-chevron-down accordion-chevron"></i>
        </div>
        <div class="filter-accordion-body">
          <div class="filter-radio-list" id="osRadioList"></div>
        </div>
      </div>

      <div class="filter-accordion open">
        <div class="filter-accordion-summary" role="button" tabindex="0">
          <span>Genre</span>
          <i class="bi bi-chevron-down accordion-chevron"></i>
        </div>
        <div class="filter-accordion-body">
          <div class="filter-checkbox-list" id="genreCheckboxList"></div>
        </div>
      </div>

      <div class="filter-accordion open">
        <div class="filter-accordion-summary" role="button" tabindex="0">
          <span>Options</span>
          <i class="bi bi-chevron-down accordion-chevron"></i>
        </div>
        <div class="filter-accordion-body">
          <label class="filter-checkbox-item">
            <input type="checkbox" id="readyToggle">
            <span>Ready to Run Only</span>
          </label>
          <label class="filter-checkbox-item">
            <input type="checkbox" id="hideIncompatibleToggle">
            <span>Hide Incompatible</span>
          </label>
        </div>
      </div>

      <div class="filter-accordion">
        <div class="filter-accordion-summary" role="button" tabindex="0">
          <span>Advanced</span>
          <i class="bi bi-chevron-down accordion-chevron"></i>
        </div>
        <div class="filter-accordion-body">
          <div class="filter-subgroup">
            <label>Runtime</label>
            <div class="filter-checkbox-list" id="runtimePills"></div>
          </div>

          <div class="filter-subgroup">
            <label>Architecture</label>
            <div class="filter-checkbox-list" id="archPills"></div>
          </div>

          <div class="filter-subgroup">
            <label>Requirements</label>
            <div class="filter-checkbox-list" id="reqPills"></div>
          </div>
        </div>
      </div>
    </div>
  </div>

</div>

<button class="back-to-top" id="backToTop">
  <i class="bi bi-arrow-up"></i>
</button>

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
  // round that instead (see .table-wrap in shared-modal.css).
  function wrapTables(container) {
    container.querySelectorAll('table').forEach(table => {
      if (table.parentElement.classList.contains('table-wrap')) return;
      const wrap = document.createElement('div');
      wrap.className = 'table-wrap';
      table.parentNode.insertBefore(wrap, table);
      wrap.appendChild(table);
    });
  }

  // Bootstrap Icons ships a real brand glyph for Steam only; GOG/other
  // storefronts fall back to a generic icon. Epic Games gets its actual
  // logo too, inlined as SVG (Simple Icons' path, CC0) since Bootstrap
  // Icons has no Epic glyph at all - falling back to a generic icon there
  // would leave Epic looking unbranded next to Steam.
  const EPIC_GAMES_SVG = '<svg class="store-icon-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M3.537 0C2.165 0 1.66.506 1.66 1.879V18.44a4.262 4.262 0 00.02.433c.031.3.037.59.316.92.027.033.311.245.311.245.153.075.258.13.43.2l8.335 3.491c.433.199.614.276.928.27h.002c.314.006.495-.071.928-.27l8.335-3.492c.172-.07.277-.124.43-.2 0 0 .284-.211.311-.243.28-.33.285-.621.316-.92a4.261 4.261 0 00.02-.434V1.879c0-1.373-.506-1.88-1.878-1.88zm13.366 3.11h.68c1.138 0 1.688.553 1.688 1.696v1.88h-1.374v-1.8c0-.369-.17-.54-.523-.54h-.235c-.367 0-.537.17-.537.539v5.81c0 .369.17.54.537.54h.262c.353 0 .523-.171.523-.54V8.619h1.373v2.143c0 1.144-.562 1.71-1.7 1.71h-.694c-1.138 0-1.7-.566-1.7-1.71V4.82c0-1.144.562-1.709 1.7-1.709zm-12.186.08h3.114v1.274H6.117v2.603h1.648v1.275H6.117v2.774h1.74v1.275h-3.14zm3.816 0h2.198c1.138 0 1.7.564 1.7 1.708v2.445c0 1.144-.562 1.71-1.7 1.71h-.799v3.338h-1.4zm4.53 0h1.4v9.201h-1.4zm-3.13 1.235v3.392h.575c.354 0 .523-.171.523-.54V4.965c0-.368-.17-.54-.523-.54zm-3.74 10.147a1.708 1.708 0 01.591.108 1.745 1.745 0 01.49.299l-.452.546a1.247 1.247 0 00-.308-.195.91.91 0 00-.363-.068.658.658 0 00-.28.06.703.703 0 00-.224.163.783.783 0 00-.151.243.799.799 0 00-.056.299v.008a.852.852 0 00.056.31.7.7 0 00.157.245.736.736 0 00.238.16.774.774 0 00.303.058.79.79 0 00.445-.116v-.339h-.548v-.565H7.37v1.255a2.019 2.019 0 01-.524.307 1.789 1.789 0 01-.683.123 1.642 1.642 0 01-.602-.107 1.46 1.46 0 01-.478-.3 1.371 1.371 0 01-.318-.455 1.438 1.438 0 01-.115-.58v-.008a1.426 1.426 0 01.113-.57 1.449 1.449 0 01.312-.46 1.418 1.418 0 01.474-.309 1.58 1.58 0 01.598-.111 1.708 1.708 0 01.045 0zm11.963.008a2.006 2.006 0 01.612.094 1.61 1.61 0 01.507.277l-.386.546a1.562 1.562 0 00-.39-.205 1.178 1.178 0 00-.388-.07.347.347 0 00-.208.052.154.154 0 00-.07.127v.008a.158.158 0 00.022.084.198.198 0 00.076.066.831.831 0 00.147.06c.062.02.14.04.236.061a3.389 3.389 0 01.43.122 1.292 1.292 0 01.328.17.678.678 0 01.207.24.739.739 0 01.071.337v.008a.865.865 0 01-.081.382.82.82 0 01-.229.285 1.032 1.032 0 01-.353.18 1.606 1.606 0 01-.46.061 2.16 2.16 0 01-.71-.116 1.718 1.718 0 01-.593-.346l.43-.514c.277.223.578.335.9.335a.457.457 0 00.236-.05.157.157 0 00.082-.142v-.008a.15.15 0 00-.02-.077.204.204 0 00-.073-.066.753.753 0 00-.143-.062 2.45 2.45 0 00-.233-.062 5.036 5.036 0 01-.413-.113 1.26 1.26 0 01-.331-.16.72.72 0 01-.222-.243.73.73 0 01-.082-.36v-.008a.863.863 0 01.074-.359.794.794 0 01.214-.283 1.007 1.007 0 01.34-.185 1.423 1.423 0 01.448-.066 2.006 2.006 0 01.025 0zm-9.358.025h.742l1.183 2.81h-.825l-.203-.499H8.623l-.198.498h-.81zm2.197.02h.814l.663 1.08.663-1.08h.814v2.79h-.766v-1.602l-.711 1.091h-.016l-.707-1.083v1.593h-.754zm3.469 0h2.235v.658h-1.473v.422h1.334v.61h-1.334v.442h1.493v.658h-2.255zm-5.3.897l-.315.793h.624zm-1.145 5.19h8.014l-4.09 1.348z"/></svg>';

  function storeIconHtml(name) {
    const n = (name || '').toLowerCase();
    if (n.includes('steam')) return '<i class="bi bi-steam"></i>';
    if (n.includes('itch')) return '<i class="bi bi-joystick"></i>';
    if (n.includes('gog')) return '<i class="bi bi-shop-window"></i>';
    if (n.includes('epic')) return EPIC_GAMES_SVG;
    return '<i class="bi bi-box-arrow-up-right"></i>';
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
        // Restores the scroll position from just before the user clicked
        // into a port page - saved on the grid click handler above. Only
        // present right after that specific round trip (it's removed as
        // soon as it's used), so a normal fresh visit to Browse still
        // starts at the top. Needs a frame to wait for the grid's cards
        // (rendered above) to actually paint, since the page is too short
        // to scroll that far until they do.
        const savedScrollY = sessionStorage.getItem('browseScrollY');
        if (savedScrollY !== null) {
          sessionStorage.removeItem('browseScrollY');
          requestAnimationFrame(() => window.scrollTo(0, parseInt(savedScrollY, 10)));
        }
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
        // A tile click is a fresh single-genre jump, not an add-to-selection -
        // replaces whatever genre checkboxes were already ticked.
        selectedGenres.clear();
        selectedGenres.add(genre);
        document.querySelectorAll('#genreCheckboxList input').forEach(i => { i.checked = i.value === genre; });
        syncGenreTiles();
        setCookie('selectedGenres', genre);
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
  const deviceRadioList = document.getElementById('deviceRadioList');
  const osRadioList = document.getElementById('osRadioList');
  const genreCheckboxListEl = document.getElementById('genreCheckboxList');
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
  let selectedDeviceName = '';
  let selectedOSName = '';
  let currentSort = 'downloads';
  let viewMode = 'grid';
  let pageSize = 100;
  let currentPage = 1;
  let selectedGenres = new Set();
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

    // Populate genre checkbox list
    const allGenres = new Set(allPorts.flatMap(p => p.genres || []));
    [...allGenres].sort().forEach(g => createFilterCheckbox(g, genreCheckboxListEl, selectedGenres, () => {
      syncGenreTiles();
      setCookie('selectedGenres', [...selectedGenres].join('|'));
    }));

    // Populate advanced filter checkboxes
    const runtimePills = document.getElementById('runtimePills');
    const archPills = document.getElementById('archPills');
    const reqPills = document.getElementById('reqPills');

    [...new Set(allPorts.flatMap(p => p.runtime || []))].sort().forEach(r => createFilterCheckbox(r, runtimePills, selectedRuntimes));
    [...new Set(allPorts.flatMap(p => p.arch || []))].sort().forEach(a => createFilterCheckbox(a, archPills, selectedArchs));
    [...new Set(allPorts.flatMap(p => p.reqs || []))].sort().forEach(r => createFilterCheckbox(r, reqPills, selectedReqs));

    renderDeviceList();
    renderOSList();
    restoreViewAndPaging();
    restoreSavedFilters();
  }

  // Generic checkbox-list filter item (Genre / Runtime / Architecture /
  // Requirements all use this) - matches the Epic Games Store filter
  // panel's checkbox style/interaction, backed by the same Set-per-
  // category pattern for all four.
  function createFilterCheckbox(value, container, selectedSet, onChange) {
    const label = document.createElement('label');
    label.className = 'filter-checkbox-item';
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.value = value;
    input.checked = selectedSet.has(value);
    const text = document.createElement('span');
    text.textContent = value;
    label.appendChild(input);
    label.appendChild(text);
    input.addEventListener('change', () => {
      if (input.checked) selectedSet.add(value); else selectedSet.delete(value);
      if (onChange) onChange();
      filterAndSearch();
    });
    container.appendChild(label);
    return label;
  }

  function syncGenreTiles() {
    document.querySelectorAll('.genre-tile').forEach(t => t.classList.toggle('active', selectedGenres.has(t.dataset.genre)));
  }

  // Device/OS are single-choice (compatibility checking needs exactly one
  // active device+OS), so radio buttons rather than checkboxes - same
  // "box" list look as Genre/Options, re-rendered from scratch whenever
  // the selection changes since the OS list itself depends on the device.
  function createFilterRadio(value, container, name, isChecked, onSelect) {
    const label = document.createElement('label');
    label.className = 'filter-checkbox-item';
    const input = document.createElement('input');
    input.type = 'radio';
    input.name = name;
    input.value = value;
    input.checked = isChecked;
    const text = document.createElement('span');
    text.textContent = value;
    label.appendChild(input);
    label.appendChild(text);
    input.addEventListener('change', () => { if (input.checked) onSelect(value); });
    container.appendChild(label);
    return label;
  }

  function renderDeviceList() {
    deviceRadioList.innerHTML = '';
    Object.keys(devices).sort().forEach(name => {
      createFilterRadio(name, deviceRadioList, 'deviceRadio', name === selectedDeviceName, (value) => {
        selectDevice(value);
        setCookie('selectedDevice', value, 365);
        setCookie('selectedOS', selectedOSName || '', selectedOSName ? 365 : -1);
        filterAndSearch();
      });
    });
  }

  function renderOSList() {
    osRadioList.innerHTML = '';
    const osNames = currentDevice ? Object.keys(currentDevice) : [];
    osNames.forEach(name => {
      createFilterRadio(name, osRadioList, 'osRadio', name === selectedOSName, (value) => {
        selectedOSName = value;
        currentOS = currentDevice ? currentDevice[value] : null;
        renderOSList();
        setCookie('selectedOS', value, 365);
        filterAndSearch();
      });
    });
  }

  // Sets device + auto-picks its first (or previously saved) OS - shared
  // by the radio click handler and restoreSavedFilters.
  function selectDevice(deviceName) {
    selectedDeviceName = deviceName;
    currentDevice = devices[deviceName] || null;

    const osNames = currentDevice ? Object.keys(currentDevice) : [];
    const savedOS = getCookie('selectedOS');
    selectedOSName = (savedOS && osNames.includes(savedOS)) ? savedOS : (osNames[0] || '');
    currentOS = (currentDevice && selectedOSName) ? currentDevice[selectedOSName] : null;

    renderDeviceList();
    renderOSList();
  }

  function clearAdvancedFilters() {
    selectedRuntimes.clear();
    selectedArchs.clear();
    selectedReqs.clear();
    document.querySelectorAll('#runtimePills input:checked, #archPills input:checked, #reqPills input:checked').forEach(i => { i.checked = false; });
    filterAndSearch();
  }

  // ===== Per-filter clear helpers - each undoes exactly one active filter,
  // used by both the "Reset" link (via clearAllFilters) and the individual
  // removable chips in #activeFiltersRow. =====
  function clearDeviceFilter() {
    selectedDeviceName = '';
    selectedOSName = '';
    currentDevice = null;
    currentOS = null;
    renderDeviceList();
    renderOSList();

    setCookie('selectedDevice', '', -1);
    setCookie('selectedOS', '', -1);
    filterAndSearch();
  }

  function clearGenreFilter() {
    selectedGenres.clear();
    document.querySelectorAll('#genreCheckboxList input:checked').forEach(i => { i.checked = false; });
    syncGenreTiles();
    setCookie('selectedGenres', '', -1);
    filterAndSearch();
  }

  function clearGenreValue(value) {
    clearCheckboxFilter(selectedGenres, value, 'genreCheckboxList');
    syncGenreTiles();
    setCookie('selectedGenres', [...selectedGenres].join('|'));
  }

  function clearReadyToggleFilter() {
    readyToggle.checked = false;
    setCookie('readyToggle', '', -1);
    filterAndSearch();
  }

  function clearHideIncompatibleFilter() {
    hideIncompatibleToggle.checked = false;
    setCookie('hideIncompatible', '', -1);
    filterAndSearch();
  }

  function clearCheckboxFilter(set, value, containerId) {
    set.delete(value);
    const container = document.getElementById(containerId);
    const input = container.querySelector(`input[value="${CSS.escape(value)}"]`);
    if (input) input.checked = false;
    filterAndSearch();
  }

  // ===== Active filter chips: one removable chip per active filter value,
  // shown above the game grid, plus the "Filters (N)" count badge in the
  // panel header - both computed from the same list so they can't drift. =====
  function getActiveFilters() {
    const filters = [];
    if (selectedDeviceName) {
      const label = selectedOSName ? `${selectedDeviceName} (${selectedOSName})` : selectedDeviceName;
      filters.push({ label: `Device: ${label}`, clear: clearDeviceFilter });
    }
    selectedGenres.forEach(v => filters.push({ label: `Genre: ${v}`, clear: () => clearGenreValue(v) }));
    if (readyToggle.checked) filters.push({ label: 'Ready to Run Only', clear: clearReadyToggleFilter });
    if (hideIncompatibleToggle.checked) filters.push({ label: 'Hide Incompatible', clear: clearHideIncompatibleFilter });
    selectedRuntimes.forEach(v => filters.push({ label: `Runtime: ${v}`, clear: () => clearCheckboxFilter(selectedRuntimes, v, 'runtimePills') }));
    selectedArchs.forEach(v => filters.push({ label: `Arch: ${v}`, clear: () => clearCheckboxFilter(selectedArchs, v, 'archPills') }));
    selectedReqs.forEach(v => filters.push({ label: `Requires: ${v}`, clear: () => clearCheckboxFilter(selectedReqs, v, 'reqPills') }));
    return filters;
  }

  function updateActiveFilterChips() {
    const filters = getActiveFilters();
    const row = document.getElementById('activeFiltersRow');
    if (filters.length === 0) {
      row.style.display = 'none';
      row.innerHTML = '';
    } else {
      row.style.display = 'flex';
      row.innerHTML = filters.map((f, i) => `<button type="button" class="active-filter-chip" data-chip-index="${i}">${escapeHtml(f.label)} <i class="bi bi-x"></i></button>`).join('');
      row.querySelectorAll('.active-filter-chip').forEach((btn, i) => {
        btn.addEventListener('click', () => filters[i].clear());
      });
    }

    const countEl = document.getElementById('filterActiveCount');
    if (filters.length > 0) {
      countEl.textContent = `(${filters.length})`;
      countEl.style.display = '';
    } else {
      countEl.style.display = 'none';
    }
  }

  function clearAllFilters() {
    clearAdvancedFilters();
    clearDeviceFilter();
    clearGenreFilter();
    clearReadyToggleFilter();
    clearHideIncompatibleFilter();
    gamesSearchInput.value = '';
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
  const sortCurrentLabel = document.getElementById('sortCurrentLabel');
  sortOptions.forEach(option => {
    option.addEventListener('click', () => {
      sortOptions.forEach(opt => opt.classList.remove('selected'));
      option.classList.add('selected');
      currentSort = option.dataset.sort;
      // The trigger shows the active sort's name (Epic-style "Show: X"),
      // so it has to track whichever option was just picked.
      sortCurrentLabel.textContent = option.textContent;
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

  // ===== Filter accordion sections (Device/OS/Genre/Options/Advanced) =====
  // Plain div + class toggle, not native <details>/<summary> - mkdocs-
  // material applies its own heavy "admonition" styling (colored border,
  // marker icon) to any <details> inside the content area, which fought
  // this component's own look.
  document.querySelectorAll('.filter-accordion-summary').forEach(summary => {
    summary.addEventListener('click', () => {
      summary.closest('.filter-accordion').classList.toggle('open');
    });
    summary.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        summary.closest('.filter-accordion').classList.toggle('open');
      }
    });
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
    const savedGenres = getCookie('selectedGenres');
    if (savedGenres) {
      savedGenres.split('|').filter(Boolean).forEach(g => selectedGenres.add(g));
      document.querySelectorAll('#genreCheckboxList input').forEach(i => { i.checked = selectedGenres.has(i.value); });
      syncGenreTiles();
    }

    if (getCookie('readyToggle') === 'true') readyToggle.checked = true;
    if (getCookie('hideIncompatible') === 'true') hideIncompatibleToggle.checked = true;

    const savedDevice = getCookie('selectedDevice');
    if (savedDevice && devices[savedDevice]) {
      selectDevice(savedDevice);
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
      const genreMatch = selectedGenres.size === 0 || (port.genres || []).some(g => selectedGenres.has(g));
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
    updateActiveFilterChips();
  }

  function renderCardHtml(port) {
    const rtrBadge = port.rtr ? '<span class="pm-rtr-badge">RTR</span>' : '';
    const img = port.screenshot
      ? `<img class="off-glb" src="https://raw.githubusercontent.com/${port.repo}/refs/heads/main/ports/${port.id}/${port.screenshot}" alt="${escapeHtml(port.title)}" loading="lazy" onerror="this.style.display='none'">`
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
      ? `Supported: ${supported}/${total} ports`
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

  // ===== Grid click delegation: jump straight to the full /port/ page
  // (no quick-view modal); middle-click still opens it in a new tab, and
  // right-click is left to the browser's native context menu. =====
  gameGrid.addEventListener('click', (e) => {
    const card = e.target.closest('.pm-card');
    if (!card) return;
    sessionStorage.setItem('browseScrollY', window.scrollY);
    window.location.href = `../port/?name=${encodeURIComponent(card.dataset.portId)}`;
  });
  gameGrid.addEventListener('auxclick', (e) => {
    if (e.button !== 1) return;
    const card = e.target.closest('.pm-card');
    if (!card) return;
    e.preventDefault();
    window.open(`../port/?name=${encodeURIComponent(card.dataset.portId)}`, '_blank');
  });

  window.addEventListener('popstate', () => {
    const hash = window.location.hash;
    setView(hash === '#browse' ? 'browse' : 'discover', { skipHash: true });
  });

  // ===================================================================
  // Mobile filter drawer offset: measures the real, current height of
  // mkdocs-material's own sticky header (title bar, plus its separate
  // .md-tabs row when that's visible) and exposes it as a CSS variable,
  // instead of hardcoding an assumed header height in CSS. A fixed guess
  // in CSS can't track header height changes across breakpoints, browser
  // font-size settings, or theme config - measuring it directly is the
  // only way .filter-panel's slide-out drawer reliably starts below the
  // header instead of covering it.
  // ===================================================================
  function updateHeaderHeightVar() {
    const header = document.querySelector('.md-header');
    if (!header) return;
    document.documentElement.style.setProperty('--md-header-actual-height', `${header.getBoundingClientRect().height}px`);
  }
  updateHeaderHeightVar();
  window.addEventListener('resize', updateHeaderHeightVar);

  // ===================================================================
  // Initial route: #browse -> Browse view, anything else -> Discover
  // (default, matches the static HTML classes).
  // ===================================================================
  (function initFromHash() {
    if (window.location.hash === '#browse') {
      setView('browse', { skipHash: true });
    }
  })();
</script>
