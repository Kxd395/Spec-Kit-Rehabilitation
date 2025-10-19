# /speckit.compare

## Purpose

Compare the old (existing) implementation with the new (upgraded) specifications and implementation to ensure feature parity, identify improvements, and validate that all functionality is preserved.

## Prerequisites

- Original project analyzed with `/speckit.reverse-engineer`
- New specifications created with `/speckit.upgrade`
- Optionally: New implementation generated with `/speckit.implement`

## Comparison Categories

### 1. Feature Parity Check

**Verify all existing features are present in new specs:**

- List all features in old system
- Check corresponding features in new specs
- Identify any missing functionality
- Flag deprecated features to be removed

### 2. Functional Comparison

**Compare behavior of old vs new:**

- Input/output validation
- Edge case handling
- Error messages and codes
- Business logic accuracy
- Data transformations

### 3. API Comparison

**For APIs and services:**

- Endpoint compatibility
- Request/response formats
- Status codes
- Headers
- Authentication methods
- Rate limiting

### 4. Data Model Comparison

**Database schemas:**

- Table structure changes
- Column additions/deletions
- Data type changes
- Constraints and indexes
- Relationships
- Migration impact

### 5. Performance Comparison

**Measure improvements:**

- Response time (old vs new)
- Throughput
- Resource usage (CPU, memory)
- Database query efficiency
- Page load times
- Bundle sizes

### 6. Security Comparison

**Evaluate security posture:**

- Vulnerabilities fixed
- New security features added
- Authentication improvements
- Authorization enhancements
- Data protection

### 7. User Experience Comparison

**UI/UX changes:**

- Interface changes
- User workflows
- Accessibility improvements
- Mobile responsiveness
- Visual design updates

## Output Format

Generate `comparison-report.md`:

```markdown
# Old vs New Comparison Report

**Project:** [Project Name]
**Comparison Date:** [Date]
**Old Version:** Current Production
**New Version:** Upgraded Spec-Kit Implementation

## Executive Summary

**Overall Assessment:** ✅ New version ready / ⚠️ Issues to address / ❌ Not ready

**Feature Parity:** [X]% complete
**Performance:** [Better / Same / Worse]
**Security:** [Improved / Same / Degraded]

### Key Findings

- ✅ All critical features migrated
- ✅ Performance improved by 40%
- ✅ 15 security vulnerabilities fixed
- ⚠️ 2 minor features pending review
- ❌ Mobile UI needs refinement

## Feature-by-Feature Comparison

### Feature: User Authentication

#### Old Implementation

**Location:** `src/auth/login.js`
**Functionality:**

- Username/password login
- Session-based auth
- No rate limiting
- Passwords stored with MD5 (⚠️ weak)

**Issues:**

- 🔴 Vulnerable to brute force attacks
- 🔴 Weak password hashing
- 🟡 No 2FA support
- 🟡 Sessions don't expire

#### New Implementation

**Location:** `specs/001-authentication/spec.md`, `specs/001-authentication/plan.md`
**Functionality:**

- Username/password login (✅ same)
- JWT-based auth (🆕 improved)
- Rate limiting: 5 attempts per 15 min (🆕 added)
- Bcrypt password hashing (✅ fixed)
- 2FA support (🆕 added)
- Token expiration: 1 hour (🆕 added)

**Improvements:**

- ✅ Brute force protection via rate limiting
- ✅ Strong password hashing (bcrypt)
- ✅ Added 2FA for enhanced security
- ✅ Stateless auth with JWTs
- ✅ Automatic token expiration

**Status:** ✅ Ready for migration

---

### Feature: User Profile Management

[Continue for each feature...]

## API Endpoint Comparison

| Endpoint | Old | New | Status | Notes |
|----------|-----|-----|--------|-------|
| POST /api/login | ✅ | ✅ | ✅ Compatible | Request format unchanged |
| POST /api/register | ✅ | ✅ | ⚠️ Modified | Now requires email verification |
| GET /api/profile | ✅ | ✅ | ✅ Compatible | Response includes new fields |
| PUT /api/profile | ✅ | ✅ | ✅ Compatible | Backward compatible |
| DELETE /api/account | ✅ | ✅ | ✅ Compatible | Added soft delete |
| GET /api/admin/users | ✅ | ✅ | ⚠️ Modified | Pagination now required |

**Breaking Changes:**

- ⚠️ `/api/register` now requires email verification before account activation
- ⚠️ `/api/admin/users` requires pagination parameters (breaking for existing clients)

**Recommended Actions:**

- Version API as `/api/v2/` to maintain backward compatibility
- Provide migration guide for API consumers
- Deprecate old endpoints with 6-month sunset period

## Data Model Comparison

### Users Table

| Column | Old Type | New Type | Change | Migration |
|--------|----------|----------|--------|-----------|
| id | INT | UUID | Modified | Generate UUIDs for existing rows |
| username | VARCHAR(50) | VARCHAR(100) | Extended | No migration needed |
| password | VARCHAR(32) | VARCHAR(255) | Extended | Rehash all passwords on next login |
| created_at | DATETIME | TIMESTAMP | Modified | Convert to UTC timestamps |
| email | - | VARCHAR(255) | Added | Prompt users to add email |
| two_factor_secret | - | VARCHAR(255) | Added | NULL for existing users |

**Migration Script:**

```sql
-- Add new columns
ALTER TABLE users ADD COLUMN email VARCHAR(255);
ALTER TABLE users ADD COLUMN two_factor_secret VARCHAR(255);

