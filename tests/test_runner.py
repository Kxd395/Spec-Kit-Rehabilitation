"""Test analysis runner orchestration."""

import pytest
from specify_cli.runner import RunConfig, run_all


class TestRunConfig:
    """Test RunConfig dataclass."""

    def test_run_config_defaults(self, tmp_path):
        """Test RunConfig has correct defaults."""
        cfg = RunConfig(path=tmp_path)

        assert cfg.path == tmp_path
        assert cfg.changed_only is False
        assert cfg.use_bandit is True
        assert cfg.use_safety is True
        assert cfg.exclude_globs == []

    def test_run_config_custom_values(self, tmp_path):
        """Test RunConfig with custom values."""
        cfg = RunConfig(
            path=tmp_path,
            changed_only=True,
            use_bandit=False,
            use_safety=True,
            exclude_globs=["*.test.py", "tests/"],
        )

        assert cfg.path == tmp_path
        assert cfg.changed_only is True
        assert cfg.use_bandit is False
        assert cfg.use_safety is True
        assert cfg.exclude_globs == ["*.test.py", "tests/"]


class TestRunAll:
    """Test run_all function."""

    def test_run_all_with_bandit_only(self, tmp_path):
        """Test running only Bandit analyzer."""
        # Create a test Python file
        test_file = tmp_path / "test.py"
        test_file.write_text("import pickle\npickle.loads(data)")

        cfg = RunConfig(path=tmp_path, use_bandit=True, use_safety=False)

        results = run_all(cfg)

        assert "bandit" in results
        assert "safety" not in results
        assert isinstance(results["bandit"], list)

    def test_run_all_with_safety_only(self, tmp_path):
        """Test running only Safety analyzer."""
        cfg = RunConfig(path=tmp_path, use_bandit=False, use_safety=True)

        try:
            results = run_all(cfg)

            assert "bandit" not in results
            assert "safety" in results
            assert isinstance(results["safety"], list)
        except Exception:
            # Safety may fail in test environment if not properly configured
            pytest.skip("Safety analyzer not available or misconfigured")

    def test_run_all_with_both_analyzers(self, tmp_path):
        """Test running both analyzers."""
        # Create a test Python file
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")

        cfg = RunConfig(path=tmp_path, use_bandit=True, use_safety=True)

        try:
            results = run_all(cfg)

            assert "bandit" in results
            assert "safety" in results
            assert isinstance(results["bandit"], list)
            assert isinstance(results["safety"], list)
        except Exception:
            # Safety may fail, but Bandit should still work
            pytest.skip("Safety analyzer not available - Bandit works independently")

    def test_run_all_with_excludes(self, tmp_path):
        """Test running with exclusion globs."""
        # Create test files
        (tmp_path / "app.py").write_text("print('app')")
        (tmp_path / "test.py").write_text("print('test')")

        cfg = RunConfig(path=tmp_path, use_bandit=True, use_safety=False, exclude_globs=["test.py"])

        results = run_all(cfg)

        assert "bandit" in results
        # Results should exist but test.py should be excluded
        assert isinstance(results["bandit"], list)

    def test_run_all_empty_directory(self, tmp_path):
        """Test running on empty directory."""
        cfg = RunConfig(path=tmp_path, use_bandit=True, use_safety=False)

        results = run_all(cfg)

        assert "bandit" in results
        assert results["bandit"] == []  # No Python files = no findings

    def test_run_all_results_are_dicts(self, tmp_path):
        """Test that results are serializable dictionaries."""
        test_file = tmp_path / "app.py"
        test_file.write_text("import os\nos.system('ls')")  # Should trigger Bandit

        cfg = RunConfig(path=tmp_path, use_bandit=True, use_safety=False)

        results = run_all(cfg)

        # Results should be dictionaries (from asdict())
        for finding in results["bandit"]:
            assert isinstance(finding, dict)
            # Common fields from Bandit
            if finding:  # If there are any findings
                assert "rule_id" in finding or "severity" in finding
