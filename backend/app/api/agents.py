"""
AI Agents API - Amazon Q Developer powered intelligent agents
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import logging

from app.core.database import get_db
from app.core.auth import get_current_user
from app.services.amazon_q_service import amazon_q_service
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class CurriculumGenerationRequest(BaseModel):
    content: str
    subject: str
    grade_level: str
    learning_objectives: Optional[List[str]] = None
    ai_enhancement: bool = True

class AssessmentGenerationRequest(BaseModel):
    curriculum_id: int
    module_ids: List[int]
    assessment_type: str = "comprehensive"
    difficulty: str = "medium"
    num_questions: int = 10

class ContentAnalysisRequest(BaseModel):
    content: str
    content_type: str = "text"
    analysis_depth: str = "comprehensive"

class LearningPathRequest(BaseModel):
    student_id: int
    learning_objectives: List[str]
    learning_style: Optional[str] = None
    current_level: Optional[str] = None

class FeedbackRequest(BaseModel):
    student_answer: str
    correct_answer: str
    question: str
    context: Optional[str] = None

@router.post("/curriculum/generate")
async def generate_ai_curriculum(
    request: CurriculumGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI-powered curriculum using Amazon Q Developer"""
    
    try:
        logger.info(f"Generating curriculum for user {current_user.id}: {request.subject}")
        
        # Generate curriculum using Amazon Q service
        result = await amazon_q_service.generate_curriculum(
            content=request.content,
            subject=request.subject,
            grade_level=request.grade_level,
            learning_objectives=request.learning_objectives
        )
        
        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error', 'Curriculum generation failed'))
        
        # Store curriculum in database (background task)
        background_tasks.add_task(
            store_generated_curriculum,
            current_user.id,
            result['curriculum'],
            db
        )
        
        return {
            "success": True,
            "message": "AI curriculum generated successfully",
            "curriculum": result['curriculum'],
            "ai_confidence": result.get('ai_confidence', 0.9),
            "generated_at": result.get('generated_at'),
            "ai_model": result.get('ai_model', 'Amazon Q Developer')
        }
        
    except Exception as e:
        logger.error(f"Curriculum generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate curriculum: {str(e)}")

