# GitHub Actions Integration Guide

This guide shows how to integrate Spec-Kit into your GitHub Actions CI/CD pipeline with SARIF output for native code scanning.

## Quick Setup

Add this workflow to `.github/workflows/spec-kit.yml`:

```yaml
name: Spec-Kit Security Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  security-scan:
    name: Security & Quality Analysis
    runs-on: ubuntu-latest
    
    permissions:
      # Required for uploading SARIF results
      security-events: write
      # Required for PR comments
      pull-requests: write
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          # Fetch full history for changed file detection
          fetch-depth: 0
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install Spec-Kit
        run: |
          pip install --upgrade pip
          pip install specify-cli bandit safety radon
      
      - name: Run Spec-Kit audit
        run: |
          specify audit . \
            --output sarif \
            --output markdown \
            --fail-on-severity HIGH \
            --changed-only
        continue-on-error: true
      
      - name: Upload SARIF results
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: .speckit/analysis/report.sarif
          category: spec-kit
      
      - name: Upload analysis artifacts
        uses: actions/upload-artifact@v4
        with:
          name: spec-kit-reports
          path: .speckit/analysis/
      
      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('.speckit/analysis/report.md', 'utf8');
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🔍 Spec-Kit Analysis Results\n\n${report}`
            });
```

## Configuration

### 1. Enable Code Scanning

In your repository:
1. Go to **Settings** → **Code security and analysis**
2. Enable **Code scanning**
3. The SARIF upload will create alerts automatically

### 2. Configure Thresholds

Create `.speckit.toml` in your repository root:

```toml
[security]
severity_threshold = "MEDIUM"

[ci]
fail_on_severity = "HIGH"
max_findings = -1  # -1 = unlimited
pr_mode = true

[scan]
changed_only = true  # Only scan changed files in PRs
```

### 3. Environment Variables

Set these in your repository secrets if needed:

```yaml
env:
  SPECKIT_SEVERITY_THRESHOLD: HIGH
  SPECKIT_FAIL_ON_SEVERITY: HIGH
  SPECKIT_TELEMETRY: 0
```

## Advanced Examples

### Scan Only Changed Files in PRs

```yaml
- name: Run Spec-Kit on changed files
  if: github.event_name == 'pull_request'
  run: |
    specify audit . \
      --changed-only \
      --fail-on-severity HIGH
```

### Create Baseline on Main Branch

```yaml
- name: Create baseline
  if: github.ref == 'refs/heads/main'
  run: |
    specify baseline create --output .speckit/baseline.json
    
- name: Commit baseline
  uses: stefanzweifel/git-auto-commit-action@v5
  with:
    commit_message: "chore: update security baseline"
    file_pattern: .speckit/baseline.json
```

### Respect Existing Baseline

```yaml
- name: Run audit with baseline
  run: |
    specify audit . \
      --respect-baseline \
      --fail-on-new-findings
```

### Generate Multiple Report Formats

```yaml
- name: Run comprehensive audit
  run: |
    specify audit . \
      --output sarif \
      --output json \
      --output html \
      --output markdown
```

### Matrix Testing Across Python Versions

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
        os: [ubuntu-latest, macos-latest, windows-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Run Spec-Kit
        run: specify audit .
```

## SARIF Benefits

When you upload SARIF to GitHub:

✅ **PR Annotations**: Findings appear as inline comments  
✅ **Security Dashboard**: Centralized view of all issues  
✅ **Trend Analysis**: Track findings over time  
✅ **Filtering**: Filter by severity, rule, file  
✅ **Dismissal**: Mark false positives  

## Viewing Results

### Code Scanning Alerts
1. Go to **Security** → **Code scanning**
2. View all findings by severity
3. Click findings to see details and remediation

### PR Annotations
- Findings appear inline on changed lines
- Click "Show more details" for full context
- Dismiss false positives directly

### Artifacts
- Download full reports from Actions artifacts
- HTML report for sharing with non-technical stakeholders

## Exit Codes

Spec-Kit uses these exit codes for CI:

- **0**: Success (no findings above threshold)
- **1**: Failure (findings exceed threshold or max count)
- **2**: Error (configuration or runtime error)

## Troubleshooting

### SARIF Upload Fails

**Problem**: `Error: Advanced Security must be enabled`

**Solution**: Enable GitHub Advanced Security or use free public repo features

### No PR Comments

**Problem**: Comments don't appear on PRs

**Solution**: Verify `pull-requests: write` permission is set

### Changed Files Not Detected

**Problem**: `--changed-only` scans all files

**Solution**: Ensure `fetch-depth: 0` in checkout step

### Baseline Not Respected

**Problem**: Baseline findings still cause failures

**Solution**: Check config has `respect_baseline = true` and baseline file exists

## Best Practices

1. **Start with baseline**: Create baseline before enforcing in CI
2. **Fail on HIGH only**: Don't block PRs on low severity issues initially
3. **Scan changed files**: Use `--changed-only` for faster PR checks
4. **Upload artifacts**: Keep reports for audit trail
5. **Review weekly**: Schedule full scans even if PRs are clean

## Pre-commit Integration

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: spec-kit
        name: Spec-Kit Security Scan
        entry: specify audit --changed-only --fail-on-severity HIGH
        language: system
        pass_filenames: false
        always_run: true
```

Install hook:
```bash
pip install pre-commit
pre-commit install
```

## Next Steps

- Read [Configuration Guide](configuration.md)
- Learn about [Baseline Management](baseline.md)
- See [Triage Workflow](triage.md)
- Explore [Report Formats](reports.md)
