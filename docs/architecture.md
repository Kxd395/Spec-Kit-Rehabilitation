# Architecture

## Overview

Spec-Kit is organized into modular components for extensibility and maintainability.

## Key Modules

### analyzers/

Tool wrappers that emit normalized dataclass findings.

- `bandit_analyzer.py` - Python code security scanner
- `safety_analyzer.py` - Dependency vulnerability scanner

Each analyzer:
- Returns a list of dataclass findings
- Provides `run()` method
- Supports conversion to dictionaries via `asdict()`

### reporters/

Output formatters for analysis results.

- `sarif.py` - SARIF 2.1.0 writer (GitHub Code Scanning compatible)
- `html.py` - HTML report generator (XSS-safe)

All reporters:
- Accept findings as dictionaries
- Write to specified output paths
- Return the path to the generated file

### commands/

Typer CLI entry points.

- `audit.py` - Main security analysis command
- `doctor.py` - Environment validation command

Commands handle:
- Argument parsing
- Configuration merging (file + ENV + CLI)
- Orchestration
- Exit code management

### Core Modules

- **config.py** - TOML + ENV + CLI configuration merger
- **runner.py** - Orchestrates multiple analyzers
- **baseline.py** - Fingerprinting and finding filtration
- **cli.py** - Bootstrap entry point
- **gitutils.py** - Git integration for changed files

## Data Flow

```
1. audit command loads config
   ├── TOML file (.speckit.toml)
   ├── Environment variables (SPECKIT_*)
   └── CLI arguments (highest priority)

2. runner executes analyzers
   ├── BanditAnalyzer.run() → List[BanditFinding]
   └── SafetyAnalyzer.run() → List[SafetyFinding]

3. baseline filters code findings (if enabled)
   ├── load_baseline() → baseline fingerprints
   └── filter_with_baseline() → filtered findings

4. reporters write output
   ├── SARIF → .speckit/analysis/report.sarif
   ├── HTML → .speckit/analysis/report.html
   └── JSON → .speckit/analysis/analysis.json

5. exit code reflects severity gate
   ├── 0 = No gated findings
   ├── 1 = Findings at or above threshold
   └── 2 = Missing analyzers (strict mode)
```

## Extensibility

### Adding a New Analyzer

1. Create `src/specify_cli/analyzers/your_analyzer.py`
2. Define a dataclass for findings:

```python
from dataclasses import dataclass, asdict

@dataclass
class YourFinding:
    rule_id: str
    severity: str
    file_path: str
    line: int
    message: str

    def to_dict(self):
        return asdict(self)
```

3. Implement the analyzer class:

```python
class YourAnalyzer:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def run(self) -> list[YourFinding]:
        # Implement tool execution and parsing
        return findings
```

4. Wire into `runner.py`:

```python
if config.use_your_tool:
    analyzer = YourAnalyzer(path)
    results["your_tool"] = [f.to_dict() for f in analyzer.run()]
```

5. Update SARIF/HTML reporters to handle new finding types

### Adding a New Reporter

1. Create `src/specify_cli/reporters/your_reporter.py`
2. Implement writer function:

```python
def write_your_format(
    code_findings: list[dict],
    dep_findings: list[dict],
    output_path: Path
) -> Path:
    # Generate output
    output_path.write_text(content)
    return output_path
```

3. Wire into `audit.py` command:

```python
elif eff_output.lower() == "yourformat":
    out = write_your_format(code_findings, dep_findings, out_dir / "report.ext")
    console.print(f"[green]Your format written:[/green] {out}")
```

## Configuration Precedence

Configuration values are resolved in this order (highest to lowest priority):

1. **CLI arguments** - `--fail-on HIGH`
2. **Environment variables** - `export SPECKIT_FAIL_ON=HIGH`
3. **TOML file** - `.speckit.toml` in repository root
4. **Defaults** - Hardcoded fallbacks

Example:
```python
# If user runs: specify audit --fail-on HIGH
# And .speckit.toml has: fail_on = "MEDIUM"
# And ENV has: SPECKIT_FAIL_ON=LOW
# Result: HIGH (CLI wins)
```

## Security Considerations

### XSS Prevention

All dynamic content in HTML reports is escaped using `html.escape()`:

```python
def _e(v):
    return html.escape("" if v is None else str(v), quote=True)
```

### Command Injection Prevention

No shell execution with user input. All subprocess calls use list syntax:

```python
# GOOD
subprocess.run(["bandit", "-r", str(path)])

# NEVER
subprocess.run(f"bandit -r {path}", shell=True)  # Vulnerable!
```

### Path Traversal Prevention

All paths use `pathlib.Path` and are resolved relative to repository root.

## Performance Characteristics

- **Bandit**: O(n) where n = lines of Python code
- **Safety**: O(n) where n = dependencies in manifest
- **Baseline filtering**: O(n log n) for fingerprint matching
- **SARIF generation**: O(n) where n = total findings

Typical runtimes:
- Small project (1K LOC, 20 deps): ~2-5 seconds
- Medium project (10K LOC, 100 deps): ~10-30 seconds
- Large project (100K LOC, 500 deps): ~60-180 seconds

## Testing Strategy

- **Unit tests**: Test individual analyzers, reporters, config loading
- **Integration tests**: Test full audit flow with temp directories
- **Security tests**: Verify XSS prevention, error handling, excludes
- **Acceptance tests**: Test exit code gating with real findings

Run tests:
```bash
pytest --cov=src --cov-report=term-missing
```
