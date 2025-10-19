"""Banner display for CLI."""
from rich.console import Console
from rich.panel import Panel


def show_banner(console: Console | None = None) -> None:
    """Display the Spec-Kit banner."""
    if console is None:
        console = Console()
    banner = Panel.fit("[bold]Spec-Kit[/bold] - Specification Tool", border_style="cyan")
    console.print(banner)
