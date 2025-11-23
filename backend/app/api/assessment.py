from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.curriculum import Assessment, Question
from app.models.user import User
from app.schemas.curriculum import AssessmentResponse, QuestionResponse
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
    assessment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).join(Assessment.curriculum).filter(
        Assessment.id == assessment_id,
        Assessment.curriculum.has(user_id=current_user.id)
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return assessment

@router.get("/{assessment_id}/questions", response_model=List[QuestionResponse])
async def get_questions(
    assessment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).join(Assessment.curriculum).filter(
        Assessment.id == assessment_id,
        Assessment.curriculum.has(user_id=current_user.id)
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    return db.query(Question).filter(Question.assessment_id == assessment_id).all()

@router.post("/{assessment_id}/submit")
async def submit_assessment(
    assessment_id: int,
    answers: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    questions = db.query(Question).filter(Question.assessment_id == assessment_id).all()
    
    total_points = 0
    earned_points = 0
    
    for question in questions:
        total_points += question.points
        user_answer = answers.get(str(question.id))
        
        if user_answer and user_answer.lower().strip() == question.correct_answer.lower().strip():
            earned_points += question.points
    
    score = (earned_points / total_points * 100) if total_points > 0 else 0
    
    return {
        "score": score,
        "earned_points": earned_points,
        "total_points": total_points,
        "passed": score >= 70
    }