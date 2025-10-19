"""Audit command for static analysis."""
from __future__ import annotations
import json
from pathlib import Path
from shutil import which as _which
import typer
from rich.console import Console
from rich.panel import Panel

from specify_cli.runner import run_all, RunConfig
from specify_cli.reporters.sarif import combine_to_sarif, write_sarif
from specify_cli.reporters.html import write_html
from specify_cli.baseline import load_baseline, filter_with_baseline
from specify_cli.store import save_last_run
from specify_cli.config import load_config
from specify_cli.analyzers.bandit_analyzer import BANDIT as _BANDIT_OK

app = typer.Typer(help="Run static analysis")


def _gate_code(findings, threshold: str) -> int:
    """Check if findings exceed severity threshold.
    
    Args:
        findings: List of finding dictionaries
        threshold: Severity threshold (HIGH, MEDIUM, LOW)
        
    Returns:
        1 if threshold exceeded, 0 otherwise
    """
    sev = [str(f.get("severity", "")).upper() for f in findings]
    high = sev.count("HIGH") + sev.count("CRITICAL")
    med = sev.count("MEDIUM")
    low = sev.count("LOW")
    t = threshold.upper()
    if t == "HIGH" and high > 0:
        return 1
    if t == "MEDIUM" and (high + med) > 0:
        return 1
    if t == "LOW" and (high + med + low) > 0:
        return 1
    return 0


@app.command("run")
def audit(
    path: Path = typer.Option(Path.cwd(), "--path", help="Folder to analyze"),
    output: str = typer.Option(None, "--output", help="sarif or html or json"),
    fail_on: str = typer.Option(None, "--fail-on", help="HIGH or MEDIUM or LOW"),
    respect_baseline: bool = typer.Option(None, "--respect-baseline"),
    changed_only: bool = typer.Option(None, "--changed-only"),
    bandit: bool = typer.Option(None, "--bandit/--no-bandit"),
    safety: bool = typer.Option(None, "--safety/--no-safety"),
    strict: bool = typer.Option(False, "--strict", help="Fail if a requested analyzer is unavailable"),
):
    """Run security analysis with Bandit and Safety."""
    console = Console()
    cfg = load_config(path)
    
    # Merge config with CLI overrides
    eff_output = output or cfg.output.format
    eff_fail = fail_on or cfg.analysis.fail_on
    eff_baseline = cfg.analysis.respect_baseline if respect_baseline is None else respect_baseline
    eff_changed = cfg.analysis.changed_only if changed_only is None else changed_only
    use_bandit = cfg.analyzers.bandit if bandit is None else bandit
    use_safety = cfg.analyzers.safety if safety is None else safety

    # Check analyzer availability in strict mode
    if strict:
        missing = []
        if use_bandit and not _BANDIT_OK:
            missing.append("bandit")
        if use_safety and not _which("safety"):
            missing.append("safety")
        if missing:
            console.print(f"[red]Missing analyzers:[/red] {', '.join(missing)}")
            raise typer.Exit(code=2)
    
    # Merge config with CLI overrides
    eff_output = output or cfg.output.format
    eff_fail = fail_on or cfg.analysis.fail_on
    eff_baseline = cfg.analysis.respect_baseline if respect_baseline is None else respect_baseline
    eff_changed = cfg.analysis.changed_only if changed_only is None else changed_only
    use_bandit = cfg.analyzers.bandit if bandit is None else bandit
    use_safety = cfg.analyzers.safety if safety is None else safety

    console.print(Panel(
        f"Target: {path}\nOutput: {eff_output}\nFail on: {eff_fail}\nBandit: {use_bandit}\nSafety: {use_safety}\nExcludes: {cfg.exclude_paths}",
        title="Audit"
    ))

    # Run analyzers
    results = run_all(RunConfig(
        path=path,
        changed_only=eff_changed,
        use_bandit=use_bandit,
        use_safety=use_safety,
        exclude_globs=list(cfg.exclude_paths),
    ))

    code_findings = results.get("bandit", [])
    dep_findings = results.get("safety", [])

    # Apply baseline filtering
    if eff_baseline and code_findings:
        base = load_baseline()
        code_findings = filter_with_baseline(code_findings, base)

    # Write output
    out_dir = path / cfg.output.directory
    out_dir.mkdir(parents=True, exist_ok=True)

    if eff_output.lower() == "sarif":
        sarif = combine_to_sarif(code_findings, dep_findings, repo_root=path, dep_artifact_hint="requirements.txt")
        out = write_sarif(sarif, out_dir / "report.sarif")
        console.print(f"[green]SARIF written:[/green] {out}")
    elif eff_output.lower() == "html":
        out = write_html(code_findings, dep_findings, out_dir / "report.html")
        console.print(f"[green]HTML written:[/green] {out}")
    else:
        out = out_dir / "analysis.json"
        out.write_text(json.dumps({"code": code_findings, "dependencies": dep_findings}, indent=2))
        console.print(f"[green]JSON written:[/green] {out}")

    # Save last run
    save_last_run({"code": code_findings, "dependencies": dep_findings}, out_dir)

    # Check severity threshold
    rc = max(_gate_code(code_findings, eff_fail), _gate_code(dep_findings, eff_fail))
    raise typer.Exit(code=rc)
