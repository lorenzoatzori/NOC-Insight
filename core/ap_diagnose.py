# noc_insight/commands/ap_diagnose.py
"""
AP / Port diagnostic command.

This command correlates static topology info with passive log analysis
in order to speed up NOC troubleshooting.
"""

import click
from pathlib import Path

from noc_insight.core.log_analyzer import LogAnalyzer
from noc_insight.core.decision_engine import DecisionEngine


@click.command()
@click.option("--switch", required=True, help="Switch name (e.g. SW-3F-01)")
@click.option("--port", required=True, help="Interface name (e.g. Gi1/0/24)")
@click.option("--ap", required=False, help="AP name (optional)")
@click.option(
    "--logs-dir",
    default="noc_insight/logs",
    show_default=True,
    help="Directory containing device log files",
)
def ap_diagnose(switch, port, ap, logs_dir):
    """Diagnose an AP or switch port using passive log analysis."""

    logs_path = Path(logs_dir)
    analyzer = LogAnalyzer(logs_path)

    # --- PORT ANALYSIS ---
    port_result = analyzer.analyze_port(switch=switch, port=port)

    click.echo("\n[PORT STATUS]")
    click.echo(f"Switch     : {switch}")
    click.echo(f"Port       : {port}")
    click.echo(f"Link state : {port_result['link'] or 'unknown'}")
    click.echo(f"Err-disable: {'YES' if port_result['err_disable'] else 'NO'}")
    click.echo(f"PoE        : {port_result['poe'] or 'ok'}")

    if port_result["last_event"]:
        click.echo("\nLast port-related log event:")
        click.echo(port_result["last_event"])
    else:
        click.echo("\nNo relevant port events found in logs.")

    # --- DECISION ENGINE (PORT) ---
    click.echo("\n[TROUBLESHOOTING HINTS]")
    for hint in DecisionEngine.analyze_port(port_result):
        click.echo(f"- {hint}")

    # --- AP ANALYSIS (optional) ---
    if ap:
        ap_result = analyzer.analyze_ap(ap_id=ap, wlc="WLC-01")

        click.echo("\n[AP STATUS]")
        click.echo(f"AP         : {ap}")
        click.echo(f"AP status  : {ap_result['ap_status'] or 'unknown'}")

        if ap_result["last_event"]:
            click.echo("Last AP-related log event:")
            click.echo(ap_result["last_event"])
        else:
            click.echo("No AP-related events found in logs.")

        # --- DECISION ENGINE (AP) ---
        click.echo("\n[AP TROUBLESHOOTING HINTS]")
        for hint in DecisionEngine.analyze_ap(ap_result):
            click.echo(f"- {hint}")


if __name__ == "__main__":
    ap_diagnose()
