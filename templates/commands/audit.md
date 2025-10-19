# /speckit.audit

## ⚠️ IMPORTANT DISCLAIMER

**This command provides AI-assisted guidance, NOT automated security scanning.**

- ❌ This is NOT a replacement for professional security audits
- ❌ This does NOT provide deterministic vulnerability detection
- ❌ Results depend entirely on AI interpretation and may miss critical issues
- ✅ Use this as an exploratory tool to identify areas for manual review
- ✅ Always follow up with proper security tools (Snyk, SonarQube, OWASP ZAP, etc.)
- ✅ Treat findings as suggestions requiring human verification

**For production security:** Use dedicated security scanning tools and professional auditors.

---

## Purpose

Perform AI-assisted security, quality, and architecture analysis on an existing project or generated specifications. This command guides the AI to help identify potential vulnerabilities, anti-patterns, technical debt, and areas for improvement.

## Prerequisites

- Project has been analyzed with `/speckit.reverse-engineer` OR
- Working in an existing codebase

## Audit Categories

### 1. Security Audit

**OWASP Top 10 Vulnerabilities:**

- Injection attacks (SQL, NoSQL, Command, LDAP)
- Broken authentication
- Sensitive data exposure
- XML External Entities (XXE)
- Broken access control
- Security misconfiguration
- Cross-Site Scripting (XSS)
- Insecure deserialization
- Using components with known vulnerabilities
- Insufficient logging & monitoring

**Additional Security Checks:**

- Hard-coded secrets and credentials
- Weak cryptographic algorithms
- Missing HTTPS/TLS enforcement
- CORS misconfiguration
- Unsafe file uploads
- Session management issues
- CSRF protection
- Rate limiting and DoS protection

### 2. Dependency Audit

**Check all dependencies for:**

- Known CVEs and security vulnerabilities
- Outdated packages (versions more than 2 years old)
- Deprecated packages (no longer maintained)
- License compatibility issues
- Excessive dependencies (bloat)
- Transitive dependency risks

**Tools to leverage:**

- npm audit, yarn audit (JavaScript)
- pip-audit, safety (Python)
- cargo audit (Rust)
- bundler-audit (Ruby)

### 3. Code Quality Audit

**Analyze:**

- Code complexity (cyclomatic complexity)
- Code duplication
- Long functions/methods (>50 lines)
- Deep nesting (>4 levels)
- Magic numbers and hardcoded values
- Inconsistent naming conventions
- Missing error handling
- Poor separation of concerns

### 4. Architecture Audit

**Evaluate:**

- Tight coupling between components
- Missing abstraction layers
- Monolithic vs. modular design
- Circular dependencies
- Missing design patterns where appropriate
- Scalability concerns
- Single points of failure
- Missing caching strategies

### 5. Performance Audit

**Identify:**

- N+1 query problems
- Missing database indexes
- Inefficient algorithms
- Memory leaks
- Missing pagination
- Large payload sizes
- Unoptimized images/assets
- Missing CDN usage

### 6. Accessibility Audit (for web projects)

**Check:**

- WCAG 2.1 compliance (Level AA minimum)
- Missing alt text for images
- Poor keyboard navigation
- Missing ARIA labels
- Insufficient color contrast
- Missing focus indicators
- Screen reader compatibility

### 7. Compliance Audit

**Verify compliance with:**

- GDPR (data privacy, EU)
- CCPA (California privacy)
- HIPAA (healthcare data, US)
- PCI-DSS (payment card data)
- SOC 2 (security controls)
- Industry-specific regulations

### 8. Testing Audit

**Evaluate:**

- Test coverage percentage
- Missing critical path tests
- Missing edge case tests
- No integration tests
- No end-to-end tests
- Missing performance tests
- Brittle/flaky tests

## Output Format

Generate `audit-report.md` with:

