# Phase 5 Planning: v0.1.0a5

**Status**: Planning
**Start Date**: 2025-01-XX
**Target Version**: v0.1.0a5
**Previous Phase**: Phase 4 v0.1.0a4 (COMPLETE)

---

## 📊 Current State

### Phase 4 Results ✅
- **Version**: v0.1.0a4 released
- **Refactoring**: __init__.py reduced from 1,198 → 176 lines (-85%)
- **Modules**: 11 → 24 (+13 new modules)
- **Tests**: 33 → 37 passing tests (+4 fixed)
- **Coverage**: 33% → 39% (+6%)
- **Breaking Changes**: 0

### Known Issues
1. **3 failing acceptance tests** in `test_exit_code_thresholds.py`:
   - Missing functions: `get_severity_level`, `should_report_finding`
   - Missing config attributes: `config.security`, `config.ci`
   - Missing method: `SpecKitConfig.from_dict()`

2. **1 benchmark error**: `test_bandit_scaling` requires pytest-benchmark plugin

3. **Coverage gaps**:
   - Many modules at 0-20% coverage
   - Target: 50%+ overall coverage

4. **User experience**:
   - No `--verbose` flag for detailed output
   - Error messages could be more helpful
   - Missing user documentation

---

## 🎯 Phase 5 Objectives

### Primary Goals
1. **Fix remaining test failures** (3 acceptance tests + 1 benchmark)
2. **Increase test coverage** to 50%+
3. **Improve error messages** and user feedback
4. **Add `--verbose` flag** for detailed output
5. **Enhance documentation** for end users

### Success Criteria
- [ ] 100% tests passing (currently 37/41 passing, 5 skipped)
- [ ] Coverage ≥ 50% (currently 39%)
- [ ] `--verbose` flag implemented and tested
- [ ] Error messages improved and tested
- [ ] User documentation complete
- [ ] v0.1.0a5 released

---

## 📝 Implementation Plan

### PR-8: Fix Acceptance Tests
**Objective**: Fix the 3 failing tests in `test_exit_code_thresholds.py`

**Tasks**:
1. Add missing functions to `config.py`:
   - `get_severity_level(severity: str) -> int`
   - `should_report_finding(finding: dict, threshold: str) -> bool`

2. Add missing config sections:
   - `SecurityCfg` dataclass with `severity_threshold`, `bandit_enabled`
   - `CICfg` dataclass with `fail_on_severity`, `max_findings`
   - Add to `SpecKitConfig`

3. Add `SpecKitConfig.from_dict()` class method

4. Update `load_config()` to handle new config sections

**Estimated Impact**:
- Lines: +80-100
- Tests: +0 (fixing existing)
- Files: 1 modified (config.py)

---

### PR-9: Increase Test Coverage
**Objective**: Boost coverage from 39% → 50%+

**Targets** (prioritized by impact):
1. **High-value, low-coverage modules**:
   - `analyzers/bandit_analyzer.py`: 89% → 95%+ (add edge case tests)
   - `baseline.py`: 40% → 70%+ (add baseline logic tests)
   - `commands/init_impl.py`: 22% → 50%+ (add command tests)
   - `reporters/sarif.py`: 85% → 95%+ (add SARIF edge cases)

2. **Zero-coverage modules** (prioritize by user impact):
   - `cli.py`: 0% → 80%+ (critical for CLI)
   - `runner.py`: 0% → 60%+ (core execution)
   - `commands/audit.py`: 0% → 50%+ (key feature)

**Estimated Impact**:
- Lines: +300-400 (new tests)
- Coverage: 39% → 55-60%
- Files: 15-20 test files added/modified

---

### PR-10: Add --verbose Flag
**Objective**: Implement detailed output mode for debugging

**Implementation**:
1. Add `--verbose/-v` flag to CLI commands
2. Create `VerboseLogger` class for formatted output
3. Add verbose output to:
   - File scanning progress
   - Analyzer execution details
   - Configuration loading
   - Baseline comparison
   - Report generation

4. Add tests for verbose output

**Estimated Impact**:
- Lines: +150-200
- Tests: +8-10
- Files: 2 new (verbose.py, test_verbose.py), 5 modified

---

### PR-11: Improve Error Messages
**Objective**: Make errors more actionable and user-friendly

**Categories**:
1. **Configuration errors**:
   - Missing config file → Suggest `specify init`
   - Invalid TOML → Show line number and syntax error
   - Invalid values → Show valid options

