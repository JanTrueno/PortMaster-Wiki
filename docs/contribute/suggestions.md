---
hide:
  - navigation
  - toc

search:
  exclude: true
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.1.0/dist/fuse.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<div class="filters-container">
  <div class="search-wrapper">
    <input type="text" id="searchInput" placeholder="Search suggestions..." class="search-bar">
    
    <!-- Sort Dropdown -->
    <div class="sort-dropdown-wrapper">
      <button class="sort-toggle-btn" id="sortToggleBtn">
        <i class="bi bi-sort-down"></i>
      </button>
      <div class="sort-dropdown" id="sortDropdown">
        <div class="sort-option" data-sort="az">A-Z</div>
        <div class="sort-option" data-sort="za">Z-A</div>
        <div class="sort-option selected" data-sort="votes">Most Votes</div>
        <div class="sort-option" data-sort="date-added">Date Added (Newest)</div>
      </div>
    </div>
    
    <button class="filter-toggle-btn" id="filterToggleBtn">
      <span></span>
      <span></span>
      <span></span>
    </button>
  </div>
  <p id="portsCounter">Showing: 0 suggestions</p>
</div>

<!-- Filter Overlay -->
<div class="filter-overlay" id="filterOverlay"></div>

<!-- Back to Top Button -->
<button class="back-to-top" id="backToTop">
  <i class="bi bi-arrow-up"></i>
</button>

<!-- Filter Panel -->
<div class="filter-panel" id="filterPanel">
  <div class="filter-panel-header">
    <h2>Filters</h2>
    <button class="close-panel-btn" id="closePanelBtn">&times;</button>
  </div>

  <div class="filter-group">
    <label for="statusSelect">Status</label>
    <select id="statusSelect" class="filter-dropdown">
      <option value="">All Statuses</option>
      <option value="Open">Open</option>
      <option value="Complete">Complete</option>
      <option value="Rejected">Rejected</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="feasibilitySelect">Feasibility</label>
    <select id="feasibilitySelect" class="filter-dropdown">
      <option value="">All Feasibility</option>
      <option value="High">High</option>
      <option value="Medium">Medium</option>
      <option value="Low">Low</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="categorySelect">Category</label>
    <select id="categorySelect" class="filter-dropdown">
      <option value="">All Categories</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="engineSelect">Engine</label>
    <select id="engineSelect" class="filter-dropdown">
      <option value="">All Engines</option>
    </select>
  </div>

  <div class="filter-group">
    <label for="contentSelect">Content Type</label>
    <select id="contentSelect" class="filter-dropdown">
      <option value="">All Types</option>
      <option value="Open Source">Open Source</option>
      <option value="Commercial">Commercial</option>
    </select>
  </div>

  <button class="clear-all-filters-btn" onclick="clearAllFilters()">
    <i class="bi bi-x-circle"></i> Clear All Filters
  </button>

  <div class="filter-group advanced-filters">
    <label class="advanced-label" onclick="toggleAdvancedFilters()">
      Advanced <i class="bi bi-chevron-down" id="advancedArrow"></i>
    </label>
    <div class="advanced-filters-content" id="advancedFiltersContent">
      <div class="filter-subgroup">
        <label>Language</label>
        <div class="filter-pills" id="languagePills"></div>
      </div>

      <div class="filter-subgroup">
        <label>License</label>
        <div class="filter-pills" id="licensePills"></div>
      </div>

      <div class="filter-subgroup">
        <label>Dependencies</label>
        <div class="filter-pills" id="dependenciesPills"></div>
      </div>

      <button class="clear-filters-btn" onclick="clearAdvancedFilters()">
        <i class="bi bi-x-circle"></i> Clear All
      </button>
    </div>
  </div>
</div>

