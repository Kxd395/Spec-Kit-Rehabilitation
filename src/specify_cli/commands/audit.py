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
from specify_cli.verbose import VerboseLogger

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
    strict: bool = typer.Option(
        False, "--strict", help="Fail if a requested analyzer is unavailable"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """Run security analysis with Bandit and Safety."""
    console = Console()
    logger = VerboseLogger(enabled=verbose)
    logger.start()

    logger.section("Configuration", "⚙️")
    logger.info(f"Loading config from: {path}")
    cfg = load_config(path)

    # Merge config with CLI overrides
    eff_output = output or cfg.output.format
    eff_fail = fail_on or cfg.analysis.fail_on
    eff_baseline = cfg.analysis.respect_baseline if respect_baseline is None else respect_baseline
    eff_changed = cfg.analysis.changed_only if changed_only is None else changed_only
    use_bandit = cfg.analyzers.bandit if bandit is None else bandit
    use_safety = cfg.analyzers.safety if safety is None else safety

    logger.detail("Output format", eff_output)
    logger.detail("Fail threshold", eff_fail)
    logger.detail("Baseline filtering", str(eff_baseline))
    logger.detail("Changed files only", str(eff_changed))
    logger.detail("Use Bandit", str(use_bandit))
    logger.detail("Use Safety", str(use_safety))
    logger.detail("Exclude patterns", str(cfg.exclude_paths))

    # Check analyzer availability in strict mode
    logger.section("Analyzer Availability", "🔍")
    if strict:
        logger.info("Strict mode enabled - checking analyzer availability")
        missing = []
        if use_bandit and not _BANDIT_OK:
            missing.append("bandit")
            logger.error("Bandit not available")
        else:
            logger.success("Bandit available")
        if use_safety and not _which("safety"):
            missing.append("safety")
            logger.error("Safety not available")
        else:
            logger.success("Safety available")
        if missing:
            console.print(f"[red]Missing analyzers:[/red] {', '.join(missing)}")
            raise typer.Exit(code=2)
    else:
        logger.info("Checking available analyzers")
        if use_bandit:
            status = "✅ available" if _BANDIT_OK else "⚠️ unavailable (will skip)"
            logger.info(f"Bandit: {status}")
        if use_safety:
            status = "✅ available" if _which("safety") else "⚠️ unavailable (will skip)"
            logger.info(f"Safety: {status}")

    logger.section("Running Analysis", "🔬")
    console.print(
        Panel(
            f"Target: {path}\nOutput: {eff_output}\nFail on: {eff_fail}\nBandit: {use_bandit}\nSafety: {use_safety}\nExcludes: {cfg.exclude_paths}",
            title="Audit",
        )
    )

    # Run analyzers
    logger.info("Executing analyzers...")
    results = run_all(
        RunConfig(
            path=path,
            changed_only=eff_changed,
            use_bandit=use_bandit,
            use_safety=use_safety,
            exclude_globs=list(cfg.exclude_paths),
        )
    )
    logger.success(f"Analysis complete in {logger.elapsed()}")

    code_findings = results.get("bandit", [])
    dep_findings = results.get("safety", [])

    logger.section("Results Summary", "📊")
    logger.info(f"Code findings: {len(code_findings)}")
    logger.info(f"Dependency findings: {len(dep_findings)}")

    # Apply baseline filtering
    if eff_baseline and code_findings:
        logger.info("Applying baseline filtering...")
        base = load_baseline()
        original_count = len(code_findings)
        code_findings = filter_with_baseline(code_findings, base)
        filtered = original_count - len(code_findings)
        logger.success(f"Filtered {filtered} findings using baseline")

    # Write output
    logger.section("Output Generation", "📝")
    out_dir = path / cfg.output.directory
    out_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Output directory: {out_dir}")

    if eff_output.lower() == "sarif":
        logger.info("Generating SARIF report...")
        sarif = combine_to_sarif(
            code_findings, dep_findings, repo_root=path, dep_artifact_hint="requirements.txt"
        )
        out = write_sarif(sarif, out_dir / "report.sarif")
        console.print(f"[green]SARIF written:[/green] {out}")
        logger.success(f"SARIF report: {out}")
    elif eff_output.lower() == "html":
        logger.info("Generating HTML report...")
        out = write_html(code_findings, dep_findings, out_dir / "report.html")
        console.print(f"[green]HTML written:[/green] {out}")
        logger.success(f"HTML report: {out}")
    else:
        logger.info("Generating JSON report...")
        out = out_dir / "analysis.json"
        out.write_text(json.dumps({"code": code_findings, "dependencies": dep_findings}, indent=2))
        console.print(f"[green]JSON written:[/green] {out}")
        logger.success(f"JSON report: {out}")

    # Save last run
    logger.info("Saving run metadata...")
    save_last_run({"code": code_findings, "dependencies": dep_findings}, out_dir)
    logger.success("Metadata saved")

    # Check severity threshold
    logger.section("Exit Code Determination", "🚦")
    rc = max(_gate_code(code_findings, eff_fail), _gate_code(dep_findings, eff_fail))
    if rc == 0:
        logger.success(f"No issues above threshold '{eff_fail}' - exiting with code 0")
    else:
        logger.warning(f"Found issues above threshold '{eff_fail}' - exiting with code {rc}")
    raise typer.Exit(code=rc)
