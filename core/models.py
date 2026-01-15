# noc_insight/core/models.py
from __future__ import annotations
from typing import Optional, List

class Device:
    def __init__(self, id: str, type: str, location: Optional[str]=None, uplink: Optional[str]=None, port: Optional[str]=None, vlans: Optional[List[str]]=None, switch: Optional[str]=None):
        self.id = id
        self.type = type
        self.location = location
        self.uplink = uplink
        self.port = port
        self.vlans = vlans or []
        self.switch = switch

class Port:
    def __init__(self, device: str, name: str, connected_device: Optional[str]=None, poe: Optional[bool]=None):
        self.device = device
        self.name = name
        self.connected_device = connected_device
        self.poe = poe

class VLAN:
    def __init__(self, id: str, name: str, subnet: str):
        self.id = id
        self.name = name
        self.subnet = subnet

class IPMapping:
    def __init__(self, ip: str, vlan: Optional[str]=None, device: Optional[str]=None):
        self.ip = ip
        self.vlan = vlan
        self.device = device
