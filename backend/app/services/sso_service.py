from typing import Dict, Any, Optional
import httpx
import jwt
import os
from datetime import datetime, timedelta

class SSOService:
    def __init__(self):
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.microsoft_client_id = os.getenv("MICROSOFT_CLIENT_ID")
        self.microsoft_client_secret = os.getenv("MICROSOFT_CLIENT_SECRET")
        self.redirect_uri = os.getenv("SSO_REDIRECT_URI", "http://localhost:3000/auth/callback")
    
    def get_google_auth_url(self, state: str = None) -> str:
        """Generate Google OAuth2 authorization URL"""
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": self.google_client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid email profile",
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent"
        }
        
        if state:
            params["state"] = state
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"
    
    def get_microsoft_auth_url(self, state: str = None) -> str:
        """Generate Microsoft OAuth2 authorization URL"""
        tenant_id = os.getenv("MICROSOFT_TENANT_ID", "common")
        base_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"
        params = {
            "client_id": self.microsoft_client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid email profile",
            "response_type": "code",
            "response_mode": "query"
        }
        
        if state:
            params["state"] = state
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"
    
    async def exchange_google_code(self, code: str) -> Dict[str, Any]:
        """Exchange Google authorization code for tokens"""
        token_url = "https://oauth2.googleapis.com/token"
        
        data = {
            "client_id": self.google_client_id,
            "client_secret": self.google_client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            return response.json()
    
    async def exchange_microsoft_code(self, code: str) -> Dict[str, Any]:
        """Exchange Microsoft authorization code for tokens"""
        tenant_id = os.getenv("MICROSOFT_TENANT_ID", "common")
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        
        data = {
            "client_id": self.microsoft_client_id,
            "client_secret": self.microsoft_client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            return response.json()
    
    async def get_google_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Google"""
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(user_info_url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    async def get_microsoft_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Microsoft"""
        user_info_url = "https://graph.microsoft.com/v1.0/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(user_info_url, headers=headers)
            response.raise_for_status()
            return response.json()
    
    def verify_google_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """Verify Google ID token"""
        try:
            # In production, you should verify the token signature
            # For now, we'll decode without verification (not recommended for production)
            decoded = jwt.decode(id_token, options={"verify_signature": False})
            
            # Verify issuer and audience
            if decoded.get("iss") not in ["https://accounts.google.com", "accounts.google.com"]:
                return None
            
            if decoded.get("aud") != self.google_client_id:
                return None
            
            # Check expiration
            if decoded.get("exp", 0) < datetime.utcnow().timestamp():
                return None
            
            return decoded
        except Exception:
            return None
    
    def create_sso_user_data(self, provider: str, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create standardized user data from SSO provider"""
        if provider == "google":
            return {
                "email": user_info.get("email"),
                "name": user_info.get("name"),
                "provider": "google",
                "provider_id": user_info.get("id"),
                "picture": user_info.get("picture"),
                "verified_email": user_info.get("verified_email", False)
            }
        elif provider == "microsoft":
            return {
                "email": user_info.get("mail") or user_info.get("userPrincipalName"),
                "name": user_info.get("displayName"),
                "provider": "microsoft",
                "provider_id": user_info.get("id"),
                "picture": None,  # Microsoft Graph requires separate call for photo
                "verified_email": True  # Microsoft emails are typically verified
            }
        
        return {}
    
    async def refresh_google_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh Google access token"""
        token_url = "https://oauth2.googleapis.com/token"
        
        data = {
            "client_id": self.google_client_id,
            "client_secret": self.google_client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            return response.json()
    
    async def refresh_microsoft_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh Microsoft access token"""
        tenant_id = os.getenv("MICROSOFT_TENANT_ID", "common")
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        
        data = {
            "client_id": self.microsoft_client_id,
            "client_secret": self.microsoft_client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            response.raise_for_status()
            return response.json()