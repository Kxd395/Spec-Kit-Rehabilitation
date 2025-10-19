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
class SpecKitConfig:
    analysis: AnalysisCfg = None
    output: OutputCfg = None
    analyzers: AnalyzersCfg = None
    exclude_paths: list[str] = None
    
    def __post_init__(self):
        if self.analysis is None:
            self.analysis = AnalysisCfg()
        if self.output is None:
            self.output = OutputCfg()
        if self.analyzers is None:
            self.analyzers = AnalyzersCfg()
        if self.exclude_paths is None:
            self.exclude_paths = []

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
    cfg.analysis.fail_on = os.getenv("SPECKIT_FAIL_ON", cfg.analysis.fail_on)
    cfg.analysis.respect_baseline = _env_bool("SPECKIT_RESPECT_BASELINE", cfg.analysis.respect_baseline)
    cfg.analysis.changed_only = _env_bool("SPECKIT_CHANGED_ONLY", cfg.analysis.changed_only)
    cfg.output.format = os.getenv("SPECKIT_OUTPUT", cfg.output.format)
    cfg.output.directory = os.getenv("SPECKIT_OUT_DIR", cfg.output.directory)
    cfg.analyzers.bandit = _env_bool("SPECKIT_BANDIT", cfg.analyzers.bandit)
    cfg.analyzers.safety = _env_bool("SPECKIT_SAFETY", cfg.analyzers.safety)
    cfg.analyzers.secrets = _env_bool("SPECKIT_SECRETS", cfg.analyzers.secrets)
    return cfg
