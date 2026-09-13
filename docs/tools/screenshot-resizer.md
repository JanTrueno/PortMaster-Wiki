---
title: Screenshot Resizer - PortMaster Wiki

# Nothing here for glightbox to wrap at build time - the source preview and
# the resized output are both injected into <img>/<canvas> client-side,
# after a visitor picks or drops a file. Same reasoning as
# games.md/cover-generator.md.
glightbox: false
---

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

# Screenshot Resizer

Resize any image to a 640x480 `screenshot.png`, in your browser.

Every port needs a `screenshot.{jpg,png}` that is exactly 640x480, and submissions
are checked for it. Drop an image in below, pick how it should fill the frame, and
download the result. See the [packaging documentation](../contribute/porting/packaging.md)
for where to place the file.

Scaling uses a Lanczos filter in linear light rather than the browser's own, so
fine detail and dithered patterns survive the reduction instead of shimmering.
Exact 2x, 3x and 4x enlargements are done with nearest neighbour instead, which
keeps pixel art crisp.

The PNG this writes is a full 32 bit one. Run it through the
[PNG Compressor](png-compressor.md) afterwards to get the file size down.

## Pick your screenshot

<div class="porter-tool">
  <div class="rs-setup">
    <div class="im-slot" data-slot="source">
      <div class="im-slot-preview"><i class="bi bi-image"></i></div>
      <div class="im-slot-body">
        <label for="rsSource">Source image</label>
        <input type="file" id="rsSource" accept="image/*">
        <p class="help-text">Drop an image on this card, click it to browse, or paste one from your clipboard.</p>
      </div>
    </div>

    <div class="form-group">
      <label>How should it fill 640x480?</label>
      <div class="filter-radio-list">
        <label class="filter-checkbox-item">
          <input type="radio" name="rsMode" value="contain" checked>
          <span>Keep aspect: fit the whole image in and pad the gaps with black bars</span>
        </label>
        <label class="filter-checkbox-item">
          <input type="radio" name="rsMode" value="stretch">
          <span>Stretch: fill the frame exactly, distorting the image if the shape doesn't match</span>
        </label>
        <label class="filter-checkbox-item">
          <input type="radio" name="rsMode" value="crop">
          <span>Crop: scale up to fill the frame and trim the overflow off the edges</span>
        </label>
      </div>
      <p class="help-text">Cropping is centred, so it trims evenly from both sides (or top and bottom).</p>
    </div>
  </div>
</div>

## Resized screenshot

<div class="porter-tool">
  <div class="im-stage">
    <canvas id="rsCanvas" width="640" height="480" aria-label="Resized screenshot preview"></canvas>
    <p class="im-empty" id="rsEmpty">Pick an image to get started.</p>
  </div>
  <p class="rs-meta" id="rsMeta"></p>

  <div class="action-buttons">
    <button type="button" class="primary-btn" id="rsDownload" disabled>
      <i class="bi bi-download"></i> Download PNG
    </button>
    <button type="button" class="secondary-btn" id="rsReset">Start over</button>
  </div>
</div>

