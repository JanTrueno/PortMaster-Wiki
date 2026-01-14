<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">


# PortMaster Porters
The amazing people who bring games to your handheld devices

<div class="filters-container">
  <div class="search-wrapper">
    <input type="text" id="porterSearch" class="search-bar" placeholder="Search porters...">
  </div>
</div>

<div id="portsCounter">
  Showing <span id="visible-porter-count">{{ porters | length }}</span> of {{ porters | length }} porters
</div>

<!-- Porter Detail Modal -->
<div id="porterModal" class="modal">
  <div class="modal-content porter-modal-content">
    <span class="close" onclick="closePorterModal()">&times;</span>
    
    <div class="porter-detail-header">
      <div class="porter-detail-avatar" id="modalPorterAvatar">
        <i class="bi bi-person-fill"></i>
      </div>
      <div class="porter-detail-info">
        <h1 id="modalPorterName"></h1>
        <p class="porter-detail-bio" id="modalPorterBio"></p>
        <div class="porter-detail-links" id="modalPorterLinks"></div>
      </div>
    </div>
    
    <div class="porter-detail-stats">
      <div class="porter-stat-item">
        <i class="bi bi-box-seam"></i>
        <span id="modalPortCount">0</span>
        <label>Ports</label>
      </div>
      <div class="porter-stat-item">
        <i class="bi bi-download"></i>
        <span id="modalDownloads">0</span>
        <label>Downloads</label>
      </div>
    </div>
    
    <div class="porter-ports-section">
      <h2>Ports by this Porter</h2>
      <div class="porter-ports-grid" id="modalPortsGrid">
        <!-- Ports will be populated here -->
      </div>
    </div>
  </div>
</div>

