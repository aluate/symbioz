# Database Migrations

**Phase 2.5 — CONTROL_OTTO_PHASE2_5_FOUNDATIONS.md**

This document tracks database schema migrations for Life OS backend.

---

## Migration System

We use **Alembic** for database migrations.

### Setup

1. Install Alembic:
   ```bash
   pip install alembic
   ```

2. Configuration:
   - `alembic.ini` - Alembic configuration
   - `migrations/env.py` - Migration environment
   - `migrations/versions/` - Migration scripts

### Running Migrations

**Create a new migration:**
```bash
cd apps/life_os/backend
alembic revision --autogenerate -m "description"
```

**Apply migrations:**
```bash
alembic upgrade head
```

**Rollback one migration:**
```bash
alembic downgrade -1
```

**Check current revision:**
```bash
alembic current
```

**Check pending migrations:**
```bash
alembic heads
```

---

## Migration History

### 001_initial_phase2_5 (2025-01-XX)

**Phase 2.5 Baseline Migration**

Creates:
- `households` table
- `user_profiles` table
- `categories` table
- `category_versions` table
- `otto_events` table

Adds to existing tables:
- `household_id` and `user_id` to: `otto_runs`, `otto_tasks`, `life_os_tasks`, `bills`, `calendar_events`, `income`, `transactions`
- `reasoning` and `evidence` to `otto_runs`
- `category_id` and `category_version` to `transactions`

**Status:** ✅ Created

---

## Migration Health Check

The `EnvStatusSkill` checks for pending migrations:

- If Alembic is installed and configured, it checks if current revision matches head
- If migrations are pending, it reports:
  - `needs_migration: true`
  - Action: "Run: alembic upgrade head"

**Note:** For development, SQLite auto-creates tables. Migrations are required before production.

---

## Best Practices

1. **Always create a migration** when:
   - Adding new models
   - Adding/removing columns
   - Changing column types
   - Adding/removing foreign keys

2. **Test migrations**:
   - Test upgrade path
   - Test downgrade path (if applicable)
   - Test on sample data

3. **Document changes**:
   - Update this file
   - Add comments in migration script
   - Note any data migrations needed

4. **Before production**:
   - Review all migrations
   - Test on staging
   - Backup database before applying

---

## Troubleshooting

**"Target database is not up to date"**
- Run `alembic upgrade head`

**"Can't locate revision identified by 'xxx'"**
- Check `alembic_version` table in database
- May need to manually set revision or recreate database

**"Table already exists"**
- Migration may have been partially applied
- Check database state vs migration scripts
- May need to manually fix or recreate

