# /speckit.migrate

## Purpose

Create and execute a comprehensive migration plan to transition from an existing project to the improved Spec-Kit version. Handles code migration, data migration, testing, and deployment strategy.

## Prerequisites

- Completed `/speckit.reverse-engineer` - Specs generated from existing code
- Completed `/speckit.audit` - Issues identified
- Completed `/speckit.upgrade` - Improved specs created
- Completed `/speckit.plan` - New implementation plan ready

## Migration Strategies

### Strategy 1: Strangler Fig Pattern (Recommended)

**Gradual replacement of old system:**

1. New and old systems run in parallel
2. Migrate one feature at a time
3. Route traffic gradually to new implementation
4. Retire old code after validation

**Benefits:**

- Low risk - can roll back any feature
- Continuous delivery - ship improvements incrementally
- Learn and adapt during migration
- No big-bang deployment

**Process:**

```
[Old System] ←→ [Router/Proxy] ←→ [New System]
                     ↓
              Feature Flags control routing
```

### Strategy 2: Feature Flags

**Run both implementations, toggle at runtime:**

1. Deploy new code alongside old
2. Use feature flags to control which code executes
3. Gradually enable for users (10% → 50% → 100%)
4. Monitor metrics and rollback if needed

### Strategy 3: Blue-Green Deployment

**Two complete environments:**

1. Build entire new system (Green)
2. Keep old system running (Blue)
3. Switch traffic atomically
4. Keep blue environment for rollback

**Best for:** Smaller projects where full rebuild is feasible

### Strategy 4: Database-First Migration

**When data model changes significantly:**

1. Migrate database schema first
2. Update old code to work with new schema
3. Deploy new application code
4. Cleanup old tables/columns

## Migration Plan Template

```markdown
# Migration Plan: [Project Name]

## Executive Summary

- **Current State:** [Brief description]
- **Target State:** [Brief description]
- **Strategy:** [Strangler Fig / Feature Flags / Blue-Green]
- **Timeline:** [X weeks]
- **Risk Level:** [Low / Medium / High]

## Phase 1: Preparation (Week 1)

### Infrastructure Setup

- [ ] Set up new hosting environment
- [ ] Configure CI/CD pipeline
- [ ] Set up monitoring (DataDog/New Relic/etc.)
- [ ] Configure logging (Elasticsearch/CloudWatch/etc.)
- [ ] Set up error tracking (Sentry/Rollbar/etc.)

### Database Migration Prep

- [ ] Backup production database
- [ ] Create migration scripts
- [ ] Test migrations on copy of production data
- [ ] Plan for rollback

### Feature Flag Setup

- [ ] Install feature flag service (LaunchDarkly/Unleash/etc.)
- [ ] Define flags for each feature
- [ ] Test flag toggling in dev environment

## Phase 2: Foundation Migration (Week 2)

### Core Infrastructure

- [ ] Deploy authentication service
- [ ] Deploy API gateway/router
- [ ] Set up database connections
- [ ] Configure caching layer

### Data Migration

- [ ] Run database migration scripts
- [ ] Verify data integrity
- [ ] Update indices
- [ ] Test queries

### Validation

- [ ] Run integration tests
- [ ] Performance testing
- [ ] Security scanning
- [ ] Load testing

## Phase 3: Feature Migration (Weeks 3-6)

### Feature 001: Authentication (Week 3)

**Preparation:**

- [ ] Deploy new auth service
- [ ] Configure routing to old auth initially
- [ ] Smoke test new auth in staging

**Migration:**

- [ ] Enable for internal users (Monday)
- [ ] Monitor for errors and performance
- [ ] Enable for 10% of users (Wednesday)
- [ ] Monitor metrics
- [ ] Enable for 50% of users (Friday)
- [ ] Full rollout (following Monday)
- [ ] Decommission old auth (Week 4)

**Rollback Plan:**

- If error rate > 1%: Roll back to 10%
- If error rate > 5%: Full rollback to old system
- Rollback trigger: Feature flag toggle

**Success Metrics:**

- Error rate < 0.1%
- Latency < 200ms (p95)
- No user complaints
- All tests passing

### Feature 002: [Next Feature] (Week 4)

[Repeat structure...]

## Phase 4: Final Cutover (Week 7)

### Complete Migration

- [ ] All features migrated and validated
- [ ] 100% of traffic on new system
- [ ] Old system in read-only mode

### Cleanup

- [ ] Remove feature flags
- [ ] Decommission old infrastructure
- [ ] Archive old code repository
- [ ] Update documentation

### Post-Migration

- [ ] Monitor for 2 weeks
- [ ] Address any issues
- [ ] Performance optimization
- [ ] User feedback survey

## Data Migration Details

### User Data

**Source:** `old_db.users`
**Target:** `new_db.users`

**Mapping:**

```sql
-- Migration script
INSERT INTO new_db.users (id, email, hashed_password, created_at)
SELECT
  id,
  email,
  bcrypt_hash(legacy_password) as hashed_password,
  created_at