<div class="porters-grid">
{% for porter_id, porter in porters.items() %}
  {% if porter.port_count is defined and porter.port_count > 0 %}
  <div class="porter-card" onclick="openPorterModal('{{ porter_id }}')"
       data-name="{{ porter.name | default(porter_id) }}"
       data-bio="{{ porter.bio | default('') | e }}"
       data-image="{{ porter.image | default('') }}"
       data-webpage="{{ porter.webpage | default('') }}"
       data-social="{{ porter.social | default('') }}"
       data-support="{{ porter.support | default('') }}"
       data-port-count="{{ porter.port_count | default(0) }}"
       data-total-downloads="{{ porter.total_downloads | default(0) }}"
       data-ports="{{ porter.ports | default([]) | join(',') }}">
    
    <div class="porter-avatar">
      {% if porter.image %}
      <img src="{{ porter.image }}" alt="{{ porter.name | default(porter_id) }}" loading="lazy" data-glightbox="false" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
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
  // Port data for modal
  const portsData = {{ ports.ports | tojson | safe }};
  const portStats = {{ port_stats.ports | tojson | safe }};
  
  const porterCards = document.querySelectorAll('.porter-card');
  const searchInput = document.getElementById('porterSearch');
  
  // Search functionality
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
  
  // Modal functions
  function openPorterModal(porterId) {
    const card = document.querySelector(`[data-name="${porterId}"], [onclick*="'${porterId}'"]`);
    if (!card) return;
    
    const name = card.dataset.name;
    const bio = card.dataset.bio;
    const image = card.dataset.image;
    const webpage = card.dataset.webpage;
    const social = card.dataset.social;
    const support = card.dataset.support;
    const portCount = card.dataset.portCount;
    const totalDownloads = parseInt(card.dataset.totalDownloads) || 0;
    const ports = card.dataset.ports ? card.dataset.ports.split(',').filter(Boolean) : [];
    
    // Set basic info
    document.getElementById('modalPorterName').textContent = name;
    document.getElementById('modalPorterBio').textContent = bio || 'No bio available';
    document.getElementById('modalPorterBio').style.display = bio ? '' : 'none';
    document.getElementById('modalPortCount').textContent = portCount;
    document.getElementById('modalDownloads').textContent = totalDownloads.toLocaleString();
    
    // Set avatar
    const avatarEl = document.getElementById('modalPorterAvatar');
    if (image) {
      avatarEl.innerHTML = `<img src="${image}" alt="${name}" data-glightbox="false" onerror="this.parentElement.innerHTML='<i class=\\'bi bi-person-fill\\'></i>'">`;
    } else {
      avatarEl.innerHTML = '<i class="bi bi-person-fill"></i>';
    }
    
    // Set links
    const linksEl = document.getElementById('modalPorterLinks');
    let linksHTML = '';
    if (webpage) {
      linksHTML += `<a href="${webpage}" target="_blank" class="porter-link"><i class="bi bi-globe"></i> Website</a>`;
    }
    if (social) {
      linksHTML += `<a href="${social}" target="_blank" class="porter-link"><i class="bi bi-chat"></i> Social</a>`;
    }
    if (support) {
      linksHTML += `<a href="${support}" target="_blank" class="porter-link support-link"><i class="bi bi-heart-fill"></i> Support</a>`;
    }
    linksEl.innerHTML = linksHTML || '<span class="no-links">No links available</span>';
    
    // Populate ports grid - styled exactly like game cards
    const portsGrid = document.getElementById('modalPortsGrid');
    if (ports.length > 0) {
      let portsHTML = '';
      ports.forEach(portKey => {
        const port = portsData[portKey];
        if (port) {
          const attr = port.attr || {};
          const source = port.source || {};
          const title = attr.title || portKey.replace('.zip', '');
          const portId = portKey.replace('.zip', '');
          const downloads = portStats[portKey] || 0;
          const dateAdded = source.date_added || '—';
          
          // Determine repo
          const isMV = source.url && (source.url.includes('PortMaster-MV') || source.url.includes('MV-New'));
          const repoOwner = isMV ? 'PortsMaster-MV' : 'PortsMaster';
          const repoName = isMV ? 'PortMaster-MV-New' : 'PortMaster-New';
          
          const screenshot = attr.image && attr.image.screenshot 
            ? `https://raw.githubusercontent.com/${repoOwner}/${repoName}/refs/heads/main/ports/${portId}/${attr.image.screenshot}`
            : '';
          
          portsHTML += `
            <div class="game-card porter-game-card" onclick="window.location.href='../games/#modal-${portId}'">
              ${screenshot ? `<img src="${screenshot}" alt="${title}" data-glightbox="false" loading="lazy" onerror="this.style.display='none'">` : ''}
              <h3>${title}</h3>
              <div class="card-stats">
                <span class="card-stat">
                  <i class="bi bi-download"></i>
                  ${downloads > 0 ? downloads.toLocaleString() : '—'}
                </span>
                <span class="card-stat">
                  <i class="bi bi-calendar-plus"></i>
                  ${dateAdded}
                </span>
              </div>
            </div>
          `;
        }
      });
      portsGrid.innerHTML = portsHTML;
    } else {
      portsGrid.innerHTML = '<p class="no-ports">No ports found</p>';
    }
    
    // Show modal with animation and push to history
    const modal = document.getElementById('porterModal');
    modal.style.display = 'block';
    modal.offsetHeight;
    modal.classList.add('show');
    history.pushState({ porter: porterId }, '', '#porter-' + encodeURIComponent(porterId));
  }
  
  function closePorterModal(updateHistory = true) {
    const modal = document.getElementById('porterModal');
    if (!modal.classList.contains('show')) return;
    
    // Animate out
    modal.classList.remove('show');
    
    // Wait for animation to complete before hiding
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300);
    
    // Only update history if not triggered by back button
    if (updateHistory && window.location.hash.startsWith('#porter-')) {
      history.pushState({ porter: null }, '', window.location.pathname);
    }
  }
  
  // Handle back/forward button
  window.addEventListener('popstate', (e) => {
    const hash = window.location.hash;
    
    if (hash.startsWith('#porter-')) {
      // Opening a modal from history
      const porterId = decodeURIComponent(hash.replace('#porter-', ''));
      openPorterModal(porterId);
    } else {
      // Close modal when going back
      closePorterModal(false);
    }
  });
  
  // Close modal on outside click
  window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
      closePorterModal(true);
    }
  });
  
  // Handle hash on page load
  window.addEventListener('load', () => {
    const hash = window.location.hash.substring(1);
    if (hash && hash.startsWith('porter-')) {
      const porterId = decodeURIComponent(hash.replace('porter-', ''));
      // Use replaceState for initial load to not add extra history entry
      history.replaceState({ porter: porterId }, '', '#porter-' + encodeURIComponent(porterId));
      openPorterModal(porterId);
    }
  });
</script>