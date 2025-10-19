"""Test baseline fingerprinting and path normalization."""
from pathlib import Path
from specify_cli.baseline import Baseline


class TestBaselineFingerprints:
    """Test baseline fingerprint stability and path handling."""
    
    def test_fingerprint_stability_across_runs(self, tmp_path):
        """Verify same finding produces same fingerprint."""
        baseline_path = tmp_path / "baseline.json"
        baseline = Baseline(baseline_path)
        
        finding1 = {
            "file": "src/app.py",
            "line": 42,
            "rule_id": "B101",
            "message": "Use of assert detected"
        }
        
        # Add finding twice - should get same hash
        hash1 = baseline._finding_hash(finding1)
        hash2 = baseline._finding_hash(finding1)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex length
    
    def test_different_findings_different_hashes(self, tmp_path):
        """Verify different findings produce different hashes."""
        baseline = Baseline(tmp_path / "baseline.json")
        
        finding1 = {"file": "a.py", "line": 1, "rule_id": "B101", "message": "test1"}
        finding2 = {"file": "a.py", "line": 2, "rule_id": "B101", "message": "test1"}
        
        hash1 = baseline._finding_hash(finding1)
        hash2 = baseline._finding_hash(finding2)
        
        assert hash1 != hash2
    
    def test_baselined_finding_suppressed(self, tmp_path):
        """Verify baselined findings are properly suppressed."""
        baseline_path = tmp_path / "baseline.json"
        baseline = Baseline(baseline_path)
        
        finding = {
            "file": "test.py",
            "line": 10,
            "rule_id": "B201",
            "message": "Flask debug mode"
        }
        
        # Add to baseline
        baseline.add_finding(finding, "test suppression")
        baseline.save()
        
        # Reload and check
        baseline2 = Baseline(baseline_path)
        assert baseline2.is_baselined(finding) is True
    
    def test_non_baselined_finding_not_suppressed(self, tmp_path):
        """Verify non-baselined findings are not suppressed."""
        baseline_path = tmp_path / "baseline.json"
        baseline = Baseline(baseline_path)
        
        finding = {
            "file": "test.py",
            "line": 10,
            "rule_id": "B201",
            "message": "Flask debug mode"
        }
        
        # Don't add to baseline
        baseline.save()
        
        # Check not suppressed
        assert baseline.is_baselined(finding) is False
