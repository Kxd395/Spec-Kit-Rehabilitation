"""Verbose output utilities for detailed logging and debugging.

This module provides the VerboseLogger class for formatted, detailed output
when the --verbose flag is enabled.
"""

from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
import time

console = Console()


class VerboseLogger:
    """Logger for detailed verbose output with rich formatting."""
    
    def __init__(self, enabled: bool = False):
        """Initialize the verbose logger.
        
        Args:
            enabled: Whether verbose logging is enabled
        """
        self.enabled = enabled
        self._start_time: Optional[float] = None
    
    def start(self) -> None:
        """Start timing for the current operation."""
        if self.enabled:
            self._start_time = time.time()
    
    def elapsed(self) -> str:
        """Get elapsed time since start().
        
        Returns:
            Formatted elapsed time string
        """
        if self._start_time is None:
            return "0.00s"
        elapsed = time.time() - self._start_time
        return f"{elapsed:.2f}s"
    
    def section(self, title: str, emoji: str = "📋") -> None:
        """Print a section header.
        
        Args:
            title: Section title
            emoji: Emoji to display (default: 📋)
        """
        if self.enabled:
            console.print(f"\n{emoji} [bold cyan]{title}[/bold cyan]")
    
    def info(self, message: str) -> None:
        """Print an info message.
        
        Args:
            message: Message to print
        """
        if self.enabled:
            console.print(f"  ℹ️  {message}")
    
    def success(self, message: str) -> None:
        """Print a success message.
        
        Args:
            message: Message to print
        """
        if self.enabled:
            console.print(f"  ✅ [green]{message}[/green]")
    
    def warning(self, message: str) -> None:
        """Print a warning message.
        
        Args:
            message: Message to print
        """
        if self.enabled:
            console.print(f"  ⚠️  [yellow]{message}[/yellow]")
    
    def error(self, message: str) -> None:
        """Print an error message.
        
        Args:
            message: Message to print
        """
        if self.enabled:
            console.print(f"  ❌ [red]{message}[/red]")
    
    def detail(self, key: str, value: str) -> None:
        """Print a key-value detail.
        
        Args:
            key: Detail key
            value: Detail value
        """
        if self.enabled:
            console.print(f"     • {key}: [dim]{value}[/dim]")
    
    def code(self, code: str, language: str = "python") -> None:
        """Print syntax-highlighted code.
        
        Args:
            code: Code to display
            language: Programming language (default: python)
        """
        if self.enabled:
            syntax = Syntax(code, language, theme="monokai", line_numbers=False)
            console.print(syntax)
    
    def table(self, title: str, headers: list[str], rows: list[list[str]]) -> None:
        """Print a formatted table.
        
        Args:
            title: Table title
            headers: Column headers
            rows: Table rows
        """
        if self.enabled:
            table = Table(title=title, show_header=True, header_style="bold magenta")
            for header in headers:
                table.add_column(header)
            for row in rows:
                table.add_row(*row)
            console.print(table)
    
    def panel(self, content: str, title: str, border_style: str = "blue") -> None:
        """Print content in a panel.
        
        Args:
            content: Content to display
            title: Panel title
            border_style: Border color (default: blue)
        """
        if self.enabled:
            panel = Panel(content, title=title, border_style=border_style)
            console.print(panel)
    
    def files(self, files: list[str], max_display: int = 10) -> None:
        """Print a list of files.
        
        Args:
            files: List of file paths
            max_display: Maximum files to display (default: 10)
        """
        if self.enabled:
            displayed = files[:max_display]
            for f in displayed:
                console.print(f"     • {f}")
            if len(files) > max_display:
                remaining = len(files) - max_display
                console.print(f"     ... and {remaining} more files")
    
    def progress(self, current: int, total: int, item: str = "") -> None:
        """Print progress information.
        
        Args:
            current: Current item number
            total: Total items
            item: Optional item description
        """
        if self.enabled:
            percentage = (current / total * 100) if total > 0 else 0
            item_str = f" ({item})" if item else ""
            console.print(f"     [{current}/{total}] {percentage:.1f}%{item_str}")
    
    def separator(self) -> None:
        """Print a visual separator."""
        if self.enabled:
            console.print("  " + "─" * 60)
