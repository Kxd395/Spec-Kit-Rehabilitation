# Phase 4 Revised Plan - Production Grade

**Based on**: review41.md hyper-critical analysis  
**Date**: October 18, 2025  
**Current Version**: v0.1.0a3 (Grade A - 94/100)  
**Target**: v0.1.0a4 → v0.2.0 (Grade A+ - 97+/100)

---

## 🎯 Critical Changes from Original Plan

### Problems Identified in Original Phase 4 Plan

1. **Scope Mixing**: 4 different change types in one phase (correctness, refactor, UX, new analyzer)
2. **Underspecified Refactor**: No git history preservation plan, no import map, no backout strategy
3. **Percentage-Driven Testing**: Coverage goal without targeting actual risk areas
4. **Soft Performance Goals**: No hardware profile, dataset fixtures, or reproducible harness
5. **Vague UX Goals**: "Interactive mode" not acceptance-testable
6. **Secrets Analyzer Iceberg**: Engine choice, redaction policy, SARIF mapping underestimated

### Solution: Split into Two Releases

```
v0.1.0a4 (4-6 weeks) → Refactor + Test + Perf (NO NEW FEATURES)
v0.2.0   (2-4 weeks) → Secrets + Config + UX enhancements
```

---

## 📋 Release v0.1.0a4: Correctness + Maintainability

**Primary Objective**: Make system easier to change without breaking users

**Feature Freeze**: No new analyzers, no new config keys, no CLI contract changes

### Work Item A: Refactor __init__.py Safely

**Impact**: Maintainability, Testability  
**Time**: 8-12 hours

#### Extracted Modules
```
src/specify_cli/
├── github/
│   ├── auth.py           # Token header builder
│   ├── download.py       # Repo zip fetch with retries
│   └── extraction.py     # Safe zip extraction (path traversal prevention)
├── ui/
│   ├── banner.py         # Banner function
│   ├── progress.py       # Simple progress printer
│   └── prompts.py        # User prompts
├── vscode/
│   └── settings.py       # Deep merge dict with type checks
└── commands/
    ├── init.py           # Bootstrap logic
    └── check.py          # Doctor-style checks
```

#### Safety Plan

**1. Use `git mv` to retain history:**
```bash
git mv src/specify_cli/__init__.py src/specify_cli/_monolith.py
# Then progressively split into target modules
git mv src/specify_cli/_monolith.py src/specify_cli/ui/banner.py
# Repeat for each logical chunk
```

**2. Import shim for backward compatibility:**
```python
# src/specify_cli/compat.py
from specify_cli.ui.banner import show_banner
from specify_cli.github.download import download_repo
__all__ = ["show_banner", "download_repo"]
```

**3. Deprecation window:**
- Keep internal legacy import paths working for one minor release
- Add runtime warning via logging once per process

**4. Backout plan:**
- Single revert commit restores pre-split tree
- Use `git revert` of the refactor PR

#### Acceptance Criteria

✅ Lines remaining in `__init__.py` < 200  
✅ All imports resolve with cold install  
✅ `specify init` and `specify check` work with new modules  
✅ No change in CLI help output (except module paths in stack traces)  

#### Required Tests

**tests/integration/test_init_flow.py**
- Asserts repo bootstraps
- Files are created
- Banner prints

**tests/integration/test_check_flow.py**
- Doctor-style checks do not regress

**Unit tests:**
- `tests/test_github_download.py` - Retry logic, timeout handling
- `tests/test_github_extraction.py` - Windows path separators, UTF-8 filenames
- `tests/test_vscode_settings.py` - Merge edge cases (key type conflicts)

#### Risk Hotspots to Test

⚠️ **Windows path separators and UTF-8 filenames** in extraction  
⚠️ **Archives with top-level folder vs flat files**  
⚠️ **VS Code settings JSON merge** when key exists with different types  

---

### Work Item B: Risk-Weighted Tests to 80% Coverage

**Impact**: Reliability  
**Time**: 6-8 hours

**Do NOT chase raw percentage.** Target modules that can break users:

