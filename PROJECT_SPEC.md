# Spec-Kit: Project Specification (Reworked)

**Version**: v0.1.0a4 → v0.1.0a5  
**Status**: Active Development (Phase 5)  
**Last Updated**: 2025-10-19  
**Type**: Python CLI Security Analysis Tool

---

## 🎯 Project Vision

**Spec-Kit** is a comprehensive security analysis CLI tool that helps developers:
1. **Scan** Python code for security vulnerabilities using Bandit
2. **Check** dependencies for known CVEs using Safety
3. **Generate** standardized reports (SARIF, HTML)
4. **Track** security issues over time with baselines
5. **Integrate** seamlessly into CI/CD pipelines

### Design Philosophy
- **CLI-First**: Simple, intuitive command-line interface
- **Developer-Friendly**: Clear error messages, helpful output
- **Modular**: Easy to extend with new analyzers
- **Standards-Compliant**: SARIF 2.1.0 output for tool integration
- **Git-Aware**: Analyze only changed files, track issues over time

---

## 📋 Core Specifications

### System Architecture

```
specify-cli/
├── CLI Layer (cli.py, commands/)
│   ├── Command parsing & validation
│   ├── User input/output
│   └── Error handling
│
├── Analysis Layer (analyzers/, runner.py)
│   ├── Bandit integration (code scanning)
│   ├── Safety integration (dependency checking)
│   └── Analyzer orchestration
│
├── Processing Layer (baseline.py, config.py)
│   ├── Configuration management
│   ├── Baseline fingerprinting
│   └── Finding deduplication
│
├── Output Layer (reporters/)
│   ├── SARIF 2.1.0 reporter
│   ├── HTML reporter
│   └── Console output
│
├── Integration Layer (github/, vscode/)
│   ├── GitHub integration
│   └── VS Code settings
│
└── Utilities (gitutils.py, store.py, ui/)
    ├── Git operations
    ├── Data persistence
    └── UI components
```

### Module Specifications

#### 1. CLI Module (`cli.py`, `commands/`)
**Purpose**: Command-line interface and command handlers

**Commands**:
- `specify init` - Initialize project with security scanning
- `specify audit` - Run security analysis
- `specify doctor` - Check tool prerequisites
- `specify <template>` - Generate various templates

**Requirements**:
- Click framework for CLI
- Rich for terminal UI
- Input validation and error handling
- Help text and examples

**Current Status**: ❌ 0% coverage, needs tests

---

#### 2. Analyzers Module (`analyzers/`)
**Purpose**: Security scanner integrations

##### Bandit Analyzer (`bandit_analyzer.py`)
**Function**: Scan Python code for security issues
**Input**: Directory path, exclusion patterns
**Output**: List of security findings with severity, CWE, line numbers
**Current Status**: ✅ 89% coverage, working

##### Safety Analyzer (`safety_analyzer.py`)
**Function**: Check dependencies for CVEs
**Input**: requirements.txt or installed packages
**Output**: List of vulnerable packages with CVE IDs, severity
**Current Status**: ⚠️ 36% coverage, needs more tests

**Specifications**:
- Must handle missing tools gracefully
- Must provide installation instructions on error
- Must normalize severity levels
- Must support custom configurations

---

#### 3. Configuration Module (`config.py`)
**Purpose**: Manage application configuration

**Configuration Sources** (priority order):
1. CLI flags (highest priority)
2. Environment variables (SPECKIT_*)
3. `.speckit.toml` file
4. Defaults (lowest priority)

**Config Structure**:
```python
@dataclass
class SpecKitConfig:
    analysis: AnalysisCfg      # fail_on, respect_baseline, changed_only
    output: OutputCfg          # format, directory
    analyzers: AnalyzersCfg    # bandit, safety, secrets
    security: SecurityCfg      # severity_threshold, thresholds (NEW)
    ci: CICfg                  # fail_on_severity, max_findings (NEW)
    exclude_paths: list[str]   # Glob patterns to exclude
```

