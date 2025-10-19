# Security Analyzers

This directory contains the security scanner implementations that power `specify audit`.

## Available Analyzers

### 1. Bandit Analyzer (`bandit_analyzer.py`)

**Purpose**: Scans Python source code for common security issues

**Features**:
- AST-based static analysis
- 40+ built-in security rules
- CWE mapping
- Exclude pattern support (`.venv/**`, `build/**`, etc.)
- Confidence and severity ratings

**Example Usage**:
```python
from specify_cli.analyzers.bandit_analyzer import BanditAnalyzer
from pathlib import Path

analyzer = BanditAnalyzer(
    target=Path("./src"),
    exclude_globs=[".venv/**", "build/**", "*.pyc"]
)
findings = analyzer.run()  # Returns List[BanditFinding]
```

**Finding Structure**:
```python
@dataclass
class BanditFinding:
    file_path: str      # Relative path to file
    line: int           # Line number
    rule_id: str        # e.g., "B201"
    severity: str       # HIGH/MEDIUM/LOW
    confidence: str     # HIGH/MEDIUM/LOW
    message: str        # Description of issue
    cwe: int | None     # CWE ID if available
```

**Common Issues Detected**:
- Hardcoded passwords/secrets
- SQL injection vulnerabilities
- Command injection risks
- Insecure deserialization
- Weak cryptography
- Path traversal issues
- XSS vulnerabilities in templates

---

### 2. Safety Analyzer (`safety_analyzer.py`)

**Purpose**: Scans Python dependencies for known CVEs and security advisories

**Features**:
- Manifest file detection (6 formats supported)
- CVE database lookup
- Advisory ID tracking
- Fix version recommendations
- Explicit error handling (no silent failures)

**Supported Manifest Files** (in priority order):
1. `requirements.txt`
2. `requirements-dev.txt`
3. `requirements.in`
4. `poetry.lock`
5. `Pipfile.lock`
6. `pyproject.toml`

**Example Usage**:
```python
from specify_cli.analyzers.safety_analyzer import SafetyAnalyzer
from pathlib import Path

analyzer = SafetyAnalyzer(project_root=Path("."))
findings = analyzer.run()  # Returns List[SafetyFinding]
```

**Finding Structure**:
```python
@dataclass
class SafetyFinding:
    package: str              # Package name
    installed_version: str    # Current version
    advisory_id: str          # Safety advisory ID
    cve: Optional[str]        # CVE ID if available
    severity: str             # HIGH/MEDIUM/LOW
    vulnerable_spec: str      # Affected version range
    fix_version: Optional[str]  # Recommended fix version
```

**How It Works**:
1. Searches for manifest files in project root
2. Runs `safety scan --json --file <manifest>` (or legacy `safety check`)
3. Parses JSON output
4. Normalizes findings across Safety API versions
5. Returns structured findings with fix recommendations

**Error Handling**:
- ❌ Safety CLI missing → Raises `FileNotFoundError`
- ❌ Invalid JSON response → Raises `json.JSONDecodeError`
- ❌ Non-zero exit code (other than 1) → Raises `subprocess.CalledProcessError`
- ⚠️ No manifest found → Warns and scans current environment

---

## Architecture

### Analyzer Interface

All analyzers follow this pattern:

```python
class Analyzer:
    def __init__(self, project_root: Path, **options):
        """Initialize analyzer with project root and options"""
        pass
    
    def run(self) -> List[Finding]:
        """Execute analysis and return findings"""
        pass
```

### Finding Dataclasses

All findings use `@dataclass` for type safety and easy serialization:

```python
from dataclasses import dataclass, asdict

finding = BanditFinding(...)
dict_form = asdict(finding)  # For JSON serialization
```

### Integration with Runner

The `runner.py` module orchestrates multiple analyzers:

```python
# runner.py
def run_all(cfg: RunConfig) -> Dict[str, List[dict]]:
    out = {}
    if cfg.use_bandit:
        bandit = BanditAnalyzer(cfg.path, exclude_globs=cfg.exclude_globs).run()
        out["bandit"] = [asdict(b) for b in bandit]
    if cfg.use_safety:
        safety = SafetyAnalyzer(cfg.path).run()
        out["safety"] = [asdict(s) for s in safety]
    return out
```

---

## Adding a New Analyzer

### Step 1: Create Analyzer File

Create `analyzers/new_analyzer.py`:

```python
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List
from specify_cli.logging import get_logger

log = get_logger(__name__)

@dataclass
class NewFinding:
    """Finding structure"""
    file_path: str
    line: int
    rule_id: str
    severity: str
    message: str

class NewAnalyzer:
    """New analyzer implementation"""
    
    def __init__(self, project_root: Path, **options):
        self.root = Path(project_root)
        # Store options
    
    def run(self) -> List[NewFinding]:
        """Run analysis"""
        findings = []
        # Implementation
        return findings
```

### Step 2: Update Runner

Add to `runner.py`:

