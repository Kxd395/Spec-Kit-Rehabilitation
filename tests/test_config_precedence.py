"""Test config precedence and validation."""
import os
import pytest
from specify_cli.config import load_config


class TestConfigPrecedence:
    """Test environment variable precedence over defaults."""
    
    def test_env_overrides_defaults(self, tmp_path, monkeypatch):
        """Verify SPECKIT_* env vars override config file."""
        # Set environment variables
        monkeypatch.setenv("SPECKIT_OUTPUT_DIR", str(tmp_path / "custom_output"))
        monkeypatch.setenv("SPECKIT_BANDIT_ENABLED", "false")
        monkeypatch.setenv("SPECKIT_SAFETY_ENABLED", "true")
        
        config = load_config()
        
        assert config.output_dir == tmp_path / "custom_output"
        assert config.bandit_enabled is False
        assert config.safety_enabled is True
    
    def test_all_env_vars_respected(self, tmp_path, monkeypatch):
        """Verify all SPECKIT_* environment variables work."""
        monkeypatch.setenv("SPECKIT_OUTPUT_DIR", str(tmp_path / "out"))
        monkeypatch.setenv("SPECKIT_BANDIT_ENABLED", "true")
        monkeypatch.setenv("SPECKIT_SAFETY_ENABLED", "false")
        monkeypatch.setenv("SPECKIT_EXCLUDE_PATHS", "node_modules,*.min.js")
        
        config = load_config()
        
        assert config.output_dir == tmp_path / "out"
        assert config.bandit_enabled is True
        assert config.safety_enabled is False
        assert "node_modules" in config.exclude_paths