**Environment Variables**:
- `SPECKIT_OUT_DIR` - Output directory
- `SPECKIT_BANDIT` - Enable/disable Bandit (true/false)
- `SPECKIT_SAFETY` - Enable/disable Safety (true/false)
- `SPECKIT_FAIL_ON` - Severity threshold for exit code
- `SPECKIT_RESPECT_BASELINE` - Use baseline filtering (true/false)
- `SPECKIT_CHANGED_ONLY` - Analyze only changed files (true/false)

**Current Status**: ✅ 97% coverage, needs security/CI sections added

---

#### 4. Baseline Module (`baseline.py`)
**Purpose**: Track and filter known security issues

**Features**:
- SHA-256 fingerprinting of findings
- JSON baseline storage
- Automatic baseline updates
- Finding suppression

**Fingerprint Algorithm**:
```
hash = sha256(rule_id + file_path + line + message)
```

**Baseline File**: `.speckit/baseline.json`
```json
{
  "findings": [
    {
      "hash": "abc123...",
      "rule_id": "B201",
      "file_path": "app.py",
      "line": 45,
      "message": "Flask debug mode",
      "first_seen": "2025-10-19T10:30:00Z"
    }
  ]
}
```

**Current Status**: ⚠️ 40% coverage, needs more tests

---

#### 5. Reporters Module (`reporters/`)
**Purpose**: Generate security analysis reports

##### SARIF Reporter (`sarif.py`)
**Specification**: SARIF 2.1.0 compliant
**Output**: `.sarif` JSON file
**Features**:
- Finding fingerprints for deduplication
- Severity level mapping (error/warning/note)
- CWE/CVE tagging
- Source location tracking
- Tool metadata

**Current Status**: ✅ 85% coverage, working

##### HTML Reporter (`html.py`)
**Output**: `.html` report file
**Features**:
- XSS protection (all dynamic content escaped)
- Summary statistics
- Sortable tables
- Mobile-responsive

**Current Status**: ✅ 100% coverage, working

---

#### 6. Runner Module (`runner.py`)
**Purpose**: Orchestrate analysis execution

**Workflow**:
1. Load configuration
2. Validate prerequisites (check tools)
3. Discover Python files
4. Run enabled analyzers
5. Load baseline (if enabled)
6. Filter baselined findings
7. Generate reports
8. Determine exit code

**Exit Codes**:
- `0` - Success, no issues or under threshold
- `1` - High severity findings or exceeded threshold
- `2` - Tool error (missing dependencies, invalid config)

**Current Status**: ❌ 0% coverage, needs tests

---

#### 7. Git Integration (`gitutils.py`)
**Purpose**: Git repository operations

**Features**:
- Detect if directory is git repo
- Get changed files (git diff)
- Get file history
- Get current branch

**Use Cases**:
- `--changed-only` flag (analyze only modified files)
- Git-aware baseline tracking
- Integration with GitHub Actions

**Current Status**: ❌ 0% coverage, needs tests

---

#### 8. Data Store (`store.py`)
**Purpose**: Persist analysis results

**Storage**:
- Location: `.speckit/runs/`
- Format: JSON
- Naming: `run_<timestamp>.json`

**Data**:
- Analysis timestamp
- Configuration used
- Findings (code + dependencies)
- Tool versions
- Execution time

**Current Status**: ✅ 100% tests passing, but 0% coverage metric (bug?)

---

#### 9. UI Components (`ui/`)

##### Tracker (`tracker.py`)
**Purpose**: Progress tracking for long operations
**Features**: Step tracking, timing, success/error states

##### Selector (`selector.py`)
**Purpose**: Interactive selection prompts
**Features**: List selection, validation, default values

##### Banner (`banner.py`)
**Purpose**: ASCII art and branding

**Current Status**: ⚠️ 51-54% coverage, needs more tests

---

## 🔧 Technical Specifications

### Language & Runtime
- **Python**: 3.13+ (using latest features)
- **Package Manager**: uv (fast pip alternative)
- **Virtual Environment**: .venv

