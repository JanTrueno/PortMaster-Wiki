<div class="porter-tool">

<h1>Markdown Generator</h1>
<p class="subtitle">Create port README files with controls documentation</p>

<div class="section">
  <div class="section-header">
    <div class="section-number">1</div>
    <h3 class="section-title">Notes & Credits</h3>
  </div>
  <textarea
    id="markdownInput"
    placeholder="Thank the developers, add installation notes, or include any additional information about the port..."
  ></textarea>
</div>

<div class="section">
  <div class="section-header">
    <div class="section-number">2</div>
    <h3 class="section-title">Controls</h3>
  </div>

  <table class="controls-table" id="tableContainer">
    <thead>
      <tr>
        <th style="width: 35%;">Button</th>
        <th style="width: 65%;">Action</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><input type="text" class="col1" placeholder="e.g., A Button" /></td>
        <td><input type="text" class="col2" placeholder="e.g., Jump" /></td>
      </tr>
      <tr>
        <td><input type="text" class="col1" placeholder="e.g., B Button" /></td>
        <td><input type="text" class="col2" placeholder="e.g., Attack" /></td>
      </tr>
      <tr>
        <td><input type="text" class="col1" placeholder="e.g., Start" /></td>
        <td><input type="text" class="col2" placeholder="e.g., Pause" /></td>
      </tr>
    </tbody>
  </table>

  <div class="table-actions">
    <button class="add-row-btn" onclick="addRow()">
      <span class="icon">+</span>
      Add Row
    </button>
    <button class="clear-btn" onclick="clearTable()">
      Clear All Rows
    </button>
  </div>
</div>

<div class="section">
  <div class="section-header">
    <div class="section-number">3</div>
    <h3 class="section-title">Generated Output</h3>
  </div>
  
  <div class="output-container">
    <pre id="outputArea"><div class="output-placeholder">Click "Generate Markdown" to see your output here...</div></pre>
  </div>

  <div class="action-buttons">
    <button class="add-row-btn" onclick="generateMarkdown(); return false;" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; background: var(--md-accent-fg-color); color: white; border: none; border-radius: 6px; font-weight: 500; cursor: pointer; font-size: 0.95rem;">
      <span class="icon">⚡</span>
      Generate Markdown
    </button>

    <button class="clear-btn" onclick="downloadMarkdown(); return false;" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; background: transparent; color: var(--md-default-fg-color--light); border: 1px solid var(--card-border); border-radius: 6px; font-weight: 500; cursor: pointer; font-size: 0.95rem;">
      <span class="icon">📥</span>
      Download README.md
    </button>
  </div>
</div>

<script>
function addRow() {
  const tbody = document.querySelector('#tableContainer tbody');
  const row = document.createElement('tr');

  row.innerHTML = `
    <td><input type="text" class="col1" placeholder="e.g., Select" /></td>
    <td><input type="text" class="col2" placeholder="e.g., Open Menu" /></td>
  `;

  tbody.appendChild(row);
  
  // Focus the first input in the new row
  row.querySelector('.col1').focus();
}

function clearTable() {
  const tbody = document.querySelector('#tableContainer tbody');
  tbody.innerHTML = `
    <tr>
      <td><input type="text" class="col1" placeholder="e.g., A Button" /></td>
      <td><input type="text" class="col2" placeholder="e.g., Jump" /></td>
    </tr>
    <tr>
      <td><input type="text" class="col1" placeholder="e.g., B Button" /></td>
      <td><input type="text" class="col2" placeholder="e.g., Attack" /></td>
    </tr>
    <tr>
      <td><input type="text" class="col1" placeholder="e.g., Start" /></td>
      <td><input type="text" class="col2" placeholder="e.g., Pause" /></td>
    </tr>
  `;
}

function generateMarkdown() {
  const notes = document.getElementById('markdownInput').value.trim();

  const rows = Array.from(
    document.querySelectorAll('#tableContainer tbody tr')
  )
    .map(row => {
      const b = row.querySelector('.col1').value.trim();
      const a = row.querySelector('.col2').value.trim();
      if (!b && !a) return null; // skip empty rows
      return `| ${b} | ${a} |`;
    })
    .filter(Boolean);

  // Only add controls section if there are rows with data
  const controlsSection = rows.length > 0 
    ? [
        '## Controls',
        '',
        '| Button | Action |',
        '|--------|--------|',
        ...rows
      ].join('\n')
    : '';

  const notesSection = notes
    ? `## Notes\n\n${notes}`
    : '';

  // Build output with proper spacing
  const parts = [notesSection, controlsSection].filter(Boolean);
  const output = parts.length > 0 
    ? parts.join('\n\n')
    : 'No content generated. Please add notes or controls.';

  document.getElementById('outputArea').textContent = output;
}

function downloadMarkdown() {
  const content = document.getElementById('outputArea').textContent;
  
  // Don't download if it's the placeholder or empty
  if (!content || content.includes('Click "Generate Markdown"') || content.includes('No content generated')) {
    alert('Please generate markdown before downloading.');
    return;
  }

  const blob = new Blob([content], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = 'README.md';
  a.click();

  URL.revokeObjectURL(url);
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
  // Ctrl/Cmd + Enter to generate
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    generateMarkdown();
  }
});
</script>

</div>