# noc_insight/core/decision_engine.py
"""
Decision engine for NOC-Insight.

Transforms low-level signals (logs, states, flags)
into human-readable troubleshooting hints.

This module DOES NOT try to be "smart" or "AI-like".
It encodes real NOC reasoning and best practices.
"""

from typing import Dict, List


class DecisionEngine:
    @staticmethod
    def analyze_port(port_data: Dict) -> List[str]:
        """Return actionable hints based on port analysis."""
        hints: List[str] = []

        if port_data.get("err_disable"):
            hints.append(
                "POSSIBLE CAUSE: Port is err-disabled → check port-security, BPDU Guard, or policy violations"
            )

        if port_data.get("poe") == "fault":
            hints.append(
                "POSSIBLE CAUSE: PoE fault → verify power budget, cable quality, or AP power requirements"
            )

        if port_data.get("link") == "down":
            hints.append(
                "POSSIBLE CAUSE: Link down → check cable, NIC/AP status, or administrative shutdown"
            )

        if not hints:
            hints.append("No obvious issues detected from logs")

        return hints

    @staticmethod
    def analyze_ap(ap_data: Dict) -> List[str]:
        """Return actionable hints based on AP analysis."""
        hints: List[str] = []

        if ap_data.get("ap_status") == "join_failed":
            hints.append(
                "POSSIBLE CAUSE: AP failed to join WLC → check connectivity, CAPWAP, or AP authorization"
            )

        if not hints:
            hints.append("No AP-specific issues detected from logs")

        return hints
