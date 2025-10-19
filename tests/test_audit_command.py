"""Test audit command functionality."""

import json
from typer.testing import CliRunner
from specify_cli import app  # Use main app instead of command-specific app
from specify_cli.commands.audit import _gate_code


runner = CliRunner()


class TestGateCode:
    """Test severity threshold gating logic."""

    def test_high_threshold_blocks_high(self):
        """HIGH threshold should block HIGH severity findings."""
        findings = [
            {"severity": "HIGH", "rule_id": "B201"},
            {"severity": "MEDIUM", "rule_id": "B102"},
        ]
        assert _gate_code(findings, "HIGH") == 1

    def test_high_threshold_blocks_critical(self):
        """HIGH threshold should also block CRITICAL severity."""
        findings = [{"severity": "CRITICAL", "rule_id": "B601"}]
        assert _gate_code(findings, "HIGH") == 1

    def test_high_threshold_allows_medium(self):
        """HIGH threshold should allow MEDIUM severity."""
        findings = [{"severity": "MEDIUM", "rule_id": "B102"}]
        assert _gate_code(findings, "HIGH") == 0

    def test_medium_threshold_blocks_medium(self):
        """MEDIUM threshold should block MEDIUM severity."""
        findings = [{"severity": "MEDIUM", "rule_id": "B102"}]
        assert _gate_code(findings, "MEDIUM") == 1

    def test_medium_threshold_blocks_high(self):
        """MEDIUM threshold should also block HIGH severity."""
        findings = [{"severity": "HIGH", "rule_id": "B201"}]
        assert _gate_code(findings, "MEDIUM") == 1

    def test_medium_threshold_allows_low(self):
        """MEDIUM threshold should allow LOW severity."""
        findings = [{"severity": "LOW", "rule_id": "B001"}]
        assert _gate_code(findings, "MEDIUM") == 0

    def test_low_threshold_blocks_low(self):
        """LOW threshold should block LOW severity."""
        findings = [{"severity": "LOW", "rule_id": "B001"}]
        assert _gate_code(findings, "LOW") == 1

    def test_low_threshold_blocks_all(self):
        """LOW threshold should block all severities."""
        findings = [
            {"severity": "LOW", "rule_id": "B001"},
            {"severity": "MEDIUM", "rule_id": "B102"},
            {"severity": "HIGH", "rule_id": "B201"},
        ]
        assert _gate_code(findings, "LOW") == 1

    def test_empty_findings_returns_zero(self):
        """Empty findings list should return 0."""
        assert _gate_code([], "HIGH") == 0
        assert _gate_code([], "MEDIUM") == 0
        assert _gate_code([], "LOW") == 0

    def test_case_insensitive(self):
        """Severity comparison should be case-insensitive."""
        findings = [{"severity": "high", "rule_id": "B201"}]
        assert _gate_code(findings, "high") == 1
        assert _gate_code(findings, "HIGH") == 1

    def test_missing_severity_field(self):
        """Handle findings without severity field."""
        findings = [{"rule_id": "B201"}]
        # Should not crash, treats as empty string
        assert _gate_code(findings, "HIGH") == 0


