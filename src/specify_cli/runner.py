"""Analysis runner orchestration."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List
from specify_cli.analyzers.bandit_analyzer import BanditAnalyzer


@dataclass
class RunConfig:
    """Configuration for analysis run."""
    path: Path
    changed_only: bool = False


def run_all(cfg: RunConfig) -> Dict[str, List[dict]]:
    """Run all enabled analyzers.
    
    Args:
        cfg: Run configuration
        
    Returns:
        Dictionary mapping analyzer name to list of findings
    """
    bandit = BanditAnalyzer(Path(cfg.path)).run()
    return {"bandit": [b.__dict__ for b in bandit]}
