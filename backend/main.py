from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, curriculum, assessment, analytics, learning_paths, curriculum_enhanced, auth_enhanced, files, tasks, agents
from app.core.database import engine
from app.models import Base
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Edweave Pack API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(agents.router, tags=["agents"])

@app.get("/")
async def root():
    return {"message": "Edweave Pack API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}