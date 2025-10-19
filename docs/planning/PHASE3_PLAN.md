# Phase 3: Coverage Improvements Plan

**Status**: 🚀 In Progress
**Start Date**: October 19, 2025
**Goal**: Increase code coverage from 24% to 70%+
**Estimated Duration**: 2-3 hours

---

## 📊 Current Coverage Status

**Overall Coverage**: 24%

**Low Coverage Modules** (Priority Targets):
- `github/extraction.py`: 10%
- `commands/init_impl.py`: 11%
- `ui/selector.py`: 13%
- `github/download.py`: 16%
- `vscode/settings.py`: 18%
- `ui/tracker.py`: 19%

**Medium Coverage Modules**:
- `logging_config.py`: 71%
- `gitutils.py`: 75%
- `baseline.py`: 81%

**High Coverage Modules** (>90%):
- Most command modules
- Configuration
- Analyzers

---

## 🎯 Phase 3 Goals

### Primary Goals
1. ✅ Increase overall coverage to 70%+
2. ✅ Bring all critical modules to 60%+ coverage
3. ✅ Maintain 100% test pass rate
4. ✅ Maintain zero linting/type errors
5. ✅ Document all new test patterns

### Success Criteria
- [ ] Overall coverage ≥ 70%
- [ ] No module below 40% coverage (except UI/experimental)
- [ ] All tests passing (100%)
- [ ] Zero quality gate failures
- [ ] Comprehensive test documentation

---

## 📋 Task Breakdown

### Task 1: Test GitHub Download Module
**File**: `tests/test_github_download.py` (new)
**Target**: `src/specify_cli/github/download.py`
**Current Coverage**: 16%
**Target Coverage**: 70%+

**Functions to Test**:
1. `fetch_latest_release(repo_owner, repo_name, token=None)`
   - ✅ Success case (valid repo)
   - ✅ Error case (invalid repo)
   - ✅ Error case (network failure)
   - ✅ Error case (auth required)

2. `download_template(release, template_dir, token=None)`
   - ✅ Success case (valid release)
   - ✅ Error case (no assets)
   - ✅ Error case (download failure)
   - ✅ Progress tracking validation

**Estimated Duration**: 45 minutes

---

### Task 2: Test GitHub Extraction Module
**File**: `tests/test_github_extraction.py` (new)
**Target**: `src/specify_cli/github/extraction.py`
**Current Coverage**: 10%
**Target Coverage**: 70%+

**Functions to Test**:
1. `extract_template(zip_path, extract_dir)`
   - ✅ Success case (valid zip)
   - ✅ Error case (corrupted zip)
   - ✅ Error case (invalid path)
   - ✅ Permission errors

2. Helper functions
   - ✅ File handling edge cases
   - ✅ Directory creation
   - ✅ Cleanup on failure

**Estimated Duration**: 30 minutes

---

### Task 3: Test Init Implementation Module
**File**: `tests/test_init_impl.py` (new)
**Target**: `src/specify_cli/commands/init_impl.py`
**Current Coverage**: 11%
**Target Coverage**: 60%+

**Functions to Test**:
1. `init(project_name, template, options)`
   - ✅ Success case (standard init)
   - ✅ Git initialization
   - ✅ Configuration setup
   - ✅ Template selection

2. Error cases
   - ✅ Directory exists
   - ✅ Invalid template
   - ✅ Permission errors
   - ✅ Git failures

**Estimated Duration**: 45 minutes

---

### Task 4: Test Logging Config Module
**File**: `tests/test_logging_config.py` (expand existing)
**Target**: `src/specify_cli/logging_config.py`
**Current Coverage**: 71%
**Target Coverage**: 90%+

**Additional Tests Needed**:
1. `ColoredFormatter` edge cases
   - ✅ All log levels
   - ✅ Exception formatting
   - ✅ Long messages
   - ✅ Special characters

2. `setup_logging()` variations
   - ✅ File logging
   - ✅ Multiple handlers
   - ✅ Error conditions

**Estimated Duration**: 30 minutes

---

### Task 5: Test UI Modules (Optional)
**Files**: `tests/test_ui_selector.py`, `tests/test_ui_tracker.py` (new)
**Targets**: `src/specify_cli/ui/selector.py`, `ui/tracker.py`
**Current Coverage**: 13%, 19%
**Target Coverage**: 40%+ (lower priority, interactive)

**Note**: UI modules are interactive and harder to test. May skip if time-constrained.

