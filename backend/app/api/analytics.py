from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.curriculum import Curriculum, Assessment
from app.models.user import User
from app.api.auth import get_current_user

router = APIRouter()

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
    
    return {
        "total_curricula": curriculum_count,
        "total_assessments": assessment_count,
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
        ]
    }