<!-- Single Reusable Modal -->
<div id="suggestionModal" class="modal">
  <div class="modal-content">
    <span class="close" onclick="closeModal()">&times;</span>

    <div class="modal-header-section">
      <h1 class="modal-main-title" id="modal-title"></h1>
      
      <div class="modal-screenshot-container" id="modal-screenshot-container">
        <img src="" alt="" class="modal-screenshot no-lightbox" id="modal-screenshot">
      </div>

      <div class="modal-description" id="modal-description"></div>

      <div class="votes-display">
        <i class="bi bi-hand-thumbs-up-fill"></i>
        <span class="votes-number" id="modal-votes">0</span>
        <span class="votes-label">Votes</span>
      </div>

      <div class="modal-button-container">
        <a href="#" class="modal-download-btn" id="modal-website-btn" target="_blank" rel="noopener noreferrer">
          <i class="bi bi-globe"></i>&nbsp;&nbsp;Visit Website
        </a>
      </div>
    </div>

    <div class="modal-details-section">
      <h2 class="modal-section-title">Details</h2>
      <div class="modal-info-grid" id="modal-info-grid"></div>
    </div>

    <div class="modal-text-section" id="modal-comment-section">
      <h2 class="modal-section-title">Comments</h2>
      <div class="modal-text-content" id="modal-comment"></div>
    </div>
  </div>
</div>

<!-- Grid Container -->
<div class="game-grid" id="suggestionsGrid"></div>

<div class="no-results" id="noResults" style="display: none;">
  <i class="bi bi-search"></i>
  <p>No suggestions match your filters</p>
</div>

<script>
// Global variables
let suggestionsData = [];
let filteredSuggestions = [];
let currentSort = 'votes';

// Cookie utilities
function setCookie(name, value, days = 365) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = name + '=' + encodeURIComponent(value) + '; expires=' + expires + '; path=/; SameSite=Lax';
}

function getCookie(name) {
  return document.cookie.split('; ').reduce((r, v) => {
    const parts = v.split('=');
    return parts[0] === name ? decodeURIComponent(parts[1]) : r;
  }, '');
}

// Load suggestions from JSON
async function loadSuggestions() {
  try {
    const response = await fetch('../../assets/json/suggestions_new.json');
    suggestionsData = await response.json();
    console.log('Loaded suggestions:', suggestionsData.length);
    
    // Initialize filters
    initializeFilters();
    
    // Load saved filters
    loadFiltersFromCookies();
    
    // Apply initial sort and display
    applySortAndFilters();
  } catch (error) {
    console.error('Error loading suggestions:', error);
  }
}

// Initialize filter options
function initializeFilters() {
  // Categories
  const categories = [...new Set(suggestionsData.map(s => s.category).filter(Boolean))].sort();
  const categorySelect = document.getElementById('categorySelect');
  categories.forEach(cat => {
    const option = document.createElement('option');
    option.value = cat;
    option.textContent = cat;
    categorySelect.appendChild(option);
  });

  // Engines
  const engines = [...new Set(suggestionsData.map(s => s.engine).filter(Boolean))].sort();
  const engineSelect = document.getElementById('engineSelect');
  engines.forEach(eng => {
    const option = document.createElement('option');
    option.value = eng;
    option.textContent = eng;
    engineSelect.appendChild(option);
  });

  // Languages
  const languages = [...new Set(suggestionsData.map(s => s.language).filter(Boolean))].sort();
  const languagePills = document.getElementById('languagePills');
  languages.forEach(lang => {
    const pill = createFilterPill(lang, 'language');
    languagePills.appendChild(pill);
  });

  // Licenses
  const licenses = [...new Set(suggestionsData.map(s => s.license).filter(Boolean))].sort();
  const licensePills = document.getElementById('licensePills');
  licenses.forEach(lic => {
    const pill = createFilterPill(lic, 'license');
    licensePills.appendChild(pill);
  });

  // Dependencies
  const allDeps = suggestionsData.flatMap(s => 
    s.dependencies ? s.dependencies.split(',').map(d => d.trim()).filter(Boolean) : []
  );
  const dependencies = [...new Set(allDeps)].sort();
  const depPills = document.getElementById('dependenciesPills');
  dependencies.forEach(dep => {
    const pill = createFilterPill(dep, 'dependency');
    depPills.appendChild(pill);
  });
}

// Create filter pill
function createFilterPill(text, type) {
  const pill = document.createElement('div');
  pill.className = 'filter-pill';
  pill.textContent = text;
  pill.dataset.type = type;
  pill.dataset.value = text;
  
  pill.addEventListener('click', () => {
    pill.classList.toggle('selected');
    saveFiltersToCookies();
    applySortAndFilters();
  });
  
  return pill;
}

