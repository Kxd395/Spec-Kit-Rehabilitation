"""Test config precedence and validation."""

from specify_cli.config import load_config


class TestConfigPrecedence:
    """Test environment variable precedence over defaults."""

    def test_env_overrides_defaults(self, tmp_path, monkeypatch):
        """Verify SPECKIT_* env vars override config file."""
        # Set environment variables
        monkeypatch.setenv("SPECKIT_OUT_DIR", str(tmp_path / "custom_output"))
        monkeypatch.setenv("SPECKIT_BANDIT", "false")

        config = load_config(repo_root=tmp_path)

        assert str(config.output.directory) == str(tmp_path / "custom_output")
        assert config.analyzers.bandit is False
        assert config.analyzers.safety is True  # Should remain default

    def test_all_env_vars_respected(self, tmp_path, monkeypatch):
        """Test that all environment variables are properly respected."""
        monkeypatch.setenv("SPECKIT_OUT_DIR", str(tmp_path / "env_output"))
        monkeypatch.setenv("SPECKIT_BANDIT", "false")
        monkeypatch.setenv("SPECKIT_SAFETY", "false")

        config = load_config(repo_root=tmp_path)

        assert str(config.output.directory) == str(tmp_path / "env_output")
        assert config.analyzers.bandit is False
        assert config.analyzers.safety is False
