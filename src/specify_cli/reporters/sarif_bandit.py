"""SARIF reporter for GitHub Code Scanning integration."""

from __future__ import annotations
import json
import hashlib
from pathlib import Path
from typing import Dict, List


def _hash(s: str) -> str:
    """Generate short hash for fingerprinting.

    Args:
        s: String to hash

    Returns:
        First 16 chars of SHA256 hash
    """
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def bandit_findings_to_sarif(findings: List[Dict], repo_root: Path) -> Dict:
    """Convert Bandit findings to SARIF 2.1.0 format.

    Args:
        findings: List of finding dictionaries from BanditAnalyzer
        repo_root: Root directory of the repository

    Returns:
        SARIF document as dictionary
    """
    rules = {}
    results = []

    for f in findings:
        rule_id = f["rule_id"]
        if rule_id not in rules:
            rules[rule_id] = {
                "id": rule_id,
                "shortDescription": {"text": f"Bandit {rule_id}"},
                "defaultConfiguration": {"level": _map_level(f["severity"])},
                "help": {"text": f.get("message", ""), "markdown": f.get("message", "")},
                "properties": {"tags": ["security"], "precision": f.get("confidence", "MEDIUM")},
            }
            if f.get("cwe"):
                rules[rule_id]["properties"]["cwe"] = f"CWE-{f['cwe']}"

        phys_loc = {
            "artifactLocation": {
                "uri": str(Path(f["file_path"]).resolve().relative_to(repo_root.resolve()))
            },
            "region": {"startLine": int(f["line"])},
        }

        results.append(
            {
                "ruleId": rule_id,
                "level": _map_level(f["severity"]),
                "message": {"text": f["message"]},
                "locations": [{"physicalLocation": phys_loc}],
                "fingerprints": {
                    "primaryLocationLineHash": _hash(f"{f['file_path']}:{f['line']}:{rule_id}")
                },
            }
        )

    sarif = {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "SpecKit Bandit Bridge",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }
    return sarif


def _map_level(sev: str) -> str:
    """Map severity to SARIF level.

    Args:
        sev: Severity string (HIGH, MEDIUM, LOW)

    Returns:
        SARIF level (error, warning, note)
    """
    sev = sev.upper()
    if sev == "HIGH":
        return "error"
    if sev == "MEDIUM":
        return "warning"
    return "note"


def write_sarif(doc: Dict, out_path: Path) -> Path:
    """Write SARIF document to file.

    Args:
        doc: SARIF document dictionary
        out_path: Path to write to

    Returns:
        Path that was written
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc, indent=2))
    return out_path
