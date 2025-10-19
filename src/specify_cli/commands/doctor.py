"""Doctor command for environment checks."""
from __future__ import annotations
import importlib
import shutil
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Environment checks")


def _version(mod: str) -> str:
    """Get package version.
    
    Args:
        mod: Module name
        
    Returns:
        Version string or status
    """
    try:
        m = importlib.import_module(mod)
        return getattr(m, "__version__", "not found")
    except Exception:
        return "not installed"


@app.command("run")
def doctor():
    """Check development environment."""
    console = Console()
    t = Table(title="SpecKit Doctor")
    t.add_column("Tool")
    t.add_column("Status")
    t.add_row("bandit", _version("bandit"))
    t.add_row("safety (python pkg)", _version("safety"))
    t.add_row("safety (cli)", shutil.which("safety") or "missing")
    t.add_row("radon", _version("radon"))
    console.print(t)
    console.print("If missing, run: pip install -e '.[analysis]'")