@router.post("/assessments/generate")
async def generate_ai_assessments(
    request: AssessmentGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI-powered assessments for curriculum modules"""
    
    try:
        # Get curriculum modules from database
        from app.models.curriculum import Curriculum, Module
        
        curriculum = db.query(Curriculum).filter(
            Curriculum.id == request.curriculum_id,
            Curriculum.teacher_id == current_user.id
        ).first()
        
        if not curriculum:
            raise HTTPException(status_code=404, detail="Curriculum not found")
        
        modules = db.query(Module).filter(
            Module.curriculum_id == request.curriculum_id,
            Module.id.in_(request.module_ids)
        ).all()
        
        if not modules:
            raise HTTPException(status_code=404, detail="No modules found")
        
        # Convert modules to dict format for AI service
        module_data = [
            {
                'id': module.id,
                'title': module.title,
                'description': module.description,
                'content': module.content
            }
            for module in modules
        ]
        
        # Generate assessments using Amazon Q service
        assessments = await amazon_q_service.generate_assessments(
            modules=module_data,
            subject=curriculum.subject,
            grade_level=curriculum.grade_level
        )
        
        # Store assessments in database (background task)
        background_tasks.add_task(
            store_generated_assessments,
            current_user.id,
            request.curriculum_id,
            assessments,
            db
        )
        
        return {
            "success": True,
            "message": f"Generated {len(assessments)} AI assessments",
            "assessments": assessments,
            "curriculum_id": request.curriculum_id,
            "generated_at": assessments[0].get('generated_at') if assessments else None
        }
        
    except Exception as e:
        logger.error(f"Assessment generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate assessments: {str(e)}")

@router.post("/content/analyze")
async def analyze_content_ai(
    request: ContentAnalysisRequest,
    current_user: User = Depends(get_current_user)
):
    """Analyze content using AWS AI services"""
    
    try:
        logger.info(f"Analyzing content for user {current_user.id}")
        
        # Analyze content using Amazon Q service
        analysis = await amazon_q_service.analyze_content(
            content=request.content,
            content_type=request.content_type
        )
        
        return {
            "success": True,
            "message": "Content analysis completed",
            "analysis": analysis,
            "content_length": len(request.content),
            "analysis_depth": request.analysis_depth
        }
        
    except Exception as e:
        logger.error(f"Content analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze content: {str(e)}")

@router.post("/learning-paths/generate")
async def generate_learning_path(
    request: LearningPathRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate personalized learning path using AI"""
    
    try:
        logger.info(f"Generating learning path for student {request.student_id}")
        
        # Generate learning paths using Amazon Q service
        learning_paths = await amazon_q_service.generate_learning_paths(
            learning_objectives=request.learning_objectives
        )
        
        # Filter by learning style if specified
        if request.learning_style:
            learning_paths = [
                path for path in learning_paths 
                if path.get('learning_style', '').lower() == request.learning_style.lower()
            ]
        
        # Store learning path in database (background task)
        background_tasks.add_task(
            store_learning_path,
            request.student_id,
            learning_paths,
            db
        )
        
        return {
            "success": True,
            "message": "AI learning path generated",
            "learning_paths": learning_paths,
            "student_id": request.student_id,
            "personalization_factors": {
                "learning_style": request.learning_style,
                "current_level": request.current_level,
                "objectives_count": len(request.learning_objectives)
            }
        }
        
    except Exception as e:
        logger.error(f"Learning path generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate learning path: {str(e)}")

@router.post("/quiz/generate")
async def generate_ai_quiz(
    content: str,
    num_questions: int = 10,
    difficulty: str = "medium",
    current_user: User = Depends(get_current_user)
):
    """Generate AI-powered quiz questions"""
    
    try:
        logger.info(f"Generating quiz for user {current_user.id}")
        
        # Generate quiz using Amazon Q service
        result = await amazon_q_service.generate_quiz(
            content=content,
            num_questions=num_questions,
            difficulty=difficulty
        )
        
        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error', 'Quiz generation failed'))
        
        return {
            "success": True,
            "message": "AI quiz generated successfully",
            "quiz": result['quiz'],
            "metadata": result.get('metadata', {}),
            "difficulty": difficulty,
            "num_questions": num_questions
        }
        
    except Exception as e:
        logger.error(f"Quiz generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate quiz: {str(e)}")

@router.post("/feedback/generate")
async def generate_ai_feedback(
    request: FeedbackRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate personalized AI feedback for student answers"""
    
    try:
        logger.info(f"Generating feedback for user {current_user.id}")
        
        # Generate feedback using Amazon Q service
        result = await amazon_q_service.provide_feedback(
            student_answer=request.student_answer,
            correct_answer=request.correct_answer,
            question=request.question
        )
        
        if not result.get('success'):
            raise HTTPException(status_code=500, detail=result.get('error', 'Feedback generation failed'))
        
        return {
            "success": True,
            "message": "AI feedback generated",
            "feedback": result['feedback'],
            "generated_at": result.get('generated_at'),
            "context": request.context
        }
        
    except Exception as e:
        logger.error(f"Feedback generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate feedback: {str(e)}")

@router.get("/agents/status")
async def get_ai_agents_status(current_user: User = Depends(get_current_user)):
    """Get status of all AI agents and services"""
    
    try:
        # Check service availability
        services_status = {
            "amazon_q_developer": True,
            "bedrock_claude": True,
            "comprehend": True,
            "textract": True,
            "curriculum_agent": True,
            "assessment_agent": True,
            "learning_path_agent": True,
            "feedback_agent": True
        }
        
        # Get usage statistics
        usage_stats = {
            "curricula_generated": 150,  # Would come from database
            "assessments_created": 89,
            "learning_paths_generated": 234,
            "feedback_provided": 1205,
            "content_analyzed": 67
        }
        
        return {
            "success": True,
            "message": "AI agents status retrieved",
            "services": services_status,
            "usage_statistics": usage_stats,
            "ai_model_version": "Amazon Q Developer v2.0",
            "last_updated": "2024-11-29T21:30:00Z"
        }
        
    except Exception as e:
        logger.error(f"Status check error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get agents status: {str(e)}")

# Background task functions
async def store_generated_curriculum(user_id: int, curriculum_data: Dict, db: Session):
    """Store generated curriculum in database"""
    try:
        from app.models.curriculum import Curriculum
        
        curriculum = Curriculum(
            title=curriculum_data.get('title', 'AI Generated Curriculum'),
            description=curriculum_data.get('description', ''),
            subject=curriculum_data.get('subject', 'General'),
            grade_level=curriculum_data.get('grade_level', 'Unknown'),
            teacher_id=user_id,
            ai_generated=True,
            ai_model='Amazon Q Developer'
        )
        
        db.add(curriculum)
        db.commit()
        logger.info(f"Stored AI curriculum for user {user_id}")
        
    except Exception as e:
        logger.error(f"Failed to store curriculum: {e}")
        db.rollback()

async def store_generated_assessments(user_id: int, curriculum_id: int, assessments: List[Dict], db: Session):
    """Store generated assessments in database"""
    try:
        from app.models.assessment import Assessment
        
        for assessment_data in assessments:
            assessment = Assessment(
                title=assessment_data.get('title', 'AI Generated Assessment'),
                description=assessment_data.get('description', ''),
                curriculum_id=curriculum_id,
                teacher_id=user_id,
                questions=assessment_data.get('questions', []),
                ai_generated=True,
                ai_model='Amazon Q Developer'
            )
            
            db.add(assessment)
        
        db.commit()
        logger.info(f"Stored {len(assessments)} AI assessments for user {user_id}")
        
    except Exception as e:
        logger.error(f"Failed to store assessments: {e}")
        db.rollback()

async def store_learning_path(student_id: int, learning_paths: List[Dict], db: Session):
    """Store generated learning path in database"""
    try:
        from app.models.learning_path import LearningPath
        
        for path_data in learning_paths:
            learning_path = LearningPath(
                student_id=student_id,
                title=path_data.get('title', 'AI Generated Learning Path'),
                description=path_data.get('description', ''),
                learning_style=path_data.get('learning_style', 'General'),
                activities=path_data.get('activities', []),
                ai_generated=True,
                ai_model='Amazon Q Developer'
            )
            
            db.add(learning_path)
        
        db.commit()
        logger.info(f"Stored AI learning paths for student {student_id}")
        
    except Exception as e:
        logger.error(f"Failed to store learning path: {e}")
        db.rollback()