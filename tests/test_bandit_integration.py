"""Integration tests for Bandit analyzer."""

from pathlib import Path
from specify_cli.analyzers.bandit_analyzer import BanditAnalyzer, BANDIT


def test_bandit_scans_repo(tmp_path: Path):
    """Test that Bandit can scan a simple Python file."""
    p = tmp_path / "proj"
    p.mkdir()
    (p / "bad.py").write_text("eval('1+1')\n")

    findings = BanditAnalyzer(p).run()
    assert isinstance(findings, list)

    if BANDIT:
        # If Bandit is installed, we should get findings
        assert any(f.rule_id for f in findings)


def test_bandit_empty_directory(tmp_path: Path):
    """Test Bandit on directory with no Python files."""
    p = tmp_path / "empty"
    p.mkdir()

    findings = BanditAnalyzer(p).run()
    assert isinstance(findings, list)
    assert len(findings) == 0


def test_bandit_finding_structure(tmp_path: Path):
    """Test that findings have expected structure."""
    p = tmp_path / "proj"
    p.mkdir()
    (p / "test.py").write_text("import pickle\npickle.loads(b'data')\n")

    findings = BanditAnalyzer(p).run()

    if BANDIT and len(findings) > 0:
        f = findings[0]
        assert hasattr(f, "file_path")
        assert hasattr(f, "line")
        assert hasattr(f, "rule_id")
        assert hasattr(f, "severity")
        assert hasattr(f, "confidence")
        assert hasattr(f, "message")
        assert f.severity in ["LOW", "MEDIUM", "HIGH"]
