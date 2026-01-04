---
hide:
  - navigation
  - toc
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">

<div class="preview-container" style="max-width: 1200px; margin: 0 auto; display: block !important; width: 100%;">
  <img class="off-glb" src="assets/images/retroid-pocket-5.png"/>
  <video class="overlay-video" autoplay loop muted playsinline>
    <source src="assets/videos/homepage.mp4" type="video/mp4">
  </video>
</div>

<div style="text-align: center; margin: 2rem 0;">
  <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">Welcome to PortMaster</h1>
  <p style="font-size: 1.25rem; color: var(--md-default-fg-color--light); margin-bottom: 2rem;">Your all-in-one manager for native game ports on Linux-based handhelds</p>
</div>

<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; padding: 2rem; background: linear-gradient(135deg, rgba(77, 190, 238, 0.1), rgba(77, 190, 238, 0.05)); border-radius: 12px; margin: 2rem 0; text-align: center;">
  <div>
    <div id="portCount" style="font-size: 2.5rem; font-weight: 700; color: #4DBEEE; margin-bottom: 0.5rem;">0</div>
    <div style="font-size: 0.9rem; color: var(--md-default-fg-color--light); text-transform: uppercase; letter-spacing: 0.5px;">Game Ports</div>
  </div>
  <div>
    <div style="font-size: 2.5rem; font-weight: 700; color: #4DBEEE; margin-bottom: 0.5rem;">50+</div>
    <div style="font-size: 0.9rem; color: var(--md-default-fg-color--light); text-transform: uppercase; letter-spacing: 0.5px;">Supported Devices</div>
  </div>
  <div>
    <div style="font-size: 2.5rem; font-weight: 700; color: #4DBEEE; margin-bottom: 0.5rem;">Active</div>
    <div style="font-size: 0.9rem; color: var(--md-default-fg-color--light); text-transform: uppercase; letter-spacing: 0.5px;">Community</div>
  </div>
  <div>
    <div style="font-size: 2.5rem; font-weight: 700; color: #4DBEEE; margin-bottom: 0.5rem;">Free</div>
    <div style="font-size: 0.9rem; color: var(--md-default-fg-color--light); text-transform: uppercase; letter-spacing: 0.5px;">Open Source</div>
  </div>
</div>

<script>
(function() {
  const totalPorts = {{ ports['ports'] | length }};
  const roundedPorts = Math.floor(totalPorts / 100) * 100;
  const portCountEl = document.getElementById('portCount');
  let current = 0;
  const duration = 1000;
  const increment = roundedPorts / (duration / 16);
  
  function updateCount() {
    current += increment;
    if (current < roundedPorts) {
      portCountEl.textContent = Math.floor(current) + '+';
      requestAnimationFrame(updateCount);
    } else {
      portCountEl.textContent = roundedPorts + '+';
    }
  }
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        updateCount();
        observer.disconnect();
      }
    });
  });
  
  observer.observe(portCountEl);
})();
</script>

<h2>Recently Added Ports</h2>

