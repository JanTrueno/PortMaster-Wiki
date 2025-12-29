import json
from pathlib import Path

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