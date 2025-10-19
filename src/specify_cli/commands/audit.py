"""Audit command for running security analysis."""
from __future__ import annotations
import json
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel

from specify_cli.runner import run_all, RunConfig
from specify_cli.reporters.sarif_bandit import bandit_findings_to_sarif, write_sarif
from specify_cli.baseline import load_baseline, filter_with_baseline
from specify_cli.store import save_last_run

app = typer.Typer(help="Run static analysis")


@app.command("run")
def audit(
    path: Path = typer.Option(Path.cwd(), "--path", help="Folder to analyze"),
    output: str = typer.Option("sarif", "--output", help="sarif or html or json or markdown"),
    fail_on: str = typer.Option("HIGH", "--fail-on", help="HIGH or MEDIUM or LOW"),
    respect_baseline: bool = typer.Option(True, "--respect-baseline", help="Filter baseline findings"),
    changed_only: bool = typer.Option(False, "--changed-only", help="Only scan changed files"),
):
    """Run security audit and generate report."""
    console = Console()
    console.print(
        Panel(
            f"Target: {path}\nOutput: {output}\nFail on: {fail_on}\n"
            f"Baseline: {respect_baseline}\nChanged only: {changed_only}",
            title="Audit"
        )
    )

    # Run analyzers
    results = run_all(RunConfig(path=path, changed_only=changed_only))
    findings = results.get("bandit", [])

    # Apply baseline filter
    if respect_baseline:
        base = load_baseline()
        if base:
            original_count = len(findings)
            findings = filter_with_baseline(findings, base)
            console.print(f"[yellow]Baseline filtered {original_count - len(findings)} findings[/yellow]")

    out_dir = path / ".speckit" / "analysis"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate output
    if output.lower() == "sarif":
        sarif = bandit_findings_to_sarif(findings, repo_root=path)
        out = write_sarif(sarif, out_dir / "report.sarif")
        console.print(f"[green]SARIF written:[/green] {out}")
    elif output.lower() == "html":
        # Import here to avoid circular dependency
        from specify_cli.reporters.html import write_html
        out = write_html(findings, out_dir / "report.html")
        console.print(f"[green]HTML written:[/green] {out}")
    elif output.lower() == "json":
        out = out_dir / "analysis.json"
        out.write_text(json.dumps(findings, indent=2))
        console.print(f"[green]JSON written:[/green] {out}")
    else:  # markdown
        out = out_dir / "security-report.md"
        lines = [f"# Security report", "", f"Findings: {len(findings)}", ""]
        for f in findings:
            lines += [
                f"## {f.get('rule_id', 'UNKNOWN')} - {f.get('severity', 'UNKNOWN')}",
                f"- File: `{f.get('file_path', 'unknown')}:{f.get('line', 0)}`",
                f"- Message: {f.get('message', '')}",
                f"- Confidence: {f.get('confidence', 'UNKNOWN')}",
                f"- CWE: {f.get('cwe') or 'N/A'}",
                ""
            ]
        out.write_text("\n".join(lines))
        console.print(f"[green]Markdown written:[/green] {out}")

    # Save for delta reporting
    save_last_run({"findings": findings}, out_dir)

    # Calculate exit code
    high = sum(1 for f in findings if (f.get("severity", "").upper() == "HIGH"))
    med = sum(1 for f in findings if (f.get("severity", "").upper() == "MEDIUM"))
    low = sum(1 for f in findings if (f.get("severity", "").upper() == "LOW"))

    console.print(f"\n[bold]Summary:[/bold] {high} HIGH, {med} MEDIUM, {low} LOW")

    rc = 0
    if fail_on.upper() == "HIGH" and high > 0:
        console.print("[red]Failing due to HIGH severity findings[/red]")
        rc = 1
    elif fail_on.upper() == "MEDIUM" and (high + med) > 0:
        console.print("[red]Failing due to MEDIUM+ severity findings[/red]")
        rc = 1
    elif fail_on.upper() == "LOW" and (high + med + low) > 0:
        console.print("[red]Failing due to LOW+ severity findings[/red]")
        rc = 1
    
    if rc == 0:
        console.print("[green]✓ All checks passed[/green]")
    
    raise typer.Exit(code=rc)
