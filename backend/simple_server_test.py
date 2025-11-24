#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.core.database import engine
from app.models import Base
import uvicorn

# Create a simple app for testing
app = FastAPI(title="Test API")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include auth router
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Test API"}

if __name__ == "__main__":
    print("Starting test server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")