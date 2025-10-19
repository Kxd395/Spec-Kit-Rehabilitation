"""SARIF (Static Analysis Results Interchange Format) reporter.

Generates SARIF 2.1.0 compatible reports for GitHub Code Scanning integration.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


class SARIFReporter:
    """Generate SARIF format reports."""
    
    SARIF_VERSION = "2.1.0"
    SCHEMA_URL = "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json"
    
    def __init__(self, tool_name: str = "Spec-Kit", tool_version: str = "0.1.0"):
        """Initialize SARIF reporter.
        
        Args:
            tool_name: Name of the analysis tool
            tool_version: Version of the analysis tool
        """
        self.tool_name = tool_name
        self.tool_version = tool_version
        self.rules: Dict[str, Dict[str, Any]] = {}
        self.results: List[Dict[str, Any]] = []
    
    def add_finding(
        self,
        rule_id: str,
        message: str,
        file_path: str,
        line: int,
        column: int = 1,
        severity: str = "warning",
        rule_name: Optional[str] = None,
        rule_description: Optional[str] = None,
        help_uri: Optional[str] = None,
        cwe_ids: Optional[List[int]] = None,
        snippet: Optional[str] = None,
    ) -> None:
        """Add a finding to the SARIF report.
        
        Args:
            rule_id: Unique identifier for the rule
            message: Description of the finding
            file_path: Path to the file containing the issue
            line: Line number (1-based)
            column: Column number (1-based)
            severity: SARIF level (error, warning, note)
            rule_name: Human-readable rule name
            rule_description: Detailed rule description
            help_uri: URL to documentation
            cwe_ids: List of CWE identifiers
            snippet: Code snippet showing the issue
        """
        # Register rule if not already present
        if rule_id not in self.rules:
            self.rules[rule_id] = self._create_rule(
                rule_id=rule_id,
                name=rule_name or rule_id,
                description=rule_description or message,
                help_uri=help_uri,
                cwe_ids=cwe_ids,
            )
        
        # Create result
        result = {
            "ruleId": rule_id,
            "level": self._normalize_severity(severity),
            "message": {"text": message},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": str(Path(file_path)),
                            "uriBaseId": "%SRCROOT%",
                        },
                        "region": {
                            "startLine": line,
                            "startColumn": column,
                        },
                    }
                }
            ],
        }
        
        # Add code snippet if provided
        if snippet:
            result["locations"][0]["physicalLocation"]["region"]["snippet"] = {
                "text": snippet
            }
        
        self.results.append(result)
    
    def _create_rule(
        self,
        rule_id: str,
        name: str,
        description: str,
        help_uri: Optional[str] = None,
        cwe_ids: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """Create a SARIF rule definition.
        
        Args:
            rule_id: Unique identifier
            name: Short name
            description: Full description
            help_uri: Documentation URL
            cwe_ids: List of CWE identifiers
            
        Returns:
            SARIF rule object
        """
        rule = {
            "id": rule_id,
            "name": name,
            "shortDescription": {"text": name},
            "fullDescription": {"text": description},
        }
        
        if help_uri:
            rule["helpUri"] = help_uri
        
        # Add CWE mappings
        if cwe_ids:
            rule["properties"] = {
                "tags": [f"CWE-{cwe_id}" for cwe_id in cwe_ids],
                "security-severity": self._cwe_to_cvss_severity(cwe_ids[0]),
            }
        
        return rule
    
    def _normalize_severity(self, severity: str) -> str:
        """Convert severity to SARIF level.
        
        Args:
            severity: Input severity (LOW, MEDIUM, HIGH, CRITICAL, etc.)
            
        Returns:
            SARIF level (error, warning, note)
        """
        severity_upper = severity.upper()
        
        if severity_upper in ("CRITICAL", "HIGH"):
            return "error"
        elif severity_upper == "MEDIUM":
            return "warning"
        else:
            return "note"
    
    def _cwe_to_cvss_severity(self, cwe_id: int) -> str:
        """Map CWE to approximate CVSS severity score.
        
        This is a simplified mapping. Real CVSS requires context.
        
        Args:
            cwe_id: CWE identifier
            
        Returns:
            CVSS score as string
        """
        # High severity CWEs
        high_severity_cwes = {
            78, 79, 89, 94, 95, 119, 120, 190, 287, 306, 307, 311, 798, 915
        }
        
        if cwe_id in high_severity_cwes:
            return "8.0"  # High
        else:
            return "5.0"  # Medium
    
    def generate(self) -> Dict[str, Any]:
        """Generate complete SARIF document.
        
        Returns:
            SARIF JSON structure
        """
        return {
            "version": self.SARIF_VERSION,
            "$schema": self.SCHEMA_URL,
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": self.tool_name,
                            "version": self.tool_version,
                            "informationUri": "https://github.com/Kxd395/Spec-Kit-Rehabilitation",
                            "rules": list(self.rules.values()),
                        }
                    },
                    "results": self.results,
                    "columnKind": "utf16CodeUnits",
                    "properties": {
                        "analysisTime": datetime.now(timezone.utc).isoformat(),
                    },
                }
            ],
        }
    
    def save(self, output_path: Path) -> None:
        """Save SARIF report to file.
        
        Args:
            output_path: Path to save report
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.generate(), f, indent=2)
    
    def to_json(self) -> str:
        """Convert to JSON string.
        
        Returns:
            SARIF report as JSON string
        """
        return json.dumps(self.generate(), indent=2)


# Example usage for integration with existing analyzers
def findings_to_sarif(
    findings: List[Dict[str, Any]],
    output_path: Path,
    tool_name: str = "Spec-Kit",
    tool_version: str = "0.1.0",
) -> None:
    """Convert findings to SARIF format.
    
    Args:
        findings: List of finding dictionaries
        output_path: Path to save SARIF file
        tool_name: Name of the tool
        tool_version: Version of the tool
        
    Expected finding format:
        {
            "rule_id": "B101",
            "message": "Use of assert detected",
            "file": "src/example.py",
            "line": 42,
            "column": 5,
            "severity": "LOW",
            "cwe_ids": [703],
            "snippet": "assert user.is_admin",
        }
    """
    reporter = SARIFReporter(tool_name, tool_version)
    
    for finding in findings:
        reporter.add_finding(
            rule_id=finding.get("rule_id", "UNKNOWN"),
            message=finding.get("message", "No description"),
            file_path=finding.get("file", "unknown"),
            line=finding.get("line", 1),
            column=finding.get("column", 1),
            severity=finding.get("severity", "warning"),
            cwe_ids=finding.get("cwe_ids"),
            snippet=finding.get("snippet"),
        )
    
    reporter.save(output_path)
