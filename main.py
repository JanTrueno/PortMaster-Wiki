import json
import markdown
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.error

MARKDOWN_EXTENSIONS = ["tables", "fenced_code"]


def render_markdown_field(content):
    """Render a desc/inst markdown field to HTML at build time, so the
    standalone port page doesn't need to ship a markdown parser to the
    client just to show text that never changes without a rebuild."""
    content = (content or "").strip()
    if not content or content == "None":
        return ""
    return markdown.markdown(content, extensions=MARKDOWN_EXTENSIONS)

def download_github_json(url, local_path):
    """Download a JSON file from GitHub to local path"""
    try:
        print(f"Downloading {url}...")
        with urllib.request.urlopen(url) as response:
            data = response.read()
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with local_path.open('wb') as f:
                f.write(data)
        print(f"✓ Downloaded to {local_path}")
        return True
    except urllib.error.URLError as e:
        print(f"✗ Failed to download {url}: {e}")
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
        "featured_ports.json": f"{github_info}/featured_ports.json",
    }

    success_count = 0
    for filename, url in files_to_download.items():
        local_path = base_path / filename
        if download_github_json(url, local_path):
            success_count += 1

    print(f"\nDownloaded {success_count}/{len(files_to_download)} files successfully")
    return success_count > 0

def define_env(env):
    base_path = Path(__file__).parent / "docs" / "assets" / "json"

    # Download JSONs from GitHub (comment out if you want to use local files only)
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
    port_details = {}
    for key, port in merged_ports["ports"].items():
        port_id = key.replace(".zip", "")
        attr = port.get("attr") or {}
        source = port.get("source") or {}
        source_url = source.get("url") or ""
        is_mv = "PortMaster-MV" in source_url or "MV-New" in source_url
        repo = "PortsMaster-MV/PortMaster-MV-New" if is_mv else "PortsMaster/PortMaster-New"

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
        }

    port_details_path = base_path / "port_details.json"
    with port_details_path.open("w", encoding="utf-8") as f:
        json.dump(port_details, f, ensure_ascii=True, separators=(",", ":"))

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

        if node.get("type") == "category":
            groups = []
            for child in node.get("children", []):
                if child.get("deprecated"):
                    continue
                group = build_featured_group(child)
                if group["ports"]:
                    groups.append(group)
            if groups:
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
