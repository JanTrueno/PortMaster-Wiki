---
hide:
  - navigation
  - toc

search:
  exclude: true
---

<div style="display:none">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
</div>
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
  <div class="carousel-card" onclick="window.location.href='../port/#{{ port_id }}'">
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
        {{ downloads | default(0) }}
      </span>
      <span class="card-stat">
        <i class="bi bi-calendar-plus"></i>
        {{ date_added }}
      </span>
    </div>
  </div>
{% endif %}
{% endmacro %}

<div class="featured-category featured-category--first">
  <div class="featured-category-header">
    <h1>Recently Added Ports</h1>
    <p>The newest ports to hit PortMaster in the last 30 days.</p>
  </div>

  <div class="carousel-container">
    <button class="carousel-btn carousel-btn-left" onclick="scrollCarousel('recentPortsCarousel', -1)">
      <i class="bi bi-chevron-left"></i>
    </button>
    <div class="carousel-track" id="recentPortsCarousel">
      {% set prev_month_ts = now().timestamp() - 2592000 %}
      {% set thirty_days_ago_str = now().fromtimestamp(prev_month_ts).strftime('%Y-%m-%d') %}
      {% set count = namespace(value=0) %}

      {% for port_key in sorted_orders['date-added'] %}
        {% set port = ports['ports'][port_key] %}
        {% set source = port.source or {} %}
        {% set date_added = source.date_added or '' %}

        {% if date_added and date_added >= thirty_days_ago_str and count.value < 20 %}
          {% set count.value = count.value + 1 %}
          {{ port_card(port_key) }}
        {% endif %}
      {% endfor %}
    </div>
    <button class="carousel-btn carousel-btn-right" onclick="scrollCarousel('recentPortsCarousel', 1)">
      <i class="bi bi-chevron-right"></i>
    </button>
  </div>
  <div class="carousel-see-all"><a href="../all-games/" class="see-all-link">See All <i class="bi bi-chevron-right"></i></a></div>
  <div class="carousel-dots"></div>
</div>

<div class="featured-category">
  <div class="featured-category-header">
    <h1>Popular Ports</h1>
    <p>The most downloaded ports on PortMaster.</p>
  </div>

  <div class="carousel-container">
    <button class="carousel-btn carousel-btn-left" onclick="scrollCarousel('popularPortsCarousel', -1)">
      <i class="bi bi-chevron-left"></i>
    </button>
    <div class="carousel-track" id="popularPortsCarousel">
      {% for port_key in sorted_orders['downloads'][:20] %}
        {{ port_card(port_key) }}
      {% endfor %}
    </div>
    <button class="carousel-btn carousel-btn-right" onclick="scrollCarousel('popularPortsCarousel', 1)">
      <i class="bi bi-chevron-right"></i>
    </button>
  </div>
  <div class="carousel-see-all"><a href="../all-games/" class="see-all-link">See All <i class="bi bi-chevron-right"></i></a></div>
  <div class="carousel-dots"></div>
</div>

{% for category in featured_categories %}
{% set cat_index = loop.index %}
<div class="featured-category">
  <div class="featured-category-header">
    <h1>{{ category.name }}</h1>
  </div>

  {% for group in category.groups %}
  {% set track_id = 'carousel-' ~ cat_index ~ '-' ~ loop.index %}
  <div class="featured-group">
    <div class="featured-group-header">
      <h2>{{ group.name }}</h2>
    </div>
    <div class="carousel-container">
      <button class="carousel-btn carousel-btn-left" onclick="scrollCarousel('{{ track_id }}', -1)">
        <i class="bi bi-chevron-left"></i>
      </button>
      <div class="carousel-track" id="{{ track_id }}">
        {% for port_key in group.ports %}
          {{ port_card(port_key) }}
        {% endfor %}
      </div>
      <button class="carousel-btn carousel-btn-right" onclick="scrollCarousel('{{ track_id }}', 1)">
        <i class="bi bi-chevron-right"></i>
      </button>
    </div>
    <div class="carousel-see-all"><a href="../all-games/" class="see-all-link">See All <i class="bi bi-chevron-right"></i></a></div>
    <div class="carousel-dots"></div>
  </div>
  {% endfor %}
</div>
{% endfor %}

<div style="text-align: center; padding: 2rem; background: var(--md-code-bg-color); border-radius: 12px; margin: 2.5rem auto;">
  <h3 style="font-size: 1.5rem; margin: 0 0 1rem 0;">Looking for something specific?</h3>
  <p style="margin: 0 0 1.5rem 0;">Search, filter by device, genre, or requirements, and browse the full library of {{ total_port_count }} ports.</p>
  <a href="../all-games/" class="md-button" style="display: inline-flex; align-items: center; gap: 0.5rem;">
    <i class="bi bi-search"></i> Browse All Games
  </a>
</div>

<script>
function scrollCarousel(trackId, direction) {
  const track = document.getElementById(trackId);
  if (!track) return;
  const cards = track.querySelectorAll('.carousel-card');
  if (cards.length > 0) {
    const cardWidth = cards[0].offsetWidth + 16;
    track.scrollBy({ left: direction * cardWidth, behavior: 'smooth' });
  }
}

function initCarouselDots(track) {
  const dotsWrap = track.closest('.carousel-container').parentElement.querySelector('.carousel-dots');
  if (!dotsWrap) return;

  function getMetrics() {
    const cards = track.querySelectorAll('.carousel-card');
    const cardWidth = cards.length ? cards[0].offsetWidth + 16 : 0;
    const perPage = cardWidth ? Math.max(1, Math.round(track.clientWidth / cardWidth)) : 1;
    const pageCount = cardWidth ? Math.max(1, Math.ceil(cards.length / perPage)) : 1;
    return { cardWidth, perPage, pageCount };
  }

  function build() {
    const { cardWidth, perPage, pageCount } = getMetrics();
    dotsWrap.innerHTML = '';
    if (pageCount <= 1) {
      dotsWrap.style.display = 'none';
      return;
    }
    dotsWrap.style.display = 'flex';
    for (let i = 0; i < pageCount; i++) {
      const dot = document.createElement('button');
      dot.className = 'carousel-dot';
      dot.setAttribute('aria-label', 'Go to slide ' + (i + 1));
      dot.addEventListener('click', () => {
        track.scrollTo({ left: i * perPage * cardWidth, behavior: 'smooth' });
      });
      dotsWrap.appendChild(dot);
    }
    updateActiveDot();
  }

  function updateActiveDot() {
    const { cardWidth, perPage } = getMetrics();
    const pageWidth = perPage * cardWidth;
    const dots = dotsWrap.querySelectorAll('.carousel-dot');
    if (!dots.length || !pageWidth) return;
    const activeIndex = Math.min(dots.length - 1, Math.round(track.scrollLeft / pageWidth));
    dots.forEach((dot, i) => dot.classList.toggle('active', i === activeIndex));
  }

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(build, 200);
  });
  track.addEventListener('scroll', () => window.requestAnimationFrame(updateActiveDot));

  build();
}

document.querySelectorAll('.carousel-track').forEach(initCarouselDots);
</script>
