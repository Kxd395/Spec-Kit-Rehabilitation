"""Git utilities for changed file detection."""
from __future__ import annotations
import subprocess
from pathlib import Path
from typing import List


def changed_python_files(repo_root: Path) -> List[Path]:
    """Get list of changed Python files in git repo.
    
    Args:
        repo_root: Root of the git repository
        
    Returns:
        List of paths to changed .py files
    """
    try:
        # Try to get changed files from git diff
        res = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            return [Path(repo_root, p) for p in res.stdout.splitlines() if p.endswith(".py")]
    except Exception:
        pass
    
    # Fallback: list all tracked Python files
    try:
        res = subprocess.run(
            ["git", "ls-files", "*.py"],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0:
            return [Path(repo_root, p) for p in res.stdout.splitlines() if p]
    except Exception:
        pass
    
    return []
