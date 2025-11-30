from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import json
import logging

from app.core.database import get_db
from app.models.user import User
from app.models.curriculum import Curriculum, Assessment
from app.api.auth import get_current_user
from app.services.aws_ai_service import AWSAIService
from app.services.q_assistant_service import QAssistantService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize AI services
aws_ai = AWSAIService()
q_assistant = QAssistantService()

@router.post("/analyze-document")
async def analyze_document(
    s3_bucket: str,
    s3_key: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze uploaded document using Textract + Comprehend"""
    
    try:
        analysis = await aws_ai.analyze_document_content(s3_bucket, s3_key)
        
        return {
            "success": True,
            "analysis": analysis,
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error(f"Document analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-curriculum-ai")
async def generate_curriculum_ai(
    content: str,
    subject: str,
    grade_level: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate curriculum using Bedrock AI"""
    
    try:
        curriculum_data = await aws_ai.generate_curriculum_with_bedrock(
            content=content,
            subject=subject,
            grade_level=grade_level
        )
        
        # Save to database
        db_curriculum = Curriculum(
            title=curriculum_data.get("title", f"{subject} Curriculum"),
            subject=subject,
            grade_level=grade_level,
            description=curriculum_data.get("description", "AI-generated curriculum"),
            content_data=curriculum_data,
            ai_generated=True,
            amazon_q_powered=True,
            created_by=current_user.id
        )
        
        db.add(db_curriculum)
        db.commit()
        db.refresh(db_curriculum)
        
        return {
            "success": True,
            "curriculum_id": db_curriculum.id,
            "curriculum_data": curriculum_data
        }
        
    except Exception as e:
        logger.error(f"AI curriculum generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-assessment-ai")
async def generate_assessment_ai(
    curriculum_id: int,
    difficulty: str = "medium",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate assessment using Bedrock AI"""
    
    try:
        # Get curriculum data
        curriculum = db.query(Curriculum).filter(
            Curriculum.id == curriculum_id,
            Curriculum.created_by == current_user.id
        ).first()
        
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        
        # Generate questions
        questions = await aws_ai.generate_assessment_questions(
            curriculum_data=curriculum.content_data,
            difficulty=difficulty
        )
        
        # Create assessment
        assessment_data = {
            "questions": questions,
            "total_points": sum(q.get("points", 5) for q in questions),
            "difficulty": difficulty,
            "ai_generated": True
        }
        
        db_assessment = Assessment(
            title=f"AI Assessment - {curriculum.title}",
            curriculum_id=curriculum_id,
            assessment_data=assessment_data,
            total_points=assessment_data["total_points"],
            ai_generated=True,
            created_by=current_user.id
        )
        
        db.add(db_assessment)
        db.commit()
        db.refresh(db_assessment)
        
        return {
            "success": True,
            "assessment_id": db_assessment.id,
            "questions": questions,
            "total_points": assessment_data["total_points"]
        }
        
    except Exception as e:
        logger.error(f"AI assessment generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auto-grade")
async def auto_grade_response(
    assessment_id: int,
    question_id: int,
    student_answer: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Auto-grade student response using AI"""
    
    try:
        # Get assessment and question
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        
        questions = assessment.assessment_data.get("questions", [])
        question = next((q for q in questions if q.get("id") == question_id), None)
        
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        # Grade response
        grading_result = await aws_ai.auto_grade_response(question, student_answer)
        
        return {
            "success": True,
            "grading_result": grading_result,
            "question_id": question_id,
            "assessment_id": assessment_id
        }
        
    except Exception as e:
        logger.error(f"Auto-grading failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/learning-insights")
async def get_learning_insights(
    curriculum_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate learning insights using AI analytics"""
    
    try:
        # Mock student data for now - in production, fetch from database
        student_data = [
            {"student_id": 1, "score": 85, "assessment": "Quiz 1", "time_spent": 30},
            {"student_id": 2, "score": 92, "assessment": "Quiz 1", "time_spent": 25},
            {"student_id": 3, "score": 78, "assessment": "Quiz 1", "time_spent": 40}
        ]
        
        insights = await aws_ai.generate_learning_insights(student_data)
        
        return {
            "success": True,
            "insights": insights,
            "curriculum_id": curriculum_id,
            "generated_at": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Learning insights generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/q-chat")
async def chat_with_q_assistant(
    message: str,
    context: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(get_current_user)
):
    """Chat with Amazon Q Assistant"""
    
    try:
        user_role = current_user.role or "teacher"
        
        response = await q_assistant.chat_with_q(
            user_role=user_role,
            message=message,
            context=context
        )
        
        return {
            "success": True,
            "response": response,
            "user_role": user_role
        }
        
    except Exception as e:
        logger.error(f"Q Assistant chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/teaching-suggestions/{curriculum_id}")
async def get_teaching_suggestions(
    curriculum_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered teaching suggestions"""
    
    try:
        curriculum = db.query(Curriculum).filter(
            Curriculum.id == curriculum_id,
            Curriculum.created_by == current_user.id
        ).first()
        
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        
        suggestions = await q_assistant.get_teaching_suggestions(
            curriculum_data=curriculum.content_data,
            student_performance=[]  # Add actual performance data
        )
        
        return {
            "success": True,
            "suggestions": suggestions,
            "curriculum_id": curriculum_id
        }
        
    except Exception as e:
        logger.error(f"Teaching suggestions failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain-concept")
async def explain_concept(
    concept: str,
    grade_level: str,
    learning_style: str = "mixed",
    current_user: User = Depends(get_current_user)
):
    """Get AI explanation of concept for students"""
    
    try:
        explanation = await q_assistant.explain_concept(
            concept=concept,
            grade_level=grade_level,
            learning_style=learning_style
        )
        
        return {
            "success": True,
            "explanation": explanation
        }
        
    except Exception as e:
        logger.error(f"Concept explanation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-study-plan")
async def generate_study_plan(
    goals: List[str],
    available_time: int,
    current_level: str,
    current_user: User = Depends(get_current_user)
):
    """Generate personalized study plan"""
    
    try:
        study_plan = await q_assistant.generate_study_plan(
            student_goals=goals,
            available_time=available_time,
            current_level=current_level
        )
        
        return {
            "success": True,
            "study_plan": study_plan,
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error(f"Study plan generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/text-to-speech")
async def convert_text_to_speech(
    text: str,
    voice_id: str = "Joanna",
    current_user: User = Depends(get_current_user)
):
    """Convert text to speech using Polly"""
    
    try:
        audio_data = await aws_ai.text_to_speech(text, voice_id)
        
        return {
            "success": True,
            "audio_length": len(audio_data),
            "voice_id": voice_id,
            "message": "Audio generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Text-to-speech failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate-content")
async def translate_content(
    text: str,
    target_language: str = "es",
    current_user: User = Depends(get_current_user)
):
    """Translate content using AWS Translate"""
    
    try:
        translated_text = await aws_ai.translate_content(text, target_language)
        
        return {
            "success": True,
            "original_text": text[:100] + "..." if len(text) > 100 else text,
            "translated_text": translated_text,
            "target_language": target_language
        }
        
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-curriculum-quality")
async def analyze_curriculum_quality(
    curriculum_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze curriculum quality using AI"""
    
    try:
        curriculum = db.query(Curriculum).filter(
            Curriculum.id == curriculum_id,
            Curriculum.created_by == current_user.id
        ).first()
        
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        
        analysis = await q_assistant.analyze_curriculum_quality(curriculum.content_data)
        
        return {
            "success": True,
            "analysis": analysis,
            "curriculum_id": curriculum_id
        }
        
    except Exception as e:
        logger.error(f"Curriculum quality analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))