#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate
from app.api.auth import get_password_hash, create_access_token
from datetime import timedelta
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/test-register")
async def test_register(user: UserCreate, db: Session = Depends(get_db)):
    """Test registration endpoint with detailed error reporting"""
    try:
        print(f"Test registration for: {user.email}")
        
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
        
        # Create token
        access_token = create_access_token(
            data={"sub": db_user.email}, 
            expires_delta=timedelta(minutes=30)
        )
        
        return {"access_token": access_token, "token_type": "bearer", "message": "SUCCESS"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Detailed error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)