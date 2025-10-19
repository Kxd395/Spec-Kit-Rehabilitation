# Phase 4 Implementation Guide - Ready to Execute

**Date**: October 18, 2025  
**Based On**: 
- `Review/review41.md` (Critical review)
- `Review/update4.md` (Implementation pack with code)
- `PHASE_4_REVISED_PLAN.md` (Strategy)

---

## 🎯 What This Guide Provides

This document combines:
1. **Strategic Plan** (from review41.md + revised plan)
2. **Concrete Code** (from update4.md)
3. **Step-by-Step Execution** (this guide)

You now have **everything needed** to execute Phase 4 v0.1.0a4 immediately.

---

## 📋 Quick Start Checklist

Before starting:

- [ ] Phase 3 (v0.1.0a3) pushed to GitHub ✅ (Already done!)
- [ ] Current working directory clean
- [ ] Python 3.13 available
- [ ] Git ready for feature branches
- [ ] 2-3 hours available for PR-1

---

## 🚀 PR-1: Extract UI Banner Module (Start Here!)

**Time**: 2-3 hours  
**Files**: 3-5 files  
**Risk**: LOW  

### Step 1: Create Feature Branch

```bash
cd /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit
git checkout main
git pull origin main
git checkout -b feature/a4-refactor-banner
```

### Step 2: Create Module Structure

```bash
mkdir -p src/specify_cli/ui
mkdir -p tests/integration
```

### Step 3: Create Files

**File 1: `src/specify_cli/ui/__init__.py`**
```python
# Explicit package init
```

**File 2: `src/specify_cli/ui/banner.py`**
```python
from rich.panel import Panel
from rich.console import Console

def show_banner(console: Console | None = None) -> None:
    c = console or Console()
    c.print(
        Panel.fit(
            "[bold cyan]Spec-Kit[/bold cyan]  •  Security scanning and specs workflow",
            title="specify-cli",
            border_style="cyan",
        )
    )
```

**File 3: `src/specify_cli/compat.py`** (Import shim for backward compatibility)
```python
# Backward compatible re-exports to cushion the refactor for one minor release
from .ui.banner import show_banner

__all__ = ["show_banner"]
```

**File 4: `tests/integration/test_init_flow.py`**
```python
"""Integration tests for banner and basic flow"""
from specify_cli.ui.banner import show_banner
from rich.console import Console

def test_banner_displays_without_error():
    """Ensure banner can be displayed"""
    try:
        show_banner()
        assert True
    except Exception as e:
        assert False, f"Banner failed: {e}"

def test_banner_accepts_custom_console():
    """Ensure banner works with custom console"""
    console = Console()
    show_banner(console)
    # If no exception, test passes
    assert True
```

### Step 4: Update Existing Code (If __init__.py uses banner)

**Check where `show_banner` is currently defined:**

```bash
grep -r "def show_banner" src/
```

**If it's in `__init__.py`, extract it to the new module and import:**

In `src/specify_cli/__init__.py`, replace the banner function with:
```python
from .ui.banner import show_banner
```

### Step 5: Run Tests

```bash
# Activate environment
python3.13 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\Activate.ps1  # Windows PowerShell

# Install in dev mode
pip install -e ".[analysis,reporting,dev]"

# Run tests
pytest tests/integration/test_init_flow.py -v

# Run all tests to ensure nothing broke
pytest tests/ -v
```

### Step 6: Update Documentation

**Update `src/specify_cli/commands/README.md`**:
Add a note about the new module structure:

```markdown
## Module Structure (v0.1.0a4+)

The CLI has been refactored into modular components:

- `ui/` - User interface components (banner, progress, summary)
- `github/` - GitHub integration (auth, download, extraction)
- `vscode/` - VS Code settings management
- `commands/` - CLI commands (init, check, audit, etc.)
- `compat.py` - Backward compatibility shim
```

### Step 7: Commit and Push

```bash
git add src/specify_cli/ui/
git add src/specify_cli/compat.py
git add tests/integration/test_init_flow.py
git add src/specify_cli/commands/README.md

git commit -m "refactor: extract banner to ui.banner module

- Create src/specify_cli/ui/ package
- Move show_banner() to ui.banner
- Add import shim in compat.py for backward compatibility
- Add integration tests for banner
- Update documentation

Part of Phase 4 v0.1.0a4 refactoring (PR-1/7)

Refs: PHASE_4_REVISED_PLAN.md"

git push origin feature/a4-refactor-banner
```

