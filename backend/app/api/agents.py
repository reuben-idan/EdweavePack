from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api.auth import get_current_user
from agents.orchestrator import AgentOrchestrator
from agents.curriculum_architect import CurriculumArchitectAgent
from agents.assessment_generator import AssessmentGeneratorAgent
from agents.personalized_learning import PersonalizedLearningAgent
from agents.auto_grader import AutoGraderAgent
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json

router = APIRouter(prefix="/api/agents", tags=["agents"])

class CurriculumGenerationRequest(BaseModel):
    content: str
    level: str
    subject: str
    student_profiles: Optional[List[Dict[str, Any]]] = None

class AssessmentGenerationRequest(BaseModel):
    module: Dict[str, Any]
    assessment_type: str = "mixed"

class LearningPathRequest(BaseModel):
    student_profile: Dict[str, Any]
    curriculum: Dict[str, Any]

class GradingRequest(BaseModel):
    submission: Dict[str, Any]
    assessment: Dict[str, Any]
    student_profile: Dict[str, Any]

@router.post("/curriculum/generate")
async def generate_curriculum(
    request: CurriculumGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate complete curriculum using Agent Orchestrator"""
    try:
        orchestrator = AgentOrchestrator()
        
        curriculum = await orchestrator.create_complete_curriculum(
            content=request.content,
            level=request.level,
            subject=request.subject,
            student_profiles=request.student_profiles
        )
        
        return {
            "status": "success",
            "curriculum": curriculum,
            "agent_used": "curriculum_architect + assessment_generator + personalized_learning"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Curriculum generation failed: {str(e)}")

@router.post("/assessment/generate")
async def generate_assessment(
    request: AssessmentGenerationRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate assessment using Assessment Generator Agent"""
    try:
        agent = AssessmentGeneratorAgent()
        
        assessment = await agent.generate_assessment(
            module=request.module,
            assessment_type=request.assessment_type
        )
        
        return {
            "status": "success",
            "assessment": assessment,
            "agent_used": "assessment_generator"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment generation failed: {str(e)}")

@router.post("/learning-path/generate")
async def generate_learning_path(
    request: LearningPathRequest,
    current_user: User = Depends(get_current_user)
):
    """Generate personalized learning path"""
    try:
        agent = PersonalizedLearningAgent()
        
        learning_path = await agent.generate_learning_path(
            student_profile=request.student_profile,
            curriculum=request.curriculum
        )
        
        return {
            "status": "success",
            "learning_path": learning_path,
            "agent_used": "personalized_learning"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning path generation failed: {str(e)}")

@router.post("/grade/submission")
async def grade_submission(
    request: GradingRequest,
    current_user: User = Depends(get_current_user)
):
    """Grade submission using Auto-Grader Agent"""
    try:
        orchestrator = AgentOrchestrator()
        
        result = await orchestrator.process_student_submission(
            submission=request.submission,
            assessment=request.assessment,
            student_profile=request.student_profile
        )
        
        return {
            "status": "success",
            "grading_result": result,
            "agent_used": "auto_grader + personalized_learning"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grading failed: {str(e)}")

@router.get("/bloom-taxonomy/align/{level}")
async def align_to_bloom_level(
    level: str,
    objectives: str,  # JSON string of objectives array
    current_user: User = Depends(get_current_user)
):
    """Align learning objectives to specific Bloom's taxonomy level"""
    try:
        agent = CurriculumArchitectAgent()
        
        objectives_list = json.loads(objectives)
        aligned_objectives = await agent.align_to_bloom_taxonomy(objectives_list, level)
        
        return {
            "status": "success",
            "aligned_objectives": aligned_objectives,
            "bloom_level": level,
            "agent_used": "curriculum_architect"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bloom alignment failed: {str(e)}")

@router.post("/question-bank/generate")
async def generate_question_bank(
    topic: str,
    bloom_level: str,
    count: int = 10,
    current_user: User = Depends(get_current_user)
):
    """Generate question bank for specific topic and Bloom level"""
    try:
        agent = AssessmentGeneratorAgent()
        
        questions = await agent.generate_question_bank(
            topic=topic,
            bloom_level=bloom_level,
            count=count
        )
        
        return {
            "status": "success",
            "questions": questions,
            "topic": topic,
            "bloom_level": bloom_level,
            "agent_used": "assessment_generator"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question bank generation failed: {str(e)}")

@router.post("/remediation/generate")
async def generate_remediation_plan(
    student_id: str,
    weak_areas: List[str],
    current_user: User = Depends(get_current_user)
):
    """Generate remediation plan for student weak areas"""
    try:
        agent = PersonalizedLearningAgent()
        
        remediation_plan = await agent.generate_remediation_plan(
            student_id=student_id,
            weak_areas=weak_areas
        )
        
        return {
            "status": "success",
            "remediation_plan": remediation_plan,
            "student_id": student_id,
            "agent_used": "personalized_learning"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Remediation plan generation failed: {str(e)}")

@router.post("/analytics/insights")
async def generate_progress_insights(
    student_data: List[Dict[str, Any]],
    current_user: User = Depends(get_current_user)
):
    """Generate comprehensive progress insights"""
    try:
        orchestrator = AgentOrchestrator()
        
        insights = await orchestrator.generate_progress_insights(student_data)
        
        return {
            "status": "success",
            "insights": insights,
            "students_analyzed": len(student_data),
            "agent_used": "orchestrator"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Insights generation failed: {str(e)}")

@router.get("/kiro/config")
async def get_kiro_configuration(
    current_user: User = Depends(get_current_user)
):
    """Get current Kiro agent configuration"""
    try:
        import yaml
        
        with open('agents/kiro_config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        return {
            "status": "success",
            "kiro_config": config,
            "agents_available": [
                "curriculum_architect",
                "assessment_generator", 
                "personalized_learning",
                "auto_grader"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Config retrieval failed: {str(e)}")

@router.post("/batch/grade-submissions")
async def batch_grade_submissions(
    submissions: List[Dict[str, Any]],
    assessment: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Batch grade multiple submissions"""
    try:
        agent = AutoGraderAgent()
        
        # Process in background for large batches
        if len(submissions) > 10:
            background_tasks.add_task(
                _process_batch_grading,
                submissions,
                assessment,
                current_user.id
            )
            
            return {
                "status": "processing",
                "message": "Batch grading started in background",
                "submission_count": len(submissions)
            }
        else:
            # Process immediately for small batches
            results = await agent.batch_grade_submissions(submissions, assessment)
            
            return {
                "status": "success",
                "grading_results": results,
                "submission_count": len(submissions),
                "agent_used": "auto_grader"
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch grading failed: {str(e)}")

async def _process_batch_grading(submissions: List[Dict], assessment: Dict, user_id: int):
    """Background task for batch grading"""
    try:
        agent = AutoGraderAgent()
        results = await agent.batch_grade_submissions(submissions, assessment)
        
        # Store results or notify user
        # Implementation depends on notification system
        
    except Exception as e:
        # Log error and notify user of failure
        import logging
        logging.error(f"Batch grading failed for user {user_id}: {str(e)}")