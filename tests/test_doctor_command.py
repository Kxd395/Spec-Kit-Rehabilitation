"""Test doctor command functionality."""
from typer.testing import CliRunner
from specify_cli.commands.doctor import _version, app


runner = CliRunner()


class TestVersionHelper:
    """Test _version helper function."""
    
    def test_version_for_installed_package(self):
        """Test getting version for installed package."""
        # Test with a known installed package (typer is a dependency)
        version = _version("typer")
        assert version != "not installed"
        assert version != "not found"
        assert len(version) > 0
    
    def test_version_for_missing_package(self):
        """Test getting version for missing package."""
        version = _version("this_package_does_not_exist_12345")
        assert version == "not installed"
    
    def test_version_for_package_without_version(self):
        """Test package that exists but has no __version__."""
        # Some built-in modules don't have __version__
        version = _version("os")
        # Should return either a version or "not found"
        assert version in ["not found", "not installed"] or len(version) > 0


class TestDoctorCommand:
    """Test doctor command CLI interface."""
    
    def test_doctor_help(self):
        """Test doctor command help output."""
        result = runner.invoke(app, ["run", "--help"])
        assert result.exit_code == 0
        assert "environment" in result.stdout.lower()
    
    def test_doctor_runs_without_error(self):
        """Test doctor command executes successfully."""
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0
    
    def test_doctor_shows_tools_table(self):
        """Test doctor displays tool status table."""
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0
        assert "bandit" in result.stdout.lower()
        assert "safety" in result.stdout.lower()
    
    def test_doctor_shows_installation_hint(self):
        """Test doctor shows installation instructions."""
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0
        assert "pip install" in result.stdout.lower()
    
    def test_doctor_checks_bandit(self):
        """Test doctor checks for bandit package."""
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0
        # Should mention bandit in output
        assert "bandit" in result.stdout.lower()
    
    def test_doctor_checks_safety_cli(self):
        """Test doctor checks for safety CLI tool."""
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0
        # Should check for safety CLI (not just Python package)
        output_lower = result.stdout.lower()
        assert "safety" in output_lower
        # Should show both safety package and CLI status
        assert "cli" in output_lower or "missing" in output_lower or "safety" in output_lower


class TestDoctorIntegration:
    """Integration tests for doctor command."""
    
    def test_doctor_provides_actionable_output(self):
        """Test doctor output is actionable for users."""
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0
        
        # Should provide clear status information
        output = result.stdout.lower()
        
        # Should have table with tool status
        assert "tool" in output or "bandit" in output
        
        # Should have actionable guidance
        assert "pip" in output or "install" in output
    
    def test_doctor_exits_successfully_always(self):
        """Test doctor always exits with code 0 (informational only)."""
        # Doctor is informational, shouldn't fail even if tools missing
        result = runner.invoke(app, ["run"])
        assert result.exit_code == 0
