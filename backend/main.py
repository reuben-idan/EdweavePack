from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, curriculum, assessment, analytics, learning_paths
from app.core.database import engine
from app.models import Base

app = FastAPI(title="Edweave Pack API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(curriculum.router, prefix="/api/curriculum", tags=["curriculum"])
app.include_router(assessment.router, prefix="/api/assessment", tags=["assessment"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(learning_paths.router, prefix="/api/learning-paths", tags=["learning-paths"])

@app.get("/")
async def root():
    return {"message": "Edweave Pack API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}