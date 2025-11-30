# AWS Cognito Setup Script for EdweavePack (PowerShell)
# This script creates the Cognito User Pool and App Client

param(
    [string]$Region = "us-east-1",
    [string]$PoolName = "edweavepack-userpool",
    [string]$ClientName = "edweavepack-web"
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Setting up AWS Cognito for EdweavePack..." -ForegroundColor Green

# Generate unique domain prefix
$DomainPrefix = "edweavepack-$(Get-Date -Format 'yyyyMMddHHmmss')"

try {
    # 1. Create Cognito User Pool
    Write-Host "📝 Creating Cognito User Pool: $PoolName" -ForegroundColor Yellow
    
    $poolConfig = @{
        PoolName = $PoolName
        Policies = @{
            PasswordPolicy = @{
                MinimumLength = 8
                RequireUppercase = $true
                RequireLowercase = $true
                RequireNumbers = $true
                RequireSymbols = $true
            }
        }
        AutoVerifiedAttributes = @("email")
        Schema = @(
            @{
                Name = "email"
                AttributeDataType = "String"
                Required = $true
                Mutable = $true
            },
            @{
                Name = "name"
                AttributeDataType = "String"
                Required = $true
                Mutable = $true
            }
        )
        VerificationMessageTemplate = @{
            DefaultEmailOption = "CONFIRM_WITH_CODE"
        }
    }
    
    $poolResult = aws cognito-idp create-user-pool --cli-input-json ($poolConfig | ConvertTo-Json -Depth 10) --region $Region --query 'UserPool.Id' --output text
    $PoolId = $poolResult.Trim()
    
    Write-Host "✅ User Pool created with ID: $PoolId" -ForegroundColor Green

    # 2. Create App Client
    Write-Host "📱 Creating App Client: $ClientName" -ForegroundColor Yellow
    
    $clientResult = aws cognito-idp create-user-pool-client `
        --user-pool-id $PoolId `
        --client-name $ClientName `
        --generate-secret `
        --explicit-auth-flows "ALLOW_USER_PASSWORD_AUTH" "ALLOW_REFRESH_TOKEN_AUTH" "ALLOW_USER_SRP_AUTH" `
        --supported-identity-providers "COGNITO" `
        --callback-urls "https://localhost:3000/callback" "http://localhost:3000/callback" `
        --logout-urls "https://localhost:3000/" "http://localhost:3000/" `
        --allowed-o-auth-flows "code" `
        --allowed-o-auth-scopes "openid" "email" "profile" `
        --allowed-o-auth-flows-user-pool-client `
        --region $Region `
        --query 'UserPoolClient.ClientId' `
        --output text
    
    $ClientId = $clientResult.Trim()
    Write-Host "✅ App Client created with ID: $ClientId" -ForegroundColor Green

    # 3. Create Cognito Domain
    Write-Host "🌐 Creating Cognito Domain: $DomainPrefix" -ForegroundColor Yellow
    
    aws cognito-idp create-user-pool-domain `
        --domain $DomainPrefix `
        --user-pool-id $PoolId `
        --region $Region
    
    $CognitoDomain = "$DomainPrefix.auth.$Region.amazoncognito.com"
    Write-Host "✅ Domain created: https://$CognitoDomain" -ForegroundColor Green

    # 4. Get Client Secret
    $clientDetails = aws cognito-idp describe-user-pool-client `
        --user-pool-id $PoolId `
        --client-id $ClientId `
        --region $Region `
        --query 'UserPoolClient.ClientSecret' `
        --output text
    
    $ClientSecret = $clientDetails.Trim()

    # 5. Create/Update AWS Secrets Manager secret
    Write-Host "🔐 Storing credentials in AWS Secrets Manager..." -ForegroundColor Yellow
    
    $secretValue = @{
        COGNITO_POOL_ID = $PoolId
        COGNITO_REGION = $Region
        COGNITO_CLIENT_ID = $ClientId
        COGNITO_CLIENT_SECRET = $ClientSecret
        COGNITO_DOMAIN = $CognitoDomain
        COGNITO_JWKS_URL = "https://cognito-idp.$Region.amazonaws.com/$PoolId/.well-known/jwks.json"
    } | ConvertTo-Json -Compress

    # Try to create secret, if it exists, update it
    try {
        aws secretsmanager create-secret `
            --name "edweavepack/cognito" `
            --description "EdweavePack Cognito configuration" `
            --secret-string $secretValue `
            --region $Region
    }
    catch {
        aws secretsmanager update-secret `
            --secret-id "edweavepack/cognito" `
            --secret-string $secretValue `
            --region $Region
    }

    Write-Host "✅ Credentials stored in AWS Secrets Manager" -ForegroundColor Green

    # Generate JWKS URL
    $JwksUrl = "https://cognito-idp.$Region.amazonaws.com/$PoolId/.well-known/jwks.json"

    # Output configuration
    Write-Host ""
    Write-Host "🎉 Cognito Setup Complete!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "Pool ID: $PoolId" -ForegroundColor White
    Write-Host "Client ID: $ClientId" -ForegroundColor White
    Write-Host "Region: $Region" -ForegroundColor White
    Write-Host "JWKS URL: $JwksUrl" -ForegroundColor White
    Write-Host "Domain: https://$CognitoDomain" -ForegroundColor White
    Write-Host ""
    Write-Host "📝 Environment Variables for Backend:" -ForegroundColor Yellow
    Write-Host "COGNITO_POOL_ID=$PoolId"
    Write-Host "COGNITO_REGION=$Region"
    Write-Host "COGNITO_CLIENT_ID=$ClientId"
    Write-Host "COGNITO_JWKS_URL=$JwksUrl"
    Write-Host ""
    Write-Host "🔗 Test JWKS endpoint:" -ForegroundColor Yellow
    Write-Host "Invoke-WebRequest -Uri '$JwksUrl'"

    # Create .env file with values
    $envContent = @"
COGNITO_POOL_ID=$PoolId
COGNITO_REGION=$Region
COGNITO_CLIENT_ID=$ClientId
COGNITO_JWKS_URL=$JwksUrl
"@
    
    $envContent | Out-File -FilePath "backend\.env.cognito" -Encoding UTF8
    Write-Host ""
    Write-Host "✅ Environment variables saved to backend\.env.cognito" -ForegroundColor Green
    Write-Host "   Copy these values to your backend\.env file" -ForegroundColor Yellow

}
catch {
    Write-Host "❌ Error during Cognito setup: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}