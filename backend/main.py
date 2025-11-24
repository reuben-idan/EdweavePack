from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import auth, curriculum, assessment, analytics, learning_paths, curriculum_enhanced, auth_enhanced, files, tasks, agents, student_endpoints
from app.core.database import engine
from app.models import Base
import logging
import traceback
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Edweave Pack API", version="1.0.0")

# Enhanced CORS configuration for production
allowed_origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://edweavepack.com",
    "https://www.edweavepack.com",
    "https://*.edweavepack.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Global exception handler (debug mode)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Global exception handler caught: {exc}")
    logger.error(f"Exception type: {type(exc)}")
    logger.error(f"Traceback: {traceback.format_exc()}")
    
    # Return detailed error for debugging
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Internal server error: {str(exc)}",
            "type": "internal_server_error",
            "exception_type": str(type(exc))
        }
    )

# HTTP exception handler for better error responses (temporarily disabled)
# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     """Handle HTTP exceptions with consistent format"""
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "detail": exc.detail,
#             "type": "http_exception",
#             "status_code": exc.status_code
#         }
#     )

# Create tables
try:
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully")
except Exception as e:
    logger.error(f"❌ Error creating database tables: {e}")
    raise

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(auth_enhanced.router, prefix="/api/auth/sso", tags=["sso"])
app.include_router(files.router, prefix="/api/files", tags=["files"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(curriculum.router, prefix="/api/curriculum", tags=["curriculum"])
app.include_router(curriculum_enhanced.router, prefix="/api/curriculum/enhanced", tags=["curriculum-enhanced"])
app.include_router(assessment.router, prefix="/api/assessment", tags=["assessment"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(learning_paths.router, prefix="/api/learning-paths", tags=["learning-paths"])
app.include_router(student_endpoints.router, prefix="/api", tags=["students"])
app.include_router(agents.router, tags=["agents"])

@app.get("/")
async def root():
    return {"message": "Edweave Pack API"}

@app.get("/health")
async def health_check():
    """Health check endpoint with database connectivity test"""
    try:
        # Test database connection
        from app.core.database import get_db
        from sqlalchemy import text
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "database": "disconnected",
                "error": "Database connection failed"
            }
        )