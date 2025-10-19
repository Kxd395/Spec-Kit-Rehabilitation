"""Tests for error handling and structured error messages."""
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

from specify_cli.errors import (
    SpecKitError,
    ConfigError,
    AnalyzerError,
    FileNotFoundError,
    ValidationError,
    DependencyError,
    GitError,
    missing_config_file,
    invalid_output_format,
    analyzer_not_available,
    git_not_available,
    not_a_git_repo,
)


class TestSpecKitError:
    """Test base SpecKitError class."""
    
    def test_init_message_only(self):
        """Test error with message only."""
        error = SpecKitError("Test error")
        assert error.message == "Test error"
        assert error.hint is None
        assert error.details == {}
    
    def test_init_with_hint(self):
        """Test error with hint."""
        error = SpecKitError("Test error", hint="Try this fix")
        assert error.message == "Test error"
        assert error.hint == "Try this fix"
    
    def test_init_with_details(self):
        """Test error with details."""
        details = {"key": "value", "number": 42}
        error = SpecKitError("Test error", details=details)
        assert error.details == details
    
    @patch('specify_cli.errors.console')
    def test_display_message_only(self, mock_console):
        """Test display() with message only."""
        error = SpecKitError("Test error")
        error.display()
        
        mock_console.print.assert_called_once()
    
    @patch('specify_cli.errors.console')
    def test_display_with_hint(self, mock_console):
        """Test display() with hint."""
        error = SpecKitError("Test error", hint="Try this")
        error.display()
        
        mock_console.print.assert_called_once()
    
    @patch('specify_cli.errors.console')
    def test_display_with_details(self, mock_console):
        """Test display() with details."""
        error = SpecKitError("Test error", details={"key": "value"})
        error.display()
        
        mock_console.print.assert_called_once()


class TestConfigError:
    """Test ConfigError class."""
    
    def test_init_without_config_file(self):
        """Test ConfigError without config file."""
        error = ConfigError("Invalid config")
        assert error.message == "Invalid config"
        assert "config_file" not in error.details
    
    def test_init_with_config_file(self):
        """Test ConfigError with config file path."""
        path = Path("/path/to/config.toml")
        error = ConfigError("Invalid config", config_file=path)
        assert error.message == "Invalid config"
        assert error.details["config_file"] == str(path)
    
    def test_init_with_hint(self):
        """Test ConfigError with hint."""
        error = ConfigError("Invalid config", hint="Check syntax")
        assert error.hint == "Check syntax"


class TestAnalyzerError:
    """Test AnalyzerError class."""
    
    def test_init_basic(self):
        """Test AnalyzerError basic initialization."""
        error = AnalyzerError("bandit", "Analyzer failed")
        assert error.message == "Analyzer failed"
        assert error.details["analyzer"] == "bandit"
    
    def test_init_with_hint(self):
        """Test AnalyzerError with hint."""
        error = AnalyzerError("bandit", "Analyzer failed", hint="Check installation")
        assert error.hint == "Check installation"


class TestFileNotFoundError:
    """Test FileNotFoundError class."""
    
    def test_init(self):
        """Test FileNotFoundError initialization."""
        path = Path("/path/to/missing.txt")
        error = FileNotFoundError(path)
        assert "File not found" in error.message
        assert error.details["file_path"] == str(path)
    
    def test_init_with_hint(self):
        """Test FileNotFoundError with hint."""
        path = Path("/path/to/missing.txt")
        error = FileNotFoundError(path, hint="Create the file first")
        assert error.hint == "Create the file first"


class TestValidationError:
    """Test ValidationError class."""
    
    def test_init_basic(self):
        """Test ValidationError basic initialization."""
        error = ValidationError("format", "xml", "must be 'json' or 'html'")
        assert "Invalid value for 'format'" in error.message
        assert error.details["field"] == "format"
        assert error.details["value"] == "xml"
        assert error.details["reason"] == "must be 'json' or 'html'"
    
    def test_init_with_hint(self):
        """Test ValidationError with hint."""
        error = ValidationError("format", "xml", "invalid", hint="Use 'json'")
        assert error.hint == "Use 'json'"


