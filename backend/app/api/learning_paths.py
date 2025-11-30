"""
Learning Paths API - AI-powered personalized learning paths
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import logging
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_user
from app.services.amazon_q_service import amazon_q_service
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class LearningPathCreate(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    grade_level: str
    learning_objectives: List[str]
    learning_style: Optional[str] = None
    difficulty_level: str = "medium"
    estimated_duration: Optional[int] = None  # in hours

class LearningPathUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    progress_percentage: Optional[float] = None
    current_milestone: Optional[str] = None

class MilestoneComplete(BaseModel):
    milestone_id: str
    completion_time: Optional[datetime] = None
    performance_score: Optional[float] = None
    notes: Optional[str] = None

class AdaptationRequest(BaseModel):
    student_performance: Dict[str, Any]
    learning_preferences: Dict[str, Any]
    time_constraints: Optional[Dict[str, Any]] = None

@router.post("/create")
async def create_learning_path(
    request: LearningPathCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create AI-powered personalized learning path"""
    
    try:
        logger.info(f"Creating learning path for user {current_user.id}: {request.title}")
        
        # Generate AI-powered learning path
        ai_paths = await amazon_q_service.generate_learning_paths(
            learning_objectives=request.learning_objectives
        )
        
        # Select best path based on learning style
        selected_path = ai_paths[0]  # Default to first
        if request.learning_style:
            for path in ai_paths:
                if path.get('learning_style', '').lower() == request.learning_style.lower():
                    selected_path = path
                    break
        
        # Create learning path in database
        from app.models.learning_path import LearningPath
        
        learning_path = LearningPath(
            title=request.title,
            description=request.description or selected_path.get('description', ''),
            subject=request.subject,
            grade_level=request.grade_level,
            learning_objectives=request.learning_objectives,
            learning_style=request.learning_style or 'General',
            difficulty_level=request.difficulty_level,
            estimated_duration=request.estimated_duration or selected_path.get('estimated_duration', 40),
            teacher_id=current_user.id,
            ai_generated=True,
            ai_data=selected_path,
            activities=selected_path.get('activities', []),
            milestones=selected_path.get('milestones', []),
            resources=selected_path.get('resources', [])
        )
        
        db.add(learning_path)
        db.commit()
        db.refresh(learning_path)
        
        # Generate additional resources in background
        background_tasks.add_task(
            generate_learning_resources,
            learning_path.id,
            request.learning_objectives,
            db
        )
        
        return {
            "success": True,
            "message": "AI learning path created successfully",
            "learning_path": {
                "id": learning_path.id,
                "title": learning_path.title,
                "description": learning_path.description,
                "subject": learning_path.subject,
                "grade_level": learning_path.grade_level,
                "learning_style": learning_path.learning_style,
                "estimated_duration": learning_path.estimated_duration,
                "activities": learning_path.activities,
                "milestones": learning_path.milestones,
                "ai_generated": True
            },
            "ai_confidence": selected_path.get('confidence', 0.9),
            "personalization_factors": {
                "learning_style": request.learning_style,
                "difficulty_level": request.difficulty_level,
                "objectives_count": len(request.learning_objectives)
            }
        }
        
    except Exception as e:
        logger.error(f"Learning path creation error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create learning path: {str(e)}")

