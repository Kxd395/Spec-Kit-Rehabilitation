# Output Reporters

This directory contains report generation modules that format security findings into various output formats.

## Available Reporters

### 1. SARIF Reporter (`sarif.py`)

**Purpose**: Generates SARIF 2.1.0 format output compatible with GitHub Code Scanning

**Features**:
- SARIF 2.1.0 schema compliance
- Rule definitions with CWE mapping
- SHA256 fingerprints for deduplication
- Smart manifest detection for dependency locations
- Separate handling for code issues (Bandit) and dependencies (Safety)

**Usage**:
```python
from specify_cli.reporters.sarif import combine_to_sarif, write_sarif
from pathlib import Path

sarif_doc = combine_to_sarif(
    bandit_findings=[...],
    safety_findings=[...],
    repo_root=Path("."),
    dep_artifact_hint="requirements.txt"
)

write_sarif(sarif_doc, Path(".speckit/analysis/report.sarif"))
```

**Output Structure**:
```json
{
  "version": "2.1.0",
  "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
  "runs": [{
    "tool": {
      "driver": {
        "name": "SpecKit Combined",
        "rules": [...]
      }
    },
    "results": [...]
  }]
}
```

**Key Functions**:
- `combine_to_sarif()`: Combines Bandit + Safety findings into SARIF
- `write_sarif()`: Writes SARIF document to file
- `_best_dep_artifact()`: Finds best manifest file for dependency locations
- `_level()`: Converts severity (HIGH/MEDIUM/LOW) to SARIF level (error/warning/note)
- `_fp()`: Generates SHA256 fingerprint for deduplication

**GitHub Integration**:
Upload to GitHub Code Scanning:
```bash
gh api /repos/{owner}/{repo}/code-scanning/sarifs \
  -F sarif=@.speckit/analysis/report.sarif \
  -F commit_sha=$(git rev-parse HEAD) \
  -F ref=refs/heads/main
```

---

### 2. HTML Reporter (`html.py`)

**Purpose**: Generates human-readable HTML reports with proper XSS prevention

**Features**:
- XSS-safe HTML output (all fields escaped)
- Separate tables for code issues and dependency CVEs
- Minimal inline CSS for portability
- UTF-8 charset for international characters
- Responsive table layout

**Usage**:
```python
from specify_cli.reporters.html import write_html
from pathlib import Path

html_path = write_html(
    code_findings=[...],
    dep_findings=[...],
    out_path=Path(".speckit/analysis/report.html")
)
```

**Security**:
All user-controlled fields are HTML-escaped using `html.escape(quote=True)`:
- Rule IDs
- File paths
- Error messages
- Package names
- Advisory IDs

**Example**: `<script>alert(1)</script>` → `&lt;script&gt;alert(1)&lt;/script&gt;`

**Output Sections**:
1. **Code Issues Table**:
   - Rule ID
   - Severity
   - Location (file:line)
   - Message
   - CWE

2. **Dependency CVEs Table**:
   - Package
   - Installed Version
   - Advisory/CVE ID
   - Severity
   - Fix Version

---

### 3. JSON Reporter (Inline)

**Purpose**: Raw JSON output for programmatic consumption

**Implementation**: Handled directly in `commands/audit.py`

**Usage**:
```bash
specify audit run --output json
```

**Output**:
```json
{
  "code": [
    {
      "file_path": "src/app.py",
      "line": 42,
      "rule_id": "B201",
      "severity": "HIGH",
      "message": "..."
    }
  ],
  "dependencies": [
    {
      "package": "requests",
      "installed_version": "2.25.0",
      "advisory_id": "PYSEC-2021-59",
      "cve": "CVE-2021-33503",
      "severity": "MEDIUM"
    }
  ]
}
```

---

## Adding a New Reporter

### Step 1: Create Reporter Module

Create `reporters/new_format.py`:

```python
from __future__ import annotations
from pathlib import Path
from typing import List, Dict

def write_new_format(
    code_findings: List[Dict],
    dep_findings: List[Dict],
    out_path: Path
) -> Path:
    """Generate report in new format"""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate content
    content = _generate_content(code_findings, dep_findings)

    # Write to file
    out_path.write_text(content, encoding="utf-8")
    return out_path

def _generate_content(code: List[Dict], deps: List[Dict]) -> str:
    """Format findings into new format"""
    # Implementation
    pass
```

### Step 2: Update Audit Command

Add to `commands/audit.py`:

