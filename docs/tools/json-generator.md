<div class="porter-tool">

<h1>Port JSON Generator</h1>
<p class="subtitle">Create port.json files for PortMaster submissions</p>

<div class="section">
  <div class="section-header">
    <div class="section-number">1</div>
    <h3 class="section-title">Basic Information</h3>
  </div>
  
  <div class="form-group">
    <label for="zipName">Zip Name (e.g., gamename.zip)</label>
    <input type="text" id="zipName" placeholder="gamename.zip" />
    <p class="help-text">The filename of your port zip file</p>
  </div>

  <div class="form-group">
    <label for="scriptName">Script Name (e.g., Game Name.sh)</label>
    <input type="text" id="scriptName" placeholder="Game Name.sh" />
    <p class="help-text">The launch script filename (usually "Game Name.sh")</p>
  </div>

  <div class="form-group">
    <label for="folderName">Folder Name (e.g., gamename)</label>
    <input type="text" id="folderName" placeholder="gamename" />
    <p class="help-text">The port folder name (lowercase, no spaces)</p>
  </div>

  <div class="form-group">
    <label for="title">Game Title</label>
    <input type="text" id="title" placeholder="Game Name" />
  </div>

  <div class="form-group">
    <label for="porter">Porter Name(s) (comma-separated)</label>
    <input type="text" id="porter" placeholder="YourName, AnotherPorter" />
  </div>

  <div class="form-group">
    <label for="desc">Short Description</label>
    <textarea id="desc" placeholder="Brief game description (plain text)"></textarea>
  </div>

  <div class="form-group">
    <label for="descMd">Description (Markdown - optional)</label>
    <textarea id="descMd" placeholder="Detailed description with markdown formatting (optional)"></textarea>
  </div>
</div>

<div class="section">
  <div class="section-header">
    <div class="section-number">2</div>
    <h3 class="section-title">Installation Instructions</h3>
  </div>

  <div class="form-group">
    <label for="inst">Instructions (Plain Text)</label>
    <textarea id="inst" placeholder="Installation instructions (plain text)"></textarea>
  </div>

  <div class="form-group">
    <label for="instMd">Instructions (Markdown - optional)</label>
    <textarea id="instMd" placeholder="Installation instructions with markdown formatting (optional)"></textarea>
  </div>
</div>

<div class="section">
  <div class="section-header">
    <div class="section-number">3</div>
    <h3 class="section-title">Game Attributes</h3>
  </div>

  <div class="form-row">
    <div class="form-group">
      <label for="availability">Availability</label>
      <select id="availability">
        <option value="free">Free</option>
        <option value="paid">Paid</option>
        <option value="demo">Demo</option>
      </select>
    </div>

    <div class="form-group">
      <label for="genres">Genres (comma-separated)</label>
      <input type="text" id="genres" placeholder="action, adventure, rpg" />
    </div>
  </div>

  <div class="form-row">
    <div class="form-group">
      <label>
        <input type="checkbox" id="rtr" />
        Ready to Run (RTR)
      </label>
      <p class="help-text">Check if game files are included</p>
    </div>

    <div class="form-group">
      <label>
        <input type="checkbox" id="exp" />
        Experimental
      </label>
      <p class="help-text">Check if port is experimental</p>
    </div>
  </div>

  <div class="form-group">
    <label for="arch">Architecture (comma-separated)</label>
    <input type="text" id="arch" placeholder="aarch64, x86_64" value="aarch64" />
    <p class="help-text">Common: aarch64, x86_64, armhf</p>
  </div>

  <div class="form-group">
    <label for="runtime">Runtime (select if needed)</label>
    <select id="runtime" multiple size="8">
      <option value="">None</option>
      <option value="godot">Godot</option>
      <option value="fna">FNA</option>
      <option value="mono-6.12.0.122">Mono 6.12</option>
      <option value="love-11.4">LÖVE 11.4</option>
      <option value="solarus-1.6.5">Solarus 1.6.5</option>
      <option value="jdk-zulu17.42.19">JDK Zulu 17</option>
      <option value="openssl-1.1.1w">OpenSSL 1.1.1w</option>
      <option value="sdl2">SDL2</option>
      <option value="sdl2_image">SDL2_image</option>
      <option value="sdl2_mixer">SDL2_mixer</option>
      <option value="sdl2_ttf">SDL2_ttf</option>
    </select>
    <p class="help-text">Hold Ctrl/Cmd to select multiple. Leave unselected if no runtime needed.</p>
  </div>

  <div class="form-group">
    <label for="minGlibc">Minimum GLIBC Version (optional)</label>
    <input type="text" id="minGlibc" placeholder="2.27" />
  </div>
</div>

<div class="section">
  <div class="section-header">
    <div class="section-number">4</div>
    <h3 class="section-title">Store Links</h3>
  </div>

  <table class="controls-table" id="storeTable">
    <thead>
      <tr>
        <th style="width: 20%;">Store Name</th>
        <th style="width: 40%;">Game URL</th>
        <th style="width: 40%;">Developer URL</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><input type="text" class="store-name" placeholder="Steam" /></td>
        <td><input type="text" class="store-game-url" placeholder="https://store.steampowered.com/app/..." /></td>
        <td><input type="text" class="store-dev-url" placeholder="https://..." /></td>
      </tr>
    </tbody>
  </table>
  <div class="table-actions">
    <button class="add-row-btn" onclick="addStoreRow()">
      <span class="icon">+</span>
      Add Store Link
    </button>
    <button class="clear-btn" onclick="clearStores()">
      Clear Store Links
    </button>
  </div>
