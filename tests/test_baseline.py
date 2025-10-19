"""Test baseline management functionality."""

import json
from specify_cli.baseline import Baseline


class TestBaselineInit:
    """Test Baseline initialization."""

    def test_baseline_init_new_file(self, tmp_path):
        """Test creating baseline with non-existent file."""
        baseline_path = tmp_path / "baseline.json"
        baseline = Baseline(baseline_path)

        assert baseline.baseline_path == baseline_path
        assert baseline.findings == {}
        assert baseline.metadata == {}

    def test_baseline_init_existing_file(self, tmp_path):
        """Test loading existing baseline file."""
        baseline_path = tmp_path / "baseline.json"

        # Create existing baseline
        data = {
            "version": "1.0",
            "created_at": "2025-01-01T00:00:00",
            "updated_at": "2025-01-01T00:00:00",
            "finding_count": 1,
            "findings": {
                "abc123": {
                    "finding": {"rule_id": "B101", "file": "test.py", "line": 10},
                    "reason": "test",
                    "created_at": "2025-01-01T00:00:00",
                    "created_by": "user",
                }
            },
        }
        baseline_path.write_text(json.dumps(data))

        baseline = Baseline(baseline_path)

        assert len(baseline.findings) == 1
        assert "abc123" in baseline.findings
        assert baseline.metadata["version"] == "1.0"


class TestFindingHash:
    """Test finding hash generation."""

    def test_finding_hash_stable(self, tmp_path):
        """Test that same finding produces same hash."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test issue"}

        hash1 = baseline._finding_hash(finding)
        hash2 = baseline._finding_hash(finding)

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex length

    def test_finding_hash_different_for_different_findings(self, tmp_path):
        """Test that different findings produce different hashes."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding1 = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Issue 1"}
        finding2 = {"file": "test.py", "line": 20, "rule_id": "B101", "message": "Issue 1"}

        hash1 = baseline._finding_hash(finding1)
        hash2 = baseline._finding_hash(finding2)

        assert hash1 != hash2

    def test_finding_hash_handles_missing_fields(self, tmp_path):
        """Test hash generation with missing fields."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py"}  # Missing line, rule_id, message

        hash_value = baseline._finding_hash(finding)
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64


class TestAddFinding:
    """Test adding findings to baseline."""

    def test_add_finding_basic(self, tmp_path):
        """Test adding a finding to baseline."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test issue"}

        hash_value = baseline.add_finding(finding)

        assert hash_value in baseline.findings
        assert baseline.findings[hash_value]["finding"] == finding
        assert baseline.findings[hash_value]["reason"] == "baselined"

    def test_add_finding_with_reason(self, tmp_path):
        """Test adding finding with custom reason."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}
        hash_value = baseline.add_finding(finding, reason="false positive")

        assert baseline.findings[hash_value]["reason"] == "false positive"

    def test_add_finding_with_created_by(self, tmp_path):
        """Test adding finding with creator."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}
        hash_value = baseline.add_finding(finding, created_by="alice")

        assert baseline.findings[hash_value]["created_by"] == "alice"

    def test_add_finding_includes_timestamp(self, tmp_path):
        """Test that added finding includes timestamp."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}
        hash_value = baseline.add_finding(finding)

        assert "created_at" in baseline.findings[hash_value]
        assert isinstance(baseline.findings[hash_value]["created_at"], str)


class TestIsBaselined:
    """Test checking if findings are baselined."""

    def test_is_baselined_true(self, tmp_path):
        """Test is_baselined returns True for baselined finding."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}
        baseline.add_finding(finding)

        assert baseline.is_baselined(finding) is True

    def test_is_baselined_false(self, tmp_path):
        """Test is_baselined returns False for new finding."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}

        assert baseline.is_baselined(finding) is False

    def test_is_baselined_after_removal(self, tmp_path):
        """Test is_baselined after removing finding."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}
        baseline.add_finding(finding)
        baseline.remove_finding(finding)

        assert baseline.is_baselined(finding) is False


class TestRemoveFinding:
    """Test removing findings from baseline."""

    def test_remove_finding_exists(self, tmp_path):
        """Test removing an existing finding."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}
        baseline.add_finding(finding)

        result = baseline.remove_finding(finding)

        assert result is True
        assert not baseline.is_baselined(finding)

    def test_remove_finding_not_exists(self, tmp_path):
        """Test removing non-existent finding."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}

        result = baseline.remove_finding(finding)

        assert result is False