<div class="carousel-container">
  <button class="carousel-btn carousel-btn-left" onclick="scrollCarousel(-1)">
    <i class="bi bi-chevron-left"></i>
  </button>
  <div class="carousel-track" id="newPortsCarousel">
    {% set prev_month_ts = now().timestamp() - 2592000 %}
    {% set thirty_days_ago_str = now().fromtimestamp(prev_month_ts).strftime('%Y-%m-%d') %}
    {% set count = namespace(value=0) %}
    
    {% for port_key in sorted_orders['date-added'] %}
      {% set port = ports['ports'][port_key] %}
      {% set source = port.source or {} %}
      {% set date_added = source.date_added or '' %}
      
      {% if date_added and date_added >= thirty_days_ago_str and count.value < 20 %}
        {% set count.value = count.value + 1 %}
        {% set port_id = port_key.replace('.zip', '') %}
        {% set attr = port.attr or {} %}
        {% set title = attr.title or port_id %}
        {% set screenshot = attr.image.screenshot if attr.image else '' %}
        {% set downloads = port_stats.ports[port_key] | default(0) %}
        {% set is_mv = 'PortMaster-MV' in (source.url or '') or 'MV-New' in (source.url or '') %}
        {% set repo_owner = 'PortsMaster-MV' if is_mv else 'PortsMaster' %}
        {% set repo_name = 'PortMaster-MV-New' if is_mv else 'PortMaster-New' %}
        
        <div class="carousel-card" onclick="window.location.href='games/#modal-{{ port_id }}'">
          {% if screenshot %}
          <img src="https://raw.githubusercontent.com/{{ repo_owner }}/{{ repo_name }}/refs/heads/main/ports/{{ port_id }}/{{ screenshot }}" 
               alt="{{ title }}" 
               loading="lazy"
               onerror="this.style.display='none'">
          {% endif %}
          <h3>{{ title }}</h3>
          <div class="card-stats">
            <span class="card-stat">
              <i class="bi bi-download"></i>
              {{ downloads | default(0) }}
            </span>
            <span class="card-stat">
              <i class="bi bi-calendar-plus"></i>
              {{ date_added }}
            </span>
          </div>
        </div>
      {% endif %}
    {% endfor %}
  </div>
  <button class="carousel-btn carousel-btn-right" onclick="scrollCarousel(1)">
    <i class="bi bi-chevron-right"></i>
  </button>
</div>

<script>
function scrollCarousel(direction) {
  const track = document.getElementById('newPortsCarousel');
  const cards = track.querySelectorAll('.carousel-card');
  if (cards.length > 0) {
    const cardWidth = cards[0].offsetWidth + 16; 
    track.scrollBy({ left: direction * cardWidth, behavior: 'smooth' });
  }
}
</script>

<h2>How It Works</h2>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin: 2rem 0;">
  <div style="text-align: center; padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 12px;">
    <div style="display: inline-flex; align-items: center; justify-content: center; width: 50px; height: 50px; background: linear-gradient(135deg, #4DBEEE, #3ba9d4); color: white; font-size: 1.5rem; font-weight: 700; border-radius: 50%; margin-bottom: 1rem;">1</div>
    <h3 style="font-size: 1.1rem; margin: 0.5rem 0;">Launch PortMaster</h3>
    <p style="color: var(--md-default-fg-color--light); font-size: 0.85rem; margin: 0.5rem 0 0 0;">Pre-installed on most custom firmware or <a href="installation/installing-portmaster/" style="color: #4DBEEE;">quick to install</a></p>
  </div>
  <div style="text-align: center; padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 12px;">
    <div style="display: inline-flex; align-items: center; justify-content: center; width: 50px; height: 50px; background: linear-gradient(135deg, #4DBEEE, #3ba9d4); color: white; font-size: 1.5rem; font-weight: 700; border-radius: 50%; margin-bottom: 1rem;">2</div>
    <h3 style="font-size: 1.1rem; margin: 0.5rem 0;">Browse & Install</h3>
    <p style="color: var(--md-default-fg-color--light); font-size: 0.85rem; margin: 0.5rem 0 0 0;">Browse in-app or on our <a href="games/" style="color: #4DBEEE;">website</a>, then install directly</p>
  </div>
  <div style="text-align: center; padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 12px;">
    <div style="display: inline-flex; align-items: center; justify-content: center; width: 50px; height: 50px; background: linear-gradient(135deg, #4DBEEE, #3ba9d4); color: white; font-size: 1.5rem; font-weight: 700; border-radius: 50%; margin-bottom: 1rem;">3</div>
    <h3 style="font-size: 1.1rem; margin: 0.5rem 0;">Play!</h3>
    <p style="color: var(--md-default-fg-color--light); font-size: 0.85rem; margin: 0.5rem 0 0 0;">Dependencies handled automatically—just launch and enjoy</p>
  </div>
</div>

<h2>Key Features</h2>