// Apply sorting and filtering
function applySortAndFilters() {
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  const statusFilter = document.getElementById('statusSelect').value;
  const feasibilityFilter = document.getElementById('feasibilitySelect').value;
  const categoryFilter = document.getElementById('categorySelect').value;
  const engineFilter = document.getElementById('engineSelect').value;
  const contentFilter = document.getElementById('contentSelect').value;
  
  // Get active pills
  const activeLanguages = getActivePills('language');
  const activeLicenses = getActivePills('license');
  const activeDependencies = getActivePills('dependency');
  
  // Filter suggestions
  filteredSuggestions = suggestionsData.filter(suggestion => {
    // Search filter
    if (searchTerm && !suggestion.title.toLowerCase().includes(searchTerm)) {
      return false;
    }
    
    // Status filter
    if (statusFilter && suggestion.status !== statusFilter) {
      return false;
    }
    
    // Feasibility filter
    if (feasibilityFilter && suggestion.feasibility !== feasibilityFilter) {
      return false;
    }
    
    // Category filter
    if (categoryFilter && suggestion.category !== categoryFilter) {
      return false;
    }
    
    // Engine filter
    if (engineFilter && suggestion.engine !== engineFilter) {
      return false;
    }
    
    // Content filter
    if (contentFilter && suggestion.content !== contentFilter) {
      return false;
    }
    
    // Language filter
    if (activeLanguages.length > 0 && !activeLanguages.includes(suggestion.language)) {
      return false;
    }
    
    // License filter
    if (activeLicenses.length > 0 && !activeLicenses.includes(suggestion.license)) {
      return false;
    }
    
    // Dependencies filter
    if (activeDependencies.length > 0) {
      const deps = suggestion.dependencies ? suggestion.dependencies.split(',').map(d => d.trim()) : [];
      if (!activeDependencies.some(dep => deps.includes(dep))) {
        return false;
      }
    }
    
    return true;
  });
  
  // Sort suggestions
  sortSuggestions();
  
  // Display
  displaySuggestions();
  updateCounter();
}

// Sort suggestions
function sortSuggestions() {
  switch (currentSort) {
    case 'az':
      filteredSuggestions.sort((a, b) => a.title.localeCompare(b.title));
      break;
    case 'za':
      filteredSuggestions.sort((a, b) => b.title.localeCompare(a.title));
      break;
    case 'votes':
      filteredSuggestions.sort((a, b) => (b.voteCount || 0) - (a.voteCount || 0));
      break;
    case 'date-added':
      filteredSuggestions.sort((a, b) => new Date(b.date) - new Date(a.date));
      break;
  }
}

// Display suggestions
function displaySuggestions() {
  const grid = document.getElementById('suggestionsGrid');
  const noResults = document.getElementById('noResults');
  
  grid.innerHTML = '';
  
  if (filteredSuggestions.length === 0) {
    grid.style.display = 'none';
    noResults.style.display = 'block';
    return;
  }
  
  grid.style.display = 'grid';
  noResults.style.display = 'none';
  
  filteredSuggestions.forEach(suggestion => {
    const card = createSuggestionCard(suggestion);
    grid.appendChild(card);
  });
}

