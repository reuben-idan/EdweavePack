from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse, Token, ForgotPasswordRequest, ResetPasswordRequest, UpdateProfileRequest, UpdatePasswordRequest
import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # Truncate password to 72 bytes for bcrypt compatibility
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"Registration attempt for: {user.email}")
        
        # Basic validation
        if not user.email or not user.email.strip():
            raise HTTPException(status_code=400, detail="Email is required")
        
        if not user.password or len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        
        if not user.full_name or not user.full_name.strip():
            raise HTTPException(status_code=400, detail="Full name is required")
        
        # Clean email
        email = user.email.strip().lower()
        
        # Check existing user
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        db_user = User(
            email=email,
            name=user.full_name.strip(),
            hashed_password=get_password_hash(user.password),
            institution=user.institution or "Not specified",
            role=user.role or "teacher",
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        print(f"User created: {db_user.email}")
        
        # Create token
        access_token = create_access_token(
            data={"sub": db_user.email}, 
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException as he:
        print(f"HTTP Exception: {he.detail}")
        raise he
    except Exception as e:
        print(f"Registration error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        if 'db' in locals() and db:
            try:
                db.rollback()
            except:
                pass
        raise HTTPException(
            status_code=500, 
            detail=f"UPDATED_CODE: Registration failed: {str(e)} (Type: {type(e).__name__})"
        )

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == form_data.username).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is disabled",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again."
        )

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "full_name": current_user.name,
        "is_active": current_user.is_active,
        "institution": current_user.institution,
        "role": current_user.role
    }

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    print(f"Password reset requested for: {request.email}")
    
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        print(f"User not found: {request.email}")
        # Don't reveal if email exists
        return {"message": "If email exists, reset link has been sent"}
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    reset_expires = datetime.utcnow() + timedelta(hours=1)
    
    user.reset_token = reset_token
    user.reset_token_expires = reset_expires
    
    try:
        db.commit()
        print(f"Reset token saved for user: {user.email}")
    except Exception as e:
        print(f"Database error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
    
    # Send email
    try:
        send_reset_email(user.email, user.name, reset_token)
        print(f"Reset process completed for: {user.email}")
    except Exception as e:
        print(f"Email sending failed: {e}")
    
    return {"message": "If email exists, reset link has been sent"}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    print(f"Password reset attempt with token: {request.token[:10]}...")
    
    user = db.query(User).filter(
        User.reset_token == request.token,
        User.reset_token_expires > datetime.utcnow()
    ).first()
    
    if not user:
        print(f"Invalid or expired token: {request.token[:10]}...")
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    try:
        # Update password
        user.hashed_password = get_password_hash(request.password)
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()
        
        print(f"Password reset successful for user: {user.email}")
        return {"message": "Password reset successfully"}
    except Exception as e:
        print(f"Password reset error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to reset password")

@router.put("/profile")
async def update_profile(request: UpdateProfileRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Check if email is already taken by another user
        if request.email != current_user.email:
            existing_user = db.query(User).filter(User.email == request.email, User.id != current_user.id).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already in use")
        
        # Update user data
        current_user.name = request.fullName
        current_user.email = request.email
        current_user.institution = request.institution
        
        db.commit()
        db.refresh(current_user)
        
        print(f"Profile updated for user {current_user.id}: {current_user.name}, {current_user.email}")
        
        return {
            "message": "Profile updated successfully",
            "user": {
                "id": current_user.id,
                "name": current_user.name,
                "full_name": current_user.name,
                "email": current_user.email,
                "institution": current_user.institution,
                "role": current_user.role,
                "is_active": current_user.is_active
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Profile update error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")

@router.put("/password")
async def update_password(request: UpdatePasswordRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Verify current password
        if not verify_password(request.current_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        
        # Update password
        current_user.hashed_password = get_password_hash(request.new_password)
        db.commit()
        
        print(f"Password updated for user {current_user.id}")
        
        return {"message": "Password updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Password update error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update password: {str(e)}")

def send_reset_email(email: str, name: str, token: str):
    """Send password reset email"""
    email_enabled = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
    reset_url = f"http://localhost:3000/reset-password/{token}"
    
    if not email_enabled:
        print(f"\n=== PASSWORD RESET LINK (Email disabled) ===")
        print(f"User: {name} ({email})")
        print(f"Reset URL: {reset_url}")
        print(f"Token: {token}")
        print(f"=========================================\n")
        return
    
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    if not smtp_username or not smtp_password:
        print(f"\n=== PASSWORD RESET LINK (SMTP not configured) ===")
        print(f"User: {name} ({email})")
        print(f"Reset URL: {reset_url}")
        print(f"=========================================\n")
        return
    
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = email
    msg['Subject'] = "EdweavePack - Password Reset Request"
    
    body = f"""Hi {name},

You requested a password reset for your EdweavePack account.

Click the link below to reset your password:
{reset_url}

This link will expire in 1 hour.

If you didn't request this reset, please ignore this email.

Best regards,
EdweavePack Team"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        print(f"Reset email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        print(f"\n=== PASSWORD RESET LINK (Email failed) ===")
        print(f"User: {name} ({email})")
        print(f"Reset URL: {reset_url}")
        print(f"=========================================\n")