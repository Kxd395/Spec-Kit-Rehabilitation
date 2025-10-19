# Development Workflow & Rules

> **Last Updated**: 2025-10-19
> **Status**: Active Constitution
> **Applies To**: All development work on Spec-Kit

---

## Core Principles

### 1. Pre-Push Checklist (NON-NEGOTIABLE)

Before **ANY** `git push` operation, the following MUST be completed:

#### Repository Hygiene
- [ ] **Clean repository root** - Remove all temporary/review documentation files
- [ ] **Move working docs** - Session notes, planning docs, completion summaries → `/review-docs/`
- [ ] **Verify root contents** - Only essential project files remain (see [Approved Root Files](#approved-root-files))

#### Documentation Updates
- [ ] **CHANGELOG.md** - Add entry for ALL changes (features, fixes, refactors)
- [ ] **Version bump** - Update `pyproject.toml` if needed (see [Version Rules](#version-rules))
- [ ] **README.md** - Update if APIs, features, or usage changed
- [ ] **Affected docs** - Update any docs in `docs/` folder that reference changed code

#### Code Quality
- [ ] **Tests passing** - All tests must pass (`pytest`)
- [ ] **Coverage check** - Verify coverage didn't drop (target: 50%+)
- [ ] **Linting** - No new linting errors introduced

### 2. Version Rules

**When to bump version in `pyproject.toml`:**

- **MAJOR** (x.0.0): Breaking changes, API changes, removed features
- **MINOR** (0.x.0): New features, new commands, new analyzers
- **PATCH** (0.0.x): Bug fixes, documentation updates, refactoring

**Special Rule**: Any changes to `src/specify_cli/__init__.py` **REQUIRE**:
1. Version bump in `pyproject.toml`
2. Entry in `CHANGELOG.md`

### 3. CHANGELOG.md Format

Every change MUST follow this format:

```markdown
## [Version] - YYYY-MM-DD

### Added
- New features, commands, or capabilities

### Changed
- Modifications to existing functionality

### Fixed
- Bug fixes

### Removed
- Deprecated or removed features

### Internal
- Refactoring, code cleanup (no user-facing changes)
```

**Example**:
```markdown
## [0.1.0a5] - 2025-10-19

### Added
- Config enhancements: SecurityCfg, CICfg, PerformanceCfg, TelemetryCfg
- New helper functions: get_severity_level(), should_report_finding()

### Fixed
- audit.py: Fixed wrong import name (BANDIT_AVAILABLE → BANDIT)

### Internal
- Increased test coverage to 50% (88 passing tests)
- Added comprehensive tests for runner, baseline, audit, doctor modules
```

### 4. Approved Root Files

**Essential Documentation**:
- `README.md` - Project overview
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines
- `CODE_OF_CONDUCT.md` - Community standards
- `LICENSE` - Project license
- `SECURITY.md` - Security policy
- `SUPPORT.md` - Support information

**Configuration Files**:
- `pyproject.toml` - Python project config
- `.gitignore` - Git ignore rules
- `.gitattributes` - Git attributes
- `.speckit.toml` - Spec-Kit config (if present)

**Build/CI Files**:
- `.github/workflows/` - GitHub Actions
- `scripts/` - Utility scripts

**Source & Tests**:
- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation

**DO NOT COMMIT to root**:
- Session working files (SESSION_SUMMARY.md, etc.)
- Planning documents (PHASE_X_PLAN.md, etc.)
- Completion reports (PR_X_COMPLETE.md, etc.)
- Tracking spreadsheets (TEST_TRACKING.md, etc.)
- Old project files (AGENTS.md, spec-driven.md, etc.)

These belong in `/review-docs/` folder (outside repository).

---

## Development Process

### Phase/PR Workflow

1. **Planning Phase**:
   - Create planning document in `/review-docs/phase-X/`
   - Document goals, acceptance criteria, tasks
   - Get user approval before implementation

2. **Implementation Phase**:
   - Create feature branch: `feature/phase-X-pr-Y-description`
   - Write tests FIRST (TDD)
   - Implement functionality
   - Run tests locally
   - Update documentation

3. **Pre-Merge Checklist**:
   - [ ] All tests passing
   - [ ] Coverage target met
   - [ ] Documentation updated
   - [ ] CHANGELOG.md entry added
   - [ ] Version bumped (if needed)
   - [ ] Root directory clean

4. **Merge & Release**:
   - Merge to `main`
   - Create git tag for versions
   - Push to GitHub
   - Create GitHub release (for versions)

5. **Post-Push**:
   - Move planning/completion docs to `/review-docs/`
   - Verify clean repository state
   - Update tracking documents

### Testing Standards

**Coverage Targets**:
- Overall: 50%+ (current)
- New code: 80%+ coverage
- Critical paths: 100% coverage (audit, baseline, config)

**Test Quality**:
- ❌ NO superficial tests just for coverage numbers
- ✅ Tests must verify actual behavior
- ✅ Tests must catch real bugs
- ✅ Edge cases and error handling required

**Test Categories**:
1. **Unit tests** - Individual functions/classes
2. **Integration tests** - Module interactions
3. **Acceptance tests** - End-to-end workflows
4. **Regression tests** - Bug fixes

---

## AI Agent Rules

> From AGENTS.md (old project file - rules still apply)

**Any changes to `__init__.py` require:**
1. Version bump in `pyproject.toml`
2. Entry in `CHANGELOG.md`

**When adding new agent support:**
- Use actual CLI tool name as AGENT_CONFIG key
- Update README.md supported agents table
- Update CLI help text (`--ai` parameter)
- Update release package scripts
- Update agent context update scripts (bash + PowerShell)
- Test CLI tool checks (if required)

---

## Governance

### Constitution Authority
This document supersedes all ad-hoc practices. When in conflict, this document wins.

### Amendments
Changes to this document require:
1. Documentation of reason for change
2. User approval
3. Update to "Last Updated" date
4. Entry in CHANGELOG.md

### Enforcement
- **Pre-push checklist is mandatory** - No exceptions
- **Documentation updates are mandatory** - No exceptions
- **Version rules are mandatory** - No exceptions
- **Test quality standards are mandatory** - No exceptions

### Violations
If rules are violated (e.g., pushing without cleanup):
1. Stop immediately
2. Fix the violation (cleanup, update docs, etc.)
3. Push correction
4. Document what went wrong and how to prevent it

---

## Quick Reference Card

**Before EVERY git push:**
```bash
# 1. Clean root directory
ls -1 *.md  # Should only show essential docs

# 2. Update CHANGELOG.md
# Add entry for your changes

# 3. Check version (if __init__.py changed)
# Update pyproject.toml version

# 4. Run tests
pytest

# 5. Verify coverage
pytest --cov=src/specify_cli --cov-report=term

# 6. Git status check
git status  # Should be clean or only intended changes

# 7. Push
git push origin main
```

---

**Version**: 1.0.0
**Ratified**: 2025-10-19
**Last Amended**: 2025-10-19
