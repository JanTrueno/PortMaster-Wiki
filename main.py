import json
import markdown
import os
import random
import re
import time
from pathlib import Path
from datetime import datetime, timedelta
import urllib.request
import urllib.error

MARKDOWN_EXTENSIONS = ["tables", "fenced_code"]

# The current community challenge port, manually updated each month (also
# shown on the homepage). Kept as one shared constant so index.md and the
# games.md hero banner never drift out of sync with each other.
PORT_OF_THE_MONTH_KEY = "dragondragonfirefire.zip"

# Hero banner override: some ports are a near-duplicate of another slide
# already in the rotation (plain "2048" next to "2048 Plus" adds no
# variety), so they're excluded from hero candidacy entirely.
HERO_EXCLUDE_KEYS = {"2048.zip"}

# Set at the end of define_env(), read by on_post_build() to measure how
# long the actual mkdocs build phase (markdown->HTML, theme templating,
# search indexing) takes on top of define_env's own work.
_config_done_time = None

# FAST_BUILD=1 mkdocs build - skips the two slowest, data-only steps (the
# GitHub JSON downloads and the per-port markdown render into
# port_details.json) and reuses whatever's already on disk instead. Only
# useful for iterating on templates/CSS/JS, where port data hasn't
# changed - never use it for a build that's meant to ship, since it can
# silently serve stale port data.
FAST_BUILD = os.environ.get("FAST_BUILD") == "1"

# markdown.markdown() rebuilds the whole parser/extension pipeline from
# scratch on every call, which is wasteful when called thousands of times
# (desc + inst for every port). Reuse one Markdown instance instead and
# .reset() it between conversions.
_markdown_renderer = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)


def render_markdown_field(content):
    """Render a desc/inst markdown field to HTML at build time, so the
    standalone port page doesn't need to ship a markdown parser to the
    client just to show text that never changes without a rebuild."""
    content = (content or "").strip()
    if not content or content == "None":
        return ""
    # Some ports' desc_md/inst_md in the upstream ports.json mix real
    # newlines with literal backslash-n sequences (e.g. "Das Erbe"), which
    # Python-Markdown won't treat as line breaks. Normalize them to real
    # newlines first so lists/paragraphs render instead of showing "\n".
    content = content.replace("\\n", "\n")
    _markdown_renderer.reset()
    return _markdown_renderer.convert(content)

def download_github_json(url, local_path):
    """Download a JSON file from GitHub to local path"""
    try:
        print(f"Downloading {url}...", flush=True)
        with urllib.request.urlopen(url) as response:
            data = response.read()
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with local_path.open('wb') as f:
                f.write(data)
        print(f"✓ Downloaded to {local_path}", flush=True)
        return True
    except urllib.error.URLError as e:
        print(f"✗ Failed to download {url}: {e}", flush=True)
        return False

def download_portmaster_jsons(base_path):
    """Download all PortMaster JSON files from GitHub"""
    # Use latest releases
    github_release = "https://github.com/PortsMaster/PortMaster-New/releases/latest/download"
    github_mv_release = "https://github.com/PortsMaster-MV/PortMaster-MV-New/releases/latest/download"
    github_info = "https://raw.githubusercontent.com/PortsMaster/PortMaster-Info/refs/heads/main"

    files_to_download = {
        "ports.json": f"{github_release}/ports.json",
        "ports-MV.json": f"{github_mv_release}/ports.json",
        "port_stats.json": f"{github_info}/port_stats.json",
        "device_info.json": f"{github_info}/device_info.json",
        "porters.json": f"{github_info}/porters.json",
        "runtimes_zips.json": f"{github_release}/runtimes_zips.json",
        # featured_ports.json is NOT downloaded here anymore - it's now a
        # manually curated file (see docs/assets/json/featured_ports.json)
        # and re-downloading it on every build would overwrite that curation
        # with upstream's version.
    }

    success_count = 0
    for filename, url in files_to_download.items():
        local_path = base_path / filename
        if download_github_json(url, local_path):
            success_count += 1

    print(f"\nDownloaded {success_count}/{len(files_to_download)} files successfully", flush=True)
    return success_count > 0

MOSAIC_TILE_COUNT = 36
MOSAIC_CANDIDATE_LIMIT = 90


