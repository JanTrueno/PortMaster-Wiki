<!DOCTYPE html>
<html lang="en" data-md-color-scheme="dark">
<head>
  <meta charset="UTF-8" />
  <title>Markdown Generator Test</title>
  <style>
    /* Apply existing color scheme for the page */
    body {
      background-color: var(--md-default-bg-color);
      color: var(--md-default-fg-color);
    }

    textarea, input {
      padding: var(--custom-input-padding); /* Use new custom padding variable */
      margin: var(--custom-margin); /* Use new custom margin variable */
      width: 100%;
    }

    pre {
      background-color: var(--md-code-bg-color);
      color: var(--md-code-fg-color);
      border-radius: var(--custom-table-border-radius); /* Use new custom border radius */
      overflow: auto;
    }

    table {
      width: 100%;
      background-color: var(--md-typeset-table-color);
      border-collapse: collapse;
    }

    /* Apply hover effect for better interaction feedback */
    button:hover {
      background-color: var(--md-primary-bg-color);
      color: var(--md-accent-fg-color);
    }

  </style>
</head>
<body>

<h1>Markdown Generator Test</h1>

<p>This tool will generate port markdowns, needs a proper clean up. </p>

<h3>1. Notes</h3>
<textarea id="markdownInput" placeholder="Thank the developers here and other notes..."></textarea>

<h3>2. Controls</h3>
<table id="tableContainer">
  <thead>
    <tr>
      <th>Button</th>
      <th>Action</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><input type="text" placeholder="Button" class="col1" /></td>
      <td><input type="text" placeholder="Action" class="col2" /></td>
    </tr>
    <tr>
      <td><input type="text" placeholder="Button" class="col1" /></td>
      <td><input type="text" placeholder="Action" class="col2" /></td>
    </tr>
  </tbody>
</table>
<p><button class="md-button md-button--primary" onclick="addRow()">Add Row</button></p>

<h3>3. Output</h3>
<pre id="outputArea"></pre>

<p>
  <a href="#" onclick="generateMarkdown(); return false;" class="md-button md-button--primary">[Generate Markdown]</a><br />
  <br> 
  <a href="#" onclick="downloadMarkdown(); return false;" class="md-button md-button--primary">[Download Markdown]</a>
</p>

<script>
function addRow() {
  const container = document.getElementById('tableContainer').getElementsByTagName('tbody')[0];
  const newRow = document.createElement('tr');
  newRow.innerHTML = `
    <td><input type="text" placeholder="Button Text" class="col1" /></td>
    <td><input type="text" placeholder="Action URL" class="col2" /></td>
  `;
  container.appendChild(newRow);
}

function generateMarkdown() {
  const intro = document.getElementById('markdownInput').value.trim();

  const rows = Array.from(document.querySelectorAll('#tableContainer tbody tr')).map(row => {
    const col1 = row.querySelector('.col1').value.trim();
    const col2 = row.querySelector('.col2').value.trim();
    return `| ${col1} | ${col2} |`;
  });

  let tableMarkdown = '\n## Data Table\n\n| Button | Action |\n|--------|--------|\n' + rows.join('\n');

  const buttons = `
[Download Markdown]{ .md-button .md-button--primary }
`.trim();

  const full = `${intro}\n\n${buttons}\n\n${tableMarkdown}`;
  document.getElementById('outputArea').textContent = full;
}

function downloadMarkdown() {
  const md = document.getElementById('outputArea').textContent;
  const blob = new Blob([md], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'README.md';
  a.click();
  URL.revokeObjectURL(url);
}
</script>

</body>
</html>




