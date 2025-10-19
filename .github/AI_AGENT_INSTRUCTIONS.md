# AI Agent Instructions for Spec-Kit Development

> **Purpose**: Instructions for AI coding assistants working on Spec-Kit
> **Last Updated**: 2025-10-19
> **Authority**: These rules are MANDATORY and supersede ad-hoc decisions

---

## 🚨 MANDATORY PRE-PUSH CHECKLIST

Before **ANY** `git push` operation, you MUST complete ALL items:

### 1. Repository Hygiene ✅
```bash
# Check root directory - should only show essential files
ls -1 *.md

# Essential files ONLY:
# - README.md, CHANGELOG.md, CONTRIBUTING.md
# - CODE_OF_CONDUCT.md, LICENSE, SECURITY.md, SUPPORT.md
# - DEVELOPMENT_WORKFLOW.md

# If you see ANY of these, STOP and clean up:
# - PHASE_*.md, PR_*.md, SESSION_*.md
# - TEST_TRACKING.md, PROJECT_SPEC.md, RELEASE_NOTES_*.md
# - AGENTS.md, spec-driven.md (old project files)

# Move temp files to review-docs/
mv PHASE_*.md ../review-docs/phase-X/
mv PR_*.md ../review-docs/phase-X/
mv SESSION_*.md ../review-docs/phase-X/
# etc.
```

### 2. Documentation Updates ✅
```bash
# CHANGELOG.md - ALWAYS update with your changes
# Format:
## [Version] - YYYY-MM-DD

### Added
- New features

### Changed
- Modifications

### Fixed
- Bug fixes

### Internal
- Refactoring (no user-facing changes)

# README.md - Update if APIs, features, or usage changed
# docs/ - Update any affected documentation
```

### 3. Version Management ✅
```bash
# Check if __init__.py was modified
git diff main src/specify_cli/__init__.py

# If __init__.py changed:
# 1. Bump version in pyproject.toml
#    - MAJOR: Breaking changes
#    - MINOR: New features
#    - PATCH: Bug fixes
# 2. Add CHANGELOG.md entry
# 3. Update version references in docs

# Current version check:
grep version pyproject.toml
```

### 4. Quality Gates ✅
```bash
# Run all tests
pytest

# Check coverage (target: 50%+)
pytest --cov=src/specify_cli --cov-report=term

# Verify no new linting errors
# (if ruff/pylint is configured)

# Clean git status
git status  # Should show only intended changes
```

---

## 🎯 Development Workflow

### Phase/PR Process

1. **Planning** → Create docs in `/review-docs/phase-X/`
2. **Implementation** → Feature branch: `feature/phase-X-pr-Y-description`
3. **Testing** → Write tests FIRST (TDD), get 80%+ coverage on new code
4. **Documentation** → Update CHANGELOG.md, README.md, version
5. **Cleanup** → Move temp docs to review-docs/
6. **Merge** → Only after ALL checklist items complete

### Testing Standards

**Quality Over Quantity**:
- ❌ NO superficial tests just for coverage numbers
- ✅ Tests must verify actual behavior and catch real bugs
- ✅ Edge cases and error handling required

**Coverage Targets**:
- Overall: 50%+ (current baseline)
- New code: 80%+ coverage
- Critical paths: 100% coverage (audit, baseline, config)

---

## 📚 Key Reference Documents

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **DEVELOPMENT_WORKFLOW.md** | Complete development rules | Before EVERY push |
| **CHANGELOG.md** | Version history | Before/after EVERY change |
| **CONTRIBUTING.md** | Contribution guidelines | When adding features |
| **review-docs/old-project-docs/AGENTS.md** | Agent integration rules | When modifying agent support |

---

## 🔧 Special Rules

### Rule: __init__.py Changes
**Any modification to `src/specify_cli/__init__.py` requires:**
1. Version bump in `pyproject.toml`
2. Entry in `CHANGELOG.md`
3. Update version references in docs

### Rule: Config Changes
**Any modification to `src/specify_cli/config.py` requires:**
1. Tests for new config options
2. Documentation in README.md or docs/
3. CHANGELOG.md entry

### Rule: Command Changes
**Any modification to commands/ requires:**
1. Acceptance tests
2. Help text updates
3. Documentation updates
4. CHANGELOG.md entry

---

## 🚫 Common Mistakes to Avoid

1. **Pushing without cleanup** → Check root directory first
2. **Forgetting CHANGELOG.md** → Update on EVERY change
3. **Skipping version bump** → Required for __init__.py changes
4. **Superficial tests** → Quality over quantity
5. **Incomplete documentation** → Update all affected docs

---

## ✅ Pre-Push Command Sequence

Run this EXACT sequence before every push:

```bash
# 1. Check for temp files in root
ls -1 *.md | grep -E "(PHASE_|PR_|SESSION_|TEST_TRACKING|PROJECT_SPEC)" && echo "❌ CLEANUP NEEDED" || echo "✅ Root clean"

# 2. Verify CHANGELOG.md was updated
git diff main CHANGELOG.md | grep "^+" | tail -5

# 3. Check version consistency (if __init__.py changed)
git diff main src/specify_cli/__init__.py | head -20

# 4. Run tests
pytest

# 5. Check coverage
pytest --cov=src/specify_cli --cov-report=term-missing | tail -20

# 6. Verify git status
git status

# 7. Only if ALL checks pass:
git push origin main
```

---

## 🤖 AI Agent Self-Check

Before responding with "ready to push" or executing `git push`, ask yourself:

- [ ] Did I clean the repository root?
- [ ] Did I update CHANGELOG.md?
- [ ] Did I bump version (if __init__.py changed)?
- [ ] Did I update README.md (if features changed)?
- [ ] Did I run and verify tests?
- [ ] Did I verify coverage didn't drop?
- [ ] Is git status clean (only intended changes)?

**If ANY answer is "NO" or "UNSURE" → DO NOT PUSH**

---

## 📖 Full Documentation

For complete rules and rationale, see:
- **[DEVELOPMENT_WORKFLOW.md](../DEVELOPMENT_WORKFLOW.md)** - Complete development constitution
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines
- **[review-docs/old-project-docs/AGENTS.md](../../review-docs/old-project-docs/AGENTS.md)** - Agent integration rules

---

**Version**: 1.0.0
**Created**: 2025-10-19
**Last Updated**: 2025-10-19
