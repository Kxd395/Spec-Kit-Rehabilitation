"""Storage for analysis run history."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict


def save_last_run(data: Dict, out_dir: Path) -> Path:
    """Save last run data for delta reporting.
    
    Args:
        data: Analysis results data
        out_dir: Output directory
        
    Returns:
        Path to saved file
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / "last_run.json"
    p.write_text(json.dumps(data, indent=2))
    return p
