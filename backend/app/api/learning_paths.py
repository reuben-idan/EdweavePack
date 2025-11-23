from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.curriculum import Curriculum
from app.models.student import Student, AssessmentAttempt, LearningAnalytics, StudentLearningPath
from app.models.user import User
from app.api.auth import get_current_user
from app.services.ai_service import AIService
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
ai_service = AIService()

class StudentCreate(BaseModel):
    name: str
    email: str
    grade_level: str
    learning_style: str = "visual"
    phone: str = ""
    address: str = ""
    parent_name: str = ""
    parent_email: str = ""
    parent_phone: str = ""
    target_exams: List[str] = []
    subjects: List[str] = []
    goals: str = ""
    strengths: str = ""
    weaknesses: str = ""

@router.post("/students")
async def create_student(
    student_data: StudentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new student profile"""
    
    # Check if email already exists
    existing_student = db.query(Student).filter(Student.email == student_data.email).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    student = Student(
        name=student_data.name,
        email=student_data.email,
        hashed_password="temp_password",  # Will be set when student first logs in
        teacher_id=current_user.id,
        grade_level=student_data.grade_level,
        learning_style=student_data.learning_style,
        is_active=True
    )
    
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "grade_level": student.grade_level,
        "learning_style": student.learning_style,
        "is_active": student.is_active,
        "created_at": student.created_at,
        "subjects": student_data.subjects,
        "target_exams": student_data.target_exams,
        "goals": student_data.goals,
        "strengths": student_data.strengths,
        "weaknesses": student_data.weaknesses
    }

@router.get("/students")
async def get_students(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all students for the current teacher"""
    
    students = db.query(Student).filter(Student.teacher_id == current_user.id).all()
    
    return [
        {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "grade_level": student.grade_level,
            "learning_style": student.learning_style,
            "is_active": student.is_active,
            "created_at": student.created_at,
            "subjects": [],
            "target_exams": [],
            "phone": "",
            "address": "",
            "parent_name": "",
            "parent_email": "",
            "parent_phone": "",
            "goals": "",
            "strengths": "",
            "weaknesses": ""
        }
        for student in students
    ]

@router.get("/students/{student_id}")
async def get_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific student"""
    
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.teacher_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "grade_level": student.grade_level,
        "learning_style": student.learning_style,
        "is_active": student.is_active,
        "created_at": student.created_at
    }

@router.put("/students/{student_id}")
async def update_student(
    student_id: int,
    student_data: StudentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a student"""
    
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.teacher_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if email is already taken by another student
    if student_data.email != student.email:
        existing_student = db.query(Student).filter(
            Student.email == student_data.email,
            Student.id != student_id
        ).first()
        if existing_student:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update student data
    student.name = student_data.name
    student.email = student_data.email
    student.grade_level = student_data.grade_level
    student.learning_style = student_data.learning_style
    
    db.commit()
    db.refresh(student)
    
    return {
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "grade_level": student.grade_level,
        "learning_style": student.learning_style,
        "is_active": student.is_active,
        "created_at": student.created_at
    }

@router.delete("/students/{student_id}")
async def delete_student(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a student"""
    
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.teacher_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    
    return {"message": "Student deleted successfully"}

@router.post("/personalized/{student_id}/{curriculum_id}")
async def generate_personalized_path(
    student_id: int,
    curriculum_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate personalized learning path for a student"""
    
    # Get student and curriculum
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.teacher_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    curriculum = db.query(Curriculum).filter(
        Curriculum.id == curriculum_id,
        Curriculum.user_id == current_user.id
    ).first()
    
    if not curriculum:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    
    # Simplified prior performance
    prior_performance = {
        "average_score": 0,
        "attempts_count": 0,
        "strengths": [],
        "weaknesses": []
    }
    
    # Create student profile for AI
    student_profile = {
        "age": student.age,
        "learning_style": student.learning_style,
        "interests": student.interests,
        "prior_performance": prior_performance
    }
    
    # Generate personalized path using AI
    personalized_data = await ai_service.generate_personalized_path(
        student_profile, 
        curriculum.metadata
    )
    
    # Save or update personalized path in student learning path
    existing_path = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == student_id,
        StudentLearningPath.curriculum_id == curriculum_id
    ).first()
    
    if existing_path:
        existing_path.path_data = personalized_data
        existing_path.progress_data = {"completed_blocks": [], "current_week": 1}
    else:
        new_path = StudentLearningPath(
            student_id=student_id,
            curriculum_id=curriculum_id,
            path_data=personalized_data,
            progress_data={"completed_blocks": [], "current_week": 1}
        )
        db.add(new_path)
    
    db.commit()
    
    return {
        "student_id": student_id,
        "curriculum_id": curriculum_id,
        "personalized_path": personalized_data,
        "message": "Personalized learning path generated successfully"
    }

@router.get("/personalized/{student_id}/{curriculum_id}")
async def get_personalized_path(
    student_id: int,
    curriculum_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized learning path for a student"""
    
    path = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == student_id,
        StudentLearningPath.curriculum_id == curriculum_id
    ).first()
    
    if not path:
        raise HTTPException(status_code=404, detail="Personalized path not found")
    
    # Verify teacher owns the student
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.teacher_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "student_id": student_id,
        "curriculum_id": curriculum_id,
        "path_data": path.path_data,
        "progress": path.progress_data,
        "created_at": path.created_at,
        "updated_at": path.updated_at
    }

@router.put("/progress/{student_id}/{curriculum_id}")
async def update_progress(
    student_id: int,
    curriculum_id: int,
    progress_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update student progress on personalized path"""
    
    path = db.query(StudentLearningPath).filter(
        StudentLearningPath.student_id == student_id,
        StudentLearningPath.curriculum_id == curriculum_id
    ).first()
    
    if not path:
        raise HTTPException(status_code=404, detail="Personalized path not found")
    
    # Update progress
    current_progress = path.progress_data or {}
    current_progress.update(progress_data)
    path.progress_data = current_progress
    
    db.commit()
    
    return {
        "student_id": student_id,
        "curriculum_id": curriculum_id,
        "updated_progress": path.progress_data,
        "message": "Progress updated successfully"
    }

@router.get("/analytics/{student_id}")
async def get_student_analytics(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics for a student"""
    
    # Verify teacher owns the student
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.teacher_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get all assessment attempts
    attempts = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.student_id == student_id
    ).all()
    
    # Prepare data for AI analysis
    student_data = []
    for attempt in attempts:
        student_data.append({
            "assessment_id": attempt.assessment_id,
            "total_score": attempt.total_score,
            "max_score": attempt.max_score,
            "percentage": (attempt.total_score / attempt.max_score * 100) if attempt.max_score > 0 else 0,
            "answers": attempt.answers,
            "feedback": attempt.feedback,
            "completed_at": attempt.completed_at.isoformat()
        })
    
    # Generate analytics insights using AI
    if student_data:
        analytics_insights = await ai_service.generate_analytics_insights(student_data)
        
        # Save analytics to database
        analytics = LearningAnalytics(
            student_id=student_id,
            curriculum_id=attempts[0].assessment_id if attempts else None,  # Use first assessment's curriculum
            mastery_data=analytics_insights.get("mastery_analysis", {}),
            misconceptions=analytics_insights.get("common_misconceptions", []),
            learning_gaps=analytics_insights.get("learning_gaps", []),
            recommendations=analytics_insights.get("remediation_suggestions", [])
        )
        db.add(analytics)
        db.commit()
    else:
        analytics_insights = {
            "mastery_analysis": "No assessment data available",
            "common_misconceptions": [],
            "learning_gaps": [],
            "remediation_suggestions": ["Complete some assessments to generate insights"],
            "performance_trends": "Insufficient data",
            "differentiation_needs": "Assessment needed"
        }
    
    return {
        "student_id": student_id,
        "student_name": student.name,
        "total_assessments": len(attempts),
        "average_score": sum(attempt.total_score / attempt.max_score for attempt in attempts) / len(attempts) * 100 if attempts else 0,
        "analytics_insights": analytics_insights,
        "recent_performance": student_data[-5:] if student_data else []  # Last 5 attempts
    }