```markdown
# Security & Quality Audit Report

**Project:** [Project Name]
**Audit Date:** [Date]
**Auditor:** AI Assistant

## Executive Summary

[High-level overview of findings]

**Risk Level:** 🔴 High / 🟡 Medium / 🟢 Low

**Critical Issues:** X
**High Priority:** Y
**Medium Priority:** Z
**Low Priority:** W

## Critical Findings

### [Issue #1: SQL Injection Vulnerability]

**Severity:** 🔴 Critical
**Category:** Security - Injection
**Location:** `src/auth/login.js:45`
**CVSS Score:** 9.1

**Description:**
User input is directly concatenated into SQL query without sanitization.

**Code:**
\`\`\`javascript
const query = `SELECT * FROM users WHERE username='${username}'`;
\`\`\`

**Impact:**
Attackers can execute arbitrary SQL commands, potentially accessing or deleting all database data.

**Recommendation:**
Use parameterized queries or ORM with proper input validation.

**Fixed Code:**
\`\`\`javascript
const query = 'SELECT * FROM users WHERE username = ?';
db.query(query, [username]);
\`\`\`

## High Priority Findings

[Continue with all findings...]

## Dependency Vulnerabilities

| Package | Version | CVE | Severity | Fix Available |
|---------|---------|-----|----------|---------------|
| lodash | 4.17.15 | CVE-2020-8203 | High | 4.17.21 |
| ...     | ...     | ...          | ...      | ...           |

## Architecture Recommendations

[Architecture improvements...]

## Performance Bottlenecks

[Performance issues...]

## Compliance Gaps

[Compliance issues...]

## Remediation Roadmap

### Immediate (Do Now)
1. Fix critical security vulnerabilities
2. Update vulnerable dependencies
3. ...

### Short-term (This Sprint)
1. Add input validation
2. Implement rate limiting
3. ...

### Medium-term (This Quarter)
1. Refactor tightly coupled modules
2. Add comprehensive test coverage
3. ...

### Long-term (This Year)
1. Modernize architecture
2. Implement monitoring
3. ...
```

## Instructions for AI Agent

1. **Scan the entire codebase systematically:**
   - Use grep_search to find security anti-patterns
   - Read all configuration files
   - Check dependency manifests

2. **Security Analysis:**
   - Search for common vulnerability patterns:
     - `eval(`, `exec(`, `system(`
     - String concatenation in SQL queries
     - Missing input validation
     - Hard-coded secrets/passwords
   - Check authentication and authorization flows
   - Review session management

3. **Dependency Analysis:**
   - Parse package.json, requirements.txt, Cargo.toml, etc.
   - Check each dependency against known vulnerability databases
   - Identify outdated packages

4. **Code Quality:**
   - Identify overly complex functions
   - Find code duplication
   - Check for error handling
   - Review naming conventions

5. **Architecture Review:**
   - Map component dependencies
   - Identify coupling issues
   - Check for proper separation of concerns
   - Evaluate scalability

6. **Prioritization:**
   - Rank issues by severity and impact
   - Consider exploitability and business impact
   - Create actionable remediation plan

7. **Documentation:**
   - Provide specific file locations and line numbers
   - Include code snippets showing the issue
   - Suggest concrete fixes with code examples
   - Estimate effort for each remediation

## Severity Classification

- **🔴 Critical:** Immediate security risk, data breach potential, system compromise
- **🟠 High:** Significant security/quality issue, should be fixed soon
- **🟡 Medium:** Moderate issue, fix in near term
- **🟢 Low:** Minor improvement, nice to have

## Example Usage

```bash
# Full audit
/speckit.audit

# Security-focused audit only
/speckit.audit --focus security

# Dependency audit only
/speckit.audit --focus dependencies
```

## Follow-up Commands

After auditing:

- `/speckit.upgrade` - Generate improved specs addressing issues
- `/speckit.plan` - Create remediation implementation plan
- `/speckit.implement` - Fix identified issues
