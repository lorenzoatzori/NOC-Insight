# noc_insight/core/log_analyzer.py
"""
Passive log analyzer for NOC-Insight.

This module parses plain-text log files and extracts troubleshooting signals
for switches, ports and APs.

Design goals:
- NO live SSH
- NO vendor lock-in (pattern based)
- Safe to run on jump hosts
- Easy to extend with new patterns

Expected log layout:
  noc_insight/logs/
    ├── SW-3F-01.log
    ├── SW-CORE-01.log
    └── WLC-01.log

Logs are treated as append-only text files.
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Optional, List
import re


# --- Pattern definitions (vendor-agnostic) ---
PATTERNS = {
    "link_down": re.compile(r"LINK-3-UPDOWN|Interface .* down", re.IGNORECASE),
    "link_up": re.compile(r"LINK-3-UPDOWN|Interface .* up", re.IGNORECASE),
    "err_disable": re.compile(r"ERR-?DISABLE", re.IGNORECASE),
    "poe_fault": re.compile(r"POWER_DENY|PoE fault|power inline.*deny", re.IGNORECASE),
    "ap_join_fail": re.compile(r"CAPWAP|Join failed|AP .* not joined", re.IGNORECASE),
}


class LogAnalyzer:
    def __init__(self, logs_dir: Path):
        self.logs_dir = logs_dir

    def _read_log(self, name: str) -> List[str]:
        path = self.logs_dir / f"{name}.log"
        if not path.exists():
            return []
        try:
            return path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            return []

    def analyze_port(self, switch: str, port: str) -> Dict[str, Optional[str]]:
        """Analyze logs for a specific switch port."""
        lines = self._read_log(switch)
        result = {
            "link": None,
            "err_disable": False,
            "poe": None,
            "last_event": None,
        }

        for line in reversed(lines):  # newest first
            if port not in line:
                continue

            if PATTERNS["err_disable"].search(line):
                result["err_disable"] = True
                result["last_event"] = line
                break

            if PATTERNS["poe_fault"].search(line):
                result["poe"] = "fault"
                result["last_event"] = line
                break

            if PATTERNS["link_down"].search(line):
                result["link"] = "down"
                result["last_event"] = line
                break

            if PATTERNS["link_up"].search(line):
                result["link"] = "up"
                result["last_event"] = line
                break

        return result

    def analyze_ap(self, ap_id: str, wlc: Optional[str] = None) -> Dict[str, Optional[str]]:
        """Analyze AP-related logs (typically on WLC)."""
        if not wlc:
            return {"ap_status": None, "last_event": None}

        lines = self._read_log(wlc)
        for line in reversed(lines):
            if ap_id not in line:
                continue
            if PATTERNS["ap_join_fail"].search(line):
                return {
                    "ap_status": "join_failed",
                    "last_event": line,
                }
        return {"ap_status": None, "last_event": None}
