# Security Scanning

## Tools

- **Bandit** for Python code issues
- **Safety** for dependency CVEs

## Run

```bash
specify audit run --output sarif --fail-on MEDIUM --strict
```

## Outputs

- `.speckit/analysis/report.sarif` - GitHub Code Scanning compatible
- `.speckit/analysis/report.html` - Human-readable report
- `.speckit/analysis/analysis.json` - Raw JSON output

## Exit Codes

- `0` - No gated findings
- `1` - Findings at or above --fail-on threshold
- `2` - Missing analyzers when --strict is used

## Configuration

Create `.speckit.toml` in your repository root. See `templates/.speckit.toml.example` for all options.

### Example Configuration

```toml
[analysis]
fail_on = "MEDIUM"
respect_baseline = true
changed_only = false

[output]
format = "sarif"
directory = ".speckit/analysis"

[analyzers]
bandit = true
safety = true
secrets = false

[exclude]
paths = [
  ".venv/**",
  "build/**",
  "dist/**"
]
```

## Baselines

Create a baseline once to capture known issues, then enable `respect_baseline` in `.speckit.toml` to filter them from future runs.

```bash
# Create baseline (run once)
specify audit run --output json

# Future runs will filter baseline findings if respect_baseline = true
specify audit run --output sarif
```

## CI Integration

Use the provided GitHub Actions workflow to upload SARIF to GitHub Code Scanning.

### GitHub Actions Workflow

See `.github/workflows/specify-audit.yml` for the complete workflow that:
1. Installs Python and dependencies
2. Runs `specify audit`
3. Uploads SARIF to GitHub Code Scanning

This enables automatic security scanning on pull requests and commits to main.

## Command Options

- `--path` - Directory to analyze (default: current directory)
- `--output` - Output format: `sarif`, `html`, or `json` (default: from config)
- `--fail-on` - Severity threshold: `HIGH`, `MEDIUM`, or `LOW` (default: from config)
- `--strict` - Fail if requested analyzers are unavailable
- `--bandit/--no-bandit` - Enable/disable Bandit analyzer
- `--safety/--no-safety` - Enable/disable Safety analyzer
- `--respect-baseline` - Filter findings present in baseline
- `--changed-only` - Only analyze changed files (Git-aware)

## Best Practices

1. **Run locally before committing** to catch issues early
2. **Use --strict in CI** to ensure consistent analyzer availability
3. **Create baselines** for legacy codebases to track new issues only
4. **Set appropriate fail thresholds** - `MEDIUM` is recommended for most projects
5. **Review SARIF in GitHub** for inline code annotations