**Estimated Duration**: 1 hour (if pursued)

---

## 🛠️ Implementation Strategy

### Step 1: Setup Test Infrastructure
1. Create test fixture utilities
2. Setup mock GitHub API responses
3. Create temporary file/directory fixtures
4. Setup httpx mocking for network calls

### Step 2: Implement Tests (Priority Order)
1. GitHub download (highest impact)
2. GitHub extraction (related to #1)
3. Init implementation (critical path)
4. Logging config (complete existing coverage)
5. UI modules (if time permits)

### Step 3: Validation
1. Run full test suite after each module
2. Check coverage reports
3. Verify no regressions
4. Update documentation

### Step 4: Documentation
1. Document test patterns used
2. Update CONTRIBUTING.md with test examples
3. Create PHASE3_COMPLETE.md
4. Update SESSION_SUMMARY.md

---

## 📐 Test Patterns to Use

### Pattern 1: Mocking HTTP Requests
```python
import httpx
import respx

@respx.mock
def test_fetch_release_success():
    respx.get("https://api.github.com/repos/owner/repo/releases/latest").mock(
        return_value=httpx.Response(200, json={"tag_name": "v1.0.0"})
    )
    result = fetch_latest_release("owner", "repo")
    assert result["tag_name"] == "v1.0.0"
```

### Pattern 2: Temporary File Fixtures
```python
import pytest
from pathlib import Path

@pytest.fixture
def temp_zip(tmp_path):
    zip_path = tmp_path / "test.zip"
    # Create test zip file
    return zip_path

def test_extraction(temp_zip):
    extract_dir = temp_zip.parent / "extracted"
    extract_template(temp_zip, extract_dir)
    assert extract_dir.exists()
```

### Pattern 3: Exception Testing
```python
import pytest
from zipfile import BadZipFile

def test_extract_bad_zip(tmp_path):
    bad_zip = tmp_path / "bad.zip"
    bad_zip.write_text("not a zip")

    with pytest.raises(BadZipFile):
        extract_template(bad_zip, tmp_path / "out")
```

---

## 📊 Expected Outcomes

### Coverage Improvements
| Module | Current | Target | Improvement |
|--------|---------|--------|-------------|
| github/download.py | 16% | 70% | +54% |
| github/extraction.py | 10% | 70% | +60% |
| commands/init_impl.py | 11% | 60% | +49% |
| logging_config.py | 71% | 90% | +19% |
| **Overall** | **24%** | **70%** | **+46%** |

### Quality Metrics (Maintain)
- ✅ Ruff errors: 0
- ✅ Mypy errors: 0
- ✅ Test pass rate: 100%
- ✅ Pre-commit hooks: All passing

---

## 🚀 Getting Started

**First Command**:
```bash
# Create test file for github download
touch tests/test_github_download.py

# Install testing dependencies (if needed)
uv pip install respx pytest-httpx
```

**First Test to Write**:
```python
# tests/test_github_download.py
import pytest
import httpx
import respx
from specify_cli.github.download import fetch_latest_release

@respx.mock
def test_fetch_latest_release_success():
    """Test successful fetch of latest release from GitHub."""
    respx.get(
        "https://api.github.com/repos/test-owner/test-repo/releases/latest"
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "tag_name": "v1.0.0",
                "name": "Test Release",
                "assets": [{"name": "template.zip"}]
            }
        )
    )

    result = fetch_latest_release("test-owner", "test-repo")

    assert result is not None
    assert result["tag_name"] == "v1.0.0"
    assert result["name"] == "Test Release"
```

---

## ✅ Completion Checklist

### Before Starting
- [x] Phase 1 & 2 complete
- [x] Repository in clean state
- [x] All quality gates passing
- [x] Plan documented

### During Implementation
- [ ] Task 1: GitHub download tests (70%+ coverage)
- [ ] Task 2: GitHub extraction tests (70%+ coverage)
- [ ] Task 3: Init implementation tests (60%+ coverage)
- [ ] Task 4: Logging config tests (90%+ coverage)
- [ ] All tests passing after each module
- [ ] Coverage verified after each module

### After Completion
- [ ] Overall coverage ≥ 70%
- [ ] Full test suite passing
- [ ] Zero quality gate failures
- [ ] PHASE3_COMPLETE.md created
- [ ] SESSION_SUMMARY.md updated
- [ ] All commits pushed to GitHub

---

**Status**: Ready to begin Task 1 🚀

**Next Action**: Create `tests/test_github_download.py` and implement first test case
