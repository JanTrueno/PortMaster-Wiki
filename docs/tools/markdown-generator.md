---
title: README Generator - PortMaster Wiki

# No build-time images on this page for glightbox to wrap - everything is
# form fields and client-side rendered output. Same reasoning as
# games.md/cover-generator.md.
glightbox: false
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

# README Generator

Use this form to generate a `README.md` file for your port, right in your browser.
It matches the [Port Markdown Generator](https://portmaster.games/port-markdown.html){:target="_blank" rel="noopener"}
on the main PortMaster site field for field and byte for byte - the download is
identical. See the [packaging documentation](../contribute/porting/packaging.md)
for where to place the file, and
[here](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax){:target="_blank" rel="noopener"}
is documentation on Markdown writing and formatting syntax.

<div class="porter-tool porter-tool-panel">

<div class="filter-accordion open">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Notes</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="form-group">
      <label for="steamCommand">SteamDB Command</label>
      <div class="tool-inline-row">
        <input type="text" id="steamCommand" placeholder="+app_update 123456 validate" />
        <button type="button" class="add-row-btn" id="steamBtn">
          <i class="bi bi-steam"></i>
          Add Steam Instructions
        </button>
      </div>
      <p class="help-text">Look the app up on <a href="https://steamdb.info" target="_blank" rel="noopener">SteamDB</a>,
      paste its install command here, and a Steam Instructions section is appended to the notes.</p>
    </div>

    <div class="form-group">
      <label for="notes">Notes</label>
      <textarea id="notes" placeholder="Thank the developers, add installation notes, or include any additional information about the port... (markdown supported)"></textarea>
    </div>
  </div>
</div>

<div class="filter-accordion">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Compile Instructions <small>*optional</small></span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <div class="form-group">
      <label for="compile" class="sr-only">Compile Instructions</label>
      <textarea id="compile" placeholder="Commands needed to compile the port..."></textarea>
      <p class="help-text">Added to the README as a shell code block.</p>
    </div>
  </div>
</div>

<div class="filter-accordion">
  <div class="filter-accordion-summary" role="button" tabindex="0">
    <span>Controls</span>
    <i class="bi bi-chevron-down accordion-chevron"></i>
  </div>
  <div class="filter-accordion-body">
    <table class="controls-table" id="controlsTable">
      <thead>
        <tr>
          <th style="width: 35%;">Button</th>
          <th style="width: 57%;">Action</th>
          <th class="row-actions"></th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>

    <div class="table-actions">
      <button type="button" class="add-row-btn" id="addMappingBtn">
        <i class="bi bi-plus-lg"></i>
        Add Button Mapping
      </button>
      <button type="button" class="clear-btn" id="clearMappingsBtn">
        Clear All Rows
      </button>
    </div>
  </div>
</div>

</div>

## Generated README

<div class="porter-tool">
  <div class="output-container">
    <pre id="outputArea"><div class="output-placeholder">Fill in the form - the README output updates live here...</div></pre>
  </div>

  <div class="action-buttons">
    <button type="button" class="primary-btn" id="downloadBtn">
      <i class="bi bi-download"></i>
      Download README.md
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
  const notesEl = document.getElementById('notes');
  const compileEl = document.getElementById('compile');
  const outputArea = document.getElementById('outputArea');
  const PLACEHOLDER = '<div class="output-placeholder">Fill in the form - the README output updates live here...</div>';

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

  function addSteamInstructions() {
    const command = document.getElementById('steamCommand').value;
    const instructions = "### Steam Instructions\n* [Open Steam console](steam://open/console)\n* Copy and paste command: " + command;
    notesEl.value = notesEl.value + "\n\n" + instructions;
    refreshOutput();
    notesEl.focus();
  }

  function addRow() {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td><input type="text" class="col1" placeholder="e.g., A Button" /></td>
      <td><input type="text" class="col2" placeholder="e.g., Jump" /></td>
      <td class="row-actions"><button type="button" class="row-delete-btn" title="Remove mapping"><i class="bi bi-x-lg"></i></button></td>
    `;
    document.querySelector('#controlsTable tbody').appendChild(row);
    row.querySelector('input').focus();
  }

  // Mirrors portmaster.games/port-markdown.html renderMarkdown(): sections
  // joined with blank lines, the compact |--|--| separator, no padding
  // around table cells, and <br/> stripped - the download is byte-identical.
  function buildMarkdown() {
    let notes = notesEl.value;
    if (notes != "") {
      notes = "## Notes\n\n" + notes + "\n";
    }

    let compile = compileEl.value;
    if (compile != "") {
      compile = "## Compile\n\n" + "```shell\n" + compile + "\n```" + "\n";
    }

    let controls = "";
    document.querySelectorAll('#controlsTable tbody tr').forEach(row => {
      const button = row.querySelector('.col1').value;
      const action = row.querySelector('.col2').value;
      controls = controls + "|" + button + "|" + action + "|\n";
    });
    if (controls != "") {
      controls = "## Controls\n\n| Button | Action |\n|--|--| \n" + controls + "\n";
    }

    return (notes + "\n" + controls + "\n" + compile).replaceAll("<br/>", "");
  }

  function refreshOutput() {
    const markdown = buildMarkdown();
    if (markdown.replaceAll('\n', '').trim() === '') {
      outputArea.innerHTML = PLACEHOLDER;
    } else {
      outputArea.textContent = markdown;
    }
  }

  function downloadMarkdown() {
    const markdown = buildMarkdown();
    if (markdown.replaceAll('\n', '').trim() === '') {
      alert('Add some notes, controls, or compile instructions first.');
      return;
    }

    const blob = new Blob([markdown], { type: 'application/text' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'README.md';
    a.click();
    URL.revokeObjectURL(a.href);
  }

  scope.addEventListener('input', refreshOutput);
  scope.addEventListener('change', refreshOutput);

  document.getElementById('steamBtn').addEventListener('click', addSteamInstructions);

  document.getElementById('addMappingBtn').addEventListener('click', addRow);
  document.getElementById('clearMappingsBtn').addEventListener('click', () => {
    document.querySelector('#controlsTable tbody').innerHTML = '';
    refreshOutput();
  });

  scope.addEventListener('click', e => {
    const btn = e.target.closest('.row-delete-btn');
    if (btn) {
      btn.closest('tr').remove();
      refreshOutput();
    }
  });

  document.getElementById('downloadBtn').addEventListener('click', downloadMarkdown);

  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      downloadMarkdown();
    }
  });
})();
</script>
