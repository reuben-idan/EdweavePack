from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.core.database import get_db
from app.models.curriculum import Curriculum, Assessment
from app.models.student import Student, AssessmentAttempt, LearningAnalytics
from app.models.user import User
from app.api.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

@router.get("/dashboard")
async def get_dashboard_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get curriculum count
    curriculum_count = db.query(Curriculum).filter(Curriculum.user_id == current_user.id).count()
    
    # Get assessment count
    assessment_count = db.query(Assessment).join(Assessment.curriculum).filter(
        Assessment.curriculum.has(user_id=current_user.id)
    ).count()
    
    # Get recent curricula
    recent_curricula = db.query(Curriculum).filter(
        Curriculum.user_id == current_user.id
    ).order_by(Curriculum.created_at.desc()).limit(5).all()
    
    # Subject distribution
    subject_stats = db.query(
        Curriculum.subject,
        func.count(Curriculum.id).label('count')
    ).filter(
        Curriculum.user_id == current_user.id
    ).group_by(Curriculum.subject).all()
    
    # Get student count
    student_count = db.query(Student).filter(Student.teacher_id == current_user.id).count()
    
    # Get recent assessment attempts
    recent_attempts = db.query(AssessmentAttempt).join(Student).filter(
        Student.teacher_id == current_user.id
    ).order_by(AssessmentAttempt.completed_at.desc()).limit(10).all()
    
    # Calculate average class performance
    all_attempts = db.query(AssessmentAttempt).join(Student).filter(
        Student.teacher_id == current_user.id
    ).all()
    
    avg_performance = sum(
        attempt.total_score / attempt.max_score for attempt in all_attempts
    ) / len(all_attempts) * 100 if all_attempts else 0
    
    return {
        "total_curricula": curriculum_count,
        "total_assessments": assessment_count,
        "total_students": student_count,
        "average_class_performance": round(avg_performance, 2),
        "recent_curricula": [
            {
                "id": c.id,
                "title": c.title,
                "subject": c.subject,
                "created_at": c.created_at
            } for c in recent_curricula
        ],
        "subject_distribution": [
            {"subject": stat.subject, "count": stat.count}
            for stat in subject_stats
        ],
        "recent_activity": [
            {
                "student_name": attempt.student.name,
                "assessment_id": attempt.assessment_id,
                "score_percentage": round((attempt.total_score / attempt.max_score * 100), 1) if attempt.max_score > 0 else 0,
                "completed_at": attempt.completed_at
            } for attempt in recent_attempts
        ]
    }

@router.get("/class-performance")
async def get_class_performance(
    curriculum_id: int = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed class performance analytics"""
    
    # Base query for student attempts
    query = db.query(AssessmentAttempt).join(Student).filter(
        Student.teacher_id == current_user.id
    )
    
    if curriculum_id:
        query = query.join(Assessment).filter(Assessment.curriculum_id == curriculum_id)
    
    attempts = query.all()
    
    if not attempts:
        return {
            "message": "No assessment data available",
            "total_attempts": 0,
            "class_average": 0,
            "performance_distribution": {},
            "mastery_levels": {}
        }
    
    # Calculate performance metrics
    scores = [attempt.total_score / attempt.max_score * 100 for attempt in attempts if attempt.max_score > 0]
    
    performance_distribution = {
        "excellent": len([s for s in scores if s >= 90]),
        "good": len([s for s in scores if 80 <= s < 90]),
        "satisfactory": len([s for s in scores if 70 <= s < 80]),
        "needs_improvement": len([s for s in scores if s < 70])
    }
    
    # Mastery analysis by concept (simplified)
    mastery_levels = {
        "high_mastery": len([s for s in scores if s >= 85]),
        "developing": len([s for s in scores if 70 <= s < 85]),
        "emerging": len([s for s in scores if s < 70])
    }
    
    return {
        "total_attempts": len(attempts),
        "class_average": round(sum(scores) / len(scores), 2) if scores else 0,
        "performance_distribution": performance_distribution,
        "mastery_levels": mastery_levels,
        "score_range": {
            "highest": max(scores) if scores else 0,
            "lowest": min(scores) if scores else 0
        }
    }

@router.get("/misconceptions")
async def get_common_misconceptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Identify common misconceptions across all students"""
    
    # Get all students' assessment data
    students = db.query(Student).filter(Student.teacher_id == current_user.id).all()
    
    all_student_data = []
    for student in students:
        attempts = db.query(AssessmentAttempt).filter(
            AssessmentAttempt.student_id == student.id
        ).all()
        
        for attempt in attempts:
            all_student_data.append({
                "student_id": student.id,
                "student_name": student.name,
                "assessment_id": attempt.assessment_id,
                "answers": attempt.answers,
                "scores": attempt.scores,
                "feedback": attempt.feedback
            })
    
    if not all_student_data:
        return {
            "message": "No assessment data available for analysis",
            "common_misconceptions": [],
            "remediation_suggestions": []
        }
    
    # Generate insights using AI
    insights = await ai_service.generate_analytics_insights(all_student_data)
    
    return {
        "total_students_analyzed": len(students),
        "total_assessments_analyzed": len(all_student_data),
        "common_misconceptions": insights.get("common_misconceptions", []),
        "learning_gaps": insights.get("learning_gaps", []),
        "remediation_suggestions": insights.get("remediation_suggestions", []),
        "mastery_analysis": insights.get("mastery_analysis", "Analysis pending")
    }

@router.get("/progress-tracking/{student_id}")
async def track_student_progress(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track individual student progress over time"""
    
    # Verify student belongs to teacher
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.teacher_id == current_user.id
    ).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get all attempts chronologically
    attempts = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.student_id == student_id
    ).order_by(AssessmentAttempt.completed_at).all()
    
    progress_data = []
    for attempt in attempts:
        progress_data.append({
            "date": attempt.completed_at.isoformat(),
            "assessment_id": attempt.assessment_id,
            "score_percentage": round((attempt.total_score / attempt.max_score * 100), 2) if attempt.max_score > 0 else 0,
            "total_score": attempt.total_score,
            "max_score": attempt.max_score
        })
    
    # Calculate trends
    if len(progress_data) >= 2:
        recent_avg = sum(p["score_percentage"] for p in progress_data[-3:]) / min(3, len(progress_data))
        early_avg = sum(p["score_percentage"] for p in progress_data[:3]) / min(3, len(progress_data))
        trend = "improving" if recent_avg > early_avg else "declining" if recent_avg < early_avg else "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "student_id": student_id,
        "student_name": student.name,
        "total_assessments": len(attempts),
        "progress_data": progress_data,
        "current_average": round(sum(p["score_percentage"] for p in progress_data) / len(progress_data), 2) if progress_data else 0,
        "trend": trend,
        "latest_score": progress_data[-1]["score_percentage"] if progress_data else 0
    }