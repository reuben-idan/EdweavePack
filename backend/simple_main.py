from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
import jwt
import hashlib
import time
import json
from typing import Optional, Dict, Any

app = FastAPI(title="EdweavePack API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
JWT_SECRET = "edweavepack-hackathon-2025-secret"

# In-memory storage (for demo)
users_db = {}
curricula_db = {}
assessments_db = {}

# Models
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "teacher"

class UserLogin(BaseModel):
    email: str
    password: str

# Helper functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(user_data: dict) -> str:
    payload = {
        "user_id": user_data["id"],
        "email": user_data["email"],
        "role": user_data["role"],
        "exp": int(time.time()) + 86400  # 24 hours
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "EdweavePack", "version": "3.0.0"}

@app.get("/")
async def root():
    return {"message": "EdweavePack API", "status": "running"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "api": "ready"}

@app.post("/api/auth/register")
async def register(user_data: UserRegister):
    # Check if user exists
    if user_data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user_id = f"user_{len(users_db) + 1}"
    hashed_password = hash_password(user_data.password)
    
    user = {
        "id": user_id,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": user_data.role,
        "password": hashed_password
    }
    
    users_db[user_data.email] = user
    
    # Create token
    token = create_token(user)
    
    return {
        "message": "Registration successful",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        },
        "access_token": token,
        "token_type": "bearer"
    }

@app.post("/api/auth/token")
async def login(username: str = Form(...), password: str = Form(...)):
    # Check if user exists (username is email)
    if username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_found = users_db[username]
    
    # Verify password
    hashed_input = hash_password(password)
    stored_hash = user_found["password"]
    
    if hashed_input != stored_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    token = create_token(user_found)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_found["id"],
            "email": user_found["email"],
            "full_name": user_found["full_name"],
            "role": user_found["role"]
        }
    }

@app.get("/api/auth/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        email = payload.get("email")
        
        if email not in users_db:
            raise HTTPException(status_code=401, detail="User not found")
        
        user = users_db[email]
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/curriculum/")
async def get_curricula(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {"curricula": list(curricula_db.values()), "count": len(curricula_db)}

@app.post("/api/curriculum/")
async def create_curriculum(curriculum_data: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    curriculum_id = f"curr_{len(curricula_db) + 1}"
    
    curriculum = {
        "id": curriculum_id,
        "title": curriculum_data.get('title', 'AI-Generated Curriculum'),
        "subject": curriculum_data.get('subject', 'General'),
        "grade_level": curriculum_data.get('grade_level', 'K-12'),
        "ai_generated_content": "Sample AI-generated curriculum content",
        "created_at": time.time(),
        "aws_ai_enhanced": True
    }
    
    curricula_db[curriculum_id] = curriculum
    return curriculum

@app.post("/api/files/simple-upload")
async def upload_file(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {
        "filename": "uploaded_file.pdf",
        "content": "Sample extracted content",
        "full_content": "Full extracted content from uploaded file",
        "task_id": "task_123",
        "status": "completed"
    }

@app.get("/api/analytics/dashboard")
async def get_analytics_dashboard(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return {
        "platform_stats": {
            "total_students": len(users_db),
            "active_curricula": len(curricula_db),
            "assessments_created": len(assessments_db)
        },
        "ai_insights": "Sample AI insights for educational platform",
        "generated_at": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)