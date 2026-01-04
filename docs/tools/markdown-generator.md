<div class="mdgen">

<style>
/* ===============================
   Markdown Generator – Polished CSS
   =============================== */

.mdgen {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.mdgen h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--md-default-fg-color);
}

.mdgen .subtitle {
  color: var(--md-default-fg-color--light);
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.mdgen .section {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: box-shadow 0.2s ease;
}

.mdgen .section:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.mdgen .section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.mdgen .section-number {
  background: var(--md-accent-fg-color);
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
}

.mdgen .section-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  color: var(--md-default-fg-color);
}

.mdgen textarea,
.mdgen input[type="text"] {
  width: 100%;
  padding: 0.875rem 1rem;
  border-radius: 8px;
  border: 1px solid var(--card-border);
  background: var(--md-default-bg-color);
  color: var(--md-default-fg-color);
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.2s ease;
}

.mdgen textarea {
  min-height: 140px;
  resize: vertical;
  font-family: inherit;
  line-height: 1.6;
}

.mdgen textarea:focus,
.mdgen input[type="text"]:focus {
  outline: none;
  border-color: var(--md-accent-fg-color);
  box-shadow: 0 0 0 3px rgba(244,149,25,0.15);
}

.mdgen .controls-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin-top: 1rem;
  overflow: hidden;
  border-radius: 8px;
  border: 1px solid var(--card-border);
}

.mdgen .controls-table thead {
  background: var(--md-typeset-table-color);
}

.mdgen .controls-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--md-default-fg-color);
  border-bottom: 2px solid var(--card-border);
}

.mdgen .controls-table td {
  padding: 0.75rem;
  border-bottom: 1px solid var(--md-typeset-table-color--light);
}

.mdgen .controls-table tr:last-child td {
  border-bottom: none;
}

.mdgen .controls-table input {
  margin: 0;
}

.mdgen .table-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--card-border);
}

.mdgen .btn-row {
  display: flex;
  gap: 0.75rem;
}

.mdgen .add-row-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: var(--md-accent-fg-color);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
}

.mdgen .add-row-btn:hover {
  background: #d67f0f;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(244, 149, 25, 0.3);
}

.mdgen .add-row-btn:active {
  transform: translateY(0);
}

.mdgen .clear-btn {
  padding: 0.625rem 1.25rem;
  background: transparent;
  color: var(--md-default-fg-color--light);
  border: 1px solid var(--card-border);
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
}

.mdgen .clear-btn:hover {
  background: var(--card-bg-hover);
  border-color: var(--md-default-fg-color--lighter);
}

.mdgen .output-container {
  position: relative;
}

.mdgen pre {
  margin: 0;
  padding: 1.5rem;
  background: var(--md-code-bg-color);
  color: var(--md-code-fg-color);
  border-radius: 8px;
  overflow-x: auto;
  font-size: 0.9rem;
  line-height: 1.6;
  font-family: 'Roboto Mono', monospace;
  border: 1px solid var(--card-border);
  max-height: 500px;
  overflow-y: auto;
}

.mdgen .output-placeholder {
  color: var(--md-default-fg-color--lighter);
  font-style: italic;
  text-align: center;
  padding: 3rem;
}

.mdgen .action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  flex-wrap: wrap;
}

.mdgen .primary-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  background: var(--md-accent-fg-color);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  font-size: 1rem;
}

.mdgen .primary-btn:hover {
  background: #d67f0f;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 149, 25, 0.3);
}

.mdgen .primary-btn:active {
  transform: translateY(0);
}

.mdgen .secondary-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  background: transparent;
  color: var(--md-default-fg-color);
  border: 2px solid var(--card-border);
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  font-size: 1rem;
}

.mdgen .secondary-btn:hover {
  background: var(--card-bg-hover);
  border-color: var(--md-accent-fg-color);
  color: var(--md-accent-fg-color);
}

.mdgen .icon {
  font-size: 1.2rem;
}

/* Dark mode specific adjustments */
[data-md-color-scheme="dark"] .mdgen .section {
  background: var(--card-bg);
}

[data-md-color-scheme="dark"] .mdgen .controls-table {
  border-color: var(--card-border);
}

/* Responsive */
@media (max-width: 768px) {
  .mdgen {
    padding: 0 0.5rem;
  }
  
  .mdgen h1 {
    font-size: 2rem;
  }
  
  .mdgen .action-buttons {
    flex-direction: column;
  }
  
  .mdgen .primary-btn,
  .mdgen .secondary-btn {
    width: 100%;
    justify-content: center;
  }
  
  .mdgen .table-actions {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
}
</style>

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
    <a href="#" class="primary-btn" onclick="generateMarkdown(); return false;">
      <span class="icon">⚡</span>
      Generate Markdown
    </a>

    <a href="#" class="secondary-btn" onclick="downloadMarkdown(); return false;">
      <span class="icon">📥</span>
      Download README.md
    </a>
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