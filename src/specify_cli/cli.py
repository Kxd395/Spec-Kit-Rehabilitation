"""Specify CLI - Spec-first analysis tool."""

from __future__ import annotations
import typer

# Import sub-commands
from specify_cli.commands.audit import app as audit_app
from specify_cli.commands.doctor import app as doctor_app

# Create main app
app = typer.Typer(help="Spec-first analysis CLI")

# Register sub-commands
app.add_typer(audit_app, name="audit", help="Run security analysis")
app.add_typer(doctor_app, name="doctor", help="Check environment and tools")


if __name__ == "__main__":
    app()