// Create suggestion card
function createSuggestionCard(suggestion) {
  const card = document.createElement('div');
  card.className = 'game-card';
  
  // Add incompatible class for completed/rejected
  if (suggestion.status === 'Complete' || suggestion.status === 'Rejected') {
    card.classList.add('incompatible');
  }
  
  card.onclick = () => openModal(suggestion);
  
  // Image container with overlay icon
  const imageContainer = document.createElement('div');
  imageContainer.style.position = 'relative';
  
  // Image
  const img = document.createElement('img');
  img.src = suggestion.imageurl || '../../assets/images/placeholder.png';
  img.alt = suggestion.title;
  img.className = 'no-lightbox';
  img.style.backgroundColor = 'var(--md-default-bg-color)'; // Prevent flash
  img.onerror = function() {
    this.src = '../../assets/images/placeholder.png';
    this.style.backgroundColor = 'transparent';
  };
  img.onload = function() {
    this.style.backgroundColor = 'transparent';
  };
  
  imageContainer.appendChild(img);
  
  // Add overlay icon for completed/rejected
  if (suggestion.status === 'Complete') {
    const checkmark = document.createElement('i');
    checkmark.className = 'bi bi-check-circle-fill status-overlay-icon';
    checkmark.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 5rem; color: #4caf50 !important; opacity: 1 !important; filter: grayscale(0%) !important; -webkit-filter: grayscale(0%) !important; text-shadow: 0 4px 12px rgba(0,0,0,0.8); pointer-events: none; z-index: 10;';
    imageContainer.appendChild(checkmark);
  } else if (suggestion.status === 'Rejected') {
    const xmark = document.createElement('i');
    xmark.className = 'bi bi-x-circle-fill status-overlay-icon';
    xmark.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 5rem; color: #f44336 !important; opacity: 1 !important; filter: grayscale(0%) !important; -webkit-filter: grayscale(0%) !important; text-shadow: 0 4px 12px rgba(0,0,0,0.8); pointer-events: none; z-index: 10;';
    imageContainer.appendChild(xmark);
  }
  
  // Title
  const title = document.createElement('h3');
  title.textContent = suggestion.title;
  
  // Stats
  const stats = document.createElement('div');
  stats.className = 'card-stats';
  
  // Feasibility pill
  const feasibilityStat = document.createElement('div');
  feasibilityStat.className = 'card-stat';
  const feasibilityBadge = document.createElement('span');
  const feasibilityLevel = (suggestion.feasibility || 'Unknown').toLowerCase();
  feasibilityBadge.className = `feasibility-badge ${feasibilityLevel}`;
  feasibilityBadge.textContent = suggestion.feasibility || 'Unknown';
  
  // Add inline styles to ensure colors work and match modal pill shape
  const colors = {
    'high': '#4caf50',
    'medium': '#ff9800',
    'low': '#f44336',
    'unknown': '#9e9e9e'
  };
  if (colors[feasibilityLevel]) {
    feasibilityBadge.style.backgroundColor = colors[feasibilityLevel];
    feasibilityBadge.style.color = '#ffffff';
  }
  // Pill styling to match modal info badges
  feasibilityBadge.style.display = 'inline-block';
  feasibilityBadge.style.padding = '0.15rem 0.4rem';
  feasibilityBadge.style.borderRadius = '4px';
  feasibilityBadge.style.fontSize = '0.65rem';
  feasibilityBadge.style.fontWeight = '500';
  
  feasibilityStat.appendChild(feasibilityBadge);
  
  // Votes with status icon
  const votesStat = document.createElement('div');
  votesStat.className = 'card-stat';
  votesStat.innerHTML = `<i class="bi bi-hand-thumbs-up"></i> ${suggestion.voteCount || 0}`;
  
  stats.appendChild(feasibilityStat);
  stats.appendChild(votesStat);
  
  card.appendChild(imageContainer);
  card.appendChild(title);
  card.appendChild(stats);
  
  return card;
}

