---
title: Port JSON Generator - PortMaster Wiki

# No build-time images on this page for glightbox to wrap - everything is
# form fields and client-side rendered output. Same reasoning as
# games.md/cover-generator.md.
glightbox: false
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

# Port JSON Generator

Use this form to generate a `port.json` file for your port, right in your browser.
The porter, runtime and device lists are rebuilt every hour, so they stay current.
See the [packaging documentation](../contribute/porting/packaging.md) for where to
place the file.

<div class="porter-tool porter-tool-panel">

<div class="filter-accordion open">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Basics</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="form-row">
      <div class="form-group">
        <label for="title">Port Title</label>
        <input type="text" id="title" placeholder="Game Name" />
      </div>

      <div class="form-group">
        <label for="zipName">Zip File Name</label>
        <input type="text" id="zipName" placeholder="gamename.zip" />
        <p class="help-text">Uniquely identifies the port, e.g. <code>gamename.zip</code></p>
      </div>
    </div>

    <div class="form-row">
      <div class="form-group">
        <label for="scriptName">Script Name</label>
        <input type="text" id="scriptName" placeholder="Game Name.sh" />
        <p class="help-text">The port's launch script, ending in <code>.sh</code>. A port has one.</p>
      </div>

      <div class="form-group">
        <label for="dirName">Directory Name</label>
        <input type="text" id="dirName" placeholder="gamename" />
        <p class="help-text">The port folder name (lowercase, no spaces)</p>
      </div>
    </div>
  </div>
</div>

<div class="filter-accordion">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Genres &amp; Porter</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="form-group">
      <label>Genres</label>
      <div class="tool-check-grid" id="genreList">
        <label class="filter-checkbox-item"><input type="checkbox" value="action" /><span>Action</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="adventure" /><span>Adventure</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="arcade" /><span>Arcade</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="casino/card" /><span>Casino/Card</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="fps" /><span>First Person Shooter (FPS)</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="platformer" /><span>Platformer</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="puzzle" /><span>Puzzle</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="racing" /><span>Racing</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="rhythm" /><span>Rhythm</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="rpg" /><span>Role-playing game (RPG)</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="simulation" /><span>Simulation</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="sports" /><span>Sports</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="strategy" /><span>Strategy</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="visual novel" /><span>Visual Novel</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="other" /><span>Other</span></label>
      </div>
    </div>

    <div class="form-group">
      <label for="porter">Porter</label>
      <select id="porter" multiple size="6">
{%- for porter_name in porters | sort(case_sensitive=false) %}
<option value="{{ porter_name | e }}">{{ porter_name | e }}</option>
{%- endfor %}
      </select>
      <p class="help-text">Hold Ctrl/Cmd to select multiple. This is every porter credited in the library.
      Not listed yet? Add yourself below.</p>
    </div>

    <div class="form-group">
      <label for="addPorter">Add Porter</label>
      <div class="tool-inline-row">
        <input type="text" id="addPorter" placeholder="YourPorterName" />
        <button type="button" class="add-row-btn" id="addPorterBtn">
          <i class="bi bi-plus-lg"></i>
          Add
        </button>
      </div>
    </div>
  </div>
</div>

<div class="filter-accordion">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Description &amp; Instructions</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="form-group">
      <label for="description">Description (plain text)</label>
      <textarea id="description" placeholder="Brief game description (plain text)"></textarea>
    </div>

    <div class="form-group">
      <label for="descriptionMd">Description (markdown) <small>*optional</small></label>
      <textarea id="descriptionMd" placeholder="Detailed description with markdown formatting (optional)"></textarea>
    </div>

    <div class="form-group">
      <label for="instructions">Instructions (plain text)</label>
      <textarea id="instructions" placeholder="Installation instructions (plain text)"></textarea>
    </div>

    <div class="form-group">
      <label for="instructionsMd">Instructions (markdown) <small>*optional</small></label>
      <textarea id="instructionsMd" placeholder="Installation instructions with markdown formatting (optional)"></textarea>
    </div>
  </div>
</div>

