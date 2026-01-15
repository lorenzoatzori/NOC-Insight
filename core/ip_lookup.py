# noc_insight/core/ip_lookup.py
from typing import Optional
import ipaddress
from .context_loader import ContextLoader

def lookup_ip(ip: str, ctx: ContextLoader) -> str:
    info = ctx.ip_map.get(ip)
    lines = [f"IP: {ip}"]

    if info:
        vlan_obj = ctx.vlans.get(info.vlan) if info.vlan else None
        if vlan_obj:
            lines.append(f"VLAN: {info.vlan} ({vlan_obj.name})")
            lines.append(f"Subnet: {vlan_obj.subnet}")
        else:
            lines.append(f"VLAN: {info.vlan or '-'}")
            lines.append("Subnet: -")

        if info.device:
            device = ctx.devices.get(info.device)
            if device:
                lines.append(f"Device: {device.id}")
                lines.append(f"Device type: {device.type}")
                lines.append(f"Location: {device.location or '-'}")
                port_name = device.port
                switch_name = device.switch or device.id
                if port_name:
                    port_key = f"{switch_name}|{port_name}"
                    port = ctx.ports.get(port_key)
                    if port:
                        lines.append(f"Switch: {port.device}")
                        lines.append(f"Port: {port.name}")
                        lines.append(f"PoE: {'Yes' if port.poe else 'No'}")
                    else:
                        lines.append(f"Switch: {switch_name}")
                        lines.append(f"Port: {port_name}")
            else:
                lines.append(f"Device: {info.device}")
    else:
        # fallback: try VLAN by subnet
        try:
            ipobj = ipaddress.ip_address(ip)
            found = False
            for vlan in ctx.vlans.values():
                net = ipaddress.ip_network(vlan.subnet, strict=False)
                if ipobj in net:
                    lines.append(f"VLAN: {vlan.id} ({vlan.name})")
                    lines.append(f"Subnet: {vlan.subnet}")
                    found = True
                    break
            if not found:
                lines.append("VLAN: -")
                lines.append("Subnet: -")
            lines.append("Device: -")
        except ValueError:
            lines.append("VLAN: -")
            lines.append("Subnet: -")
            lines.append("Device: -")
    return "\n".join(lines)
