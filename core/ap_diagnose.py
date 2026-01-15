# noc_insight/core/ap_diagnose.py
from typing import Optional
from .context_loader import ContextLoader


def diagnose_ap(ap_id: str, ctx: ContextLoader) -> str:
    lines = [f"AP: {ap_id}"]

    ap = ctx.devices.get(ap_id)
    if not ap:
        lines.append("[!] AP not found in context")
        return '\n'.join(lines)

    # Switch
    switch_name = ap.switch
    port_name = ap.port
    if switch_name:
        lines.append(f"Switch: {switch_name}")
    else:
        lines.append("Switch: -")

    if port_name:
        lines.append(f"Port: {port_name}")
    else:
        lines.append("Port: -")

    # PoE
    poe_str = '-'
    if switch_name and port_name:
        port_key = f"{switch_name}|{port_name}"
        port_obj = ctx.ports.get(port_key)
        if port_obj and port_obj.poe is not None:
            poe_str = 'Yes' if port_obj.poe else 'No'
    lines.append(f"PoE: {poe_str}")

    # AP VLANs
    vlans_str = ', '.join(ap.vlans) if ap.vlans else '-'
    lines.append(f"VLANs: {vlans_str}")

    # Additional status placeholder (future: err-disable, link down)
    lines.append(f"Status: Unknown")

    return '\n'.join(lines)
