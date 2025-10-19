#!/usr/bin/env python3
"""
Version synchronization script for Spec-Kit CLI.

Ensures version numbers are consistent across:
- pyproject.toml
- src/specify_cli/__init__.py
- CHANGELOG.md (header)

Usage:
    python scripts/sync_version.py               # Check consistency
    python scripts/sync_version.py --set 1.0.0   # Set new version
    python scripts/sync_version.py --bump minor  # Bump version (major|minor|patch)
"""

from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Tuple, Optional
import argparse


def get_project_root() -> Path:
    """Get the project root directory."""
    script_path = Path(__file__).resolve()
    # scripts/sync_version.py -> project_root
    return script_path.parent.parent


def get_version_from_pyproject(project_root: Path) -> Optional[str]:
    """Extract version from pyproject.toml."""
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    return match.group(1) if match else None


def get_version_from_init(project_root: Path) -> Optional[str]:
    """Extract version from __init__.py."""
    init_path = project_root / "src" / "specify_cli" / "__init__.py"
    if not init_path.exists():
        return None

    content = init_path.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*"([^"]+)"', content, re.MULTILINE)
    return match.group(1) if match else None


def set_version_in_pyproject(project_root: Path, version: str) -> None:
    """Update version in pyproject.toml."""
    pyproject_path = project_root / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")

    # Replace version line
    new_content = re.sub(
        r'^version\s*=\s*"[^"]+"',
        f'version = "{version}"',
        content,
        flags=re.MULTILINE,
    )

    pyproject_path.write_text(new_content, encoding="utf-8")
    print(f'✅ Updated pyproject.toml: version = "{version}"')


def set_version_in_init(project_root: Path, version: str) -> None:
    """Update version in __init__.py."""
    init_path = project_root / "src" / "specify_cli" / "__init__.py"
    content = init_path.read_text(encoding="utf-8")

    # Check if __version__ exists
    if "__version__" in content:
        # Replace existing version
        new_content = re.sub(
            r'^__version__\s*=\s*"[^"]+"',
            f'__version__ = "{version}"',
            content,
            flags=re.MULTILINE,
        )
    else:
        # Add __version__ after imports, before __all__
        lines = content.split("\n")
        insert_pos = 0

        # Find position after imports, before __all__
        for i, line in enumerate(lines):
            if line.startswith("__all__"):
                insert_pos = i
                break
            elif line.startswith("import ") or line.startswith("from "):
                insert_pos = i + 1

        lines.insert(insert_pos, f'__version__ = "{version}"')
        lines.insert(insert_pos + 1, "")
        new_content = "\n".join(lines)

    init_path.write_text(new_content, encoding="utf-8")
    print(f'✅ Updated __init__.py: __version__ = "{version}"')


def update_changelog_header(project_root: Path, version: str) -> None:
    """Update CHANGELOG.md header with new version."""
    changelog_path = project_root / "CHANGELOG.md"
    if not changelog_path.exists():
        print("⚠️  CHANGELOG.md not found, skipping")
        return

    content = changelog_path.read_text(encoding="utf-8")

    # Check if version already has an entry
    if re.search(rf"^## \[{re.escape(version)}\]", content, re.MULTILINE):
        print(f"✅ CHANGELOG.md already has entry for version {version}")
        return

    # Add new version header at the top (after the main title)
    lines = content.split("\n")
    insert_pos = 0

    # Find position after main title
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_pos = i + 1
            # Skip empty lines after title
            while insert_pos < len(lines) and not lines[insert_pos].strip():
                insert_pos += 1
            break

    # Insert new version header
    from datetime import date

    today = date.today().strftime("%Y-%m-%d")
    lines.insert(insert_pos, f"## [{version}] - {today}")
    lines.insert(insert_pos + 1, "")
    lines.insert(insert_pos + 2, "### Added")
    lines.insert(insert_pos + 3, "- ")
    lines.insert(insert_pos + 4, "")
    lines.insert(insert_pos + 5, "### Changed")
    lines.insert(insert_pos + 6, "- ")
    lines.insert(insert_pos + 7, "")

    new_content = "\n".join(lines)
    changelog_path.write_text(new_content, encoding="utf-8")
    print(f"✅ Updated CHANGELOG.md with version {version} header")


def bump_version(version: str, part: str) -> str:
    """Bump version number.

    Args:
        version: Current version (e.g., "0.1.0a4")
        part: Part to bump ('major', 'minor', 'patch')

    Returns:
        New version string
    """
    # Parse version (supports alpha/beta/rc suffixes)
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)([a-z]+\d+)?$", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")

    major, minor, patch, suffix = match.groups()
    major, minor, patch = int(major), int(minor), int(patch)

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump part: {part}. Use 'major', 'minor', or 'patch'")

    # Remove suffix when bumping (e.g., 0.1.0a4 -> 0.1.1)
    return f"{major}.{minor}.{patch}"


def check_version_consistency(project_root: Path) -> Tuple[bool, str]:
    """Check if versions are consistent across files.

    Returns:
        (is_consistent, message)
    """
    pyproject_version = get_version_from_pyproject(project_root)
    init_version = get_version_from_init(project_root)

    versions = {
        "pyproject.toml": pyproject_version,
        "__init__.py": init_version,
    }

    # Filter out None values
    versions = {k: v for k, v in versions.items() if v is not None}

    if not versions:
        return False, "❌ No version found in any file"

    unique_versions = set(versions.values())

    if len(unique_versions) == 1:
        version = unique_versions.pop()
        return True, f"✅ All versions consistent: {version}"
    else:
        msg = "❌ Version mismatch detected:\n"
        for file, version in versions.items():
            msg += f"  - {file}: {version}\n"
        return False, msg


def main():
    parser = argparse.ArgumentParser(description="Synchronize version numbers across project files")
    parser.add_argument(
        "--set",
        metavar="VERSION",
        help="Set version to specified value (e.g., 1.0.0)",
    )
    parser.add_argument(
        "--bump",
        metavar="PART",
        choices=["major", "minor", "patch"],
        help="Bump version (major, minor, or patch)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check version consistency (default if no other flags)",
    )

    args = parser.parse_args()

    project_root = get_project_root()

    # Default behavior: check consistency
    if not args.set and not args.bump:
        args.check = True

    if args.check:
        is_consistent, message = check_version_consistency(project_root)
        print(message)
        sys.exit(0 if is_consistent else 1)

    # Get current version
    current_version = get_version_from_pyproject(project_root)
    if not current_version:
        print("❌ Could not determine current version from pyproject.toml")
        sys.exit(1)

    # Determine new version
    if args.set:
        new_version = args.set
    elif args.bump:
        new_version = bump_version(current_version, args.bump)
    else:
        print("❌ No action specified. Use --set, --bump, or --check")
        sys.exit(1)

    print(f"Updating version: {current_version} → {new_version}")
    print()

    # Update all files
    set_version_in_pyproject(project_root, new_version)
    set_version_in_init(project_root, new_version)
    update_changelog_header(project_root, new_version)

    print()
    print(f"✅ Version synchronized to {new_version}")
    print()
    print("Next steps:")
    print("  1. Review the changes: git diff")
    print("  2. Update CHANGELOG.md with actual changes")
    print("  3. Commit: git add -A && git commit -m 'chore: bump version to {new_version}'")


if __name__ == "__main__":
    main()
