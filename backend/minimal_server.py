import sys
sys.path.append('.')

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# Import database and models
from app.core.database import get_db, engine, Base
from app.models.user import User

# Create app
app = FastAPI()

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

# Schemas
class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str
    institution: str = None
    role: str = "teacher"

class Token(BaseModel):
    access_token: str
    token_type: str

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, "test-secret", algorithm="HS256")

@app.post("/api/auth/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"Registration request: {user.email}")
        
        # Create tables if needed
        Base.metadata.create_all(bind=engine)
        
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
        
        print(f"User registered: {db_user.email}")
        return {"access_token": token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Minimal server running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)