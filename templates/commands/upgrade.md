# /speckit.upgrade

## Purpose

Transform existing specifications and audit findings into improved, modernized specifications that incorporate best practices, fix security issues, and leverage modern technologies.

## Prerequisites

- Completed `/speckit.reverse-engineer` to generate initial specs
- Optionally completed `/speckit.audit` to identify issues
- Review current specs in `specs/` directory

## Upgrade Strategy

### 1. Analyze Current State

**Review existing specifications:**

- Read all feature specs in `specs/`
- Review constitution and principles
- Check audit report for identified issues
- Understand current architecture

### 2. Identify Improvement Opportunities

**Security Improvements:**

- Fix vulnerabilities identified in audit
- Add missing security measures
- Implement defense in depth
- Add security requirements to specs

**Architecture Improvements:**

- Decouple tightly coupled components
- Add proper abstraction layers
- Implement design patterns
- Improve scalability
- Add fault tolerance

**Technology Modernization:**

- Upgrade to current framework versions
- Replace deprecated libraries
- Adopt modern best practices
- Leverage new platform features

**Quality Improvements:**

- Add comprehensive testing requirements
- Improve error handling
- Add logging and monitoring
- Enhance documentation

**Performance Optimization:**

- Add caching strategies
- Optimize database queries
- Implement lazy loading
- Add CDN for static assets

**User Experience:**

- Improve accessibility
- Enhance responsiveness
- Optimize for mobile
- Improve loading times

### 3. Modernize Tech Stack

**Evaluate alternatives:**

- **Frontend:**
  - Legacy jQuery → Modern React/Vue/Svelte
  - Class components → Hooks/Composition API
  - REST → GraphQL (if beneficial)
  - CSS → Tailwind/CSS Modules

- **Backend:**
  - Monolith → Microservices (if scale requires)
  - Blocking I/O → Async/await
  - Manual queries → ORM
  - Sessions → JWT tokens

- **Database:**
  - Add indexes for performance
  - Implement caching layer (Redis)
  - Consider read replicas
  - Add database migrations

- **Infrastructure:**
  - Manual deployment → CI/CD
  - Single server → Load balanced
  - No monitoring → APM + logging
  - No backups → Automated backups

### 4. Enhance Specifications

**Update each feature spec to include:**

- **Security Requirements:**
  - Input validation rules
  - Authentication/authorization
  - Data encryption
  - Rate limiting

- **Performance Requirements:**
  - Response time targets
  - Throughput requirements
  - Scalability goals
  - Resource limits

- **Quality Requirements:**
  - Test coverage expectations
  - Code quality standards
  - Documentation requirements
  - Error handling approach

- **Accessibility Requirements:**
  - WCAG compliance level
  - Keyboard navigation
  - Screen reader support
  - Color contrast ratios

- **Monitoring Requirements:**
  - Key metrics to track
  - Alerting thresholds
  - Logging requirements
  - Error tracking

### 5. Create Migration Plan

**Document transition strategy:**

- **Incremental approach** (preferred)
  - Feature-by-feature migration
  - Strangler fig pattern
  - Feature flags
  - Gradual rollout

- **Big bang approach** (when necessary)
  - Complete rewrite
  - Parallel run period
  - Cutover plan
  - Rollback strategy

## Output Structure

```markdown
specs/
├── upgraded/
│   ├── 001-authentication/
│   │   ├── spec.md              # Upgraded spec with security, performance
│   │   ├── migration-plan.md    # How to migrate from old to new
│   │   └── improvements.md      # What was improved and why
│   ├── 002-user-management/
│   │   └── ...
│   └── constitution.md          # Updated principles
├── original/                    # Backup of original specs
│   └── ...
└── upgrade-summary.md           # Overall upgrade summary
```

## Upgrade Summary Format

