import sys
sys.path.append('.')

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db, engine, Base
from app.models.user import User
from app.schemas.auth import UserCreate, Token
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import traceback

# Create FastAPI app
app = FastAPI(title="Test Registration API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "test-secret", algorithm="HS256")

@app.post("/api/auth/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"Registration request: {user}")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Validate
        if not user.email or len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Invalid input")
        
        # Check existing user
        existing = db.query(User).filter(User.email == user.email.lower()).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        db_user = User(
            email=user.email.lower(),
            name=user.full_name,
            hashed_password=get_password_hash(user.password),
            institution=user.institution or "Not specified",
            role=user.role,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Create token
        token = create_access_token({"sub": db_user.email})
        
        print(f"User registered successfully: {db_user.email}")
        return {"access_token": token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Test server running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)