class TestSaveLoad:
    """Test saving and loading baseline."""

    def test_save_creates_file(self, tmp_path):
        """Test save creates baseline file."""
        baseline_path = tmp_path / "baseline.json"
        baseline = Baseline(baseline_path)

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}
        baseline.add_finding(finding)
        baseline.save()

        assert baseline_path.exists()

    def test_save_creates_parent_dirs(self, tmp_path):
        """Test save creates parent directories."""
        baseline_path = tmp_path / "nested" / "dir" / "baseline.json"
        baseline = Baseline(baseline_path)

        baseline.add_finding({"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"})
        baseline.save()

        assert baseline_path.exists()
        assert baseline_path.parent.exists()

    def test_save_and_load_round_trip(self, tmp_path):
        """Test saving and loading preserves data."""
        baseline_path = tmp_path / "baseline.json"

        # Create and save
        baseline1 = Baseline(baseline_path)
        finding1 = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test 1"}
        finding2 = {"file": "app.py", "line": 20, "rule_id": "B201", "message": "Test 2"}
        baseline1.add_finding(finding1)
        baseline1.add_finding(finding2)
        baseline1.save()

        # Load and verify
        baseline2 = Baseline(baseline_path)

        assert len(baseline2.findings) == 2
        assert baseline2.is_baselined(finding1)
        assert baseline2.is_baselined(finding2)

    def test_load_populates_metadata(self, tmp_path):
        """Test load populates metadata correctly."""
        baseline_path = tmp_path / "baseline.json"

        data = {
            "version": "1.0",
            "created_at": "2025-01-01T00:00:00",
            "updated_at": "2025-01-02T00:00:00",
            "finding_count": 0,
            "findings": {},
        }
        baseline_path.write_text(json.dumps(data))

        baseline = Baseline(baseline_path)

        assert baseline.metadata["version"] == "1.0"
        assert baseline.metadata["created_at"] == "2025-01-01T00:00:00"
        assert baseline.metadata["updated_at"] == "2025-01-02T00:00:00"


class TestFilterFindings:
    """Test filtering findings against baseline."""

    def test_filter_findings_respect_baseline_true(self, tmp_path):
        """Test filtering with respect_baseline=True."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding1 = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test 1"}
        finding2 = {"file": "app.py", "line": 20, "rule_id": "B201", "message": "Test 2"}

        baseline.add_finding(finding1)

        new, baselined = baseline.filter_findings([finding1, finding2], respect_baseline=True)

        assert len(new) == 1
        assert finding2 in new
        assert len(baselined) == 1
        assert finding1 in baselined

    def test_filter_findings_respect_baseline_false(self, tmp_path):
        """Test filtering with respect_baseline=False."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding1 = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test 1"}
        finding2 = {"file": "app.py", "line": 20, "rule_id": "B201", "message": "Test 2"}

        baseline.add_finding(finding1)

        new, baselined = baseline.filter_findings([finding1, finding2], respect_baseline=False)

        assert len(new) == 2
        assert len(baselined) == 0

    def test_filter_findings_empty_list(self, tmp_path):
        """Test filtering empty findings list."""
        baseline = Baseline(tmp_path / "baseline.json")

        new, baselined = baseline.filter_findings([], respect_baseline=True)

        assert new == []
        assert baselined == []


class TestGetStats:
    """Test baseline statistics."""

    def test_get_stats_empty_baseline(self, tmp_path):
        """Test stats for empty baseline."""
        baseline = Baseline(tmp_path / "baseline.json")

        stats = baseline.get_stats()

        assert stats["total_findings"] == 0
        assert stats["severity_counts"] == {}
        assert stats["rule_counts"] == {}

    def test_get_stats_with_findings(self, tmp_path):
        """Test stats with findings."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding1 = {
            "file": "test.py",
            "line": 10,
            "rule_id": "B101",
            "severity": "HIGH",
            "message": "Test 1",
        }
        finding2 = {
            "file": "app.py",
            "line": 20,
            "rule_id": "B101",
            "severity": "HIGH",
            "message": "Test 2",
        }
        finding3 = {
            "file": "main.py",
            "line": 30,
            "rule_id": "B201",
            "severity": "MEDIUM",
            "message": "Test 3",
        }

        baseline.add_finding(finding1)
        baseline.add_finding(finding2)
        baseline.add_finding(finding3)

        stats = baseline.get_stats()

        assert stats["total_findings"] == 3
        assert stats["severity_counts"]["HIGH"] == 2
        assert stats["severity_counts"]["MEDIUM"] == 1
        assert stats["rule_counts"]["B101"] == 2
        assert stats["rule_counts"]["B201"] == 1

    def test_get_stats_includes_timestamps(self, tmp_path):
        """Test stats includes created/updated timestamps."""
        baseline_path = tmp_path / "baseline.json"
        baseline = Baseline(baseline_path)

        finding = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test"}
        baseline.add_finding(finding)
        baseline.save()

        # Reload to get metadata
        baseline2 = Baseline(baseline_path)
        stats = baseline2.get_stats()

        assert "created_at" in stats
        assert "updated_at" in stats


class TestGetBaselinedHashes:
    """Test getting set of baselined hashes."""

    def test_get_baselined_hashes_empty(self, tmp_path):
        """Test getting hashes from empty baseline."""
        baseline = Baseline(tmp_path / "baseline.json")

        hashes = baseline.get_baselined_hashes()

        assert isinstance(hashes, set)
        assert len(hashes) == 0

    def test_get_baselined_hashes_with_findings(self, tmp_path):
        """Test getting hashes with findings."""
        baseline = Baseline(tmp_path / "baseline.json")

        finding1 = {"file": "test.py", "line": 10, "rule_id": "B101", "message": "Test 1"}
        finding2 = {"file": "app.py", "line": 20, "rule_id": "B201", "message": "Test 2"}

        hash1 = baseline.add_finding(finding1)
        hash2 = baseline.add_finding(finding2)

        hashes = baseline.get_baselined_hashes()

        assert isinstance(hashes, set)
        assert len(hashes) == 2
        assert hash1 in hashes
        assert hash2 in hashes
