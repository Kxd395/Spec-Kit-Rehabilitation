"""Configuration management for SpecKit."""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os

try:
    import tomllib  # py311+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore

# Script type choices for project initialization
SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}


def _env_bool(name: str, default: bool) -> bool:
    v = os.getenv(name, None)
    if v is None:
        return default
    return str(v).lower() in ("1", "true", "yes", "on")


@dataclass
class AnalysisCfg:
    fail_on: str = "HIGH"
    respect_baseline: bool = True
    changed_only: bool = False


@dataclass
class OutputCfg:
    format: str = "sarif"
    directory: str = ".speckit/analysis"


@dataclass
class AnalyzersCfg:
    bandit: bool = True
    safety: bool = True
    secrets: bool = False


@dataclass
class SecurityCfg:
    """Security analysis configuration."""

    severity_threshold: str = "MEDIUM"
    allow_list: list[str] | None = None  # Rule IDs to skip
    deny_list: list[str] | None = None  # Rule IDs to always report

    def __post_init__(self):
        if self.allow_list is None:
            self.allow_list = []
        if self.deny_list is None:
            self.deny_list = []


@dataclass
class CICfg:
    """CI/CD integration configuration."""

    fail_on_severity: str = "HIGH"
    max_findings: int = -1  # -1 = unlimited


@dataclass
class PerformanceCfg:
    """Performance tuning configuration."""

    max_workers: int = 4


@dataclass
class TelemetryCfg:
    """Telemetry configuration."""

    enabled: bool = False


@dataclass
class SpecKitConfig:
    analysis: AnalysisCfg | None = None
    output: OutputCfg | None = None
    analyzers: AnalyzersCfg | None = None
    security: SecurityCfg | None = None
    ci: CICfg | None = None
    performance: PerformanceCfg | None = None
    telemetry: TelemetryCfg | None = None
    exclude_paths: list[str] | None = None

    def __post_init__(self):
        if self.analysis is None:
            self.analysis = AnalysisCfg()
        if self.output is None:
            self.output = OutputCfg()
        if self.analyzers is None:
            self.analyzers = AnalyzersCfg()
        if self.security is None:
            self.security = SecurityCfg()
        if self.ci is None:
            self.ci = CICfg()
        if self.performance is None:
            self.performance = PerformanceCfg()
        if self.telemetry is None:
            self.telemetry = TelemetryCfg()
        if self.exclude_paths is None:
            self.exclude_paths = []

    @classmethod
    def from_dict(cls, data: dict) -> "SpecKitConfig":
        """Create config from dictionary (e.g., parsed TOML).

        Args:
            data: Configuration dictionary

        Returns:
            SpecKitConfig instance with values from dict
        """
        cfg = cls()

        # Security section
        if "security" in data:
            s = data["security"]
            assert cfg.security is not None  # Initialized in __post_init__
            cfg.security = SecurityCfg(
                severity_threshold=s.get("severity_threshold", cfg.security.severity_threshold),
                allow_list=s.get("allow_list", cfg.security.allow_list),
                deny_list=s.get("deny_list", cfg.security.deny_list),
            )

        # CI section
        if "ci" in data:
            c = data["ci"]
            assert cfg.ci is not None  # Initialized in __post_init__
            cfg.ci = CICfg(
                fail_on_severity=c.get("fail_on_severity", cfg.ci.fail_on_severity),
                max_findings=c.get("max_findings", cfg.ci.max_findings),
            )

        # Performance section
        if "performance" in data:
            p = data["performance"]
            assert cfg.performance is not None  # Initialized in __post_init__
            cfg.performance = PerformanceCfg(
                max_workers=p.get("max_workers", cfg.performance.max_workers),
            )

        # Telemetry section
        if "telemetry" in data:
            t = data["telemetry"]
            assert cfg.telemetry is not None  # Initialized in __post_init__
            cfg.telemetry = TelemetryCfg(
                enabled=t.get("enabled", cfg.telemetry.enabled),
            )

        # Analysis section
        if "analysis" in data:
            a = data["analysis"]
            assert cfg.analysis is not None  # Initialized in __post_init__
            cfg.analysis = AnalysisCfg(
                fail_on=a.get("fail_on", cfg.analysis.fail_on),
                respect_baseline=a.get("respect_baseline", cfg.analysis.respect_baseline),
                changed_only=a.get("changed_only", cfg.analysis.changed_only),
            )

        # Output section
        if "output" in data:
            o = data["output"]
            assert cfg.output is not None  # Initialized in __post_init__
            cfg.output = OutputCfg(
                format=o.get("format", cfg.output.format),
                directory=o.get("directory", cfg.output.directory),
            )

        # Analyzers section
        if "analyzers" in data:
            z = data["analyzers"]
            assert cfg.analyzers is not None  # Initialized in __post_init__
            cfg.analyzers = AnalyzersCfg(
                bandit=z.get("bandit", cfg.analyzers.bandit),
                safety=z.get("safety", cfg.analyzers.safety),
                secrets=z.get("secrets", cfg.analyzers.secrets),
            )

        # Exclude paths
        if "exclude" in data and "paths" in data["exclude"]:
            cfg.exclude_paths = list(data["exclude"]["paths"])

        return cfg