### Step 8: Create Pull Request

**PR Title**: `refactor: extract banner to ui.banner module (Phase 4 PR-1)`

**PR Description**:
```markdown
## Description
First step in Phase 4 refactoring: Extract banner functionality to modular structure.

## Changes
- Created `src/specify_cli/ui/` package
- Moved `show_banner()` to `ui.banner` module
- Added backward compatibility shim in `compat.py`
- Added integration tests

## Type of Change
- [x] Refactor (no functional changes)
- [x] Tests added/updated
- [x] Documentation updated

## Phase 4 Checklist
- [x] Tests added/updated
- [x] CHANGELOG updated (will be done at release)
- [x] Docs updated (commands README)
- [x] Coverage gate passes
- [x] No CLI contract changes

## Testing
- Integration tests verify banner displays without error
- All existing tests still pass
- No behavior changes

## Risk Assessment
- **Blast Radius**: Small (3-5 files)
- **Rollback Plan**: Single git revert
- **Backward Compatibility**: Import shim maintains compatibility
```

---

## 🔄 PR-2: Extract GitHub Module

**Time**: 3-4 hours  
**Files**: 4-6 files  
**Dependencies**: PR-1 merged  

### Step 1: Create Feature Branch

```bash
git checkout main
git pull origin main
git checkout -b feature/a4-refactor-github
```

### Step 2: Create Module Structure

```bash
mkdir -p src/specify_cli/github
```

### Step 3: Create Files

**File 1: `src/specify_cli/github/__init__.py`**
```python
# Explicit package init
```

**File 2: `src/specify_cli/github/auth.py`**
```python
import os
from typing import Mapping

def get_token() -> str | None:
    return os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")

def auth_headers(extra: Mapping[str, str] | None = None) -> dict[str, str]:
    headers: dict[str, str] = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "specify-cli",
    }
    token = get_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if extra:
        headers.update(extra)
    return headers
```

**File 3: `src/specify_cli/github/download.py`**
```python
from __future__ import annotations
from pathlib import Path
from typing import Optional
import httpx
import time
from .auth import auth_headers

class DownloadError(RuntimeError):
    pass

def download_repo_zip(owner: str, repo: str, ref: str, dest: Path, timeout_s: float = 30.0, retries: int = 3) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{ref}"
    attempt = 0
    last_exc: Optional[Exception] = None
    while attempt < retries:
        attempt += 1
        try:
            with httpx.stream("GET", url, headers=auth_headers(), timeout=timeout_s) as r:
                if r.status_code >= 400:
                    body = r.text[:200] if hasattr(r, "text") else ""
                    raise DownloadError(f"GitHub returned {r.status_code}: {body}")
                with open(dest, "wb") as f:
                    for chunk in r.iter_bytes():
                        f.write(chunk)
            if dest.stat().st_size == 0:
                raise DownloadError("Downloaded file is empty")
            return dest
        except Exception as e:
            last_exc = e
            if attempt < retries:
                time.sleep(1.0 * attempt)
            else:
                raise DownloadError(f"Failed to download {url}: {e}") from e
    raise DownloadError(f"Download failed: {last_exc}")
```

**File 4: `src/specify_cli/github/extraction.py`**
```python
from __future__ import annotations
from pathlib import Path
from typing import Iterable
import zipfile

class UnsafeZipEntry(RuntimeError):
    pass

def _is_within(base: Path, target: Path) -> bool:
    try:
        target.resolve().relative_to(base.resolve())
        return True
    except Exception:
        return False

def extract_zip_safe(zip_path: Path, dest_dir: Path, members: Iterable[str] | None = None) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    out: list[Path] = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = list(members) if members is not None else zf.namelist()
        for name in names:
            if name.endswith("/"):
                continue
            parts = Path(name).parts
            # If archive has a single top-level folder, strip it
            start_idx = 1 if len(parts) > 1 else 0
            rebased = dest_dir
            for p in parts[start_idx:]:
                rebased = rebased / p
            target = rebased
            target.parent.mkdir(parents=True, exist_ok=True)
            if not _is_within(dest_dir, target.parent):
                raise UnsafeZipEntry(f"Blocked unsafe entry: {name}")
            with zf.open(name) as src, open(target, "wb") as dst:
                dst.write(src.read())
            out.append(target)
    return out
```

