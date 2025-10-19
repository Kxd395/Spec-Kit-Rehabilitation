# Quick Start: Your First Real Analyzer

**Goal:** Get your first working security scanner running THIS WEEKEND

**Time:** 4-6 hours

---

## ✅ What You'll Build

A real Python security scanner that:
- Actually runs Bandit (not just prompts AI)
- Detects real vulnerabilities
- Produces deterministic results
- Has tests that prove it works

---

## 🚀 Step-by-Step Implementation

### **Step 1: Install Dependencies** (10 minutes)

```bash
cd /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit

# Install security tools
pip install bandit[toml] safety radon

# Install for development
pip install -e ".[dev,security]"
```

### **Step 2: Create Vulnerable Test Code** (20 minutes)

Create `tests/fixtures/vulnerable_code/sql_injection.py`:

```python
"""Intentionally vulnerable code for testing security scanner."""

import sqlite3

def vulnerable_query(user_input):
    """SQL Injection vulnerability - BAD CODE!"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # VULNERABLE: String concatenation with user input
    query = "SELECT * FROM users WHERE username = '" + user_input + "'"
    cursor.execute(query)

    return cursor.fetchall()


def another_vulnerability(password):
    """Hardcoded secret - BAD CODE!"""
    # SECURITY VIOLATION: Hardcoded API credentials (example for testing)
    api_key = "EXAMPLE_KEY_abc123def456ghi789jkl"

    if password == "admin123":  # Hardcoded password
        return api_key
    return None


def eval_vulnerability(user_code):
    """Code injection - BAD CODE!"""
    # DANGEROUS: eval with user input
    result = eval(user_code)
    return result
```

Create `tests/fixtures/safe_code/parameterized_query.py`:

```python
"""Safe code examples for comparison."""

import sqlite3

def safe_query(user_input):
    """Parameterized query - SAFE!"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # SAFE: Parameterized query
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (user_input,))

    return cursor.fetchall()


def safe_secrets():
    """Use environment variables - SAFE!"""
    import os
    api_key = os.environ.get('API_KEY')
    return api_key
```

### **Step 3: Create Security Analyzer** (45 minutes)

Create `src/specify_cli/analyzers/__init__.py`:

```python
"""Analysis modules for code scanning."""

from .security import SecurityAnalyzer

__all__ = ['SecurityAnalyzer']
```

Create `src/specify_cli/analyzers/security.py`:

```python
"""Security analysis using Bandit."""

import json
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from bandit.core import manager as bandit_manager
    from bandit.core import config as bandit_config
    BANDIT_AVAILABLE = True
except ImportError:
    BANDIT_AVAILABLE = False


class Severity(str, Enum):
    """Security issue severity levels."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class SecurityIssue:
    """Represents a security vulnerability."""
    file_path: str
    line_number: int
    test_id: str
    issue_type: str
    severity: Severity
    confidence: str
    description: str

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class SecurityAnalyzer:
    """Scans Python code for security vulnerabilities using Bandit."""

    def __init__(self, target_path: Path):
        """
        Initialize security analyzer.

        Args:
            target_path: Path to analyze (file or directory)
        """
        self.target_path = Path(target_path)
        self.issues: List[SecurityIssue] = []

    def scan(self) -> List[SecurityIssue]:
        """
        Run security scan on Python files.

        Returns:
            List of security issues found

        Raises:
            ImportError: If bandit is not installed
        """
        if not BANDIT_AVAILABLE:
            raise ImportError(
                "Bandit not installed. Install with: pip install 'specify-cli[security]'"
            )

        # Configure Bandit
        b_conf = bandit_config.BanditConfig()
        b_mgr = bandit_manager.BanditManager(b_conf, 'file')

        # Find Python files
        if self.target_path.is_file():
            python_files = [self.target_path]
        else:
            python_files = list(self.target_path.rglob("*.py"))
            # Exclude common non-source directories
            python_files = [
                f for f in python_files
                if not any(p in f.parts for p in ['.venv', 'venv', '__pycache__', '.git'])
            ]

        if not python_files:
            return []

        # Run Bandit scan
        b_mgr.discover_files([str(f) for f in python_files])
        b_mgr.run_tests()

        # Convert results to our format
        for result in b_mgr.get_issue_list():
            issue = SecurityIssue(
                file_path=result.fname,
                line_number=result.lineno,
                test_id=result.test_id,
                issue_type=result.test,
                severity=Severity(result.issue_severity),
                confidence=result.issue_confidence,
                description=result.text,
            )
            self.issues.append(issue)

        return self.issues

    def to_json(self) -> str:
        """Export findings as JSON."""
        return json.dumps([issue.to_dict() for issue in self.issues], indent=2)

    def to_markdown(self) -> str:
        """Export findings as Markdown."""
        if not self.issues:
            return "✅ No security issues found.\n"

        md = f"# Security Scan Results\n\n"
        md += f"**Total Issues:** {len(self.issues)}\n\n"

        # Group by severity
        by_severity = {}
        for issue in self.issues:
            severity = issue.severity.value
            by_severity.setdefault(severity, []).append(issue)

        for severity in ['HIGH', 'MEDIUM', 'LOW']:
            issues = by_severity.get(severity, [])
            if not issues:
                continue

            md += f"## {severity} Severity ({len(issues)} issues)\n\n"
            for issue in issues:
                md += f"### {issue.test_id}: {issue.issue_type}\n\n"
                md += f"- **File:** `{issue.file_path}:{issue.line_number}`\n"
                md += f"- **Confidence:** {issue.confidence}\n"
                md += f"- **Description:** {issue.description}\n\n"

        return md

    @property
    def has_issues(self) -> bool:
        """Check if any issues were found."""
        return len(self.issues) > 0

    @property
    def high_severity_count(self) -> int:
        """Count of high severity issues."""
        return sum(1 for i in self.issues if i.severity == Severity.HIGH)
```

