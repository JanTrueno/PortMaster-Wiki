---
title: Port Details - PortMaster Wiki
hide:
  - navigation
  - toc

search:
  exclude: true
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<div class="port-page" id="port-page-root">
  <a href="../all-games/" class="port-page-back"><i class="bi bi-arrow-left"></i> All Games</a>

  <div id="port-page-loading" class="port-page-loading">Loading...</div>

  <div id="port-page-notfound" class="port-page-not-found" style="display:none">
    <p>We couldn't find that port.</p>
    <a href="../all-games/" class="md-button">Browse All Games</a>
  </div>

  <div class="port-page-content" id="port-page-content" style="display:none">
    <div class="modal-header-section">
      <h1 class="modal-main-title" id="port-title"></h1>

      <div class="modal-screenshot-container" id="port-screenshot-container">
        <img src="" alt="" class="modal-screenshot" id="port-screenshot">
      </div>

      <div class="modal-description">
        <div class="desc-md" id="port-desc"></div>
      </div>

      <div class="modal-button-container">
        <div class="download-actions">
          <a href="#" class="modal-download-btn" id="port-download-btn">Download</a>
          <button class="share-btn" id="port-share-btn" title="Share port" type="button">
            <i class="bi bi-share"></i>
          </button>
        </div>
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
            <div class="info-value" id="port-porter">—</div>
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
  </div>
</div>

<script src="../javascripts/port-page.js"></script>
