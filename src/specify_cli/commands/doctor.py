"""Doctor command for environment checks."""

from __future__ import annotations
import importlib
import shutil
import typer
from rich.console import Console
from rich.table import Table

from specify_cli.verbose import VerboseLogger

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
    except (ImportError, AttributeError):
        # Module not installed or has no __version__ attribute
        return "not installed"


@app.command("run")
def doctor(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """Check development environment."""
    console = Console()
    logger = VerboseLogger(enabled=verbose)
    logger.start()

    logger.section("Environment Check", "🏥")
    logger.info("Checking tool availability and versions...")

    t = Table(title="SpecKit Doctor")
    t.add_column("Tool")
    t.add_column("Status")

    # Check packages
    tools = [
        ("bandit", "bandit"),
        ("safety (python pkg)", "safety"),
        ("safety (cli)", None),  # Special case - CLI tool
        ("radon", "radon"),
    ]

    for tool_name, module_name in tools:
        if module_name:
            version = _version(module_name)
            t.add_row(tool_name, version)
            if verbose:
                if version == "not installed":
                    logger.warning(f"{tool_name}: not installed")
                elif version == "not found":
                    logger.warning(f"{tool_name}: installed but version not found")
                else:
                    logger.success(f"{tool_name}: {version}")
        else:
            # Check CLI tool
            cli_path = shutil.which("safety")
            status = cli_path or "missing"
            t.add_row(tool_name, status)
            if verbose:
                if cli_path:
                    logger.success(f"safety CLI: {cli_path}")
                else:
                    logger.warning("safety CLI: not found in PATH")

    console.print(t)

    logger.separator()
    logger.info(f"Check complete in {logger.elapsed()}")
    console.print("If missing, run: pip install -e '.[analysis]'")