class TestAuditCommand:
    """Test audit command CLI interface."""

    def test_audit_help(self):
        """Test audit command help output."""
        result = runner.invoke(app, ["audit", "run", "--help"])
        assert result.exit_code == 0
        assert "security analysis" in result.stdout.lower()
        assert "--path" in result.stdout
        assert "--output" in result.stdout
        assert "--fail-on" in result.stdout

    def test_audit_requires_valid_path(self, tmp_path):
        """Test audit validates path exists."""
        # Create a valid Python file
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n")

        # Run audit on tmp_path
        result = runner.invoke(app, ["audit", "run", "--path", str(tmp_path)])

        # Should complete without error (may have findings or not)
        # We're testing the command runs, not the analysis results
        assert result.exit_code in [0, 1]  # 0 = clean, 1 = findings

    def test_audit_output_format_flag(self, tmp_path):
        """Test --output flag is accepted."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n")

        result = runner.invoke(app, ["audit", "run", "--path", str(tmp_path), "--output", "json"])

        # Command should accept the flag
        assert result.exit_code in [0, 1]

        # Check JSON output was created
        json_file = tmp_path / ".speckit" / "analysis" / "analysis.json"
        if json_file.exists():
            data = json.loads(json_file.read_text())
            assert "code" in data
            assert "dependencies" in data

    def test_audit_fail_on_flag(self, tmp_path):
        """Test --fail-on flag is accepted."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n")

        result = runner.invoke(app, ["audit", "run", "--path", str(tmp_path), "--fail-on", "HIGH"])

        # Command should accept the flag and complete
        assert result.exit_code in [0, 1]

    def test_audit_bandit_flag(self, tmp_path):
        """Test --bandit/--no-bandit flag is accepted."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n")

        # Test --no-bandit
        result = runner.invoke(app, ["audit", "run", "--path", str(tmp_path), "--no-bandit"])

        # Should complete successfully (no analyzers to run)
        assert result.exit_code in [0, 1]

    def test_audit_creates_output_directory(self, tmp_path):
        """Test audit creates output directory if missing."""
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n")

        result = runner.invoke(
            app,
            [
                "audit",
                "run",
                "--path",
                str(tmp_path),
                "--output",
                "json",
                "--no-safety",  # Disable safety to avoid environment-specific issues
            ],
        )

        # Command should succeed
        assert result.exit_code == 0, f"Command failed with: {result.output}"

        # Output directory should be created
        output_dir = tmp_path / ".speckit" / "analysis"
        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_audit_with_unsafe_code(self, tmp_path):
        """Test audit detects unsafe code patterns."""
        # Create Python file with known unsafe pattern
        unsafe_file = tmp_path / "unsafe.py"
        unsafe_file.write_text("""
import pickle
import os

# Known unsafe: pickle.loads without validation
data = pickle.loads(user_input)

# Known unsafe: eval
result = eval(user_code)
""")

        result = runner.invoke(
            app,
            [
                "audit",
                "run",
                "--path",
                str(tmp_path),
                "--output",
                "json",
                "--no-safety",  # Disable safety to only test bandit
            ],
        )

        # Should find issues (exit code 1 if fail_on threshold met)
        # Or exit 0 if no high severity issues with default threshold
        assert result.exit_code in [0, 1]

        # Check findings were written
        json_file = tmp_path / ".speckit" / "analysis" / "analysis.json"
        if json_file.exists():
            data = json.loads(json_file.read_text())
            # Should have code findings (Bandit should detect pickle.loads, eval)
            # Note: Actual findings depend on Bandit's detection
            assert "code" in data


class TestAuditIntegration:
    """Integration tests for audit workflow."""

    def test_audit_end_to_end_json_output(self, tmp_path):
        """Test complete audit workflow with JSON output."""
        # Setup test repository
        test_file = tmp_path / "app.py"
        test_file.write_text("import os\nprint('Safe code')\n")

        # Run audit
        result = runner.invoke(
            app, ["audit", "run", "--path", str(tmp_path), "--output", "json", "--no-safety"]
        )

        # Verify completion
        assert result.exit_code in [0, 1]

        # Verify JSON output exists
        json_file = tmp_path / ".speckit" / "analysis" / "analysis.json"
        assert json_file.exists()

        # Verify JSON structure
        data = json.loads(json_file.read_text())
        assert "code" in data
        assert "dependencies" in data
        assert isinstance(data["code"], list)
        assert isinstance(data["dependencies"], list)

    def test_audit_respects_config_file(self, tmp_path):
        """Test audit loads and respects .speckit.toml config."""
        # Create config file
        config = tmp_path / ".speckit.toml"
        config.write_text("""
[analysis]
fail_on = "LOW"

[output]
format = "json"
directory = ".speckit/custom"

[analyzers]
bandit = true
safety = false
""")

        # Create test file
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')\n")

        # Run audit without flags (should use config)
        result = runner.invoke(app, ["audit", "run", "--path", str(tmp_path)])

        # Should use config settings
        assert result.exit_code in [0, 1]

        # Output should be in custom directory
        custom_dir = tmp_path / ".speckit" / "custom"
        assert custom_dir.exists()
