from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

class StudentBase(BaseModel):
    email: EmailStr
    name: str
    age: Optional[int] = None
    learning_style: Optional[str] = None
    target_exams: Optional[List[str]] = []
    exam_date: Optional[datetime] = None

class StudentCreate(StudentBase):
    password: str

class StudentResponse(BaseModel):
    id: int
    email: str
    name: str
    age: Optional[int]
    learning_style: Optional[str]
    target_exams: Optional[List[str]]
    exam_date: Optional[datetime]
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class StudentGoalCreate(BaseModel):
    goals: str
    subject_focus: List[str]
    strengths: Optional[str] = None
    weaknesses: Optional[str] = None
    timeline: Optional[datetime] = None
    study_material_url: Optional[str] = None

class QuizSubmission(BaseModel):
    answers: Dict[str, Any]
    time_taken_minutes: float

class TaskUpdate(BaseModel):
    completed: bool

class LearningPathResponse(BaseModel):
    id: int
    title: str
    description: str
    total_weeks: int
    difficulty_level: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class WeeklyPlanResponse(BaseModel):
    id: int
    week_number: int
    title: str
    topics: List[str]
    estimated_hours: float
    difficulty: str
    progress_percentage: float
    
    class Config:
        from_attributes = True

class DailyTaskResponse(BaseModel):
    id: int
    task_type: str
    title: str
    description: Optional[str]
    duration_minutes: int
    priority: str
    is_completed: bool
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class QuizResponse(BaseModel):
    id: int
    title: str
    description: str
    questions: List[Dict[str, Any]]
    time_limit_minutes: int
    total_points: int
    quiz_type: str
    
    class Config:
        from_attributes = True

class ProgressResponse(BaseModel):
    overall_progress: float
    subject_mastery: Dict[str, float]
    tasks_completed: int
    quizzes_taken: int
    average_score: float
    study_streak: int
    recommendations: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True