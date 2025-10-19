"""Combined SARIF reporter for Bandit + Safety findings."""

from __future__ import annotations
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional


def _level(sev: str) -> str:
    s = (sev or "").upper()
    if s in ("CRITICAL", "HIGH"):
        return "error"
    if s == "MEDIUM":
        return "warning"
    return "note"


def _fp(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]


def _best_dep_artifact(repo_root: Path, hint: Optional[str]) -> Optional[str]:
    if hint:
        p = repo_root / hint
        if p.exists():
            return str(hint)
    for name in (
        "requirements.txt",
        "requirements-dev.txt",
        "poetry.lock",
        "Pipfile.lock",
        "pyproject.toml",
    ):
        if (repo_root / name).exists():
            return name
    return None


def combine_to_sarif(
    bandit_findings: List[dict],
    safety_findings: List[dict],
    repo_root: Path,
    dep_artifact_hint: Optional[str] = None,
) -> Dict:
    rules = {}
    results = []
    root = repo_root.resolve()

    # Bandit
    for f in bandit_findings:
        rid = f["rule_id"]
        if rid not in rules:
            rule = {
                "id": rid,
                "shortDescription": {"text": f"Bandit {rid}"},
                "defaultConfiguration": {"level": _level(f.get("severity", ""))},
                "properties": {
                    "tags": ["security", "code"],
                    "precision": f.get("confidence", "MEDIUM"),
                },
            }
            if f.get("cwe"):
                rule["properties"]["cwe"] = f"CWE-{f['cwe']}"
            rules[rid] = rule
        rel = str(Path(f["file_path"]).resolve().relative_to(root))
        results.append(
            {
                "ruleId": rid,
                "level": _level(f.get("severity", "")),
                "message": {"text": f.get("message", "")},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": rel},
                            "region": {"startLine": int(f.get("line", 1))},
                        }
                    }
                ],
                "fingerprints": {"primaryLocationLineHash": _fp(f"{rel}:{f.get('line',1)}:{rid}")},
            }
        )

    # Safety
    dep_art = _best_dep_artifact(repo_root, dep_artifact_hint)
    for v in safety_findings:
        rid = f"SAFETY-{v.get('advisory_id','UNKNOWN')}"
        if rid not in rules:
            rule = {
                "id": rid,
                "shortDescription": {
                    "text": f"Dependency vulnerability {v.get('advisory_id','') or v.get('cve','')}"
                },
                "defaultConfiguration": {"level": _level(v.get("severity", ""))},
                "properties": {"tags": ["security", "dependency"]},
            }
            if v.get("cve"):
                rule["properties"]["cve"] = v["cve"]
            rules[rid] = rule

        msg = f"{v.get('package','')} {v.get('installed_version','')} vulnerable. Spec: {v.get('vulnerable_spec','')}. Fix: {v.get('fix_version','') or 'N/A'}"
        fp_src = f"{v.get('package','')}:{v.get('installed_version','')}:{v.get('advisory_id','')}"
        locs = []
        if dep_art:
            locs = [{"physicalLocation": {"artifactLocation": {"uri": dep_art}}}]
        results.append(
            {
                "ruleId": rid,
                "level": _level(v.get("severity", "")),
                "message": {"text": msg},
                "locations": locs,
                "fingerprints": {"primaryLocationLineHash": _fp(fp_src)},
            }
        )

    return {
        "version": "2.1.0",
        "$schema": "https://schemastore.azurewebsites.net/schemas/json/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {"driver": {"name": "SpecKit Combined", "rules": list(rules.values())}},
                "results": results,
            }
        ],
    }


def write_sarif(doc: Dict, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(doc, indent=2))
    return out_path
