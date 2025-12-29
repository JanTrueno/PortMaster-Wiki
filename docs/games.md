---
hide:
  - navigation
  - toc

search:
  exclude: true
---

<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.1.0/dist/fuse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>



<div class="filters-container">

  <!-- Search Bar -->
  <div class="filters-row">
    <input type="text" id="searchInput" placeholder="Search ports..." class="search-bar">
  </div>
  
  <!-- Dropdowns + Checkboxes -->
  <div class="filters-row fixed-row">
    <select id="deviceSelect" class="filter-dropdown">
      <option value="">Select your device...</option>
    </select>

    <select id="osSelect" class="filter-dropdown" disabled>
      <option value="">Select OS...</option>
    </select>

    <select id="genreSelect" class="filter-dropdown">
      <option value="">All Genres</option>
    </select>

    <label class="filter-button-checkbox">
      <input type="checkbox" id="readyToggle"> Ready to Run Only
    </label>

    <label class="filter-button-checkbox">
      <input type="checkbox" id="hideIncompatibleToggle"> Hide Incompatible
    </label>
  </div>

  <!-- Counter -->
  <p id="portsCounter">Supported: 0 | Unsupported: 0</p>
</div>

<div class="game-grid">

{% for key, port in ports.ports.items() | default({}) %}
  {% set is_mv = port.source and port.source.url and ('PortMaster-MV' in port.source.url or 'MV-New' in port.source.url) %}
  {% set repo_owner = 'PortsMaster-MV' if is_mv else 'PortsMaster' %}
  {% set repo_name = 'PortMaster-MV-New' if is_mv else 'PortMaster-New' %}
  {% set port_id = key | replace('.zip','') %}
  
  <div class="game-card" onclick="openModal('modal-{{ port_id }}')"
       data-genres="{{ port.attr.genres | default([]) | join(',') if port.attr and port.attr.genres else '' }}"
       data-reqs="{{ port.attr.reqs | default([]) | join(',') if port.attr and port.attr.reqs else '' }}"
       data-arch="{{ port.attr.arch | default([]) | join(',') if port.attr and port.attr.arch else '' }}"
       data-runtime="{{ port.attr.runtime | default([]) | join(',') if port.attr and port.attr.runtime else '' }}"
       data-rtr="{{ port.attr.rtr | default(false) | string | lower }}"
       data-repo="{{ repo_owner }}/{{ repo_name }}"
       data-key="{{ key }}"
       data-port-id="{{ port_id }}">
    
    {% if port.attr and port.attr.image and port.attr.image.screenshot %}
    <img src="https://raw.githubusercontent.com/{{ repo_owner }}/{{ repo_name }}/refs/heads/main/ports/{{ port_id }}/{{ port.attr.image.screenshot }}" 
         alt="{{ port.attr.title if port.attr and port.attr.title else '' }}" 
         loading="lazy"
         onerror="console.error('Failed to load image for key={{ key }}, port_id={{ port_id }}, URL:', this.src)">
    {% endif %}

    <h3>{{ port.attr.title if port.attr and port.attr.title else '' }}</h3>
  </div>

  <div id="modal-{{ port_id }}" class="modal">
    <div class="modal-content">
      <span class="close" onclick="closeModal('modal-{{ port_id }}')">&times;</span>

      {% if port.attr and port.attr.image and port.attr.image.screenshot %}
      <img src="https://raw.githubusercontent.com/{{ repo_owner }}/{{ repo_name }}/refs/heads/main/ports/{{ port_id }}/{{ port.attr.image.screenshot }}" 
           alt="{{ port.attr.title if port.attr and port.attr.title else '' }}"
           onerror="console.error('Failed to load modal image for {{ key }}:', this.src)">
      {% endif %}

      <h1>{{ port.attr.title if port.attr and port.attr.title else '' }}</h1>

      <div class="markdown-content">
        {% if port.attr and (port.attr.desc_md or port.attr.desc) %}
        <h2>Description</h2>
        <div class="desc-md" data-desc="{{ port.attr.desc_md | e }}" data-desc_plain="{{ port.attr.desc | e }}"></div>
        {% endif %}

        {% if port.attr and (port.attr.inst_md or port.attr.inst) %}
        <h2>Instructions</h2>
        <div class="inst-md" data-inst="{{ port.attr.inst_md | e }}" data-inst_plain="{{ port.attr.inst | e }}"></div>
        {% endif %}
      </div>

      {% if port.attr and port.attr.genres %}
      <p><strong>Genres:</strong> {{ port.attr.genres | default([]) | join(", ") }}</p>
      {% endif %}

      {% if port.attr and port.attr.runtime %}
      <p><strong>Runtimes:</strong> 
        {{ port.attr.runtime | join(", ") }}
      </p>
      {% endif %}

      <a href="{{ port.source.url if port.source and port.source.url else '#' }}" class="download-button">Download</a>
    </div>
  </div>
{% endfor %}

</div>