<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin: 2rem 0;">
  <div style="padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 8px;">
    <i class="bi bi-joystick" style="font-size: 2rem; color: #4DBEEE; display: block; margin-bottom: 0.75rem;"></i>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Massive Library</h3>
    <p style="margin: 0; font-size: 0.9rem; color: var(--md-default-fg-color--light);">Browse and install from over 1000 native game ports</p>
  </div>
  <div style="padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 8px;">
    <i class="bi bi-funnel" style="font-size: 2rem; color: #4DBEEE; display: block; margin-bottom: 0.75rem;"></i>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Smart Filtering</h3>
    <p style="margin: 0; font-size: 0.9rem; color: var(--md-default-fg-color--light);">Filter by genre, runtime, updates, and installation status</p>
  </div>
  <div style="padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 8px;">
    <i class="bi bi-download" style="font-size: 2rem; color: #4DBEEE; display: block; margin-bottom: 0.75rem;"></i>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Easy Management</h3>
    <p style="margin: 0; font-size: 0.9rem; color: var(--md-default-fg-color--light);">Install, update, or uninstall with ease</p>
  </div>
  <div style="padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 8px;">
    <i class="bi bi-eye" style="font-size: 2rem; color: #4DBEEE; display: block; margin-bottom: 0.75rem;"></i>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Preview First</h3>
    <p style="margin: 0; font-size: 0.9rem; color: var(--md-default-fg-color--light);">Preview games before installing to make informed choices</p>
  </div>
  <div style="padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 8px;">
    <i class="bi bi-gear" style="font-size: 2rem; color: #4DBEEE; display: block; margin-bottom: 0.75rem;"></i>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Auto Dependencies</h3>
    <p style="margin: 0; font-size: 0.9rem; color: var(--md-default-fg-color--light);">Automatic handling of dependencies and runtimes</p>
  </div>
  <div style="padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 8px;">
    <i class="bi bi-palette" style="font-size: 2rem; color: #4DBEEE; display: block; margin-bottom: 0.75rem;"></i>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Customizable</h3>
    <p style="margin: 0; font-size: 0.9rem; color: var(--md-default-fg-color--light);">Personalize with customizable themes</p>
  </div>
  <div style="padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 8px;">
    <i class="bi bi-lightning" style="font-size: 2rem; color: #4DBEEE; display: block; margin-bottom: 0.75rem;"></i>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Optimized Performance</h3>
    <p style="margin: 0; font-size: 0.9rem; color: var(--md-default-fg-color--light);">Lightweight and fast for handheld devices</p>
  </div>
  <div style="padding: 1.5rem; background: var(--md-code-bg-color); border-radius: 8px;">
    <i class="bi bi-cpu" style="font-size: 2rem; color: #4DBEEE; display: block; margin-bottom: 0.75rem;"></i>
    <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">Wide Compatibility</h3>
    <p style="margin: 0; font-size: 0.9rem; color: var(--md-default-fg-color--light);">Compatible with major Linux-based firmware</p>
  </div>
</div>

<div style="padding: 2rem; background: var(--md-code-bg-color); border-radius: 12px; margin: 2rem 0;">
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start;">
    <div>
      <h3 style="font-size: 1.5rem; margin: 0 0 1rem 0;">Game Showcase</h3>
      <p>From beloved indie titles to retro classics, PortMaster brings an incredible variety of games to your handheld device.</p>
      <p>Every port is optimized for performance and playability. Our community of dedicated porters brings new games every week.</p>
      <p><a href="games/" class="md-button">Explore All Games</a></p>
    </div>
    <div style="position: relative; width: 100%; padding-bottom: 56.25%; background: #000; border-radius: 8px; overflow: hidden;">
      <iframe src="https://player.vimeo.com/video/1083313795?badge=0&autopause=0&player_id=0&app_id=58479" 
              frameborder="0" 
              allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media" 
              style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
              title="PortMaster Game Showcase">
      </iframe>
    </div>
  </div>
</div>

<script src="https://player.vimeo.com/api/player.js"></script>

<div style="text-align: center; padding: 2rem; background: var(--md-code-bg-color); border-radius: 12px; margin: 2rem 0;">
  <h3 style="font-size: 1.5rem; margin: 0 0 1rem 0;">Compatible Devices</h3>
  <p style="margin: 0 0 1.5rem 0;">PortMaster works seamlessly with <strong>50+ Linux-based handheld devices</strong>, including popular custom firmware like AmberELEC, ArkOS, and muOS.</p>
  <a href="installation/supported-handhelds/" class="md-button">See All Supported Devices</a>
