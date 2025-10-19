"""Test HTML escaping to prevent XSS attacks."""

from pathlib import Path
from specify_cli.reporters.html import write_html


def test_html_escapes_dynamic_fields(tmp_path: Path):
    """Verify all dynamic fields are escaped to prevent XSS."""
    code = [
        {
            "rule_id": "B101",
            "severity": "HIGH",
            "file_path": "x.py",
            "line": 1,
            "message": "<script>alert('XSS')</script>",
            "cwe": "79",
        }
    ]
    deps = [
        {
            "package": "<b>malicious</b>",
            "installed_version": "0.1",
            "advisory_id": "ADV-1",
            "severity": "HIGH",
            "fix_version": None,
        }
    ]

    out = tmp_path / "r.html"
    write_html(code, deps, out)
    content = out.read_text()

    # Verify script tags are escaped
    assert "<script>" not in content
    assert "&lt;script&gt;" in content
    # Note: Single quotes are also escaped as &#x27;
    assert "alert(&#x27;XSS&#x27;)" in content or "alert('XSS')" in content  # Content preserved

    # Verify HTML tags are escaped
    assert "<b>malicious</b>" not in content
    assert "&lt;b&gt;malicious&lt;/b&gt;" in content