| Module | Risk | Test File |
|--------|------|-----------|
| `baseline.py` | Regex suppression, path normalization | `test_baseline_regex.py` |
| `baseline.py` | Fingerprint stability | `test_baseline_fingerprint_stability.py` |
| `config.py` | Precedence tree, invalid values | `test_config_precedence_all_env.py` |
| `config.py` | Validation errors | `test_config_validation.py` |
| `runner.py` | Error propagation when analyzer fails | `test_runner_partial_failure.py` |
| `gitutils.py` | Changed-only logic | `test_gitutils_changed_only.py` |
| `store.py` | Write faults, JSON recovery | `test_store_resilience.py` |

#### Exact Test List

**tests/test_baseline_regex.py**
- Inline suppression with unicode
- Multi-line matches
- Platform paths

**tests/test_baseline_fingerprint_stability.py**
- Same finding set across path prefixes yields identical fingerprint

**tests/test_config_precedence_all_env.py**
- Set every `SPECKIT_*` env var and confirm overrides

**tests/test_config_validation.py**
- Values outside allowed enum → validation errors

**tests/test_runner_partial_failure.py**
- Monkeypatch `SafetyAnalyzer.run()` to raise `CalledProcessError`
- Assert exit code and message preserved when Bandit still runs

**tests/test_gitutils_changed_only.py**
- Simulate dirty repo using temp git init
- Create files across include and exclude globs

**tests/test_store_resilience.py**
- Corrupt last run file
- Ensure new run overwrites cleanly

#### Coverage Gate

- Keep CI threshold at **70%** for now
- **Fail PR if any risk-weighted tests are missing**
- Add custom check script:

```python
# scripts/check_required_tests.py
REQUIRED = [
    "tests/test_baseline_regex.py",
    "tests/test_baseline_fingerprint_stability.py",
    "tests/test_config_precedence_all_env.py",
    "tests/test_config_validation.py",
    "tests/test_runner_partial_failure.py",
    "tests/test_gitutils_changed_only.py",
    "tests/test_store_resilience.py",
]
# Assert all exist and are collected by pytest
```

---

### Work Item C: Performance Harness + Baseline Numbers

**Impact**: Predictability, Scalability  
**Time**: 4-6 hours

#### Benchmark Harness

**Hardware Profile (CI)**:
- Platform: `ubuntu-latest`
- CPU: 2 vCPU
- RAM: 7 GB
- Python: 3.13

**Test Suites**:
- **Small**: 1k LOC
- **Medium**: 10k LOC
- **Large**: 100k LOC
- Synthetic `requirements.txt`: 20, 100, 500 dependencies

#### Implementation

**scripts/bench/generate_repo.py**
```python
# Synthesize trees deterministically
def generate_python_files(count: int, lines_per_file: int) -> Path:
    """Generate synthetic Python code with known patterns"""
    pass

def generate_requirements(dep_count: int) -> Path:
    """Generate requirements.txt with popular packages"""
    pass
```

**Pytest Benchmark Tests**:
```bash
# Default: benchmarks disabled
pytest tests/perf -q --benchmark-disable

# Run benchmarks
pytest tests/perf --benchmark-only --benchmark-autosave
```

**Record JSON outputs in `.benchmarks/` for trend tracking**

#### Targets with Guardrails

| Analyzer | Dataset | Target | Hardware |
|----------|---------|--------|----------|
| Bandit | 1k LOC | < 3s | CI 2vCPU |
| Bandit | 10k LOC | < 15s | CI 2vCPU |
| Bandit | 100k LOC | < 90s | CI 2vCPU |
| Safety | 20 deps | < 2s | CI 2vCPU |
| Safety | 100 deps | < 10s | CI 2vCPU |
| Safety | 500 deps | < 60s | CI 2vCPU |
| SARIF | 1k results | < 3s, < 300MB | CI 2vCPU |

#### Optimization Steps (If Targets Miss)

1. **Parallelize analyzers** with `ThreadPoolExecutor` (external processes only)
2. **Memoize manifest detection** per run
3. **Stream results into SARIF writer** (chunk, not whole list concatenation)

#### Acceptance Criteria

✅ CI job named "Performance smoke" prints three timing lines  
✅ Exits green under targets  
✅ Failing a target fails job and blocks merge  

---

### Work Item D: Minimal UX Polish (No Contract Changes)

