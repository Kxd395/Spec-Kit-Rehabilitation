"""Test SARIF output generation."""
from pathlib import Path
from specify_cli.reporters.sarif import combine_to_sarif


def test_sarif_contains_runs_and_results(tmp_path: Path):
    """Verify SARIF output contains proper structure with runs and results."""
    # Create sample findings
    code = [{
        "rule_id": "B101",
        "severity": "HIGH",
        "file_path": str(tmp_path / "x.py"),
        "line": 1,
        "message": "Test security issue",
        "cwe": "79"
    }]
    deps = [{
        "package": "flask",
        "installed_version": "0.5",
        "advisory_id": "ADV-1",
        "severity": "HIGH",
        "vulnerable_spec": ">=0.5",
        "fix_version": "2.0"
    }]
    
    # Generate SARIF
    sarif = combine_to_sarif(code, deps, tmp_path, dep_artifact_hint="requirements.txt")
    
    # Verify SARIF structure
    assert sarif["version"] == "2.1.0", "Should be SARIF 2.1.0"
    assert "$schema" in sarif, "Should have schema"
    assert "runs" in sarif, "Should have runs array"
    assert len(sarif["runs"]) > 0, "Should have at least one run"
    
    # Verify results exist
    run = sarif["runs"][0]
    assert "results" in run, "Run should have results"
    assert len(run["results"]) > 0, "Should have findings"
    
    # Verify rules exist
    assert "tool" in run, "Run should have tool info"
    assert "driver" in run["tool"], "Tool should have driver"


def test_sarif_fingerprints_present(tmp_path: Path):
    """Verify SARIF findings include fingerprints for deduplication."""
    code = [{
        "rule_id": "B201",
        "severity": "MEDIUM",
        "file_path": str(tmp_path / "test.py"),
        "line": 10,
        "message": "Flask app running in debug mode"
    }]
    
    sarif = combine_to_sarif(code, [], tmp_path)
    
    # Check first result has fingerprints (field name is 'fingerprints' not 'partialFingerprints')
    result = sarif["runs"][0]["results"][0]
    assert "fingerprints" in result, "Should have fingerprints"
    assert "primaryLocationLineHash" in result["fingerprints"], \
        "Should have line hash fingerprint"
