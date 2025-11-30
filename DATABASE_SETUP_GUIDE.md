# Database Setup Guide - ECS RunTask & CodeBuild

This guide covers running database migrations and seeding test data using ephemeral ECS RunTask or CodeBuild jobs.

## 📁 Created Files

### Migration & Seed Scripts
- `backend/migrate.py` - Alembic migration runner
- `backend/seed_data.py` - Test data seeding script
- `verify-database.py` - Database verification script
- `verify-db.sql` - SQL verification queries

### ECS RunTask Scripts
- `run-migrations.sh` / `run-migrations.ps1` - Run migrations via ECS
- `run-seed-data.sh` / `run-seed-data.ps1` - Seed data via ECS
- `setup-database.ps1` - Complete database setup

### CodeBuild Alternative
- `codebuild-database-setup.yml` - CodeBuild buildspec for database setup

## 🚀 ECS RunTask Method

### Prerequisites
- ECS Cluster: `edweavepack-cluster`
- Task Definition: `edweavepack-backend`
- VPC Subnet ID and Security Group
- Database URL configured in task definition

### Step 1: Run Migrations

**PowerShell:**
```powershell
.\run-migrations.ps1 -SubnetId "subnet-xxx" -SecurityGroup "sg-xxx"
```

**Bash:**
```bash
# Update subnet and security group in script first
./run-migrations.sh
```

### Step 2: Seed Test Data

**PowerShell:**
```powershell
.\run-seed-data.ps1 -SubnetId "subnet-xxx" -SecurityGroup "sg-xxx"
```

**Bash:**
```bash
./run-seed-data.sh
```

### Step 3: Complete Setup (All-in-One)

**PowerShell:**
```powershell
.\setup-database.ps1 -SubnetId "subnet-xxx" -SecurityGroup "sg-xxx" -DatabaseUrl "postgresql://..."
```

## 🏗️ CodeBuild Method

### Create CodeBuild Project

```bash
aws codebuild create-project \
  --name "edweavepack-database-setup" \
  --source type=GITHUB,location=https://github.com/your-repo/EdweavePack.git \
  --artifacts type=NO_ARTIFACTS \
  --environment type=LINUX_CONTAINER,image=aws/codebuild/amazonlinux2-x86_64-standard:3.0 \
  --service-role arn:aws:iam::account:role/CodeBuildServiceRole \
  --environment-variables name=DATABASE_URL,value=postgresql://...
```

### Run CodeBuild Job

```bash
aws codebuild start-build --project-name "edweavepack-database-setup"
```

## 🔍 Verification

### Database Verification Script

```bash
# Set DATABASE_URL environment variable
export DATABASE_URL="postgresql://user:pass@host:5432/dbname"

# Run verification
python verify-database.py
```

**Expected Output:**
```
EdweavePack Database Verification
========================================
🔍 Verifying database setup...
📊 Found 3 tables:
   - assessments
   - curricula  
   - users
✅ All required tables exist
📈 users: 3 records
📈 curricula: 3 records
📈 assessments: 2 records
✅ Database verification successful
```

### SQL Verification (via psql)

```bash
# Connect to database
psql $DATABASE_URL

# Run verification queries
\i verify-db.sql
```

**Key Queries:**
```sql
-- Count records
SELECT COUNT(*) FROM users;    -- Should be > 0
SELECT COUNT(*) FROM curricula; -- Should be > 0

-- Sample data
SELECT id, email, name FROM users LIMIT 3;
SELECT id, title, subject FROM curricula LIMIT 3;
```

## 📊 Expected Results

### Migration Logs
```
✅ Database migrations completed successfully
INFO  [alembic.runtime.migration] Context impl PostgreSQLImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade -> abc123, Initial migration
```

### Seed Data Logs
```
Created user: teacher1@edweavepack.com
Created user: teacher2@edweavepack.com  
Created user: admin@edweavepack.com
Created curriculum: Introduction to Python Programming
Created curriculum: Algebra Fundamentals
Created curriculum: Cell Biology Basics
Created assessment: Python Basics Quiz
Created assessment: Algebra Assessment

✅ Seed data created successfully:
   Users: 3
   Curricula: 3
   Assessments: 2
```

### Database Counts
- **Users**: 3 records (2 teachers, 1 admin)
- **Curricula**: 3 records (Python, Algebra, Biology)
- **Assessments**: 2 records (Python Quiz, Algebra Assessment)

## 🔧 Configuration

### Environment Variables Required

```env
DATABASE_URL=postgresql://user:pass@host:5432/edweavepack
```

### ECS Task Definition Updates

Add to container environment:
```json
{
  "environment": [
    {
      "name": "DATABASE_URL",
      "value": "postgresql://user:pass@rds-endpoint:5432/edweavepack"
    }
  ]
}
```

### Network Configuration

- **Subnet**: Must have internet access for package downloads
- **Security Group**: Must allow outbound HTTPS (443) and database access
- **Public IP**: Required for Fargate tasks to download packages

## 🚨 Troubleshooting

### Common Issues

1. **Task fails to start**
   - Check subnet has internet access
   - Verify security group allows outbound traffic
   - Ensure task definition is valid

2. **Database connection fails**
   - Verify DATABASE_URL is correct
   - Check security group allows database port (5432)
   - Ensure RDS is accessible from subnet

3. **Migration fails**
   - Check if database exists
   - Verify user has CREATE TABLE permissions
   - Review CloudWatch logs for detailed errors

### Debug Commands

```bash
# Check ECS task logs
aws logs get-log-events \
  --log-group-name "/ecs/edweavepack-backend" \
  --log-stream-name "ecs/backend/task-id"

# Test database connectivity
psql $DATABASE_URL -c "SELECT version();"

# Check task definition
aws ecs describe-task-definition --task-definition edweavepack-backend
```

## ✅ Success Criteria

- [x] Migration task completes with exit code 0
- [x] Seed data task completes with exit code 0  
- [x] `SELECT COUNT(*) FROM users` returns > 0
- [x] `SELECT COUNT(*) FROM curricula` returns > 0
- [x] Database verification script passes
- [x] Sample queries return expected data

## 🎯 Next Steps

After successful database setup:

1. **Deploy Application**: Update ECS service with latest task definition
2. **Test Endpoints**: Verify API endpoints work with seeded data
3. **Monitor Logs**: Check application logs for any database-related errors
4. **Backup Database**: Create initial backup of seeded database

The database is now ready for EdweavePack application deployment!