def load_config(repo_root: Path, file_path: Optional[Path] = None) -> SpecKitConfig:
    """Load configuration from .speckit.toml with ENV overrides.

    Args:
        repo_root: Repository root directory
        file_path: Optional specific config file path

    Returns:
        Complete configuration with TOML + ENV merged
    """
    path = file_path or (repo_root / ".speckit.toml")
    cfg = SpecKitConfig()
    if path.exists():
        data = tomllib.loads(path.read_text())
        a = data.get("analysis", {})
        o = data.get("output", {})
        z = data.get("analyzers", {})
        ex = data.get("exclude", {}).get("paths", [])
        assert cfg.analysis is not None  # Initialized in __post_init__
        assert cfg.output is not None  # Initialized in __post_init__
        assert cfg.analyzers is not None  # Initialized in __post_init__
        cfg.analysis = AnalysisCfg(
            fail_on=a.get("fail_on", cfg.analysis.fail_on),
            respect_baseline=a.get("respect_baseline", cfg.analysis.respect_baseline),
            changed_only=a.get("changed_only", cfg.analysis.changed_only),
        )
        cfg.output = OutputCfg(
            format=o.get("format", cfg.output.format),
            directory=o.get("directory", cfg.output.directory),
        )
        cfg.analyzers = AnalyzersCfg(
            bandit=z.get("bandit", cfg.analyzers.bandit),
            safety=z.get("safety", cfg.analyzers.safety),
            secrets=z.get("secrets", cfg.analyzers.secrets),
        )
        cfg.exclude_paths = list(ex or [])

    # ENV overrides
    assert cfg.analysis is not None  # Initialized in __post_init__
    assert cfg.output is not None  # Initialized in __post_init__
    cfg.analysis.fail_on = os.getenv("SPECKIT_FAIL_ON", cfg.analysis.fail_on)
    cfg.analysis.respect_baseline = _env_bool(
        "SPECKIT_RESPECT_BASELINE", cfg.analysis.respect_baseline
    )
    cfg.analysis.changed_only = _env_bool("SPECKIT_CHANGED_ONLY", cfg.analysis.changed_only)
    cfg.output.format = os.getenv("SPECKIT_OUTPUT", cfg.output.format)
    cfg.output.directory = os.getenv("SPECKIT_OUT_DIR", cfg.output.directory)
    assert cfg.analyzers is not None  # Initialized in __post_init__
    cfg.analyzers.bandit = _env_bool("SPECKIT_BANDIT", cfg.analyzers.bandit)
    cfg.analyzers.safety = _env_bool("SPECKIT_SAFETY", cfg.analyzers.safety)
    cfg.analyzers.secrets = _env_bool("SPECKIT_SECRETS", cfg.analyzers.secrets)
    return cfg


def get_severity_level(severity: str) -> int:
    """Convert severity string to numeric level.

    Args:
        severity: Severity string (LOW, MEDIUM, HIGH, CRITICAL)

    Returns:
        Numeric level (0=LOW, 1=MEDIUM, 2=HIGH, 3=CRITICAL)
    """
    severity_map = {
        "LOW": 0,
        "MEDIUM": 1,
        "HIGH": 2,
        "CRITICAL": 3,
    }
    return severity_map.get(severity.upper(), 1)  # Default to MEDIUM


def should_report_finding(
    finding_severity: str,
    threshold: str,
    allow_list: list[str],
    deny_list: list[str],
    rule_id: str,
) -> bool:
    """Determine if a finding should be reported.

    Args:
        finding_severity: Severity of the finding
        threshold: Minimum severity threshold
        allow_list: Rule IDs to skip (even if they meet threshold)
        deny_list: Rule IDs to always report (even if below threshold)
        rule_id: The finding's rule ID

    Returns:
        True if finding should be reported, False otherwise
    """
    # Check deny list first (highest priority)
    if rule_id in deny_list:
        return True

    # Check allow list (skip even if meets threshold)
    if rule_id in allow_list:
        return False

    # Check severity threshold
    finding_level = get_severity_level(finding_severity)
    threshold_level = get_severity_level(threshold)

    return finding_level >= threshold_level