**Impact**: Developer Experience  
**Time**: 2-3 hours

**Keep it safe and measurable. No interactive prompts in a4.**

#### Additions

1. **`--verbose` flag** to `specify audit`:
   - Show analyzer start/finish lines + elapsed time
   
2. **Summary table at end**:
   - Counts per severity
   - Dependency vulns scanned/vulnerable
   - Output path

#### Acceptance Criteria

✅ `specify audit run --verbose` prints 3-step progress with timing  
✅ Summary shows counts per severity  
✅ Summary shows dependency vulns scanned and vulnerable  

#### Implementation Stub

```python
# src/specify_cli/ui/summary.py
from rich.table import Table

def make_summary(code_findings, dep_findings, duration_s: float, out_dir: str) -> Table:
    sev = [f.get("severity","").upper() for f in code_findings]
    hi = sev.count("HIGH") + sev.count("CRITICAL")
    md = sev.count("MEDIUM")
    lo = sev.count("LOW")
    
    t = Table(title="Audit Summary")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Code issues", f"{len(code_findings)} total • {hi} HIGH • {md} MED • {lo} LOW")
    t.add_row("Dependencies", f"{len(dep_findings)} vulnerable" if dep_findings else "0 vulnerable")
    t.add_row("Duration", f"{duration_s:.1f} seconds")
    t.add_row("Output", out_dir)
    return t
```

---

## 📦 Release v0.2.0: New Capabilities

**Primary Objective**: Features requiring new config keys and UX

### Work Item E: Secrets Analyzer MVP

**Time**: 6-8 hours

**Constraint**: Minimize false positives, avoid sensitive data leaks

#### Decisions (Locked)

- **Engine**: `detect-secrets` (Python native, stable CLI)
- **Redaction**: All outputs show only secret type + truncated hash
- **SARIF Mapping**: Rule IDs `DS-NNN`, CWE-798

#### Implementation Slices

**src/specify_cli/analyzers/secrets_analyzer.py**
```python
@dataclass
class SecretFinding:
    kind: str          # e.g., "AWS Access Key"
    file_path: str
    line: int
    detector: str      # e.g., "AWSKeyDetector"
    hash_prefix: str   # First 8 chars of SHA256
    entropy: float

class SecretsAnalyzer:
    def run(self) -> List[SecretFinding]:
        # Collect via subprocess with JSON
        # Normalize to dataclass
        # Respect exclude globs from config
        pass
```

**Reporters**:
- **SARIF**: Level `error` always, message references file + detector, help link to remediation
- **HTML**: No raw match content, never echo the secret

#### Configuration

```toml
[analyzers]
secrets = true  # Default: false (opt-in)

[secrets]
min_entropy = 3.5
allow_list = [
    "^EXAMPLE_.*",  # Regex patterns
]
```

#### Testing

**tests/test_secrets_analyzer.py**
- Unit tests using synthetic secrets + allow list

**tests/integration/test_secrets_e2e.py**
- SARIF includes `DS-` rules
- HTML escapes fields

**tests/test_secrets_redaction.py**
- No raw secret substrings in any output files

#### Security Review Checklist

✅ No subprocess invocation accepts user input without `shlex`  
✅ No secret values logged  
✅ Fail closed: If CLI missing in `--strict`, exit code 2  

---

### Work Item F: Config Validation Commands

**Time**: 3-4 hours

#### New Commands

1. **`specify config init`**
   - Scaffold `.speckit.toml` from prompts

2. **`specify config validate`**
   - Print validation errors

3. **`specify config show`**
   - Print effective config with source annotations (CLI vs ENV vs file)

#### Validation Rules

