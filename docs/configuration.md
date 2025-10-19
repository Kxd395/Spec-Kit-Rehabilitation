# Configuration Reference for .speckit.toml

This document explains every option in `.speckit.toml` with examples and use cases.

## Quick Start

Create `.speckit.toml` in your repository root:

```toml
[security]
severity_threshold = "MEDIUM"

[ci]
fail_on_severity = "HIGH"
```

That's it! Spec-Kit will now fail CI builds only when HIGH or CRITICAL findings are detected.

---

## Complete Configuration Reference

### `[scan]` - File Scanning

Controls which files are analyzed.

```toml
[scan]
includes = ["src/**/*.py", "tests/**/*.py"]
excludes = ["**/migrations/**", "**/__pycache__/**"]
changed_only = false
```

**Options:**

- `includes` (list): Glob patterns for files to scan
  - Default: `["**/*.py"]`
  - Example: `["src/**/*.py", "lib/**/*.py"]`

- `excludes` (list): Glob patterns for files to skip
  - Default: `[]`
  - Common: `["**/migrations/**", "**/venv/**", "**/.git/**"]`

- `changed_only` (bool): Only scan files changed in git
  - Default: `false`
  - Use `true` for faster PR checks

**Use Cases:**

```toml
# Monorepo: scan multiple packages
includes = ["packages/api/**/*.py", "packages/worker/**/*.py"]

# Skip generated code
excludes = ["**/*_pb2.py", "**/generated/**"]

# Fast PR mode
changed_only = true
```

---

### `[security]` - Security Scanning

Controls security analysis behavior.

```toml
[security]
severity_threshold = "MEDIUM"
allow = []
deny = ["B602", "B603"]
bandit_enabled = true
safety_enabled = true
secrets_enabled = true
```

**Options:**

- `severity_threshold` (string): Minimum severity to report
  - Values: `"LOW"`, `"MEDIUM"`, `"HIGH"`, `"CRITICAL"`
  - Default: `"MEDIUM"`
  - Lower values = more findings reported

