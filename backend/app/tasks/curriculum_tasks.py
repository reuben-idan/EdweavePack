from celery import current_task
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.curriculum import Curriculum
from app.models.files import Module
from app.services.ai_service import AIService
import json
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def curriculum_generation(self, curriculum_id: int):
    """Generate curriculum content using AI"""
    db = SessionLocal()
    
    try:
        current_task.update_state(state='PROGRESS', meta={'progress': 10})
        
        # Get curriculum record
        curriculum = db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
        if not curriculum:
            raise Exception(f"Curriculum {curriculum_id} not found")
        
        current_task.update_state(state='PROGRESS', meta={'progress': 30})
        
        # Generate curriculum using AI service
        ai_service = AIService()
        curriculum_data = await ai_service.generate_curriculum(
            curriculum.source_content,
            curriculum.subject,
            curriculum.grade_level
        )
        
        current_task.update_state(state='PROGRESS', meta={'progress': 60})
        
        # Update curriculum metadata
        curriculum.metadata = curriculum_data
        db.commit()
        
        # Create individual modules
        for week_data in curriculum_data.get("weekly_modules", []):
            for i, block in enumerate(week_data.get("content_blocks", [])):
                module = Module(
                    title=block["title"],
                    description=block["description"],
                    curriculum_id=curriculum_id,
                    week_number=week_data["week_number"],
                    sequence_order=i + 1,
                    bloom_level=block.get("bloom_level", "Apply"),
                    estimated_duration=block.get("estimated_duration", 60),
                    content_data=json.dumps(block),
                    activities=json.dumps(block.get("activities", [])),
                    resources=json.dumps(block.get("resources", []))
                )
                db.add(module)
        
        db.commit()
        
        current_task.update_state(state='PROGRESS', meta={'progress': 100})
        
        return {
            "curriculum_id": curriculum_id,
            "status": "completed",
            "modules_created": len(curriculum_data.get("weekly_modules", [])),
            "learning_objectives": curriculum_data.get("learning_objectives", [])
        }
        
    except Exception as e:
        logger.error(f"Curriculum generation failed for {curriculum_id}: {str(e)}")
        raise Exception(f"Curriculum generation failed: {str(e)}")
        
    finally:
        db.close()

@celery_app.task(bind=True)
def generate_learning_path(self, student_id: int, curriculum_id: int):
    """Generate personalized learning path for student"""
    db = SessionLocal()
    
    try:
        current_task.update_state(state='PROGRESS', meta={'progress': 20})
        
        from app.models.student import Student, PersonalizedPath
        from app.models.curriculum import Curriculum
        
        # Get student and curriculum
        student = db.query(Student).filter(Student.id == student_id).first()
        curriculum = db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
        
        if not student or not curriculum:
            raise Exception("Student or curriculum not found")
        
        current_task.update_state(state='PROGRESS', meta={'progress': 50})
        
        # Generate personalized path using AI
        ai_service = AIService()
        student_profile = {
            "age": student.age,
            "learning_style": student.learning_style,
            "interests": student.interests or []
        }
        
        path_data = await ai_service.generate_personalized_path(
            student_profile, curriculum.metadata
        )
        
        current_task.update_state(state='PROGRESS', meta={'progress': 80})
        
        # Save or update personalized path
        existing_path = db.query(PersonalizedPath).filter(
            PersonalizedPath.student_id == student_id,
            PersonalizedPath.curriculum_id == curriculum_id
        ).first()
        
        if existing_path:
            existing_path.path_data = path_data
        else:
            new_path = PersonalizedPath(
                student_id=student_id,
                curriculum_id=curriculum_id,
                path_data=path_data,
                progress={"completed_modules": [], "current_week": 1}
            )
            db.add(new_path)
        
        db.commit()
        
        return {
            "student_id": student_id,
            "curriculum_id": curriculum_id,
            "status": "completed",
            "path_generated": True
        }
        
    except Exception as e:
        logger.error(f"Learning path generation failed: {str(e)}")
        raise Exception(f"Learning path generation failed: {str(e)}")
        
    finally:
        db.close()