# 📁 FILE ORGANIZATION GUIDE

**Date:** October 18, 2025  
**Purpose:** Explains what files belong where and why

---

## 🗂️ REPOSITORY STRUCTURE

### Root (Product Files - Keep)

```
/
├── .speckit.toml                    # User-facing config example
├── pyproject.toml                   # Package metadata
├── README.md                        # Main documentation
├── CHANGELOG.md                     # Version history
├── LICENSE                          # Legal
├── CONTRIBUTING.md                  # How to contribute
├── CODE_OF_CONDUCT.md               # Community guidelines
├── SECURITY.md                      # Security policy
├── IMPLEMENTATION_ROADMAP.md        # Active planning (Phase 1-6)
└── PHASE_1_COMPLETE.md              # Current status summary
```

**Why These Stay:**
- User-facing documentation
- Package configuration
- Active development planning

---

### /src (Code - Keep All)

```
src/specify_cli/
├── __init__.py                      # Entry point
├── config.py                        # ✅ NEW: Config loader
├── baseline.py                      # ✅ NEW: Baseline management
├── reporters/
│   ├── __init__.py
│   └── sarif.py                     # ✅ NEW: SARIF reporter
└── analyzers/                       # 🔜 TODO: Add analyzers
```

**All code files stay in main repo.**

---

### /docs (Documentation - Keep All)

```
docs/
├── index.md
├── installation.md
├── quickstart.md
├── README.md
├── ci_examples.md                   # ✅ NEW: GitHub Actions
├── configuration.md                 # ✅ NEW: Config reference
└── local-development.md
```

**Active user documentation stays.**

---

### /tests (Tests - Keep All)

```
tests/
├── __init__.py
├── test_cli.py                      # Existing tests
├── acceptance/
│   ├── __init__.py
│   └── test_exit_code_thresholds.py # ✅ NEW: Acceptance tests
└── unit/                            # 🔜 TODO: Add unit tests
    ├── test_config.py
    ├── test_baseline.py
    └── test_sarif.py
```

**All test files stay in main repo.**

---

### /Review (Development Context - Archive)

```
Review/
├── review1.md                       # Bootstrap instructions
├── review2.md                       # Gap analysis (30 items)
├── CRITICAL_ASSESSMENT.md           # ✅ NEW: Grade B+ assessment
├── DEPENDENCIES_AND_TESTING.md      # ✅ NEW: Complete deps list
└── archive/                         # Historical docs
    ├── HONEST_ASSESSMENT.md         # Initial critique
    ├── LIMITATIONS.md               # Original limitations
    ├── STRUCTURE_ANALYSIS.md        # Structure review
    ├── STRUCTURE_QUICK_ANSWER.md    # Quick structure notes
    ├── STRUCTURE_GUIDE.md           # Structure guide
    ├── FIX_SUMMARY.md               # Early fixes
    ├── REHABILITATION-ENHANCEMENT-SUMMARY.md
    ├── FORK_COMPLETE.md             # Fork success summary
    └── YES_THIS_HELPS.md            # Gap analysis response
```

**Why These Move:**
- Historical context, not active development
- Valuable for understanding project evolution
- Should NOT be in end-user product
- Keep in Review/ for team reference

---

## 🎯 WHAT FILES DO

### Active Product Files

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Main entry point | Users |
| `.speckit.toml` | Config example | Users |
| `pyproject.toml` | Package build | Developers |
| `CHANGELOG.md` | Version history | Users |
| `IMPLEMENTATION_ROADMAP.md` | 6-phase plan | Developers |
| `PHASE_1_COMPLETE.md` | Status update | Developers |
| `docs/*.md` | User guides | Users |
| `src/**/*.py` | Code | Developers |
| `tests/**/*.py` | Tests | Developers |

### Review/Context Files

| File | Purpose | Audience |
|------|---------|----------|
| `Review/review1.md` | Bootstrap guide | Team |
| `Review/review2.md` | Gap analysis | Team |
| `Review/CRITICAL_ASSESSMENT.md` | Grade B+ | Team |
| `Review/DEPENDENCIES_AND_TESTING.md` | Deps guide | Team |
| `Review/archive/*` | Historical | Team (archive) |

---

## 📋 LIFECYCLE PLAN

### After Phase 2 (Bandit Integration)

**Archive:**
- `PHASE_1_COMPLETE.md` → `Review/archive/`
- Create `PHASE_2_COMPLETE.md`

### After MVP (Phases 1-3)

