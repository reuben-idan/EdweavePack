#!/bin/bash

# AWS Cognito Setup Script for EdweavePack
# This script creates the Cognito User Pool and App Client

set -e

# Configuration
POOL_NAME="edweavepack-userpool"
CLIENT_NAME="edweavepack-web"
REGION="us-east-1"
DOMAIN_PREFIX="edweavepack-$(date +%s)"

echo "🚀 Setting up AWS Cognito for EdweavePack..."

# 1. Create Cognito User Pool
echo "📝 Creating Cognito User Pool: $POOL_NAME"
POOL_ID=$(aws cognito-idp create-user-pool \
  --pool-name "$POOL_NAME" \
  --policies PasswordPolicy='{MinimumLength=8,RequireUppercase=true,RequireLowercase=true,RequireNumbers=true,RequireSymbols=true}' \
  --auto-verified-attributes email \
  --schema '[
    {
      "Name": "email",
      "AttributeDataType": "String",
      "Required": true,
      "Mutable": true
    },
    {
      "Name": "name",
      "AttributeDataType": "String", 
      "Required": true,
      "Mutable": true
    }
  ]' \
  --verification-message-template DefaultEmailOption=CONFIRM_WITH_CODE \
  --region "$REGION" \
  --query 'UserPool.Id' \
  --output text)

echo "✅ User Pool created with ID: $POOL_ID"

# 2. Create App Client
echo "📱 Creating App Client: $CLIENT_NAME"
CLIENT_ID=$(aws cognito-idp create-user-pool-client \
  --user-pool-id "$POOL_ID" \
  --client-name "$CLIENT_NAME" \
  --generate-secret \
  --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH ALLOW_USER_SRP_AUTH \
  --supported-identity-providers COGNITO \
  --callback-urls '["https://localhost:3000/callback","http://localhost:3000/callback"]' \
  --logout-urls '["https://localhost:3000/","http://localhost:3000/"]' \
  --allowed-o-auth-flows code \
  --allowed-o-auth-scopes openid email profile \
  --allowed-o-auth-flows-user-pool-client \
  --region "$REGION" \
  --query 'UserPoolClient.ClientId' \
  --output text)

echo "✅ App Client created with ID: $CLIENT_ID"

# 3. Create Cognito Domain
echo "🌐 Creating Cognito Domain: $DOMAIN_PREFIX"
aws cognito-idp create-user-pool-domain \
  --domain "$DOMAIN_PREFIX" \
  --user-pool-id "$POOL_ID" \
  --region "$REGION"

echo "✅ Domain created: https://$DOMAIN_PREFIX.auth.$REGION.amazoncognito.com"

# 4. Get Client Secret
CLIENT_SECRET=$(aws cognito-idp describe-user-pool-client \
  --user-pool-id "$POOL_ID" \
  --client-id "$CLIENT_ID" \
  --region "$REGION" \
  --query 'UserPoolClient.ClientSecret' \
  --output text)

# 5. Create/Update AWS Secrets Manager secret
echo "🔐 Storing credentials in AWS Secrets Manager..."
aws secretsmanager create-secret \
  --name "edweavepack/cognito" \
  --description "EdweavePack Cognito configuration" \
  --secret-string "{
    \"COGNITO_POOL_ID\": \"$POOL_ID\",
    \"COGNITO_REGION\": \"$REGION\",
    \"COGNITO_CLIENT_ID\": \"$CLIENT_ID\",
    \"COGNITO_CLIENT_SECRET\": \"$CLIENT_SECRET\",
    \"COGNITO_DOMAIN\": \"$DOMAIN_PREFIX.auth.$REGION.amazoncognito.com\",
    \"COGNITO_JWKS_URL\": \"https://cognito-idp.$REGION.amazonaws.com/$POOL_ID/.well-known/jwks.json\"
  }" \
  --region "$REGION" 2>/dev/null || \

aws secretsmanager update-secret \
  --secret-id "edweavepack/cognito" \
  --secret-string "{
    \"COGNITO_POOL_ID\": \"$POOL_ID\",
    \"COGNITO_REGION\": \"$REGION\",
    \"COGNITO_CLIENT_ID\": \"$CLIENT_ID\",
    \"COGNITO_CLIENT_SECRET\": \"$CLIENT_SECRET\",
    \"COGNITO_DOMAIN\": \"$DOMAIN_PREFIX.auth.$REGION.amazoncognito.com\",
    \"COGNITO_JWKS_URL\": \"https://cognito-idp.$REGION.amazonaws.com/$POOL_ID/.well-known/jwks.json\"
  }" \
  --region "$REGION"

echo "✅ Credentials stored in AWS Secrets Manager"

# 6. Generate JWKS URL
JWKS_URL="https://cognito-idp.$REGION.amazonaws.com/$POOL_ID/.well-known/jwks.json"

# Output configuration
echo ""
echo "🎉 Cognito Setup Complete!"
echo "================================"
echo "Pool ID: $POOL_ID"
echo "Client ID: $CLIENT_ID"
echo "Region: $REGION"
echo "JWKS URL: $JWKS_URL"
echo "Domain: https://$DOMAIN_PREFIX.auth.$REGION.amazoncognito.com"
echo ""
echo "📝 Environment Variables for Backend:"
echo "COGNITO_POOL_ID=$POOL_ID"
echo "COGNITO_REGION=$REGION"
echo "COGNITO_CLIENT_ID=$CLIENT_ID"
echo "COGNITO_JWKS_URL=$JWKS_URL"
echo ""
echo "🔗 Test JWKS endpoint:"
echo "curl $JWKS_URL"