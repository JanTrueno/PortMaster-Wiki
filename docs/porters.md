---
# Porter cards link straight to /porter/?name=<id> now (no quick-view
# modal), so this page no longer embeds each porter's full bio + resolved
# port list, or the entire ports.json/port_stats.json blobs, inline in its
# own HTML - that inline data was the reason this page rendered to ~2MB
# and (combined with glightbox's regex bug - see games.md) dominated the
# site build. glightbox itself is still skipped here since every <img> is
# already opted out via off-glb.
glightbox: false
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

# PortMaster Porters
The amazing people who bring games to your handheld devices

<div class="filters-container">
  <div class="filters-left">
    <div class="search-wrapper">
      <input type="text" id="porterSearch" class="search-bar" placeholder="Search porters...">
    </div>
  </div>
  <div class="filters-right">
    <p id="portsCounter">Showing <span id="visible-porter-count">{{ porters | length }}</span> of {{ porters | length }} porters</p>
  </div>
</div>

<div class="porters-grid">
{% for porter_id, porter in porters.items() %}
  {% if porter.port_count is defined and porter.port_count > 0 %}
  <div class="porter-card" onclick="window.location.href='../porter/?name={{ porter_id | urlencode }}'" data-name="{{ porter.name | default(porter_id) }}">
    <div class="porter-avatar">
      {% if porter.image %}
      <img src="{{ porter.image }}" alt="{{ porter.name | default(porter_id) }}" loading="lazy" class="off-glb" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
      <div class="porter-avatar-placeholder" style="display: none;">
        <i class="bi bi-person-fill"></i>
      </div>
      {% else %}
      <div class="porter-avatar-placeholder">
        <i class="bi bi-person-fill"></i>
      </div>
      {% endif %}
    </div>

    <h3>{{ porter.name | default(porter_id) }}</h3>

    <div class="porter-stats">
      <span class="porter-stat">
        <i class="bi bi-box-seam"></i>
        {{ porter.port_count | default(0) }} ports
      </span>
      <span class="porter-stat">
        <i class="bi bi-download"></i>
        {{ "{:,}".format(porter.total_downloads | default(0)) }}
      </span>
    </div>

    {% if porter.support %}
    <div class="porter-support-badge">
      <i class="bi bi-heart-fill"></i> Support
    </div>
    {% endif %}
  </div>
  {% endif %}
{% endfor %}
</div>

<script>
  const porterCards = document.querySelectorAll('.porter-card');
  const searchInput = document.getElementById('porterSearch');

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase().trim();
    let visible = 0;

    porterCards.forEach(card => {
      const name = card.dataset.name.toLowerCase();
      const matches = !query || name.includes(query);
      card.style.display = matches ? 'flex' : 'none';
      if (matches) visible++;
    });

    document.getElementById('visible-porter-count').textContent = visible;
  });
</script>