<script>
(function () {
  // Fixed by the packaging rules: a port's screenshot has to be exactly
  // 640x480, so the canvas size is the whole point of the tool and is never
  // derived from the source image.
  const OUT_W = 640, OUT_H = 480;
  const OUT_ASPECT = OUT_W / OUT_H;

  const canvas = document.getElementById('rsCanvas');
  const ctx = canvas.getContext('2d');
  const emptyMsg = document.getElementById('rsEmpty');
  const meta = document.getElementById('rsMeta');
  const downloadBtn = document.getElementById('rsDownload');
  const resetBtn = document.getElementById('rsReset');
  const input = document.getElementById('rsSource');
  const slot = input.closest('.im-slot');
  const preview = slot.querySelector('.im-slot-preview');

  let source = null;   // ImageData of the decoded source
  let mode = 'contain';

  // ===================================================================
  // Resampler
  //
  // drawImage is the browser's own scaler, and at anything past a 2:1
  // reduction it samples far too few source pixels - fine lines and the
  // dithered patterns retro games are full of come out shimmering. This is
  // a separable Lanczos-3 filter instead, which is what an image editor
  // would use, and it runs in linear light: averaging sRGB values directly
  // treats the encoding as if it were brightness, which darkens edges and
  // is where most "it looks off" resizes come from.
  // ===================================================================
  const LANCZOS_A = 3;

  const TO_LINEAR = new Float32Array(256);
  for (let i = 0; i < 256; i++) {
    const c = i / 255;
    TO_LINEAR[i] = c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  }

  // The encode back to sRGB is a pow() per channel per pixel otherwise.
  // 16384 steps is a finer grid than 8 bit output can represent, so the
  // table costs nothing in accuracy.
  const SRGB_STEPS = 16384;
  const TO_SRGB = new Uint8Array(SRGB_STEPS + 1);
  for (let i = 0; i <= SRGB_STEPS; i++) {
    const l = i / SRGB_STEPS;
    const c = l <= 0.0031308 ? l * 12.92 : 1.055 * Math.pow(l, 1 / 2.4) - 0.055;
    TO_SRGB[i] = Math.round(c * 255);
  }

  function encode(linear) {
    if (linear <= 0) return 0;
    if (linear >= 1) return 255;
    return TO_SRGB[(linear * SRGB_STEPS) | 0];
  }

  function lanczos(x) {
    if (x === 0) return 1;
    if (x <= -LANCZOS_A || x >= LANCZOS_A) return 0;
    const px = Math.PI * x;
    return (LANCZOS_A * Math.sin(px) * Math.sin(px / LANCZOS_A)) / (px * px);
  }

  // Per output pixel: which source pixels it reads and how much of each.
  // Computed once per axis and reused down every row or column.
  function weightsFor(srcStart, srcSize, dstSize) {
    const scale = dstSize / srcSize;
    // Shrinking has to widen the kernel in source space, or the filter
    // steps straight over source pixels without ever looking at them -
    // that gap is exactly what aliasing is.
    const filterScale = scale < 1 ? scale : 1;
    const support = LANCZOS_A / filterScale;

    const starts = new Int32Array(dstSize);
    const counts = new Int32Array(dstSize);
    const offsets = new Int32Array(dstSize);
    const weights = new Float32Array(dstSize * (Math.ceil(support) * 2 + 2));

    let at = 0;
    for (let i = 0; i < dstSize; i++) {
      const centre = srcStart + (i + 0.5) / scale;
      // Clamped to the region being read, then renormalised below, which
      // handles the edges without smearing a repeated border inwards.
      const lo = Math.max(srcStart, Math.floor(centre - support));
      const hi = Math.min(srcStart + srcSize - 1, Math.ceil(centre + support));

      let sum = 0;
      offsets[i] = at;
      starts[i] = lo;
      for (let x = lo; x <= hi; x++) {
        const w = lanczos((x + 0.5 - centre) * filterScale);
        weights[at++] = w;
        sum += w;
      }
      counts[i] = hi - lo + 1;
      if (sum !== 0) {
        for (let k = offsets[i]; k < at; k++) weights[k] /= sum;
      }
    }

    return { starts, counts, offsets, weights };
  }

  // Horizontal pass: source bytes in, premultiplied linear floats out.
  // Premultiplied because a transparent pixel's RGB is arbitrary, and
  // letting it into the average is what produces haloed edges.
  function passX(data, srcW, x0, y0, cropW, cropH, dstW) {
    const wx = weightsFor(x0, cropW, dstW);
    const out = new Float32Array(dstW * cropH * 4);

    for (let y = 0; y < cropH; y++) {
      const srcRow = (y0 + y) * srcW;
      const dstRow = y * dstW * 4;
      for (let i = 0; i < dstW; i++) {
        let r = 0, g = 0, b = 0, a = 0;
        const start = wx.starts[i], n = wx.counts[i], off = wx.offsets[i];
        for (let k = 0; k < n; k++) {
          const w = wx.weights[off + k];
          const p = (srcRow + start + k) * 4;
          const al = data[p + 3] / 255;
          const aw = al * w;
          r += TO_LINEAR[data[p]] * aw;
          g += TO_LINEAR[data[p + 1]] * aw;
          b += TO_LINEAR[data[p + 2]] * aw;
          a += aw;
        }
        const o = dstRow + i * 4;
        out[o] = r; out[o + 1] = g; out[o + 2] = b; out[o + 3] = a;
      }
    }
    return out;
  }

  // Vertical pass, straight into the output ImageData. The result is
  // composited over the black frame as it is written: with a black
  // background, "over black" is just the premultiplied value itself, so
  // there is nothing to undo and every output pixel ends up opaque.
  function passY(mid, dstW, srcH, dstH, out) {
    const wy = weightsFor(0, srcH, dstH);
    const px = out.data;

    for (let j = 0; j < dstH; j++) {
      const start = wy.starts[j], n = wy.counts[j], off = wy.offsets[j];
      for (let i = 0; i < dstW; i++) {
        let r = 0, g = 0, b = 0;
        for (let k = 0; k < n; k++) {
          const w = wy.weights[off + k];
          const p = ((start + k) * dstW + i) * 4;
          r += mid[p] * w; g += mid[p + 1] * w; b += mid[p + 2] * w;
        }
        const o = (j * dstW + i) * 4;
        px[o] = encode(r); px[o + 1] = encode(g); px[o + 2] = encode(b);
        px[o + 3] = 255;
      }
    }
  }

  // An exact 2x, 3x or 4x enlargement of pixel art should stay pixel art.
  // Any filter at all would blur edges that are meant to be hard, so these
  // ratios are replicated instead of resampled. 1x falls out of the same
  // path as a straight copy.
  function nearest(data, srcW, x0, y0, cropW, cropH, factor, out) {
    const px = out.data;
    const dstW = cropW * factor;
    for (let y = 0; y < cropH * factor; y++) {
      const srcRow = (y0 + ((y / factor) | 0)) * srcW;
      for (let x = 0; x < dstW; x++) {
        const p = (srcRow + x0 + ((x / factor) | 0)) * 4;
        const o = (y * dstW + x) * 4;
        const al = data[p + 3] / 255;
        // Same composite over black as the filtered path, so a source with
        // alpha lands identically either way.
        px[o] = Math.round(data[p] * al);
        px[o + 1] = Math.round(data[p + 1] * al);
        px[o + 2] = Math.round(data[p + 2] * al);
        px[o + 3] = 255;
      }
    }
  }

  function integerFactor(cropW, cropH, dw, dh) {
    if (dw % cropW || dh % cropH) return 0;
    const fx = dw / cropW, fy = dh / cropH;
    return (fx === fy && fx >= 1 && fx <= 4) ? fx : 0;
  }

  function resize(src, sx, sy, sw, sh, dw, dh) {
    const out = new ImageData(dw, dh);
    const factor = integerFactor(sw, sh, dw, dh);
    if (factor) {
      nearest(src.data, src.width, sx, sy, sw, sh, factor, out);
      return { image: out, filter: factor === 1 ? 'copied 1:1' : factor + 'x nearest neighbour' };
    }
    const mid = passX(src.data, src.width, sx, sy, sw, sh, dw);
    passY(mid, dw, sh, dh, out);
    return { image: out, filter: 'Lanczos 3' };
  }

  // ===================================================================
  // Modes
  // ===================================================================

  // Each mode is just a different pair of rectangles: which part of the
  // source to read, and where in the 640x480 frame to put it.
  function rects(img) {
    const sw = img.width, sh = img.height;

    if (mode === 'stretch') {
      return { src: [0, 0, sw, sh], dst: [0, 0, OUT_W, OUT_H] };
    }

    if (mode === 'crop') {
      // Widest centred rectangle of the source that is already 4:3, blown
      // up to the full frame - so the trim is exact rather than the result
      // of scaling and then guessing at an offset.
      let cw, ch;
      if (sw / sh > OUT_ASPECT) {
        ch = sh; cw = Math.round(sh * OUT_ASPECT);
      } else {
        cw = sw; ch = Math.round(sw / OUT_ASPECT);
      }
      return {
        src: [Math.round((sw - cw) / 2), Math.round((sh - ch) / 2), cw, ch],
        dst: [0, 0, OUT_W, OUT_H]
      };
    }

    // contain: scale to whichever axis runs out first, centre the rest.
    const scale = Math.min(OUT_W / sw, OUT_H / sh);
    const w = Math.max(1, Math.round(sw * scale));
    const h = Math.max(1, Math.round(sh * scale));
    return {
      src: [0, 0, sw, sh],
      dst: [Math.round((OUT_W - w) / 2), Math.round((OUT_H - h) / 2), w, h]
    };
  }

  function describe(img, r, filter) {
    const bits = [img.width + ' x ' + img.height + ' source'];
    if (mode === 'crop') {
      const trimmedX = img.width - r.src[2];
      const trimmedY = img.height - r.src[3];
      if (trimmedX) bits.push('trimmed ' + Math.round(trimmedX / 2) + 'px from each side');
      else if (trimmedY) bits.push('trimmed ' + Math.round(trimmedY / 2) + 'px from the top and bottom');
      else bits.push('nothing to trim, the source is already 4:3');
    } else if (mode === 'contain') {
      const barX = OUT_W - r.dst[2];
      const barY = OUT_H - r.dst[3];
      if (barX) bits.push(Math.round(barX / 2) + 'px black bars left and right');
      else if (barY) bits.push(Math.round(barY / 2) + 'px black bars top and bottom');
      else bits.push('no bars needed, the source is already 4:3');
    } else {
      const sa = img.width / img.height;
      bits.push(Math.abs(sa - OUT_ASPECT) < 0.005
        ? 'no distortion, the source is already 4:3'
        : (sa > OUT_ASPECT ? 'squeezed horizontally' : 'stretched horizontally'));
    }
    bits.push(filter);
    bits.push('output 640 x 480 PNG');
    return bits.join(' - ');
  }

  function render() {
    // display, not visibility: a hidden-but-laid-out canvas would still
    // reserve its 640x480 box and push the placeholder off to one side.
    emptyMsg.style.display = source ? 'none' : '';
    canvas.style.display = source ? '' : 'none';
    downloadBtn.disabled = !source;
    meta.textContent = '';
    if (!source) return;

    // Painted on every mode, not just the letterboxed one: a source with an
    // alpha channel would otherwise leave see-through patches in a file that
    // is meant to be a flat screenshot.
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, OUT_W, OUT_H);

    const r = rects(source);
    const [sx, sy, sw, sh] = r.src;
    const [dx, dy, dw, dh] = r.dst;
    const { image, filter } = resize(source, sx, sy, sw, sh, dw, dh);
    // putImageData replaces rather than blends, which is what we want: the
    // resampler already composited the source over black.
    ctx.putImageData(image, dx, dy);

    meta.textContent = describe(source, r, filter);
  }

  function loadImage(src) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = src;
    });
  }

  function handleFile(file) {
    if (!file || !file.type || !file.type.startsWith('image/')) {
      source = null;
      slot.classList.remove('is-filled');
      preview.innerHTML = '<i class="bi bi-exclamation-triangle"></i>';
      render();
      return;
    }

    const url = URL.createObjectURL(file);
    loadImage(url).then(img => {
      // Decoded once into pixels: the filter works on the source array
      // directly, and re-reading it on every mode change would be waste.
      const buf = document.createElement('canvas');
      buf.width = img.width;
      buf.height = img.height;
      const bx = buf.getContext('2d', { willReadFrequently: true });
      bx.drawImage(img, 0, 0);
      source = bx.getImageData(0, 0, img.width, img.height);

      preview.innerHTML = '';
      const thumb = new Image();
      thumb.src = url;
      thumb.alt = '';
      preview.appendChild(thumb);
      slot.classList.add('is-filled');
      render();
    }).catch(() => {
      source = null;
      slot.classList.remove('is-filled');
      preview.innerHTML = '<i class="bi bi-exclamation-triangle"></i>';
      render();
    });
  }

  input.addEventListener('change', () => {
    handleFile(input.files && input.files[0]);
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
    handleFile(file);
  });

  // Screenshots usually start life on the clipboard, so save people the
  // round trip through a file on disk. The file input can't be synced from
  // here - there's no FileList to assign - so its caption stays empty.
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

  document.querySelectorAll('input[name="rsMode"]').forEach(radio => {
    radio.addEventListener('change', () => {
      if (!radio.checked) return;
      mode = radio.value;
      render();
    });
  });

  downloadBtn.addEventListener('click', () => {
    canvas.toBlob(blob => {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      // PortMaster looks for this exact filename inside a port folder, so
      // the download always saves as screenshot.png rather than being named
      // after whichever image was dropped in.
      a.download = 'screenshot.png';
      a.click();
      // Revoking immediately can cancel the download in some browsers.
      setTimeout(() => URL.revokeObjectURL(a.href), 10000);
    }, 'image/png');
  });

  resetBtn.addEventListener('click', () => {
    source = null;
    input.value = '';
    slot.classList.remove('is-filled', 'is-dragover');
    preview.innerHTML = '<i class="bi bi-image"></i>';
    const first = document.querySelector('input[name="rsMode"][value="contain"]');
    if (first) first.checked = true;
    mode = 'contain';
    render();
  });

  render();
})();
</script>
