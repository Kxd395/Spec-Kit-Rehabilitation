"""Structured error messages and exceptions for Spec-Kit CLI.

This module provides user-friendly error messages and custom exceptions
to improve the debugging experience.
"""

from typing import Any, Optional
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


class SpecKitError(Exception):
    """Base exception for all Spec-Kit errors."""

    def __init__(self, message: str, hint: Optional[str] = None, details: Optional[dict] = None):
        """Initialize error with message, optional hint, and details.

        Args:
            message: Error message
            hint: Optional hint for resolution
            details: Optional dictionary of additional details
        """
        self.message = message
        self.hint = hint
        self.details = details or {}
        super().__init__(message)

    def display(self) -> None:
        """Display formatted error with rich formatting."""
        content = Text()
        content.append("❌ ", style="bold red")
        content.append(self.message, style="red")

        if self.hint:
            content.append("\n\n💡 ", style="bold yellow")
            content.append("Hint: ", style="bold yellow")
            content.append(self.hint, style="yellow")

        if self.details:
            content.append("\n\n📋 Details:\n", style="bold cyan")
            for key, value in self.details.items():
                content.append(f"  • {key}: ", style="cyan")
                content.append(f"{value}\n", style="dim")

        panel = Panel(content, title="[bold red]Error[/bold red]", border_style="red")
        console.print(panel)


class ConfigError(SpecKitError):
    """Error in configuration file or settings."""

    def __init__(self, message: str, config_file: Optional[Path] = None, **kwargs):
        """Initialize configuration error.

        Args:
            message: Error message
            config_file: Path to problematic config file
            **kwargs: Additional arguments for SpecKitError
        """
        details = kwargs.get("details", {})
        if config_file:
            details["config_file"] = str(config_file)
        kwargs["details"] = details
        super().__init__(message, **kwargs)


class AnalyzerError(SpecKitError):
    """Error running an analyzer."""

    def __init__(self, analyzer: str, message: str, **kwargs):
        """Initialize analyzer error.

        Args:
            analyzer: Name of the analyzer (e.g., 'bandit', 'safety')
            message: Error message
            **kwargs: Additional arguments for SpecKitError
        """
        details = kwargs.get("details", {})
        details["analyzer"] = analyzer
        kwargs["details"] = details
        super().__init__(message, **kwargs)


class FileNotFoundError(SpecKitError):
    """Required file not found."""

    def __init__(self, file_path: Path, **kwargs):
        """Initialize file not found error.

        Args:
            file_path: Path to missing file
            **kwargs: Additional arguments for SpecKitError
        """
        message = f"File not found: {file_path}"
        details = kwargs.get("details", {})
        details["file_path"] = str(file_path)
        kwargs["details"] = details
        super().__init__(message, **kwargs)


class ValidationError(SpecKitError):
    """Data validation error."""

    def __init__(self, field: str, value: Any, reason: str, **kwargs):
        """Initialize validation error.

        Args:
            field: Field name that failed validation
            value: Invalid value
            reason: Reason for validation failure
            **kwargs: Additional arguments for SpecKitError
        """
        message = f"Invalid value for '{field}': {reason}"
        details = kwargs.get("details", {})
        details["field"] = field
        details["value"] = str(value)
        details["reason"] = reason
        kwargs["details"] = details
        super().__init__(message, **kwargs)


class DependencyError(SpecKitError):
    """Missing or incompatible dependency."""

    def __init__(self, dependency: str, required_version: Optional[str] = None, **kwargs):
        """Initialize dependency error.

        Args:
            dependency: Name of missing dependency
            required_version: Required version if applicable
            **kwargs: Additional arguments for SpecKitError
        """
        message = f"Missing or incompatible dependency: {dependency}"
        if required_version:
            message += f" (requires {required_version})"

        details = kwargs.get("details", {})
        details["dependency"] = dependency
        if required_version:
            details["required_version"] = required_version
        kwargs["details"] = details

        if "hint" not in kwargs:
            kwargs["hint"] = f"Install with: pip install {dependency}"

        super().__init__(message, **kwargs)


class GitError(SpecKitError):
    """Git operation error."""

    def __init__(self, message: str, command: Optional[str] = None, **kwargs):
        """Initialize Git error.

        Args:
            message: Error message
            command: Git command that failed
            **kwargs: Additional arguments for SpecKitError
        """
        details = kwargs.get("details", {})
        if command:
            details["command"] = command
        kwargs["details"] = details
        super().__init__(message, **kwargs)


# Common error messages with helpers
def missing_config_file(config_path: Path) -> ConfigError:
    """Create error for missing config file.

    Args:
        config_path: Path where config was expected

    Returns:
        ConfigError with helpful message
    """
    return ConfigError(
        f"Configuration file not found: {config_path}",
        config_file=config_path,
        hint="Run 'specify init' to create a default configuration",
    )


def invalid_output_format(format_name: str, valid_formats: list[str]) -> ValidationError:
    """Create error for invalid output format.

    Args:
        format_name: Invalid format name
        valid_formats: List of valid format names

    Returns:
        ValidationError with helpful message
    """
    return ValidationError(
        field="output_format",
        value=format_name,
        reason=f"must be one of: {', '.join(valid_formats)}",
        hint=f"Valid formats: {', '.join(valid_formats)}",
    )


def analyzer_not_available(analyzer_name: str, strict_mode: bool = False) -> AnalyzerError:
    """Create error for unavailable analyzer.

    Args:
        analyzer_name: Name of unavailable analyzer
        strict_mode: Whether running in strict mode

    Returns:
        AnalyzerError with helpful message
    """
    message = f"Analyzer '{analyzer_name}' is not available"
    if strict_mode:
        message += " (strict mode enabled)"

    hints = {
        "bandit": "Install with: pip install bandit",
        "safety": "Install with: pip install safety",
        "radon": "Install with: pip install radon",
    }

    return AnalyzerError(
        analyzer=analyzer_name,
        message=message,
        hint=hints.get(analyzer_name, f"Install {analyzer_name} and try again"),
    )


def git_not_available() -> GitError:
    """Create error for missing Git.

    Returns:
        GitError with helpful message
    """
    return GitError(
        "Git is not available in PATH", hint="Install Git: https://git-scm.com/downloads"
    )


def not_a_git_repo(path: Path) -> GitError:
    """Create error for non-Git directory.

    Args:
        path: Path that is not a Git repository

    Returns:
        GitError with helpful message
    """
    return GitError(f"Not a Git repository: {path}", hint="Initialize with: git init")
