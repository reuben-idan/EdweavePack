from jose import jwt
import requests
import os
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import json

security = HTTPBearer()

class CognitoJWTValidator:
    def __init__(self):
        self.pool_id = os.getenv("COGNITO_POOL_ID")
        self.region = os.getenv("COGNITO_REGION", "us-east-1")
        self.client_id = os.getenv("COGNITO_CLIENT_ID")
        self.jwks_url = os.getenv("COGNITO_JWKS_URL") or f"https://cognito-idp.{self.region}.amazonaws.com/{self.pool_id}/.well-known/jwks.json"
        self._jwks = None
        
        # Validate required environment variables
        if not self.pool_id or not self.client_id:
            raise ValueError("COGNITO_POOL_ID and COGNITO_CLIENT_ID must be set")
    
    def get_jwks(self):
        if not self._jwks:
            try:
                response = requests.get(self.jwks_url, timeout=10)
                response.raise_for_status()
                self._jwks = response.json()
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Unable to fetch JWKS: {str(e)}"
                )
        return self._jwks
    
    def verify_token(self, token: str) -> dict:
        try:
            # Get token header
            header = jwt.get_unverified_header(token)
            kid = header.get('kid')
            
            if not kid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token missing kid in header"
                )
            
            # Find matching key
            jwks = self.get_jwks()
            key = None
            for k in jwks['keys']:
                if k['kid'] == kid:
                    key = k
                    break
            
            if not key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unable to find matching key"
                )
            
            # Verify token
            claims = jwt.decode(
                token,
                key,
                algorithms=[key['alg']],
                audience=self.client_id,
                issuer=f"https://cognito-idp.{self.region}.amazonaws.com/{self.pool_id}"
            )
            
            return claims
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTClaimsError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token validation failed: {str(e)}"
            )
    
    def test_jwks_connection(self) -> bool:
        """Test if JWKS endpoint is accessible"""
        try:
            response = requests.get(self.jwks_url, timeout=5)
            response.raise_for_status()
            return True
        except Exception:
            return False

# Global validator instance
cognito_validator = CognitoJWTValidator()

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify Cognito JWT token and return claims"""
    return cognito_validator.verify_token(credentials.credentials)

def get_current_user(claims: dict = Depends(verify_jwt)) -> dict:
    """Extract user information from JWT claims"""
    return {
        "user_id": claims.get("sub"),
        "email": claims.get("email"),
        "name": claims.get("name"),
        "email_verified": claims.get("email_verified", False)
    }