</div>

<div class="section">
  <div class="section-header">
    <div class="section-number">5</div>
    <h3 class="section-title">Generated JSON</h3>
  </div>
  
  <div class="output-container">
    <pre id="outputArea"><div class="output-placeholder">Click "Generate JSON" to see your output here...</div></pre>
  </div>

  <div class="action-buttons">
    <button class="add-row-btn" onclick="generateJSON()" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; background: var(--md-accent-fg-color); color: white; border: none; border-radius: 6px; font-weight: 500; cursor: pointer; font-size: 0.95rem;">
      <span class="icon">⚡</span>
      Generate JSON
    </button>

    <button class="clear-btn" onclick="downloadJSON()" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; background: transparent; color: var(--md-default-fg-color--light); border: 1px solid var(--card-border); border-radius: 6px; font-weight: 500; cursor: pointer; font-size: 0.95rem;">
      <span class="icon">📥</span>
      Download port.json
    </button>
  </div>
</div>

<script>
// Add store row function
function addStoreRow() {
  const tbody = document.querySelector('#storeTable tbody');
  const row = document.createElement('tr');
  row.innerHTML = `
    <td><input type="text" class="store-name" placeholder="Store Name" /></td>
    <td><input type="text" class="store-game-url" placeholder="Game URL" /></td>
    <td><input type="text" class="store-dev-url" placeholder="Developer URL" /></td>
  `;
  tbody.appendChild(row);
  row.querySelector('input').focus();
}

// Clear stores function
function clearStores() {
  document.querySelector('#storeTable tbody').innerHTML = `
    <tr>
      <td><input type="text" class="store-name" placeholder="Steam" /></td>
      <td><input type="text" class="store-game-url" placeholder="https://..." /></td>
      <td><input type="text" class="store-dev-url" placeholder="https://..." /></td>
    </tr>
  `;
}

// Generate JSON
function generateJSON() {
  // Get basic fields
  const scriptName = document.getElementById('scriptName').value.trim();
  const folderName = document.getElementById('folderName').value.trim();
  
  // Build items array
  const items = [];
  if (scriptName) items.push(scriptName);
  if (folderName) items.push(folderName);
  
  // Collect porters
  const porterInput = document.getElementById('porter').value.trim();
  const porters = porterInput ? porterInput.split(',').map(p => p.trim()) : [];

  // Collect genres
  const genresInput = document.getElementById('genres').value.trim();
  const genres = genresInput ? genresInput.split(',').map(g => g.trim()) : [];

  // Collect architecture
  const archInput = document.getElementById('arch').value.trim();
  const arch = archInput ? archInput.split(',').map(a => a.trim()) : [];

  // Collect runtime from multi-select
  const runtimeSelect = document.getElementById('runtime');
  const selectedOptions = Array.from(runtimeSelect.selectedOptions);
  const runtime = selectedOptions
    .map(opt => opt.value)
    .filter(val => val !== ""); // Filter out "None" option

  // Collect store links
  const stores = [];
  document.querySelectorAll('#storeTable tbody tr').forEach(row => {
    const name = row.querySelector('.store-name').value.trim();
    const gameurl = row.querySelector('.store-game-url').value.trim();
    const developerurl = row.querySelector('.store-dev-url').value.trim();
    if (name && gameurl) {
      stores.push({ name, gameurl, developerurl: developerurl || "" });
    }
  });

  // Build JSON object
  const portJSON = {
    version: 4,
    name: document.getElementById('zipName').value.trim() || "gamename.zip",
    items: items.length > 0 ? items : ["Game Name.sh", "gamename"],
    items_opt: null,
    attr: {
      title: document.getElementById('title').value.trim() || "Game Title",
      porter: porters,
      desc: document.getElementById('desc').value.trim() || "",
      desc_md: document.getElementById('descMd').value.trim() || null,
      inst: document.getElementById('inst').value.trim() || "",
      inst_md: document.getElementById('instMd').value.trim() || null,
      genres: genres,
      image: {},
      rtr: document.getElementById('rtr').checked,
      exp: document.getElementById('exp').checked,
      runtime: runtime,
      store: stores,
      availability: document.getElementById('availability').value,
      reqs: [],
      arch: arch,
      min_glibc: document.getElementById('minGlibc').value.trim()
    }
  };

  // Display formatted JSON
  const jsonString = JSON.stringify(portJSON, null, 4);
  document.getElementById('outputArea').textContent = jsonString;
}

// Download JSON
function downloadJSON() {
  const content = document.getElementById('outputArea').textContent;
  
  if (!content || content.includes('Click "Generate JSON"')) {
    alert('Please generate JSON before downloading.');
    return;
  }

  const blob = new Blob([content], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = 'port.json';
  a.click();

  URL.revokeObjectURL(url);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    generateJSON();
  }
});
</script>

</div>