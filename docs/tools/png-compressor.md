---
title: PNG Compressor - PortMaster Wiki

# Nothing here for glightbox to wrap at build time - the comparison images
# are both injected client-side, after a visitor picks or drops a file.
# Same reasoning as games.md/cover-generator.md.
glightbox: false
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

# PNG Compressor

Shrink a `screenshot.png` or `cover.png` without leaving your browser.

A screenshot straight out of a capture tool is usually a 24 or 32 bit PNG, which
stores a full colour value for every pixel. Cutting it down to a palette of at
most 256 colours typically saves 70-90% with no visible difference, which is what
[pngquant](https://pngquant.org/){:target="_blank" rel="noopener"} is for.

This page is not pngquant - it is the same approach written in JavaScript, so
nothing is uploaded and nothing has to be installed. Median cut picks the
palette, a couple of Lloyd passes tighten it up, Floyd-Steinberg dithering hides
the banding, and the result is written out as a palette PNG. Expect results in
the same range as pngquant, give or take a few percent.

## Pick your PNG

<div class="porter-tool">
  <div class="pq-setup">
    <div class="im-slot" data-slot="source">
      <div class="im-slot-preview"><i class="bi bi-file-earmark-image"></i></div>
      <div class="im-slot-body">
        <label for="pqSource">Image</label>
        <input type="file" id="pqSource" accept="image/*">
        <p class="help-text">Drop an image on this card, click it to browse, or paste one from your clipboard.</p>
      </div>
    </div>

    <div class="pq-controls">
      <div class="form-group">
        <label for="pqQuality">Quality <span class="pq-value" id="pqQualityValue">80</span></label>
        <input type="range" id="pqQuality" min="10" max="100" step="1" value="80">
        <p class="help-text" id="pqQualityNote">Fewer colours means a smaller file and, past a point, visible banding.</p>
      </div>

      <div class="form-group">
        <label class="filter-checkbox-item pq-dither">
          <input type="checkbox" id="pqDither" checked>
          <span>Dither</span>
        </label>
        <p class="help-text">Trades a little noise for smoother gradients. Worth turning off for pixel art, where it only makes the file bigger.</p>
      </div>
    </div>
  </div>
</div>

## Before and after

<div class="porter-tool">
  <div class="pq-result" id="pqResult" hidden>
    <div class="pq-compare" id="pqCompare">
      <img id="pqAfterImg" alt="Compressed image">
      <div class="pq-compare-overlay" id="pqOverlay">
        <img id="pqBeforeImg" alt="Original image">
      </div>
      <span class="pq-tag pq-tag-left">Original</span>
      <span class="pq-tag pq-tag-right">Compressed</span>
      <div class="pq-compare-handle" id="pqHandle" role="slider" tabindex="0"
           aria-label="Reveal more of the original or the compressed image"
           aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"></div>
    </div>

    <div class="pq-sizes" id="pqSizes"></div>
  </div>

  <p class="im-empty" id="pqEmpty">Pick an image to get started.</p>

  <div class="action-buttons">
    <button type="button" class="primary-btn" id="pqDownload" disabled>
      <i class="bi bi-download"></i> Download PNG
    </button>
    <button type="button" class="secondary-btn" id="pqReset">Start over</button>
  </div>
</div>

<script>
(function () {
  const MAX_COLORS = 256;

  const input = document.getElementById('pqSource');
  const slot = input.closest('.im-slot');
  const preview = slot.querySelector('.im-slot-preview');
  const quality = document.getElementById('pqQuality');
  const qualityValue = document.getElementById('pqQualityValue');
  const qualityNote = document.getElementById('pqQualityNote');
  const dither = document.getElementById('pqDither');
  const result = document.getElementById('pqResult');
  const emptyMsg = document.getElementById('pqEmpty');
  const beforeImg = document.getElementById('pqBeforeImg');
  const afterImg = document.getElementById('pqAfterImg');
  const compare = document.getElementById('pqCompare');
  const overlay = document.getElementById('pqOverlay');
  const handle = document.getElementById('pqHandle');
  const sizes = document.getElementById('pqSizes');
  const downloadBtn = document.getElementById('pqDownload');
  const resetBtn = document.getElementById('pqReset');

  let sourceName = 'screenshot.png';
  let sourceBytes = 0;      // the file as it arrived, for the "before" figure
  let sourceUrl = null;
  let pixels = null;        // ImageData of the decoded source
  let colours = null;       // unique source colours, built once per image
  let resultUrl = null;
  let resultBlob = null;
  let runId = 0;            // guards against a slow run overwriting a newer one
  let debounce = null;

  // ===================================================================
  // Quantiser
  // ===================================================================

  // The slider is a quality number because that's what pngquant calls it,
  // but what it actually buys you is palette slots. Curved so the top of
  // the range stays near-lossless and the bottom is where both the real
  // savings and the visible banding live.
  function paletteSizeFor(q) {
    const t = q / 100;
    return Math.max(2, Math.min(MAX_COLORS, Math.round(2 + Math.pow(t, 2.2) * (MAX_COLORS - 2))));
  }

  // Both the palette search and the Lloyd passes are linear in the number
  // of distinct colours, and anything with a gradient or a bit of grain in
  // it carries hundreds of thousands. Past this many buckets they get
  // merged down, which costs a pass over the buckets rather than over the
  // pixels.
  const MAX_BUCKETS = 1 << 15;

  // One pass over the pixels, done once when an image is loaded rather than
  // on every slider nudge - median cut runs over these buckets, not over
  // the raw pixels, so changing quality only costs a re-quantise.
  function buildColours(data) {
    const counts = new Map();
    for (let i = 0; i < data.length; i += 4) {
      const a = data[i + 3];
      // Fully transparent pixels collapse into one bucket: their RGB is
      // invisible, so letting it vary would burn palette slots on colours
      // nobody can see.
      const key = a === 0 ? 0 : ((data[i] << 24 | data[i + 1] << 16 | data[i + 2] << 8 | a) >>> 0);
      counts.set(key, (counts.get(key) || 0) + 1);
    }

    const exact = new Array(counts.size);
    let n = 0;
    for (const [key, count] of counts) {
      exact[n++] = key === 0
        ? { r: 0, g: 0, b: 0, a: 0, count }
        : { r: key >>> 24, g: (key >>> 16) & 255, b: (key >>> 8) & 255, a: key & 255, count };
    }

    let merged = exact;
    for (let shift = 1; shift <= 4 && merged.length > MAX_BUCKETS; shift++) {
      merged = mergeColours(exact, shift);
    }
    return merged;
  }

  // Re-key the buckets with the low bits dropped and add their sums up.
  // Each merged bucket still reports the mean of the real colours inside
  // it, so the palette is built from true averages - only the grouping is
  // coarser, never the values.
  function mergeColours(entries, shift) {
    const mask = (255 >> shift) << shift;
    const groups = new Map();
    for (const e of entries) {
      const key = e.a === 0 ? 0 :
        ((((e.r & mask) << 24) | ((e.g & mask) << 16) | ((e.b & mask) << 8) | (e.a & mask)) >>> 0);
      let g = groups.get(key);
      if (g === undefined) { g = { r: 0, g: 0, b: 0, a: 0, count: 0 }; groups.set(key, g); }
      g.r += e.r * e.count; g.g += e.g * e.count;
      g.b += e.b * e.count; g.a += e.a * e.count; g.count += e.count;
    }

    const out = new Array(groups.size);
    let n = 0;
    for (const g of groups.values()) {
      out[n++] = { r: g.r / g.count, g: g.g / g.count, b: g.b / g.count, a: g.a / g.count, count: g.count };
    }
    return out;
  }

  function boxOf(entries) {
    let weight = 0;
    const mins = [255, 255, 255, 255], maxs = [0, 0, 0, 0];
    for (const e of entries) {
      weight += e.count;
      const v = [e.r, e.g, e.b, e.a];
      for (let c = 0; c < 4; c++) {
        if (v[c] < mins[c]) mins[c] = v[c];
        if (v[c] > maxs[c]) maxs[c] = v[c];
      }
    }
    let channel = 0, range = -1;
    for (let c = 0; c < 4; c++) {
      if (maxs[c] - mins[c] > range) { range = maxs[c] - mins[c]; channel = c; }
    }
    return { entries, weight, channel, range };
  }

  // Median cut: repeatedly split the box that is costing the most, along
  // whichever channel it covers the widest. Ranked by pixels x spread
  // rather than pixels alone, so a big flat area of one colour doesn't
  // soak up the whole palette.
  function medianCut(entries, maxColours) {
    const boxes = [boxOf(entries)];

    while (boxes.length < maxColours) {
      let pick = -1, best = 0;
      for (let i = 0; i < boxes.length; i++) {
        const b = boxes[i];
        if (b.entries.length < 2 || b.range === 0) continue;
        const score = b.weight * b.range;
        if (score > best) { best = score; pick = i; }
      }
      if (pick < 0) break;

      const box = boxes[pick];
      const key = ['r', 'g', 'b', 'a'][box.channel];
      const sorted = box.entries.slice().sort((x, y) => x[key] - y[key]);

      // Split at the weighted median, not the midpoint of the list: a few
      // very common colours should not be outvoted by a long tail of ones
      // that show up in a handful of pixels each.
      const half = box.weight / 2;
      let acc = 0, cut = 1;
      for (let i = 0; i < sorted.length; i++) {
        acc += sorted[i].count;
        if (acc >= half) { cut = i + 1; break; }
      }
      // Both halves have to come away with something. Letting the cut land
      // on either end hands back a box identical to the one being split
      // plus an empty one, which is not a split at all - it just repeats
      // until the palette is full of entries averaged over no colours.
      if (cut < 1) cut = 1;
      if (cut > sorted.length - 1) cut = sorted.length - 1;

      boxes.splice(pick, 1, boxOf(sorted.slice(0, cut)), boxOf(sorted.slice(cut)));
    }

    return boxes.map(box => {
      let r = 0, g = 0, b = 0, a = 0, w = 0;
      for (const e of box.entries) {
        r += e.r * e.count; g += e.g * e.count;
        b += e.b * e.count; a += e.a * e.count; w += e.count;
      }
      return [Math.round(r / w), Math.round(g / w), Math.round(b / w), Math.round(a / w)];
    });
  }

  // Two Lloyd passes over the colour buckets. Median cut alone lands the
  // palette entries at box averages, which is close but not the best set;
  // reassigning and re-averaging tightens them up for a few ms.
  function refine(palette, entries) {
    for (let pass = 0; pass < 2; pass++) {
      const index = buildIndex(palette);
      const sums = new Float64Array(palette.length * 5);
      for (const e of entries) {
        const idx = nearest(palette, index, e.r, e.g, e.b, e.a);
        const o = idx * 5;
        sums[o] += e.r * e.count; sums[o + 1] += e.g * e.count;
        sums[o + 2] += e.b * e.count; sums[o + 3] += e.a * e.count;
        sums[o + 4] += e.count;
      }
      for (let i = 0; i < palette.length; i++) {
        const o = i * 5, w = sums[o + 4];
        if (!w) continue; // an entry nothing mapped to - leave it where it is
        palette[i] = [
          Math.round(sums[o] / w), Math.round(sums[o + 1] / w),
          Math.round(sums[o + 2] / w), Math.round(sums[o + 3] / w)
        ];
      }
    }
    return palette;
  }

  // Palette entries ordered by green, which is the channel the eye weighs
  // most, so a search can start next to the query and walk outwards.
  function buildIndex(palette) {
    const order = palette.map((_, i) => i).sort((a, b) => palette[a][1] - palette[b][1]);
    const greens = new Float64Array(order.length);
    for (let i = 0; i < order.length; i++) greens[i] = palette[order[i]][1];
    return { order, greens };
  }

  // Still an exact nearest neighbour - a side is only abandoned once its
  // green difference alone beats the best distance so far, and every entry
  // further out on that side is further still in green. It just gets there
  // after a handful of comparisons instead of all 256, which is the whole
  // cost of remapping a few million pixels.
  function nearest(palette, index, r, g, b, a) {
    const order = index.order, greens = index.greens, n = order.length;

    let lo = 0, hi = n;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (greens[mid] < g) lo = mid + 1; else hi = mid;
    }

    let best = order[0], bestD = Infinity;
    let left = lo - 1, right = lo;
    while (left >= 0 || right < n) {
      let takeRight;
      if (left < 0) takeRight = true;
      else if (right >= n) takeRight = false;
      else takeRight = (greens[right] - g) < (g - greens[left]);

      const at = takeRight ? right++ : left--;
      const dg = greens[at] - g;
      if (dg * dg >= bestD) {
        if (takeRight) right = n; else left = -1;
        continue;
      }

      const p = palette[order[at]];
      const dr = r - p[0], db = b - p[2], da = a - p[3];
      const d = dr * dr + dg * dg + db * db + da * da;
      if (d < bestD) { bestD = d; best = order[at]; if (d === 0) break; }
    }
    return best;
  }

  // Map every pixel to a palette index, optionally diffusing the error.
  // The cache is keyed on the exact colour asked for, which pays off on
  // game art: large flat runs ask the same question over and over.
  function remap(data, width, height, palette, useDither) {
    const indices = new Uint8Array(width * height);
    const index = buildIndex(palette);
    const cache = new Map();

    const lookup = (r, g, b, a) => {
      const key = (r << 24 | g << 16 | b << 8 | a) >>> 0;
      let idx = cache.get(key);
      if (idx === undefined) {
        idx = nearest(palette, index, r, g, b, a);
        // Bounded so a photographic source with millions of distinct
        // error-adjusted colours can't grow the cache without limit.
        if (cache.size < 1 << 17) cache.set(key, idx);
      }
      return idx;
    };

    if (!useDither) {
      for (let i = 0, p = 0; p < indices.length; p++, i += 4) {
        indices[p] = lookup(data[i], data[i + 1], data[i + 2], data[i + 3]);
      }
      return indices;
    }

    // Floyd-Steinberg over two running error rows, so only the current and
    // next scanline are ever held in float form.
    const w4 = width * 4;
    let curr = new Float32Array(w4 + 8);
    let next = new Float32Array(w4 + 8);

    for (let y = 0; y < height; y++) {
      const row = y * w4;
      for (let x = 0; x < width; x++) {
        const i = row + x * 4, e = x * 4;
        const r = clamp(data[i] + curr[e]);
        const g = clamp(data[i + 1] + curr[e + 1]);
        const b = clamp(data[i + 2] + curr[e + 2]);
        const a = clamp(data[i + 3] + curr[e + 3]);

        const idx = lookup(Math.round(r), Math.round(g), Math.round(b), Math.round(a));
        indices[y * width + x] = idx;

        const p = palette[idx];
        const er = r - p[0], eg = g - p[1], eb = b - p[2], ea = a - p[3];

        // 7/16 right, 3/16 down-left, 5/16 down, 1/16 down-right.
        if (x + 1 < width) spread(curr, e + 4, er, eg, eb, ea, 7 / 16);
        if (x > 0) spread(next, e - 4, er, eg, eb, ea, 3 / 16);
        spread(next, e, er, eg, eb, ea, 5 / 16);
        if (x + 1 < width) spread(next, e + 4, er, eg, eb, ea, 1 / 16);
      }
      const swap = curr;
      curr = next;
      next = swap;
      next.fill(0);
    }

    return indices;
  }

  function clamp(v) { return v < 0 ? 0 : v > 255 ? 255 : v; }

  function spread(buf, at, er, eg, eb, ea, f) {
    buf[at] += er * f; buf[at + 1] += eg * f;
    buf[at + 2] += eb * f; buf[at + 3] += ea * f;
  }

  // ===================================================================
  // Palette PNG writer
  // ===================================================================

  const CRC_TABLE = (() => {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      t[n] = c >>> 0;
    }
    return t;
  })();

  function crc32(bytes) {
    let c = 0xFFFFFFFF;
    for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 255] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }

  function chunk(type, body) {
    const out = new Uint8Array(12 + body.length);
    const view = new DataView(out.buffer);
    view.setUint32(0, body.length);
    for (let i = 0; i < 4; i++) out[4 + i] = type.charCodeAt(i);
    out.set(body, 8);
    view.setUint32(8 + body.length, crc32(out.subarray(4, 8 + body.length)));
    return out;
  }

  // CompressionStream('deflate') emits a zlib stream, which is exactly what
  // an IDAT payload is meant to be - no deflate implementation needed.
  async function deflate(bytes) {
    const stream = new Blob([bytes]).stream()
      .pipeThrough(new CompressionStream('deflate'));
    return new Uint8Array(await new Response(stream).arrayBuffer());
  }

  // Palette images don't have to spend a whole byte per pixel: a 16 colour
  // image packs four pixels into one, which is most of why the bottom of
  // the quality range drops off so sharply.
  function depthFor(count) {
    if (count <= 2) return 1;
    if (count <= 4) return 2;
    if (count <= 16) return 4;
    return 8;
  }

  async function encodePNG(width, height, indices, palette) {
    const depth = depthFor(palette.length);
    const perByte = 8 / depth;
    const rowBytes = Math.ceil(width / perByte);
    // Every scanline carries a leading filter byte. Palette indices aren't
    // numerically related to their neighbours, so filtering them is a loss -
    // libpng picks None for palette images too.
    const raw = new Uint8Array((rowBytes + 1) * height);

    for (let y = 0; y < height; y++) {
      const dst = y * (rowBytes + 1) + 1;
      const src = y * width;
      if (depth === 8) {
        raw.set(indices.subarray(src, src + width), dst);
      } else {
        for (let x = 0; x < width; x++) {
          const shift = 8 - depth - (x % perByte) * depth;
          raw[dst + ((x / perByte) | 0)] |= indices[src + x] << shift;
        }
      }
    }

    const ihdr = new Uint8Array(13);
    const iv = new DataView(ihdr.buffer);
    iv.setUint32(0, width);
    iv.setUint32(4, height);
    ihdr[8] = depth;
    ihdr[9] = 3; // colour type 3: indexed
    // 10, 11, 12 stay zero: deflate, adaptive filtering, no interlace.

    const plte = new Uint8Array(palette.length * 3);
    for (let i = 0; i < palette.length; i++) {
      plte[i * 3] = palette[i][0];
      plte[i * 3 + 1] = palette[i][1];
      plte[i * 3 + 2] = palette[i][2];
    }

    // tRNS only has to cover the palette up to the last see-through entry,
    // and the palette is sorted so those come first - an opaque image drops
    // the chunk entirely.
    let lastAlpha = -1;
    for (let i = 0; i < palette.length; i++) if (palette[i][3] < 255) lastAlpha = i;

    const parts = [
      new Uint8Array([137, 80, 78, 71, 13, 10, 26, 10]),
      chunk('IHDR', ihdr),
      chunk('PLTE', plte)
    ];
    if (lastAlpha >= 0) {
      const trns = new Uint8Array(lastAlpha + 1);
      for (let i = 0; i <= lastAlpha; i++) trns[i] = palette[i][3];
      parts.push(chunk('tRNS', trns));
    }
    parts.push(chunk('IDAT', await deflate(raw)));
    parts.push(chunk('IEND', new Uint8Array(0)));

    return new Blob(parts, { type: 'image/png' });
  }

  // ===================================================================
  // Wiring
  // ===================================================================

  function formatBytes(n) {
    if (n < 1024) return n + ' B';
    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + ' KB';
    return (n / (1024 * 1024)).toFixed(2) + ' MB';
  }

  function loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = src;
    });
  }

  function setBusy(on) {
    compare.classList.toggle('is-busy', on);
    downloadBtn.disabled = on || !resultBlob;
  }

  async function compress() {
    if (!pixels) return;
    const id = ++runId;
    setBusy(true);
    // Let the browser paint the busy state before the main thread goes away
    // for however long the quantiser takes.
    await new Promise(r => setTimeout(r, 0));
    if (id !== runId) return;

    const wanted = paletteSizeFor(Number(quality.value));
    const palette = refine(medianCut(colours, wanted), colours);
    // Transparent entries first so tRNS can stop early.
    palette.sort((a, b) => a[3] - b[3]);

    const indices = remap(pixels.data, pixels.width, pixels.height, palette, dither.checked);
    const blob = await encodePNG(pixels.width, pixels.height, indices, palette);
    if (id !== runId) return;

    if (resultUrl) URL.revokeObjectURL(resultUrl);
    resultBlob = blob;
    resultUrl = URL.createObjectURL(blob);
    afterImg.src = resultUrl;

    const delta = sourceBytes ? Math.round((1 - blob.size / sourceBytes) * 100) : 0;
    sizes.innerHTML =
      '<span class="pq-size"><strong>Original</strong> ' + formatBytes(sourceBytes) + '</span>' +
      '<span class="pq-size"><strong>Compressed</strong> ' + formatBytes(blob.size) + '</span>' +
      '<span class="pq-size pq-delta ' + (delta > 0 ? 'is-smaller' : 'is-bigger') + '">' +
      (delta > 0 ? delta + '% smaller' : Math.abs(delta) + '% bigger') + '</span>';

    qualityNote.textContent = palette.length + ' colour palette at ' +
      depthFor(palette.length) + ' bits per pixel.';

    setBusy(false);
  }

  function schedule() {
    clearTimeout(debounce);
    debounce = setTimeout(compress, 180);
  }

  async function handleFile(file) {
    if (!file || !file.type || !file.type.startsWith('image/')) {
      reset();
      preview.innerHTML = '<i class="bi bi-exclamation-triangle"></i>';
      return;
    }

    if (!window.CompressionStream) {
      preview.innerHTML = '<i class="bi bi-exclamation-triangle"></i>';
      sizes.textContent = 'This browser has no CompressionStream, which this page needs to write the PNG.';
      result.hidden = false;
      return;
    }

    if (sourceUrl) URL.revokeObjectURL(sourceUrl);
    sourceUrl = URL.createObjectURL(file);
    sourceBytes = file.size;
    sourceName = file.name && /\.png$/i.test(file.name) ? file.name : 'screenshot.png';

    try {
      const img = await loadImage(sourceUrl);
      const canvas = document.createElement('canvas');
      canvas.width = img.width;
      canvas.height = img.height;
      const ctx = canvas.getContext('2d', { willReadFrequently: true });
      ctx.drawImage(img, 0, 0);
      pixels = ctx.getImageData(0, 0, img.width, img.height);
      colours = buildColours(pixels.data);

      preview.innerHTML = '';
      const thumb = new Image();
      thumb.src = sourceUrl;
      thumb.alt = '';
      preview.appendChild(thumb);
      slot.classList.add('is-filled');

      beforeImg.src = sourceUrl;
      // Locks the box to the source's shape so the two layers stay aligned
      // while the compressed image is still being written.
      compare.style.aspectRatio = img.width + ' / ' + img.height;
      result.hidden = false;
      emptyMsg.style.display = 'none';
      setPosition(50);
      await compress();
    } catch (e) {
      reset();
      preview.innerHTML = '<i class="bi bi-exclamation-triangle"></i>';
    }
  }

  function reset() {
    runId++;
    pixels = null;
    colours = null;
    resultBlob = null;
    sourceBytes = 0;
    if (resultUrl) { URL.revokeObjectURL(resultUrl); resultUrl = null; }
    if (sourceUrl) { URL.revokeObjectURL(sourceUrl); sourceUrl = null; }
    input.value = '';
    slot.classList.remove('is-filled', 'is-dragover');
    preview.innerHTML = '<i class="bi bi-file-earmark-image"></i>';
    beforeImg.removeAttribute('src');
    afterImg.removeAttribute('src');
    sizes.textContent = '';
    result.hidden = true;
    emptyMsg.style.display = '';
    downloadBtn.disabled = true;
    compare.classList.remove('is-busy');
    qualityNote.textContent = 'Fewer colours means a smaller file and, past a point, visible banding.';
  }

  // ===== Comparison slider =====
  function setPosition(pct) {
    const clamped = Math.max(0, Math.min(100, pct));
    compare.style.setProperty('--pq-pos', clamped + '%');
    handle.setAttribute('aria-valuenow', Math.round(clamped));
  }

  function positionFromEvent(e) {
    const box = compare.getBoundingClientRect();
    setPosition(((e.clientX - box.left) / box.width) * 100);
  }

  // Pointer events rather than mouse+touch pairs: one code path covers a
  // mouse, a finger and a stylus, and capture keeps the drag alive when the
  // pointer leaves the box.
  compare.addEventListener('pointerdown', (e) => {
    if (result.hidden) return;
    compare.setPointerCapture(e.pointerId);
    compare.classList.add('is-dragging');
    positionFromEvent(e);
  });

  compare.addEventListener('pointermove', (e) => {
    if (!compare.hasPointerCapture(e.pointerId)) return;
    positionFromEvent(e);
  });

  ['pointerup', 'pointercancel'].forEach(evt => compare.addEventListener(evt, (e) => {
    compare.releasePointerCapture(e.pointerId);
    compare.classList.remove('is-dragging');
  }));

  handle.addEventListener('keydown', (e) => {
    const step = e.shiftKey ? 10 : 2;
    const now = Number(handle.getAttribute('aria-valuenow'));
    if (e.key === 'ArrowLeft') setPosition(now - step);
    else if (e.key === 'ArrowRight') setPosition(now + step);
    else if (e.key === 'Home') setPosition(0);
    else if (e.key === 'End') setPosition(100);
    else return;
    e.preventDefault();
  });

  // ===== Slot: click, native picker, drag-and-drop or paste =====
  input.addEventListener('change', () => {
    handleFile(input.files && input.files[0]);
  });

  slot.addEventListener('click', (e) => {
    if (e.target === input || e.target.closest('label[for]')) return;
    input.click();
  });

  ['dragenter', 'dragover'].forEach(evt => slot.addEventListener(evt, (e) => {
    e.preventDefault(); // required or the browser rejects the drop outright
    slot.classList.add('is-dragover');
  }));

  slot.addEventListener('dragleave', (e) => {
    if (slot.contains(e.relatedTarget)) return;
    slot.classList.remove('is-dragover');
  });

  slot.addEventListener('drop', (e) => {
    e.preventDefault();
    slot.classList.remove('is-dragover');
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    if (!file) return;
    input.files = e.dataTransfer.files;
    handleFile(file);
  });

  document.addEventListener('paste', (e) => {
    const items = e.clipboardData && e.clipboardData.items;
    if (!items) return;
    for (const item of items) {
      if (item.kind !== 'file' || !item.type.startsWith('image/')) continue;
      const file = item.getAsFile();
      if (!file) continue;
      e.preventDefault();
      input.value = '';
      handleFile(file);
      return;
    }
  });

  quality.addEventListener('input', () => {
    qualityValue.textContent = quality.value;
    schedule();
  });

  dither.addEventListener('change', schedule);

  downloadBtn.addEventListener('click', () => {
    if (!resultBlob) return;
    const a = document.createElement('a');
    a.href = URL.createObjectURL(resultBlob);
    a.download = sourceName;
    a.click();
    // Revoking immediately can cancel the download in some browsers.
    setTimeout(() => URL.revokeObjectURL(a.href), 10000);
  });

  resetBtn.addEventListener('click', () => {
    reset();
    quality.value = 80;
    qualityValue.textContent = '80';
    dither.checked = true;
  });

  setPosition(50);
})();
</script>
