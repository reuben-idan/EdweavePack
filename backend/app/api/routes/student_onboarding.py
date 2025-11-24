from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.student import (
    StudentGoalCreate, StudentSubjectsCreate, 
    StudentAvailabilityCreate, StudentUploadCreate
)
from app.models.user import User
from app.core.auth import get_current_user
from app.services.s3_service import upload_file_to_s3
from app.tasks.learning_path import generate_learning_path
import json

router = APIRouter()

@router.post("/goals")
async def set_student_goals(
    goals: StudentGoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    metadata = current_user.metadata or {}
    metadata["goals"] = goals.dict()
    current_user.metadata = metadata
    db.commit()
    return {"message": "Goals saved successfully"}

@router.post("/subjects")
async def set_student_subjects(
    subjects: StudentSubjectsCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    metadata = current_user.metadata or {}
    metadata["subjects"] = subjects.subjects
    current_user.metadata = metadata
    db.commit()
    return {"message": "Subjects saved successfully"}

@router.post("/availability")
async def set_student_availability(
    availability: StudentAvailabilityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    metadata = current_user.metadata or {}
    metadata["availability"] = availability.dict()
    current_user.metadata = metadata
    db.commit()
    return {"message": "Availability saved successfully"}

@router.post("/uploads")
async def upload_study_materials(
    file: UploadFile = File(None),
    content_url: str = None,
    text_content: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    metadata = current_user.metadata or {}
    uploads = metadata.get("uploads", [])
    
    if file:
        file_url = await upload_file_to_s3(file, f"student-materials/{current_user.id}")
        uploads.append({"type": "file", "url": file_url, "name": file.filename})
    elif content_url:
        uploads.append({"type": "url", "url": content_url})
    elif text_content:
        uploads.append({"type": "text", "content": text_content})
    
    metadata["uploads"] = uploads
    current_user.metadata = metadata
    db.commit()
    return {"message": "Materials uploaded successfully"}

@router.post("/complete")
async def complete_onboarding(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    generate_learning_path.delay(current_user.id)
    
    metadata = current_user.metadata or {}
    metadata["onboarding_complete"] = True
    current_user.metadata = metadata
    db.commit()
    
    return {"message": "Onboarding completed, generating learning path..."}