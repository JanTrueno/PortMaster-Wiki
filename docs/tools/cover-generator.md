---
title: Cover Generator - PortMaster Wiki

# Nothing here for glightbox to wrap at build time - the slot previews and
# the generated cover are all injected into <img>/<canvas> client-side,
# after a visitor picks or drops a file. Same reasoning as games.md/port.md.
glightbox: false
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

# Cover Generator

Build a mixv1 style cover for EmulationStation, in your browser.

Port packages usually include a `cover.png` that shows up in EmulationStation
and other frontends. This tool builds one for you, using the same mixv1
layout as [EmulationStation-ImageMaker](https://github.com/JanTrueno/EmulationStation-ImageMaker){:target="_blank" rel="noopener"}.


## Pick your images

Need artwork? [SteamGridDB](https://www.steamgriddb.com/){:target="_blank" rel="noopener"}
has screenshots, logos, and header images for most games.

<div class="porter-tool">
  <div class="im-slots">
    <div class="im-slot" data-slot="screenshot">
      <div class="im-slot-preview"><i class="bi bi-image"></i></div>
      <div class="im-slot-body">
        <label for="imScreenshot">Screenshot</label>
        <input type="file" id="imScreenshot" accept="image/*">
      </div>
    </div>

    <div class="im-slot" data-slot="logo">
      <div class="im-slot-preview"><i class="bi bi-badge-tm"></i></div>
      <div class="im-slot-body">
        <label for="imLogo">Logo</label>
        <input type="file" id="imLogo" accept="image/*">
      </div>
    </div>

    <div class="im-slot" data-slot="thumb">
      <div class="im-slot-preview"><i class="bi bi-card-image"></i></div>
      <div class="im-slot-body">
        <label for="imThumb">Thumb</label>
        <input type="file" id="imThumb" accept="image/*">
      </div>
    </div>
  </div>
</div>

## Generated cover

<div class="porter-tool">
  <div class="im-stage">
    <canvas id="imCanvas" width="640" height="480" aria-label="Generated cover preview"></canvas>
    <p class="im-empty" id="imEmpty">Pick a screenshot to get started.</p>
  </div>

  <div class="action-buttons">
    <button type="button" class="primary-btn" id="imDownload" disabled>
      <i class="bi bi-download"></i> Download PNG
    </button>
    <button type="button" class="secondary-btn" id="imReset">Start over</button>
  </div>
</div>

<script>
(function () {
  // ===================================================================
  // Browser port of imgmaker.py's mixv1 config. Every constant below is
  // straight out of config/mixv1.ini - keep them in step with that file:
  //
  //   canvas 640x480          screenshot 576x384 at (26,0), bezel 10, radius 10
  //   thumb  104x48 at (8,419)    logo scale 0.45, anchored bottom-right
  //   template 120x112 at (0,480) -> bounds-checked to (0,368)
  // ===================================================================
  const CANVAS_W = 640, CANVAS_H = 480;
  const SHOT_W = 576, SHOT_H = 384, SHOT_POS = [26, 0];
  const BEZEL = 10, RADIUS = 10;
  const THUMB_W = 104, THUMB_H = 48, THUMB_POS = [8, 419];
  const LOGO_SCALE = 0.45, LOGO_POS = [640, 480];
  const TPL_W = 120, TPL_H = 112, TPL_POS = [0, 480];
  const TEMPLATE_SRC = '../../assets/images/imagemaker/floppy.png';

  const SLOT_ICONS = {
    screenshot: 'bi-image',
    logo: 'bi-badge-tm',
    thumb: 'bi-card-image'
  };

  const canvas = document.getElementById('imCanvas');
  const ctx = canvas.getContext('2d');
  const emptyMsg = document.getElementById('imEmpty');
  const downloadBtn = document.getElementById('imDownload');
  const resetBtn = document.getElementById('imReset');

  const images = { screenshot: null, logo: null, thumb: null };
  let templateImage = null;

  const templateReady = loadImage(TEMPLATE_SRC)
    .then(img => { templateImage = img; })
    .catch(() => { templateImage = null; });

  function loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = src;
    });
  }

  // imgmaker.py's bounds_check: nudge a layer back inside the canvas rather
  // than letting it hang off the edge. The mixv1 config leans on this - the
  // logo and template are both positioned at the far corner (640,480) and
  // rely on being pulled back by their own size.
  function boundsCheck(pos, w, h) {
    let [x, y] = pos;
    if (x < 0) x = 0;
    if (y < 0) y = 0;
    if (x + w > CANVAS_W) x = CANVAS_W - w;
    if (y + h > CANVAS_H) y = CANVAS_H - h;
    return [x, y];
  }

  function scratch(w, h) {
    const c = document.createElement('canvas');
    c.width = w; c.height = h;
    const cx = c.getContext('2d');
    cx.imageSmoothingEnabled = true;
    cx.imageSmoothingQuality = 'high';
    return { c, cx };
  }

  // ===== Dominant colour =====
  // Stands in for Python's colorthief. Median cut over a 5-bit histogram -
  // the same family of algorithm - then the average of the most populous
  // box. Matches colorthief closely on real screenshots without pulling in
  // a library, though it won't always agree to the exact byte.
  function dominantColor(img) {
    const MAX = 200; // sampling cap; full resolution buys nothing here
    const scale = Math.min(1, MAX / Math.max(img.width, img.height));
    const w = Math.max(1, Math.round(img.width * scale));
    const h = Math.max(1, Math.round(img.height * scale));
    const { c, cx } = scratch(w, h);
    cx.drawImage(img, 0, 0, w, h);
    const data = cx.getImageData(0, 0, w, h).data;

    const pixels = [];
    for (let i = 0; i < data.length; i += 4) {
      const a = data[i + 3];
      // colorthief skips transparent pixels and near-white ones, so that a
      // white background doesn't become "the" colour of the image.
      if (a < 125) continue;
      const r = data[i], g = data[i + 1], b = data[i + 2];
      if (r > 250 && g > 250 && b > 250) continue;
      pixels.push([r, g, b]);
    }
    if (!pixels.length) return [128, 128, 128];

    let boxes = [pixels];
    while (boxes.length < 5) {
      boxes.sort((a, b) => b.length - a.length);
      const box = boxes.shift();
      if (!box || box.length < 2) { if (box) boxes.push(box); break; }

      // Split along whichever channel has the widest spread.
      const mins = [255, 255, 255], maxs = [0, 0, 0];
      for (const p of box) {
        for (let ch = 0; ch < 3; ch++) {
          if (p[ch] < mins[ch]) mins[ch] = p[ch];
          if (p[ch] > maxs[ch]) maxs[ch] = p[ch];
        }
      }
      let ch = 0, best = -1;
      for (let i = 0; i < 3; i++) {
        const range = maxs[i] - mins[i];
        if (range > best) { best = range; ch = i; }
      }
      if (best === 0) { boxes.push(box); break; }

      box.sort((a, b) => a[ch] - b[ch]);
      const mid = box.length >> 1;
      boxes.push(box.slice(0, mid), box.slice(mid));
    }

    boxes.sort((a, b) => b.length - a.length);
    const winner = boxes[0];
    let r = 0, g = 0, b = 0;
    for (const p of winner) { r += p[0]; g += p[1]; b += p[2]; }
    return [
      Math.round(r / winner.length),
      Math.round(g / winner.length),
      Math.round(b / winner.length)
    ];
  }

  // ===== Bezel =====
  // create_3d_bezel(): ten 1px rounded outlines stepping from the dominant
  // colour to transparent, blurred, with the screenshot laid on top.
  function buildBezel(shot, colour) {
    const w = SHOT_W + 2 * BEZEL;
    const h = SHOT_H + 2 * BEZEL;
    const { c, cx } = scratch(w, h);

    cx.filter = 'blur(2px)'; // PIL's GaussianBlur(radius=2)
    cx.lineWidth = 1;
    for (let i = 0; i < BEZEL; i++) {
      const t = 1 - i / BEZEL;
      cx.strokeStyle = `rgba(${Math.round(colour[0] * t)},${Math.round(colour[1] * t)},${Math.round(colour[2] * t)},${t})`;
      cx.beginPath();
      // +0.5 keeps a 1px stroke on the pixel grid instead of straddling two.
      cx.roundRect(i + 0.5, i + 0.5, w - 2 * i - 1, h - 2 * i - 1, RADIUS);
      cx.stroke();
    }

    cx.filter = 'none';
    cx.drawImage(shot, 0, 0, shot.width, shot.height, BEZEL, BEZEL, SHOT_W, SHOT_H);
    return c;
  }

  function render() {
    ctx.clearRect(0, 0, CANVAS_W, CANVAS_H);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';

    const hasAny = images.screenshot || images.logo || images.thumb;
    emptyMsg.style.display = hasAny ? 'none' : '';
    // display, not visibility: a hidden-but-laid-out canvas would still
    // reserve its 640x480 box and push the placeholder off to one side.
    canvas.style.display = hasAny ? '' : 'none';
    downloadBtn.disabled = !hasAny;
    if (!hasAny) return;

    // Paste order matches imgmaker.py: screenshot, logo, thumb, template.
    if (images.screenshot) {
      const bezel = buildBezel(images.screenshot, dominantColor(images.screenshot));
      const [x, y] = boundsCheck(SHOT_POS, bezel.width, bezel.height);
      ctx.drawImage(bezel, x, y);
    }

    if (images.logo) {
      // Math.floor, not round: imgmaker.py uses int(), which truncates.
      // Rounding lands a pixel off for most aspect ratios and shifts the
      // logo, since it's anchored to the bottom-right by its own size.
      const aspect = images.logo.width / images.logo.height;
      let lw = Math.floor(CANVAS_W * LOGO_SCALE);
      let lh = Math.floor(lw / aspect);
      if (lh > CANVAS_H) { lh = CANVAS_H; lw = Math.floor(lh * aspect); }
      const [x, y] = boundsCheck(LOGO_POS, lw, lh);
      ctx.drawImage(images.logo, x, y, lw, lh);
    }

    if (images.thumb) {
      const [x, y] = boundsCheck(THUMB_POS, THUMB_W, THUMB_H);
      ctx.drawImage(images.thumb, x, y, THUMB_W, THUMB_H);
    }

    // always_on = false in mixv1.ini: no thumb means no floppy, otherwise
    // you get an empty disk label.
    if (templateImage && images.thumb) {
      const [x, y] = boundsCheck(TPL_POS, TPL_W, TPL_H);
      ctx.drawImage(templateImage, x, y, TPL_W, TPL_H);
    }
  }

  // ===== Slots: click, native picker, or drag-and-drop onto the card =====
  function handleFile(key, slot, file) {
    if (!file || !file.type || !file.type.startsWith('image/')) {
      slot.classList.remove('is-filled');
      slot.querySelector('.im-slot-preview').innerHTML = '<i class="bi bi-exclamation-triangle"></i>';
      return;
    }

    const preview = slot.querySelector('.im-slot-preview');
    const url = URL.createObjectURL(file);
    loadImage(url).then(img => {
      images[key] = img;
      preview.innerHTML = '';
      const thumb = new Image();
      thumb.src = url;
      thumb.alt = '';
      preview.appendChild(thumb);
      slot.classList.add('is-filled');
      return templateReady;
    }).then(render).catch(() => {
      slot.classList.remove('is-filled');
      preview.innerHTML = '<i class="bi bi-exclamation-triangle"></i>';
    });
  }

  function wireSlot(inputId, key) {
    const input = document.getElementById(inputId);
    const slot = input.closest('.im-slot');

    input.addEventListener('change', () => {
      handleFile(key, slot, input.files && input.files[0]);
    });

    // Whole-card picker: clicking anywhere else on the card opens the same
    // dialog the native input/label already open on their own - skip those
    // two so the click isn't handled twice (one native, one synthetic).
    slot.addEventListener('click', (e) => {
      if (e.target === input || e.target.closest('label[for]')) return;
      input.click();
    });

    ['dragenter', 'dragover'].forEach(evt => slot.addEventListener(evt, (e) => {
      e.preventDefault(); // required or the browser rejects the drop outright
      slot.classList.add('is-dragover');
    }));

    slot.addEventListener('dragleave', (e) => {
      // Fires when the pointer crosses onto a child element too (e.g. from
      // the card padding onto the preview box), not just when it truly
      // leaves the card - only clear the highlight once it's actually gone.
      if (slot.contains(e.relatedTarget)) return;
      slot.classList.remove('is-dragover');
    });

    slot.addEventListener('drop', (e) => {
      e.preventDefault();
      slot.classList.remove('is-dragover');
      const file = e.dataTransfer.files && e.dataTransfer.files[0];
      if (!file) return;
      // Syncs the native input too, so its "Choose File" caption reflects
      // a dropped file the same way it would a manually picked one.
      input.files = e.dataTransfer.files;
      handleFile(key, slot, file);
    });
  }

  wireSlot('imScreenshot', 'screenshot');
  wireSlot('imLogo', 'logo');
  wireSlot('imThumb', 'thumb');

  downloadBtn.addEventListener('click', () => {
    canvas.toBlob(blob => {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      // EmulationStation looks for this exact filename inside a port
      // folder, so the download always saves as cover.png rather than
      // being named after whichever source image was picked.
      a.download = 'cover.png';
      a.click();
      // Revoking immediately can cancel the download in some browsers.
      setTimeout(() => URL.revokeObjectURL(a.href), 10000);
    }, 'image/png');
  });

  resetBtn.addEventListener('click', () => {
    Object.keys(images).forEach(k => { images[k] = null; });
    document.querySelectorAll('.im-slot').forEach(slot => {
      slot.classList.remove('is-filled', 'is-dragover');
      const input = slot.querySelector('input[type="file"]');
      input.value = '';
      slot.querySelector('.im-slot-preview').innerHTML = `<i class="bi ${SLOT_ICONS[slot.dataset.slot]}"></i>`;
    });
    render();
  });

  render();
})();
</script>