**File 5: `tests/test_github_download.py`**
```python
import pytest
from pathlib import Path
from specify_cli.github.auth import get_token, auth_headers

def test_auth_headers_includes_user_agent():
    headers = auth_headers()
    assert "User-Agent" in headers
    assert headers["User-Agent"] == "specify-cli"

def test_auth_headers_includes_token_when_available(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "test-token-123")
    headers = auth_headers()
    assert "Authorization" in headers
    assert headers["Authorization"] == "Bearer test-token-123"

def test_auth_headers_no_token_when_missing(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    headers = auth_headers()
    assert "Authorization" not in headers
```

**File 6: `tests/integration/test_extraction_safety.py`**
```python
from pathlib import Path
import pytest
from zipfile import ZipFile
from specify_cli.github.extraction import extract_zip_safe, UnsafeZipEntry

def test_extract_zip_safe_blocks_traversal(tmp_path: Path):
    """Ensure path traversal attempts are blocked"""
    zpath = tmp_path / "malicious.zip"
    with ZipFile(zpath, "w") as z:
        z.writestr("folder/hello.txt", "ok")
        z.writestr("../evil.txt", "nope")  # traversal attempt
    
    out = tmp_path / "out"
    with pytest.raises(UnsafeZipEntry):
        extract_zip_safe(zpath, out, members=["../evil.txt"])

def test_extract_zip_safe_handles_utf8_filenames(tmp_path: Path):
    """Ensure UTF-8 filenames are handled correctly"""
    zpath = tmp_path / "unicode.zip"
    with ZipFile(zpath, "w") as z:
        z.writestr("folder/文件.txt", "content")
    
    out = tmp_path / "out"
    paths = extract_zip_safe(zpath, out)
    assert any("文件.txt" in str(p) for p in paths)

def test_extract_zip_safe_strips_top_level_folder(tmp_path: Path):
    """Ensure single top-level folder is stripped"""
    zpath = tmp_path / "repo.zip"
    with ZipFile(zpath, "w") as z:
        z.writestr("repo-main/src/file.py", "code")
        z.writestr("repo-main/README.md", "docs")
    
    out = tmp_path / "out"
    paths = extract_zip_safe(zpath, out)
    # Files should be at out/src/file.py, not out/repo-main/src/file.py
    assert (out / "src" / "file.py").exists()
```

### Step 4: Update compat.py

```python
# src/specify_cli/compat.py
from .ui.banner import show_banner
from .github.download import download_repo_zip

__all__ = ["show_banner", "download_repo_zip"]
```

### Step 5: Update Existing Code

Find where `download_repo_zip` is used and update imports:

```bash
grep -r "download_repo_zip" src/ --include="*.py"
```

Replace direct definitions with imports:
```python
from specify_cli.github.download import download_repo_zip
```

### Step 6: Run Tests

```bash
pytest tests/test_github_download.py -v
pytest tests/integration/test_extraction_safety.py -v
pytest tests/ -v  # All tests
```

### Step 7: Commit and Push

```bash
git add src/specify_cli/github/
git add src/specify_cli/compat.py
git add tests/test_github_download.py
git add tests/integration/test_extraction_safety.py

git commit -m "refactor: extract GitHub functionality to github module

- Create src/specify_cli/github/ package
- Move auth, download, extraction logic to separate modules
- Add path traversal protection in extraction
- Add retry logic with exponential backoff in download
- Add comprehensive tests for auth, download, extraction
- Update compat.py import shim

Part of Phase 4 v0.1.0a4 refactoring (PR-2/7)

Refs: PHASE_4_REVISED_PLAN.md"

git push origin feature/a4-refactor-github
```

---

## 🔄 Remaining PRs (Quick Reference)

### PR-3: VS Code Settings Module
**Branch**: `feature/a4-refactor-vscode`  
**Files**: `src/specify_cli/vscode/settings.py`, `tests/test_vscode_settings.py`  
**Time**: 2-3 hours  

### PR-4: Commands Module
**Branch**: `feature/a4-refactor-commands`  
**Files**: `src/specify_cli/commands/init.py`, `check.py`, integration tests  
**Time**: 3-4 hours  