### **Step 4: Add CLI Command** (30 minutes)

Add to `src/specify_cli/__init__.py` (before the `main()` function):

```python
@app.command()
def audit(
    path: Path = typer.Argument(
        Path.cwd(),
        help="Path to analyze (file or directory)"
    ),
    output: str = typer.Option(
        "markdown",
        help="Output format: json, markdown"
    ),
    save_report: bool = typer.Option(
        True,
        help="Save report to .speckit/analysis/"
    ),
):
    """
    Run security analysis using real tools (Bandit).

    This command performs actual static analysis, not AI prompts.
    Results are deterministic and reproducible.

    Example:
        specify audit src/
        specify audit myfile.py --output json
    """
    from specify_cli.analyzers.security import SecurityAnalyzer

    console.print(Panel(
        f"[cyan]Security Analysis[/cyan]\n\n"
        f"Target: {path}\n"
        f"Tool: Bandit (Python Security Scanner)",
        title="Analysis Configuration",
        border_style="cyan"
    ))

    # Run security scan
    with console.status("[cyan]Scanning for vulnerabilities..."):
        try:
            analyzer = SecurityAnalyzer(path)
            issues = analyzer.scan()
        except ImportError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Scan failed:[/red] {e}")
            raise typer.Exit(1)

    # Display summary
    if issues:
        high_count = analyzer.high_severity_count
        emoji = "🔴" if high_count > 0 else "🟡"
        console.print(f"\n{emoji} [yellow]Found {len(issues)} security issues[/yellow]")
        console.print(f"   - High severity: {high_count}")
        console.print(f"   - Medium/Low: {len(issues) - high_count}")
    else:
        console.print("\n✅ [green]No security issues found![/green]")

    # Generate report
    if output == "json":
        report_content = analyzer.to_json()
        report_ext = "json"
    else:
        report_content = analyzer.to_markdown()
        report_ext = "md"

    # Save report
    if save_report:
        output_dir = path / ".speckit" / "analysis" if path.is_dir() else Path.cwd() / ".speckit" / "analysis"
        output_dir.mkdir(parents=True, exist_ok=True)

        report_file = output_dir / f"security-report.{report_ext}"
        with open(report_file, 'w') as f:
            f.write(report_content)

        console.print(f"\n📄 Report saved to: [cyan]{report_file}[/cyan]")
    else:
        console.print(f"\n{report_content}")

    # Exit with error code if high severity issues found
    if analyzer.high_severity_count > 0:
        console.print("\n[red]⚠️  High severity issues detected![/red]")
        raise typer.Exit(1)
```

### **Step 5: Write Tests** (45 minutes)

Create `tests/test_security_analyzer.py`:

