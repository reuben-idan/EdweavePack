# AWS Cognito Setup Guide for EdweavePack

This guide walks you through setting up AWS Cognito as the authentication provider for EdweavePack.

## Prerequisites

- AWS CLI installed and configured with appropriate permissions
- AWS account with Cognito access
- PowerShell (Windows) or Bash (Unix/Linux/macOS)

## Quick Setup

### Option 1: Automated Setup (Recommended)

**Windows (PowerShell):**
```powershell
.\setup-cognito.ps1
```

**Unix/Linux/macOS (Bash):**
```bash
chmod +x setup-cognito.sh
./setup-cognito.sh
```

### Option 2: Manual Setup

1. **Create User Pool:**
```bash
aws cognito-idp create-user-pool \
  --pool-name "edweavepack-userpool" \
  --policies PasswordPolicy='{MinimumLength=8,RequireUppercase=true,RequireLowercase=true,RequireNumbers=true,RequireSymbols=true}' \
  --auto-verified-attributes email \
  --region us-east-1
```

2. **Create App Client:**
```bash
aws cognito-idp create-user-pool-client \
  --user-pool-id YOUR_POOL_ID \
  --client-name "edweavepack-web" \
  --generate-secret \
  --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH ALLOW_USER_SRP_AUTH \
  --region us-east-1
```

## Configuration

### Environment Variables

Add these to your `backend/.env` file:

```env
# AWS Cognito Authentication
COGNITO_POOL_ID=your_pool_id_here
COGNITO_REGION=us-east-1
COGNITO_CLIENT_ID=your_client_id_here
COGNITO_JWKS_URL=https://cognito-idp.us-east-1.amazonaws.com/YOUR_POOL_ID/.well-known/jwks.json
```

### Docker Compose

The `docker-compose.yml` has been updated to include Cognito environment variables. Make sure to set them in your environment or `.env` file.

### ECS Task Definition

For AWS ECS deployment, add these environment variables to your task definition:

```json
{
  "environment": [
    {
      "name": "COGNITO_POOL_ID",
      "value": "your_pool_id"
    },
    {
      "name": "COGNITO_REGION", 
      "value": "us-east-1"
    },
    {
      "name": "COGNITO_CLIENT_ID",
      "value": "your_client_id"
    },
    {
      "name": "COGNITO_JWKS_URL",
      "value": "https://cognito-idp.us-east-1.amazonaws.com/YOUR_POOL_ID/.well-known/jwks.json"
    }
  ]
}
```

## Validation

Run the validation script to test your setup:

```bash
python validate-cognito.py
```

Expected output:
```
🚀 EdweavePack Cognito Validation
========================================
✅ COGNITO_POOL_ID: us-east-1_XXXXXXXXX
✅ COGNITO_CLIENT_ID: xxxxxxxxxxxxxxxxxx
✅ COGNITO_REGION: us-east-1

🔍 Testing JWKS endpoint: https://cognito-idp.us-east-1.amazonaws.com/...
✅ JWKS endpoint accessible
📊 Found 2 signing keys

🧪 Testing Cognito JWT validator...
✅ CognitoJWTValidator initialized successfully
✅ JWKS connection test passed

🎉 All Cognito validation tests passed!
```

## Usage in FastAPI

The JWT validation is automatically handled by the `CognitoJWTValidator` class:

```python
from fastapi import Depends
from auth.cognito import get_current_user

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['name']}", "user_id": user['user_id']}
```

## Testing JWT Validation

### Manual Token Test

1. **Get a test token from Cognito:**
```bash
aws cognito-idp admin-initiate-auth \
  --user-pool-id YOUR_POOL_ID \
  --client-id YOUR_CLIENT_ID \
  --auth-flow ADMIN_NO_SRP_AUTH \
  --auth-parameters USERNAME=test@example.com,PASSWORD=TempPassword123!
```

2. **Test with curl:**
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/api/protected-endpoint
```

### JWKS Endpoint Test

Verify the JWKS endpoint is accessible:

```bash
curl https://cognito-idp.us-east-1.amazonaws.com/YOUR_POOL_ID/.well-known/jwks.json
```

Expected response:
```json
{
  "keys": [
    {
      "alg": "RS256",
      "e": "AQAB",
      "kid": "...",
      "kty": "RSA",
      "n": "...",
      "use": "sig"
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **"Unable to fetch JWKS" error:**
   - Check internet connectivity
   - Verify COGNITO_POOL_ID and COGNITO_REGION are correct
   - Ensure the User Pool exists in the specified region

2. **"Token validation failed" error:**
   - Verify the token is not expired
   - Check that COGNITO_CLIENT_ID matches the token's audience
   - Ensure the token was issued by the correct User Pool

3. **Environment variables not loaded:**
   - Check `.env` file exists in backend directory
   - Verify environment variables are set correctly
   - Restart the application after changing environment variables

### Debug Mode

Enable debug logging in your FastAPI application:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

- Store sensitive values (Client Secret) in AWS Secrets Manager
- Use HTTPS in production
- Implement proper CORS policies
- Regularly rotate secrets
- Monitor authentication logs

## Production Deployment

For production deployment:

1. **Use AWS Secrets Manager:**
```bash
aws secretsmanager get-secret-value \
  --secret-id edweavepack/cognito \
  --query SecretString --output text
```

2. **Update callback URLs:**
   - Replace localhost URLs with your production domain
   - Update both callback and logout URLs

3. **Configure custom domain:**
   - Set up a custom domain for Cognito Hosted UI
   - Update DNS records as required

## Support

- **Validation Script:** `python validate-cognito.py`
- **AWS Documentation:** [Cognito Developer Guide](https://docs.aws.amazon.com/cognito/)
- **FastAPI JWT:** [python-jose documentation](https://python-jose.readthedocs.io/)

---

**Output from Setup:**
- Pool ID: `us-east-1_XXXXXXXXX`
- Client ID: `xxxxxxxxxxxxxxxxxx`
- JWKS URL: `https://cognito-idp.us-east-1.amazonaws.com/us-east-1_XXXXXXXXX/.well-known/jwks.json`