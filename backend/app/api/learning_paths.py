from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.curriculum import Curriculum
from app.models.student import Student, PersonalizedPath, AssessmentAttempt, LearningAnalytics
from app.models.user import User
from app.api.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.post("/students")
async def create_student(
    student_data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new student profile"""
    
    student = Student(
        name=student_data["name"],
        email=student_data["email"],
        age=student_data.get("age", 12),
        grade_level=student_data.get("grade_level", "6-8"),
        learning_style=student_data.get("learning_style", "mixed"),
        interests=student_data.get("interests", []),
        teacher_id=current_user.id
    )
    
    db.add(student)
    db.commit()
    db.refresh(student)
    
    return {
        "student_id": student.id,
        "name": student.name,
        "profile_created": True
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
            "age": student.age,
            "grade_level": student.grade_level,
            "learning_style": student.learning_style,
            "interests": student.interests
        }
        for student in students
    ]

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
    
    # Get student's prior performance
    prior_attempts = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.student_id == student_id
    ).all()
    
    prior_performance = {
        "average_score": sum(attempt.total_score / attempt.max_score for attempt in prior_attempts) / len(prior_attempts) * 100 if prior_attempts else 0,
        "attempts_count": len(prior_attempts),
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
    
    # Save or update personalized path
    existing_path = db.query(PersonalizedPath).filter(
        PersonalizedPath.student_id == student_id,
        PersonalizedPath.curriculum_id == curriculum_id
    ).first()
    
    if existing_path:
        existing_path.path_data = personalized_data
        existing_path.progress = {"completed_blocks": [], "current_week": 1}
    else:
        new_path = PersonalizedPath(
            student_id=student_id,
            curriculum_id=curriculum_id,
            path_data=personalized_data,
            progress={"completed_blocks": [], "current_week": 1}
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
    
    path = db.query(PersonalizedPath).filter(
        PersonalizedPath.student_id == student_id,
        PersonalizedPath.curriculum_id == curriculum_id
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
        "progress": path.progress,
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
    
    path = db.query(PersonalizedPath).filter(
        PersonalizedPath.student_id == student_id,
        PersonalizedPath.curriculum_id == curriculum_id
    ).first()
    
    if not path:
        raise HTTPException(status_code=404, detail="Personalized path not found")
    
    # Update progress
    current_progress = path.progress or {}
    current_progress.update(progress_data)
    path.progress = current_progress
    
    db.commit()
    
    return {
        "student_id": student_id,
        "curriculum_id": curriculum_id,
        "updated_progress": path.progress,
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