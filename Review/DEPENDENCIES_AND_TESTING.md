# 🔧 COMPLETE DEPENDENCIES & TESTING REQUIREMENTS

**Date:** October 18, 2025  
**Purpose:** Comprehensive list of ALL dependencies and testing tools needed for production

---

## 📦 CORE DEPENDENCIES (Required)

### Current (Already in pyproject.toml)
```toml
dependencies = [
    "typer>=0.9.0",           # CLI framework
    "rich>=13.0.0",            # Terminal formatting
    "httpx>=0.24.0",           # HTTP client (for template downloads)
    "platformdirs",            # Cross-platform paths
    "readchar",                # Interactive input
    "truststore>=0.10.4",      # SSL certificates
    "tomli>=2.0.1; python_version < '3.11'",  # TOML parsing (added)
]
```

### MISSING - Add NOW
```toml
dependencies = [
    # ... existing ...
    "click>=8.1.0",            # Typer dependency, make explicit
    "pydantic>=2.0.0",         # Data validation for findings
    "pathspec>=0.11.0",        # Gitignore-style path matching
]
```

---

## 🔒 SECURITY ANALYSIS (Optional - analysis)

### Current
```toml
[project.optional-dependencies]
analysis = [
    "bandit[toml]>=1.7.5",    # Python security linter
    "safety>=2.3.5",           # Dependency vulnerability scanner
    "radon>=6.0.1",            # Code complexity metrics
    "detect-secrets>=1.4.0",   # Secrets detection
]
```

### RECOMMENDED ADDITIONS
```toml
analysis = [
    # ... existing ...
    "pip-audit>=2.6.0",        # Better than safety, OSSF recommended
    "semgrep>=1.45.0",         # Custom rule engine (powerful!)
    "vulture>=2.10",           # Dead code detection
    "dodgy>=0.2.1",            # Additional secrets patterns
]
```

**Why Add These:**
- `pip-audit`: OSS Foundation backed, better CVE database
- `semgrep`: Custom rules = your differentiator
- `vulture`: Find unused code
- `dodgy`: More secret patterns than detect-secrets

---

## 📊 REPORTING (Optional - reporting)

### NEW Section - Add to pyproject.toml
```toml
[project.optional-dependencies]
reporting = [
    "jinja2>=3.1.0",           # HTML template engine
    "markdown>=3.5.0",         # Rich markdown rendering
    "pygments>=2.17.0",        # Syntax highlighting in HTML
    "tabulate>=0.9.0",         # Nice terminal tables
]
```

**Why:**
- Jinja2: HTML reports for stakeholders
- Pygments: Syntax-highlighted code snippets
- Tabulate: Pretty CLI output

---

## 🧪 TESTING (Optional - dev)

### Current
```toml
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]
```

### CRITICAL ADDITIONS
```toml
dev = [
    # ... existing ...
    
    # Type Checking
    "mypy>=1.7.0",             # Static type checker
    "types-toml>=0.10.0",      # Type stubs for TOML
    "types-jinja2>=2.11.0",    # Type stubs for Jinja2
    
    # Advanced Testing
    "pytest-benchmark>=4.0.0", # Performance benchmarks
    "pytest-timeout>=2.2.0",   # Prevent hanging tests
    "pytest-xdist>=3.5.0",     # Parallel test execution
    "hypothesis>=6.92.0",      # Property-based testing
    
    # Test Utilities
    "faker>=22.0.0",           # Generate test data
    "freezegun>=1.4.0",        # Mock datetime
    
    # Code Quality
    "pre-commit>=3.6.0",       # Git hooks
    "pylint>=3.0.0",           # Additional linting
    "bandit[toml]>=1.7.5",     # Dogfood our own tool
    "coverage[toml]>=7.4.0",   # Coverage with TOML config
    
    # Documentation
    "mkdocs>=1.5.0",           # Documentation site
    "mkdocs-material>=9.5.0",  # Nice theme
]
```

---

## 🔨 BUILD & RELEASE (Optional - build)

### NEW Section
```toml
[project.optional-dependencies]
build = [
    "build>=1.0.0",            # PEP 517 builder
    "twine>=4.0.0",            # PyPI upload
    "wheel>=0.42.0",           # Wheel distribution
    "setuptools>=69.0.0",      # Setup tools
]
```

---

## 📋 COMPLETE pyproject.toml

Here's the FULL recommended pyproject.toml:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "specify-cli"
version = "0.1.0"
description = "Spec-Driven Development with real security and quality analysis"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "Apache-2.0"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["security", "analysis", "cli", "spec-driven", "bandit", "safety"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Quality Assurance",
    "Topic :: Security",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "httpx>=0.24.0",
    "platformdirs",
    "readchar",
    "truststore>=0.10.4",
    "tomli>=2.0.1; python_version < '3.11'",
    "click>=8.1.0",
    "pydantic>=2.0.0",
    "pathspec>=0.11.0",
]

