"""Test git utility functions."""
import pytest
from pathlib import Path
from specify_cli.gitutils import is_git_repo, get_changed_files


class TestIsGitRepo:
    """Test git repository detection."""
    
    def test_is_git_repo_in_git_repo(self, tmp_path):
        """Test detection in actual git repo."""
        # Initialize a git repo
        import subprocess
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        
        assert is_git_repo(tmp_path) is True
    
    def test_is_git_repo_not_git_repo(self, tmp_path):
        """Test detection in non-git directory."""
        # Just a regular directory
        result = is_git_repo(tmp_path)
        
        assert result is False
    
    def test_is_git_repo_with_string_path(self, tmp_path):
        """Test with string path instead of Path object."""
        import subprocess
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        
        assert is_git_repo(str(tmp_path)) is True


class TestGetChangedFiles:
    """Test getting changed files in git repo."""
    
    def test_get_changed_files_no_changes(self, tmp_path):
        """Test with no changed files."""
        import subprocess
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path)
        
        # Create and commit a file
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")
        subprocess.run(["git", "add", "."], cwd=tmp_path)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=tmp_path)
        
        changed = get_changed_files(tmp_path)
        
        assert isinstance(changed, list)
        assert len(changed) == 0
    
    def test_get_changed_files_with_changes(self, tmp_path):
        """Test with changed files."""
        import subprocess
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmp_path)
        
        # Create and commit a file
        test_file = tmp_path / "test.py"
        test_file.write_text("print('hello')")
        subprocess.run(["git", "add", "."], cwd=tmp_path)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=tmp_path)
        
        # Modify the file
        test_file.write_text("print('hello world')")
        
        changed = get_changed_files(tmp_path)
        
        assert isinstance(changed, list)
        assert len(changed) >= 1
        assert any("test.py" in f for f in changed)
    
    def test_get_changed_files_non_git_repo(self, tmp_path):
        """Test with non-git directory returns empty list."""
        changed = get_changed_files(tmp_path)
        
        assert changed == []
