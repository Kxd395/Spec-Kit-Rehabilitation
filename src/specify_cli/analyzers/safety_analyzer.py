from __future__ import annotations
import json
import shlex
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from specify_cli.logging import get_logger

log = get_logger(__name__)


@dataclass
class SafetyFinding:
    package: str
    installed_version: str
    advisory_id: str
    cve: Optional[str]
    severity: str
    vulnerable_spec: str
    fix_version: Optional[str]


class SafetyAnalyzer:
    """
    Runs Safety via CLI. Prefers a dependency manifest when possible.
    Supported order:
      1) requirements.txt
      2) requirements-dev.txt
      3) requirements.in
      4) poetry.lock
      5) Pipfile.lock
      6) pyproject.toml
      else: scan current environment
    """

    def __init__(self, project_root: Path):
        self.root = Path(project_root)

    def _which_safety(self) -> str:
        exe = shutil.which("safety")
        if not exe:
            msg = "safety CLI not found. Install extras: pip install -e '.[analysis]'"
            log.error(msg)
            raise FileNotFoundError(msg)
        return exe

    def _choose_manifest(self) -> Tuple[str, Optional[Path]]:
        cands = [
            "requirements.txt",
            "requirements-dev.txt",
            "requirements.in",
            "poetry.lock",
            "Pipfile.lock",
            "pyproject.toml",
        ]
        for name in cands:
            p = self.root / name
            if p.exists():
                return ("file", p)
        return ("env", None)

    def _run_json(self, cmd: str) -> Dict[str, Any]:
        try:
            proc = subprocess.run(
                shlex.split(cmd),
                cwd=str(self.root),
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            log.error("safety command not found")
            raise
        except OSError as e:
            log.error(f"OS error invoking safety: {e}")
            raise

        if proc.returncode not in (0, 1):  # 1 can mean vulnerabilities found
            log.error(f"safety failed rc={proc.returncode}: {proc.stderr.strip()}")
            raise subprocess.CalledProcessError(proc.returncode, cmd, proc.stdout, proc.stderr)

        out = proc.stdout.strip()
        try:
            return json.loads(out or "{}")
        except json.JSONDecodeError:
            log.error("Failed to parse safety JSON output")
            raise

    def run(self) -> List[SafetyFinding]:
        self._which_safety()
        mode, manifest = self._choose_manifest()

        data: Optional[Dict[str, Any]] = None
        if mode == "file" and manifest:
            log.info(f"Running safety against {manifest.name}")
            # New CLI
            try:
                data = self._run_json(f"safety scan --json --file {shlex.quote(str(manifest))}")
            except (subprocess.SubprocessError, json.JSONDecodeError, RuntimeError):
                # safety scan failed - try legacy command
                log.warning("safety scan failed. Trying legacy 'safety check --json --file'.")
                data = self._run_json(f"safety check --json --file {shlex.quote(str(manifest))}")
        else:
            log.warning("No supported manifest found. Scanning current Python environment.")
            try:
                data = self._run_json("safety scan --json")
            except (subprocess.SubprocessError, json.JSONDecodeError, RuntimeError):
                # safety scan failed - try legacy command
                log.warning("safety scan failed. Trying legacy 'safety check --json'.")
                data = self._run_json("safety check --json")

        findings: List[SafetyFinding] = []
        vulns = []
        if isinstance(data, dict) and "vulnerabilities" in data:
            vulns = data.get("vulnerabilities", [])
        elif isinstance(data, list):
            vulns = data

        for v in vulns:
            pkg = v.get("package_name") or v.get("package") or v.get("name") or ""
            inst_ver = v.get("installed_version") or v.get("version") or ""
            adv_id = v.get("vulnerability_id") or v.get("id") or v.get("advisory_id") or ""
            severity = (v.get("severity") or "").upper() or "UNKNOWN"
            spec = v.get("affected_versions") or v.get("spec") or ""
            fix = None
            if isinstance(v.get("fix_versions"), list) and v["fix_versions"]:
                fix = v["fix_versions"][0]
            elif v.get("fixed_version"):
                fix = v.get("fixed_version")
            cve = v.get("cve") or v.get("CVE") or None

            findings.append(
                SafetyFinding(
                    package=pkg,
                    installed_version=inst_ver,
                    advisory_id=str(adv_id),
                    cve=cve,
                    severity=severity,
                    vulnerable_spec=str(spec),
                    fix_version=fix,
                )
            )
        return findings

    @staticmethod
    def to_dicts(items: List[SafetyFinding]) -> List[Dict[str, Any]]:
        return [asdict(i) for i in items]
