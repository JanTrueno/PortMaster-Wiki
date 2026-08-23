---
hide:
  - navigation
  - toc
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">

{% set total_downloads = port_stats.get('total_downloads', 0) %}
{% set porter_count = porters | length %}
{% set device_count = devices | length %}

{% set prev_month_ts = now().timestamp() - 2592000 %}
{% set thirty_days_ago_str = now().fromtimestamp(prev_month_ts).strftime('%Y-%m-%d') %}
{% set new_this_month = namespace(value=0) %}
{% for port_key, port in ports['ports'].items() %}
  {% set source = port.source or {} %}
  {% if (source.date_added or '') >= thirty_days_ago_str %}
    {% set new_this_month.value = new_this_month.value + 1 %}
  {% endif %}
{% endfor %}

<!-- ===== HERO ===== -->
<section class="hero">
  <div class="hero-content">
    <h1>Real PC &amp; indie games, running natively on your handheld</h1>
    <p class="hero-subtitle">Stardew Valley, Celeste, Balatro, Limbo, and {{ total_port_count }}+ more &mdash; installed and running on cheap Linux-based handhelds with PortMaster. Completely free. Not emulation.</p>
    <div class="hero-cta-group">
      <a href="games/" class="hero-btn hero-btn-primary">Discover {{ total_port_count }}+ Games</a>
      <a href="installation/installing-portmaster/" class="hero-btn hero-btn-secondary">Get PortMaster</a>
    </div>
  </div>
  <div class="hero-visual">
    <div class="preview-container">
      <img class="off-glb" src="assets/images/retroid-pocket-5.png" alt="A handheld gaming device running PortMaster"/>
      <video class="overlay-video" autoplay loop muted playsinline>
        <source src="assets/videos/homepage.mp4" type="video/mp4">
      </video>
    </div>
  </div>
</section>

<!-- ===== STATS CARDS ===== -->
<section class="home-section">
  <div class="stats-cards-grid">
    <div class="stats-card">
      <i class="bi bi-download stats-card-icon"></i>
      <span class="stats-card-value">{{ "{:,}".format(total_downloads) }}</span>
      <span class="stats-card-label">Downloads</span>
    </div>
    <div class="stats-card">
      <i class="bi bi-controller stats-card-icon"></i>
      <span class="stats-card-value">{{ device_count }}+</span>
      <span class="stats-card-label">Devices Supported</span>
    </div>
    <div class="stats-card">
      <i class="bi bi-person-workspace stats-card-icon"></i>
      <span class="stats-card-value">{{ porter_count }}</span>
      <span class="stats-card-label">Porters</span>
    </div>
    <div class="stats-card">
      <i class="bi bi-calendar-plus stats-card-icon"></i>
      <span class="stats-card-value">{{ new_this_month.value }}</span>
      <span class="stats-card-label">Added This Month</span>
    </div>
  </div>
</section>

<!-- ===== SHOWCASE (the library) ===== -->
<section class="showcase">
  <div class="showcase-mosaic" aria-hidden="true">
    {% for tile in mosaic_ports %}
      <img class="off-glb" src="https://raw.githubusercontent.com/{{ tile.repo }}/refs/heads/main/ports/{{ tile.id }}/{{ tile.screenshot }}" alt="" loading="lazy" onerror="this.style.visibility='hidden'">
    {% endfor %}
  </div>

  <div class="showcase-inner">
    <div class="showcase-text">
      <h2>{{ total_port_count }}+ games,<br>ready to install.</h2>
      <p>Stardew Valley, Celeste, Balatro, Half-Life, Doom &mdash; plus hundreds you've never heard of. Pick one, press install, play. No setup, no terminal.</p>
    </div>
  </div>

  <p class="showcase-caption">Every port is free and community-made &mdash; and runs on {{ device_count }}+ Linux handhelds.</p>
</section>

<!-- ===== GET INVOLVED (Community + Contribute) ===== -->
<section class="home-section">
  <div class="get-involved-grid">
    <div class="get-involved-card">
      <i class="bi bi-discord get-involved-icon"></i>
      <h3>Join the Community</h3>
      <p>Share your favorite ports, get help with installation, and stay updated on the latest releases with thousands of fellow handheld enthusiasts.</p>
      <a href="https://discord.gg/eqjK6yNQS4" class="hero-btn hero-btn-secondary">Join Our Discord</a>
    </div>
    <div class="get-involved-card">
      <i class="bi bi-github get-involved-icon"></i>
      <h3>Contribute</h3>
      <p>PortMaster is open-source and built by a passionate global community. Help make handheld gaming accessible for everyone.</p>
      <a href="https://github.com/PortsMaster/PortMaster-New" class="hero-btn hero-btn-secondary">View on GitHub</a>
    </div>
  </div>
</section>