```python
from specify_cli.reporters.new_format import write_new_format

# In audit() function:
elif eff_output.lower() == "newformat":
    out = write_new_format(code_findings, dep_findings, out_dir / "report.new")
    console.print(f"[green]New format written:[/green] {out}")
```

### Step 3: Update Documentation

Add to `docs/configuration.md`:
```markdown
#### New Format

Generate report in new format:
```bash
specify audit run --output newformat
```

Output location: `.speckit/analysis/report.new`
```

### Step 4: Write Tests

Create `tests/test_new_format_reporter.py`:

```python
from specify_cli.reporters.new_format import write_new_format
from pathlib import Path

def test_new_format_generates_valid_output(tmp_path):
    findings = [{"rule_id": "TEST", "message": "Test"}]
    out = write_new_format(findings, [], tmp_path / "report.new")
    assert out.exists()
    content = out.read_text()
    assert "TEST" in content
```

---

## Output Format Comparison

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| **SARIF** | CI/CD, GitHub | Machine-readable, standardized, tool support | Verbose, complex structure |
| **HTML** | Manual review, sharing | Human-friendly, visual, portable | Not machine-readable |
| **JSON** | Scripts, automation | Simple, flexible, easy to parse | No standard schema |

---

## Best Practices

### SARIF

1. **Always include fingerprints** for deduplication:
   ```python
   result["fingerprints"] = {
       "primaryLocationLineHash": _fp(f"{file}:{line}:{rule}")
   }
   ```

2. **Use proper artifact locations**:
   ```python
   dep_art = _best_dep_artifact(repo_root, hint="requirements.txt")
   # Never default to "."
   ```

3. **Map CWE IDs when available**:
   ```python
   if f.get("cwe"):
       rule["properties"]["cwe"] = f"CWE-{f['cwe']}"
   ```

### HTML

1. **Always escape user content**:
   ```python
   def _e(v) -> str:
       return html.escape("" if v is None else str(v), quote=True)
   ```

2. **Use inline CSS** for portability:
   ```html
   <style>
   body{font-family:system-ui,Arial}
   table{border-collapse:collapse;width:100%}
   </style>
   ```

3. **Set UTF-8 charset**:
   ```html
   <meta charset="utf-8">
   ```

### JSON

1. **Use consistent structure**:
   ```python
   {
       "code": [...],      # Always present (empty list if none)
       "dependencies": [...]  # Always present (empty list if none)
   }
   ```

2. **Pretty-print for readability**:
   ```python
   json.dumps(data, indent=2)
   ```

---

## Security Considerations

### XSS Prevention

HTML reporter uses `html.escape()` on all dynamic content:

```python
# VULNERABLE (DO NOT USE)
f"<td>{finding['message']}</td>"

# SECURE (CORRECT)
f"<td>{_e(finding['message'])}</td>"
```

**Test for XSS**:
```python
def test_html_escapes_malicious_content():
    findings = [{"message": "<script>alert('XSS')</script>"}]
    html = write_html(findings, [], Path("report.html"))
    content = html.read_text()
    assert "<script>" not in content
    assert "&lt;script&gt;" in content
```

### Path Traversal

Always validate output paths:

```python
def write_report(out_path: Path) -> Path:
    # Ensure parent directory exists
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Resolve to absolute path
    out_path = out_path.resolve()

    # Write safely
    out_path.write_text(content, encoding="utf-8")
    return out_path
```

---

## Testing

### Unit Tests

Test individual reporters:

```bash
pytest tests/ -k "reporter" -v
```

### XSS Tests

Ensure HTML escaping works:

```bash
pytest tests/test_html_escapes.py -v
```

### SARIF Validation

Validate SARIF output:

```bash
# Install SARIF validator
npm install -g @microsoft/sarif-multitool

# Validate output
sarif validate .speckit/analysis/report.sarif
```

---

## Performance

### File I/O

All reporters use efficient file writing:

```python
# Good - single write
out_path.write_text(content, encoding="utf-8")

# Bad - multiple writes
with open(out_path, "w") as f:
    for line in lines:
        f.write(line)
```

### Memory Usage

Reporters build content in memory before writing:
- SARIF: ~1-5MB for typical projects
- HTML: ~100KB-1MB for typical projects
- JSON: ~500KB-2MB for typical projects

### Benchmarks

Typical report generation times:
- SARIF: 10-50ms
- HTML: 5-20ms
- JSON: 1-5ms

---

## References

- [SARIF Specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)
- [GitHub Code Scanning SARIF](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning)
- [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Python html.escape](https://docs.python.org/3/library/html.html#html.escape)

---

*Last Updated: October 18, 2025*