2. **Tool errors**:
   - Bandit not found → Installation instructions
   - Safety not found → Installation instructions
   - Git not found → Installation instructions

3. **Runtime errors**:
   - No Python files found → Check exclude patterns
   - Baseline not found → Show baseline creation command
   - Permission denied → Show required permissions

**Estimated Impact**:
- Lines: +200-250
- Tests: +15-20
- Files: 1 new (errors.py), 8 modified, 1 test file

---

### PR-12: User Documentation
**Objective**: Complete end-user documentation

**Sections**:
1. **docs/quickstart.md** (enhance existing):
   - Installation steps
   - First scan walkthrough
   - Basic configuration
   - Viewing results

2. **docs/configuration.md** (new):
   - All config options explained
   - Environment variables
   - CLI flags
   - Examples for common use cases

3. **docs/commands.md** (new):
   - Command reference
   - Options and flags
   - Examples for each command

4. **docs/troubleshooting.md** (new):
   - Common errors and fixes
   - Performance tips
   - Integration guides

**Estimated Impact**:
- Lines: +800-1000 (docs)
- Files: 3 new, 2 modified

---

## 📈 Projected Metrics

### Before Phase 5 (v0.1.0a4)
- Lines: ~1,340 (source)
- Tests: 37 passing / 41 total (90% pass rate)
- Coverage: 39%
- Modules: 24
- Docs: Basic (README, templates)

### After Phase 5 (v0.1.0a5)
- Lines: ~1,600-1,700 (source)
- Tests: 41+ passing / 41+ total (100% pass rate)
- Coverage: 50-60%
- Modules: 26-27 (+2-3)
- Docs: Comprehensive (+ 4 guides)

---

## 🔄 Development Workflow

### For Each PR:
1. Create feature branch: `feature/phase-5-pr-X-description`
2. Implement changes with tests
3. Run full test suite: `pytest -v`
4. Check coverage: `pytest --cov=src/specify_cli --cov-report=html`
5. Update CHANGELOG.md
6. Create PR with:
   - Clear description
   - Test results
   - Coverage delta
   - Breaking changes (if any)
7. Merge to main
8. Tag intermediate alphas if needed

### Final Release:
1. Verify all PRs merged
2. Run full test suite + coverage report
3. Update version to v0.1.0a5
4. Create release notes: `RELEASE_NOTES_v0.1.0a5.md`
5. Tag release: `git tag -a v0.1.0a5 -m "Release v0.1.0a5"`
6. Push tag: `git push origin v0.1.0a5`

---

## 🗓️ Timeline Estimate

| PR | Description | Estimated Time | Priority |
|----|-------------|----------------|----------|
| PR-8 | Fix acceptance tests | 2-3 hours | HIGH |
| PR-9 | Increase test coverage | 6-8 hours | HIGH |
| PR-10 | Add --verbose flag | 3-4 hours | MEDIUM |
| PR-11 | Improve error messages | 4-5 hours | MEDIUM |
| PR-12 | User documentation | 3-4 hours | MEDIUM |

**Total Estimated Time**: 18-24 hours
**Recommended Approach**: Complete PRs in sequence (8 → 9 → 10 → 11 → 12)

---

## 🚀 Post-Phase 5 Considerations

### Future Phases (v0.1.0a6+):
1. **Phase 6**: Performance optimization (baseline caching, parallel scans)
2. **Phase 7**: Additional analyzers (semgrep, mypy, flake8)
3. **Phase 8**: CI/CD integrations (GitHub Actions, GitLab CI)
4. **Phase 9**: Web UI / dashboard
5. **Phase 10**: Beta release (v0.1.0b1)

### PyPI Release:
- Target after Phase 5 completion
- Requires: 100% passing tests, 50%+ coverage, complete docs
- Steps: Build dist, upload to PyPI, announce release

---

## 📌 Notes

### Design Principles:
- Maintain backward compatibility (no breaking changes)
- Keep __init__.py under 200 lines
- All new features must have tests
- Coverage should never decrease
- Documentation for all public APIs

### Testing Strategy:
- Unit tests for all new functions
- Integration tests for CLI commands
- Acceptance tests for user workflows
- Performance tests for critical paths

### Risk Mitigation:
- Small, focused PRs (easier to review and revert)
- Run full test suite before each commit
- Keep main branch always deployable
- Tag intermediate alphas for safety

---

**Next Steps**: Start with PR-8 (fix acceptance tests) to get to 100% passing tests baseline.