```markdown
# Specification Upgrade Summary

## Overview

**Original Version:** Current implementation
**Target Version:** Modernized implementation
**Upgrade Date:** [Date]

## Key Improvements

### Security Enhancements
- ✅ Added input validation on all user inputs
- ✅ Implemented JWT-based authentication
- ✅ Added rate limiting
- ✅ Encrypted sensitive data at rest
- ✅ Fixed SQL injection vulnerabilities

### Architecture Improvements
- ✅ Decoupled authentication module
- ✅ Implemented repository pattern
- ✅ Added caching layer
- ✅ Introduced event-driven architecture for notifications

### Technology Upgrades
- ✅ React 16 → React 18 with concurrent features
- ✅ Node 14 → Node 20 LTS
- ✅ PostgreSQL 12 → PostgreSQL 16
- ✅ Added TypeScript for type safety

### Performance Optimizations
- ✅ Database query optimization (indexes added)
- ✅ Implemented Redis caching
- ✅ Code splitting and lazy loading
- ✅ CDN for static assets

### Quality Improvements
- ✅ Test coverage: 45% → 85%
- ✅ Added E2E tests with Playwright
- ✅ Implemented proper error handling
- ✅ Added comprehensive logging

## Feature-by-Feature Changes

### Feature 001: Authentication
**Original Issues:**
- Passwords stored in plaintext
- No rate limiting on login
- Session fixation vulnerability

**Improvements:**
- Bcrypt password hashing
- Rate limiting (5 attempts per 15 minutes)
- Session regeneration after login
- JWT tokens with refresh mechanism
- 2FA support

**Migration Strategy:**
- Deploy new auth service alongside old
- Gradually migrate users
- Force password reset on first login to new system

### [Continue for each feature...]

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Data loss during migration | Low | High | Backup before migration, dry run |
| Downtime during cutover | Medium | Medium | Blue-green deployment |
| User resistance to UI changes | High | Low | Gradual rollout, user training |

## Rollout Plan

### Phase 1: Foundation (Week 1-2)
- Set up new infrastructure
- Implement core security improvements
- Add monitoring and logging

### Phase 2: Backend Migration (Week 3-4)
- Deploy new API alongside old
- Implement feature flags
- Migrate database schema

### Phase 3: Frontend Migration (Week 5-6)
- Roll out new UI to 10% of users
- Gather feedback
- Fix critical issues

### Phase 4: Full Rollout (Week 7-8)
- Gradual increase to 100%
- Monitor metrics
- Decommission old system

## Success Metrics

- 🎯 Zero security vulnerabilities (High/Critical)
- 🎯 95% test coverage
- 🎯 API response time < 200ms (p95)
- 🎯 99.9% uptime
- 🎯 Zero data loss during migration
- 🎯 User satisfaction score > 4.5/5
```

## Instructions for AI Agent

1. **Review all existing specs and audit findings:**
   - Read constitution, specs, audit report
   - Identify patterns of issues
   - Note current technology choices

2. **Research modern alternatives:**
   - Find current versions of frameworks
   - Identify better libraries/tools
   - Consider new architectural patterns
   - Evaluate industry best practices

3. **Prioritize improvements:**
   - Critical security fixes first
   - High-impact architectural changes
   - Performance optimizations
   - Quality of life improvements

4. **Create upgraded specs:**
   - Maintain original functionality
   - Add security requirements
   - Include performance targets
   - Specify quality standards
   - Document accessibility needs

5. **Plan migration strategy:**
   - Prefer incremental over big bang
   - Minimize risk and downtime
   - Provide rollback options
   - Consider user impact

6. **Document everything:**
   - What changed and why
   - How to migrate
   - Risks and mitigations
   - Success criteria

## Upgrade Principles

- ✅ **Maintain functionality:** Don't lose existing features
- ✅ **Fix security first:** Address all critical vulnerabilities
- ✅ **Incremental is better:** Gradual migration reduces risk
- ✅ **Measure success:** Define clear metrics
- ✅ **Plan for rollback:** Always have an escape hatch
- ✅ **User-centric:** Minimize disruption to users
- ✅ **Future-proof:** Choose sustainable technologies

## Example Usage

```bash
# Upgrade all specifications
/speckit.upgrade

# Upgrade specific feature
/speckit.upgrade --feature 001-authentication

# Focus on security improvements only
/speckit.upgrade --focus security
```

## Follow-up Commands

After upgrading specs:

- `/speckit.plan` - Create implementation plan for upgraded specs
- `/speckit.tasks` - Break down into actionable tasks
- `/speckit.implement` - Build the improved version
- `/speckit.compare` - Compare old vs new specifications
