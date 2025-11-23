from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json

from app.core.database import get_db
from app.models.student import Student
from app.core.database import get_db

router = APIRouter(prefix="/student", tags=["student"])

@router.get("/dashboard")
async def get_student_dashboard(db: Session = Depends(get_db)):
    return {"message": "Student dashboard", "data": {}}