-- Extend password column for bcrypt
ALTER TABLE users MODIFY password VARCHAR(255);

-- Prompt users to update
UPDATE users SET password_reset_required = TRUE;
```

## Performance Comparison

### Response Time (95th Percentile)

| Endpoint | Old (ms) | New (ms) | Improvement |
|----------|----------|----------|-------------|
| GET /api/profile | 450 | 180 | ⬆️ 60% faster |
| POST /api/login | 320 | 220 | ⬆️ 31% faster |
| GET /api/admin/users | 2400 | 350 | ⬆️ 85% faster |
| PUT /api/profile | 280 | 190 | ⬆️ 32% faster |

**Key Optimizations:**

- ✅ Added database indexes on frequently queried columns
- ✅ Implemented Redis caching for user profiles
- ✅ Optimized N+1 queries in admin endpoint
- ✅ Added pagination to reduce payload size

### Resource Usage

| Metric | Old | New | Change |
|--------|-----|-----|--------|
| Avg CPU | 65% | 35% | ⬇️ 46% reduction |
| Avg Memory | 2.1 GB | 1.4 GB | ⬇️ 33% reduction |
| DB Connections | 150 | 50 | ⬇️ 67% reduction |

### Page Load Times

| Page | Old (s) | New (s) | Improvement |
|------|---------|---------|-------------|
| Login | 2.8 | 1.2 | ⬆️ 57% faster |
| Dashboard | 4.5 | 1.8 | ⬆️ 60% faster |
| Profile | 3.2 | 1.5 | ⬆️ 53% faster |

**Frontend Optimizations:**

- ✅ Code splitting reduced initial bundle size
- ✅ Lazy loading for non-critical components
- ✅ Image optimization and WebP format
- ✅ CDN for static assets

## Security Comparison

### Vulnerabilities Fixed

| Vulnerability | CVSS | Status |
|---------------|------|--------|
| SQL Injection in login | 9.1 Critical | ✅ Fixed (parameterized queries) |
| Weak password hashing (MD5) | 8.3 High | ✅ Fixed (bcrypt) |
| No rate limiting | 7.5 High | ✅ Fixed (5 attempts/15 min) |
| XSS in profile fields | 6.8 Medium | ✅ Fixed (input sanitization) |
| Missing CSRF protection | 6.5 Medium | ✅ Fixed (CSRF tokens) |

### Security Enhancements Added

- ✅ Two-factor authentication
- ✅ JWT-based stateless auth
- ✅ Password complexity requirements
- ✅ Account lockout after failed attempts
- ✅ Security headers (CSP, HSTS, etc.)
- ✅ Input validation on all endpoints
- ✅ Audit logging for sensitive actions

## User Experience Comparison

### Accessibility Improvements

| Criterion | Old | New | Status |
|-----------|-----|-----|--------|
| WCAG 2.1 Level AA | ❌ | ✅ | ✅ Compliant |
| Keyboard navigation | Partial | Complete | ✅ Improved |
| Screen reader support | Poor | Excellent | ✅ Improved |
| Color contrast | 3.5:1 | 4.8:1 | ✅ Improved |
| Focus indicators | Missing | Visible | ✅ Added |

### Mobile Experience

- ✅ Responsive design (vs fixed desktop-only)
- ✅ Touch-friendly controls
- ✅ Optimized for slower connections
- ✅ PWA support with offline mode

### User Workflows

**Old: Login Process**

1. Enter credentials
2. Click login
3. Redirect to dashboard

**New: Login Process**

1. Enter credentials
2. Click login
3. [If 2FA enabled] Enter verification code
4. Redirect to dashboard

**Impact:** Minimal change, optional 2FA step improves security

## Missing Features Analysis

### Features Intentionally Deprecated

- ❌ **Flash-based file uploader** - Replaced with modern HTML5 uploader
- ❌ **Legacy admin panel** - Replaced with new React-based admin panel
- ❌ **XML API** - JSON-only in new version (breaking change)

### Features Pending Migration

- ⚠️ **Email templates customization** - Planned for Phase 2
- ⚠️ **Advanced reporting** - Planned for Phase 3

## Test Coverage Comparison

| Category | Old Coverage | New Coverage | Change |
|----------|--------------|--------------|--------|
| Unit Tests | 42% | 85% | ⬆️ +43% |
| Integration Tests | 15% | 68% | ⬆️ +53% |
| E2E Tests | 0% | 45% | ⬆️ +45% |

**Testing Improvements:**

- ✅ Added comprehensive unit test suite
- ✅ Integration tests for all API endpoints
- ✅ E2E tests with Playwright for critical user flows
- ✅ Performance regression tests

## Deployment Comparison

### Old Deployment Process

1. Manual SSH to server
2. Git pull
3. Restart service
4. Hope it works

**Issues:** Manual, error-prone, no rollback

### New Deployment Process

1. Push to GitHub
2. CI/CD pipeline runs tests
3. Automated deployment to staging
4. Approval required for production
5. Blue-green deployment
6. Automated rollback on errors

**Improvements:**

- ✅ Fully automated
- ✅ Zero-downtime deployments
- ✅ Automatic rollback
- ✅ Staging environment for validation

## Recommendation

### Overall Assessment: ✅ **Ready for Migration with Minor Adjustments**

**Strengths:**

- ✅ All critical features migrated
- ✅ Significant performance improvements
- ✅ Security vulnerabilities addressed
- ✅ Better code quality and test coverage

**Action Items Before Migration:**

1. 📋 Complete pending features (email templates, reporting)
2. 📋 Create API migration guide for breaking changes
3. 📋 Train support team on new features
4. 📋 Conduct user acceptance testing
5. 📋 Prepare rollback plan

**Timeline:** Ready for migration in 2 weeks after action items completed

## Next Steps

1. Review this comparison with stakeholders
2. Address action items
3. Create detailed migration plan with `/speckit.migrate`
4. Schedule migration window
5. Execute migration
```

## Instructions for AI Agent

1. **Analyze both versions thoroughly:**
   - Read all original code/specs
   - Read all upgraded specs and implementation
   - Create comprehensive feature inventory

2. **Compare feature-by-feature:**
   - Document what exists in each
   - Flag any missing functionality
   - Note improvements and changes
   - Identify breaking changes

3. **Measure performance:**
   - If possible, benchmark both versions
   - Compare resource usage
   - Evaluate scalability improvements

4. **Security assessment:**
   - List vulnerabilities fixed
   - Note new security features
   - Verify nothing was downgraded

5. **User impact analysis:**
   - Identify workflow changes
   - Note UI/UX improvements
   - Flag potential user confusion

6. **Provide clear recommendation:**
   - Ready / Not Ready / Ready with conditions
   - List specific action items
   - Estimate timeline

## Example Usage

```bash
# Full comparison
/speckit.compare

# Compare specific feature
/speckit.compare --feature 001-authentication

# Performance comparison only
/speckit.compare --focus performance
```

## Follow-up Commands

- `/speckit.migrate` - Create migration plan based on comparison
- `/speckit.test-from-code` - Generate tests to verify equivalence
- `/speckit.implement` - Address any gaps identified
