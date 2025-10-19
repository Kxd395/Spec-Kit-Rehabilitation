# Commands

CLI entry points for Spec-Kit.

## Commands

### audit

Runs security analyzers via runner and writes output in multiple formats.

**Features**:
- Multi-analyzer orchestration (Bandit + Safety)
- SARIF, HTML, and JSON output formats
- Baseline filtering support
- Exit code gating by severity
- Strict mode for analyzer availability checks

**Usage**:
```bash
specify audit run --output sarif --fail-on MEDIUM --strict
```

### doctor

Verifies tool presence and prints versions.

**Features**:
- Checks Python version
- Verifies Bandit availability
- Verifies Safety CLI presence
- Displays versions for all tools

**Usage**:
```bash
specify doctor run
```

## Adding a New Command

1. Create `src/specify_cli/commands/your_command.py`
2. Import Typer and create app:

```python
import typer
app = typer.Typer(help="Your command description")

@app.command("run")
def your_command():
    """Your command logic."""
    pass
```

3. Register in main CLI (`src/specify_cli/__init__.py`):

```python
from specify_cli.commands import your_command
app.add_typer(your_command.app, name="your-command")
```

## Best Practices

- Use `typer.Option()` for all parameters
- Provide clear help text for all options
- Use Rich Console for output formatting
- Return appropriate exit codes (0=success, 1=findings, 2=error)
- Load configuration early and merge with CLI arguments
- Log operations using the logging module
