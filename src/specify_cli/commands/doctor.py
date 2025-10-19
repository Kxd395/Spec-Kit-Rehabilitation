"""Doctor command for environment validation."""
from __future__ import annotations
import importlib
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Environment checks")


def _version(mod: str) -> str:
    """Get version of a module.
    
    Args:
        mod: Module name to check
        
    Returns:
        Version string or status message
    """
    try:
        m = importlib.import_module(mod)
        return getattr(m, "__version__", "not found")
    except Exception:
        return "not installed"


@app.command("run")
def doctor():
    """Check installed tools and versions."""
    console = Console()
    t = Table(title="SpecKit Doctor")
    t.add_column("Tool")
    t.add_column("Status")
    t.add_row("bandit", _version("bandit"))
    t.add_row("safety", _version("safety"))
    t.add_row("radon", _version("radon"))
    t.add_row("typer", _version("typer"))
    t.add_row("rich", _version("rich"))
    console.print(t)
    console.print("\n[yellow]If missing, run:[/yellow] pip install -e '.[analysis]'")
