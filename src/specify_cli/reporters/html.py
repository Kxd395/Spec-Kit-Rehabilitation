"""HTML reporter for security findings."""
from __future__ import annotations
from pathlib import Path
from typing import List, Dict


def write_html(findings: List[Dict], out_path: Path) -> Path:
    """Generate HTML report from findings.
    
    Args:
        findings: List of finding dictionaries
        out_path: Output path for HTML file
        
    Returns:
        Path to written HTML file
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Group by severity
    high = [f for f in findings if f.get("severity", "").upper() == "HIGH"]
    medium = [f for f in findings if f.get("severity", "").upper() == "MEDIUM"]
    low = [f for f in findings if f.get("severity", "").upper() == "LOW"]
    
    # Generate table rows
    rows = []
    for f in findings:
        severity = f.get("severity", "UNKNOWN")
        color = {"HIGH": "#dc3545", "MEDIUM": "#fd7e14", "LOW": "#ffc107"}.get(
            severity.upper(), "#6c757d"
        )
        rows.append(
            f'<tr>'
            f'<td><span class="badge" style="background-color:{color}">{severity}</span></td>'
            f'<td><code>{f.get("rule_id", "UNKNOWN")}</code></td>'
            f'<td><code>{f.get("file_path", "unknown")}:{f.get("line", 0)}</code></td>'
            f'<td>{f.get("message", "")}</td>'
            f'<td>{f.get("confidence", "UNKNOWN")}</td>'
            f'<td>{f.get("cwe") or "N/A"}</td>'
            f'</tr>'
        )
    
    html = f"""<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>SpecKit Security Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f8f9fa;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #212529;
            margin-bottom: 10px;
        }}
        .summary {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        .summary-item {{
            flex: 1;
            text-align: center;
        }}
        .summary-count {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .summary-label {{
            color: #6c757d;
            font-size: 14px;
            text-transform: uppercase;
        }}
        .high {{ color: #dc3545; }}
        .medium {{ color: #fd7e14; }}
        .low {{ color: #ffc107; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            text-align: left;
            padding: 12px;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #495057;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        code {{
            background: #f1f3f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            color: white;
            font-size: 12px;
            font-weight: 600;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #dee2e6;
            color: #6c757d;
            font-size: 14px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 SpecKit Security Report</h1>
        <p style="color: #6c757d; margin-bottom: 20px;">Static security analysis results</p>
        
        <div class="summary">
            <div class="summary-item">
                <div class="summary-count high">{len(high)}</div>
                <div class="summary-label">High</div>
            </div>
            <div class="summary-item">
                <div class="summary-count medium">{len(medium)}</div>
                <div class="summary-label">Medium</div>
            </div>
            <div class="summary-item">
                <div class="summary-count low">{len(low)}</div>
                <div class="summary-label">Low</div>
            </div>
            <div class="summary-item">
                <div class="summary-count">{len(findings)}</div>
                <div class="summary-label">Total</div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Severity</th>
                    <th>Rule</th>
                    <th>Location</th>
                    <th>Message</th>
                    <th>Confidence</th>
                    <th>CWE</th>
                </tr>
            </thead>
            <tbody>
                {"".join(rows) if rows else '<tr><td colspan="6" style="text-align:center;color:#6c757d;">No findings detected ✓</td></tr>'}
            </tbody>
        </table>
        
        <div class="footer">
            Generated by <strong>SpecKit</strong> • 
            Spec-first security analysis CLI
        </div>
    </div>
</body>
</html>"""
    
    out_path.write_text(html)
    return out_path
