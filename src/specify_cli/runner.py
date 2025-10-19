"""Analysis runner orchestration."""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List

from specify_cli.analyzers.bandit_analyzer import BanditAnalyzer
from specify_cli.analyzers.safety_analyzer import SafetyAnalyzer


@dataclass
class RunConfig:
    """Configuration for analysis run."""

    path: Path
    changed_only: bool = False
    use_bandit: bool = True
    use_safety: bool = True
    exclude_globs: List[str] = field(default_factory=list)


def run_all(cfg: RunConfig) -> Dict[str, List[dict]]:
    """Run all enabled analyzers.

    Args:
        cfg: Run configuration

    Returns:
        Dictionary mapping analyzer name to list of findings
    """
    out: Dict[str, List[dict]] = {}
    excludes = cfg.exclude_globs or []

    if cfg.use_bandit:
        bandit = BanditAnalyzer(Path(cfg.path), exclude_globs=excludes).run()
        out["bandit"] = [asdict(b) for b in bandit]

    if cfg.use_safety:
        safety = SafetyAnalyzer(Path(cfg.path)).run()
        out["safety"] = [asdict(s) for s in safety]

    return out