**Update:**
- `README.md` - Add real usage examples
- `CHANGELOG.md` - Add v0.2.0 notes

**Archive:**
- `IMPLEMENTATION_ROADMAP.md` → `Review/archive/`
- Create `docs/roadmap.md` (public version)

### After v1.0 Release

**Remove from main repo:**
- Move all `Review/` to separate `spec-kit-dev-notes` repo
- Keep clean production repo

**Keep in main repo:**
- README, CHANGELOG, LICENSE
- docs/ (user facing)
- src/, tests/
- pyproject.toml, .speckit.toml

---

## 🗑️ WHAT TO DELETE (Eventually)

### Never Delete

❌ **Don't delete these - they're valuable history:**
- Review/ files (move to archive repo instead)
- Early assessments (show your thinking)
- Gap analyses (show professional approach)

### Can Delete After v1.0

✅ **These served their purpose:**
- Bootstrap/setup guides (Review/review1.md)
- One-time planning docs
- Duplicate content

**But:** Create separate dev-notes repo instead of deleting

---

## 🎯 CURRENT STATUS (Post-Organization)

### Root Directory NOW

```
/
├── .speckit.toml                    # Config example
├── pyproject.toml                   # Package metadata  
├── README.md                        # Main docs
├── CHANGELOG.md                     # History
├── LICENSE                          # Legal
├── CONTRIBUTING.md                  # Guidelines
├── CODE_OF_CONDUCT.md               # Community
├── SECURITY.md                      # Security
├── IMPLEMENTATION_ROADMAP.md        # 6-phase plan
├── PHASE_1_COMPLETE.md              # Current status
├── src/                             # Code
├── docs/                            # Documentation
├── tests/                           # Tests
├── templates/                       # Templates
├── scripts/                         # Scripts
├── memory/                          # Memory
├── media/                           # Media
├── htmlcov/                         # Coverage reports
└── Review/                          # Development context
    ├── review1.md
    ├── review2.md
    ├── CRITICAL_ASSESSMENT.md
    ├── DEPENDENCIES_AND_TESTING.md
    └── archive/                     # Historical docs
        ├── HONEST_ASSESSMENT.md
        ├── LIMITATIONS.md
        ├── STRUCTURE_*.md
        ├── FIX_SUMMARY.md
        ├── REHABILITATION-ENHANCEMENT-SUMMARY.md
        ├── FORK_COMPLETE.md
        └── YES_THIS_HELPS.md
```

### Key Changes

✅ **Moved to Review/archive/:**
- 9 historical/planning documents
- Keeps root clean
- Preserves history

✅ **Added to Review/:**
- CRITICAL_ASSESSMENT.md (Grade B+)
- DEPENDENCIES_AND_TESTING.md (Complete deps)

✅ **Kept in Root:**
- Active product files
- Current status docs
- User-facing content

---

## 🎯 RECOMMENDATIONS

### For This Weekend

1. ✅ **Keep current organization** - it's clean now
2. 🔜 **Add unit tests** to tests/unit/
3. 🔜 **Implement Bandit analyzer** in src/specify_cli/analyzers/
4. 🔜 **Wire CLI commands** in src/specify_cli/commands/

### For v0.2.0 Release

1. Archive PHASE_1_COMPLETE.md
2. Create PHASE_2_COMPLETE.md
3. Update README with real examples
4. Add CHANGELOG entries

### For v1.0 Release

1. Create separate `spec-kit-dev-notes` repo
2. Move entire Review/ directory there
3. Keep only production files in main repo
4. Link to dev-notes repo in CONTRIBUTING.md

---

## 📊 FILE COUNT

### Main Repo (Before Cleanup)
```
Root markdown files:  27
Moved to archive:      9
Remaining in root:    18
```

### Main Repo (After Cleanup)
```
Root markdown files:   9  (clean!)
Review/ files:         2
Review/archive/ files: 9
Total:                20
```

**Much cleaner!** ✅

---

## 🎯 SUMMARY

### What We Did
1. ✅ Moved 9 historical docs to Review/archive/
2. ✅ Created 2 new Review/ docs (assessment, dependencies)
3. ✅ Kept root clean (9 essential files)
4. ✅ Preserved all history

### Why This Matters
- **Users:** See clean, professional repo
- **Developers:** Have full context in Review/
- **Maintainers:** Can track project evolution
- **Future:** Easy to extract to dev-notes repo

### Next Steps
- Focus on implementation (Phase 2)
- Add tests as you build
- Archive each phase when complete
- Keep root directory clean

**Result:** Professional, maintainable repository structure ✨