</div>

<div style="text-align: center; padding: 2rem; background: var(--md-code-bg-color); border-radius: 12px; margin: 2rem 0;">
  <h3 style="font-size: 1.5rem; margin: 0 0 1rem 0;">Connect with Fellow Handheld Enthusiasts</h3>
  <p style="max-width: 600px; margin: 0 auto 1.5rem; color: var(--md-default-fg-color--light);">Join thousands of handheld gaming enthusiasts on our Discord server. Share your favorite ports, get help with installation, contribute to the project, and stay updated on the latest releases.</p>
  <a href="https://discord.gg/eqjK6yNQS4" class="md-button" style="display: inline-flex; align-items: center; gap: 0.5rem;">
    <i class="bi bi-discord"></i> Join Our Discord
  </a>
</div>

<div style="padding: 2rem; background: var(--md-code-bg-color); border-radius: 12px; margin: 2rem 0;">
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: start;">
    <div>
      <h3 style="font-size: 1.5rem; margin: 0 0 1rem 0;">Port of the Month</h3>
      <p>Every month we feature a community challenge port where you can compete for the best score! Join fellow porters in testing your skills and climbing the leaderboard.</p>
      <p>Discuss strategies, share your scores, and see how you rank against the community.</p>
      <p><a href="https://discordapp.com/channels/1122861252088172575/1249310815312678993" class="md-button" style="display: inline-flex; align-items: center; gap: 0.5rem;">
        <i class="bi bi-discord"></i> Join the Challenge
      </a></p>
    </div>
    <div>
      {% set port_key = 'barhop.zip' %}
      {% set port = ports['ports'][port_key] %}
      {% set port_id = port_key.replace('.zip', '') %}
      {% set attr = port.attr or {} %}
      {% set title = attr.title or port_id %}
      {% set screenshot = attr.image.screenshot if attr.image else '' %}
      {% set downloads = port_stats.ports[port_key] | default(0) %}
      {% set source = port.source or {} %}
      {% set date_added = source.date_added or '' %}
      {% set is_mv = 'PortMaster-MV' in (source.url or '') or 'MV-New' in (source.url or '') %}
      {% set repo_owner = 'PortsMaster-MV' if is_mv else 'PortsMaster' %}
      {% set repo_name = 'PortMaster-MV-New' if is_mv else 'PortMaster-New' %}
      
      <div class="carousel-card" onclick="window.location.href='games/#modal-{{ port_id }}'" style="cursor: pointer; max-width: 400px; margin: 0 auto;">
        {% if screenshot %}
        <img src="https://raw.githubusercontent.com/{{ repo_owner }}/{{ repo_name }}/refs/heads/main/ports/{{ port_id }}/{{ screenshot }}" 
             alt="{{ title }}" 
             loading="lazy"
             onerror="this.style.display='none'">
        {% endif %}
        <h3>{{ title }}</h3>
        <div class="card-stats">
          <span class="card-stat">
            <i class="bi bi-download"></i>
            {{ downloads | default(0) }}
          </span>
          <span class="card-stat">
            <i class="bi bi-calendar-plus"></i>
            {{ date_added }}
          </span>
        </div>
      </div>
    </div>
  </div>
</div>

<div style="text-align: center; padding: 2rem; background: var(--md-code-bg-color); border-radius: 12px; margin: 2rem 0;">
  <h3 style="font-size: 1.5rem; margin: 0 0 1rem 0;">Open Source</h3>
  <p style="margin: 0 0 1.5rem 0;">PortMaster is open-source and built by a passionate global community. Thanks to all contributors who help make handheld gaming accessible and enjoyable for everyone.</p>
  <a href="https://github.com/PortsMaster/PortMaster-New" class="md-button" style="display: inline-flex; align-items: center; gap: 0.5rem;">
    <i class="bi bi-github"></i> View on GitHub
  </a>
</div>

