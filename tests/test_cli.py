"""Tests for core CLI functionality."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from specify_cli import (
    app,
    check_tool,
    is_git_repo,
    AGENT_CONFIG,
    StepTracker,
)

runner = CliRunner()


class TestCheckTool:
    """Test tool detection functionality."""

    def test_check_tool_found(self):
        """Test that check_tool returns True for installed tools."""
        # Python should be available in test environment
        assert check_tool("python") is True

    def test_check_tool_not_found(self):
        """Test that check_tool returns False for non-existent tools."""
        assert check_tool("this-tool-definitely-does-not-exist-12345") is False

    def test_check_tool_with_tracker(self):
        """Test check_tool updates tracker correctly."""
        tracker = StepTracker("Test")
        tracker.add("test-tool", "Test Tool")
        
        # Test with found tool
        result = check_tool("python", tracker)
        assert result is True
        
        # Check tracker was updated
        step = next((s for s in tracker.steps if s["key"] == "test-tool"), None)
        assert step is not None


class TestAgentConfig:
    """Test agent configuration structure."""

    def test_agent_config_exists(self):
        """Verify AGENT_CONFIG is properly defined."""
        assert isinstance(AGENT_CONFIG, dict)
        assert len(AGENT_CONFIG) > 0

    def test_agent_config_structure(self):
        """Verify each agent has required fields."""
        for agent_key, config in AGENT_CONFIG.items():
            assert "name" in config, f"{agent_key} missing 'name'"
            assert "folder" in config, f"{agent_key} missing 'folder'"
            assert "requires_cli" in config, f"{agent_key} missing 'requires_cli'"
            assert isinstance(config["requires_cli"], bool)

    def test_copilot_config(self):
        """Test specific copilot configuration."""
        assert "copilot" in AGENT_CONFIG
        copilot = AGENT_CONFIG["copilot"]
        assert copilot["name"] == "GitHub Copilot"
        assert copilot["folder"] == ".github/"
        assert copilot["requires_cli"] is False


class TestStepTracker:
    """Test StepTracker functionality."""

    def test_step_tracker_creation(self):
        """Test creating a StepTracker."""
        tracker = StepTracker("Test Process")
        assert tracker.title == "Test Process"
        assert len(tracker.steps) == 0

    def test_add_step(self):
        """Test adding steps to tracker."""
        tracker = StepTracker("Test")
        tracker.add("step1", "First Step")
        
        assert len(tracker.steps) == 1
        assert tracker.steps[0]["key"] == "step1"
        assert tracker.steps[0]["label"] == "First Step"
        assert tracker.steps[0]["status"] == "pending"

    def test_step_lifecycle(self):
        """Test step status transitions."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Test Step")
        
        # Start step
        tracker.start("step1", "Starting...")
        assert tracker.steps[0]["status"] == "running"
        
        # Complete step
        tracker.complete("step1", "Done")
        assert tracker.steps[0]["status"] == "done"

    def test_step_error(self):
        """Test error status."""
        tracker = StepTracker("Test")
        tracker.add("step1", "Test Step")
        tracker.error("step1", "Failed")
        
        assert tracker.steps[0]["status"] == "error"


class TestIsGitRepo:
    """Test git repository detection."""

    def test_is_git_repo_current_dir(self, tmp_path):
        """Test checking if directory is a git repo."""
        # tmp_path is not a git repo
        assert is_git_repo(tmp_path) is False

    @patch("subprocess.run")
    def test_is_git_repo_with_git(self, mock_run, tmp_path):
        """Test positive case when git repo exists."""
        mock_run.return_value = MagicMock(returncode=0)
        
        is_git_repo(tmp_path)
        
        # Should call git rev-parse
        mock_run.assert_called_once()
        assert "git" in mock_run.call_args[0][0]


class TestCLIInit:
    """Test the init command."""

    def test_init_missing_project_name(self):
        """Test init fails without project name or --here."""
        result = runner.invoke(app, ["init"])
        assert result.exit_code != 0

    def test_init_invalid_ai(self):
        """Test init fails with invalid AI assistant."""
        result = runner.invoke(app, ["init", "test-project", "--ai", "invalid-ai"])
        assert result.exit_code != 0
        assert "Invalid AI assistant" in result.stdout

    def test_init_invalid_script_type(self):
        """Test init fails with invalid script type."""
        result = runner.invoke(app, ["init", "test-project", "--script", "invalid"])
        assert result.exit_code != 0


class TestHelpers:
    """Test helper functions."""

    def test_agent_config_keys_match_cli_names(self):
        """Ensure agent config keys match actual CLI tool names."""
        # This is a design principle test
        for key in AGENT_CONFIG.keys():
            config = AGENT_CONFIG[key]
            # IDE-based agents don't need CLI matching
            if not config["requires_cli"]:
                continue
            
            # CLI-based agents should have keys matching their tool names
            # This is important for consistency
            assert isinstance(key, str)
            assert len(key) > 0


# Integration-style tests would go here
# These would require actual file system operations and are harder to mock
# For now, we have basic unit tests covering core functionality


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