class TestDependencyError:
    """Test DependencyError class."""
    
    def test_init_without_version(self):
        """Test DependencyError without version requirement."""
        error = DependencyError("bandit")
        assert "bandit" in error.message
        assert error.details["dependency"] == "bandit"
        assert "Install with" in error.hint
    
    def test_init_with_version(self):
        """Test DependencyError with version requirement."""
        error = DependencyError("bandit", required_version=">=1.7.0")
        assert "bandit" in error.message
        assert ">=1.7.0" in error.message
        assert error.details["required_version"] == ">=1.7.0"
    
    def test_default_hint(self):
        """Test DependencyError has default installation hint."""
        error = DependencyError("test-package")
        assert "pip install" in error.hint
        assert "test-package" in error.hint


class TestGitError:
    """Test GitError class."""
    
    def test_init_without_command(self):
        """Test GitError without command."""
        error = GitError("Git operation failed")
        assert error.message == "Git operation failed"
        assert "command" not in error.details
    
    def test_init_with_command(self):
        """Test GitError with command."""
        error = GitError("Command failed", command="git status")
        assert error.details["command"] == "git status"


class TestErrorHelpers:
    """Test error helper functions."""
    
    def test_missing_config_file(self):
        """Test missing_config_file() helper."""
        path = Path(".speckit.toml")
        error = missing_config_file(path)
        
        assert isinstance(error, ConfigError)
        assert str(path) in error.message
        assert "specify init" in error.hint
    
    def test_invalid_output_format(self):
        """Test invalid_output_format() helper."""
        error = invalid_output_format("xml", ["json", "html", "sarif"])
        
        assert isinstance(error, ValidationError)
        assert error.details["field"] == "output_format"
        assert error.details["value"] == "xml"
        assert "json" in error.hint
        assert "html" in error.hint
    
    def test_analyzer_not_available_normal_mode(self):
        """Test analyzer_not_available() in normal mode."""
        error = analyzer_not_available("bandit", strict_mode=False)
        
        assert isinstance(error, AnalyzerError)
        assert "bandit" in error.message
        assert "strict mode" not in error.message
        assert "pip install bandit" in error.hint
    
    def test_analyzer_not_available_strict_mode(self):
        """Test analyzer_not_available() in strict mode."""
        error = analyzer_not_available("bandit", strict_mode=True)
        
        assert "strict mode" in error.message
    
    def test_analyzer_not_available_all_analyzers(self):
        """Test analyzer_not_available() for all known analyzers."""
        analyzers = ["bandit", "safety", "radon"]
        for analyzer in analyzers:
            error = analyzer_not_available(analyzer)
            assert analyzer in error.details["analyzer"]
            assert "pip install" in error.hint
    
    def test_git_not_available(self):
        """Test git_not_available() helper."""
        error = git_not_available()
        
        assert isinstance(error, GitError)
        assert "Git" in error.message
        assert "PATH" in error.message
        assert "git-scm.com" in error.hint
    
    def test_not_a_git_repo(self):
        """Test not_a_git_repo() helper."""
        path = Path("/some/directory")
        error = not_a_git_repo(path)
        
        assert isinstance(error, GitError)
        assert str(path) in error.message
        assert "git init" in error.hint


class TestErrorInheritance:
    """Test error class inheritance."""
    
    def test_all_inherit_from_speckit_error(self):
        """Test all custom errors inherit from SpecKitError."""
        errors = [
            ConfigError("test"),
            AnalyzerError("test", "message"),
            FileNotFoundError(Path("test")),
            ValidationError("field", "value", "reason"),
            DependencyError("dep"),
            GitError("message"),
        ]
        
        for error in errors:
            assert isinstance(error, SpecKitError)
            assert isinstance(error, Exception)


class TestErrorDisplay:
    """Test error display functionality."""
    
    @patch('specify_cli.errors.console')
    def test_config_error_display(self, mock_console):
        """Test ConfigError displays correctly."""
        error = ConfigError("Invalid syntax", config_file=Path("config.toml"), hint="Check line 5")
        error.display()
        
        mock_console.print.assert_called_once()
    
    @patch('specify_cli.errors.console')
    def test_analyzer_error_display(self, mock_console):
        """Test AnalyzerError displays correctly."""
        error = AnalyzerError("bandit", "Failed to run", hint="Install bandit")
        error.display()
        
        mock_console.print.assert_called_once()
    
    @patch('specify_cli.errors.console')
    def test_dependency_error_display(self, mock_console):
        """Test DependencyError displays correctly."""
        error = DependencyError("missing-package", required_version=">=1.0.0")
        error.display()
        
        mock_console.print.assert_called_once()
