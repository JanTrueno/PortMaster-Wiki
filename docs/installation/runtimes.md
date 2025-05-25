# Runtimes
PortMaster runtimes are shared engines or frameworks required for some ports to run. Sharing the runtimes between ports allows us to reduce the overall size of the port to save space on the device. 

!!! info 
    Runtimes are automatically installed on devices with an internet connection. If you have an offline device please use the [**Full Portmaster Installer**](installing-portmaster.md)!

## Download runtimes

<div id="utils-list">Loading runtimes...</div>

<script>
  fetch('../../assets/json/ports.json')
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      return response.json();
    })
    .then(data => {
      const utils = data.utils;

      if (!utils || Object.keys(utils).length === 0) {
        document.getElementById('utils-list').textContent = 'No utils found.';
        return;
      }

      const filteredEntries = Object.entries(utils).filter(([key, entry]) => {
        const lowerKey = key.toLowerCase();
        // Filter out keys with images/gameinfo AND only include aarch64 arch
        return !lowerKey.includes('images') &&
               !lowerKey.includes('gameinfo') &&
               entry.runtime_arch === 'aarch64';
      });

      if (filteredEntries.length === 0) {
        document.getElementById('utils-list').textContent = 'No utils found after filtering.';
        return;
      }

      const rows = filteredEntries.map(([key, entry]) => {
        const sizeMB = entry.size ? (entry.size / (1024 * 1024)).toFixed(1) : 'N/A';
        return `
          <tr>
            <td align="left">
              <a href="${entry.url}" target="_blank" rel="noopener" style="display:block; width:100%; height:100%; text-decoration:none; color:inherit;">
                ${entry.name || key}
              </a>
            </td>
            <td align="right">
              <a href="${entry.url}" target="_blank" rel="noopener" style="display:block; width:100%; height:100%; text-decoration:none; color:inherit;">
                ${sizeMB} MB
              </a>
            </td>
          </tr>
        `;
      }).join('');

      document.getElementById('utils-list').innerHTML = `
        <table width="100%" border="0" cellspacing="0" cellpadding="5">
          <thead>
            <tr>
              <th width="100%" align="left">Runtime Name</th>
              <th width="100%" align="right">Size</th>
            </tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      `;
    })
    .catch(err => {
      document.getElementById('utils-list').textContent = 'Error loading utils: ' + err.message;
      console.error(err);
    });
</script>

