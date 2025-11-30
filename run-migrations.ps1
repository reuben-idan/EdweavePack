# ECS RunTask for Database Migrations (PowerShell)
# This script runs database migrations using ECS RunTask

param(
    [string]$ClusterName = "edweavepack-cluster",
    [string]$TaskDefinition = "edweavepack-backend", 
    [string]$SubnetId = "subnet-0123456789abcdef0",
    [string]$SecurityGroup = "sg-0123456789abcdef0",
    [string]$Region = "us-east-1"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Running database migrations via ECS RunTask..." -ForegroundColor Green

try {
    # Run migration task
    $taskResult = aws ecs run-task `
        --cluster $ClusterName `
        --task-definition $TaskDefinition `
        --launch-type FARGATE `
        --network-configuration "awsvpcConfiguration={subnets=[$SubnetId],securityGroups=[$SecurityGroup],assignPublicIp=ENABLED}" `
        --overrides '{\"containerOverrides\":[{\"name\":\"backend\",\"command\":[\"python\",\"migrate.py\"]}]}' `
        --region $Region `
        --query 'tasks[0].taskArn' `
        --output text

    $TaskArn = $taskResult.Trim()
    Write-Host "✅ Migration task started: $TaskArn" -ForegroundColor Green

    # Wait for task completion
    Write-Host "⏳ Waiting for migration task to complete..." -ForegroundColor Yellow
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
    Write-Host "📋 Migration logs:" -ForegroundColor Cyan
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
        Write-Host "✅ Database migrations completed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Database migrations failed with exit code: $ExitCode" -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "❌ Error running migrations: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}