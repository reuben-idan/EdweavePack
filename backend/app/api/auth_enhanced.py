from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import UserResponse, Token
from app.api.auth import create_access_token, get_password_hash
from app.services.sso_service import SSOService

router = APIRouter()
sso_service = SSOService()

@router.get("/google/url")
async def get_google_auth_url(state: str = Query(None)):
    """Get Google OAuth2 authorization URL"""
    auth_url = sso_service.get_google_auth_url(state)
    return {"auth_url": auth_url}

@router.get("/microsoft/url")
async def get_microsoft_auth_url(state: str = Query(None)):
    """Get Microsoft OAuth2 authorization URL"""
    auth_url = sso_service.get_microsoft_auth_url(state)
    return {"auth_url": auth_url}

@router.post("/google/callback")
async def google_callback(
    code: str,
    db: Session = Depends(get_db)
):
    """Handle Google OAuth2 callback"""
    try:
        # Exchange code for tokens
        token_data = await sso_service.exchange_google_code(code)
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token")
        
        # Get user info from Google
        user_info = await sso_service.get_google_user_info(access_token)
        sso_user_data = sso_service.create_sso_user_data("google", user_info)
        
        # Check if user exists
        existing_user = db.query(User).filter(User.email == sso_user_data["email"]).first()
        
        if existing_user:
            # Update existing user
            user = existing_user
        else:
            # Create new user
            user = User(
                email=sso_user_data["email"],
                name=sso_user_data["name"],
                hashed_password=get_password_hash("sso_user"),  # Placeholder password
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create JWT token
        jwt_token = create_access_token(data={"sub": user.email})
        
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "provider": "google"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@router.post("/microsoft/callback")
async def microsoft_callback(
    code: str,
    db: Session = Depends(get_db)
):
    """Handle Microsoft OAuth2 callback"""
    try:
        # Exchange code for tokens
        token_data = await sso_service.exchange_microsoft_code(code)
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token")
        
        # Get user info from Microsoft
        user_info = await sso_service.get_microsoft_user_info(access_token)
        sso_user_data = sso_service.create_sso_user_data("microsoft", user_info)
        
        # Check if user exists
        existing_user = db.query(User).filter(User.email == sso_user_data["email"]).first()
        
        if existing_user:
            # Update existing user
            user = existing_user
        else:
            # Create new user
            user = User(
                email=sso_user_data["email"],
                name=sso_user_data["name"],
                hashed_password=get_password_hash("sso_user"),  # Placeholder password
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create JWT token
        jwt_token = create_access_token(data={"sub": user.email})
        
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "provider": "microsoft"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")

@router.get("/providers")
async def get_auth_providers():
    """Get available authentication providers"""
    return {
        "providers": [
            {
                "name": "google",
                "display_name": "Google",
                "enabled": bool(sso_service.google_client_id)
            },
            {
                "name": "microsoft",
                "display_name": "Microsoft",
                "enabled": bool(sso_service.microsoft_client_id)
            },
            {
                "name": "email",
                "display_name": "Email & Password",
                "enabled": True
            }
        ]
    }