### Dependencies
```toml
[project.dependencies]
python = "^3.13"
click = "^8.1.7"        # CLI framework
rich = "^13.8.1"        # Terminal UI
bandit = "^1.8.0"       # Security scanner
safety = "^3.0.0"       # CVE checker
toml = "^0.10.2"        # Config parsing
```

### Development Dependencies
```toml
[project.dev-dependencies]
pytest = "^8.4.2"
pytest-cov = "^7.0.0"
pytest-benchmark = "^5.1.0"  # TODO: Add this
ruff = "^0.8.0"             # Linter/formatter
```

### Code Style
- **Formatter**: Ruff
- **Line Length**: 100
- **Type Hints**: Required for all functions
- **Docstrings**: Required for public APIs

---

## 📊 Quality Metrics

### Current State (v0.1.0a4)
```
Total Lines:    1,340 (source code)
Modules:        24
Tests:          37 passing / 46 total
Coverage:       39%
Documentation:  Good (README, templates, phase docs)
```

### Phase 5 Targets (v0.1.0a5)
```
Total Lines:    ~1,700 (source code)
Modules:        26-27
Tests:          80+ passing / 80+ total (100%)
Coverage:       50%+
Documentation:  Excellent (+ user guides, API reference)
```

### Quality Gates
- ✅ All tests must pass
- ✅ Coverage ≥ 50% overall
- ✅ Critical modules (cli, runner, commands) ≥ 60%
- ✅ No security vulnerabilities (self-scan)
- ✅ Type hints on all public APIs
- ✅ Docstrings on all public APIs

---

## 🎯 Feature Specifications

### Implemented Features ✅

1. **Security Scanning**
   - Bandit integration
   - Safety integration
   - Custom exclusion patterns
   - Severity filtering

2. **Reporting**
   - SARIF 2.1.0 output
   - HTML reports with XSS protection
   - Console output

3. **Baseline Management**
   - Fingerprint-based tracking
   - Automatic baseline creation
   - Finding suppression

4. **Configuration**
   - TOML config file
   - Environment variables
   - CLI flags
   - Sensible defaults

5. **Project Initialization**
   - Interactive setup
   - Template generation
   - Agent configuration

### Phase 5 Features 🚧

1. **Enhanced Configuration** (PR-8)
   - Security threshold settings
   - CI/CD integration config
   - Config validation
   - from_dict() support

2. **Verbose Mode** (PR-10)
   - `--verbose/-v` flag
   - Detailed progress output
   - Debug information
   - Timing information

3. **Improved Error Handling** (PR-11)
   - Actionable error messages
   - Installation instructions
   - Troubleshooting tips
   - Context-aware suggestions

4. **User Documentation** (PR-12)
   - Configuration guide
   - Command reference
   - Troubleshooting guide
   - Integration examples

### Future Features 💡

1. **Additional Analyzers** (Phase 6-7)
   - Semgrep integration
   - MyPy type checking
   - Flake8 code quality
   - Custom rule support

2. **Performance** (Phase 6)
   - Parallel scanning
   - Incremental analysis
   - Baseline caching
   - File watching

3. **CI/CD Integration** (Phase 8)
   - GitHub Actions workflow
   - GitLab CI template
   - Jenkins plugin
   - Pre-commit hooks

4. **Advanced Reporting** (Phase 9)
   - Web dashboard
   - Trend analysis
   - Team metrics
   - Export formats (PDF, CSV)

---

## 🔒 Security Specifications

### Security by Design
1. **Input Validation**: All user input sanitized
2. **Output Escaping**: All dynamic HTML/JSON escaped
3. **File Operations**: Path traversal prevention
4. **Dependencies**: Regular security audits
5. **Secrets**: No hardcoded credentials

### Security Features
- XSS protection in HTML reports
- Command injection prevention
- Safe file handling (temp files, permissions)
- Secure baseline storage

### Self-Scanning
The tool scans itself:
```bash
cd spec-kit
specify audit
```

Expected: Clean scan (no vulnerabilities)

