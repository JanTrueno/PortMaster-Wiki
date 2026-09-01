---
title: Gameinfo Generator - PortMaster Wiki

# No build-time images on this page for glightbox to wrap - everything is
# form fields and client-side rendered output. Same reasoning as
# games.md/cover-generator.md.
glightbox: false
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

# Gameinfo Generator

Use this form to generate a `gameinfo.xml` file for your port, right in your browser.
It matches the [Port Metadata Editor](https://portmaster.games/metadata-editor.html){:target="_blank" rel="noopener"}
on the main PortMaster site field for field and byte for byte - the download is
identical. See the [packaging documentation](../contribute/porting/packaging.md)
for where to place the file.

PortMaster installs this metadata into EmulationStation when a port is installed,
alongside the [cover image](cover-generator.md). Every field is optional - blank
ones are left out of the file entirely.

<div class="porter-tool porter-tool-panel">

<div class="filter-accordion open">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Load an existing port <small>*optional</small></span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="form-group">
      <label for="loadPort">Port</label>
      <div class="tool-inline-row">
        <input type="text" id="loadPort" list="portOptions" placeholder="Start typing a port name..." autocomplete="off" />
        <button type="button" class="add-row-btn" id="loadPortBtn">
          <i class="bi bi-download"></i>
          Load
        </button>
      </div>
      <datalist id="portOptions"></datalist>
      <p class="help-text" id="loadPortStatus">Fills the form with that port's current
      <code>gameinfo.xml</code> so you can edit it, rather than starting from scratch.</p>
    </div>
  </div>
</div>

<div class="filter-accordion open">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Game details</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="form-group">
      <label for="name">Name</label>
      <input type="text" id="name" placeholder="Game Name" />
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="path">Script Path</label>
        <input type="text" id="path" placeholder="./portname.sh" />
      </div>

      <div class="form-group">
        <label for="image">Image Path</label>
        <input type="text" id="image" placeholder="./portname/cover.png" />
        <p class="help-text">PortMaster falls back to the screenshot if no cover is set.</p>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="developer">Developer</label>
        <input type="text" id="developer" placeholder="Studio Name" />
      </div>

      <div class="form-group">
        <label for="publisher">Publisher</label>
        <input type="text" id="publisher" placeholder="Publisher Name" />
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="genre">Genre</label>
        <input type="text" id="genre" placeholder="Platformer" />
      </div>

      <div class="form-group">
        <label for="date">Release Date</label>
        <input type="date" id="date" />
      </div>
    </div>

    <div class="form-group">
      <label for="description">Description</label>
      <textarea id="description" placeholder="A short description of the game..."></textarea>
    </div>
  </div>
</div>

</div>

## Generated XML

<div class="porter-tool">
  <div class="output-container">
    <pre id="outputArea"><div class="output-placeholder">Fill in the form - the XML output updates live here...</div></pre>
  </div>

  <div class="action-buttons">
    <button type="button" class="primary-btn" id="downloadBtn">
      <i class="bi bi-download"></i>
      Download gameinfo.xml
    </button>
    <button type="button" class="secondary-btn" id="clearBtn">Clear form</button>
  </div>
  <p class="help-text" style="margin-top: 0.75rem;">The output updates live as you fill in the form.
  Ctrl/Cmd + Enter downloads.</p>
</div>

<script>
(function () {
  // Delegation root for the form's own input/change handling - .md-content
  // rather than document, so this doesn't also fire on the site search box,
  // which lives outside it and emits its own 'input' events while typing.
  const scope = document.querySelector('.md-content');
  const outputArea = document.getElementById('outputArea');
  const PLACEHOLDER = '<div class="output-placeholder">Fill in the form - the XML output updates live here...</div>';

  const FIELD_IDS = ['name', 'path', 'image', 'developer', 'publisher', 'genre', 'date', 'description'];

  // Same plain div + class-toggle accordion as the Browse filter panel
  // (games.md's initFilterAccordions) - not native <details>/<summary>,
  // which mkdocs-material restyles as an admonition.
  document.querySelectorAll('.filter-accordion-summary').forEach(summary => {
    summary.addEventListener('click', () => {
      summary.closest('.filter-accordion').classList.toggle('open');
    });
    summary.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        summary.closest('.filter-accordion').classList.toggle('open');
      }
    });
  });

  const val = id => document.getElementById(id).value;

  // XML text-node escaping, matching the serializer the upstream editor
  // gets from xmlbuilder2: &, < and > are all escaped in element content.
  function esc(value) {
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;');
  }

  // Mirrors metadata-editor.html's getFormValues(): a date of YYYY-MM-DD
  // becomes YYYYMMDDT000000, empty fields are omitted entirely, and the
  // element order below is the order that function assigns them in - which
  // is what the serializer then writes, so it is not the same as the form's
  // visual order. Output is 2-space indented with a double-quoted XML
  // declaration, matching a tool-generated file such as ports/angband.
  function buildXml() {
    let date = val('date');
    if (date !== '') date = date.replaceAll('-', '') + 'T000000';

    const fields = [
      ['path', val('path')],
      ['name', val('name')],
      ['desc', val('description')],
      ['releasedate', date],
      ['developer', val('developer')],
      ['publisher', val('publisher')],
      ['genre', val('genre')],
      ['image', val('image')]
    ].filter(([, value]) => value !== '');

    const lines = ['<?xml version="1.0" encoding="utf-8"?>', '<gameList>'];
    if (fields.length === 0) {
      // An empty <game> serializes self-closing, same as the upstream tool
      // building from an empty object.
      lines.push('  <game/>');
    } else {
      lines.push('  <game>');
      fields.forEach(([tag, value]) => lines.push(`    <${tag}>${esc(value)}</${tag}>`));
      lines.push('  </game>');
    }
    lines.push('</gameList>');
    return lines.join('\n');
  }

  function isEmpty() {
    return FIELD_IDS.every(id => val(id).trim() === '');
  }

  function refreshOutput() {
    if (isEmpty()) {
      outputArea.innerHTML = PLACEHOLDER;
    } else {
      outputArea.textContent = buildXml();
    }
  }

  function downloadXml() {
    if (isEmpty()) {
      alert('Fill in at least one field first.');
      return;
    }
    const blob = new Blob([buildXml()], { type: 'application/xml' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'gameinfo.xml';
    a.click();
    URL.revokeObjectURL(a.href);
  }

  // ===== Load an existing port =====
  const loadInput = document.getElementById('loadPort');
  const loadStatus = document.getElementById('loadPortStatus');
  const portOptions = document.getElementById('portOptions');
  let portsById = {};

  // The wiki already ships this file for the games pages, so the port list
  // costs no extra request against GitHub. Two levels up, not one: this
  // page is served from /tools/gameinfo-generator/, so '../' would resolve
  // to /tools/ rather than the site root.
  fetch('../../assets/json/port_details.json')
    .then(r => r.ok ? r.json() : Promise.reject(new Error('network')))
    .then(details => {
      Object.entries(details)
        .sort((a, b) => (a[1].title || a[0]).localeCompare(b[1].title || b[0]))
        .forEach(([id, port]) => {
          const title = port.title || id;
          portsById[title.toLowerCase()] = { id, repo: port.repo };
          portsById[id.toLowerCase()] = { id, repo: port.repo };
          const opt = document.createElement('option');
          opt.value = title;
          portOptions.appendChild(opt);
        });
    })
    .catch(() => {
      loadStatus.textContent = "Couldn't load the port list. You can still fill the form in by hand.";
    });

  function setStatus(message, isError) {
    loadStatus.textContent = message;
    loadStatus.style.color = isError ? '#dc3545' : '';
  }

  // Parsed with DOMParser rather than by hand: a description can legally
  // contain escaped markup, and re-implementing entity decoding to read it
  // back would be a second place for the escaping to drift.
  function applyXml(xmlText) {
    const doc = new DOMParser().parseFromString(xmlText, 'application/xml');
    if (doc.querySelector('parsererror')) throw new Error('malformed XML');

    const text = tag => {
      const el = doc.querySelector('gameList > game > ' + tag);
      return el ? el.textContent : '';
    };

    document.getElementById('name').value = text('name');
    document.getElementById('path').value = text('path');
    document.getElementById('image').value = text('image');
    document.getElementById('developer').value = text('developer');
    document.getElementById('publisher').value = text('publisher');
    document.getElementById('genre').value = text('genre');
    document.getElementById('description').value = text('desc');

    // YYYYMMDDT000000 back to the YYYY-MM-DD an <input type="date"> wants.
    const raw = text('releasedate');
    document.getElementById('date').value = raw
      ? `${raw.slice(0, 4)}-${raw.slice(4, 6)}-${raw.slice(6, 8)}`
      : '';

    refreshOutput();
  }

  function loadPort() {
    const typed = loadInput.value.trim();
    if (!typed) {
      setStatus('Enter a port name first.', true);
      return;
    }
    const match = portsById[typed.toLowerCase()];
    if (!match) {
      setStatus(`No port called "${typed}".`, true);
      return;
    }

    setStatus('Loading…', false);
    const url = `https://raw.githubusercontent.com/${match.repo}/refs/heads/main/ports/${match.id}/gameinfo.xml`;
    fetch(url)
      .then(r => r.ok ? r.text() : Promise.reject(new Error('not found')))
      .then(xml => {
        applyXml(xml);
        setStatus(`Loaded metadata for ${typed}.`, false);
      })
      .catch(() => setStatus(`${typed} has no gameinfo.xml yet - fill the form in by hand.`, true));
  }

  document.getElementById('loadPortBtn').addEventListener('click', loadPort);
  loadInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); loadPort(); }
  });

  document.getElementById('downloadBtn').addEventListener('click', downloadXml);
  document.getElementById('clearBtn').addEventListener('click', () => {
    FIELD_IDS.forEach(id => { document.getElementById(id).value = ''; });
    loadInput.value = '';
    setStatus('Fills the form with that port’s current gameinfo.xml so you can edit it, rather than starting from scratch.', false);
    refreshOutput();
  });

  scope.addEventListener('input', refreshOutput);
  scope.addEventListener('change', refreshOutput);

  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      downloadXml();
    }
  });

  refreshOutput();
})();
</script>