```python
# src/specify_cli/config_validate.py
ALLOWED_FAIL = {"HIGH", "MEDIUM", "LOW"}
ALLOWED_FMT = {"sarif", "html", "json"}

def validate(cfg) -> List[str]:
    errs = []
    if cfg.analysis.fail_on not in ALLOWED_FAIL:
        errs.append("analysis.fail_on must be HIGH, MEDIUM, or LOW")
    if cfg.output.format not in ALLOWED_FMT:
        errs.append("output.format must be sarif, html, or json")
    for p in cfg.exclude_paths:
        if ".." in p:
            errs.append(f"exclude path contains traversal: {p}")
    # Secrets validation
    if hasattr(cfg, 'secrets'):
        if not (0 <= cfg.secrets.min_entropy <= 8):
            errs.append("secrets.min_entropy must be 0-8")
    # Analyzer validation
    if not any([cfg.analyzers.bandit, cfg.analyzers.safety, 
                getattr(cfg.analyzers, 'secrets', False)]):
        errs.append("At least one analyzer must be enabled")
    return errs
```

---

### Work Item G: Enhanced CLI Output + Interactive Mode

**Time**: 4-5 hours

#### Features

1. **Live progress** using Rich Progress
2. **Optional `--interactive`**:
   - Asks to create baseline if findings exceed threshold and no baseline exists

#### Acceptance Criteria

✅ Non-interactive behavior remains default  
✅ All interactive prompts skippable in CI (by absence of flag)  

---

## 🔄 Sequencing and PR Plan

**Avoid mega PRs.** Use isolated blast radius.

### v0.1.0a4 Sequence (7 PRs)

| PR | Description | Files Changed | Tests Required |
|----|-------------|---------------|----------------|
| **PR-1** | Create module folders, move `ui.banner` | 3-5 | Integration test |
| **PR-2** | Move `github.download` + `extraction` | 4-6 | Unit + fixture zips |
| **PR-3** | Move `vscode.settings` | 2-3 | Merge tests |
| **PR-4** | Move `commands.init` + `check` | 4-6 | Integration tests |
| **PR-5** | Add risk-weighted tests | 7 test files | - |
| **PR-6** | Perf harness + CI job | 5-7 | Benchmark tests |
| **PR-7** | Minimal UX: verbose mode + summary | 3-4 | CLI output tests |

### v0.2.0 Sequence (4 PRs)

| PR | Description | Files Changed | Tests Required |
|----|-------------|---------------|----------------|
| **PR-A** | Secrets analyzer skeleton + JSON normalize | 3-5 | Unit tests |
| **PR-B** | SARIF mapping + redaction tests | 4-6 | E2E + security |
| **PR-C** | Config validate + show commands | 3-4 | CLI tests |
| **PR-D** | Progress bars + interactive mode | 3-5 | UX tests |

### PR Requirements (All)

✅ Docs update for user-visible changes  
✅ At least one new focused test  
✅ Pass coverage gate and perf smoke job  

---

## ⚠️ Risk Register + Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Import breakage after refactor | HIGH | MEDIUM | Import shim `compat.py`, repo-wide grep, integration tests |
| Cross-platform path bugs | MEDIUM | HIGH | Windows CI job for filesystem/zip tests |
| Secrets analyzer leaks sensitive data | CRITICAL | LOW | E2E test: literal secret not in any artifact |
| Performance regression from concurrency | MEDIUM | MEDIUM | Limit pool size to # analyzers, don't parallelize file reads |
| Flaky performance job | LOW | HIGH | 20% time buffer, pin runner size, warm pip cache |
| Safety JSON shape drift | MEDIUM | LOW | Tolerant parser + unit tests for both shapes |

---

## 📊 Measurable Exit Criteria

### v0.1.0a4 Must Meet ALL:

✅ `__init__.py` under 200 lines  
✅ Coverage ≥ 80% on `src/`  
✅ Performance smoke shows times under targets on CI  
✅ No CLI contract changes, existing SARIF tests pass  
✅ New verbose summary appears and is stable in tests  
✅ Docs updated: src, architecture, commands READMEs revised  

### v0.2.0 Must Meet ALL:

✅ Secrets analyzer behind config flag  
✅ Enabled by default only when `detect-secrets` installed  
✅ Redaction tests pass, no literal secrets in artifacts  
✅ Config validate/show commands documented with examples  
✅ Progress bars and interactive mode disabled by default  
✅ Benchmarks stable within 10% of a4  

---

## 🚫 What NOT to Do in Phase 4

❌ Do not introduce new CLI flags in a4 except `--verbose`  
❌ Do not add IDE extensions or dashboards  
❌ Do not replace Safety or Bandit yet  
❌ Do not add plugin system scaffolding (separate program of work)  

