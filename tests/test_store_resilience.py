"""Test store resilience with corrupt data."""

import json
from specify_cli.store import save_last_run


class TestStoreResilience:
    """Test store handles data persistence."""

    def test_save_and_load_run_data(self, tmp_path):
        """Verify store can save and load run data."""
        data = {"findings": [{"rule_id": "B101", "severity": "LOW"}], "timestamp": "2025-10-18"}

        # Save data
        saved_path = save_last_run(data, tmp_path)
        assert saved_path.exists()

        # Load and verify
        loaded = json.loads(saved_path.read_text())
        assert loaded["findings"] == data["findings"]
        assert loaded["timestamp"] == data["timestamp"]

    def test_overwrite_existing_run(self, tmp_path):
        """Verify new run overwrites existing data."""
        # First run
        data1 = {"findings": ["old"], "timestamp": "2025-01-01"}
        save_last_run(data1, tmp_path)

        # Second run
        data2 = {"findings": ["new"], "timestamp": "2025-01-02"}
        saved_path = save_last_run(data2, tmp_path)

        # Verify second run overwrote first
        loaded = json.loads(saved_path.read_text())
        assert loaded["findings"] == ["new"]
        assert loaded["timestamp"] == "2025-01-02"
