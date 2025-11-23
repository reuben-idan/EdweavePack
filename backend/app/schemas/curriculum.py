from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class CurriculumCreate(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    grade_level: str
    source_content: str

class CurriculumResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    subject: str
    grade_level: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class LearningPathResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    sequence_order: int
    content: Dict[str, Any]
    estimated_duration: Optional[int]
    
    class Config:
        from_attributes = True

class AssessmentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    assessment_type: str
    total_points: int
    time_limit: Optional[int]
    
    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    options: Optional[Dict[str, Any]]
    points: int
    
    class Config:
        from_attributes = True