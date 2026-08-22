(function () {
  const root = document.getElementById('port-page-root');
  if (!root) return;

  const loadingEl = document.getElementById('port-page-loading');
  const notFoundEl = document.getElementById('port-page-notfound');
  const contentEl = document.getElementById('port-page-content');

  let portDetails = null;
  let activePortId = null;
  const readmeCache = {};

  // URL scheme matches the legacy portmaster.games detail page
  // (detail.html?name=<port_id>) so old bookmarks/shares keep working.
  function getPortIdFromUrl() {
    return new URLSearchParams(location.search).get('name');
  }

  function setState(state) {
    loadingEl.style.display = state === 'loading' ? '' : 'none';
    notFoundEl.style.display = state === 'notfound' ? '' : 'none';
    contentEl.style.display = state === 'content' ? '' : 'none';
  }

  function badges(values) {
    if (!values || values.length === 0) return '—';
    return values.map(v => escapeHtml(v)).join(', ');
  }

  function porterLinks(values) {
    if (!values || values.length === 0) return '—';
    return values
      .map(v => `<a href="../porter/?name=${encodeURIComponent(v)}">${escapeHtml(v)}</a>`)
      .join(', ');
  }

  function escapeHtml(value) {
    const div = document.createElement('div');
    div.textContent = value;
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
    const trimmed = (name || '').trim();
    return trimmed || 'Store';
  }

  function renderPort(portId, port) {
    document.title = `${port.title} - PortMaster Wiki`;

    document.getElementById('port-title').textContent = port.title;

    const heroImg = document.getElementById('port-screenshot');
    const hero = heroImg.closest('.port-hero');
    if (port.screenshot) {
      heroImg.src = `https://raw.githubusercontent.com/${port.repo}/refs/heads/main/ports/${portId}/${port.screenshot}`;
      heroImg.alt = port.title;
      hero.style.display = '';
    } else {
      hero.style.display = 'none';
    }

    const descEl = document.getElementById('port-desc');
    descEl.innerHTML = port.descHtml || '';
    wrapTables(descEl);

    const downloadBtn = document.getElementById('port-download-btn');
    downloadBtn.href = port.url || '#';

    // ===== Stat pills =====
    document.getElementById('port-stat-downloads').textContent = port.downloads > 0 ? port.downloads.toLocaleString() : 'N/A';
    document.getElementById('port-stat-porter').textContent = port.porter && port.porter.length
      ? (port.porter.length > 1 ? `${port.porter[0]} +${port.porter.length - 1}` : port.porter[0])
      : 'Unknown';
    document.getElementById('port-stat-rtr').textContent = port.rtr ? 'Ready to Run' : 'Setup Required';
    const rtrPill = document.getElementById('port-stat-rtr-pill');
    const rtrIcon = document.getElementById('port-stat-rtr-icon');
    rtrPill.classList.toggle('port-stat-pill--warn', !port.rtr);
    rtrIcon.className = port.rtr ? 'bi bi-lightning-charge-fill' : 'bi bi-tools';

    // ===== Store links =====
    const storeWrap = document.getElementById('port-store-links');
    if (port.store && port.store.length) {
      storeWrap.innerHTML = port.store
        .map(s => `<a href="${s.url}" target="_blank" rel="noopener" class="port-store-link" title="${escapeHtml(shortStoreName(s.name))}">${storeIconHtml(s.name)} <span class="port-store-label">${escapeHtml(shortStoreName(s.name))}</span></a>`)
        .join('');
      storeWrap.style.display = '';
    } else {
      storeWrap.innerHTML = '';
      storeWrap.style.display = 'none';
    }

    // ===== Full details grid (bottom of page) =====
    document.getElementById('port-genres').innerHTML = badges(port.genres);
    document.getElementById('port-reqs').innerHTML = badges(port.reqs);
    document.getElementById('port-porter-full').innerHTML = porterLinks(port.porter);
    document.getElementById('port-downloads').textContent = port.downloads > 0 ? port.downloads.toLocaleString() : 'N/A';
    document.getElementById('port-runtimes').innerHTML = badges(port.runtime);
    document.getElementById('port-arch').innerHTML = badges(port.arch);
    document.getElementById('port-date-added').textContent = port.dateAdded || 'N/A';
    document.getElementById('port-date-updated').textContent = port.dateUpdated || 'N/A';
    document.getElementById('port-misc').textContent = port.rtr ? 'Ready to Run' : 'Setup Required';

    const instSection = document.getElementById('port-inst-section');
    const instEl = document.getElementById('port-inst');
    if (port.instHtml) {
      instEl.innerHTML = port.instHtml;
      wrapTables(instEl);
      instSection.style.display = '';
    } else {
      instSection.style.display = 'none';
    }

    activePortId = portId;
    loadReadme(portId, port.repo);
    currentPort = port;
    updateDeviceChip();
    setState('content');
  }

  function loadReadme(portId, repo) {
    const readmeEl = document.getElementById('port-readme');

    if (readmeCache[portId]) {
      readmeEl.innerHTML = readmeCache[portId];
      wrapTables(readmeEl);
      return;
    }

    readmeEl.innerHTML = '<div class="loading-spinner">Loading...</div>';
    const readmeUrl = `https://raw.githubusercontent.com/${repo}/refs/heads/main/ports/${portId}/README.md`;

    fetch(readmeUrl)
      .then(res => {
        if (!res.ok) throw new Error('Not found');
        return res.text();
      })
      .then(md => {
        const html = window.marked ? window.marked.parse(md) : md;
        readmeCache[portId] = html;
        if (activePortId === portId) {
          readmeEl.innerHTML = html;
          wrapTables(readmeEl);
        }
      })
      .catch(() => {
        const fallback = '<p>No additional information available.</p>';
        readmeCache[portId] = fallback;
        if (activePortId === portId) readmeEl.innerHTML = fallback;
      });
  }

  function showPort() {
    const portId = getPortIdFromUrl();
    if (!portId) {
      setState('notfound');
      return;
    }

    if (portDetails) {
      const port = portDetails[portId];
      if (port) {
        renderPort(portId, port);
      } else {
        setState('notfound');
      }
      return;
    }

    setState('loading');
    fetch('../assets/json/port_details.json')
      .then(res => res.json())
      .then(data => {
        portDetails = data;
        const port = portDetails[portId];
        if (port) {
          renderPort(portId, port);
        } else {
          setState('notfound');
        }
      })
      .catch(() => setState('notfound'));
  }

  window.addEventListener('popstate', showPort);
  showPort();

  // ===== Share button =====
  const shareBtn = document.getElementById('port-share-btn');
  if (shareBtn) {
    shareBtn.addEventListener('click', async () => {
      const shareUrl = window.location.href;
      const shareTitle = document.getElementById('port-title').textContent;
      const shareData = {
        title: shareTitle,
        text: `Check out ${shareTitle} on PortMaster!`,
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
        showShareConfirmation();
      } catch (err) {
        const textArea = document.createElement('textarea');
        textArea.value = shareUrl;
        textArea.style.position = 'fixed';
        textArea.style.left = '-9999px';
        document.body.appendChild(textArea);
        textArea.select();
        try {
          document.execCommand('copy');
          showShareConfirmation();
        } catch (e) {
          console.error('Copy failed:', e);
        }
        document.body.removeChild(textArea);
      }
    });
  }

  function showShareConfirmation() {
    const originalHTML = shareBtn.innerHTML;
    shareBtn.innerHTML = '<i class="bi bi-check2"></i>';
    shareBtn.style.backgroundColor = '#28a745';
    setTimeout(() => {
      shareBtn.innerHTML = originalHTML;
      shareBtn.style.backgroundColor = '';
    }, 2000);
  }

  // ===== Device compatibility chip =====
  // Reads/writes the same "selectedDevice"/"selectedOS" cookies that
  // /games/ (Browse view) uses, so picking a device on either page carries over.
  function getCookie(name) {
    const nameEQ = name + '=';
    const parts = document.cookie.split(';');
    for (let i = 0; i < parts.length; i++) {
      let c = parts[i];
      while (c.charAt(0) === ' ') c = c.substring(1);
      if (c.indexOf(nameEQ) === 0) return decodeURIComponent(c.substring(nameEQ.length));
    }
    return null;
  }

  function setCookie(name, value, days) {
    const expires = days
      ? '; expires=' + new Date(Date.now() + days * 864e5).toUTCString()
      : '';
    document.cookie = `${name}=${encodeURIComponent(value)}${expires}; path=/`;
  }

  let currentPort = null;
  let deviceInfo = null;
  let runtimeArchAvailability = null;
  let currentDevice = null;
  let currentOS = null;

  const chipBtn = document.getElementById('device-chip-btn');
  const chipPopover = document.getElementById('device-chip-popover');
  const chipDot = document.getElementById('device-chip-dot');
  const chipHint = document.getElementById('device-chip-hint');
  const deviceSelect = document.getElementById('device-chip-device');
  const osSelect = document.getElementById('device-chip-os');

  function checkCompatibility(port, device, os) {
    if (!device || !os) return null;

    const capabilities = new Set((os.capabilities || []).map(c => c.toLowerCase()));
    const primaryArch = (os.primary_arch || '').toLowerCase();

    if (port.arch.length === 0) {
      if (port.runtime.length > 0) {
        const hasCompatibleRuntime = port.runtime.some(runtime => {
          const availableArchs = (runtimeArchAvailability && runtimeArchAvailability[runtime]) || [];
          return availableArchs.includes(primaryArch) || availableArchs.some(a => capabilities.has(a));
        });
        if (!hasCompatibleRuntime) return false;
      }
    } else {
      const requiredArches = port.arch.map(a => a.toLowerCase());
      let hasArch = requiredArches.includes(primaryArch) || requiredArches.includes('all');
      if (!hasArch) hasArch = requiredArches.some(a => capabilities.has(a));
      if (!hasArch) return false;
    }

    for (const req of port.reqs) {
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

  function updateDeviceChip() {
    if (!currentPort) return;

    if (!currentDevice || !currentOS) {
      chipBtn.title = 'Check compatibility with your device';
      chipDot.className = 'device-chip-dot';
      chipHint.textContent = '';
      chipHint.className = 'device-chip-hint';
      return;
    }

    const compatible = checkCompatibility(currentPort, currentDevice, currentOS);
    chipBtn.title = `${deviceSelect.value} · ${osSelect.value} — ${compatible ? 'Compatible' : 'May not be compatible'}`;
    chipDot.className = 'device-chip-dot ' + (compatible ? 'is-compatible' : 'is-incompatible');
    chipHint.textContent = compatible
      ? 'Compatible with your device.'
      : 'May not be compatible with your device.';
    chipHint.className = 'device-chip-hint ' + (compatible ? 'is-compatible' : 'is-incompatible');
  }

  function loadDeviceData() {
    if (deviceInfo) return Promise.resolve();
    return fetch('../assets/json/device_info.json')
      .then(res => res.json())
      .then(data => {
        deviceInfo = data;
        Object.keys(deviceInfo).forEach(name => deviceSelect.appendChild(new Option(name, name)));
        return fetch('../assets/json/runtime_archs.json');
      })
      .then(res => res.json())
      .then(archs => {
        runtimeArchAvailability = {};
        Object.entries(archs).forEach(([runtime, list]) => {
          runtimeArchAvailability[runtime] = (list || []).map(a => a.toLowerCase());
        });
        restoreDeviceSelection();
      })
      .catch(() => {});
  }

  function restoreDeviceSelection() {
    const savedDevice = getCookie('selectedDevice');
    if (savedDevice && deviceInfo[savedDevice]) {
      deviceSelect.value = savedDevice;
      populateOSOptions(savedDevice);
      const savedOS = getCookie('selectedOS');
      const osNames = Object.keys(deviceInfo[savedDevice]);
      if (savedOS && osNames.includes(savedOS)) {
        osSelect.value = savedOS;
        currentDevice = deviceInfo[savedDevice];
        currentOS = currentDevice[savedOS];
      }
    }
    updateDeviceChip();
  }

  function populateOSOptions(deviceName) {
    osSelect.innerHTML = '<option value="">Select OS...</option>';
    if (!deviceName) {
      osSelect.disabled = true;
      return;
    }
    Object.keys(deviceInfo[deviceName]).forEach(osName => osSelect.appendChild(new Option(osName, osName)));
    osSelect.disabled = false;
  }

  if (chipBtn) {
    chipBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = chipPopover.style.display !== 'none';
      if (isOpen) {
        chipPopover.style.display = 'none';
        return;
      }
      chipPopover.style.display = 'flex';
      loadDeviceData();
    });

    document.addEventListener('click', (e) => {
      if (!chipPopover.contains(e.target) && e.target !== chipBtn) {
        chipPopover.style.display = 'none';
      }
    });

    deviceSelect.addEventListener('change', () => {
      const deviceName = deviceSelect.value;
      populateOSOptions(deviceName);
      currentDevice = deviceName ? deviceInfo[deviceName] : null;
      currentOS = null;
      if (deviceName) {
        setCookie('selectedDevice', deviceName, 365);
      } else {
        setCookie('selectedDevice', '', -1);
      }
      setCookie('selectedOS', '', -1);
      updateDeviceChip();
    });

    osSelect.addEventListener('change', () => {
      const osName = osSelect.value;
      currentOS = osName && currentDevice ? currentDevice[osName] : null;
      if (osName) {
        setCookie('selectedOS', osName, 365);
      } else {
        setCookie('selectedOS', '', -1);
      }
      updateDeviceChip();
    });
  }
})();