---

## 📚 Documentation Specifications

### User Documentation
- [x] README.md - Project overview
- [x] docs/quickstart.md - Getting started
- [x] docs/installation.md - Installation guide
- [ ] docs/configuration.md - Config reference (Phase 5)
- [ ] docs/commands.md - Command reference (Phase 5)
- [ ] docs/troubleshooting.md - Common issues (Phase 5)

### Developer Documentation
- [x] CONTRIBUTING.md - Contribution guidelines
- [x] CODE_OF_CONDUCT.md - Community standards
- [x] STRUCTURE_GUIDE.md - Codebase structure
- [x] PHASE_4_COMPLETE.md - Phase 4 summary
- [x] PHASE_5_PLAN.md - Phase 5 roadmap
- [x] TEST_TRACKING.md - Test documentation
- [x] PROJECT_SPEC.md - This file

### API Documentation
- [ ] Docstrings for all public functions
- [ ] Type hints for all functions
- [ ] Usage examples in docstrings
- [ ] API reference (generated from docstrings)

---

## 🧪 Testing Specifications

### Test Strategy
1. **Unit Tests**: Individual functions and classes
2. **Integration Tests**: Multi-component workflows
3. **Acceptance Tests**: End-to-end user scenarios
4. **Performance Tests**: Speed and resource usage

### Test Coverage Requirements
- Minimum: 50% overall
- Target: 70% overall
- Critical modules: 80%+
- New code: 90%+

### Test Organization
```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Multi-component tests
├── acceptance/     # End-to-end tests
└── perf/          # Performance tests
```

### CI/CD Testing
- Run on every PR
- Run on main branch
- Run nightly (full suite)
- Block merge if tests fail

---

## 🚀 Release Specifications

### Versioning
**Scheme**: Semantic Versioning (SemVer)
- Alpha: v0.1.0a1, v0.1.0a2, ...
- Beta: v0.1.0b1, v0.1.0b2, ...
- Stable: v0.1.0, v0.2.0, ...

### Release Criteria
**Alpha Release**:
- [ ] Core features working
- [ ] 50%+ test coverage
- [ ] Documentation started

**Beta Release**:
- [ ] All planned features complete
- [ ] 70%+ test coverage
- [ ] Complete documentation
- [ ] External testing

**Stable Release**:
- [ ] Production-ready
- [ ] 80%+ test coverage
- [ ] Comprehensive docs
- [ ] Security audit passed
- [ ] Performance benchmarks met

### Release Process
1. Update version in pyproject.toml
2. Update CHANGELOG.md
3. Run full test suite
4. Create release notes
5. Tag release in git
6. Build and publish to PyPI
7. Create GitHub release
8. Announce on relevant channels

---

## 🎯 Success Metrics

### User Metrics
- Installation success rate: >95%
- First scan success rate: >90%
- Error resolution rate: >80%

### Technical Metrics
- Test pass rate: 100%
- Coverage: >50%
- Build time: <5 minutes
- Scan time (medium repo): <30 seconds

### Quality Metrics
- Security vulnerabilities: 0
- Critical bugs: 0
- Documentation completeness: >90%

---

## 📞 Stakeholder Communication

### Progress Tracking
- Weekly summaries (CHANGELOG.md)
- Phase completion docs (PHASE_X_COMPLETE.md)
- Test tracking (TEST_TRACKING.md)
- This spec document (PROJECT_SPEC.md)

### Review Points
- End of each PR
- End of each Phase
- Before each release
- After user feedback

---

## 🔄 Maintenance Plan

### Regular Activities
- **Weekly**: Dependency updates
- **Monthly**: Security audit (self-scan)
- **Quarterly**: Performance review
- **Yearly**: Architecture review

### Support
- GitHub Issues for bug reports
- GitHub Discussions for Q&A
- Documentation for common issues
- Community contributions welcome

---

**Next Review**: After Phase 5 completion (v0.1.0a5)  
**Maintained By**: Development Team  
**Questions**: Open an issue on GitHub
