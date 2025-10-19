## Contributing to Spec Kit

Hi there! We're thrilled that you'd like to contribute to Spec Kit. Contributions to this project are [released](https://help.github.com/articles/github-terms-of-service/#6-contributions-under-repository-license) to the public under the [project's open source license](LICENSE).

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Prerequisites for running and testing code

These are one time installations required to be able to test your changes locally as part of the pull request (PR) submission process.

1. Install [Python 3.11+](https://www.python.org/downloads/)
1. Install [uv](https://docs.astral.sh/uv/) for package management
1. Install [Git](https://git-scm.com/downloads)
1. Have an [AI coding agent available](README.md#-supported-ai-agents)

## Submitting a pull request

>[!NOTE]
>If your pull request introduces a large change that materially impacts the work of the CLI or the rest of the repository (e.g., you're introducing new templates, arguments, or otherwise major changes), make sure that it was **discussed and agreed upon** by the project maintainers. Pull requests with large changes that did not have a prior conversation and agreement will be closed.

1. Fork and clone the repository
1. Configure and install the dependencies: `uv sync`
1. Make sure the CLI works on your machine: `uv run specify --help`
1. Create a new branch: `git checkout -b my-branch-name`
1. Make your change, add tests, and make sure everything still works
1. Test the CLI functionality with a sample project if relevant
1. Push to your fork and submit a pull request
1. Wait for your pull request to be reviewed and merged.

Here are a few things you can do that will increase the likelihood of your pull request being accepted:

- Follow the project's coding conventions.
- Write tests for new functionality.
- Update documentation (`README.md`, `spec-driven.md`) if your changes affect user-facing features.
- Keep your change as focused as possible. If there are multiple changes you would like to make that are not dependent upon each other, consider submitting them as separate pull requests.
- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
- Test your changes with the Spec-Driven Development workflow to ensure compatibility.

## Development workflow

When working on spec-kit:

1. **Code Quality**: All code must pass pre-commit hooks before committing
   - Run `pre-commit install` to set up automatic checks
   - Hooks run automatically on `git commit`
   - Or manually: `pre-commit run --all-files`

2. **Type Safety**: All Python code must have type annotations
   - Use `mypy` for type checking (included in pre-commit hooks)
   - Follow existing patterns for type hints
   - Required: 100% type coverage on new code

3. **Exception Handling**: Use specific exception types, not broad `Exception`
   - ✅ Good: `except (OSError, IOError, PermissionError):`
   - ❌ Bad: `except Exception:`
   - Only use `Exception` for top-level handlers
   - Add comments explaining expected error conditions

4. **Logging**: Use structured logging for debugging and monitoring

   ```python
   from specify_cli.logging_config import get_logger
   logger = get_logger(__name__)

   logger.debug("Detailed debugging information")
   logger.info("High-level operation flow")
   logger.warning("Recoverable issues")
   logger.error("Error conditions")
   ```

5. **Version Management**: Use the version sync script for version updates

   ```bash
   # Check version consistency
   python scripts/sync_version.py --check

   # Bump patch version (0.1.0 → 0.1.1)
   python scripts/sync_version.py --bump patch

   # Set specific version
   python scripts/sync_version.py --set 1.0.0
   ```

6. **Testing**: Test changes with the `specify` CLI commands
   - `/speckit.specify`, `/speckit.plan`, `/speckit.tasks` in your coding agent
   - Verify templates work correctly in `templates/` directory
   - Test script functionality in the `scripts/` directory
   - Ensure memory files (`memory/constitution.md`) are updated if needed

7. **Documentation**: Update docs when making user-facing changes
   - `README.md` for feature changes
   - `CHANGELOG.md` for all changes (or use version script)
   - Docstrings for new functions/classes

## Code quality standards

### Pre-commit Hooks

This project uses pre-commit hooks to maintain code quality:

```bash
# Install hooks (one-time setup)
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Run on staged files
git commit  # Hooks run automatically
```

Our hooks include:

- **ruff**: Fast Python linter (replaces flake8, isort, etc.)
- **ruff-format**: Fast Python formatter (replaces black)
- **mypy**: Static type checker
- **fix end of files**: Ensures files end with newline
- **trim trailing whitespace**: Removes trailing spaces
- **check yaml**: Validates YAML syntax
- **check toml**: Validates TOML syntax
- **check for merge conflicts**: Prevents accidental conflict markers

### Type Annotations

All Python code must have type annotations:

```python
# Good: Function with type hints
def process_file(path: Path, verbose: bool = False) -> Optional[str]:
    """Process a file and return its content."""
    if not path.exists():
        return None
    return path.read_text()

# Bad: No type hints
def process_file(path, verbose=False):
    if not path.exists():
        return None
    return path.read_text()
```

Type annotation guidelines:

- Use `from __future__ import annotations` for forward references
- Use `Optional[T]` for values that can be `None`
- Use `List[T]`, `Dict[K, V]`, `Set[T]` for collections
- Use `Path` from `pathlib` instead of `str` for file paths
- Use `TYPE_CHECKING` block for import cycles

### Exception Handling Patterns

Use specific exception types to make error handling clear:

```python
# File I/O operations
try:
    content = path.read_text()
except (OSError, IOError, UnicodeDecodeError) as e:
    # File read error or encoding issue
    logger.error(f"Failed to read {path}: {e}")
    return None

# Subprocess operations
try:
    result = subprocess.run(cmd, check=True, capture_output=True)
except (OSError, subprocess.SubprocessError) as e:
    # Command not found or execution failed
    logger.error(f"Command failed: {e}")
    raise

# HTTP requests
try:
    response = httpx.get(url)
    response.raise_for_status()
except (httpx.HTTPError, httpx.RequestError) as e:
    # HTTP error or network issue
    logger.error(f"Request failed: {e}")
    raise

# Top-level handlers (appropriate use of Exception)
try:
    # Main application logic
    init_project(args)
except Exception as e:
    # Catch-all for unexpected errors at top level
    logger.critical(f"Unexpected error: {e}")
    console.print(Panel(str(e), title="Error", border_style="red"))
    raise typer.Exit(1)
```

### Logging Guidelines

Use structured logging throughout the codebase:

```python
from specify_cli.logging_config import get_logger

logger = get_logger(__name__)

# Debug: Detailed diagnostic information
logger.debug(f"Processing file: {file_path}")
logger.debug(f"Git repo check for {path}: {is_repo}")

# Info: High-level operation flow
logger.info(f"Initializing project: {project_path}")
logger.info(f"Configuration: AI={ai}, script_type={script}")

# Warning: Recoverable issues
logger.warning("No manifest found, scanning environment")
logger.warning("Git not available, skipping repository init")

# Error: Error conditions
logger.error(f"Directory already exists: {path}")
logger.error(f"Failed to download template: {e}")

# Critical: System-level failures (rare)
logger.critical("Unable to initialize logging system")
```

Logging levels:

- **DEBUG**: Detailed diagnostic info (file paths, git operations, config values)
- **INFO**: High-level operation flow (project init, download progress)
- **WARNING**: Recoverable issues (missing files, fallback behavior)
- **ERROR**: Error conditions (failures that stop the operation)
- **CRITICAL**: System-level failures (very rare)

Enable verbose logging:

```bash
# INFO level logging
specify --verbose init myproject

# DEBUG level logging
specify --debug init myproject
```

## Testing and submission workflow

## AI contributions in Spec Kit

> [!IMPORTANT]
>
> If you are using **any kind of AI assistance** to contribute to Spec Kit,
> it must be disclosed in the pull request or issue.

We welcome and encourage the use of AI tools to help improve Spec Kit! Many valuable contributions have been enhanced with AI assistance for code generation, issue detection, and feature definition.

That being said, if you are using any kind of AI assistance (e.g., agents, ChatGPT) while contributing to Spec Kit,
**this must be disclosed in the pull request or issue**, along with the extent to which AI assistance was used (e.g., documentation comments vs. code generation).

If your PR responses or comments are being generated by an AI, disclose that as well.

As an exception, trivial spacing or typo fixes don't need to be disclosed, so long as the changes are limited to small parts of the code or short phrases.

An example disclosure:

> This PR was written primarily by GitHub Copilot.

Or a more detailed disclosure:

> I consulted ChatGPT to understand the codebase but the solution
> was fully authored manually by myself.

Failure to disclose this is first and foremost rude to the human operators on the other end of the pull request, but it also makes it difficult to
determine how much scrutiny to apply to the contribution.

In a perfect world, AI assistance would produce equal or higher quality work than any human. That isn't the world we live in today, and in most cases
where human supervision or expertise is not in the loop, it's generating code that cannot be reasonably maintained or evolved.

### What we're looking for

When submitting AI-assisted contributions, please ensure they include:

- **Clear disclosure of AI use** - You are transparent about AI use and degree to which you're using it for the contribution
- **Human understanding and testing** - You've personally tested the changes and understand what they do
- **Clear rationale** - You can explain why the change is needed and how it fits within Spec Kit's goals
- **Concrete evidence** - Include test cases, scenarios, or examples that demonstrate the improvement
- **Your own analysis** - Share your thoughts on the end-to-end developer experience

### What we'll close

We reserve the right to close contributions that appear to be:

- Untested changes submitted without verification
- Generic suggestions that don't address specific Spec Kit needs
- Bulk submissions that show no human review or understanding

### Guidelines for success

The key is demonstrating that you understand and have validated your proposed changes. If a maintainer can easily tell that a contribution was generated entirely by AI without human input or testing, it likely needs more work before submission.

Contributors who consistently submit low-effort AI-generated changes may be restricted from further contributions at the maintainers' discretion.

Please be respectful to maintainers and disclose AI assistance.

## Resources

- [Spec-Driven Development Methodology](./spec-driven.md)
- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [Using Pull Requests](https://help.github.com/articles/about-pull-requests/)
- [GitHub Help](https://help.github.com)
