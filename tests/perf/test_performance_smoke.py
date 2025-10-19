"""Performance smoke tests for Spec-Kit analyzers.

These tests ensure analyzers complete within reasonable time bounds.
Run with: pytest tests/perf/test_performance_smoke.py -v
"""

import pytest
import time
from specify_cli.analyzers.bandit_analyzer import BanditAnalyzer
from specify_cli.reporters.sarif import combine_to_sarif

# Check if pytest-benchmark is available
try:
    import pytest_benchmark  # noqa: F401

    HAS_BENCHMARK = True
except ImportError:
    HAS_BENCHMARK = False


class TestPerformanceSmoke:
    """Smoke tests to catch performance regressions."""

    def test_bandit_small_repo_under_5_seconds(self, tmp_path):
        """Verify Bandit scans small repo (<1k LOC) in under 5 seconds."""
        # Create small test files
        test_dir = tmp_path / "src"
        test_dir.mkdir()

        # Generate 10 files with ~100 lines each = ~1k LOC
        for i in range(10):
            test_file = test_dir / f"module_{i}.py"
            lines = []
            for j in range(30):
                lines.append(f"def function_{j}():")
                lines.append(f"    x = {j}")
                lines.append("    return x * 2")
            test_file.write_text("\n".join(lines))

        # Time the scan
        start = time.time()
        analyzer = BanditAnalyzer(test_dir, [])
        findings = analyzer.run()
        elapsed = time.time() - start

        # Should complete in < 5 seconds on any reasonable hardware
        assert elapsed < 5.0, f"Bandit took {elapsed:.2f}s for ~1k LOC (expected <5s)"
        assert isinstance(findings, list)

    def test_sarif_generation_under_3_seconds(self, tmp_path):
        """Verify SARIF generation for 1k findings completes in <3 seconds."""
        # Generate 1000 synthetic findings with paths under tmp_path
        findings = [
            {
                "rule_id": f"B{100 + (i % 10)}",
                "severity": "MEDIUM",
                "file_path": str(tmp_path / f"src/file_{i // 10}.py"),
                "line": (i % 100) + 1,
                "message": f"Test finding {i}",
                "cwe": "79",
            }
            for i in range(1000)
        ]

        # Time SARIF generation
        start = time.time()
        sarif = combine_to_sarif(findings, [], tmp_path)
        elapsed = time.time() - start

        # Should complete in < 3 seconds
        assert elapsed < 3.0, f"SARIF generation took {elapsed:.2f}s for 1k findings (expected <3s)"
        assert "runs" in sarif
        assert len(sarif["runs"][0]["results"]) == 1000

    def test_baseline_load_under_1_second(self, tmp_path):
        """Verify baseline loading is fast even with many findings."""
        from specify_cli.baseline import Baseline

        baseline_path = tmp_path / "baseline.json"
        baseline = Baseline(baseline_path)

        # Add 500 findings to baseline
        for i in range(500):
            finding = {
                "file": f"src/file_{i}.py",
                "line": i + 1,
                "rule_id": f"B{101 + (i % 10)}",
                "message": f"Finding {i}",
            }
            baseline.add_finding(finding, f"suppression_{i}")

        baseline.save()

        # Time reload
        start = time.time()
        baseline2 = Baseline(baseline_path)
        elapsed = time.time() - start

        # Should load in < 1 second
        assert elapsed < 1.0, f"Baseline load took {elapsed:.2f}s for 500 findings (expected <1s)"
        assert len(baseline2.findings) == 500


@pytest.mark.benchmark
@pytest.mark.skipif(not HAS_BENCHMARK, reason="pytest-benchmark not installed")
class TestPerformanceBenchmarks:
    """Optional benchmark tests (run with --benchmark-only)."""

    def test_bandit_scaling(self, benchmark, tmp_path):
        """Benchmark Bandit performance scaling."""
        test_dir = tmp_path / "src"
        test_dir.mkdir()

        # Create 5 test files
        for i in range(5):
            test_file = test_dir / f"test_{i}.py"
            test_file.write_text("import os\nprint('test')\n" * 50)

        # Benchmark
        def run_scan():
            analyzer = BanditAnalyzer(test_dir, [])
            return analyzer.run()

        result = benchmark(run_scan)
        assert isinstance(result, list)
