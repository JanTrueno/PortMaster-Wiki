---
title: Porter - PortMaster Wiki
hide:
  - navigation
  - toc
  - path

search:
  exclude: true

# Same reasoning as port.md/games.md: nothing here for glightbox to
# usefully wrap (avatar/screenshots are all injected client-side), and
# its static action-button markup triggers the same catastrophic-
# backtracking regex bug in glightbox's on_page_content.
glightbox: false
---

<div style="display:none">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
</div>
<style>.md-path { display: none; }</style>

<div class="porter-page" id="porter-page-root">
  <div id="porter-page-loading" class="port-page-loading">Loading...</div>

  <div id="porter-page-notfound" class="port-page-not-found" style="display:none">
    <p>We couldn't find that porter.</p>
    <a href="../porters/" class="hero-btn hero-btn-secondary">Browse All Porters</a>
  </div>

  <div class="porter-page-content" id="porter-page-content" style="display:none">
    <a href="../porters/" class="port-hero-back porter-back-standalone" title="Back to Porters"><i class="bi bi-arrow-left"></i></a>

    <div class="porter-detail-header">
      <div class="porter-detail-avatar" id="porter-avatar">
        <i class="bi bi-person-fill"></i>
      </div>
      <div class="porter-detail-info">
        <h1 id="porter-name"></h1>
        <p class="porter-detail-bio" id="porter-bio"></p>
        <div class="porter-detail-links" id="porter-links"></div>
      </div>
    </div>

    <div class="porter-detail-stats">
      <div class="porter-stat-item">
        <i class="bi bi-box-seam"></i>
        <span id="porter-port-count">0</span>
        <label>Ports</label>
      </div>
      <div class="porter-stat-item">
        <i class="bi bi-download"></i>
        <span id="porter-downloads">0</span>
        <label>Downloads</label>
      </div>
    </div>

    <div class="porter-ports-toolbar">
      <h2 class="porter-ports-heading">Ports by this Porter</h2>
      <div class="view-toggle-wrapper" id="viewToggleWrapper">
        <button class="view-toggle-btn active" id="gridViewBtn" title="Grid view" aria-label="Grid view">
          <i class="bi bi-grid-3x3-gap-fill"></i>
        </button>
        <button class="view-toggle-btn" id="listViewBtn" title="List view" aria-label="List view">
          <i class="bi bi-list-ul"></i>
        </button>
      </div>
    </div>

    <div class="game-grid" id="porter-ports-grid"></div>
  </div>
</div>

<script>
(function () {
  const loadingEl = document.getElementById('porter-page-loading');
  const notFoundEl = document.getElementById('porter-page-notfound');
  const contentEl = document.getElementById('porter-page-content');
  const grid = document.getElementById('porter-ports-grid');
  const gridViewBtn = document.getElementById('gridViewBtn');
  const listViewBtn = document.getElementById('listViewBtn');

  function getPorterIdFromUrl() {
    return new URLSearchParams(location.search).get('name');
  }

  function setState(state) {
    loadingEl.style.display = state === 'loading' ? '' : 'none';
    notFoundEl.style.display = state === 'notfound' ? '' : 'none';
    contentEl.style.display = state === 'content' ? '' : 'none';
  }

  function escapeHtml(value) {
    const div = document.createElement('div');
    div.textContent = value;
    return div.innerHTML;
  }

  function renderCardHtml(port) {
    const img = port.screenshot
      ? `<img class="off-glb" src="https://raw.githubusercontent.com/${port.repo}/refs/heads/main/ports/${port.id}/${port.screenshot}" alt="${escapeHtml(port.title)}" loading="lazy" onerror="this.style.display='none'">`
      : '';
    const downloadsText = port.downloads > 0 ? port.downloads.toLocaleString() : '—';
    return `<div class="pm-card" onclick="window.location.href='../port/?name=${encodeURIComponent(port.id)}'">${img}<h3>${escapeHtml(port.title)}</h3><div class="card-stats"><span class="card-stat"><i class="bi bi-download"></i> ${downloadsText}</span><span class="card-stat"><i class="bi bi-calendar-plus"></i> ${port.dateAdded || '—'}</span></div></div>`;
  }

  function setViewMode(mode) {
    grid.classList.toggle('list-view', mode === 'list');
    gridViewBtn.classList.toggle('active', mode === 'grid');
    listViewBtn.classList.toggle('active', mode === 'list');
  }
  gridViewBtn.addEventListener('click', () => setViewMode('grid'));
  listViewBtn.addEventListener('click', () => setViewMode('list'));

  function renderPorter(porterId, porter) {
    document.title = `${porter.name} - PortMaster Wiki`;
    document.getElementById('porter-name').textContent = porter.name;

    const bioEl = document.getElementById('porter-bio');
    bioEl.textContent = porter.bio || 'No bio available';
    bioEl.style.display = porter.bio ? '' : 'none';

    document.getElementById('porter-port-count').textContent = porter.portCount;
    document.getElementById('porter-downloads').textContent = porter.totalDownloads.toLocaleString();

    const avatarEl = document.getElementById('porter-avatar');
    if (porter.image) {
      avatarEl.innerHTML = `<img src="${porter.image}" alt="${escapeHtml(porter.name)}" class="off-glb" onerror="this.parentElement.innerHTML='<i class=\\'bi bi-person-fill\\'></i>'">`;
    } else {
      avatarEl.innerHTML = '<i class="bi bi-person-fill"></i>';
    }

    const linksEl = document.getElementById('porter-links');
    let linksHTML = '';
    if (porter.webpage) {
      linksHTML += `<a href="${porter.webpage}" target="_blank" rel="noopener" class="hero-btn hero-btn-secondary"><i class="bi bi-globe"></i> Website</a>`;
    }
    if (porter.social) {
      linksHTML += `<a href="${porter.social}" target="_blank" rel="noopener" class="hero-btn hero-btn-secondary"><i class="bi bi-chat"></i> Social</a>`;
    }
    if (porter.support) {
      linksHTML += `<a href="${porter.support}" target="_blank" rel="noopener" class="hero-btn hero-btn-secondary"><i class="bi bi-heart-fill"></i> Support</a>`;
    }
    linksEl.innerHTML = linksHTML || '<span class="no-links">No links available</span>';

    grid.innerHTML = porter.ports.length > 0
      ? porter.ports.map(renderCardHtml).join('')
      : '<p class="no-ports">No ports found</p>';

    setState('content');
  }

  function showPorter() {
    const porterId = getPorterIdFromUrl();
    if (!porterId) {
      setState('notfound');
      return;
    }

    setState('loading');
    fetch('../assets/json/porter_details.json')
      .then(res => res.json())
      .then(data => {
        const porter = data[porterId];
        if (porter) {
          renderPorter(porterId, porter);
        } else {
          setState('notfound');
        }
      })
      .catch(() => setState('notfound'));
  }

  window.addEventListener('popstate', showPorter);
  showPorter();
})();
</script>