[project.optional-dependencies]
# Security and quality analysis tools
analysis = [
    "bandit[toml]>=1.7.5",
    "safety>=2.3.5",
    "radon>=6.0.1",
    "detect-secrets>=1.4.0",
    "pip-audit>=2.6.0",
    "semgrep>=1.45.0",
    "vulture>=2.10",
    "dodgy>=0.2.1",
]

# Report generation
reporting = [
    "jinja2>=3.1.0",
    "markdown>=3.5.0",
    "pygments>=2.17.0",
    "tabulate>=0.9.0",
]

# Development tools
dev = [
    # Testing
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.0",
    "pytest-benchmark>=4.0.0",
    "pytest-timeout>=2.2.0",
    "pytest-xdist>=3.5.0",
    "hypothesis>=6.92.0",
    
    # Test utilities
    "faker>=22.0.0",
    "freezegun>=1.4.0",
    
    # Code quality
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
    "pylint>=3.0.0",
    "pre-commit>=3.6.0",
    "coverage[toml]>=7.4.0",
    
    # Type stubs
    "types-toml>=0.10.0",
    
    # Documentation
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.5.0",
]

# Build and release
build = [
    "build>=1.0.0",
    "twine>=4.0.0",
    "wheel>=0.42.0",
    "setuptools>=69.0.0",
]

# All optional dependencies
all = [
    "specify-cli[analysis,reporting,dev,build]",
]

[project.urls]
Homepage = "https://github.com/Kxd395/Spec-Kit-Rehabilitation"
Documentation = "https://github.com/Kxd395/Spec-Kit-Rehabilitation/tree/main/docs"
Repository = "https://github.com/Kxd395/Spec-Kit-Rehabilitation"
"Bug Tracker" = "https://github.com/Kxd395/Spec-Kit-Rehabilitation/issues"

[project.scripts]
specify = "specify_cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/specify_cli"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = [
    "--cov=src/specify_cli",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-report=xml",
    "--cov-fail-under=70",
    "--strict-markers",
    "--tb=short",
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
    "slow: Slow running tests",
    "benchmark: Performance benchmarks",
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/site-packages/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]

[tool.black]
line-length = 100
target-version = ['py311', 'py312']
include = '\.pyi?$'
extend-exclude = '''
/(
  \.eggs
  | \.git
  | \.venv
  | build
  | dist
)/
'''

[tool.ruff]
line-length = 100
target-version = "py311"
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by black)
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]  # Imported but unused
"tests/*" = ["S101"]      # Use of assert

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true

[[tool.mypy.overrides]]
module = [
    "bandit.*",
    "safety.*",
    "radon.*",
    "detect_secrets.*",
]
ignore_missing_imports = true

[tool.pylint.main]
py-version = "3.11"

[tool.pylint.messages_control]
disable = [
    "C0111",  # missing-docstring
    "C0103",  # invalid-name
    "R0903",  # too-few-public-methods
]

[tool.bandit]
exclude_dirs = ["tests", ".venv", "venv"]
skips = ["B101"]  # assert_used - OK in tests
```

---

## 🧪 COMPLETE TEST STRUCTURE

### Directory Layout
```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
├── unit/                          # Fast, isolated tests
│   ├── __init__.py
│   ├── test_config.py             # Config loading
│   ├── test_baseline.py           # Baseline management
│   ├── test_sarif.py              # SARIF generation
│   └── test_severity.py           # Severity mapping
├── integration/                   # Component interaction tests
│   ├── __init__.py
│   ├── test_bandit_integration.py
│   ├── test_safety_integration.py
│   ├── test_cli_config.py         # CLI + config
│   └── test_baseline_sarif.py     # Baseline + SARIF
├── acceptance/                    # User-facing behavior
│   ├── __init__.py
│   ├── test_exit_code_thresholds.py  # Already exists
│   ├── test_baseline_workflow.py
│   ├── test_sarif_upload.py
│   └── test_changed_only.py
├── e2e/                           # Full workflow tests
│   ├── __init__.py
│   └── test_full_audit.py         # End-to-end
├── performance/                   # Speed tests
│   ├── __init__.py
│   ├── test_baseline_speed.py
│   └── test_scan_speed.py
└── fixtures/                      # Test data
    ├── vulnerable_code/
    │   ├── sql_injection.py
    │   ├── command_injection.py
    │   ├── hardcoded_secrets.py
    │   └── complex_functions.py
    ├── configs/
    │   ├── strict.toml
    │   ├── lenient.toml
    │   └── invalid.toml
    └── expected_outputs/
        ├── sample.sarif
        └── sample_baseline.json
