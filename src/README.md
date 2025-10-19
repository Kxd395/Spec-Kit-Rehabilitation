# Source Code Directory

This directory contains the main `specify-cli` Python package source code.

## Structure

```
src/specify_cli/
├── analyzers/          # Security analyzers (Bandit, Safety)
├── commands/           # CLI command modules (audit, doctor)
├── reporters/          # Output formatters (SARIF, HTML, JSON)
├── __init__.py        # Main CLI application and init/check commands
├── baseline.py        # Baseline filtering system
├── cli.py             # CLI application bootstrap
├── config.py          # Configuration management (.speckit.toml + ENV)
├── gitutils.py        # Git integration utilities
├── logging.py         # Logging configuration
├── runner.py          # Analyzer orchestration
└── store.py           # Data persistence utilities
```

## Key Modules

### Analyzers (`analyzers/`)
Security scanning implementations:
- **bandit_analyzer.py**: Python code security scanner with exclude pattern support
- **safety_analyzer.py**: Dependency vulnerability scanner with manifest detection

### Commands (`commands/`)
CLI command implementations:
- **audit.py**: Main security analysis command (`specify audit run`)
- **doctor.py**: Environment validation command (`specify doctor run`)

### Reporters (`reporters/`)
Output format generators:
- **sarif.py**: SARIF 2.1.0 format (GitHub Code Scanning compatible)
- **html.py**: XSS-safe HTML reports

### Core Files

- **config.py**: Configuration system supporting `.speckit.toml` files and environment variable overrides
- **baseline.py**: Smart baseline filtering with regex support and inline comment suppression
- **runner.py**: Orchestrates multiple analyzers (Bandit + Safety)
- **__init__.py**: Main CLI application, template downloading, project initialization

## Development

### Adding a New Analyzer

1. Create `analyzers/new_analyzer.py`:
```python
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

@dataclass
class NewFinding:
    # Define finding structure
    pass

class NewAnalyzer:
    def __init__(self, project_root: Path):
        self.root = project_root

    def run(self) -> List[NewFinding]:
        # Implementation
        pass
```

2. Update `runner.py`:
```python
if cfg.use_new:
    new = NewAnalyzer(Path(cfg.path)).run()
    out["new"] = [asdict(n) for n in new]
```

3. Update `config.py` to add analyzer toggle:
```python
@dataclass
class AnalyzersCfg:
    new: bool = False
```

4. Update `sarif.py` to include findings in SARIF output

### Adding a New Command

1. Create `commands/new_command.py`:
```python
import typer
from rich.console import Console

app = typer.Typer(help="Command description")

@app.command("run")
def new_command():
    """Command implementation"""
    console = Console()
    # Implementation
```

2. Register in `cli.py`:
```python
from specify_cli.commands import new_command
app.add_typer(new_command.app, name="new")
```

### Adding a New Reporter

1. Create `reporters/new_format.py`:
```python
from pathlib import Path
from typing import List, Dict

def write_new_format(
    code_findings: List[Dict],
    dep_findings: List[Dict],
    out_path: Path
) -> Path:
    # Generate output
    out_path.write_text(content)
    return out_path
```

2. Update `commands/audit.py`:
```python
elif eff_output.lower() == "newformat":
    out = write_new_format(code_findings, dep_findings, out_dir / "report.new")
    console.print(f"[green]New format written:[/green] {out}")
```

## Testing

Run tests from project root:
```bash
pytest tests/
pytest tests/test_cli.py -v
pytest --cov=src/specify_cli --cov-report=html
```

## Code Quality

This codebase follows these standards:
- ✅ Type hints on all public functions
- ✅ Docstrings for public APIs
- ✅ dataclasses for structured data
- ✅ Proper error handling with logging
- ✅ pathlib.Path instead of string paths
- ✅ Black formatting (100 char line length)
- ✅ Ruff linting

Run quality checks:
```bash
black src/
ruff check src/
mypy src/
```

## Security

Security considerations:
- All HTML output uses `html.escape()` to prevent XSS
- No SQL injection vectors (no SQL usage)
- Command execution uses `shlex.split()` for safety
- Explicit error handling (no silent failures)
- Input validation on user-provided paths

## Performance

Performance characteristics:
- Bandit: ~1-5 seconds for typical projects
- Safety: ~2-10 seconds depending on manifest size
- Can scan ~10,000 LOC in under 10 seconds
- Parallel execution of analyzers possible (future enhancement)

## Architecture

See `../docs/architecture.md` (to be created) for detailed system architecture documentation.