```python
from specify_cli.analyzers.new_analyzer import NewAnalyzer

@dataclass
class RunConfig:
    use_new: bool = True  # Add toggle

def run_all(cfg: RunConfig) -> Dict[str, List[dict]]:
    if cfg.use_new:
        new = NewAnalyzer(cfg.path).run()
        out["new"] = [asdict(n) for n in new]
```

### Step 3: Update Config

Add to `config.py`:

```python
@dataclass
class AnalyzersCfg:
    new: bool = True  # Add toggle
```

### Step 4: Update Reporter

Add to `reporters/sarif.py` (and others):

```python
def combine_to_sarif(..., new_findings: List[dict]) -> Dict:
    # Add new_findings to SARIF output
```

### Step 5: Update Command

Add to `commands/audit.py`:

```python
def audit(..., new: bool = typer.Option(None, "--new/--no-new")):
    use_new = cfg.analyzers.new if new is None else new
    results = run_all(RunConfig(..., use_new=use_new))
    new_findings = results.get("new", [])
```

### Step 6: Write Tests

Create `tests/test_new_integration.py`:

```python
from specify_cli.analyzers.new_analyzer import NewAnalyzer

def test_new_analyzer_detects_issues(tmp_path):
    # Create test case
    (tmp_path / "test.py").write_text("...")
    analyzer = NewAnalyzer(tmp_path)
    findings = analyzer.run()
    assert len(findings) > 0
```

---

## Testing

### Unit Tests

Test individual analyzers:

```bash
pytest tests/test_bandit_integration.py -v
pytest tests/ -k "analyzer" -v
```

### Integration Tests

Test analyzer orchestration:

```bash
pytest tests/acceptance/test_exit_code_thresholds.py -v
```

### Coverage

Check analyzer test coverage:

```bash
pytest --cov=src/specify_cli/analyzers --cov-report=html
open htmlcov/index.html
```

---

## Performance Considerations

### Bandit Performance
- Typical scan: 1-5 seconds for 10,000 LOC
- Memory usage: ~50-100MB
- Scales linearly with code size
- Can be optimized with exclude patterns

### Safety Performance
- Typical scan: 2-10 seconds
- Depends on manifest size and network latency
- API rate limits may apply
- Cache results when possible

### Optimization Tips

1. **Use Exclude Patterns**:
   ```python
   analyzer = BanditAnalyzer(
       target=path,
       exclude_globs=[".venv/**", "build/**", "tests/**"]
   )
   ```

2. **Parallel Execution** (future):
   ```python
   import concurrent.futures
   
   with concurrent.futures.ThreadPoolExecutor() as executor:
       bandit_future = executor.submit(bandit.run)
       safety_future = executor.submit(safety.run)
       results = {
           "bandit": bandit_future.result(),
           "safety": safety_future.result()
       }
   ```

3. **Incremental Analysis**:
   ```python
   # Only scan changed files
   from specify_cli.gitutils import changed_python_files
   changed = changed_python_files(repo_root)
   # Filter findings to changed files only
   ```

---

## Security Considerations

### False Positives

Analyzers may report false positives. Use:

1. **Baseline Filtering**: Accept current issues, catch new ones
2. **Inline Suppression**: `# nosec` for Bandit
3. **Exclude Patterns**: Skip test files, generated code

### False Negatives

Static analysis has limitations:
- Runtime-only issues not detected
- Complex data flows may be missed
- Third-party library internals not scanned

**Recommendation**: Use multiple analyzers and manual code review.

### Data Privacy

- Analyzers run locally (no data sent to cloud)
- Safety queries PyPI/Safety DB (package names only)
- No source code uploaded

---

## Dependencies

### Bandit
- `bandit[toml]>=1.7.8`
- Python 3.11+
- No external API calls

### Safety
- `safety>=3.2.4` (Python package)
- `safety` CLI tool (separate installation)
- Requires network access for CVE database

### Installation

```bash
# Install all analyzers
pip install -e ".[analysis]"

# Verify installation
specify doctor run
```

---

## Troubleshooting

### Bandit Not Found

**Error**: `BANDIT_AVAILABLE = False`

**Solution**:
```bash
pip install bandit[toml]
```

### Safety CLI Missing

**Error**: `FileNotFoundError: safety CLI not found`

**Solution**:
```bash
pip install safety
# Verify
which safety
safety --version
```

### Safety API Errors

**Error**: `Failed to parse safety JSON output`

**Causes**:
- Network timeout
- Invalid manifest file
- Safety API changes

**Solution**:
```bash
# Test safety directly
safety scan --json --file requirements.txt
# Or legacy
safety check --json --file requirements.txt
```

### Exclude Patterns Not Working

**Issue**: `.venv` files still scanned

**Solution**: Use glob patterns with `**`:
```python
exclude_globs=[".venv/**", "**/__pycache__/**"]
```

---

## References

- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Safety Documentation](https://docs.pyupio.com/docs/safety-cli)
- [OWASP Security Scanning](https://owasp.org/www-community/controls/Static_Code_Analysis)
- [CWE Database](https://cwe.mitre.org/)
- [CVE Database](https://cve.mitre.org/)

---

*Last Updated: October 18, 2025*