<script>
  // ===== Global Variables =====
  let devices = {};
  let currentDevice = null;
  let currentOS = null;

  const deviceSelect = document.getElementById('deviceSelect');
  const osSelect = document.getElementById('osSelect');
  const genreSelect = document.getElementById('genreSelect');
  const searchInput = document.getElementById('searchInput');
  const readyToggle = document.getElementById('readyToggle');
  const hideIncompatibleToggle = document.getElementById('hideIncompatibleToggle');
  const allCards = document.querySelectorAll('.game-card');

  // ===== Load Devices =====
  fetch('/assets/json/device_info.json')
    .then(res => res.json())
    .then(data => {
      devices = data;
      Object.keys(devices).forEach(deviceName => deviceSelect.appendChild(new Option(deviceName, deviceName)));
    });

  // ===== Device & OS Dropdowns =====
  deviceSelect.addEventListener('change', e => {
    const selectedDevice = e.target.value;
    currentDevice = selectedDevice ? devices[selectedDevice] : null;

    osSelect.innerHTML = '<option value="">Select OS...</option>';
    if (currentDevice) {
      const osNames = Object.keys(currentDevice);
      osNames.forEach(osName => osSelect.appendChild(new Option(osName, osName)));
      osSelect.disabled = false;

      if (osNames.length > 0) {
        osSelect.value = osNames[0];
        currentOS = currentDevice[osNames[0]];
      }
    } else {
      osSelect.disabled = true;
      currentOS = null;
    }
    filterAndSearch();
  });

  osSelect.addEventListener('change', e => {
    const selectedOS = e.target.value;
    currentOS = selectedOS ? currentDevice[selectedOS] : null;
    filterAndSearch();
  });

  // ===== Ports Data =====
  const portsData = Array.from(allCards).map(card => {
    const title = card.querySelector('h3')?.textContent.trim() || '';
    const genres = card.dataset.genres ? card.dataset.genres.split(',').map(g => g.trim()).filter(Boolean) : [];
    const reqs = card.dataset.reqs ? card.dataset.reqs.split(',') : [];
    const arch = card.dataset.arch ? card.dataset.arch.split(',') : [];
    const runtime = card.dataset.runtime ? card.dataset.runtime.split(',').map(r => r.trim()).filter(Boolean) : [];
    const rtr = card.dataset.rtr === "true";

    return { card, title, genres, reqs, arch, runtime, rtr };
  });

  const fuse = new Fuse(portsData, {
    keys: [{ name: 'title', weight: 0.6 }, { name: 'genres', weight: 0.1 }],
    threshold: 0.4
  });

  // Populate Genre Dropdown
  new Set(portsData.flatMap(p => p.genres)).forEach(g => genreSelect.appendChild(new Option(g, g)));

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

  // ===== Compatibility Check =====
  function isCompatible(port) {
    if (!currentDevice) return !readyToggle.checked || port.rtr === true;

    const deviceCap = currentOS || Object.values(currentDevice)[0];
    const capabilities = new Set([
        ...(deviceCap.capabilities || []),
        ...(currentOS?.capabilities || [])
    ]);

    if (readyToggle.checked && !port.rtr) return false;

    // Get the primary architecture of the device
    const primaryArch = deviceCap.primary_arch?.toLowerCase();

    // Check architecture compatibility
    if (!port.arch || port.arch.length === 0) {
      // No arch specified - check if runtime is compatible
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
      } else {
        // No arch and no runtime - assume compatible
        return true;
      }
    } else {
      // Check if device has one of the required architectures
      const requiredArches = new Set(port.arch.map(a => a.toLowerCase()));
      let hasArch = false;
      for (const arch of requiredArches) {
        if (capabilities.has(arch)) { hasArch = true; break; }
      }
      if (!hasArch) return false;
    }

    // Check requirements
    for (const req of port.reqs || []) {
        if (req.startsWith("!")) {
            if (capabilities.has(req.slice(1).toLowerCase())) return false;
        } else if (req.includes("|")) {
            if (!req.split("|").map(x=>x.trim().toLowerCase()).some(opt=>capabilities.has(opt))) return false;
        } else if (!capabilities.has(req.toLowerCase())) return false;
    }

    return true;
  }

  // ===== Filter + Search + Counter =====
  [searchInput, genreSelect, readyToggle, hideIncompatibleToggle].forEach(el => el.addEventListener('input', filterAndSearch));

  function filterAndSearch() {
    const query = searchInput.value.trim();
    const selectedGenre = genreSelect.value;
    const hideIncompatible = hideIncompatibleToggle.checked;
    const searchSet = query ? new Set(fuse.search(query).map(r => r.item)) : null;

    let supported = 0, unsupported = 0;

    portsData.forEach(port => {
      const matchSearch = !searchSet || searchSet.has(port);
      const genreMatch = !selectedGenre || port.genres.length === 0 || port.genres.includes(selectedGenre);
      const compatible = isCompatible(port);
      const visible = matchSearch && genreMatch && (!hideIncompatible || compatible);

      port.card.style.display = visible ? "flex" : "none";
      port.card.style.opacity = compatible ? "1" : "0.4";

      if (visible) compatible ? supported++ : unsupported++;
    });

    document.getElementById("portsCounter").textContent = `Supported: ${supported} | Unsupported: ${unsupported}`;
  }

  // ===== Modal Functions =====
  function openModal(id) {
    const modal = document.getElementById(id);
    modal.style.display = "block";
    history.replaceState(null, null, "#" + id);
    modal.addEventListener("click", e => { if(e.target === modal) closeModal(id); });
  }
  function closeModal(id) {
    document.getElementById(id).style.display = "none";
    history.replaceState(null, null, window.location.pathname);
  }

  // ===== Render Markdown =====
  function renderMarkdown() {
    document.querySelectorAll('.desc-md, .inst-md').forEach(el => {
      let md = el.dataset.desc || el.dataset.inst;
      if (!md || md.trim() === "None") md = el.dataset.desc_plain || el.dataset.inst_plain;
      if (md && md.trim()) el.innerHTML = marked.parse(md);
    });
  }

  // ===== Initialize =====
  window.addEventListener('load', () => {
    filterAndSearch();
    renderMarkdown();

    const hash = window.location.hash.substring(1);
    if (hash) {
      const modal = document.getElementById(hash);
      if (modal) openModal(hash);
    }
  });

</script>