- `allow` (list): Rule IDs to suppress (won't be reported)
  - Default: `[]`
  - Example: `["B101", "B601"]` (suppress assert and shell exec)

- `deny` (list): Rule IDs to always report (even if below threshold)
  - Default: `[]`
  - Example: `["B602"]` (always report shell=True)

- `bandit_enabled` (bool): Enable Bandit security scanner
  - Default: `true`

- `safety_enabled` (bool): Enable Safety CVE scanner
  - Default: `true`

- `secrets_enabled` (bool): Enable secrets detection
  - Default: `true`

**Use Cases:**

```toml
# Strict security for production
severity_threshold = "LOW"
deny = ["B602", "B603", "B605"]  # Always report shell commands

# Allow test assertions
allow = ["B101"]

# Disable expensive scanners
safety_enabled = false
```

---

### `[dependencies]` - Dependency Scanning

Controls package vulnerability scanning.

```toml
[dependencies]
manager = "pip"
fail_on = "HIGH"
check_outdated = true
```

**Options:**

- `manager` (string): Package manager to use
  - Values: `"pip"`, `"poetry"`, `"pipenv"`
  - Default: `"pip"`

- `fail_on` (string): Severity level that causes exit 1
  - Values: `"LOW"`, `"MEDIUM"`, `"HIGH"`, `"CRITICAL"`
  - Default: `"HIGH"`

- `check_outdated` (bool): Check for outdated packages
  - Default: `true`

**Use Cases:**

```toml
# Poetry project
manager = "poetry"

# Strict CVE enforcement
fail_on = "MEDIUM"

# Skip outdated checks (faster scans)
check_outdated = false
```

---

### `[quality]` - Code Quality

Controls quality analysis thresholds.

```toml
[quality]
complexity_threshold = 10
maintainability_threshold = 20
max_function_lines = 50
max_nesting_depth = 4
radon_enabled = true
duplication_enabled = false
```

**Options:**

- `complexity_threshold` (int): Maximum cyclomatic complexity
  - Default: `10`
  - Recommended: 10 (simple), 20 (complex), 50 (very complex)

- `maintainability_threshold` (int): Minimum maintainability index (0-100)
  - Default: `20`
  - Higher = more maintainable

- `max_function_lines` (int): Maximum lines per function
  - Default: `50`

- `max_nesting_depth` (int): Maximum control flow nesting
  - Default: `4`

- `radon_enabled` (bool): Enable Radon quality scanner
  - Default: `true`

- `duplication_enabled` (bool): Enable duplicate code detection
  - Default: `false` (experimental)

**Use Cases:**

```toml
# Strict quality standards
complexity_threshold = 5
max_function_lines = 30
max_nesting_depth = 3

# Lenient for legacy code
complexity_threshold = 20
maintainability_threshold = 10
```

---

### `[secrets]` - Secrets Detection

Controls secrets scanning sensitivity.

```toml
[secrets]
entropy_threshold = 4.5
allowlist_patterns = ["EXAMPLE_.*", "FAKE_.*", "TEST_.*"]
```

**Options:**

- `entropy_threshold` (float): Minimum entropy for high-entropy strings
  - Range: `0.0` to `8.0`
  - Default: `4.5`
  - Higher = fewer false positives

- `allowlist_patterns` (list): Regex patterns to ignore
  - Default: `["EXAMPLE_.*", "FAKE_.*", "TEST_.*"]`

**Use Cases:**

```toml
# Sensitive: catch more potential secrets
entropy_threshold = 3.5

# Ignore test fixtures
allowlist_patterns = [
    "EXAMPLE_.*",
    "FAKE_.*",
    "TEST_KEY_.*",
    "sk_test_.*",  # Stripe test keys
]
```

---

### `[report]` - Report Generation

Controls output formats and content.

```toml
[report]
formats = ["markdown", "json"]
out_dir = ".speckit/analysis"
include_snippets = true
group_by_severity = true
```

**Options:**

- `formats` (list): Output formats to generate
  - Values: `"markdown"`, `"json"`, `"sarif"`, `"html"`
  - Default: `["markdown"]`

- `out_dir` (string): Directory for output files
  - Default: `".speckit/analysis"`

- `include_snippets` (bool): Include code snippets in reports
  - Default: `true`

- `group_by_severity` (bool): Group findings by severity in output
  - Default: `true`

**Use Cases:**

```toml
# CI: generate SARIF for GitHub
formats = ["sarif", "markdown"]

# Stakeholder reports
formats = ["html", "markdown"]
include_snippets = false

# Machine-readable only
formats = ["json", "sarif"]
```

---

### `[baseline]` - Baseline Management

Controls suppression of known findings.

```toml
[baseline]
file = ".speckit/baseline.json"
respect_baseline = true
respect_inline_suppressions = true
```

**Options:**

- `file` (string): Path to baseline file
  - Default: `".speckit/baseline.json"`

- `respect_baseline` (bool): Suppress baselined findings
  - Default: `true`

- `respect_inline_suppressions` (bool): Honor inline comments
  - Default: `true`

**Inline Suppression Examples:**

```python
# speckit: ignore-line
dangerous_code()

# speckit: ignore=B602 reason=validated input
subprocess.call(cmd, shell=True)

# speckit: ignore=B101,B102
assert condition
```

**Use Cases:**

```toml
# Adoption mode: suppress all existing issues
respect_baseline = true

# Enforce everything (ignore baseline)
respect_baseline = false

# Disable inline suppressions
respect_inline_suppressions = false
```

---

### `[performance]` - Performance Tuning

Controls scan performance and caching.

```toml
[performance]
max_workers = 4
warm_cache = true
cache_dir = ".speckit/cache"
```

**Options:**

- `max_workers` (int): Maximum parallel workers
  - Default: `4`
  - Recommended: Number of CPU cores

- `warm_cache` (bool): Enable file hash caching
  - Default: `true`

- `cache_dir` (string): Cache directory path
  - Default: `".speckit/cache"`

**Use Cases:**

```toml
# Fast CI: maximize parallelism
max_workers = 8

# Disable caching for clean runs
warm_cache = false

# Custom cache location
cache_dir = "/tmp/speckit-cache"
```

---

### `[ci]` - CI/CD Integration

Controls CI build behavior.

```toml
[ci]
fail_on_severity = "HIGH"
max_findings = -1
pr_mode = false
```

**Options:**

- `fail_on_severity` (string): Exit 1 on this severity or higher
  - Values: `"LOW"`, `"MEDIUM"`, `"HIGH"`, `"CRITICAL"`
  - Default: `"HIGH"`

- `max_findings` (int): Maximum allowed findings
  - Default: `-1` (unlimited)
  - Use `0` to fail on any finding

- `pr_mode` (bool): Optimize for pull request checks
  - Default: `false`
  - Enables `changed_only`, faster reporting

**Use Cases:**

```toml
# Strict: no findings allowed
fail_on_severity = "LOW"
max_findings = 0

# Production branch: high bar
fail_on_severity = "HIGH"

# PR checks: fast feedback
pr_mode = true
```

---

### `[telemetry]` - Telemetry

Controls anonymous usage statistics.

```toml
[telemetry]
enabled = false
anonymous = true
```

**Options:**

- `enabled` (bool): Enable telemetry
  - Default: `false`

- `anonymous` (bool): Anonymize data
  - Default: `true`

**Environment Variable:**

```bash
SPECKIT_TELEMETRY=1  # Enable
SPECKIT_TELEMETRY=0  # Disable (default)
```

---

## Environment Variable Overrides

These environment variables override config file settings:

| Variable | Overrides | Example |
|----------|-----------|---------|
| `SPECKIT_SEVERITY_THRESHOLD` | `security.severity_threshold` | `MEDIUM` |
| `SPECKIT_FAIL_ON_SEVERITY` | `ci.fail_on_severity` | `HIGH` |
| `SPECKIT_MAX_FINDINGS` | `ci.max_findings` | `10` |
| `SPECKIT_TELEMETRY` | `telemetry.enabled` | `1` or `0` |

**Example:**

```bash
SPECKIT_FAIL_ON_SEVERITY=CRITICAL specify audit .
```

---

## CLI Flag Overrides

CLI flags take precedence over both config and environment variables:

```bash
specify audit . \
  --config custom.toml \
  --fail-on-severity HIGH \
  --max-findings 5 \
  --output sarif \
  --output markdown
```

**Precedence Order:**
1. CLI flags (highest)
2. Environment variables
3. Config file
4. Defaults (lowest)

---

## Real-World Examples

### Startup: Fast iteration

```toml
[security]
severity_threshold = "HIGH"

[ci]
fail_on_severity = "CRITICAL"
pr_mode = true

[performance]
max_workers = 8
```

### Enterprise: Comprehensive scanning

```toml
[security]
severity_threshold = "LOW"
deny = ["B602", "B603", "B605"]

[dependencies]
fail_on = "MEDIUM"

[quality]
complexity_threshold = 10
max_function_lines = 50

[ci]
fail_on_severity = "MEDIUM"
max_findings = 0

[report]
formats = ["sarif", "html", "json"]
```

### Legacy codebase: Gradual adoption

```toml
[security]
severity_threshold = "MEDIUM"

[baseline]
respect_baseline = true
respect_inline_suppressions = true

[ci]
fail_on_severity = "HIGH"
max_findings = -1
```

### Open source: Public transparency

```toml
[security]
severity_threshold = "MEDIUM"

[report]
formats = ["markdown", "sarif"]
include_snippets = true

[ci]
fail_on_severity = "HIGH"
```

---

## Validation

Spec-Kit validates your config on load. Common errors:

**Invalid severity:**
```
Error: Invalid severity 'SUPER_HIGH'. Use: LOW, MEDIUM, HIGH, CRITICAL
```

**Invalid format:**
```
Error: Invalid report format 'pdf'. Use: markdown, json, sarif, html
```

**Missing file:**
```
Warning: Baseline file '.speckit/baseline.json' not found. Creating new baseline.
```

---

## Next Steps

- See [CI Integration Guide](ci_examples.md) for GitHub Actions examples
- See [Baseline Management](baseline.md) for adoption workflows
- See [Triage Guide](triage.md) for false positive handling

---

**Generated from:** Spec-Kit v0.1.0  
**Schema version:** 1.0  
**Last updated:** October 18, 2025
