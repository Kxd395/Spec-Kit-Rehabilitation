from rich.panel import Panel
from rich.console import Console

def show_banner(console: Console | None = None) -> None:
    c = console or Console()
    c.print(
        Panel.fit(
            "[bold cyan]Spec-Kit[/bold cyan]  •  Security scanning and specs workflow",
            title="specify-cli",
            border_style="cyan",
        )
    )
