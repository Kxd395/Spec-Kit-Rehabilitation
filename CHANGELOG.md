# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to the Specify CLI and templates are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Development Workflow Constitution**: `DEVELOPMENT_WORKFLOW.md` with mandatory pre-push checklist
  - Repository hygiene rules (clean root directory before push)
  - Documentation update requirements (CHANGELOG.md, README.md, version bumps)
  - Testing standards (50%+ coverage, quality over quantity)
  - Version bump rules (especially for `__init__.py` changes)
  - Approved root files list and Phase/PR workflow process

- **AI Agent Instructions**: `.github/AI_AGENT_INSTRUCTIONS.md` for AI coding assistants
  - Mandatory pre-push checklist with command sequences
  - Self-check questions before pushing
  - References to DEVELOPMENT_WORKFLOW.md for complete rules
  - Common mistakes to avoid

- **Development Configuration**: `[development]` section in `.speckit.toml`
  - `enforce_pre_push_checklist = true` - Workflow enforcement
  - `require_changelog_updates = true` - Mandatory CHANGELOG entries
  - `require_version_bump_on_init = true` - Version consistency
  - `approved_root_files` - List of allowed root directory files
  - `forbidden_root_patterns` - Patterns that should never be in root
  - Testing requirements: min_coverage, min_new_code_coverage

### Changed

- **Constitution Template**: `memory/constitution.md` now references DEVELOPMENT_WORKFLOW.md
  - Clarifies that template is for projects using Spec-Kit
  - Points to DEVELOPMENT_WORKFLOW.md for Spec-Kit's own rules

- **README.md**: Added Contributing section with links to development documentation
  - References DEVELOPMENT_WORKFLOW.md for contributors
  - Special section for AI agents with mandatory pre-push checklist
  - Links to AI_AGENT_INSTRUCTIONS.md and .speckit.toml configuration

## [0.1.0a3] - 2025-10-18

### Added

- **Security Scanning**: Complete Phase 3 implementation with Bandit and Safety analyzers
  - `specify audit` command with SARIF, HTML, and JSON output formats
  - SARIF 2.1.0 output compatible with GitHub Code Scanning
  - HTML reports with XSS-safe escaping using `html.escape()` on all dynamic fields
  - Baseline filtering system to track only new findings
  - Exclude pattern support (fnmatch globs) integrated with Bandit analyzer
  - Smart manifest detection for Safety (6 formats supported)
  - Exit code gating by severity threshold (HIGH, MEDIUM, LOW)
  - `--strict` flag to fail when requested analyzers are unavailable
  - Configuration system with TOML + ENV + CLI precedence
  - SHA256 fingerprints for finding deduplication
  - CWE mapping in SARIF rules
  
- **Documentation**: Comprehensive documentation for Phase 3 features
  - `docs/security-scanning.md` - Security scanning guide
  - `docs/architecture.md` - System architecture overview
  - `templates/.speckit.toml.example` - Configuration template
  - README files for all subdirectories (commands, tests, scripts, templates)
  - Security scanning section in main README with CI integration examples

- **Testing**: Security and configuration test suite
  - `test_html_escapes.py` - XSS prevention validation
  - `test_safety_error_handling.py` - Error case handling
  - `test_excludes_applied.py` - Exclude pattern verification
  - `test_config_loading.py` - Configuration precedence tests
  - `test_sarif_generation.py` - SARIF structure validation

- **CI/CD**: GitHub Actions workflows for automated security scanning
  - `.github/workflows/specify-audit.yml` - SARIF upload to GitHub Code Scanning
  - `.github/workflows/coverage.yml` - 70% coverage threshold enforcement

### Changed

- **SARIF Reporter**: Now points to real dependency manifest files instead of defaulting to "."
- **Safety Analyzer**: Explicit error handling with FileNotFoundError when CLI is missing
- **Config System**: Structured as AnalysisCfg, OutputCfg, AnalyzersCfg with exclude_paths at top level
- **Audit Command**: Integrated strict mode and config-driven exclude patterns

### Fixed

- **XSS Prevention**: All dynamic fields in HTML reporter now escaped with `html.escape()`
- **Bandit Integration**: Exclude glob patterns now properly honored
- **Error Handling**: Safety analyzer raises explicit errors instead of silent failures

## [0.0.20] - 2025-10-14

### Added

