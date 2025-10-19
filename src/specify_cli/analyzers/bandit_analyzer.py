"""Bandit security analyzer for Python code."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any

try:
    from bandit.core import manager as bandit_manager
    from bandit.core import config as bandit_config
    BANDIT = True
except Exception:
    BANDIT = False

SEVERITY_MAP = {"LOW": "note", "MEDIUM": "warning", "HIGH": "error"}


@dataclass
class BanditFinding:
    """Represents a single Bandit security finding."""
    file_path: str
    line: int
    rule_id: str
    severity: str
    confidence: str
    message: str
    cwe: int | None


class BanditAnalyzer:
    """Wrapper for Bandit security scanner."""
    
    def __init__(self, target: Path):
        """Initialize analyzer with target path.
        
        Args:
            target: Directory or file to analyze
        """
        self.target = Path(target)

    def run(self) -> List[BanditFinding]:
        """Run Bandit analysis on target.
        
        Returns:
            List of BanditFinding objects
        """
        if not BANDIT:
            return []
        
        cfg = bandit_config.BanditConfig()
        mgr = bandit_manager.BanditManager(cfg, "file")
        
        # Find Python files, excluding common patterns
        py_files = []
        for p in self.target.rglob("*.py"):
            # Skip virtual environments and build artifacts
            if any(part in p.parts for part in ['.venv', 'venv', '.tox', 'build', 'dist', '__pycache__']):
                continue
            py_files.append(str(p))
        
        if not py_files:
            return []
        
        mgr.discover_files(py_files)
        mgr.run_tests()
        
        out: List[BanditFinding] = []
        for i in mgr.get_issue_list():
            cwe = None
            if hasattr(i, "cwe") and isinstance(i.cwe, dict):
                cwe = i.cwe.get("id")
            
            # Handle both old and new attribute names
            severity = getattr(i, 'issue_severity', getattr(i, 'severity', 'MEDIUM'))
            confidence = getattr(i, 'issue_confidence', getattr(i, 'confidence', 'MEDIUM'))
            
            out.append(
                BanditFinding(
                    file_path=i.fname,
                    line=int(getattr(i, "lineno", 1) or 1),
                    rule_id=i.test_id or "BXXX",
                    severity=str(severity),
                    confidence=str(confidence),
                    message=i.text or "",
                    cwe=cwe,
                )
            )
        return out

    @staticmethod
    def to_dicts(findings: List[BanditFinding]) -> List[Dict[str, Any]]:
        """Convert findings to dictionaries.
        
        Args:
            findings: List of BanditFinding objects
            
        Returns:
            List of dictionaries
        """
        return [asdict(f) for f in findings]
