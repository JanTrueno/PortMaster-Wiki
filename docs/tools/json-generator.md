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
It matches the [Port JSON Generator](https://portmaster.games/port-json.html){:target="_blank" rel="noopener"}
on the main PortMaster site field for field and byte for byte - the download is
identical. See the [packaging documentation](../contribute/porting/packaging.md)
for where to place the file.

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
        <p class="help-text">Comma-separated for multiple scripts, e.g. <code>Game Name.sh, Game Name 2.sh</code></p>
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
      <select id="porter" multiple size="6"></select>
      <p class="help-text">Hold Ctrl/Cmd to select multiple. The list is loaded from
      <a href="https://github.com/PortsMaster/PortMaster-Info" target="_blank" rel="noopener">PortMaster-Info</a>.</p>
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
        <optgroup label="Misc">
          <option value="mesa_pkg_0.1.squashfs">Mesapack 0.1</option>
          <option value="mono-6.12.0.122-aarch64.squashfs">Mono (6.12.0.112)</option>
          <option value="pyxel_2.2.8_python_3.11.squashfs">Pyxel 2.2.8</option>
          <option value="renpy_8.3.4.squashfs">RenPY 8.3.4</option>
          <option value="rlvm.squashfs">Real Live VM</option>
          <option value="solarus-1.6.5.squashfs">Solarus 1.6.5</option>
          <option value="weston_pkg_0.2.squashfs">Westonpack 0.2</option>
        </optgroup>
        <optgroup label="GoDot / FRT">
          <option value="frt_2.1.6.squashfs">GoDot / FRT 2.1.6</option>
          <option value="frt_3.0.6_v1.squashfs">GoDot / FRT 3.0.6</option>
          <option value="frt_3.1.2.squashfs">GoDot / FRT 3.1.2</option>
          <option value="frt_3.2.3.squashfs">GoDot / FRT 3.2.3</option>
          <option value="frt_3.3.4.squashfs">GoDot / FRT 3.3.4</option>
          <option value="frt_3.4.5.squashfs">GoDot / FRT 3.4.5</option>
          <option value="frt_3.5.2.squashfs">GoDot / FRT 3.5.2</option>
          <option value="frt_3.6.squashfs">Godot / FRT 3.6</option>
          <option value="frt_4.0.4.squashfs">Godot / FRT 4.0.4</option>
          <option value="frt_4.1.3.squashfs">Godot / FRT 4.1.3</option>
        </optgroup>
        <optgroup label="Java">
          <option value="zulu11.48.21-ca-jdk11.0.11-linux.aarch64.squashfs">Java jdk11.0.11</option>
          <option value="zulu17.48.15-ca-jdk17.0.10-linux.aarch64.squashfs">Java jdk17.0.10</option>
          <option value="zulu17.54.21-ca-jre17.0.13-linux.squashfs">Java jre17.0.13</option>
        </optgroup>
      </select>
      <p class="help-text">Hold Ctrl/Cmd to select multiple. Leave unselected if no runtime is needed.</p>
    </div>

    <div class="form-group">
      <label>Architecture</label>
      <div class="tool-check-grid" id="archList">
        <label class="filter-checkbox-item"><input type="checkbox" value="aarch64" /><span>AArch64</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="" /><span>Runtime</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="armhf" /><span>ARMHF</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="x86_64" /><span>x86_64</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" value="x86" /><span>x86</span></label>
      </div>
      <p class="help-text">Ports that rely on a runtime alone can leave this empty.</p>
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
    <span>Requirements</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="filter-subgroup">
      <label>Resolution</label>
      <div class="filter-radio-list">
        <label class="filter-checkbox-item"><input type="radio" name="resRadio" value="notlowres" /><span>Not Lowres: Exclude 480x320 (351p, OGA, zpg pro, rgb10)</span></label>
        <label class="filter-checkbox-item"><input type="radio" name="resRadio" value="hires" /><span>Highres: Anything above 640x480</span></label>
        <label class="filter-checkbox-item"><input type="radio" name="resRadio" value="anyres" checked /><span>Any Resolution</span></label>
      </div>
    </div>

    <div class="filter-subgroup">
      <label>Ram</label>
      <div class="filter-radio-list">
        <label class="filter-checkbox-item"><input type="radio" name="ramRadio" value="anygb" checked /><span>No Minimum Ram</span></label>
        <label class="filter-checkbox-item"><input type="radio" name="ramRadio" value="2gb" /><span>2gb Ram Minimum</span></label>
        <label class="filter-checkbox-item"><input type="radio" name="ramRadio" value="4gb" /><span>4gb Ram Minimum</span></label>
      </div>
    </div>

    <div class="filter-subgroup">
      <label>Other</label>
      <div class="filter-radio-list">
        <label class="filter-checkbox-item"><input type="checkbox" id="reqPower" value="power" /><span>Power: any device above an rk3326 cpu</span></label>
        <label class="filter-checkbox-item"><input type="checkbox" id="reqOpengl" value="opengl" /><span>OpenGL: any device with OpenGL, not OpenGLES</span></label>
      </div>
    </div>
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

  // Porter list - same source as the portmaster.games generator.
  fetch('https://raw.githubusercontent.com/PortsMaster/PortMaster-Info/main/porters.json')
    .then(r => r.ok ? r.json() : Promise.reject(new Error('network')))
    .then(porters => {
      Object.keys(porters).sort((a, b) => a.localeCompare(b)).forEach(name => {
        const opt = document.createElement('option');
        opt.value = name;
        opt.textContent = name;
        porterSelect.appendChild(opt);
      });
    })
    .catch(() => {});

  function checkedValues(listId) {
    return Array.from(document.querySelectorAll('#' + listId + ' input:checked'))
      .map(i => i.value)
      .filter(v => v !== '');
  }

  function radioValue(name) {
    const el = document.querySelector(`input[name="${name}"]:checked`);
    return el ? el.value : '';
  }

  // Mirrors portmaster.games/js/port-json.js getFormValues(): key order,
  // 2-space indentation, items split on ',' without trimming, items_opt: [],
  // image: null and min_glibc: "" - the download is byte-identical.
  function buildPortJson() {
    const items = document.getElementById('scriptName').value.split(',');
    items.push(document.getElementById('dirName').value);

    const reqs = [];
    const res = radioValue('resRadio');
    if (res === 'notlowres') reqs.push('!lowres');
    if (res === 'hires') reqs.push('hires');
    const ram = radioValue('ramRadio');
    if (ram === '2gb') reqs.push('2gb');
    if (ram === '4gb') reqs.push('4gb');
    if (document.getElementById('reqPower').checked) reqs.push('power');
    if (document.getElementById('reqOpengl').checked) reqs.push('opengl');

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
        runtime: Array.from(document.getElementById('runtime').selectedOptions).map(o => o.value),
        store: store,
        availability: document.getElementById('availability').value,
        reqs: reqs,
        arch: checkedValues('archList'),
        min_glibc: ""
      }
    };
  }

  function validateForm() {
    const missing = [];
    if (!document.getElementById('title').value.trim()) missing.push('Port Title');
    if (!document.getElementById('zipName').value.trim()) missing.push('Zip File Name');
    if (!document.getElementById('scriptName').value.trim()) missing.push('Script Name');
    if (!document.getElementById('dirName').value.trim()) missing.push('Directory Name');
    if (!checkedValues('genreList').length) missing.push('Genre (at least one)');
    if (!porterSelect.selectedOptions.length) missing.push('Porter (at least one)');
    if (!document.getElementById('description').value.trim()) missing.push('Description');
    if (!document.getElementById('instructions').value.trim()) missing.push('Instructions');
    if (!checkedValues('archList').length) missing.push('Architecture (at least one)');
    return missing;
  }

  function refreshOutput() {
    outputArea.textContent = JSON.stringify(buildPortJson(), null, 2);
  }

  function downloadJSON() {
    const missing = validateForm();
    if (missing.length) {
      validationBox.innerHTML = '<strong>Missing required fields:</strong> ' + missing.join(', ');
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
    refreshOutput();
    porterSelect.focus();
  }

  function addStoreRow() {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><input type="text" class="store-name" placeholder="Steam" /></td>
      <td><input type="text" class="store-game-url" placeholder="https://store.steampowered.com/app/..." /></td>
      <td><input type="text" class="store-dev-url" placeholder="https://..." /></td>
      <td class="row-actions"><button type="button" class="row-delete-btn" title="Remove link"><i class="bi bi-x-lg"></i></button></td>
    `;
    document.querySelector('#storeTable tbody').appendChild(row);
    row.querySelector('input').focus();
  }

  scope.addEventListener('input', refreshOutput);
  scope.addEventListener('change', refreshOutput);

  document.getElementById('addPorterBtn').addEventListener('click', addPorter);
  document.getElementById('addPorter').addEventListener('keydown', e => {
    if (e.key === 'Enter') { e.preventDefault(); addPorter(); }
  });

  document.getElementById('addStoreBtn').addEventListener('click', addStoreRow);
  document.getElementById('clearStoresBtn').addEventListener('click', () => {
    document.querySelector('#storeTable tbody').innerHTML = '';
    refreshOutput();
  });

  scope.addEventListener('click', e => {
    const btn = e.target.closest('.row-delete-btn');
    if (btn) {
      btn.closest('tr').remove();
      refreshOutput();
    }
  });

  document.getElementById('downloadBtn').addEventListener('click', downloadJSON);

  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      downloadJSON();
    }
  });
})();
</script>
