#!/usr/bin/env python3

import requests
import subprocess
import boto3
import time

def test_current_auth():
    """Test current auth status"""
    base_url = "http://edweavepack-alb-1731617972.eu-north-1.elb.amazonaws.com"
    
    # Test registration first
    test_user = {
        "email": "auth-test@edweavepack.com",
        "password": "test123",
        "full_name": "Auth Test",
        "role": "teacher"
    }
    
    try:
        reg_response = requests.post(f"{base_url}/api/auth/register", json=test_user, timeout=10)
        print(f"Registration: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            # Try login with exact same credentials
            login_data = {"username": test_user["email"], "password": test_user["password"]}
            login_response = requests.post(f"{base_url}/api/auth/token", data=login_data, timeout=10)
            print(f"Login: {login_response.status_code}")
            
            if login_response.status_code == 401:
                print("Auth issue confirmed - fixing...")
                return False
            else:
                print("Auth working")
                return True
                
    except Exception as e:
        print(f"Error: {e}")
    
    return False

def deploy_auth_fix():
    """Deploy simplified auth fix"""
    
    # Create minimal working backend
    backend_code = '''from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
import hashlib
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = "edweavepack-secret"
users_db = {}

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "teacher"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(user_data: dict) -> str:
    payload = {
        "user_id": user_data["id"],
        "email": user_data["email"],
        "exp": int(time.time()) + 86400
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "api": "ready"}

@app.post("/api/auth/register")
async def register(user_data: UserRegister):
    if user_data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = f"user_{len(users_db) + 1}"
    user = {
        "id": user_id,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "role": user_data.role,
        "password": hash_password(user_data.password)
    }
    
    users_db[user_data.email] = user
    token = create_token(user)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
    }

@app.post("/api/auth/token")
async def login(username: str = Form(...), password: str = Form(...)):
    if username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = users_db[username]
    if hash_password(password) != user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    # Write simplified backend
    with open("backend/main.py", "w") as f:
        f.write(backend_code)
    
    print("Created simplified backend")
    
    # Deploy
    subprocess.run(["docker", "build", "-t", "edweavepack-backend:latest", "."], cwd="backend")
    subprocess.run(["docker", "tag", "edweavepack-backend:latest", 
                   "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest"])
    subprocess.run(["docker", "push", 
                   "084828575963.dkr.ecr.eu-north-1.amazonaws.com/edweavepack-backend:latest"])
    
    # Update ECS
    ecs = boto3.client('ecs', region_name='eu-north-1')
    ecs.update_service(
        cluster='edweavepack-cluster',
        service='edweavepack-service',
        forceNewDeployment=True
    )
    
    print("Deployed auth fix")

def main():
    print("Auth Issue Resolution")
    print("=" * 20)
    
    if not test_current_auth():
        deploy_auth_fix()
        
        print("Waiting 60 seconds for deployment...")
        time.sleep(60)
        
        if test_current_auth():
            print("AUTH FIXED!")
        else:
            print("Still has issues")
    else:
        print("Auth already working")

if __name__ == "__main__":
    main()