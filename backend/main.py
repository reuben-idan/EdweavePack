from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from contextlib import asynccontextmanager

# Import routers
from app.api.auth import router as auth_router
from app.api.curriculum import router as curriculum_router
from app.api.assessment import router as assessment_router
from app.api.files import router as files_router
from app.api.analytics import router as analytics_router
from app.api.agents import router as agents_router
from app.api.learning_paths import router as learning_paths_router
from app.api.ai_enhanced import router as ai_enhanced_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 EdweavePack API starting up...")
    logger.info("🤖 Amazon Q Developer integration enabled")
    logger.info("🧠 AWS AI services initialized")
    
    # Create database tables
    try:
        from app.core.database import Base, engine
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    yield
    # Shutdown
    logger.info("🛑 EdweavePack API shutting down...")

# Create FastAPI app
app = FastAPI(
    title="EdweavePack AI-Enhanced API",
    description="AI-Powered Educational Content Platform with comprehensive AWS AI integration",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com",
        "https://edweavepack-prod-alb-2084837426.eu-north-1.elb.amazonaws.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://localhost:8003"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for load balancer"""
    return {
        "status": "healthy",
        "service": "EdweavePack AI-Enhanced API",
        "version": "3.0.0",
        "ai_services": {
            "bedrock": "enabled",
            "textract": "enabled", 
            "comprehend": "enabled",
            "polly": "enabled",
            "translate": "enabled",
            "q_assistant": "enabled"
        },
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to EdweavePack AI-Enhanced API",
        "version": "3.0.0",
        "docs": "/docs",
        "health": "/health",
        "ai_powered": True,
        "aws_ai_integration": {
            "bedrock": "Curriculum & Assessment Generation",
            "textract": "Document Analysis",
            "comprehend": "Content Understanding",
            "polly": "Text-to-Speech",
            "translate": "Multi-language Support",
            "q_assistant": "In-app AI Assistant"
        }
    }

# Include routers with proper prefixes
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(curriculum_router, prefix="/api/curriculum", tags=["Curriculum"])
app.include_router(assessment_router, prefix="/api/assessment", tags=["Assessment"])
app.include_router(files_router, prefix="/api/files", tags=["Files"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(agents_router, prefix="/api/agents", tags=["AI Agents"])
app.include_router(learning_paths_router, prefix="/api/learning-paths", tags=["Learning Paths"])
app.include_router(ai_enhanced_router, prefix="/api/ai", tags=["AI Services"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

# 404 handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Not found",
            "message": "The requested resource was not found"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("ENVIRONMENT") == "development"
    )