---

## 📁 Concrete Task List by File Path

### v0.1.0a4 Files

**New Modules**:
```
src/specify_cli/
├── ui/
│   ├── banner.py           # Extract banner function
│   ├── progress.py         # Simple progress printer (verbose mode)
│   └── prompts.py          # User prompts
├── github/
│   ├── auth.py             # Token header builder
│   ├── download.py         # Repo zip fetch with retries
│   └── extraction.py       # Safe zip extraction (path traversal prevention)
├── vscode/
│   └── settings.py         # Deep merge dict with type checks
├── commands/
│   ├── init.py             # Move from monolith
│   └── check.py            # Move from monolith
└── compat.py               # Import shim for backward compatibility
```

**New Tests**:
```
tests/
├── integration/
│   ├── test_init_flow.py
│   └── test_check_flow.py
├── test_baseline_regex.py
├── test_baseline_fingerprint_stability.py
├── test_config_precedence_all_env.py
├── test_config_validation.py
├── test_runner_partial_failure.py
├── test_gitutils_changed_only.py
├── test_store_resilience.py
└── perf/
    ├── test_bandit_perf.py
    └── test_safety_perf.py
```

**New Scripts**:
```
scripts/
├── bench/
│   └── generate_repo.py    # Synthetic repo generator
└── check_required_tests.py  # Enforce risk-weighted tests
```

**Modified**:
- `src/specify_cli/__init__.py` (reduce to < 200 lines)
- `src/specify_cli/commands/audit.py` (add --verbose)
- `docs/architecture.md` (update with new modules)
- `src/specify_cli/commands/README.md` (update structure)

### v0.2.0 Files

**New Modules**:
```
src/specify_cli/
└── analyzers/
    └── secrets_analyzer.py
```

**New Commands**:
```
src/specify_cli/commands/
├── config_init.py
├── config_validate.py
└── config_show.py
```

**New Config Module**:
```
src/specify_cli/
└── config_validate.py
```

**New Tests**:
```
tests/
├── test_secrets_analyzer.py
├── test_secrets_redaction.py
└── integration/
    └── test_secrets_e2e.py
```

---

## 📈 Timeline and Velocity

### v0.1.0a4 Timeline (4-6 weeks)

**Sprint 1 (Weeks 1-2)**: Refactor
- PR-1 through PR-4: Module extraction
- Target: 16-24 hours

**Sprint 2 (Week 3)**: Test + Perf
- PR-5: Risk-weighted tests
- PR-6: Performance harness
- Target: 10-14 hours

**Sprint 3 (Week 4)**: UX Polish + Release Prep
- PR-7: Verbose mode + summary
- Documentation updates
- CHANGELOG finalization
- Target: 6-8 hours

**Total**: 32-46 hours

### v0.2.0 Timeline (2-4 weeks)

**Sprint 4 (Week 5)**: Secrets Analyzer
- PR-A, PR-B: Secrets detection + SARIF
- Target: 10-14 hours

**Sprint 5 (Week 6)**: Config + UX
- PR-C: Config commands
- PR-D: Progress + interactive
- Target: 7-9 hours

**Sprint 6 (Week 7-8)**: Stabilization + Release
- Bug fixes, documentation
- CHANGELOG finalization
- Target: 4-6 hours

**Total**: 21-29 hours

---

## 🏷️ Branch Strategy

**Feature Branches**:
```
feature/a4-refactor-banner
feature/a4-refactor-github
feature/a4-refactor-vscode
feature/a4-refactor-commands
feature/a4-risk-weighted-tests
feature/a4-perf-harness
feature/a4-verbose-mode

feature/v0.2.0-secrets-analyzer
feature/v0.2.0-config-commands
feature/v0.2.0-progress-ui
```

**Release Branches**:
```
release/a4     # Final stabilization for v0.1.0a4
release/v0.2.0 # Final stabilization for v0.2.0
```

**Merge Strategy**:
- Squash merge for refactor PRs (keep history readable)
- Regular merge for feature PRs

---

## 🏷️ Issue Labels

Create these labels in GitHub:

