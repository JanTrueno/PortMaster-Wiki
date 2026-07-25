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

  function renderPort(portId, port) {
    document.title = `${port.title} - PortMaster Wiki`;

    document.getElementById('port-title').textContent = port.title;

    const screenshotContainer = document.getElementById('port-screenshot-container');
    const screenshotImg = document.getElementById('port-screenshot');
    if (port.screenshot) {
      screenshotImg.src = `https://raw.githubusercontent.com/${port.repo}/refs/heads/main/ports/${portId}/${port.screenshot}`;
      screenshotImg.alt = port.title;
      screenshotContainer.style.display = '';
    } else {
      screenshotContainer.style.display = 'none';
    }

    document.getElementById('port-desc').innerHTML = port.descHtml || '';

    const downloadBtn = document.getElementById('port-download-btn');
    downloadBtn.href = port.url || '#';

    document.getElementById('port-genres').innerHTML = badges(port.genres);
    document.getElementById('port-reqs').innerHTML = badges(port.reqs);
    document.getElementById('port-porter').innerHTML = porterLinks(port.porter);
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
      instSection.style.display = '';
    } else {
      instSection.style.display = 'none';
    }

    loadReadme(portId, port.repo);
    setState('content');
  }

  function loadReadme(portId, repo) {
    const readmeEl = document.getElementById('port-readme');

    if (readmeCache[portId]) {
      readmeEl.innerHTML = readmeCache[portId];
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
        if (location.hash.slice(1) === portId) readmeEl.innerHTML = html;
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
})();
