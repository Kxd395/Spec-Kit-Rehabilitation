# /speckit.reverse-engineer

## ⚠️ IMPORTANT DISCLAIMER

**This command uses AI assistance to analyze code, NOT automated reverse-engineering tools.**

- ❌ This is NOT static analysis with AST parsing or formal code analysis
- ❌ Accuracy depends on AI's ability to understand your specific codebase
- ❌ May miss important architectural details or domain logic
- ✅ Good for generating initial documentation from undocumented code
- ✅ Helpful for understanding unfamiliar codebases
- ✅ Creates a starting point that requires human review and refinement

**For comprehensive reverse-engineering:** Consider tools like Understand, Doxygen, or language-specific analyzers.

---

## Purpose

Use AI assistance to generate comprehensive Spec-Kit specifications FROM an existing codebase. This command guides the AI to analyze the current project and creates documentation that can be used for Spec-Driven Development.

## Prerequisites
- Run this command in the root directory of the existing project you want to analyze
- Ensure you have access to read the entire codebase

## Process

### 1. Project Discovery
Analyze the existing project to understand:
- **Project Structure**: Identify all source files, directories, and organization
- **Technology Stack**: Detect frameworks, languages, build tools, and dependencies
- **Entry Points**: Find main files, startup scripts, and initialization code
- **Configuration**: Review package.json, requirements.txt, Cargo.toml, etc.

### 2. Feature Extraction
Extract features and functionality from the codebase:
- **User Flows**: Identify user-facing features and workflows
- **API Endpoints**: Catalog all routes, handlers, and APIs
- **Data Models**: Extract database schemas, types, and data structures
- **Business Logic**: Understand core functionality and rules
- **UI Components**: Identify pages, views, and components

### 3. Generate Constitution
Create `.speckit/constitution.md` with:
- **Discovered Principles**: Extract coding standards from existing patterns
- **Tech Stack**: Document current technologies in use
- **Architecture Patterns**: Identify and document design patterns
- **Security Practices**: Note authentication, authorization, and security measures
- **Testing Approach**: Document existing test strategies

### 4. Generate Feature Specifications
For each major feature, create a spec in `specs/` directory:
- **Feature Number**: Assign sequential numbers (001, 002, etc.)
- **Description**: What the feature does
- **User Stories**: How users interact with the feature
- **Acceptance Criteria**: Success conditions
- **Current Implementation**: Document how it's currently built
- **Known Issues**: Any bugs or limitations discovered

### 5. Document Current Architecture
Create `specs/current-architecture.md`:
- **System Overview**: High-level architecture
- **Component Diagram**: How parts connect
- **Data Flow**: How data moves through the system
- **Dependencies**: External services and libraries
- **Infrastructure**: Hosting, databases, caching, etc.

### 6. Create Analysis Report
Generate `analysis-report.md` with:
- **Project Summary**: Overall assessment
- **Feature Inventory**: Complete list of features
- **Tech Stack Details**: Versions, compatibility
- **Code Metrics**: Lines of code, complexity, test coverage
- **Improvement Opportunities**: Areas for enhancement

## Output Structure
```
project-root/
├── .speckit/
│   ├── constitution.md          # Project principles & standards
│   └── analysis-report.md       # Detailed analysis report
├── specs/
│   ├── 001-feature-name/
│   │   ├── spec.md             # Feature specification
│   │   └── current-impl.md     # Current implementation notes
│   ├── 002-another-feature/
│   │   ├── spec.md
│   │   └── current-impl.md
│   └── current-architecture.md  # Overall architecture doc
└── [existing project files...]
```

## Instructions for AI Agent

1. **Scan the codebase thoroughly**:
   - Use file_search and grep_search to discover all project files
   - Read key configuration files (package.json, etc.)
   - Identify main entry points

2. **Analyze code patterns**:
   - Look for routing/controller patterns
   - Identify data models and schemas
   - Extract business logic
   - Find UI components and templates

3. **Extract git history insights** (if available):
   - Review commit messages for context
   - Identify frequently changed files (hot spots)
   - Look for pattern changes over time

4. **Create specifications**:
   - Write clear, comprehensive feature specs
   - Document WHAT the system does (not just HOW)
   - Include user stories from discovered functionality
   - Add acceptance criteria based on observed behavior

5. **Be thorough but practical**:
   - Focus on major features first
   - Group related functionality
   - Don't create excessive specs for minor utilities
   - Highlight areas that need clarification

## Example Usage

```bash
# In an existing project directory
/speckit.reverse-engineer

# Or with specific focus
/speckit.reverse-engineer --focus authentication,database,api
```

## Follow-up Commands

After reverse engineering, consider:
- `/speckit.audit` - Identify security and quality issues
- `/speckit.upgrade` - Generate improved specifications
- `/speckit.clarify` - Address underspecified areas
- `/speckit.plan` - Create modern implementation plans
