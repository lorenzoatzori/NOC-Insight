import click
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.context_loader import ContextLoader
from core.ip_lookup import lookup_ip

DEFAULT_DATA_DIR = Path("data")

@click.group()
def cli():
    """NOC-Insight CLI"""
    pass

@cli.command()
@click.argument("ip")
@click.option("--data-dir", default=DEFAULT_DATA_DIR, help="Directory with context JSON files")
def ip_lookup_cmd(ip, data_dir):
    ctx = ContextLoader(Path(data_dir))
    ctx.load_all()
    result = lookup_ip(ip, ctx)
    click.echo(result)

if __name__ == "__main__":
    cli()
