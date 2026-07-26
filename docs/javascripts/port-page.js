(function () {
  const root = document.getElementById('port-page-root');
  if (!root) return;

  const loadingEl = document.getElementById('port-page-loading');
  const notFoundEl = document.getElementById('port-page-notfound');
  const contentEl = document.getElementById('port-page-content');

  let portDetails = null;
  const readmeCache = {};

  function setState(state) {
    loadingEl.style.display = state === 'loading' ? '' : 'none';
    notFoundEl.style.display = state === 'notfound' ? '' : 'none';
    contentEl.style.display = state === 'content' ? '' : 'none';
  }

  function badges(values) {
    if (!values || values.length === 0) return '—';
    return values.map(v => `<span class="info-badge">${escapeHtml(v)}</span>`).join('');
  }

  function porterLinks(values) {
    if (!values || values.length === 0) return '—';
    return values
      .map(v => `<a href="../porters/#porter-${encodeURIComponent(v)}" class="porter-link-badge">${escapeHtml(v)} <i class="bi bi-box-arrow-up-right"></i></a>`)
      .join(' ');
  }

  function escapeHtml(value) {
    const div = document.createElement('div');
    div.textContent = value;
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

  // Bootstrap Icons only ships a real brand glyph for Steam; other
  // storefronts fall back to a generic icon rather than a wrong logo.
  function storeIcon(name) {
    const n = (name || '').toLowerCase();
    if (n.includes('steam')) return 'bi-steam';
    if (n.includes('itch')) return 'bi-joystick';
    if (n.includes('gog')) return 'bi-shop-window';
    if (n.includes('epic')) return 'bi-controller';
    return 'bi-box-arrow-up-right';
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
        .map(s => `<a href="${s.url}" target="_blank" rel="noopener" class="port-store-link" title="${escapeHtml(shortStoreName(s.name))}"><i class="bi ${storeIcon(s.name)}"></i> <span class="port-store-label">${escapeHtml(shortStoreName(s.name))}</span></a>`)
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
    document.getElementById('port-misc').innerHTML = port.rtr
      ? '<span class="info-badge">Ready to Run</span>'
      : '<span class="info-badge">Setup Required</span>';

    const instSection = document.getElementById('port-inst-section');
    const instEl = document.getElementById('port-inst');
    if (port.instHtml) {
      instEl.innerHTML = port.instHtml;
      wrapTables(instEl);
      instSection.style.display = '';
    } else {
      instSection.style.display = 'none';
    }

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
        if (location.hash.slice(1) === portId) {
          readmeEl.innerHTML = html;
          wrapTables(readmeEl);
        }
      })
      .catch(() => {
        const fallback = '<p>No additional information available.</p>';
        readmeCache[portId] = fallback;
        if (location.hash.slice(1) === portId) readmeEl.innerHTML = fallback;
      });
  }

  function showPort() {
    const portId = decodeURIComponent(location.hash.slice(1));
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

  window.addEventListener('hashchange', showPort);
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
  // /all-games/ uses, so picking a device on either page carries over.
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