def _has_black_bars(image):
    """True if the image is letterboxed or pillarboxed.

    Samples the outer 10% of each edge and calls it a bar if nearly every
    sampled line there is essentially black. Checked as a pair (top AND
    bottom, or left AND right) so a game that's merely dark along one edge
    isn't mistaken for a bar.
    """
    image = image.convert("RGB")
    width, height = image.size
    band_h = max(1, height // 10)
    band_w = max(1, width // 10)

    def row_is_dark(y):
        step = max(1, width // 40)
        pixels = [image.getpixel((x, y)) for x in range(0, width, step)]
        return sum(sum(p) / 3 for p in pixels) / len(pixels) < 18

    def col_is_dark(x):
        step = max(1, height // 40)
        pixels = [image.getpixel((x, y)) for y in range(0, height, step)]
        return sum(sum(p) / 3 for p in pixels) / len(pixels) < 18

    top = sum(row_is_dark(y) for y in range(band_h))
    bottom = sum(row_is_dark(height - 1 - y) for y in range(band_h))
    left = sum(col_is_dark(x) for x in range(band_w))
    right = sum(col_is_dark(width - 1 - x) for x in range(band_w))

    letterboxed = top > band_h * 0.8 and bottom > band_h * 0.8
    pillarboxed = left > band_w * 0.8 and right > band_w * 0.8
    return letterboxed or pillarboxed


def build_mosaic_ports(base_path, port_details):
    """Pick screenshots for the homepage mosaic, skipping barred ones."""
    cache_path = base_path / "screenshot_bars.json"
    cache = {}
    if cache_path.exists():
        try:
            with cache_path.open(encoding="utf-8") as f:
                cache = json.load(f)
        except (json.JSONDecodeError, OSError):
            cache = {}

    try:
        import io
        from PIL import Image
    except ImportError:
        # No Pillow available - fall back to unfiltered, which is only a
        # cosmetic regression rather than a broken page.
        print("Pillow not available: mosaic screenshots won't be bar-filtered.", flush=True)
        Image = None

    candidates = sorted(
        ((pid, p) for pid, p in port_details.items() if p.get("screenshot")),
        key=lambda item: item[1].get("downloads", 0),
        reverse=True,
    )[:MOSAIC_CANDIDATE_LIMIT]

    chosen = []
    checked = 0
    for port_id, port in candidates:
        if len(chosen) >= MOSAIC_TILE_COUNT:
            break
        tile = {"id": port_id, "repo": port["repo"], "screenshot": port["screenshot"]}
        cache_key = f"{port_id}/{port['screenshot']}"

        if cache_key in cache:
            if not cache[cache_key]:
                chosen.append(tile)
            continue

        if Image is None or FAST_BUILD:
            chosen.append(tile)
            continue

        url = (
            f"https://raw.githubusercontent.com/{port['repo']}"
            f"/refs/heads/main/ports/{port_id}/{port['screenshot']}"
        )
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                image = Image.open(io.BytesIO(response.read()))
            barred = _has_black_bars(image)
            checked += 1
        except Exception:
            # Unreachable/undecodable - treat as usable rather than dropping
            # a port from the wall over a transient network blip.
            barred = False

        cache[cache_key] = barred
        if not barred:
            chosen.append(tile)

    if checked:
        print(f"Checked {checked} new screenshot(s) for black bars.", flush=True)
        try:
            with cache_path.open("w", encoding="utf-8") as f:
                json.dump(cache, f, indent=0, sort_keys=True)
        except OSError:
            pass

    return chosen


def define_env(env):
    base_path = Path(__file__).parent / "docs" / "assets" / "json"

    # Download JSONs from GitHub (comment out if you want to use local files only)
    if FAST_BUILD:
        print("FAST_BUILD=1: skipping GitHub JSON downloads, using local files as-is.", flush=True)
    else:
        download_portmaster_jsons(base_path)

    ports_files = [
        base_path / "ports.json",
        base_path / "ports-MV.json",
    ]
    merged_ports = {"ports": {}, "utils": {}}

    for path in ports_files:
        if not path.exists():
            continue
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
            # merge ports dict
            if "ports" in data:
                for key, value in data["ports"].items():
                    merged_ports["ports"][key] = value
            # merge utils dict
            if "utils" in data:
                for key, value in data["utils"].items():
                    merged_ports["utils"][key] = value

    env.variables["ports"] = merged_ports
    env.variables["port_of_the_month_key"] = PORT_OF_THE_MONTH_KEY

    # Build a lookup of description/instruction markdown text, keyed by port_id.
    # This is deliberately NOT embedded as HTML attributes on the card divs:
    # values can contain code fences, newlines, brackets and quotes, and
    # Python-Markdown's fenced-code preprocessor will mangle those if they sit
    # inside a raw HTML tag's attributes (it runs before/independently of raw
    # HTML block detection). Instead we ship one JSON blob in a <script> tag
    # and let JS look values up by port_id.
    port_text = {}
    for key, port in merged_ports["ports"].items():
        port_id = key.replace(".zip", "")
        attr = port.get("attr") or {}
        port_text[port_id] = {
            "desc": attr.get("desc") or "",
            "descMd": attr.get("desc_md") or "",
            "inst": attr.get("inst") or "",
            "instMd": attr.get("inst_md") or "",
        }

    # ensure_ascii keeps the output plain-ASCII (safe inside a <script> tag
    # regardless of the page's declared encoding), and escaping "</" prevents
    # a description containing the literal text "</script>" from closing the
    # tag early.
    ports_text_json = json.dumps(port_text, ensure_ascii=True).replace("</", "<\\/")
    env.variables["ports_text_json"] = ports_text_json

    # Add now() function for templates
    env.variables["now"] = datetime.now

    # Total port count for immediate display
    env.variables["total_port_count"] = len(merged_ports["ports"])

    # Build a runtime arch lookup: runtime_name -> [available archs]
    runtime_archs = {}
    for runtime_key, runtime_data in merged_ports.get("utils", {}).items():
        runtime_name = runtime_data.get("runtime_name", runtime_key)
        arch = runtime_data.get("runtime_arch", "")
        if runtime_name not in runtime_archs:
            runtime_archs[runtime_name] = []
        if arch and arch not in runtime_archs[runtime_name]:
            runtime_archs[runtime_name].append(arch)

    env.variables["runtime_archs"] = runtime_archs

    # Also ship it as a static file so the standalone port page can do the
    # same device-compatibility check as /all-games/ without re-embedding
    # this data inline on every single port page.
    with (base_path / "runtime_archs.json").open("w", encoding="utf-8") as f:
        json.dump(runtime_archs, f, ensure_ascii=True, separators=(",", ":"))

    # Load port stats (download counts)
    port_stats_path = base_path / "port_stats.json"
    port_stats = {"ports": {}, "total_downloads": 0}

    if port_stats_path.exists():
        with port_stats_path.open(encoding="utf-8") as f:
            port_stats = json.load(f)

    env.variables["port_stats"] = port_stats

    # Build a lean per-port data file for the standalone port page
    # (/port/#<id>). This intentionally ships far less than ports.json
    # (which is 2MB+ and includes fields like items/store/md5 that the page
    # never uses) so a port page load only needs one small, cacheable
    # fetch instead of pulling in the whole /all-games/ dataset. desc/inst
    # markdown is pre-rendered to HTML here too, so the client only needs a
    # markdown parser for the live-fetched README, not for this data.
    port_details_path = base_path / "port_details.json"

    if FAST_BUILD and port_details_path.exists():
        print(f"FAST_BUILD=1: reusing existing {port_details_path.name} as-is (skipping the per-port markdown render).", flush=True)
        with port_details_path.open(encoding="utf-8") as f:
            port_details = json.load(f)
    else:
        port_details = {}
        total_ports = len(merged_ports["ports"])
        print(f"Rendering port_details.json for {total_ports} ports (this involves a markdown render per port, and can take a couple of minutes)...", flush=True)
        for i, (key, port) in enumerate(merged_ports["ports"].items(), start=1):
            if i % 200 == 0 or i == total_ports:
                print(f"  ...{i}/{total_ports} ports rendered", flush=True)
            port_id = key.replace(".zip", "")
            attr = port.get("attr") or {}
            source = port.get("source") or {}
            source_url = source.get("url") or ""
            is_mv = "PortMaster-MV" in source_url or "MV-New" in source_url
            repo = "PortsMaster-MV/PortMaster-MV-New" if is_mv else "PortsMaster/PortMaster-New"

            def normalize_store_url(raw_url):
                # Some upstream ports.json entries have a bare "gameurl" with no
                # scheme (e.g. "store.epicgames.com/..."), which browsers treat
                # as a relative link on our own site instead of an absolute one.
                raw_url = raw_url.strip()
                if raw_url and not re.match(r"^https?://", raw_url, re.IGNORECASE):
                    raw_url = f"https://{raw_url}"
                return raw_url

            # Almost every entry is {"name": ..., "gameurl": ...}, but at
            # least one upstream port (arcanumce.zip) ships store as a
            # list of bare URL strings instead - handle both shapes
            # rather than assuming every entry is a dict.
            store = []
            for s in attr.get("store") or []:
                if isinstance(s, str):
                    url = s
                    name = ""
                else:
                    url = s.get("gameurl") or ""
                    name = s.get("name") or ""
                if url:
                    store.append({"name": name, "url": normalize_store_url(url)})

            port_details[port_id] = {
                "title": attr.get("title") or port_id,
                "repo": repo,
                "screenshot": (attr.get("image") or {}).get("screenshot") or "",
                "descHtml": render_markdown_field(attr.get("desc_md") or attr.get("desc")),
                "instHtml": render_markdown_field(attr.get("inst_md") or attr.get("inst")),
                "genres": attr.get("genres") or [],
                "reqs": attr.get("reqs") or [],
                "porter": attr.get("porter") or [],
                "runtime": attr.get("runtime") or [],
                "arch": attr.get("arch") or [],
                "rtr": bool(attr.get("rtr")),
                "downloads": port_stats.get("ports", {}).get(key, 0),
                "dateAdded": source.get("date_added") or "",
                "dateUpdated": source.get("date_updated") or "",
                "url": source_url,
                "store": store,
            }

        with port_details_path.open("w", encoding="utf-8") as f:
            json.dump(port_details, f, ensure_ascii=True, separators=(",", ":"))

    # Homepage screenshot mosaic: the most-downloaded ports whose screenshot
    # isn't letterboxed/pillarboxed, so the wall reads as game art rather
    # than a grid of black bars. Verdicts are cached in screenshot_bars.json
    # (keyed by port id + screenshot filename, so a re-shot screenshot is
    # re-checked) - only uncached entries hit the network.
    env.variables["mosaic_ports"] = build_mosaic_ports(base_path, port_details)

    # Load device info
    device_info_path = base_path / "device_info.json"
    device_info = {}

    if device_info_path.exists():
        with device_info_path.open(encoding="utf-8") as f:
            device_info = json.load(f)

    env.variables["device_info"] = device_info

    # Load porters info
    porters_path = base_path / "porters.json"
    porters = {}

    if porters_path.exists():
        with porters_path.open(encoding="utf-8") as f:
            porters = json.load(f)

    # Calculate port count and total downloads per porter
    porter_stats = {}
    for port_key, port_data in merged_ports.get("ports", {}).items():
        attr = port_data.get("attr", {})
        port_porters = attr.get("porter", [])
        downloads = port_stats.get("ports", {}).get(port_key, 0)

        for porter_name in port_porters:
            if porter_name not in porter_stats:
                porter_stats[porter_name] = {"port_count": 0, "total_downloads": 0, "ports": []}
            porter_stats[porter_name]["port_count"] += 1
            porter_stats[porter_name]["total_downloads"] += downloads
            porter_stats[porter_name]["ports"].append(port_key)

    # Merge porter info with stats
    for porter_name, stats in porter_stats.items():
        if porter_name in porters:
            porters[porter_name]["port_count"] = stats["port_count"]
            porters[porter_name]["total_downloads"] = stats["total_downloads"]
            porters[porter_name]["ports"] = stats["ports"]
        else:
            # Porter not in porters.json, create basic entry
            porters[porter_name] = {
                "name": porter_name,
                "bio": "",
                "social": "",
                "support": "",
                "webpage": "",
                "image": "",
                "port_count": stats["port_count"],
                "total_downloads": stats["total_downloads"],
                "ports": stats["ports"]
            }

    # Sort porters by port count (descending)
    sorted_porters = dict(sorted(porters.items(), key=lambda x: x[1].get("port_count", 0), reverse=True))

    env.variables["porters"] = sorted_porters

    # Build a lean per-porter data file for the standalone porter page
    # (/porter/?name=<id>), same reasoning as port_details.json above: one
    # small cacheable fetch instead of embedding every porter's full bio +
    # port list (with each port's title/repo/screenshot resolved) inline
    # in porters.md's own HTML, which is what made that page ~2MB.
    # Reuses port_details (already built above) for each port's display
    # fields instead of re-deriving them from merged_ports/port_stats again.
    porter_details = {}
    for porter_id, porter in sorted_porters.items():
        porter_ports = []
        for port_key in porter.get("ports", []):
            port_id = port_key.replace(".zip", "")
            pd = port_details.get(port_id)
            if pd:
                porter_ports.append({
                    "id": port_id,
                    "title": pd["title"],
                    "repo": pd["repo"],
                    "screenshot": pd["screenshot"],
                    "downloads": pd["downloads"],
                    "dateAdded": pd["dateAdded"],
                })
        porter_details[porter_id] = {
            "name": porter.get("name") or porter_id,
            "bio": porter.get("bio") or "",
            "social": porter.get("social") or "",
            "support": porter.get("support") or "",
            "webpage": porter.get("webpage") or "",
            "image": porter.get("image") or "",
            "portCount": porter.get("port_count", 0),
            "totalDownloads": porter.get("total_downloads", 0),
            "ports": porter_ports,
        }

    with (base_path / "porter_details.json").open("w", encoding="utf-8") as f:
        json.dump(porter_details, f, ensure_ascii=True, separators=(",", ":"))

    # Load packaged runtimes
    runtimes_zips_path = base_path / "runtimes_zips.json"
    runtimes_zips = []

    if runtimes_zips_path.exists():
        with runtimes_zips_path.open(encoding="utf-8") as f:
            runtimes_zips = json.load(f)

    env.variables["runtimes_zips"] = runtimes_zips

    # Load featured ports (curated themes/genres for the games.md carousels)
    featured_ports_path = base_path / "featured_ports.json"
    featured_ports_raw = []

    if featured_ports_path.exists():
        with featured_ports_path.open(encoding="utf-8") as f:
            featured_ports_raw = json.load(f)

    def build_featured_group(node):
        """Turn a featured_ports.json leaf node into a group of ports that actually exist."""
        group_ports = [key for key in node.get("ports", []) if key in merged_ports["ports"]]
        return {
            "name": node.get("name", ""),
            "description": node.get("description", ""),
            "ports": group_ports,
        }

    # Normalize both the flat (legacy) and category/children shapes into a single
    # list of {name, description, groups: [...]}, dropping deprecated entries and
    # groups that end up with no valid ports.
    featured_categories = []
    for node in featured_ports_raw:
        if node.get("deprecated"):
            continue

        if node.get("type") == "hero":
            continue  # handled separately, below, not shown as a carousel category

        if node.get("type") == "category":
            groups = []
            for child in node.get("children", []):
                if child.get("deprecated"):
                    continue
                group = build_featured_group(child)
                if group["ports"]:
                    groups.append(group)
            if groups:
                # A category like "Premium Games" can have 10+ sub-genre
                # groups, which makes Discover feel like an endless wall of
                # identical carousels. Cap how many show at once and rotate
                # a random subset each build so it varies site rebuilds
                # (hourly, per the CI cron) instead of always the same 4.
                MAX_GROUPS_PER_CATEGORY = 4
                if len(groups) > MAX_GROUPS_PER_CATEGORY:
                    groups = random.sample(groups, MAX_GROUPS_PER_CATEGORY)
                featured_categories.append({
                    "name": node.get("name", ""),
                    "description": node.get("description", ""),
                    "groups": groups,
                })
        else:
            group = build_featured_group(node)
            if group["ports"]:
                featured_categories.append({
                    "name": node.get("name", ""),
                    "description": node.get("description", ""),
                    "groups": [group],
                })

    env.variables["featured_categories"] = featured_categories

    # Pre-sort port keys for different sort orders
    port_keys = list(merged_ports["ports"].keys())

    def get_title(key):
        port = merged_ports["ports"].get(key, {})
        attr = port.get("attr", {})
        return (attr.get("title") or "").lower()

    def get_downloads(key):
        return port_stats.get("ports", {}).get(key, 0)

    def get_date_added(key):
        port = merged_ports["ports"].get(key, {})
        source = port.get("source", {})
        return source.get("date_added") or "0000-00-00"

    def get_date_updated(key):
        port = merged_ports["ports"].get(key, {})
        source = port.get("source", {})
        return source.get("date_updated") or "0000-00-00"

    # Create sorted lists of port keys
    sorted_orders = {
        "az": sorted(port_keys, key=get_title),
        "za": sorted(port_keys, key=get_title, reverse=True),
        "downloads": sorted(port_keys, key=get_downloads, reverse=True),
        "date-added": sorted(port_keys, key=get_date_added, reverse=True),
        "date-updated": sorted(port_keys, key=get_date_updated, reverse=True),
    }

    env.variables["sorted_orders"] = sorted_orders

    # ===== Discover hero banner =====
    # Preferred: whichever ports have a hand-supplied 21:9 image dropped in
    # docs/assets/images/hero/<port_id>.{jpg,png,webp} - screenshots/cover
    # art don't crop well into a wide hero card. The image filename (minus
    # extension) is the port id, so dropping/removing a file is all that's
    # needed to add/remove a hero slide - no JSON list to keep in sync.
    # Falls back to an auto-computed set (still true if no hero images exist
    # yet) so the banner never just breaks.
    HERO_DESC_MAX_LEN = 110
    HERO_IMAGE_DIR = base_path.parent / "images" / "hero"
    HERO_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]
    today = datetime.now()
    ninety_days_ago_str = (today - timedelta(days=90)).strftime("%Y-%m-%d")

    def is_rtr_key(key):
        attr = merged_ports["ports"].get(key, {}).get("attr") or {}
        return bool(attr.get("rtr"))

    def find_hero_custom_image(port_id):
        for ext in HERO_IMAGE_EXTENSIONS:
            if (HERO_IMAGE_DIR / f"{port_id}{ext}").exists():
                return f"../assets/images/hero/{port_id}{ext}"
        return None

    def build_hero_slide(label, key):
        port = merged_ports["ports"][key]
        attr = port.get("attr") or {}
        source = port.get("source") or {}
        source_url = source.get("url") or ""
        is_mv = "PortMaster-MV" in source_url or "MV-New" in source_url
        repo = "PortsMaster-MV/PortMaster-MV-New" if is_mv else "PortsMaster/PortMaster-New"
        port_id = key.replace(".zip", "")
        desc = (attr.get("desc_md") or attr.get("desc") or "").replace("\\n", " ").strip()
        if len(desc) > HERO_DESC_MAX_LEN:
            desc = desc[:HERO_DESC_MAX_LEN].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
        image = attr.get("image") or {}
        return {
            "label": label,
            "port_id": port_id,
            "title": attr.get("title") or port_id,
            "repo": repo,
            "screenshot": image.get("screenshot") or "",
            "custom_image_url": find_hero_custom_image(port_id),
            "desc": desc,
            "downloads": port_stats.get("ports", {}).get(key, 0),
            "rtr": bool(attr.get("rtr")),
            "url": source_url,
        }

    hero_used = set(HERO_EXCLUDE_KEYS)
    hero_slides = []

    # Optional labels (e.g. "Community Favorite") still come from
    # featured_ports.json's "hero" node, keyed by port id, but the node no
    # longer decides *which* ports show up - the image directory does.
    hero_node = next(
        (n for n in featured_ports_raw if n.get("type") == "hero" and not n.get("deprecated")),
        None,
    )
    hero_labels = {}
    if hero_node:
        for entry in hero_node.get("ports", []):
            key = entry.get("key") if isinstance(entry, dict) else entry
            label = entry.get("label", "") if isinstance(entry, dict) else ""
            if key:
                hero_labels[key.replace(".zip", "")] = label

    if HERO_IMAGE_DIR.exists():
        image_port_ids = sorted({
            f.stem for f in HERO_IMAGE_DIR.iterdir()
            if f.is_file() and f.suffix.lower() in HERO_IMAGE_EXTENSIONS
        })
        for port_id in image_port_ids:
            key = f"{port_id}.zip"
            if key not in merged_ports["ports"] or key in hero_used:
                continue
            hero_used.add(key)
            hero_slides.append(build_hero_slide(hero_labels.get(port_id, ""), key))

    if not hero_slides:
        def pick_top_excluding(candidate_keys):
            for key in candidate_keys:
                if key not in hero_used:
                    hero_used.add(key)
                    return key
            return None

        recent_90_keys = sorted(
            (k for k in port_keys if get_date_added(k) >= ninety_days_ago_str),
            key=get_downloads, reverse=True,
        )
        rtr_all_keys = sorted((k for k in port_keys if is_rtr_key(k)), key=get_downloads, reverse=True)
        rtr_recent_90_keys = [k for k in rtr_all_keys if get_date_added(k) >= ninety_days_ago_str]

        # Slide 1 is the same manually-set community-challenge port shown on
        # the homepage, not an auto-computed pick - the other four are.
        if PORT_OF_THE_MONTH_KEY in merged_ports["ports"]:
            hero_used.add(PORT_OF_THE_MONTH_KEY)
            hero_slides.append(build_hero_slide("Port of the Month", PORT_OF_THE_MONTH_KEY))

        hero_slide_defs = [
            ("Most Downloaded", sorted_orders["downloads"]),
            ("Trending Now", recent_90_keys),
            ("Top Ready to Run", rtr_all_keys),
            ("Trending Ready to Run", rtr_recent_90_keys),
        ]

        for label, candidates in hero_slide_defs:
            key = pick_top_excluding(candidates)
            if key:
                hero_slides.append(build_hero_slide(label, key))

    env.variables["hero_slides"] = hero_slides

    # Process device info for handhelds page
    processed_devices = {}
    for device_name, cfw_data in device_info.items():
        if device_name not in processed_devices:
            # Get manufacturer and resolution from first CFW entry
            first_cfw = next(iter(cfw_data.values()))
            manufacturer = first_cfw.get("manufacturer", "Unknown")
            resolution = first_cfw.get("resolution", [0, 0])
            cpu = first_cfw.get("cpu", "Unknown")
            ram = first_cfw.get("ram", 0)
            analogsticks = first_cfw.get("analogsticks", 0)

            # Determine aspect ratio from capabilities
            aspect_ratio = "4:3"  # default
            for cap in first_cfw.get("capabilities", []):
                if ":" in cap and any(c.isdigit() for c in cap):
                    aspect_ratio = cap
                    break

            # Check if device has unusual aspect ratio
            has_aspect_note = aspect_ratio not in ["4:3", "16:9"]

            processed_devices[device_name] = {
                "name": device_name,
                "manufacturer": manufacturer,
                "resolution": f"{resolution[0]}x{resolution[1]}",
                "aspect_ratio": aspect_ratio,
                "cpu": cpu,
                "ram_mb": ram,
                "ram_gb": round(ram / 1024, 1) if ram >= 1024 else None,
                "analogsticks": analogsticks,
                "cfw_list": sorted(cfw_data.keys()),
                "has_aspect_note": has_aspect_note,
                "cfw_count": len(cfw_data)
            }

    # Sort devices by manufacturer, then by name
    sorted_devices = dict(sorted(processed_devices.items(),
                                 key=lambda x: (x[1]["manufacturer"], x[1]["name"])))

    env.variables["devices"] = sorted_devices

    # Get unique manufacturers and CFW for filtering
    manufacturers = sorted(set(d["manufacturer"] for d in sorted_devices.values()))
    all_cfw = sorted(set(cfw for d in sorted_devices.values() for cfw in d["cfw_list"]))

    env.variables["manufacturers"] = manufacturers
    env.variables["all_cfw"] = all_cfw

    global _config_done_time
    _config_done_time = time.time()
    print("define_env finished, handing off to mkdocs for page rendering...", flush=True)


# mkdocs-macros calls these two around every single page's Jinja render.
# The main build phase after define_env gives zero console output by
# default, which is indistinguishable from a hang on a large site - this
# prints which page is being rendered and flags any that take a while,
# so a slow page (e.g. all-games.md's 1372-card loop) is visible instead
# of a silent multi-minute wait.
_page_render_start = {}


def on_pre_page_macros(env):
    _page_render_start[env.page.file.src_path] = time.time()
    print(f"  Rendering {env.page.file.src_path}...", flush=True)


def on_post_page_macros(env):
    start = _page_render_start.pop(env.page.file.src_path, None)
    if start is not None:
        elapsed = time.time() - start
        if elapsed > 0.5:
            print(f"    -> {env.page.file.src_path} took {elapsed:.1f}s", flush=True)


def on_post_build(env):
    if _config_done_time is not None:
        print(f"on_post_build reached {time.time() - _config_done_time:.1f}s after define_env finished (covers markdown->HTML + theme templating + search indexing for every page)", flush=True)
