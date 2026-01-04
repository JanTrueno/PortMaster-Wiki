import json
from pathlib import Path
from datetime import datetime

def define_env(env):
    base_path = Path(__file__).parent / "docs" / "assets" / "json"
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