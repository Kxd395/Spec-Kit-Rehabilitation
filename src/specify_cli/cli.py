"""Specify CLI - Spec-first analysis tool."""
from __future__ import annotations
from pathlib import Path
import json
import typer
from rich.console import Console
from rich.panel import Panel

from specify_cli.analyzers.bandit_analyzer import BanditAnalyzer
from specify_cli.reporters.sarif_bandit import bandit_findings_to_sarif, write_sarif

app = typer.Typer(help="Spec-first analysis CLI")
console = Console()


@app.command()
def audit(
    path: Path = typer.Option(Path.cwd(), "--path", help="Folder to analyze"),
    output: str = typer.Option("sarif", "--output", help="Output format: sarif, json, or markdown"),
    fail_on: str = typer.Option("HIGH", "--fail-on", help="Severity threshold: HIGH, MEDIUM, or LOW"),
):
    """Run security audit on Python code.
    
    Scans Python files using Bandit and generates reports in multiple formats.
    Exit code is non-zero if findings exceed the --fail-on threshold.
    """
    console.print(Panel(f"Target: {path}\nOutput: {output}\nFail on: {fail_on}", title="Audit"))
    
    analyzer = BanditAnalyzer(path)
    findings = analyzer.run()
    console.print(f"Bandit findings: {len(findings)}")

    out_dir = path / ".speckit" / "analysis"
    out_dir.mkdir(parents=True, exist_ok=True)

    if output.lower() == "sarif":
        sarif = bandit_findings_to_sarif(
            [f.__dict__ for f in findings], repo_root=path
        )
        out = write_sarif(sarif, out_dir / "report.sarif")
        console.print(f"[green]SARIF written:[/green] {out}")
    elif output.lower() == "json":
        out = out_dir / "analysis.json"
        out.write_text(json.dumps([f.__dict__ for f in findings], indent=2))
        console.print(f"[green]JSON written:[/green] {out}")
    else:
        out = out_dir / "security-report.md"
        lines = [f"# Security report", "", f"Findings: {len(findings)}", ""]
        for f in findings:
            lines += [
                f"## {f.rule_id} - {f.severity}",
                f"- File: `{f.file_path}:{f.line}`",
                f"- Message: {f.message}",
                f"- Confidence: {f.confidence}",
                f"- CWE: {f.cwe or 'N/A'}",
                ""
            ]
        out.write_text("\n".join(lines))
        console.print(f"[green]Markdown written:[/green] {out}")

    # exit code policy
    high = sum(1 for f in findings if f.severity.upper() == "HIGH")
    med = sum(1 for f in findings if f.severity.upper() == "MEDIUM")
    low = sum(1 for f in findings if f.severity.upper() == "LOW")

    rc = 0
    if fail_on.upper() == "HIGH" and high > 0:
        rc = 1
    elif fail_on.upper() == "MEDIUM" and (high + med) > 0:
        rc = 1
    elif fail_on.upper() == "LOW" and (high + med + low) > 0:
        rc = 1
    
    if rc != 0:
        console.print(f"[red]Exit code {rc}:[/red] Found {high} HIGH, {med} MEDIUM, {low} LOW")
    
    raise typer.Exit(code=rc)


if __name__ == "__main__":
    app()
