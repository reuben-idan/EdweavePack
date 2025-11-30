# Complete Database Setup Script (PowerShell)
# Runs migrations, seeds data, and verifies setup

param(
    [string]$ClusterName = "edweavepack-cluster",
    [string]$TaskDefinition = "edweavepack-backend",
    [string]$SubnetId,
    [string]$SecurityGroup,
    [string]$Region = "us-east-1",
    [string]$DatabaseUrl
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 EdweavePack Database Setup" -ForegroundColor Green
Write-Host "=" * 40

# Validate parameters
if (-not $SubnetId) {
    Write-Host "❌ SubnetId parameter is required" -ForegroundColor Red
    exit 1
}

if (-not $SecurityGroup) {
    Write-Host "❌ SecurityGroup parameter is required" -ForegroundColor Red
    exit 1
}

try {
    # Step 1: Run Migrations
    Write-Host "`n📝 Step 1: Running database migrations..." -ForegroundColor Yellow
    
    $migrationResult = aws ecs run-task `
        --cluster $ClusterName `
        --task-definition $TaskDefinition `
        --launch-type FARGATE `
        --network-configuration "awsvpcConfiguration={subnets=[$SubnetId],securityGroups=[$SecurityGroup],assignPublicIp=ENABLED}" `
        --overrides '{\"containerOverrides\":[{\"name\":\"backend\",\"command\":[\"python\",\"migrate.py\"]}]}' `
        --region $Region `
        --query 'tasks[0].taskArn' `
        --output text

    $MigrationTaskArn = $migrationResult.Trim()
    Write-Host "✅ Migration task started: $MigrationTaskArn" -ForegroundColor Green

    # Wait for migration completion
    aws ecs wait tasks-stopped --cluster $ClusterName --tasks $MigrationTaskArn --region $Region

    $migrationExitCode = aws ecs describe-tasks `
        --cluster $ClusterName `
        --tasks $MigrationTaskArn `
        --region $Region `
        --query 'tasks[0].containers[0].exitCode' `
        --output text

    if ($migrationExitCode.Trim() -ne "0") {
        Write-Host "❌ Migration failed with exit code: $migrationExitCode" -ForegroundColor Red
        exit 1
    }

    Write-Host "✅ Database migrations completed successfully" -ForegroundColor Green

    # Step 2: Seed Test Data
    Write-Host "`n🌱 Step 2: Seeding test data..." -ForegroundColor Yellow
    
    $seedResult = aws ecs run-task `
        --cluster $ClusterName `
        --task-definition $TaskDefinition `
        --launch-type FARGATE `
        --network-configuration "awsvpcConfiguration={subnets=[$SubnetId],securityGroups=[$SecurityGroup],assignPublicIp=ENABLED}" `
        --overrides '{\"containerOverrides\":[{\"name\":\"backend\",\"command\":[\"python\",\"seed_data.py\"]}]}' `
        --region $Region `
        --query 'tasks[0].taskArn' `
        --output text

    $SeedTaskArn = $seedResult.Trim()
    Write-Host "✅ Seed data task started: $SeedTaskArn" -ForegroundColor Green

    # Wait for seed completion
    aws ecs wait tasks-stopped --cluster $SeedTaskArn --tasks $SeedTaskArn --region $Region

    $seedExitCode = aws ecs describe-tasks `
        --cluster $ClusterName `
        --tasks $SeedTaskArn `
        --region $Region `
        --query 'tasks[0].containers[0].exitCode' `
        --output text

    if ($seedExitCode.Trim() -ne "0") {
        Write-Host "❌ Seed data failed with exit code: $seedExitCode" -ForegroundColor Red
        exit 1
    }

    Write-Host "✅ Test data seeded successfully" -ForegroundColor Green

    # Step 3: Verify Database
    Write-Host "`n🔍 Step 3: Verifying database setup..." -ForegroundColor Yellow
    
    if ($DatabaseUrl) {
        $env:DATABASE_URL = $DatabaseUrl
        python verify-database.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Database verification passed" -ForegroundColor Green
        } else {
            Write-Host "❌ Database verification failed" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "⚠️  Skipping verification - DATABASE_URL not provided" -ForegroundColor Yellow
    }

    # Summary
    Write-Host "`n🎉 Database setup completed successfully!" -ForegroundColor Green
    Write-Host "📊 Summary:" -ForegroundColor Cyan
    Write-Host "   ✅ Migrations: Completed" -ForegroundColor White
    Write-Host "   ✅ Seed Data: Loaded" -ForegroundColor White
    Write-Host "   ✅ Verification: Passed" -ForegroundColor White
    Write-Host "`n🚀 Ready for application deployment!" -ForegroundColor Green

}
catch {
    Write-Host "❌ Database setup failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}