<div class="filter-accordion">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Runtime &amp; Architecture</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="form-group">
      <label for="runtime">Runtime (optional)</label>
      <select id="runtime" multiple size="8">
        <option disabled>Loading runtimes...</option>
      </select>
      <p class="help-text" id="runtimeHelp">Hold Ctrl/Cmd to select multiple. Leave unselected if no runtime is needed.
      Architectures in brackets are the ones the runtime is built for.</p>
    </div>

    <div class="form-group">
      <label>Architecture</label>
      <div class="tool-check-grid" id="archList">
        <label class="filter-checkbox-item"><input type="checkbox" value="aarch64" /><span>AArch64</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="armhf" /><span>ARMHF</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="x86_64" /><span>x86_64</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="x86" /><span>x86</span></label>
      </div>
      <p class="help-text" id="archHelp">Required, unless the port uses a runtime. PortMaster takes the
      architectures from the runtime when there is one and ignores this list.</p>
    </div>
  </div>
</div>

<div class="filter-accordion">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Flags &amp; Availability</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="form-group">
      <label class="filter-checkbox-item">
        <input type="checkbox" id="rtr" />
        <span>Ready To Run</span>
      </label>
      <p class="help-text">This port is ready to run with all files required. If it only includes demo game files please specify in the description.</p>
    </div>

    <div class="form-group">
      <label class="filter-checkbox-item">
        <input type="checkbox" id="exp" />
        <span>Experimental</span>
      </label>
      <p class="help-text">This port is experimental and should not be visible unless the feature is enabled in PortMaster.</p>
    </div>

    <div class="form-group">
      <label for="availability">Availability</label>
      <select id="availability">
        <option value="full">Free game, all files included</option>
        <option value="demo">Demo files included</option>
        <option value="free">Free external assets needed</option>
        <option value="paid">Paid external assets needed</option>
      </select>
    </div>
  </div>
</div>

<div class="filter-accordion">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Store Links</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <table class="controls-table" id="storeTable">
      <thead>
        <tr>
          <th style="width: 20%;">Store Name</th>
          <th style="width: 38%;">Game URL</th>
          <th style="width: 34%;">Developer URL</th>
          <th class="row-actions"></th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <datalist id="storeNames">
      <option value="Steam"></option>
      <option value="itch.io"></option>
      <option value="GOG"></option>
      <option value="Epic Games"></option>
      <option value="Humble Bundle"></option>
      <option value="Game Jolt"></option>
      <option value="Newgrounds"></option>
      <option value="Google Play Store"></option>
      <option value="App Store"></option>
      <option value="Microsoft Store"></option>
      <option value="GitHub"></option>
    </datalist>
    <p class="help-text">Pick a store from the list so the name is spelled the way the site shows it.
    Leave the name empty and it's filled in from the game URL when it's a store we recognise.</p>
    <div class="table-actions">
      <button type="button" class="add-row-btn" id="addStoreBtn">
        <i class="bi bi-plus-lg"></i>
        Add Link
      </button>
      <button type="button" class="clear-btn" id="clearStoresBtn">
        Clear Store Links
      </button>
    </div>
  </div>
</div>

<div class="filter-accordion">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Requirements &amp; Compatibility</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <p class="help-text req-intro">Click a tag once to <strong>require</strong> it and again to
    <strong>exclude</strong> it. A third click clears it. The grid below shows which devices would
    list the port. Leave everything clear if the port should show on every device.</p>

    <div id="reqStatus" class="req-status">Loading device data...</div>
    <div id="reqTags" class="req-tags"></div>

    <div class="form-group">
      <label for="minGlibc">Minimum glibc <small>*optional</small></label>
      <input type="text" id="minGlibc" placeholder="2.35" inputmode="decimal" />
      <p class="help-text">Only fill this in if your port supplies its own binaries. Devices with an older glibc
      won't list the port. 2.35 is Ubuntu 22.04, which we build on. Leave it empty if the port runs on older
      CFWs like ArkOS.</p>
    </div>

    <div id="reqSummary" class="req-summary" aria-live="polite"></div>
    <div class="req-grid-scroll"><div id="reqGrid"></div></div>
    <p class="help-text req-note" id="reqNote"></p>
  </div>
