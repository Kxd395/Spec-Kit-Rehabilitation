"""Configuration loader for Spec-Kit.

Loads and validates .speckit.toml configuration files.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import tomli as tomllib
except ImportError:
    import tomllib  # Python 3.11+

from dataclasses import dataclass, field


@dataclass
class ScanConfig:
    """File scanning configuration."""
    includes: List[str] = field(default_factory=lambda: ["**/*.py"])
    excludes: List[str] = field(default_factory=list)
    changed_only: bool = False


@dataclass
class SecurityConfig:
    """Security scanning configuration."""
    severity_threshold: str = "MEDIUM"
    allow: List[str] = field(default_factory=list)
    deny: List[str] = field(default_factory=list)
    bandit_enabled: bool = True
    safety_enabled: bool = True
    secrets_enabled: bool = True


@dataclass
class DependencyConfig:
    """Dependency scanning configuration."""
    manager: str = "pip"
    fail_on: str = "HIGH"
    check_outdated: bool = True


@dataclass
class QualityConfig:
    """Code quality configuration."""
    complexity_threshold: int = 10
    maintainability_threshold: int = 20
    max_function_lines: int = 50
    max_nesting_depth: int = 4
    radon_enabled: bool = True
    duplication_enabled: bool = False


@dataclass
class SecretsConfig:
    """Secrets detection configuration."""
    entropy_threshold: float = 4.5
    allowlist_patterns: List[str] = field(default_factory=list)


@dataclass
class ReportConfig:
    """Report generation configuration."""
    formats: List[str] = field(default_factory=lambda: ["markdown"])
    out_dir: str = ".speckit/analysis"
    include_snippets: bool = True
    group_by_severity: bool = True


@dataclass
class BaselineConfig:
    """Baseline and suppression configuration."""
    file: str = ".speckit/baseline.json"
    respect_baseline: bool = True
    respect_inline_suppressions: bool = True


@dataclass
class PerformanceConfig:
    """Performance and caching configuration."""
    max_workers: int = 4
    warm_cache: bool = True
    cache_dir: str = ".speckit/cache"


@dataclass
class CIConfig:
    """CI/CD integration configuration."""
    fail_on_severity: str = "HIGH"
    max_findings: int = -1  # -1 = unlimited
    pr_mode: bool = False


@dataclass
class TelemetryConfig:
    """Telemetry configuration."""
    enabled: bool = False
    anonymous: bool = True


@dataclass
class SpecKitConfig:
    """Complete Spec-Kit configuration."""
    scan: ScanConfig = field(default_factory=ScanConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    dependencies: DependencyConfig = field(default_factory=DependencyConfig)
    quality: QualityConfig = field(default_factory=QualityConfig)
    secrets: SecretsConfig = field(default_factory=SecretsConfig)
    report: ReportConfig = field(default_factory=ReportConfig)
    baseline: BaselineConfig = field(default_factory=BaselineConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    ci: CIConfig = field(default_factory=CIConfig)
    telemetry: TelemetryConfig = field(default_factory=TelemetryConfig)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpecKitConfig":
        """Create config from dictionary."""
        return cls(
            scan=ScanConfig(**data.get("scan", {})),
            security=SecurityConfig(**data.get("security", {})),
            dependencies=DependencyConfig(**data.get("dependencies", {})),
            quality=QualityConfig(**data.get("quality", {})),
            secrets=SecretsConfig(**data.get("secrets", {})),
            report=ReportConfig(**data.get("report", {})),
            baseline=BaselineConfig(**data.get("baseline", {})),
            performance=PerformanceConfig(**data.get("performance", {})),
            ci=CIConfig(**data.get("ci", {})),
            telemetry=TelemetryConfig(**data.get("telemetry", {})),
        )


def find_config_file(start_path: Optional[Path] = None) -> Optional[Path]:
    """Find .speckit.toml by walking up directory tree.
    
    Args:
        start_path: Directory to start searching from (defaults to cwd)
        
    Returns:
        Path to config file, or None if not found
    """
    current = start_path or Path.cwd()
    
    # Walk up to root
    while True:
        config_path = current / ".speckit.toml"
        if config_path.exists():
            return config_path
            
        # Check if we've reached root
        parent = current.parent
        if parent == current:
            break
        current = parent
    
    return None


def load_config(
    config_path: Optional[Path] = None,
    search: bool = True
) -> SpecKitConfig:
    """Load configuration from file.
    
    Args:
        config_path: Explicit path to config file
        search: If True and config_path is None, search for config file
        
    Returns:
        SpecKitConfig with defaults for missing values
    """
    # If no explicit path, search for config
    if config_path is None and search:
        config_path = find_config_file()
    
    # If still no config, return defaults
    if config_path is None:
        return SpecKitConfig()
    
    # Load TOML file
    try:
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
        return SpecKitConfig.from_dict(data)
    except Exception as e:
        raise ValueError(f"Failed to load config from {config_path}: {e}")


def get_severity_level(severity: str) -> int:
    """Convert severity string to numeric level.
    
    Args:
        severity: Severity string (LOW, MEDIUM, HIGH, CRITICAL)
        
    Returns:
        Numeric level (0-3)
    """
    levels = {
        "LOW": 0,
        "MEDIUM": 1,
        "HIGH": 2,
        "CRITICAL": 3,
    }
    return levels.get(severity.upper(), 0)


def should_report_finding(
    finding_severity: str,
    threshold: str,
    allowed_rules: List[str],
    denied_rules: List[str],
    rule_id: Optional[str] = None,
) -> bool:
    """Determine if finding should be reported based on config.
    
    Args:
        finding_severity: Severity of the finding
        threshold: Configured severity threshold
        allowed_rules: List of rule IDs to suppress
        denied_rules: List of rule IDs to always report
        rule_id: ID of the rule that generated finding
        
    Returns:
        True if finding should be reported
    """
    # Check if rule is explicitly denied (always report)
    if rule_id and rule_id in denied_rules:
        return True
    
    # Check if rule is explicitly allowed (never report)
    if rule_id and rule_id in allowed_rules:
        return False
    
    # Check severity threshold
    finding_level = get_severity_level(finding_severity)
    threshold_level = get_severity_level(threshold)
    
    return finding_level >= threshold_level


# Environment variable overrides
def apply_env_overrides(config: SpecKitConfig) -> SpecKitConfig:
    """Apply environment variable overrides to config.
    
    Environment variables take precedence over config file.
    
    Supported variables:
        SPECKIT_SEVERITY_THRESHOLD: Override security.severity_threshold
        SPECKIT_FAIL_ON_SEVERITY: Override ci.fail_on_severity
        SPECKIT_MAX_FINDINGS: Override ci.max_findings
        SPECKIT_TELEMETRY: Override telemetry.enabled (1/0, true/false)
    """
    # Severity threshold
    if threshold := os.getenv("SPECKIT_SEVERITY_THRESHOLD"):
        config.security.severity_threshold = threshold
    
    # CI fail on severity
    if fail_on := os.getenv("SPECKIT_FAIL_ON_SEVERITY"):
        config.ci.fail_on_severity = fail_on
    
    # Max findings
    if max_findings := os.getenv("SPECKIT_MAX_FINDINGS"):
        try:
            config.ci.max_findings = int(max_findings)
        except ValueError:
            pass
    
    # Telemetry
    if telemetry := os.getenv("SPECKIT_TELEMETRY"):
        config.telemetry.enabled = telemetry.lower() in ("1", "true", "yes")
    
    return config
