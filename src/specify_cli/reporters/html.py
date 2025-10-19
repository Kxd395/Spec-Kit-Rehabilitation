"""HTML reporter for security findings."""
from __future__ import annotations
from pathlib import Path
from typing import List, Dict
import html as _html


def _e(v) -> str:
    """Escape HTML to prevent XSS."""
    return _html.escape("" if v is None else str(v), quote=True)


def write_html(code_findings: List[Dict], dep_findings: List[Dict], out_path: Path) -> Path:
    """Generate HTML report from findings."""
    out_path.parent.mkdir(parents=True, exist_ok=True)

    def _rows_code() -> str:
        rows = []
        for f in code_findings:
            rows.append(
                "<tr>"
                f"<td>{_e(f.get('rule_id'))}</td>"
                f"<td>{_e(f.get('severity'))}</td>"
                f"<td>{_e(f.get('file_path'))}:{_e(f.get('line'))}</td>"
                f"<td>{_e(f.get('message'))}</td>"
                f"<td>{_e(f.get('cwe'))}</td>"
                "</tr>"
            )
        return "".join(rows)

    def _rows_deps() -> str:
        rows = []
        for v in dep_findings:
            rows.append(
                "<tr>"
                f"<td>{_e(v.get('package'))}</td>"
                f"<td>{_e(v.get('installed_version'))}</td>"
                f"<td>{_e(v.get('advisory_id') or v.get('cve'))}</td>"
                f"<td>{_e(v.get('severity'))}</td>"
                f"<td>{_e(v.get('fix_version') or 'N/A')}</td>"
                "</tr>"
            )
        return "".join(rows)

    html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>SpecKit Report</title>
<style>body{{font-family:system-ui,Arial}} table{{border-collapse:collapse;width:100%}} td,th{{border:1px solid #ccc;padding:6px}}</style>
</head><body>
<h1>SpecKit Security Report</h1>
<h2>Code issues</h2>
<p>Total: {_e(len(code_findings))}</p>
<table><thead><tr><th>Rule</th><th>Severity</th><th>Location</th><th>Message</th><th>CWE</th></tr></thead>
<tbody>{_rows_code()}</tbody></table>
<h2>Dependency CVEs</h2>
<p>Total: {_e(len(dep_findings))}</p>
<table><thead><tr><th>Package</th><th>Installed</th><th>Advisory or CVE</th><th>Severity</th><th>Fix</th></tr></thead>
<tbody>{_rows_deps()}</tbody></table>
</body></html>"""
    out_path.write_text(html_doc)
    return out_path
