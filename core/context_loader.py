# noc_insight/core/context_loader.py
import json
from pathlib import Path
from typing import Dict, List
from .models import Device, Port, VLAN, IPMapping

class ContextLoader:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.devices: Dict[str, Device] = {}
        self.ports: Dict[str, Port] = {}
        self.vlans: Dict[str, VLAN] = {}
        self.ip_map: Dict[str, IPMapping] = {}

    def _load_json(self, filename: str):
        path = self.data_dir / filename
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_all(self):
        devices_json = self._load_json("devices.json") or {}
        for k, v in devices_json.items():
            self.devices[k] = Device(**v)

        ports_json = self._load_json("ports.json") or []
        for p in ports_json:
            key = f"{p['device']}|{p['name']}"
            self.ports[key] = Port(**p)

        vlans_json = self._load_json("vlans.json") or {}
        for k, v in vlans_json.items():
            self.vlans[k] = VLAN(**v)

        ip_map_json = self._load_json("ip_map.json") or {}
        for k, v in ip_map_json.items():
            self.ip_map[k] = IPMapping(**v)
