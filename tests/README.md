# Tests

Unit and integration tests for Spec-Kit.

## Run Tests

```bash
# Run all tests
pytest --maxfail=1 -q

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_cli.py -v
```

## Test Organization

- `test_cli.py` - CLI integration tests
- `test_html_escapes.py` - XSS prevention tests
- `test_safety_error_handling.py` - Error handling tests
- `test_excludes_applied.py` - Exclude pattern tests
- `test_config_loading.py` - Configuration tests
- `test_sarif_generation.py` - SARIF output tests
- `test_bandit_integration.py` - Bandit analyzer tests
- `acceptance/` - End-to-end acceptance tests

## Test Focus Areas

### Security Tests
- HTML escaping (XSS prevention)
- Error handling (missing tools, invalid inputs)
- Path traversal prevention
- Command injection prevention

### Functional Tests
- Analyzer execution and output parsing
- Reporter format correctness
- Configuration precedence (CLI > ENV > TOML)
- Baseline filtering logic

### Integration Tests
- Full audit command flow
- Exit code gating by severity
- Strict mode analyzer checks
- Multi-format output generation

## Writing Tests

### Unit Test Example

```python
from pathlib import Path
import pytest

def test_example(tmp_path: Path):
    # Arrange
    test_file = tmp_path / "test.py"
    test_file.write_text("x = 1")

    # Act
    result = your_function(test_file)

    # Assert
    assert result == expected_value
```

### Integration Test Example

```python
from typer.testing import CliRunner
from specify_cli import app

def test_audit_command():
    runner = CliRunner()
    result = runner.invoke(app, ["audit", "run", "--help"])
    assert result.exit_code == 0
    assert "audit" in result.stdout
```

## Test Fixtures

Use `tmp_path` fixture for temporary file creation:

```python
def test_with_temp_files(tmp_path: Path):
    config_file = tmp_path / ".speckit.toml"
    config_file.write_text("[analysis]\nfail_on='HIGH'")
    # Test logic here
```

## Mocking External Tools

For tests that interact with external tools (Bandit, Safety):

```python
def test_safety_missing_cli(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda _: None)
    with pytest.raises(FileNotFoundError):
        SafetyAnalyzer(Path.cwd()).run()
```

## Coverage Goals

- **Overall**: 70% minimum (enforced by CI)
- **Analyzers**: 80%+ (critical security code)
- **Reporters**: 80%+ (output correctness)
- **Commands**: 70%+ (CLI integration)
- **Core modules**: 80%+ (config, runner, baseline)

## Running Specific Test Categories

```bash
# Security tests only
pytest tests/test_html_escapes.py tests/test_safety_error_handling.py

# Analyzer tests only
pytest tests/test_*_analyzer.py

# Acceptance tests only
pytest tests/acceptance/
```

## Best Practices

- Keep tests isolated (no shared state)
- Use descriptive test names (test_what_when_expected)
- Test edge cases (empty inputs, None values, etc.)
- Mock external dependencies
- Assert specific error messages
- Clean up resources (use fixtures and tmp_path)
