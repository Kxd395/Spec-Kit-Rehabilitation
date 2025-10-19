"""Test exclude glob pattern filtering."""
from pathlib import Path
from specify_cli.analyzers.bandit_analyzer import BanditAnalyzer, BANDIT_AVAILABLE


def test_exclude_globs_skip_paths(tmp_path: Path):
    """Verify exclude globs properly filter out specified paths."""
    if not BANDIT_AVAILABLE:
        return  # Skip if Bandit not installed
    
    # Create virtual environment directory with vulnerable code
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    (venv_dir / "bad.py").write_text("eval('1+1')\n")
    
    # Create normal code file
    (tmp_path / "ok.py").write_text("x = 1\n")
    
    # Run analyzer with exclude pattern
    analyzer = BanditAnalyzer(tmp_path, exclude_globs=[".venv/**"])
    results = analyzer.run()
    
    # Verify .venv files are excluded
    for finding in results:
        file_path = finding.file_path
        assert ".venv/" not in file_path, f"Found excluded path in results: {file_path}"