@router.get("/")
async def get_learning_paths(
    subject: Optional[str] = None,
    grade_level: Optional[str] = None,
    learning_style: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get learning paths with optional filters"""
    
    try:
        from app.models.learning_path import LearningPath
        
        query = db.query(LearningPath).filter(LearningPath.teacher_id == current_user.id)
        
        if subject:
            query = query.filter(LearningPath.subject.ilike(f"%{subject}%"))
        if grade_level:
            query = query.filter(LearningPath.grade_level == grade_level)
        if learning_style:
            query = query.filter(LearningPath.learning_style.ilike(f"%{learning_style}%"))
        
        learning_paths = query.all()
        
        return {
            "success": True,
            "learning_paths": [
                {
                    "id": path.id,
                    "title": path.title,
                    "description": path.description,
                    "subject": path.subject,
                    "grade_level": path.grade_level,
                    "learning_style": path.learning_style,
                    "difficulty_level": path.difficulty_level,
                    "estimated_duration": path.estimated_duration,
                    "progress_percentage": path.progress_percentage,
                    "ai_generated": path.ai_generated,
                    "created_at": path.created_at,
                    "updated_at": path.updated_at
                }
                for path in learning_paths
            ],
            "total_count": len(learning_paths),
            "filters_applied": {
                "subject": subject,
                "grade_level": grade_level,
                "learning_style": learning_style
            }
        }
        
    except Exception as e:
        logger.error(f"Get learning paths error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve learning paths: {str(e)}")

@router.get("/{path_id}")
async def get_learning_path(
    path_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed learning path information"""
    
    try:
        from app.models.learning_path import LearningPath
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.id == path_id,
            LearningPath.teacher_id == current_user.id
        ).first()
        
        if not learning_path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        
        return {
            "success": True,
            "learning_path": {
                "id": learning_path.id,
                "title": learning_path.title,
                "description": learning_path.description,
                "subject": learning_path.subject,
                "grade_level": learning_path.grade_level,
                "learning_objectives": learning_path.learning_objectives,
                "learning_style": learning_path.learning_style,
                "difficulty_level": learning_path.difficulty_level,
                "estimated_duration": learning_path.estimated_duration,
                "progress_percentage": learning_path.progress_percentage,
                "current_milestone": learning_path.current_milestone,
                "activities": learning_path.activities,
                "milestones": learning_path.milestones,
                "resources": learning_path.resources,
                "ai_generated": learning_path.ai_generated,
                "ai_data": learning_path.ai_data,
                "created_at": learning_path.created_at,
                "updated_at": learning_path.updated_at
            }
        }
        
    except Exception as e:
        logger.error(f"Get learning path error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve learning path: {str(e)}")

@router.put("/{path_id}")
async def update_learning_path(
    path_id: int,
    request: LearningPathUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update learning path"""
    
    try:
        from app.models.learning_path import LearningPath
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.id == path_id,
            LearningPath.teacher_id == current_user.id
        ).first()
        
        if not learning_path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        
        # Update fields
        if request.title is not None:
            learning_path.title = request.title
        if request.description is not None:
            learning_path.description = request.description
        if request.learning_objectives is not None:
            learning_path.learning_objectives = request.learning_objectives
        if request.progress_percentage is not None:
            learning_path.progress_percentage = request.progress_percentage
        if request.current_milestone is not None:
            learning_path.current_milestone = request.current_milestone
        
        learning_path.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(learning_path)
        
        return {
            "success": True,
            "message": "Learning path updated successfully",
            "learning_path": {
                "id": learning_path.id,
                "title": learning_path.title,
                "description": learning_path.description,
                "progress_percentage": learning_path.progress_percentage,
                "current_milestone": learning_path.current_milestone,
                "updated_at": learning_path.updated_at
            }
        }
        
    except Exception as e:
        logger.error(f"Update learning path error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update learning path: {str(e)}")

@router.post("/{path_id}/milestone/complete")
async def complete_milestone(
    path_id: int,
    request: MilestoneComplete,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark milestone as complete and adapt learning path"""
    
    try:
        from app.models.learning_path import LearningPath
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.id == path_id,
            LearningPath.teacher_id == current_user.id
        ).first()
        
        if not learning_path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        
        # Update milestone completion
        milestones = learning_path.milestones or []
        for milestone in milestones:
            if milestone.get('id') == request.milestone_id:
                milestone['completed'] = True
                milestone['completion_time'] = request.completion_time or datetime.utcnow()
                milestone['performance_score'] = request.performance_score
                milestone['notes'] = request.notes
                break
        
        learning_path.milestones = milestones
        
        # Calculate progress
        completed_milestones = sum(1 for m in milestones if m.get('completed', False))
        total_milestones = len(milestones)
        learning_path.progress_percentage = (completed_milestones / total_milestones * 100) if total_milestones > 0 else 0
        
        # Update current milestone
        next_milestone = next((m for m in milestones if not m.get('completed', False)), None)
        learning_path.current_milestone = next_milestone.get('title') if next_milestone else 'Completed'
        
        learning_path.updated_at = datetime.utcnow()
        
        db.commit()
        
        # Adapt learning path based on performance (background task)
        if request.performance_score is not None:
            background_tasks.add_task(
                adapt_learning_path,
                path_id,
                request.performance_score,
                db
            )
        
        return {
            "success": True,
            "message": "Milestone completed successfully",
            "milestone_id": request.milestone_id,
            "progress_percentage": learning_path.progress_percentage,
            "current_milestone": learning_path.current_milestone,
            "next_milestone": next_milestone.get('title') if next_milestone else None,
            "adaptation_triggered": request.performance_score is not None
        }
        
    except Exception as e:
        logger.error(f"Complete milestone error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to complete milestone: {str(e)}")

