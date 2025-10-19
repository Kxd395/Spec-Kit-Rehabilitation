"""Tests for verbose output utilities."""

import time
from unittest.mock import patch

from specify_cli.verbose import VerboseLogger


class TestVerboseLogger:
    """Test VerboseLogger class."""

    def test_init_disabled_by_default(self):
        """Test logger is disabled by default."""
        logger = VerboseLogger()
        assert logger.enabled is False

    def test_init_enabled(self):
        """Test logger can be enabled."""
        logger = VerboseLogger(enabled=True)
        assert logger.enabled is True

    def test_start_timing(self):
        """Test start() initializes timing."""
        logger = VerboseLogger(enabled=True)
        assert logger._start_time is None
        logger.start()
        assert logger._start_time is not None
        assert isinstance(logger._start_time, float)

    def test_start_no_op_when_disabled(self):
        """Test start() does nothing when disabled."""
        logger = VerboseLogger(enabled=False)
        logger.start()
        assert logger._start_time is None

    def test_elapsed_before_start(self):
        """Test elapsed() returns 0.00s before start()."""
        logger = VerboseLogger(enabled=True)
        assert logger.elapsed() == "0.00s"

    def test_elapsed_after_start(self):
        """Test elapsed() returns formatted time after start()."""
        logger = VerboseLogger(enabled=True)
        logger.start()
        time.sleep(0.05)  # Sleep 50ms
        elapsed = logger.elapsed()
        assert elapsed.endswith("s")
        # Parse the time value
        time_value = float(elapsed[:-1])
        assert time_value >= 0.05
        assert time_value < 0.2  # Should be well under 200ms

    @patch("specify_cli.verbose.console")
    def test_section_prints_when_enabled(self, mock_console):
        """Test section() prints when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.section("Test Section", "🔍")

        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "Test Section" in call_args
        assert "🔍" in call_args

    @patch("specify_cli.verbose.console")
    def test_section_no_op_when_disabled(self, mock_console):
        """Test section() does nothing when disabled."""
        logger = VerboseLogger(enabled=False)
        logger.section("Test Section", "🔍")

        mock_console.print.assert_not_called()

    @patch("specify_cli.verbose.console")
    def test_info_prints_when_enabled(self, mock_console):
        """Test info() prints when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.info("Test info message")

        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "Test info message" in call_args

    @patch("specify_cli.verbose.console")
    def test_info_no_op_when_disabled(self, mock_console):
        """Test info() does nothing when disabled."""
        logger = VerboseLogger(enabled=False)
        logger.info("Test info message")

        mock_console.print.assert_not_called()

    @patch("specify_cli.verbose.console")
    def test_success_prints_when_enabled(self, mock_console):
        """Test success() prints when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.success("Test success")

        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "Test success" in call_args

    @patch("specify_cli.verbose.console")
    def test_warning_prints_when_enabled(self, mock_console):
        """Test warning() prints when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.warning("Test warning")

        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "Test warning" in call_args

    @patch("specify_cli.verbose.console")
    def test_error_prints_when_enabled(self, mock_console):
        """Test error() prints when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.error("Test error")

        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "Test error" in call_args

    @patch("specify_cli.verbose.console")
    def test_detail_prints_when_enabled(self, mock_console):
        """Test detail() prints key-value when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.detail("key", "value")

        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "key" in call_args
        assert "value" in call_args

    @patch("specify_cli.verbose.console")
    def test_code_prints_when_enabled(self, mock_console):
        """Test code() prints syntax-highlighted code when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.code("print('hello')", "python")

        mock_console.print.assert_called_once()

    @patch("specify_cli.verbose.console")
    def test_table_prints_when_enabled(self, mock_console):
        """Test table() prints formatted table when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.table("Test Table", ["Col1", "Col2"], [["A", "B"], ["C", "D"]])

        mock_console.print.assert_called_once()

    @patch("specify_cli.verbose.console")
    def test_panel_prints_when_enabled(self, mock_console):
        """Test panel() prints panel when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.panel("Test content", "Test Title")

        mock_console.print.assert_called_once()

    @patch("specify_cli.verbose.console")
    def test_files_prints_all_when_under_limit(self, mock_console):
        """Test files() prints all files when under max_display."""
        logger = VerboseLogger(enabled=True)
        files = ["file1.py", "file2.py", "file3.py"]
        logger.files(files, max_display=10)

        assert mock_console.print.call_count == 3

    @patch("specify_cli.verbose.console")
    def test_files_truncates_when_over_limit(self, mock_console):
        """Test files() truncates when over max_display."""
        logger = VerboseLogger(enabled=True)
        files = [f"file{i}.py" for i in range(15)]
        logger.files(files, max_display=10)

        # 10 files + 1 "... and X more" message
        assert mock_console.print.call_count == 11

    @patch("specify_cli.verbose.console")
    def test_progress_prints_when_enabled(self, mock_console):
        """Test progress() prints progress info when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.progress(5, 10, "processing file.py")

        mock_console.print.assert_called_once()
        call_args = str(mock_console.print.call_args)
        assert "5" in call_args
        assert "10" in call_args
        assert "50.0%" in call_args

    @patch("specify_cli.verbose.console")
    def test_separator_prints_when_enabled(self, mock_console):
        """Test separator() prints separator when enabled."""
        logger = VerboseLogger(enabled=True)
        logger.separator()

        mock_console.print.assert_called_once()


class TestVerboseLoggerIntegration:
    """Integration tests for VerboseLogger."""

    @patch("specify_cli.verbose.console")
    def test_full_workflow(self, mock_console):
        """Test full verbose logging workflow."""
        logger = VerboseLogger(enabled=True)
        logger.start()
        logger.section("Test", "🔍")
        logger.info("Starting test")
        logger.detail("key", "value")
        logger.success("Test complete")
        elapsed = logger.elapsed()

        # Should have made 4 print calls
        assert mock_console.print.call_count == 4
        assert elapsed.endswith("s")

    @patch("specify_cli.verbose.console")
    def test_disabled_workflow_no_output(self, mock_console):
        """Test disabled logger produces no output."""
        logger = VerboseLogger(enabled=False)
        logger.start()
        logger.section("Test", "🔍")
        logger.info("Starting test")
        logger.detail("key", "value")
        logger.success("Test complete")
        logger.elapsed()

        # Should have made 0 print calls
        mock_console.print.assert_not_called()