// Open modal
function openModal(suggestion) {
  const modal = document.getElementById('suggestionModal');
  
  // Set title
  document.getElementById('modal-title').textContent = suggestion.title;
  
  // Set screenshot
  const screenshot = document.getElementById('modal-screenshot');
  const screenshotContainer = document.getElementById('modal-screenshot-container');
  if (suggestion.imageurl) {
    screenshot.src = suggestion.imageurl;
    screenshot.alt = suggestion.title;
    screenshot.onerror = function() {
      this.src = '../../assets/images/placeholder.png';
    };
    screenshotContainer.style.display = 'block';
  } else {
    screenshot.src = '../../assets/images/placeholder.png';
    screenshot.alt = suggestion.title;
    screenshotContainer.style.display = 'block';
  }
  
  // Set description
  const description = document.getElementById('modal-description');
  description.textContent = suggestion.comment || 'No description available.';
  
  // Set votes
  document.getElementById('modal-votes').textContent = suggestion.voteCount || 0;
  
  // Set website button
  const websiteBtn = document.getElementById('modal-website-btn');
  if (suggestion.weburl) {
    websiteBtn.href = suggestion.weburl;
    websiteBtn.style.display = 'inline-flex';
  } else {
    websiteBtn.style.display = 'none';
  }
  
  // Build info grid
  const infoGrid = document.getElementById('modal-info-grid');
  infoGrid.innerHTML = '';
  
  const infoItems = [
    { icon: 'bi-file-text', label: 'License', value: suggestion.license || 'Unknown' },
    { icon: 'bi-box', label: 'Content', value: suggestion.content || 'Unknown' },
    { icon: 'bi-controller', label: 'Engine', value: suggestion.engine || 'Unknown' },
    { icon: 'bi-speedometer2', label: 'Feasibility', value: suggestion.feasibility || 'Unknown', badge: true },
    { icon: 'bi-flag', label: 'Status', value: suggestion.status || 'Unknown', badge: true },
    { icon: 'bi-code-square', label: 'Programming Language', value: suggestion.language || 'Unknown' },
    { icon: 'bi-folder', label: 'Category', value: suggestion.category || 'Unknown' },
    { icon: 'bi-link-45deg', label: 'Dependencies', value: suggestion.dependencies || 'None' },
    { icon: 'bi-hand-thumbs-up', label: 'Votes', value: (suggestion.voteCount || 0).toString() },
    { icon: 'bi-calendar', label: 'Date Added', value: formatDate(suggestion.date) }
  ];
  
  infoItems.forEach(item => {
    const infoItem = createInfoItem(item.icon, item.label, item.value, item.badge, item.isLink);
    infoGrid.appendChild(infoItem);
  });
  
  // Set comment
  const commentBox = document.getElementById('modal-comment');
  const commentSection = document.getElementById('modal-comment-section');
  if (suggestion.comment && suggestion.comment.trim()) {
    commentBox.textContent = suggestion.comment;
    commentSection.style.display = 'block';
  } else {
    commentSection.style.display = 'none';
  }
  
  // Show modal
  modal.style.display = 'block';
  setTimeout(() => modal.classList.add('show'), 10);
}

// Create info item
function createInfoItem(icon, label, value, isBadge = false, isLink = false) {
  const item = document.createElement('div');
  item.className = 'info-item';
  
  const iconElem = document.createElement('i');
  iconElem.className = `bi ${icon} info-icon`;
  
  const content = document.createElement('div');
  content.className = 'info-content';
  
  const heading = document.createElement('h3');
  heading.className = 'info-heading';
  heading.textContent = label;
  
  const valueElem = document.createElement('div');
  valueElem.className = 'info-value';
  
  if (isBadge) {
    if (label === 'Status') {
      const badge = document.createElement('span');
      badge.className = `status-badge ${value.toLowerCase()}`;
      badge.textContent = value;
      valueElem.appendChild(badge);
    } else if (label === 'Feasibility') {
      const badge = document.createElement('span');
      badge.className = `feasibility-badge ${value.toLowerCase()}`;
      badge.textContent = value;
      valueElem.appendChild(badge);
    }
  } else if (isLink && value !== 'N/A') {
    // Create clickable link
    const link = document.createElement('a');
    link.href = value;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.className = 'info-badge info-link';
    link.textContent = 'Visit';
    link.style.textDecoration = 'none';
    valueElem.appendChild(link);
  } else {
    // Wrap value in info-badge pill
    const badge = document.createElement('span');
    badge.className = 'info-badge';
    badge.textContent = value;
    valueElem.appendChild(badge);
  }
  
  content.appendChild(heading);
  content.appendChild(valueElem);
  
  item.appendChild(iconElem);
  item.appendChild(content);
  
  return item;
}

// Close modal
function closeModal() {
  const modal = document.getElementById('suggestionModal');
  modal.classList.remove('show');
  setTimeout(() => modal.style.display = 'none', 300);
}

