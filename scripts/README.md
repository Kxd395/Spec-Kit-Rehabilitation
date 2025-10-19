# Scripts

Development automation scripts for Spec-Kit.

## Available Scripts

### Bash Scripts (`bash/`)

All Bash scripts are designed for macOS and Linux systems.

- **`common.sh`** - Shared functions and utilities
- **`check-prerequisites.sh`** - Validates required tools are installed
- **`create-new-feature.sh`** - Scaffolds new feature branch
- **`setup-plan.sh`** - Initializes project planning structure
- **`update-agent-context.sh`** - Updates AI agent context files

### PowerShell Scripts (`powershell/`)

All PowerShell scripts are designed for Windows systems.

- **`common.ps1`** - Shared functions and utilities
- **`check-prerequisites.ps1`** - Validates required tools are installed
- **`create-new-feature.ps1`** - Scaffolds new feature branch
- **`setup-plan.ps1`** - Initializes project planning structure
- **`update-agent-context.ps1`** - Updates AI agent context files

## Usage

### Bash (macOS/Linux)

```bash
cd scripts/bash
./check-prerequisites.sh
./create-new-feature.sh feature-name
```

### PowerShell (Windows)

```powershell
cd scripts\powershell
.\check-prerequisites.ps1
.\create-new-feature.ps1 feature-name
```

## Script Principles

- **Idempotent**: Safe to run multiple times
- **Portable**: Work across different environments
- **Validated**: Check prerequisites before execution
- **Logged**: Provide clear output about operations
- **Error-safe**: Exit cleanly on errors

## Adding New Scripts

When adding new automation:

1. Create both Bash and PowerShell versions for cross-platform support
2. Add shared logic to `common.sh` / `common.ps1`
3. Include clear help text and usage examples
4. Test on target platforms before committing
5. Document in this README

## Prerequisites

All scripts assume:
- Git is installed and configured
- Python 3.11+ is available
- Basic shell environment is set up

Run `check-prerequisites.sh` / `check-prerequisites.ps1` to verify your environment.