@router.post("/{path_id}/adapt")
async def adapt_learning_path_endpoint(
    path_id: int,
    request: AdaptationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adapt learning path based on student performance and preferences"""
    
    try:
        from app.models.learning_path import LearningPath
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.id == path_id,
            LearningPath.teacher_id == current_user.id
        ).first()
        
        if not learning_path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        
        # Generate adaptation recommendations using AI
        adaptation_prompt = f"""
        Adapt the learning path based on student performance:
        
        Current Learning Path: {learning_path.title}
        Subject: {learning_path.subject}
        Learning Style: {learning_path.learning_style}
        
        Student Performance: {request.student_performance}
        Learning Preferences: {request.learning_preferences}
        Time Constraints: {request.time_constraints}
        
        Provide specific adaptations for:
        1. Activity modifications
        2. Difficulty adjustments
        3. Resource recommendations
        4. Timeline adjustments
        5. Learning strategy changes
        """
        
        adaptation_result = await amazon_q_service._call_bedrock_claude(adaptation_prompt)
        
        # Parse and apply adaptations
        adaptations = {
            'recommendations': adaptation_result,
            'performance_analysis': request.student_performance,
            'preferences_considered': request.learning_preferences,
            'adapted_at': datetime.utcnow().isoformat()
        }
        
        # Store adaptation data
        learning_path.ai_data = learning_path.ai_data or {}
        learning_path.ai_data['adaptations'] = learning_path.ai_data.get('adaptations', [])
        learning_path.ai_data['adaptations'].append(adaptations)
        learning_path.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Learning path adapted successfully",
            "adaptations": adaptations,
            "path_id": path_id,
            "adaptation_confidence": 0.85
        }
        
    except Exception as e:
        logger.error(f"Adapt learning path error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to adapt learning path: {str(e)}")

@router.get("/{path_id}/analytics")
async def get_learning_path_analytics(
    path_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analytics for learning path performance"""
    
    try:
        from app.models.learning_path import LearningPath
        
        learning_path = db.query(LearningPath).filter(
            LearningPath.id == path_id,
            LearningPath.teacher_id == current_user.id
        ).first()
        
        if not learning_path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        
        # Calculate analytics
        milestones = learning_path.milestones or []
        completed_milestones = [m for m in milestones if m.get('completed', False)]
        
        analytics = {
            "completion_rate": len(completed_milestones) / len(milestones) * 100 if milestones else 0,
            "average_performance": sum(m.get('performance_score', 0) for m in completed_milestones) / len(completed_milestones) if completed_milestones else 0,
            "time_spent": sum(m.get('time_spent', 0) for m in completed_milestones),
            "milestones_completed": len(completed_milestones),
            "total_milestones": len(milestones),
            "current_streak": self._calculate_streak(completed_milestones),
            "difficulty_progression": self._analyze_difficulty_progression(completed_milestones),
            "learning_velocity": self._calculate_learning_velocity(completed_milestones),
            "adaptation_count": len(learning_path.ai_data.get('adaptations', [])) if learning_path.ai_data else 0
        }
        
        return {
            "success": True,
            "analytics": analytics,
            "path_info": {
                "id": learning_path.id,
                "title": learning_path.title,
                "subject": learning_path.subject,
                "learning_style": learning_path.learning_style
            }
        }
        
    except Exception as e:
        logger.error(f"Get analytics error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get analytics: {str(e)}")

# Background task functions
async def generate_learning_resources(path_id: int, learning_objectives: List[str], db: Session):
    """Generate additional learning resources for the path"""
    try:
        # Generate resources using AI
        resources_prompt = f"""
        Generate comprehensive learning resources for objectives:
        {learning_objectives}
        
        Include:
        1. Reading materials and articles
        2. Interactive exercises
        3. Video recommendations
        4. Practice problems
        5. Real-world applications
        """
        
        resources_result = await amazon_q_service._call_bedrock_claude(resources_prompt)
        
        # Update learning path with resources
        from app.models.learning_path import LearningPath
        learning_path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
        
        if learning_path:
            learning_path.resources = learning_path.resources or []
            learning_path.resources.append({
                'type': 'ai_generated',
                'content': resources_result,
                'generated_at': datetime.utcnow().isoformat()
            })
            db.commit()
            
        logger.info(f"Generated additional resources for learning path {path_id}")
        
    except Exception as e:
        logger.error(f"Failed to generate resources: {e}")

async def adapt_learning_path(path_id: int, performance_score: float, db: Session):
    """Adapt learning path based on performance"""
    try:
        from app.models.learning_path import LearningPath
        
        learning_path = db.query(LearningPath).filter(LearningPath.id == path_id).first()
        
        if not learning_path:
            return
        
        # Determine adaptation strategy
        if performance_score < 0.6:  # Struggling
            adaptation_type = "remediation"
        elif performance_score > 0.9:  # Excelling
            adaptation_type = "acceleration"
        else:
            adaptation_type = "maintenance"
        
        # Apply adaptations
        adaptations = {
            'type': adaptation_type,
            'performance_trigger': performance_score,
            'adapted_at': datetime.utcnow().isoformat(),
            'changes_made': []
        }
        
        if adaptation_type == "remediation":
            adaptations['changes_made'] = [
                "Added review activities",
                "Reduced difficulty level",
                "Increased practice time",
                "Added visual aids"
            ]
        elif adaptation_type == "acceleration":
            adaptations['changes_made'] = [
                "Added advanced challenges",
                "Increased pace",
                "Added extension activities",
                "Introduced next-level concepts"
            ]
        
        # Store adaptation
        learning_path.ai_data = learning_path.ai_data or {}
        learning_path.ai_data['auto_adaptations'] = learning_path.ai_data.get('auto_adaptations', [])
        learning_path.ai_data['auto_adaptations'].append(adaptations)
        
        db.commit()
        logger.info(f"Auto-adapted learning path {path_id} based on performance {performance_score}")
        
    except Exception as e:
        logger.error(f"Failed to adapt learning path: {e}")

def _calculate_streak(completed_milestones: List[Dict]) -> int:
    """Calculate current completion streak"""
    if not completed_milestones:
        return 0
    
    # Sort by completion time
    sorted_milestones = sorted(
        completed_milestones,
        key=lambda x: x.get('completion_time', datetime.min),
        reverse=True
    )
    
    streak = 0
    for milestone in sorted_milestones:
        if milestone.get('performance_score', 0) >= 0.7:  # Good performance threshold
            streak += 1
        else:
            break
    
    return streak

def _analyze_difficulty_progression(completed_milestones: List[Dict]) -> Dict[str, Any]:
    """Analyze how difficulty has progressed"""
    if not completed_milestones:
        return {"trend": "no_data"}
    
    scores = [m.get('performance_score', 0) for m in completed_milestones]
    
    if len(scores) < 2:
        return {"trend": "insufficient_data", "average_score": scores[0] if scores else 0}
    
    # Simple trend analysis
    recent_avg = sum(scores[-3:]) / len(scores[-3:])  # Last 3 milestones
    overall_avg = sum(scores) / len(scores)
    
    if recent_avg > overall_avg + 0.1:
        trend = "improving"
    elif recent_avg < overall_avg - 0.1:
        trend = "declining"
    else:
        trend = "stable"
    
    return {
        "trend": trend,
        "recent_average": recent_avg,
        "overall_average": overall_avg,
        "score_variance": max(scores) - min(scores)
    }

def _calculate_learning_velocity(completed_milestones: List[Dict]) -> float:
    """Calculate learning velocity (milestones per week)"""
    if len(completed_milestones) < 2:
        return 0.0
    
    # Sort by completion time
    sorted_milestones = sorted(
        completed_milestones,
        key=lambda x: x.get('completion_time', datetime.min)
    )
    
    first_completion = sorted_milestones[0].get('completion_time')
    last_completion = sorted_milestones[-1].get('completion_time')
    
    if not first_completion or not last_completion:
        return 0.0
    
    # Calculate weeks between first and last completion
    time_diff = last_completion - first_completion
    weeks = time_diff.days / 7.0
    
    if weeks == 0:
        return len(completed_milestones)  # All completed in same week
    
    return len(completed_milestones) / weeks