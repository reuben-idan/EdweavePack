# ECS RunTask for Seeding Test Data (PowerShell)
# This script seeds the database with test data using ECS RunTask

param(
    [string]$ClusterName = "edweavepack-cluster",
    [string]$TaskDefinition = "edweavepack-backend",
    [string]$SubnetId = "subnet-0123456789abcdef0", 
    [string]$SecurityGroup = "sg-0123456789abcdef0",
    [string]$Region = "us-east-1"
)

$ErrorActionPreference = "Stop"

Write-Host "🌱 Seeding database with test data via ECS RunTask..." -ForegroundColor Green

try {
    # Run seed data task
    $taskResult = aws ecs run-task `
        --cluster $ClusterName `
        --task-definition $TaskDefinition `
        --launch-type FARGATE `
        --network-configuration "awsvpcConfiguration={subnets=[$SubnetId],securityGroups=[$SecurityGroup],assignPublicIp=ENABLED}" `
        --overrides '{\"containerOverrides\":[{\"name\":\"backend\",\"command\":[\"python\",\"seed_data.py\"]}]}' `
        --region $Region `
        --query 'tasks[0].taskArn' `
        --output text

    $TaskArn = $taskResult.Trim()
    Write-Host "✅ Seed data task started: $TaskArn" -ForegroundColor Green

    # Wait for task completion
    Write-Host "⏳ Waiting for seed data task to complete..." -ForegroundColor Yellow
    aws ecs wait tasks-stopped `
        --cluster $ClusterName `
        --tasks $TaskArn `
        --region $Region

    # Get task exit code
    $exitCodeResult = aws ecs describe-tasks `
        --cluster $ClusterName `
        --tasks $TaskArn `
        --region $Region `
        --query 'tasks[0].containers[0].exitCode' `
        --output text

    $ExitCode = $exitCodeResult.Trim()

    # Get logs
    Write-Host "📋 Seed data logs:" -ForegroundColor Cyan
    $LogGroup = "/ecs/edweavepack-backend"
    
    $logStreamResult = aws logs describe-log-streams `
        --log-group-name $LogGroup `
        --order-by LastEventTime `
        --descending `
        --max-items 1 `
        --query 'logStreams[0].logStreamName' `
        --output text

    $LogStream = $logStreamResult.Trim()

    if ($LogStream -ne "None" -and $LogStream -ne "null") {
        aws logs get-log-events `
            --log-group-name $LogGroup `
            --log-stream-name $LogStream `
            --query 'events[*].message' `
            --output text
    }

    if ($ExitCode -eq "0") {
        Write-Host "✅ Database seeding completed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Database seeding failed with exit code: $ExitCode" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Error seeding database: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}