"""Git utilities for changed file detection."""

from __future__ import annotations
import subprocess
from pathlib import Path
from typing import List


def is_git_repo(path: Path | str | None = None) -> bool:
    """Check if directory is a git repository.

    Args:
        path: Directory path to check (defaults to current directory)

    Returns:
        True if path is in a git repository, False otherwise
    """
    if path is None:
        check_path = Path.cwd()
    elif isinstance(path, str):
        check_path = Path(path)
    else:
        check_path = path

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            cwd=check_path,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False


def get_changed_files(repo_root: Path | str | None = None) -> List[Path]:
    """Get list of changed files in git repository.

    Args:
        repo_root: Root of the git repository (defaults to current directory)

    Returns:
        List of paths to changed files
    """
    if repo_root is None:
        root = Path.cwd()
    elif isinstance(repo_root, str):
        root = Path(repo_root)
    else:
        root = repo_root

    try:
        # Get unstaged and staged changes
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return [root / p for p in result.stdout.splitlines() if p.strip()]
    except Exception:
        pass

    return []


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