</div>

</div>

## Generated JSON

<div class="porter-tool">
  <div class="alert alert-warning" id="jsonValidation" style="display:none"></div>

  <div class="output-container">
    <pre id="outputArea"><div class="output-placeholder">Fill in the form - the JSON output updates live here...</div></pre>
  </div>

  <div class="action-buttons">
    <button type="button" class="primary-btn" id="downloadBtn">
      <i class="bi bi-download"></i>
      Download port.json
    </button>
  </div>
  <p class="help-text" style="margin-top: 0.75rem;">The output updates live as you fill in the form.
  Ctrl/Cmd + Enter downloads.</p>
</div>

<script>
(function () {
  // Delegation root for the form's own input/change/click handling below -
  // .md-content rather than document, so this doesn't also fire on
  // unrelated page chrome (the site search box lives outside it and emits
  // its own 'input' events while typing).
  const scope = document.querySelector('.md-content');
  const porterSelect = document.getElementById('porter');
  const runtimeSelect = document.getElementById('runtime');
  const outputArea = document.getElementById('outputArea');
  const validationBox = document.getElementById('jsonValidation');

  // Same plain div + class-toggle accordion as the Browse filter panel
  // (games.md's initFilterAccordions) - not native <details>/<summary>,
  // which mkdocs-material restyles as an admonition and would fight this
  // component's own look.
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

  function checkedValues(listId) {
    return Array.from(document.querySelectorAll('#' + listId + ' input:checked'))
      .map(i => i.value)
      .filter(v => v !== '');
  }

  function esc(text) {
    const d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
  }

  // innerHTML leaves quotes alone, which is fine in text but not inside an
  // attribute value.
  function escAttr(text) {
    return esc(text).replace(/"/g, '&quot;');
  }

  // ===================================================================
  // Data. All of it is the wiki's own, rebuilt hourly with the site:
  //   device_info.json   what each device and firmware reports
  //   runtime_archs.json each runtime and the architectures it exists for
  // The porter list is rendered into the page at build time instead.
  // ===================================================================
  let devices = null;       // device_info.json, or null until it loads
  let runtimeArchs = {};    // 'frt_3.5.2.squashfs' -> ['aarch64', ...]
  let vocabulary = [];      // the requirement tags the picker offers
  const tagState = new Map(); // tag -> 'req' | 'exc'

  // ===================================================================
  // Requirement tags
  //
  // PortMaster hides a port from a device unless every entry in `reqs`
  // holds against the device's capability list: 'x' needs the tag, '!x'
  // forbids it, 'a|b' needs either. The picker offers every tag that
  // appears anywhere in the device data, so it can't fall behind it.
  // ===================================================================
  const CATEGORIES = [
    { id: 'features',   title: 'Hardware',          any: false },
    { id: 'analog',     title: 'Analog sticks',     any: false },
    { id: 'ram',        title: 'RAM',               any: false },
    { id: 'ratio',      title: 'Screen shape',      any: true  },
    { id: 'resolution', title: 'Screen resolution', any: true  },
    { id: 'firmware',   title: 'Firmware',          any: true,  collapsed: true },
    { id: 'device',     title: 'Devices',           any: true,  collapsed: true }
  ];

  // What each tag means. Anything not listed gets a generic description.
  const DESCRIPTIONS = {
    opengl: 'Desktop OpenGL, not just OpenGL ES',
    power: 'More powerful than an RK3326 handheld',
    ultra: 'Flagship devices with plenty of RAM',
    hires: 'High-resolution screen, above 640x480',
    lowres: 'Low-resolution screen, below 640x480',
    wide: 'Wide screen',
    analog_1: 'At least one analog stick',
    analog_2: 'Two analog sticks'
  };

  const FEATURE_TAGS = ['opengl', 'power', 'ultra', 'hires', 'lowres', 'wide'];

  // Tags the picker leaves out. Every device reports analog_0 and 1gb, so
  // requiring them says nothing, 427:240 and 30:17 are only what 854x480 and
  // 960x544 panels reduce to, not shapes a port is written for, and restore
  // is the PortMaster restore port's own switch.
  const HIDDEN_TAGS = new Set(['analog_0', '1gb', '427:240', '30:17', 'restore']);
  const ARCH_TAGS = ['aarch64', 'armhf', 'x86', 'x86_64'];

  function ramOrder(tag) { return parseInt(tag, 10); }
  function resOrder(tag) { return -parseInt(tag, 10); }

  function buildVocabulary(data) {
    const found = new Set();
    const firmware = new Set();
    const deviceIds = new Set();
    for (const model of Object.values(data)) {
      for (const info of Object.values(model)) {
        (info.capabilities || []).forEach(c => found.add(c));
        if (info.name) firmware.add(info.name);
        if (info.device) deviceIds.add(info.device);
      }
    }

    const classify = tag => {
      if (ARCH_TAGS.includes(tag)) return null;       // set by the architecture fields
      if (HIDDEN_TAGS.has(tag)) return null;
      if (FEATURE_TAGS.includes(tag)) return 'features';
      if (/^analog_\d+$/.test(tag)) return 'analog';
      if (/^\d+gb$/.test(tag)) return 'ram';
      if (/^\d+:\d+$/.test(tag)) return 'ratio';
      if (/^\d+x\d+$/.test(tag)) return 'resolution';
      if (firmware.has(tag)) return 'firmware';
      if (deviceIds.has(tag)) return 'device';
      return null;                                    // not something the picker handles
    };

    const items = [];
    found.forEach(tag => {
      const category = classify(tag);
      if (category) items.push({ tag, category });
    });

    const featureRank = t => FEATURE_TAGS.indexOf(t);
    const sorters = {
      features: (a, b) => featureRank(a.tag) - featureRank(b.tag),
      ram: (a, b) => ramOrder(a.tag) - ramOrder(b.tag),
      resolution: (a, b) => resOrder(a.tag) - resOrder(b.tag)
    };
    items.sort((a, b) => {
      const ca = CATEGORIES.findIndex(c => c.id === a.category);
      const cb = CATEGORIES.findIndex(c => c.id === b.category);
      if (ca !== cb) return ca - cb;
      const sorter = sorters[a.category];
      return sorter ? sorter(a, b) : a.tag.localeCompare(b.tag, undefined, { numeric: true });
    });
    return items;
  }

  function describeTag(item) {
    if (DESCRIPTIONS[item.tag]) return DESCRIPTIONS[item.tag];
    switch (item.category) {
      case 'ram': return item.tag.replace('gb', ' GB of RAM or more');
      case 'ratio': return 'Screen ratio ' + item.tag;
      case 'resolution': return 'A ' + item.tag + ' screen';
      case 'firmware': return 'Running this firmware';
      case 'device': return 'This device';
      default: return item.tag;
    }
  }

  function tagLabel(tag, state) {
    return tag + ': ' + (state === 'req' ? 'required' : state === 'exc' ? 'excluded' : 'not set');
  }

  function renderTags() {
    const container = document.getElementById('reqTags');
    container.innerHTML = '';
    CATEGORIES.forEach(cat => {
      const items = vocabulary.filter(v => v.category === cat.id);
      if (!items.length) return;

      const group = document.createElement('div');
      group.className = 'req-group' + (cat.collapsed ? ' is-collapsed' : '');

      const head = document.createElement('button');
      head.type = 'button';
      head.className = 'req-group-title';
      head.innerHTML = '<span>' + esc(cat.title) + (cat.any ? ' <small>(several = any of them)</small>' : '') +
        '</span><i class="bi bi-chevron-down"></i>';
      head.addEventListener('click', () => group.classList.toggle('is-collapsed'));
      group.appendChild(head);

      const list = document.createElement('div');
      list.className = 'req-taglist';
      items.forEach(item => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'req-tag';
        btn.dataset.tag = item.tag;
        btn.title = describeTag(item);
        btn.textContent = item.tag;
        btn.setAttribute('aria-label', tagLabel(item.tag, null) + '. ' + describeTag(item));
        btn.addEventListener('click', () => cycleTag(item.tag));
        list.appendChild(btn);
      });
      group.appendChild(list);
      container.appendChild(group);
    });
    syncTagButtons();
  }

  function cycleTag(tag) {
    const next = { undefined: 'req', req: 'exc', exc: undefined }[tagState.get(tag)];
    if (next) tagState.set(tag, next); else tagState.delete(tag);
    syncTagButtons();
    refreshAll();
  }

  function syncTagButtons() {
    document.querySelectorAll('#reqTags .req-tag').forEach(btn => {
      const state = tagState.get(btn.dataset.tag);
      btn.classList.toggle('is-required', state === 'req');
      btn.classList.toggle('is-excluded', state === 'exc');
      const item = vocabulary.find(v => v.tag === btn.dataset.tag);
      btn.setAttribute('aria-label', tagLabel(btn.dataset.tag, state) + '. ' + (item ? describeTag(item) : ''));
    });
  }

  // The picker's choices as a `reqs` array. Required tags in a category that
  // says "any" (shapes, resolutions, firmware, devices) are joined with '|':
  // requiring two screen ratios at once can never be true, so the useful
  // reading is either one. Everything else is one entry per tag.
  function pickedRequirements() {
    const reqs = [];
    CATEGORIES.forEach(cat => {
      const inCat = vocabulary.filter(v => v.category === cat.id);
      const required = inCat.filter(v => tagState.get(v.tag) === 'req').map(v => v.tag);
      const excluded = inCat.filter(v => tagState.get(v.tag) === 'exc').map(v => '!' + v.tag);
      if (cat.any && required.length) reqs.push(required.join('|'));
      else required.forEach(t => reqs.push(t));
      excluded.forEach(t => reqs.push(t));
    });
    return reqs;
  }

  // ===================================================================
  // Compatibility grid
  // ===================================================================

  // Mirrors PortMaster's match_requirements() (harbourmaster/util/data.py),
  // except that it reports every entry that fails and not just the first.
  function checkRequirements(capabilities, requirements) {
    const reasons = [];
    for (const raw of requirements) {
      if (raw === '') continue;
      const exclude = raw.startsWith('!');
      const req = exclude ? raw.slice(1) : raw;
      const has = req.includes('|')
        ? req.split('|').some(r => capabilities.includes(r))
        : capabilities.includes(req);
      if (has === exclude) {
        reasons.push((exclude ? 'Excluded if: ' : 'Needs: ') + req.split('|').join(' or '));
      }
    }
    return reasons;
  }

  function versionParts(v) { return String(v).split('.').map(n => parseInt(n, 10) || 0); }
  function olderThan(a, b) {
    const x = versionParts(a), y = versionParts(b);
    for (let i = 0; i < Math.max(x.length, y.length); i++) {
      const d = (x[i] || 0) - (y[i] || 0);
      if (d) return d < 0;
    }
    return false;
  }

  // What PortMaster adds on its own: a runtime port needs a device that can
  // run one of the runtime's architectures, and a port without a runtime needs
  // one of its own listed architectures.
  function implicitRequirements() {
    const picked = Array.from(runtimeSelect.selectedOptions).map(o => o.value);
    if (picked.length) {
      return picked.map(r => (runtimeArchs[r] || []).join('|')).filter(Boolean);
    }
    const arch = checkedValues('archList');
    return arch.length ? [arch.join('|')] : [];
  }

  // The same firmware shows up spelled differently for different devices
  // ('Knulli' and 'KNULLI'), so columns are grouped ignoring case.
  function firmwareColumns(data) {
    const spellings = new Map();
    for (const model of Object.values(data)) {
      for (const fw of Object.keys(model)) {
        const key = fw.toLowerCase();
        const counts = spellings.get(key) || new Map();
        counts.set(fw, (counts.get(fw) || 0) + 1);
        spellings.set(key, counts);
      }
    }
    return Array.from(spellings.entries())
      .map(([key, counts]) => ({ key, label: Array.from(counts.entries()).sort((a, b) => b[1] - a[1])[0][0] }))
      .sort((a, b) => a.label.localeCompare(b.label));
  }

  function renderGrid() {
    const grid = document.getElementById('reqGrid');
    const summary = document.getElementById('reqSummary');
    const note = document.getElementById('reqNote');
    if (!devices) { grid.innerHTML = ''; summary.textContent = ''; return; }

    const requirements = pickedRequirements();
    const all = requirements.concat(implicitRequirements());
    const minGlibc = document.getElementById('minGlibc').value.trim();
    const glibcOk = /^\d+(\.\d+)*$/.test(minGlibc) ? minGlibc : '';

    const columns = firmwareColumns(devices);
    const models = Object.keys(devices).sort((a, b) => a.localeCompare(b));
    let shown = 0, total = 0;
    let html = '<table class="req-grid"><thead><tr><th>Device</th>';
    columns.forEach(c => { html += '<th>' + esc(c.label) + '</th>'; });
    html += '</tr></thead><tbody>';

    models.forEach(model => {
      html += '<tr><th scope="row">' + esc(model) + '</th>';
      const byKey = {};
      Object.entries(devices[model]).forEach(([fw, info]) => { byKey[fw.toLowerCase()] = info; });
      columns.forEach(col => {
        const info = byKey[col.key];
        if (!info) { html += '<td class="is-na" aria-label="not available">&ndash;</td>'; return; }
        total++;
        const reasons = checkRequirements(info.capabilities || [], all);
        if (glibcOk && info.glibc && olderThan(info.glibc, glibcOk)) {
          reasons.push('Needs glibc ' + glibcOk + ' (this has ' + info.glibc + ')');
        }
        if (reasons.length) {
          html += '<td class="is-fail" title="' + escAttr(reasons.join('\n')) + '" aria-label="hidden: ' + escAttr(reasons.join('; ')) + '">&#10005;</td>';
        } else {
          shown++;
          html += '<td class="is-pass" aria-label="listed">&#10003;</td>';
        }
      });
      html += '</tr>';
    });
    html += '</tbody></table>';
    grid.innerHTML = html;

    let text = 'Listed on <strong>' + shown + '</strong> of ' + total + ' device and firmware combinations.';
    if (total && shown === 0) text += ' <span class="req-warn">No device matches. Check for tags that contradict each other.</span>';
    summary.innerHTML = text;

    const implicit = implicitRequirements();
    const notes = [];
    if (implicit.length) notes.push('Also applied by PortMaster from the runtime or architecture: ' + implicit.join(', ') + '.');
    notes.push('Based on the website\'s device data, which is older than PortMaster\'s current device detection. ' +
      'Treat the grid as a guide, and test on a real device.');
    note.textContent = notes.join(' ');
  }

  // ===================================================================
  // Runtimes
  // ===================================================================
  const RUNTIME_FAMILIES = [
    { title: 'Godot 4 (.NET)',   test: n => /^godot_.*\.mono\./.test(n) },
    { title: 'Godot 4',          test: n => /^godot_/.test(n) },
    { title: 'Godot 3 / FRT',    test: n => /^frt_/.test(n) },
    { title: '.NET and Mono',    test: n => /^(dotnet|mono)/.test(n) },
    { title: 'Java',             test: n => /^zulu/.test(n) },
    { title: 'Python and Pyxel', test: n => /^(pyxel|python)/.test(n) },
    { title: "Ren'Py",           test: n => /^renpy/.test(n) }
  ];

  function renderRuntimes() {
    const names = Object.keys(runtimeArchs).filter(n => n.endsWith('.squashfs'));
    const groups = new Map();
    names.forEach(name => {
      const family = (RUNTIME_FAMILIES.find(f => f.test(name)) || { title: 'Other' }).title;
      if (!groups.has(family)) groups.set(family, []);
      groups.get(family).push(name);
    });
    const order = RUNTIME_FAMILIES.map(f => f.title).concat('Other');
    runtimeSelect.innerHTML = '';
    order.filter(t => groups.has(t)).forEach(title => {
      const og = document.createElement('optgroup');
      og.label = title;
      // Newest version first, so the one you want is at the top of its group.
      groups.get(title).sort((a, b) => b.localeCompare(a, undefined, { numeric: true })).forEach(name => {
        const opt = document.createElement('option');
        opt.value = name;
        const archs = (runtimeArchs[name] || []).join(', ');
        opt.textContent = name.replace(/\.squashfs$/, '') + (archs ? '  [' + archs + ']' : '');
        og.appendChild(opt);
      });
      runtimeSelect.appendChild(og);
    });
  }

  // ===================================================================
  // The file
  // ===================================================================
  // Key order and layout follow the port.json files already in the ports repo:
  // 2-space indentation, items_opt: [], image: null, and min_glibc: "" unless set.
  function buildPortJson() {
    const items = [document.getElementById('scriptName').value, document.getElementById('dirName').value];

    const store = Array.from(document.querySelectorAll('#storeTable tbody tr')).map(row => ({
      name: row.querySelector('.store-name').value,
      gameurl: row.querySelector('.store-game-url').value,
      developerurl: row.querySelector('.store-dev-url').value
    }));

    return {
      version: 4,
      name: document.getElementById('zipName').value,
      items: items,
      items_opt: [],
      attr: {
        title: document.getElementById('title').value,
        porter: Array.from(porterSelect.selectedOptions).map(o => o.value),
        desc: document.getElementById('description').value,
        desc_md: document.getElementById('descriptionMd').value || null,
        inst: document.getElementById('instructions').value,
        inst_md: document.getElementById('instructionsMd').value || null,
        genres: checkedValues('genreList'),
        image: null,
        rtr: document.getElementById('rtr').checked,
        exp: document.getElementById('exp').checked,
        runtime: Array.from(runtimeSelect.selectedOptions).map(o => o.value),
        store: store,
        availability: document.getElementById('availability').value,
        reqs: pickedRequirements(),
        arch: checkedValues('archList'),
        min_glibc: document.getElementById('minGlibc').value.trim()
      }
    };
  }

  function validateForm() {
    const missing = [];
    const script = document.getElementById('scriptName').value.trim();
    if (!document.getElementById('title').value.trim()) missing.push('Port Title');
    if (!document.getElementById('zipName').value.trim()) missing.push('Zip File Name');
    if (!script) missing.push('Script Name');
    else if (script.includes(',')) missing.push('Script Name (a port has one script, remove the comma)');
    else if (!/\.sh$/i.test(script)) missing.push('Script Name (must end in .sh)');
    if (!document.getElementById('dirName').value.trim()) missing.push('Directory Name');
    if (!checkedValues('genreList').length) missing.push('Genre (at least one)');
    if (!porterSelect.selectedOptions.length) missing.push('Porter (at least one)');
    if (!document.getElementById('description').value.trim()) missing.push('Description');
    if (!document.getElementById('instructions').value.trim()) missing.push('Instructions');
    // A runtime brings its own architectures, so only a port without one
    // has to say which it runs on.
    if (!runtimeSelect.selectedOptions.length && !checkedValues('archList').length) {
      missing.push('Architecture (at least one, or pick a runtime)');
    }
    const glibc = document.getElementById('minGlibc').value.trim();
    if (glibc && !/^\d+(\.\d+)*$/.test(glibc)) missing.push('Minimum glibc (a version like 2.32)');
    return missing;
  }

  function refreshOutput() {
    outputArea.textContent = JSON.stringify(buildPortJson(), null, 2);
  }

  function refreshAll() {
    refreshOutput();
    renderGrid();
  }

  function downloadJSON() {
    const missing = validateForm();
    if (missing.length) {
      validationBox.innerHTML = '<strong>Missing or invalid:</strong> ' + missing.map(esc).join(', ');
      validationBox.style.display = 'block';
      validationBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }
    validationBox.style.display = 'none';

    const blob = new Blob([JSON.stringify(buildPortJson(), null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'port.json';
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function addPorter() {
    const input = document.getElementById('addPorter');
    const name = input.value.trim();
    if (!name) return;
    let opt = Array.from(porterSelect.options).find(o => o.value.toLowerCase() === name.toLowerCase());
    if (!opt) {
      opt = document.createElement('option');
      opt.value = name;
      opt.textContent = name;
      porterSelect.insertBefore(opt, porterSelect.firstChild);
    }
    opt.selected = true;
    input.value = '';
    refreshAll();
    porterSelect.focus();
  }

  // Store names are free text upstream and come out as Steam/steam/STEAM and
  // itch.io/Itch.io/Itch. Offering a list and filling the name in from the
  // URL keeps new ports consistent. Same hosts the site itself recognises.
  const STORE_BY_HOST = {
    'store.steampowered.com': 'Steam', 'steampowered.com': 'Steam',
    'itch.io': 'itch.io', 'gog.com': 'GOG',
    'store.epicgames.com': 'Epic Games', 'epicgames.com': 'Epic Games',
    'gamejolt.com': 'Game Jolt', 'github.com': 'GitHub',
    'newgrounds.com': 'Newgrounds', 'humblebundle.com': 'Humble Bundle'
  };

  function storeNameFor(url) {
    let host;
    try { host = new URL(url).hostname.toLowerCase().replace(/^www\./, ''); } catch (e) { return ''; }
    if (STORE_BY_HOST[host]) return STORE_BY_HOST[host];
    if (host.endsWith('.itch.io')) return 'itch.io';
    return '';
  }

  function addStoreRow() {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><input type="text" class="store-name" list="storeNames" placeholder="Steam" /></td>
      <td><input type="text" class="store-game-url" placeholder="https://store.steampowered.com/app/..." /></td>
      <td><input type="text" class="store-dev-url" placeholder="https://..." /></td>
      <td class="row-actions"><button type="button" class="row-delete-btn" title="Remove link"><i class="bi bi-x-lg"></i></button></td>
    `;
    document.querySelector('#storeTable tbody').appendChild(row);
    row.querySelector('input').focus();
  }

  scope.addEventListener('input', e => {
    if (e.target.classList && e.target.classList.contains('store-game-url')) {
      const nameInput = e.target.closest('tr').querySelector('.store-name');
      if (!nameInput.value.trim() || nameInput.dataset.auto === '1') {
        const guess = storeNameFor(e.target.value);
        nameInput.value = guess;
        nameInput.dataset.auto = guess ? '1' : '';
      }
    } else if (e.target.classList && e.target.classList.contains('store-name')) {
      e.target.dataset.auto = '';
    }
    refreshAll();
  });
  scope.addEventListener('change', refreshAll);

  document.getElementById('addPorterBtn').addEventListener('click', addPorter);
  document.getElementById('addPorter').addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); addPorter(); }
  });

  document.getElementById('addStoreBtn').addEventListener('click', addStoreRow);
  document.getElementById('clearStoresBtn').addEventListener('click', () => {
    document.querySelector('#storeTable tbody').innerHTML = '';
    refreshAll();
  });

  scope.addEventListener('click', e => {
    const btn = e.target.closest('.row-delete-btn');
    if (btn) {
      btn.closest('tr').remove();
      refreshAll();
    }
  });

  document.getElementById('downloadBtn').addEventListener('click', downloadJSON);

  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      downloadJSON();
    }
  });

  // ===================================================================
  // Load the data, then bring the picker, runtimes and grid up.
  // ===================================================================
  const status = document.getElementById('reqStatus');
  const getJson = url => fetch(url).then(r => r.ok ? r.json() : Promise.reject(new Error(url)));

  Promise.all([
    getJson('../../assets/json/device_info.json'),
    getJson('../../assets/json/runtime_archs.json')
  ]).then(([deviceData, runtimeData]) => {
    devices = deviceData;
    runtimeArchs = runtimeData;
    vocabulary = buildVocabulary(devices);
    status.style.display = 'none';
    renderTags();
    renderRuntimes();
    refreshAll();
  }).catch(() => {
    status.textContent = 'Couldn\'t load the device data, so requirements can\'t be set right now.';
    runtimeSelect.innerHTML = '<option disabled>Couldn\'t load the runtime list</option>';
  });

  refreshOutput();
})();
</script>
