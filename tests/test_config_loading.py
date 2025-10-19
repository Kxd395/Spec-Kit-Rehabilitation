"""Test configuration loading and precedence."""

from pathlib import Path
from specify_cli.config import load_config


def test_config_env_overrides(tmp_path: Path, monkeypatch):
    """Verify environment variables override TOML file settings."""
    # Create TOML config with LOW threshold
    config_file = tmp_path / ".speckit.toml"
    config_file.write_text("[analysis]\nfail_on='LOW'\n")

    # Set ENV variable to MEDIUM (should override TOML)
    monkeypatch.setenv("SPECKIT_FAIL_ON", "MEDIUM")

    # Load config
    cfg = load_config(tmp_path)

    # Verify ENV variable took precedence
    assert cfg.analysis.fail_on == "MEDIUM", f"Expected MEDIUM from ENV, got {cfg.analysis.fail_on}"


def test_config_defaults_when_no_file(tmp_path: Path):
    """Verify default values are used when no config file exists."""
    # Load config from directory with no .speckit.toml
    cfg = load_config(tmp_path)

    # Verify defaults
    assert cfg.analysis.fail_on == "HIGH"  # Default severity
    assert cfg.output.format == "sarif"  # Default format
    assert cfg.output.directory == ".speckit/analysis"  # Default directory
