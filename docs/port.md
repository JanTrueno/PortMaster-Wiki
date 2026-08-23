---
title: Port Details - PortMaster Wiki
hide:
  - navigation
  - toc
  - path

search:
  exclude: true

# This page's screenshot/store-link images are all injected client-side by
# JS after load, so there's nothing for glightbox to wrap at build time -
# but its static markup (multiple <a> action buttons each with a nested
# <i> icon, no <img> between them) triggers catastrophic backtracking in
# glightbox's on_page_content regex, which was taking 175+ seconds on this
# one small page alone and dominating the entire site build. See the same
# fix on games.md/porters.md.
glightbox: false
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
    <a href="../games/" class="hero-btn hero-btn-secondary">Browse All Games</a>
  </div>

  <div class="port-page-content" id="port-page-content" style="display:none">

    <!-- Title block sits above both columns, store-page style: back link,
         big title, then a thin meta line (status + porter). -->
    <div class="port-titlebar">
      <a href="../games/" class="port-breadcrumb"><i class="bi bi-arrow-left"></i> All games</a>
      <h1 class="port-title" id="port-title"></h1>
      <div class="port-title-meta">
        <span class="port-title-porter" id="port-title-porter"></span>
      </div>
    </div>

    <!-- Two columns: media + long-form content on the left, a sticky
         purchase-style rail on the right. .port-hero is a direct child (not
         nested in .port-main) so that when this collapses to one column the
         DOM order becomes screenshot -> download rail -> readme, keeping the
         download button near the top instead of below the whole readme. -->
    <div class="port-layout">

      <div class="port-hero">
        <img src="" alt="" class="port-hero-img off-glb" id="port-screenshot">
      </div>

      <aside class="port-sidebar">
        <div class="port-sidebar-inner">
          <div class="port-status" id="port-status">
            <i class="bi bi-lightning-charge-fill" id="port-status-icon"></i>
            <span id="port-status-text">&mdash;</span>
          </div>
          <p class="port-status-note" id="port-status-note"></p>

          <a href="#" class="modal-download-btn port-download-cta" id="port-download-btn">Download</a>

          <div class="device-chip-wrapper">
            <button type="button" class="device-filter-btn" id="device-chip-btn" title="Check compatibility with your device">
              <span class="device-chip-dot" id="device-chip-dot"></span>
              <i class="bi bi-controller"></i>
              <span class="device-chip-label">Check your device</span>
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

          <!-- Spec sheet: label left, value right, hairline between rows. -->
          <dl class="port-facts">
            <div class="port-fact">
              <dt>Porter</dt>
              <dd id="port-porter-full">&mdash;</dd>
            </div>
            <div class="port-fact">
              <dt>Downloads</dt>
              <dd id="port-downloads">&mdash;</dd>
            </div>
            <div class="port-fact">
              <dt>Runtimes</dt>
              <dd id="port-runtimes">&mdash;</dd>
            </div>
            <div class="port-fact">
              <dt>Architecture</dt>
              <dd id="port-arch">&mdash;</dd>
            </div>
            <div class="port-fact">
              <dt>Date Added</dt>
              <dd id="port-date-added">&mdash;</dd>
            </div>
            <div class="port-fact">
              <dt>Last Updated</dt>
              <dd id="port-date-updated">&mdash;</dd>
            </div>
          </dl>

          <div class="port-store-links" id="port-store-links" style="display:none"></div>

          <button class="share-btn" id="port-share-btn" title="Share port" type="button">
            <i class="bi bi-share"></i> <span>Share</span>
          </button>
        </div>
      </aside>

      <div class="port-main">
        <div class="port-description" id="port-desc"></div>

        <div class="port-tag-groups">
          <div class="port-tag-group" id="port-genres-group">
            <h2 class="port-tag-heading">Genres</h2>
            <div class="port-tag-list" id="port-genres"></div>
          </div>
          <div class="port-tag-group" id="port-reqs-group">
            <h2 class="port-tag-heading">Requirements</h2>
            <div class="port-tag-list" id="port-reqs"></div>
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

    <!-- Similar games: built client-side from the port_details.json this
         page already loads, so it costs no extra request. Hidden entirely
         when the port has no genres to match on. -->
    <div class="port-similar" id="port-similar" style="display:none">
      <div class="carousel-section-header">
        <div class="carousel-section-title">
          <h2>Similar Games</h2>
        </div>
        <div class="carousel-nav">
          <div class="carousel-btn-group">
            <button class="carousel-btn" type="button" id="port-similar-prev" aria-label="Scroll left">
              <i class="bi bi-chevron-left"></i>
            </button>
            <button class="carousel-btn" type="button" id="port-similar-next" aria-label="Scroll right">
              <i class="bi bi-chevron-right"></i>
            </button>
          </div>
        </div>
      </div>
      <div class="carousel-container">
        <div class="carousel-track" id="port-similar-track"></div>
      </div>
    </div>

  </div>
</div>

<script src="../javascripts/port-page.js"></script>
