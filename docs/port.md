---
title: Port Details - PortMaster Wiki
hide:
  - navigation
  - toc
  - path

search:
  exclude: true
---

<div style="display:none">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
</div>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>.md-path { display: none; }</style>

<div class="port-page" id="port-page-root">
  <div id="port-page-loading" class="port-page-loading">Loading...</div>

  <div id="port-page-notfound" class="port-page-not-found" style="display:none">
    <p>We couldn't find that port.</p>
    <a href="../all-games/" class="md-button">Browse All Games</a>
  </div>

  <div class="port-page-content" id="port-page-content" style="display:none">
    <div class="port-hero">
      <a href="../all-games/" class="port-hero-back" title="Back to All Games"><i class="bi bi-arrow-left"></i></a>
      <img src="" alt="" class="port-hero-img off-glb" id="port-screenshot">
    </div>

    <div class="port-body">
      <h1 class="port-title" id="port-title"></h1>

      <div class="port-stat-pills" id="port-stat-pills">
        <div class="port-stat-pill">
          <i class="bi bi-download"></i>
          <div>
            <span class="port-stat-value" id="port-stat-downloads">—</span>
            <span class="port-stat-label">Downloads</span>
          </div>
        </div>
        <div class="port-stat-pill">
          <i class="bi bi-person-workspace"></i>
          <div>
            <span class="port-stat-value" id="port-stat-porter">—</span>
            <span class="port-stat-label">Porter</span>
          </div>
        </div>
        <div class="port-stat-pill" id="port-stat-rtr-pill">
          <i class="bi bi-lightning-charge-fill" id="port-stat-rtr-icon"></i>
          <div>
            <span class="port-stat-value" id="port-stat-rtr">—</span>
            <span class="port-stat-label">Status</span>
          </div>
        </div>
      </div>

      <div class="port-description" id="port-desc"></div>

      <div class="port-actions">
        <a href="#" class="modal-download-btn" id="port-download-btn">Download</a>
        <div class="port-store-links" id="port-store-links" style="display:none"></div>
        <div class="device-chip-wrapper">
          <button type="button" class="device-filter-btn" id="device-chip-btn" title="Check compatibility with your device">
            <span class="device-chip-dot" id="device-chip-dot"></span>
            <i class="bi bi-controller"></i>
          </button>
          <div class="device-chip-popover" id="device-chip-popover" style="display:none">
            <label for="device-chip-device">Device</label>
            <select id="device-chip-device">
              <option value="">Select your device...</option>
            </select>
            <label for="device-chip-os">Operating System</label>
            <select id="device-chip-os" disabled>
              <option value="">Select OS...</option>
            </select>
            <p class="device-chip-hint" id="device-chip-hint"></p>
          </div>
        </div>
        <button class="share-btn" id="port-share-btn" title="Share port" type="button">
          <i class="bi bi-share"></i>
        </button>
      </div>
    </div>

    <div class="modal-text-section" id="port-inst-section" style="display:none">
      <h2 class="modal-section-title">Instructions</h2>
      <div class="modal-text-content" id="port-inst"></div>
    </div>

    <div class="modal-text-section">
      <h2 class="modal-section-title">Additional Information</h2>
      <div class="modal-text-content" id="port-readme">
        <div class="loading-spinner">Loading...</div>
      </div>
    </div>

    <div class="modal-details-section">
      <h2 class="modal-section-title">Port Details</h2>

      <div class="modal-info-grid">
        <div class="info-item">
          <i class="info-icon bi bi-dpad"></i>
          <div class="info-content">
            <h3 class="info-heading">Genres</h3>
            <div class="info-value" id="port-genres">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-card-checklist"></i>
          <div class="info-content">
            <h3 class="info-heading">Requirements</h3>
            <div class="info-value" id="port-reqs">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-person-workspace"></i>
          <div class="info-content">
            <h3 class="info-heading">Porter</h3>
            <div class="info-value" id="port-porter-full">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-download"></i>
          <div class="info-content">
            <h3 class="info-heading">Downloads</h3>
            <div class="info-value" id="port-downloads">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-cpu"></i>
          <div class="info-content">
            <h3 class="info-heading">Runtimes</h3>
            <div class="info-value" id="port-runtimes">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-motherboard"></i>
          <div class="info-content">
            <h3 class="info-heading">Architecture</h3>
            <div class="info-value" id="port-arch">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-calendar-plus"></i>
          <div class="info-content">
            <h3 class="info-heading">Date Added</h3>
            <div class="info-value" id="port-date-added">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-calendar-check"></i>
          <div class="info-content">
            <h3 class="info-heading">Last Updated</h3>
            <div class="info-value" id="port-date-updated">—</div>
          </div>
        </div>

        <div class="info-item">
          <i class="info-icon bi bi-boxes"></i>
          <div class="info-content">
            <h3 class="info-heading">Miscellaneous</h3>
            <div class="info-value" id="port-misc">—</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script src="../javascripts/port-page.js"></script>
