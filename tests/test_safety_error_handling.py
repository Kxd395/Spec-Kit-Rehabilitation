"""Test Safety analyzer error handling."""

import pytest
import shutil
from pathlib import Path
from specify_cli.analyzers.safety_analyzer import SafetyAnalyzer


def test_safety_missing_cli_raises(tmp_path: Path, monkeypatch):
    """Verify SafetyAnalyzer raises FileNotFoundError when CLI is missing."""
    # Mock shutil.which to return None (CLI not found)
    monkeypatch.setattr(shutil, "which", lambda _: None)

    # Create a minimal requirements.txt
    (tmp_path / "requirements.txt").write_text("flask==2.0.0\n")

    # Should raise FileNotFoundError
    with pytest.raises(FileNotFoundError) as exc_info:
        SafetyAnalyzer(tmp_path).run()

    assert "safety" in str(exc_info.value).lower()
