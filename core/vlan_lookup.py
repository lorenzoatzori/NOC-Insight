# noc_insight/core/vlan_lookup.py

from typing import Optional
from noc_insight.core.context_loader import ContextLoader
from noc_insight.core.models import VLAN
import ipaddress


def vlan_lookup(ip: str, ctx: ContextLoader) -> Optional[VLAN]:
    """
    Resolve an IP address to its VLAN.

    Priority:
    1. Exact IP match from ip_map
    2. Subnet match from VLAN definitions

    Returns:
        VLAN object if found, otherwise None
    """

    try:
        ip_addr = ipaddress.ip_address(ip)
    except ValueError:
        return None

    # 1️⃣ Exact IP → VLAN mapping
    ip_entry = ctx.ip_map.get(ip)
    if ip_entry:
        vlan_id = ip_entry.vlan_id
        return ctx.vlans.get(vlan_id)

    # 2️⃣ Subnet match
    for vlan in ctx.vlans.values():
        try:
            subnet = ipaddress.ip_network(vlan.subnet)
            if ip_addr in subnet:
                return vlan
        except ValueError:
            continue

    return None