- `phase-4`
- `refactor`
- `test`
- `perf`
- `ux`
- `secrets`
- `config`
- `blocker`
- `a4-milestone`
- `v0.2.0-milestone`

---

## 📝 Changelog Discipline

**Each PR must add a single bullet to CHANGELOG under `[Unreleased]`**:

```markdown
## [Unreleased]

### Added (v0.1.0a4)
- Modular architecture: extracted github, ui, vscode, commands modules
- Performance benchmarking harness with CI smoke tests
- Risk-weighted test coverage targeting baseline, config, runner
- Verbose mode with timing information and summary table

### Added (v0.2.0)
- Secrets detection analyzer using detect-secrets
- Config validation commands: init, validate, show
- Live progress bars with Rich
- Optional interactive mode for baseline creation
```

---

## 📋 Communication Plan

### Weekly Status Updates

Post to GitHub Discussions or team channel:

**Format**:
```
🚀 Phase 4 Week N Update

✅ Completed:
- PR-N: Description (merged)

🔄 In Progress:
- PR-N: Description (in review)

🎯 Next Week:
- PR-N: Description (starts Monday)

⚠️ Blockers:
- None / Description of blocker
```

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Refactor (no functional changes)
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update

## Phase 4 Checklist
- [ ] Tests added/updated
- [ ] CHANGELOG updated
- [ ] Docs updated (if user-facing)
- [ ] Coverage gate passes
- [ ] Perf smoke passes (if applicable)
- [ ] No CLI contract changes (a4 only)

## Testing
How was this tested?

## Risk Assessment
- **Blast Radius**: Small / Medium / Large
- **Rollback Plan**: Describe
```

---

## 🎯 Final Grade Targets

| Metric | v0.1.0a3 | v0.1.0a4 Target | v0.2.0 Target |
|--------|----------|-----------------|---------------|
| **Overall Grade** | A (94/100) | A (95-96/100) | A+ (97+/100) |
| **Code Quality** | 25/25 | 25/25 | 25/25 |
| **Security** | 24/25 | 24/25 | 25/25 |
| **Testing** | 18/20 | 19/20 | 20/20 |
| **Documentation** | 14/15 | 15/15 | 15/15 |
| **Performance** | 13/15 | 14/15 | 15/15 |

### Grade Improvement Actions

**v0.1.0a4** (+1-2 points):
- Refactored architecture → +1 Code Quality
- Risk-weighted tests → +1 Testing
- Performance harness → +1 Performance

**v0.2.0** (+2-3 points):
- Secrets analyzer → +1 Security
- Config validation → +1 Code Quality
- Comprehensive testing → +1 Testing
- Optimizations → +1 Performance

---

## 🚀 Next Immediate Actions

### 1. Review and Approve Plan
```bash
# Read this document thoroughly
open PHASE_4_REVISED_PLAN.md
```

### 2. Create GitHub Project Board (Optional)
- Convert this plan into issues
- Organize by milestone (a4 vs v0.2.0)
- Assign estimates and priorities

### 3. Start PR-1: Banner Refactor
```bash
# Create feature branch
git checkout -b feature/a4-refactor-banner

# Create directory structure
mkdir -p src/specify_cli/ui
mkdir -p tests/integration

# Start extraction
# ... implementation ...
```

### 4. Update Team Communication
- Share this plan with stakeholders
- Set up weekly status update schedule
- Create PR templates in `.github/`

---

## 📚 Reference Documents

- **Original Plan**: `PHASE_4_PLANNING.md`
- **Critical Review**: `Review/review41.md`
- **This Document**: `PHASE_4_REVISED_PLAN.md`
- **Phase 3 Summary**: `COMPREHENSIVE_CODE_REVIEW.md`

---

## ✅ Approval Checklist

Before starting Phase 4 work:

- [ ] Review complete revised plan
- [ ] Understand split: a4 (refactor/test/perf) vs v0.2.0 (features)
- [ ] Agree on PR sequencing strategy
- [ ] Approve risk register and mitigations
- [ ] Confirm exit criteria are measurable
- [ ] Set up GitHub labels and templates
- [ ] Schedule weekly status updates
- [ ] Create feature branch for PR-1

---

**Ready to begin Phase 4 when you give the green light!** 🚦