FROM old_db.users
WHERE deleted_at IS NULL;
```

**Validation:**

```sql
-- Verify counts match
SELECT COUNT(*) FROM old_db.users WHERE deleted_at IS NULL;
SELECT COUNT(*) FROM new_db.users;

-- Verify no duplicates
SELECT email, COUNT(*) FROM new_db.users GROUP BY email HAVING COUNT(*) > 1;
```

### Transaction Data

[Similar structure for other data...]

## Rollback Procedures

### Feature-Level Rollback

```bash
# Disable feature flag
feature-flag --flag auth_v2 --state off

# Verify traffic routing back to old system
curl -H "X-Feature-Flag: auth_v2=off" https://api.example.com/health
```

### Full System Rollback

```bash
# Switch load balancer to old system
aws elbv2 modify-listener --listener-arn <arn> --default-actions Type=forward,TargetGroupArn=<old-system-arn>

# Or DNS change
aws route53 change-resource-record-sets --hosted-zone-id <zone> --change-batch file://rollback.json
```

### Database Rollback

```sql
-- Restore from backup
pg_restore -d production backup-YYYY-MM-DD.dump

-- Or run reverse migration
psql production < migration_rollback.sql
```

## Monitoring During Migration

### Key Metrics to Track

**Performance:**

- Response time (p50, p95, p99)
- Throughput (requests/second)
- Error rate
- Database query time

**Business:**

- User signups
- Conversion rate
- Feature usage
- Customer support tickets

**Infrastructure:**

- CPU usage
- Memory usage
- Database connections
- Cache hit rate

### Alert Thresholds

```yaml
alerts:
  - name: High Error Rate
    condition: error_rate > 1%
    action: Notify team, consider rollback
    
  - name: Slow Response
    condition: p95_latency > 500ms
    action: Investigate, optimize
    
  - name: Database Overload
    condition: connection_pool > 80%
    action: Scale up database
```

## Communication Plan

### Stakeholders

- **Engineering Team:** Daily standups, Slack updates
- **Product Team:** Weekly status reports
- **Executive Team:** Milestone updates
- **Customer Support:** Training sessions, FAQ document
- **End Users:** Email announcements for major changes

### User Communication

**Week before migration:**
```
Subject: We're improving [Feature]!

Hi [Name],

We're excited to announce improvements to [feature] coming next week.
What's new:
- Faster performance
- Enhanced security
- Better mobile experience

You don't need to do anything - the update will happen automatically.

Questions? Contact support@example.com
```

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Data loss during migration | Low | Critical | Full backup, dry run, verification queries |
| Extended downtime | Medium | High | Blue-green deployment, feature flags |
| Performance degradation | Medium | Medium | Load testing before migration, monitoring |
| User confusion | High | Low | Clear communication, gradual rollout |
| Third-party API failures | Low | Medium | Circuit breakers, fallback mechanisms |

## Post-Migration Validation

### Week 1 After Migration

- [ ] All metrics within acceptable range
- [ ] No critical bugs reported
- [ ] User feedback reviewed
- [ ] Performance optimizations identified

### Month 1 After Migration

- [ ] Full system stability achieved
- [ ] Old infrastructure decommissioned
- [ ] Documentation updated
- [ ] Retrospective completed

### Quarter 1 After Migration

- [ ] Business metrics improved
- [ ] Technical debt paid down
- [ ] Team velocity increased
- [ ] Security posture improved
```

## Instructions for AI Agent

1. **Assess migration complexity:**
   - Analyze differences between old and new
   - Identify data migration requirements
   - Estimate timeline and effort
   - Choose appropriate strategy

2. **Create detailed plan:**
   - Break down into phases
   - Assign specific tasks
   - Define success criteria
   - Plan rollback procedures

3. **Consider data migration:**
   - Analyze schema changes
   - Write migration scripts
   - Plan for data validation
   - Handle data transformation

4. **Plan deployment strategy:**
   - Choose deployment method
   - Set up feature flags
   - Configure monitoring
   - Prepare rollback procedures

5. **Communication:**
   - Identify stakeholders
   - Plan announcements
   - Create user documentation
   - Prepare support team

6. **Risk management:**
   - Identify potential risks
   - Plan mitigations
   - Define escalation procedures
   - Prepare contingency plans

## Example Usage

```bash
# Create migration plan
/speckit.migrate

# Specific feature only
/speckit.migrate --feature 001-authentication

# Blue-green strategy
/speckit.migrate --strategy blue-green
```

## Follow-up Commands

- `/speckit.implement` - Execute the migration
- `/speckit.test-from-code` - Generate regression tests
- `/speckit.compare` - Verify feature parity
