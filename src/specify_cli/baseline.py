"""Baseline management for Spec-Kit.

Create and manage baselines to suppress existing findings during adoption.
"""

import json
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from datetime import datetime


class Baseline:
    """Baseline manager for suppressing known findings."""
    
    def __init__(self, baseline_path: Path):
        """Initialize baseline manager.
        
        Args:
            baseline_path: Path to baseline JSON file
        """
        self.baseline_path = baseline_path
        self.findings: Dict[str, Dict[str, Any]] = {}
        self.metadata: Dict[str, Any] = {}
        
        if baseline_path.exists():
            self.load()
    
    def _finding_hash(self, finding: Dict[str, Any]) -> str:
        """Generate stable hash for a finding.
        
        Hash is based on: file path, line, rule ID, and message.
        This ensures findings are matched even if column changes slightly.
        
        Args:
            finding: Finding dictionary
            
        Returns:
            SHA256 hash as hex string
        """
        key_parts = [
            finding.get("file", ""),
            str(finding.get("line", 0)),
            finding.get("rule_id", ""),
            finding.get("message", ""),
        ]
        key_string = "|".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def add_finding(
        self,
        finding: Dict[str, Any],
        reason: str = "baselined",
        created_by: Optional[str] = None,
    ) -> str:
        """Add finding to baseline.
        
        Args:
            finding: Finding to baseline
            reason: Reason for baselining
            created_by: User who created baseline
            
        Returns:
            Hash of the finding
        """
        finding_hash = self._finding_hash(finding)
        
        self.findings[finding_hash] = {
            "finding": finding,
            "reason": reason,
            "created_at": datetime.now().isoformat(),
            "created_by": created_by or "unknown",
        }
        
        return finding_hash
    
    def is_baselined(self, finding: Dict[str, Any]) -> bool:
        """Check if finding is in baseline.
        
        Args:
            finding: Finding to check
            
        Returns:
            True if finding is baselined
        """
        finding_hash = self._finding_hash(finding)
        return finding_hash in self.findings
    
    def get_baselined_hashes(self) -> Set[str]:
        """Get set of all baselined finding hashes.
        
        Returns:
            Set of finding hashes
        """
        return set(self.findings.keys())
    
    def remove_finding(self, finding: Dict[str, Any]) -> bool:
        """Remove finding from baseline.
        
        Args:
            finding: Finding to remove
            
        Returns:
            True if finding was removed
        """
        finding_hash = self._finding_hash(finding)
        
        if finding_hash in self.findings:
            del self.findings[finding_hash]
            return True
        
        return False
    
    def save(self) -> None:
        """Save baseline to file."""
        self.baseline_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "version": "1.0",
            "created_at": self.metadata.get("created_at", datetime.now().isoformat()),
            "updated_at": datetime.now().isoformat(),
            "finding_count": len(self.findings),
            "findings": self.findings,
        }
        
        with open(self.baseline_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    def load(self) -> None:
        """Load baseline from file."""
        with open(self.baseline_path, encoding="utf-8") as f:
            data = json.load(f)
        
        self.metadata = {
            "version": data.get("version", "1.0"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"),
            "finding_count": data.get("finding_count", 0),
        }
        
        self.findings = data.get("findings", {})
    
    def filter_findings(
        self,
        findings: List[Dict[str, Any]],
        respect_baseline: bool = True,
    ) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Filter findings against baseline.
        
        Args:
            findings: List of findings to filter
            respect_baseline: If True, suppress baselined findings
            
        Returns:
            Tuple of (new_findings, baselined_findings)
        """
        if not respect_baseline:
            return findings, []
        
        new_findings = []
        baselined_findings = []
        
        for finding in findings:
            if self.is_baselined(finding):
                baselined_findings.append(finding)
            else:
                new_findings.append(finding)
        
        return new_findings, baselined_findings
    
    def get_stats(self) -> Dict[str, Any]:
        """Get baseline statistics.
        
        Returns:
            Statistics dictionary
        """
        severity_counts = {}
        rule_counts = {}
        
        for entry in self.findings.values():
            finding = entry["finding"]
            
            # Count by severity
            severity = finding.get("severity", "UNKNOWN")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Count by rule
            rule_id = finding.get("rule_id", "UNKNOWN")
            rule_counts[rule_id] = rule_counts.get(rule_id, 0) + 1
        
        return {
            "total_findings": len(self.findings),
            "severity_counts": severity_counts,
            "rule_counts": rule_counts,
            "created_at": self.metadata.get("created_at"),
            "updated_at": self.metadata.get("updated_at"),
        }


def create_baseline(
    findings: List[Dict[str, Any]],
    baseline_path: Path,
    reason: str = "initial baseline",
    created_by: Optional[str] = None,
) -> Baseline:
    """Create new baseline from findings.
    
    Args:
        findings: List of findings to baseline
        baseline_path: Path to save baseline
        reason: Reason for creating baseline
        created_by: User creating baseline
        
    Returns:
        Baseline object
    """
    baseline = Baseline(baseline_path)
    
    for finding in findings:
        baseline.add_finding(finding, reason=reason, created_by=created_by)
    
    baseline.save()
    return baseline


def check_inline_suppression(
    file_path: Path,
    line: int,
    rule_id: str,
) -> Optional[str]:
    """Check if finding is suppressed by inline comment.
    
    Supports comments like:
        # speckit: ignore=B101 reason=demo code
        # speckit: ignore=B101,B102
        # speckit: ignore-line
    
    Args:
        file_path: Path to source file
        line: Line number (1-based)
        rule_id: Rule ID to check
        
    Returns:
        Suppression reason if found, None otherwise
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()
        
        # Check current line and previous line
        for check_line in [line - 1, line - 2]:
            if check_line < 0 or check_line >= len(lines):
                continue
            
            content = lines[check_line].strip()
            
            # Look for suppression comments
            if "speckit:" in content and "ignore" in content:
                # Check for ignore-line (suppresses all rules)
                if "ignore-line" in content:
                    return "inline suppression: ignore-line"
                
                # Check for specific rule suppression
                if f"ignore={rule_id}" in content or f"ignore={rule_id}," in content:
                    # Extract reason if present
                    if "reason=" in content:
                        reason_start = content.index("reason=") + 7
                        reason = content[reason_start:].strip()
                        return f"inline suppression: {reason}"
                    return "inline suppression"
        
        return None
        
    except Exception:
        return None


# Convenience functions for simple baseline usage
BASELINE_PATH = Path(".speckit/baseline.json")


def _fingerprint(item: Dict) -> str:
    """Generate stable fingerprint for a finding."""
    key = f"{item.get('file_path')}:{item.get('line')}:{item.get('rule_id')}:{item.get('message')}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def load_baseline(path: Path = BASELINE_PATH) -> Set[str]:
    """Load baseline fingerprints from JSON file."""
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text())
        return set(data.get("fingerprints", []))
    except Exception:
        return set()


def write_baseline(findings: List[Dict], path: Path = BASELINE_PATH) -> Path:
    """Write baseline fingerprints to JSON file."""
    fp = [_fingerprint(f) for f in findings]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"algo": "speckit-sha256-v1", "fingerprints": fp}, indent=2))
    return path


def filter_with_baseline(findings: List[Dict], baseline: Set[str]) -> List[Dict]:
    """Filter out findings that exist in baseline."""
    out = []
    for f in findings:
        if _fingerprint(f) not in baseline:
            out.append(f)
    return out