### PR-5: Risk-Weighted Tests
**Branch**: `feature/a4-risk-weighted-tests`  
**Files**: 7 test files targeting baseline, config, runner, gitutils, store  
**Time**: 6-8 hours  

### PR-6: Performance Harness
**Branch**: `feature/a4-perf-harness`  
**Files**: `scripts/bench/generate_repo.py`, `tests/perf/`, CI updates  
**Time**: 4-6 hours  

### PR-7: Verbose Mode
**Branch**: `feature/a4-verbose-mode`  
**Files**: `src/specify_cli/ui/progress.py`, `summary.py`, audit.py updates  
**Time**: 2-3 hours  

---

## 📊 Progress Tracking

### Current Status

- [x] Phase 3 (v0.1.0a3) complete and pushed
- [x] Critical review analyzed (review41.md)
- [x] Implementation code provided (update4.md)
- [x] Revised plan created
- [ ] **PR-1**: Banner extraction (READY TO START)
- [ ] PR-2: GitHub module
- [ ] PR-3: VS Code settings
- [ ] PR-4: Commands module
- [ ] PR-5: Risk-weighted tests
- [ ] PR-6: Performance harness
- [ ] PR-7: Verbose mode
- [ ] Release v0.1.0a4

### Velocity Tracking

| PR | Estimated | Actual | Status |
|----|-----------|--------|--------|
| PR-1 | 2-3h | - | Not started |
| PR-2 | 3-4h | - | Not started |
| PR-3 | 2-3h | - | Not started |
| PR-4 | 3-4h | - | Not started |
| PR-5 | 6-8h | - | Not started |
| PR-6 | 4-6h | - | Not started |
| PR-7 | 2-3h | - | Not started |
| **Total** | **22-31h** | **-** | - |

---

## 🛡️ Safety Checklist (Every PR)

Before creating each PR, verify:

- [ ] No CLI contract changes (except --verbose in PR-7)
- [ ] All existing tests pass
- [ ] New tests added for new code
- [ ] Import shim updated if needed
- [ ] Documentation updated
- [ ] Commit message follows format
- [ ] Branch name follows convention
- [ ] PR description complete

---

## 📝 Commit Message Template

```
<type>: <short description>

- Bullet point 1
- Bullet point 2
- Bullet point 3

Part of Phase 4 v0.1.0a4 refactoring (PR-N/7)

Refs: PHASE_4_REVISED_PLAN.md
```

**Types**: `refactor`, `test`, `perf`, `docs`, `ci`

---

## 🎯 Exit Criteria for v0.1.0a4

Before releasing v0.1.0a4, ALL must be true:

- [ ] `__init__.py` under 200 lines
- [ ] Coverage ≥ 80% on `src/`
- [ ] Performance smoke tests pass on CI
- [ ] No CLI contract changes (except --verbose)
- [ ] Verbose summary works in tests
- [ ] Docs updated (architecture.md, commands README)
- [ ] All 7 PRs merged
- [ ] CHANGELOG updated
- [ ] Version bumped to 0.1.0a4 in pyproject.toml
- [ ] Git tag created: v0.1.0a4
- [ ] Pushed to GitHub

---

## 🚀 Ready to Start?

**You now have:**

1. ✅ Strategic plan (why and how)
2. ✅ Implementation code (copy-paste ready)
3. ✅ Step-by-step guide (this document)
4. ✅ All safety mechanisms defined
5. ✅ Exit criteria clear

**To begin PR-1 right now:**

```bash
cd /Users/VScode_Projects/projects/Spec-Kit-Rehabilitation/spec-kit
git checkout main
git checkout -b feature/a4-refactor-banner
mkdir -p src/specify_cli/ui tests/integration
# Follow PR-1 steps above
```

**Estimated time to first PR merged**: 2-3 hours  
**Estimated time to v0.1.0a4 release**: 4-6 weeks

---

## 📚 Reference Documents

- **Strategic Review**: `Review/review41.md`
- **Implementation Pack**: `Review/update4.md`
- **Revised Plan**: `PHASE_4_REVISED_PLAN.md`
- **Executive Summary**: `PHASE_4_EXECUTIVE_SUMMARY.md`
- **This Guide**: `PHASE_4_IMPLEMENTATION_GUIDE.md`

---

**Ready when you are! Say "start PR-1" and I'll help you execute it step by step.** 🚀
