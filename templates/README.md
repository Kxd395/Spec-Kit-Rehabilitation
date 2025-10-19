# Templates

Command templates and configuration examples for Spec-Kit.

## Configuration Templates

### .speckit.toml.example

Example configuration file showing all available options. Copy to `.speckit.toml` in your repository root and customize.

```bash
cp templates/.speckit.toml.example .speckit.toml
```

## AI Agent Templates

Templates for AI-assisted development workflows:

- `agent-file-template.md` - Template for agent instruction files
- `checklist-template.md` - Feature checklist template
- `plan-template.md` - Project planning template
- `spec-template.md` - Specification template
- `tasks-template.md` - Task breakdown template

## Command Templates (`commands/`)

Templates for Spec-Kit commands used in AI agent workflows:

- `analyze.md` - Code analysis command
- `audit.md` - Security audit command
- `checklist.md` - Feature checklist command
- `clarify.md` - Requirement clarification command
- `compare.md` - Comparison command
- `constitution.md` - Project constitution command
- `implement.md` - Implementation command
- `migrate.md` - Migration command
- `plan.md` - Planning command
- `reverse-engineer.md` - Reverse engineering command
- `specify.md` - Specification command
- `tasks.md` - Task management command
- `upgrade.md` - Upgrade command

## VS Code Settings

### vscode-settings.json

Example VS Code workspace settings. Merge into `.vscode/settings.json`:

```bash
cat templates/vscode-settings.json >> .vscode/settings.json
```

## Usage

### For Configuration

```bash
# Copy and customize config template
cp templates/.speckit.toml.example .speckit.toml
edit .speckit.toml
```

### For AI Workflows

Templates in `commands/` are used by AI agents to understand available Spec-Kit commands and their expected outputs.

## Best Practices

- **Keep examples minimal** - Show common use cases only
- **Document all options** - Add comments explaining each setting
- **Production-safe defaults** - Examples should be safe to use as-is
- **Update regularly** - Keep templates in sync with code changes
