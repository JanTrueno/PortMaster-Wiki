<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Port Readme Generator</title>

  <!-- Bootstrap 5 and EasyMDE -->
  <link href="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.css" rel="stylesheet">
  
  <style>
    /* Form section styles */
    .form-section {
      margin-bottom: 3rem;
    }

    .form-section label {
      font-weight: bold;
    }

    .form-section textarea, .form-section input {
      width: 100%;
      padding: 10px;
      font-size: 1rem;
      border-radius: 4px;
    }

    .btn-custom {
      padding: 12px 20px;
      font-size: 1.1rem;
      width: 100%;
      border-radius: 4px;
    }

    .hidden {
      display: none;
    }

    .table th, .table td {
      vertical-align: middle;
      padding: 12px;
      text-align: center;
    }

    /* Button color schemes */
    .btn-primary {
      background-color: var(--md-typeset-a-color);
      color: var(--md-primary-fg-color);
    }

    .btn-primary:hover {
        background-color: var(--md-typeset-a-color);
    }

    .btn-success {
        background-color: var(--md-typeset-a-color);
      color: white;
    }

    .btn-success:hover {
        background-color: var(--md-typeset-a-color);
    }

    .btn-danger {
        background-color: var(--md-typeset-a-color);
      color: white;
    }

    .btn-danger:hover {
        background-color: var(--md-typeset-a-color);
    }

    .btn-custom {
        background-color: var(--md-typeset-a-color);
      color: var(--md-default-fg-color);
      border: 1px solid var(--md-default-bg-color--light);
    }

    .btn-custom:hover {
        background-color: var(--md-typeset-a-color);
      color: var(--md-default-fg-color);
    }

  </style>
</head>

<body data-md-color-scheme="light">
  <main class="container py-5">
    <div class="text-center mb-5">
      <h1 class="display-4">Port Readme Generator</h1>
      <p class="lead">Use this form to generate a `portname.md` file for a port. Refer to the <a href="packaging.html">packaging documentation</a> for details on where to place the file.</p>
    </div>

    <div class="row">
      <div class="col-md-8 offset-md-2">
        <form id="form">
          <!-- Steam Command -->
          <div class="form-section">
            <label for="steamCommand" class="form-label">SteamDB Command</label>
            <input type="text" id="steamCommand" class="form-control" placeholder="Enter SteamDB Command">
            <button type="button" class="btn btn-primary mt-2 btn-custom" onclick="addSteamInstructions()">Add Steam Instructions</button>
          </div>

          <!-- Notes Section -->
          <div class="form-section">
            <label for="notes" class="form-label">Notes</label>
            <textarea id="notes" class="form-control" rows="4" oninput="renderMarkdown()"></textarea>
          </div>

          <!-- Compile Instructions -->
          <div class="form-section">
            <label for="compile" class="form-label">Compile Instructions (optional)</label>
            <textarea id="compile" class="form-control" rows="4" oninput="renderMarkdown()"></textarea>
          </div>

          <!-- Controls Section -->
          <div class="form-section">
            <label for="controls" class="form-label">Controls</label>
            <table id="buttons" class="table table-bordered">
              <thead>
                <tr>
                  <th>Button</th>
                  <th>Action</th>
                  <th><button type="button" class="btn btn-success btn-sm" onclick="addButtonMapping()">Add Button Mapping</button></th>
                </tr>
              </thead>
              <tbody>
                <!-- Button mappings will appear here -->
              </tbody>
            </table>
          </div>

          <button type="button" class="btn btn-primary btn-lg btn-custom" onclick="downloadReadme()">Download Readme</button>
        </form>
      </div>
    </div>

    <!-- Markdown Preview Section -->
    <div id="additional-information" class="hidden">
      <h2>Generated Markdown</h2>
      <div id="markdown" style="white-space: pre-wrap;"></div>
    </div>
  </main>

  <script src="https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.js"></script>
  <script>
    // EasyMDE instances
    const notesMarkdown = new EasyMDE({ element: document.getElementById('notes') });
    const compileMarkdown = new EasyMDE({ element: document.getElementById('compile') });

    let markdown = '';

    // Add Steam instructions to the notes
    function addSteamInstructions() {
      const steamCommand = document.getElementById("steamCommand").value;
      let notes = notesMarkdown.value();
      const instructions = `### Steam Instructions\n* [Open Steam console](steam://open/console)\n* Copy and paste command: ${steamCommand}`;
      notes += `\n\n${instructions}`;
      notesMarkdown.value(notes);
      renderMarkdown();
    }

    // Add a new row for button mapping
    function addButtonMapping() {
      const table = document.getElementById("buttons").getElementsByTagName('tbody')[0];
      const row = table.insertRow();
      const cell1 = row.insertCell(0);
      const cell2 = row.insertCell(1);
      const cell3 = row.insertCell(2);

      cell1.innerHTML = '<input type="text" class="form-control" oninput="renderMarkdown()">';
      cell2.innerHTML = '<input type="text" class="form-control" oninput="renderMarkdown()">';
      cell3.innerHTML = '<button type="button" class="btn btn-danger btn-sm" onclick="deleteRow(this)">Delete</button>';
    }

    // Delete a row from the table
    function deleteRow(button) {
      const row = button.closest('tr');
      row.remove();
      renderMarkdown();
    }

    // Render markdown preview
    function renderMarkdown() {
      markdown = '';

      let notes = notesMarkdown.value();
      if (notes) markdown += `## Notes\n\n${notes}\n`;

      let compile = compileMarkdown.value();
      if (compile) markdown += `## Compile\n\n\`\`\`shell\n${compile}\n\`\`\`\n`;

      let controls = '';
      const table = document.getElementById("buttons");
      for (let i = 1, row; row = table.rows[i]; i++) {
        const button = row.cells[0].getElementsByTagName('input')[0].value;
        const action = row.cells[1].getElementsByTagName('input')[0].value;
        controls += `| ${button} | ${action} |\n`;
      }
      if (controls) markdown += `## Controls\n\n| Button | Action |\n| --- | --- |\n${controls}\n`;

      // Display the markdown preview
      const markdownElement = document.getElementById("markdown");
      markdownElement.innerHTML = markdown.replace(/\n/g, '<br>');  // Basic markdown to HTML conversion

      document.getElementById("additional-information").classList.remove("hidden");
    }

    // Download the generated README.md file
    function downloadReadme() {
      const blob = new Blob([markdown], { type: 'text/markdown' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = 'README.md';
      link.click();
    }
  </script>
</body>
</html>