// Format date
function formatDate(dateStr) {
  if (!dateStr) return 'Unknown';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

// Update counter
function updateCounter() {
  const counter = document.getElementById('portsCounter');
  const total = suggestionsData.length;
  const showing = filteredSuggestions.length;
  
  if (showing === total) {
    counter.textContent = `Showing: ${total} suggestions`;
  } else {
    counter.textContent = `Showing: ${showing} of ${total} suggestions`;
  }
}

// Get active pills
function getActivePills(type) {
  return Array.from(document.querySelectorAll(`.filter-pill[data-type="${type}"].selected`))
    .map(pill => pill.dataset.value);
}

// Save filters to cookies
function saveFiltersToCookies() {
  const filters = {
    status: document.getElementById('statusSelect').value,
    feasibility: document.getElementById('feasibilitySelect').value,
    category: document.getElementById('categorySelect').value,
    engine: document.getElementById('engineSelect').value,
    content: document.getElementById('contentSelect').value,
    languages: getActivePills('language'),
    licenses: getActivePills('license'),
    dependencies: getActivePills('dependency'),
    sort: currentSort
  };
  setCookie('suggestionFilters', JSON.stringify(filters));
}

// Load filters from cookies
function loadFiltersFromCookies() {
  const saved = getCookie('suggestionFilters');
  if (!saved) return;
  
  try {
    const filters = JSON.parse(saved);
    
    if (filters.status) document.getElementById('statusSelect').value = filters.status;
    if (filters.feasibility) document.getElementById('feasibilitySelect').value = filters.feasibility;
    if (filters.category) document.getElementById('categorySelect').value = filters.category;
    if (filters.engine) document.getElementById('engineSelect').value = filters.engine;
    if (filters.content) document.getElementById('contentSelect').value = filters.content;
    
    // Restore pill selections
    if (filters.languages) {
      filters.languages.forEach(lang => {
        const pill = document.querySelector(`.filter-pill[data-type="language"][data-value="${lang}"]`);
        if (pill) pill.classList.add('selected');
      });
    }
    
    if (filters.licenses) {
      filters.licenses.forEach(lic => {
        const pill = document.querySelector(`.filter-pill[data-type="license"][data-value="${lic}"]`);
        if (pill) pill.classList.add('selected');
      });
    }
    
    if (filters.dependencies) {
      filters.dependencies.forEach(dep => {
        const pill = document.querySelector(`.filter-pill[data-type="dependency"][data-value="${dep}"]`);
        if (pill) pill.classList.add('selected');
      });
    }
    
    if (filters.sort) {
      currentSort = filters.sort;
      updateSortUI();
    }
  } catch (e) {
    console.error('Error loading filters:', e);
  }
}

// Update sort UI
function updateSortUI() {
  document.querySelectorAll('.sort-option').forEach(option => {
    option.classList.toggle('selected', option.dataset.sort === currentSort);
  });
}

// Clear all filters
function clearAllFilters() {
  document.getElementById('statusSelect').value = '';
  document.getElementById('feasibilitySelect').value = '';
  document.getElementById('categorySelect').value = '';
  document.getElementById('engineSelect').value = '';
  document.getElementById('contentSelect').value = '';
  document.getElementById('searchInput').value = '';
  
  document.querySelectorAll('.filter-pill.selected').forEach(pill => {
    pill.classList.remove('selected');
  });
  
  saveFiltersToCookies();
  applySortAndFilters();
}

// Clear advanced filters
function clearAdvancedFilters() {
  document.querySelectorAll('.filter-pill.selected').forEach(pill => {
    pill.classList.remove('selected');
  });
  
  saveFiltersToCookies();
  applySortAndFilters();
}

// Toggle advanced filters
function toggleAdvancedFilters() {
  const content = document.getElementById('advancedFiltersContent');
  const arrow = document.getElementById('advancedArrow');
  content.classList.toggle('open');
  arrow.classList.toggle('open');
}

// UI Event Listeners
document.getElementById('searchInput').addEventListener('input', applySortAndFilters);
document.getElementById('statusSelect').addEventListener('change', () => {
  saveFiltersToCookies();
  applySortAndFilters();
});
document.getElementById('feasibilitySelect').addEventListener('change', () => {
  saveFiltersToCookies();
  applySortAndFilters();
});
document.getElementById('categorySelect').addEventListener('change', () => {
  saveFiltersToCookies();
  applySortAndFilters();
});
document.getElementById('engineSelect').addEventListener('change', () => {
  saveFiltersToCookies();
  applySortAndFilters();
});
document.getElementById('contentSelect').addEventListener('change', () => {
  saveFiltersToCookies();
  applySortAndFilters();
});

// Filter toggle
document.getElementById('filterToggleBtn').addEventListener('click', () => {
  document.getElementById('filterPanel').classList.toggle('open');
  document.getElementById('filterOverlay').classList.toggle('active');
  document.getElementById('filterToggleBtn').classList.toggle('active');
});

document.getElementById('closePanelBtn').addEventListener('click', () => {
  document.getElementById('filterPanel').classList.remove('open');
  document.getElementById('filterOverlay').classList.remove('active');
  document.getElementById('filterToggleBtn').classList.remove('active');
});

document.getElementById('filterOverlay').addEventListener('click', () => {
  document.getElementById('filterPanel').classList.remove('open');
  document.getElementById('filterOverlay').classList.remove('active');
  document.getElementById('filterToggleBtn').classList.remove('active');
});

// Sort toggle
document.getElementById('sortToggleBtn').addEventListener('click', (e) => {
  e.stopPropagation();
  document.getElementById('sortDropdown').classList.toggle('open');
});

document.addEventListener('click', (e) => {
  const sortDropdown = document.getElementById('sortDropdown');
  const sortBtn = document.getElementById('sortToggleBtn');
  if (!sortDropdown.contains(e.target) && !sortBtn.contains(e.target)) {
    sortDropdown.classList.remove('open');
  }
});

document.querySelectorAll('.sort-option').forEach(option => {
  option.addEventListener('click', () => {
    currentSort = option.dataset.sort;
    updateSortUI();
    saveFiltersToCookies();
    applySortAndFilters();
    document.getElementById('sortDropdown').classList.remove('open');
  });
});

// Back to top button
const backToTopBtn = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
  if (window.scrollY > 300) {
    backToTopBtn.classList.add('show');
  } else {
    backToTopBtn.classList.remove('show');
  }
});

backToTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Close modal on outside click
window.onclick = function(event) {
  const modal = document.getElementById('suggestionModal');
  if (event.target === modal) {
    closeModal();
  }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeCustomSelects();
  loadSuggestions();
});

// Initialize custom select dropdowns
function initializeCustomSelects() {
  const selects = document.querySelectorAll('.filter-dropdown');
  
  selects.forEach(select => {
    if (select.customWrapper) return; // Already initialized
    
    const wrapper = document.createElement('div');
    wrapper.className = 'custom-select-wrapper';
    select.parentNode.insertBefore(wrapper, select);
    wrapper.appendChild(select);
    
    const trigger = document.createElement('div');
    trigger.className = 'custom-select-trigger';
    if (select.disabled) trigger.classList.add('disabled');
    
    const triggerText = document.createElement('span');
    triggerText.textContent = select.options[select.selectedIndex].text;
    
    const arrow = document.createElement('div');
    arrow.className = 'custom-select-arrow';
    arrow.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>';
    
    trigger.appendChild(triggerText);
    trigger.appendChild(arrow);
    wrapper.appendChild(trigger);
    
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'custom-select-options';
    
    function updateOptions() {
      optionsContainer.innerHTML = '';
      Array.from(select.options).forEach((option, index) => {
        const customOption = document.createElement('div');
        customOption.className = 'custom-select-option';
        if (index === select.selectedIndex) customOption.classList.add('selected');
        customOption.textContent = option.text;
        customOption.addEventListener('click', () => {
          select.selectedIndex = index;
          select.dispatchEvent(new Event('change'));
          triggerText.textContent = option.text;
          wrapper.classList.remove('open');
          optionsContainer.querySelectorAll('.custom-select-option').forEach(o => o.classList.remove('selected'));
          customOption.classList.add('selected');
        });
        optionsContainer.appendChild(customOption);
      });
    }
    updateOptions();
    wrapper.appendChild(optionsContainer);
    
    trigger.addEventListener('click', () => {
      if (select.disabled) return;
      document.querySelectorAll('.custom-select-wrapper.open').forEach(w => {
        if (w !== wrapper) w.classList.remove('open');
      });
      wrapper.classList.toggle('open');
    });
    
    document.addEventListener('click', (e) => {
      if (!wrapper.contains(e.target)) {
        wrapper.classList.remove('open');
      }
    });
    
    select.customWrapper = wrapper;
    select.customTrigger = triggerText;
    select.updateCustomOptions = updateOptions;
  });
}
</script>