- **Intelligent Branch Naming**: `create-new-feature` scripts now support `--short-name` parameter for custom branch names
  - When `--short-name` provided: Uses the custom name directly (cleaned and formatted)
  - When omitted: Automatically generates meaningful names using stop word filtering and length-based filtering
  - Filters out common stop words (I, want, to, the, for, etc.)
  - Removes words shorter than 3 characters (unless they're uppercase acronyms)
  - Takes 3-4 most meaningful words from the description
  - **Enforces GitHub's 244-byte branch name limit** with automatic truncation and warnings
  - Examples:
    - "I want to create user authentication" → `001-create-user-authentication`
    - "Implement OAuth2 integration for API" → `001-implement-oauth2-integration-api`
    - "Fix payment processing bug" → `001-fix-payment-processing`
    - Very long descriptions are automatically truncated at word boundaries to stay within limits
  - Designed for AI agents to provide semantic short names while maintaining standalone usability

### Changed

- Enhanced help documentation for `create-new-feature.sh` and `create-new-feature.ps1` scripts with examples
- Branch names now validated against GitHub's 244-byte limit with automatic truncation if needed

## [0.0.19] - 2025-10-10

### Added

- Support for CodeBuddy (thank you to [@lispking](https://github.com/lispking) for the contribution).
- You can now see Git-sourced errors in the Specify CLI.

### Changed

- Fixed the path to the constitution in `plan.md` (thank you to [@lyzno1](https://github.com/lyzno1) for spotting).
- Fixed backslash escapes in generated TOML files for Gemini (thank you to [@hsin19](https://github.com/hsin19) for the contribution).
- Implementation command now ensures that the correct ignore files are added (thank you to [@sigent-amazon](https://github.com/sigent-amazon) for the contribution).

## [0.0.18] - 2025-10-06

### Added

- Support for using `.` as a shorthand for current directory in `specify init .` command, equivalent to `--here` flag but more intuitive for users.
- Use the `/speckit.` command prefix to easily discover Spec Kit-related commands.
- Refactor the prompts and templates to simplify their capabilities and how they are tracked. No more polluting things with tests when they are not needed.
- Ensure that tasks are created per user story (simplifies testing and validation).
- Add support for Visual Studio Code prompt shortcuts and automatic script execution.

### Changed

- All command files now prefixed with `speckit.` (e.g., `speckit.specify.md`, `speckit.plan.md`) for better discoverability and differentiation in IDE/CLI command palettes and file explorers

## [0.0.17] - 2025-09-22

### Added

- New `/clarify` command template to surface up to 5 targeted clarification questions for an existing spec and persist answers into a Clarifications section in the spec.
- New `/analyze` command template providing a non-destructive cross-artifact discrepancy and alignment report (spec, clarifications, plan, tasks, constitution) inserted after `/tasks` and before `/implement`.
	- Note: Constitution rules are explicitly treated as non-negotiable; any conflict is a CRITICAL finding requiring artifact remediation, not weakening of principles.

## [0.0.16] - 2025-09-22

### Added

- `--force` flag for `init` command to bypass confirmation when using `--here` in a non-empty directory and proceed with merging/overwriting files.

## [0.0.15] - 2025-09-21

### Added

- Support for Roo Code.

## [0.0.14] - 2025-09-21

### Changed

- Error messages are now shown consistently.

## [0.0.13] - 2025-09-21

### Added

- Support for Kilo Code. Thank you [@shahrukhkhan489](https://github.com/shahrukhkhan489) with [#394](https://github.com/github/spec-kit/pull/394).
- Support for Auggie CLI. Thank you [@hungthai1401](https://github.com/hungthai1401) with [#137](https://github.com/github/spec-kit/pull/137).
- Agent folder security notice displayed after project provisioning completion, warning users that some agents may store credentials or auth tokens in their agent folders and recommending adding relevant folders to `.gitignore` to prevent accidental credential leakage.

### Changed

- Warning displayed to ensure that folks are aware that they might need to add their agent folder to `.gitignore`.
- Cleaned up the `check` command output.

## [0.0.12] - 2025-09-21

### Changed

- Added additional context for OpenAI Codex users - they need to set an additional environment variable, as described in [#417](https://github.com/github/spec-kit/issues/417).

## [0.0.11] - 2025-09-20

### Added

- Codex CLI support (thank you [@honjo-hiroaki-gtt](https://github.com/honjo-hiroaki-gtt) for the contribution in [#14](https://github.com/github/spec-kit/pull/14))
- Codex-aware context update tooling (Bash and PowerShell) so feature plans refresh `AGENTS.md` alongside existing assistants without manual edits.

## [0.0.10] - 2025-09-20

### Fixed

- Addressed [#378](https://github.com/github/spec-kit/issues/378) where a GitHub token may be attached to the request when it was empty.

## [0.0.9] - 2025-09-19

### Changed

- Improved agent selector UI with cyan highlighting for agent keys and gray parentheses for full names

## [0.0.8] - 2025-09-19

### Added

- Windsurf IDE support as additional AI assistant option (thank you [@raedkit](https://github.com/raedkit) for the work in [#151](https://github.com/github/spec-kit/pull/151))
- GitHub token support for API requests to handle corporate environments and rate limiting (contributed by [@zryfish](https://github.com/@zryfish) in [#243](https://github.com/github/spec-kit/pull/243))

### Changed

- Updated README with Windsurf examples and GitHub token usage
- Enhanced release workflow to include Windsurf templates

## [0.0.7] - 2025-09-18

### Changed

- Updated command instructions in the CLI.
- Cleaned up the code to not render agent-specific information when it's generic.


## [0.0.6] - 2025-09-17

### Added

- opencode support as additional AI assistant option

## [0.0.5] - 2025-09-17

### Added

- Qwen Code support as additional AI assistant option

## [0.0.4] - 2025-09-14

### Added

- SOCKS proxy support for corporate environments via `httpx[socks]` dependency

### Fixed

N/A

### Changed

N/A

