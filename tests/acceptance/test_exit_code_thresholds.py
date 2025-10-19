"""Acceptance tests for exit code thresholds.

These tests verify that the CLI properly fails builds based on
severity thresholds and finding counts.
"""

import pytest
import tempfile
from pathlib import Path
from click.testing import CliRunner

# NOTE: Import will need to be updated once we integrate config into CLI
# from specify_cli import cli


@pytest.fixture
def vulnerable_code():
    """Create temporary vulnerable Python file."""
    code = '''
import subprocess
import os

# HIGH: Command injection vulnerability
def unsafe_command(user_input):
    """Execute user input as shell command."""
    # speckit: This is intentionally vulnerable for testing
    subprocess.call(user_input, shell=True)  # B602

# MEDIUM: Use of eval
def unsafe_eval(data):
    """Evaluate user-provided string."""
    return eval(data)  # B307

# LOW: Assert statement
def check_user(user):
    """Check user permission."""
    assert user.is_admin  # B101
    return True
'''
    
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.py',
        delete=False
    ) as f:
        f.write(code)
        temp_path = Path(f.name)
    
    yield temp_path
    
    # Cleanup
    temp_path.unlink()


@pytest.fixture
def config_high_threshold(tmp_path):
    """Create config file with HIGH threshold."""
    config_content = '''
[security]
severity_threshold = "HIGH"

[ci]
fail_on_severity = "HIGH"
max_findings = -1
'''
    
    config_path = tmp_path / ".speckit.toml"
    config_path.write_text(config_content)
    
    return config_path


@pytest.fixture
def config_medium_threshold(tmp_path):
    """Create config file with MEDIUM threshold."""
    config_content = '''
[security]
severity_threshold = "MEDIUM"

[ci]
fail_on_severity = "MEDIUM"
max_findings = -1
'''
    
    config_path = tmp_path / ".speckit.toml"
    config_path.write_text(config_content)
    
    return config_path


@pytest.fixture
def config_max_findings(tmp_path):
    """Create config file with max findings limit."""
    config_content = '''
[security]
severity_threshold = "LOW"

[ci]
fail_on_severity = "LOW"
max_findings = 2
'''
    
    config_path = tmp_path / ".speckit.toml"
    config_path.write_text(config_content)
    
    return config_path


class TestExitCodeThresholds:
    """Test exit code behavior based on thresholds."""
    
    @pytest.mark.skip(reason="Integration test - requires full CLI implementation")
    def test_exit_0_when_no_high_findings(self, vulnerable_code, config_high_threshold):
        """Should exit 0 if no findings meet HIGH threshold."""
        runner = CliRunner()
        
        # Remove the HIGH severity finding from test file
        # (This test would scan a file with only MEDIUM/LOW issues)
        
        # result = runner.invoke(
        #     cli,
        #     ['audit', str(vulnerable_code), '--config', str(config_high_threshold)]
        # )
        
        # assert result.exit_code == 0
        pass
    
    @pytest.mark.skip(reason="Integration test - requires full CLI implementation")
    def test_exit_1_when_high_finding_exists(self, vulnerable_code, config_high_threshold):
        """Should exit 1 when at least one HIGH finding exists."""
        runner = CliRunner()
        
        # Vulnerable code has B602 which is HIGH severity
        
        # result = runner.invoke(
        #     cli,
        #     ['audit', str(vulnerable_code), '--config', str(config_high_threshold)]
        # )
        
        # assert result.exit_code == 1
        pass
    
    @pytest.mark.skip(reason="Integration test - requires full CLI implementation")
    def test_exit_1_when_exceeding_max_findings(self, vulnerable_code, config_max_findings):
        """Should exit 1 when findings exceed max_findings limit."""
        runner = CliRunner()
        
        # Vulnerable code has 3 findings (HIGH, MEDIUM, LOW)
        # Config allows max 2 findings
        
        # result = runner.invoke(
        #     cli,
        #     ['audit', str(vulnerable_code), '--config', str(config_max_findings)]
        # )
        
        # assert result.exit_code == 1
        # assert 'Exceeded maximum findings limit' in result.output
        pass
    
    @pytest.mark.skip(reason="Integration test - requires full CLI implementation")
    def test_cli_flag_overrides_config(self, vulnerable_code, config_medium_threshold):
        """CLI --fail-on-severity flag should override config file."""
        runner = CliRunner()
        
        # Config says MEDIUM, but CLI flag says HIGH
        
        # result = runner.invoke(
        #     cli,
        #     [
        #         'audit',
        #         str(vulnerable_code),
        #         '--config', str(config_medium_threshold),
        #         '--fail-on-severity', 'HIGH'
        #     ]
        # )
        
        # Should only fail on HIGH, not MEDIUM
        # assert result.exit_code == 1  # Because HIGH finding exists
        pass
    
    @pytest.mark.skip(reason="Integration test - requires full CLI implementation")
    def test_env_var_overrides_config(self, vulnerable_code, config_medium_threshold, monkeypatch):
        """Environment variable should override config file."""
        monkeypatch.setenv('SPECKIT_FAIL_ON_SEVERITY', 'CRITICAL')
        
        runner = CliRunner()
        
        # result = runner.invoke(
        #     cli,
        #     ['audit', str(vulnerable_code), '--config', str(config_medium_threshold)]
        # )
        
        # No CRITICAL findings, should exit 0
        # assert result.exit_code == 0
        pass


def test_config_loading():
    """Test that config module loads correctly."""
    from specify_cli.config import (
        SpecKitConfig,
        get_severity_level,
        should_report_finding,
    )
    
    # Test severity levels
    assert get_severity_level("LOW") == 0
    assert get_severity_level("MEDIUM") == 1
    assert get_severity_level("HIGH") == 2
    assert get_severity_level("CRITICAL") == 3
    
    # Test reporting logic
    assert should_report_finding("HIGH", "MEDIUM", [], [], "B602") is True
    assert should_report_finding("LOW", "MEDIUM", [], [], "B101") is False
    
    # Test allow/deny lists
    assert should_report_finding("HIGH", "LOW", ["B602"], [], "B602") is False
    assert should_report_finding("LOW", "HIGH", [], ["B101"], "B101") is True


def test_default_config():
    """Test default config creation."""
    from specify_cli.config import SpecKitConfig
    
    config = SpecKitConfig()
    
    # Verify defaults
    assert config.security.severity_threshold == "MEDIUM"
    assert config.ci.fail_on_severity == "HIGH"
    assert config.ci.max_findings == -1
    assert config.performance.max_workers == 4
    assert config.telemetry.enabled is False


def test_config_from_dict():
    """Test config creation from dictionary."""
    from specify_cli.config import SpecKitConfig
    
    data = {
        "security": {
            "severity_threshold": "HIGH",
            "bandit_enabled": True,
        },
        "ci": {
            "fail_on_severity": "CRITICAL",
            "max_findings": 10,
        },
    }
    
    config = SpecKitConfig.from_dict(data)
    
    assert config.security.severity_threshold == "HIGH"
    assert config.ci.fail_on_severity == "CRITICAL"
    assert config.ci.max_findings == 10
    
    # Verify defaults for unspecified values
    assert config.performance.max_workers == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