```

### Critical Test Files to Create

#### tests/conftest.py
```python
"""Shared pytest fixtures."""
import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def tmp_project(tmp_path):
    """Create temporary project structure."""
    (tmp_path / "src").mkdir()
    (tmp_path / ".speckit").mkdir()
    (tmp_path / ".speckit/analysis").mkdir(parents=True)
    return tmp_path

@pytest.fixture
def vulnerable_file(tmp_path):
    """Create file with security issues."""
    code = '''
import subprocess
import os

def run_command(user_input):
    subprocess.call(user_input, shell=True)  # B602

def unsafe_eval(data):
    return eval(data)  # B307
'''
    file_path = tmp_path / "vulnerable.py"
    file_path.write_text(code)
    return file_path

@pytest.fixture
def sample_config(tmp_path):
    """Create sample config file."""
    config = '''
[security]
severity_threshold = "MEDIUM"

[ci]
fail_on_severity = "HIGH"
'''
    config_path = tmp_path / ".speckit.toml"
    config_path.write_text(config)
    return config_path
```

#### tests/unit/test_config.py
```python
"""Unit tests for config module."""
import pytest
from pathlib import Path
from specify_cli.config import (
    load_config,
    get_severity_level,
    should_report_finding,
)

def test_load_default_config():
    """Should create config with defaults."""
    config = load_config(config_path=None, search=False)
    assert config.security.severity_threshold == "MEDIUM"

def test_severity_levels():
    """Should map severities to numbers."""
    assert get_severity_level("LOW") == 0
    assert get_severity_level("HIGH") == 2

def test_should_report_high_severity():
    """Should report findings above threshold."""
    assert should_report_finding("HIGH", "MEDIUM", [], [], "B602")

# Add 7 more tests...
```

---

## 🎯 INSTALLATION CHECKLIST

### For Development
```bash
# Install everything
pip install -e ".[all]"

# Or selectively
pip install -e ".[analysis,reporting,dev]"

# Set up pre-commit
pre-commit install

# Run tests
pytest

# Check types
mypy src/

# Lint
ruff check .
black --check .
```

### For CI/CD
```yaml
# .github/workflows/test.yml
- name: Install dependencies
  run: |
    pip install -e ".[analysis,dev]"
    
- name: Run tests
  run: pytest --cov --cov-report=xml

- name: Type check
  run: mypy src/

- name: Lint
  run: |
    ruff check .
    black --check .
```

---

## 📊 DEPENDENCY COST ANALYSIS

### Installation Size
```
Core only:              ~50 MB
+ analysis:            ~200 MB (semgrep is large)
+ reporting:            ~20 MB
+ dev:                ~100 MB
Total (all):          ~370 MB
```

### Installation Time
```
Core only:              ~10 seconds
+ analysis:            ~60 seconds
+ all:                 ~90 seconds
```

### Why This Is OK
- Users typically install `[analysis]` only
- Dev tools are one-time cost
- Semgrep is optional (can remove if too large)

---

## 🎯 PRIORITY INSTALLATION ORDER

### Week 1 (MVP)
```bash
pip install -e ".[analysis]"
# Gets: bandit, safety, radon, detect-secrets
```

### Week 2 (Testing)
```bash
pip install -e ".[dev]"
# Gets: pytest, coverage, mypy, ruff, black
```

### Week 3 (Reporting)
```bash
pip install -e ".[reporting]"
# Gets: jinja2, markdown, pygments
```

### Production
```bash
pip install specify-cli[analysis,reporting]
# Users don't need dev tools
```

---

## ✅ VALIDATION CHECKLIST

- [ ] All dependencies have minimum versions
- [ ] Type stubs included for mypy
- [ ] Test framework complete (pytest + plugins)
- [ ] Pre-commit hooks configured
- [ ] Coverage thresholds set (70%)
- [ ] CI matrix includes Python 3.11 and 3.12
- [ ] Optional dependencies are truly optional
- [ ] Build tools separate from runtime

---

## 🎯 NEXT STEPS

1. **Update pyproject.toml** with complete dependencies
2. **Create tests/conftest.py** with shared fixtures
3. **Create tests/unit/test_config.py** with 10 tests
4. **Install dev tools**: `pip install -e ".[dev]"`
5. **Run tests**: `pytest -v`
6. **Check coverage**: `pytest --cov`

---

**Bottom Line:**
You need **~30 dependencies total**, organized into 4 groups:
- Core (10): Always installed
- Analysis (8): Security/quality tools
- Reporting (4): HTML/markdown generation
- Dev (30+): Testing/linting/docs

**Install Order:**
1. Analysis (Week 1)
2. Dev (Week 2)
3. Reporting (Week 3)

**Total Cost:** ~370 MB, ~90 seconds install time