```python
"""Tests for security analyzer."""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from specify_cli.analyzers.security import SecurityAnalyzer, Severity


class TestSecurityAnalyzer:
    """Test security scanning functionality."""

    @pytest.fixture
    def vulnerable_code_path(self):
        """Path to vulnerable code fixtures."""
        return Path(__file__).parent / "fixtures" / "vulnerable_code"

    @pytest.fixture
    def safe_code_path(self):
        """Path to safe code fixtures."""
        return Path(__file__).parent / "fixtures" / "safe_code"

    def test_detects_sql_injection(self, vulnerable_code_path):
        """Test that SQL injection is detected."""
        sql_file = vulnerable_code_path / "sql_injection.py"

        analyzer = SecurityAnalyzer(sql_file)
        issues = analyzer.scan()

        # Should find SQL injection (B608)
        assert len(issues) > 0
        assert any("B608" in issue.test_id for issue in issues)

    def test_detects_hardcoded_password(self, vulnerable_code_path):
        """Test that hardcoded passwords are detected."""
        sql_file = vulnerable_code_path / "sql_injection.py"

        analyzer = SecurityAnalyzer(sql_file)
        issues = analyzer.scan()

        # Should find hardcoded password (B105 or B106)
        assert any(issue.test_id in ["B105", "B106"] for issue in issues)

    def test_detects_eval_usage(self, vulnerable_code_path):
        """Test that dangerous eval() is detected."""
        sql_file = vulnerable_code_path / "sql_injection.py"

        analyzer = SecurityAnalyzer(sql_file)
        issues = analyzer.scan()

        # Should find eval usage (B307)
        assert any("B307" in issue.test_id for issue in issues)

    def test_safe_code_has_fewer_issues(self, safe_code_path):
        """Test that safe code has no critical issues."""
        safe_file = safe_code_path / "parameterized_query.py"

        analyzer = SecurityAnalyzer(safe_file)
        issues = analyzer.scan()

        # Safe code should have no high severity issues
        high_issues = [i for i in issues if i.severity == Severity.HIGH]
        assert len(high_issues) == 0

    def test_scan_directory(self, vulnerable_code_path):
        """Test scanning entire directory."""
        analyzer = SecurityAnalyzer(vulnerable_code_path)
        issues = analyzer.scan()

        # Should find multiple issues across files
        assert len(issues) > 0

    def test_json_output(self, vulnerable_code_path):
        """Test JSON export."""
        sql_file = vulnerable_code_path / "sql_injection.py"

        analyzer = SecurityAnalyzer(sql_file)
        analyzer.scan()

        json_output = analyzer.to_json()
        assert "test_id" in json_output
        assert "severity" in json_output

    def test_markdown_output(self, vulnerable_code_path):
        """Test Markdown export."""
        sql_file = vulnerable_code_path / "sql_injection.py"

        analyzer = SecurityAnalyzer(sql_file)
        analyzer.scan()

        md_output = analyzer.to_markdown()
        assert "# Security Scan Results" in md_output
        assert "Total Issues" in md_output

    def test_empty_directory_returns_no_issues(self, tmp_path):
        """Test that empty directory returns no issues."""
        analyzer = SecurityAnalyzer(tmp_path)
        issues = analyzer.scan()

        assert len(issues) == 0
        assert not analyzer.has_issues
```

### **Step 6: Test It!** (20 minutes)

```bash
# Run tests
pytest tests/test_security_analyzer.py -v

# Should see output like:
# test_detects_sql_injection PASSED
# test_detects_hardcoded_password PASSED
# test_detects_eval_usage PASSED
# test_safe_code_has_fewer_issues PASSED
# ...

# Try the CLI command
specify audit tests/fixtures/vulnerable_code/

# Should output:
# 🔴 Found 5 security issues
#    - High severity: 2
#    - Medium/Low: 3
#
# 📄 Report saved to: tests/fixtures/vulnerable_code/.speckit/analysis/security-report.md
```

### **Step 7: Verify Results** (10 minutes)

Check the generated report:

```bash
cat tests/fixtures/vulnerable_code/.speckit/analysis/security-report.md
```

You should see REAL findings with:
- Exact line numbers
- Issue IDs (B608, B105, etc.)
- Severity levels
- Descriptions

---

## ✅ Success Criteria

You've succeeded when:

1. ✅ Tests pass with vulnerable code detection
2. ✅ CLI command runs without errors
3. ✅ Report is generated with actual findings
4. ✅ Same code = same results (deterministic!)
5. ✅ You understand how it works

---

## 🎯 What You've Achieved

**Before:**
```
/speckit.audit → AI reads code → maybe finds issues
```

**After:**
```
specify audit → Bandit scans code → guaranteed finds known patterns
```

You now have:
- ✅ Real security scanning
- ✅ Deterministic results
- ✅ Tests that prove it works
- ✅ Foundation for more features

---

## 🚀 Next Steps

1. **Add more vulnerable patterns** to test suite
2. **Integrate Safety** for dependency scanning
3. **Add Radon** for complexity metrics
4. **Create AI integration** that uses real findings

---

## 💡 Key Insight

**The magic is combining tools + AI:**

1. Bandit finds vulnerabilities (deterministic)
2. Save results to file
3. Tell AI: "Review these ACTUAL findings"
4. AI adds context and fix suggestions

You get:
- Reliability of tools
- Intelligence of AI
- Best of both worlds!

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'bandit'"
```bash
pip install bandit[toml]
```

### Tests fail with import errors
```bash
pip install -e ".[dev,security]"
```

### No issues found on vulnerable code
- Check Bandit is actually running
- Verify file paths are correct
- Try running Bandit directly: `bandit tests/fixtures/vulnerable_code/sql_injection.py`

---

## 📊 Comparison

### **Old Way (AI Prompts):**
- ❌ Non-deterministic
- ❌ Misses obvious issues
- ❌ Can't prove it works
- ❌ Not testable

### **New Way (Real Tools):**
- ✅ Same input = same output
- ✅ Catches known patterns reliably
- ✅ Tests prove accuracy
- ✅ CI/CD ready

---

**Congratulations!** You've built your first real code analysis tool. 🎉

Now go ship it! Then come back and add more features from the roadmap.
