from celery import current_task
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.curriculum import Assessment, Question
from app.models.student import AssessmentAttempt, StudentResponse
from app.services.ai_service import AIService
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def assessment_generation(self, curriculum_id: int, assessment_type: str = "mixed"):
    """Generate assessment questions using AI"""
    db = SessionLocal()
    
    try:
        current_task.update_state(state='PROGRESS', meta={'progress': 10})
        
        from app.models.curriculum import Curriculum
        
        # Get curriculum
        curriculum = db.query(Curriculum).filter(Curriculum.id == curriculum_id).first()
        if not curriculum:
            raise Exception(f"Curriculum {curriculum_id} not found")
        
        current_task.update_state(state='PROGRESS', meta={'progress': 30})
        
        # Generate assessment using AI
        ai_service = AIService()
        assessment_data = await ai_service.generate_assessments(curriculum.metadata, assessment_type)
        
        current_task.update_state(state='PROGRESS', meta={'progress': 60})
        
        # Create assessment record
        assessment = Assessment(
            title=assessment_data.get("title", f"AI-Generated {assessment_type.title()} Assessment"),
            description=assessment_data.get("assessment_overview", "Comprehensive assessment"),
            curriculum_id=curriculum_id,
            assessment_type=assessment_type,
            total_points=assessment_data.get("total_points", 100),
            time_limit=assessment_data.get("time_limit", 90)
        )
        
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        # Create questions
        questions_created = 0
        for q_data in assessment_data.get("questions", []):
            question = Question(
                assessment_id=assessment.id,
                question_text=q_data["question_text"],
                question_type=q_data["question_type"],
                options=q_data.get("options"),
                correct_answer=q_data.get("correct_answer", q_data.get("sample_answer", "")),
                points=q_data.get("points", 5),
                explanation=q_data.get("explanation", "")
            )
            db.add(question)
            questions_created += 1
        
        db.commit()
        
        current_task.update_state(state='PROGRESS', meta={'progress': 100})
        
        return {
            "assessment_id": assessment.id,
            "curriculum_id": curriculum_id,
            "status": "completed",
            "questions_created": questions_created,
            "total_points": assessment.total_points
        }
        
    except Exception as e:
        logger.error(f"Assessment generation failed for curriculum {curriculum_id}: {str(e)}")
        raise Exception(f"Assessment generation failed: {str(e)}")
        
    finally:
        db.close()

@celery_app.task(bind=True)
def grading(self, assessment_attempt_id: int):
    """Grade student assessment responses using AI"""
    db = SessionLocal()
    
    try:
        current_task.update_state(state='PROGRESS', meta={'progress': 10})
        
        # Get assessment attempt
        attempt = db.query(AssessmentAttempt).filter(
            AssessmentAttempt.id == assessment_attempt_id
        ).first()
        
        if not attempt:
            raise Exception(f"Assessment attempt {assessment_attempt_id} not found")
        
        current_task.update_state(state='PROGRESS', meta={'progress': 30})
        
        # Get all questions for this assessment
        questions = db.query(Question).filter(
            Question.assessment_id == attempt.assessment_id
        ).all()
        
        ai_service = AIService()
        total_earned = 0
        total_possible = 0
        detailed_feedback = {}
        
        current_task.update_state(state='PROGRESS', meta={'progress': 50})
        
        # Grade each response
        for question in questions:
            total_possible += question.points
            user_answer = attempt.answers.get(str(question.id), "")
            
            # Prepare question data for AI grading
            question_data = {
                "question_text": question.question_text,
                "question_type": question.question_type,
                "points": question.points,
                "correct_answer": question.correct_answer,
                "options": question.options
            }
            
            # Auto-grade using AI service
            grading_result = await ai_service.auto_grade_response(question_data, user_answer)
            
            # Create student response record
            student_response = StudentResponse(
                student_id=attempt.student_id,
                question_id=question.id,
                assessment_attempt_id=assessment_attempt_id,
                response_text=user_answer,
                is_correct="correct" if grading_result.get("is_correct", False) else "incorrect",
                points_earned=grading_result["score"],
                ai_feedback=grading_result.get("feedback", "")
            )
            
            db.add(student_response)
            
            total_earned += grading_result["score"]
            detailed_feedback[str(question.id)] = grading_result
        
        current_task.update_state(state='PROGRESS', meta={'progress': 80})
        
        # Update assessment attempt with final scores
        attempt.total_score = total_earned
        attempt.max_score = total_possible
        attempt.feedback = detailed_feedback
        
        db.commit()
        
        current_task.update_state(state='PROGRESS', meta={'progress': 100})
        
        percentage = (total_earned / total_possible * 100) if total_possible > 0 else 0
        
        return {
            "assessment_attempt_id": assessment_attempt_id,
            "status": "completed",
            "total_score": total_earned,
            "max_score": total_possible,
            "percentage": round(percentage, 2),
            "passed": percentage >= 70
        }
        
    except Exception as e:
        logger.error(f"Grading failed for attempt {assessment_attempt_id}: {str(e)}")
        raise Exception(f"Grading failed: {str(e)}")
        
    finally:
        db.close()

@celery_app.task(bind=True)
def batch_grade_assessments(self, assessment_id: int):
    """Grade all pending attempts for an assessment"""
    db = SessionLocal()
    
    try:
        # Get all ungraded attempts
        pending_attempts = db.query(AssessmentAttempt).filter(
            AssessmentAttempt.assessment_id == assessment_id,
            AssessmentAttempt.total_score.is_(None)
        ).all()
        
        results = []
        for i, attempt in enumerate(pending_attempts):
            current_task.update_state(
                state='PROGRESS', 
                meta={'progress': int((i / len(pending_attempts)) * 100)}
            )
            
            # Grade individual attempt
            result = grading.delay(attempt.id)
            results.append(result.get())
        
        return {
            "assessment_id": assessment_id,
            "attempts_graded": len(results),
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Batch grading failed for assessment {assessment_id}: {str(e)}")
        raise Exception(f"Batch grading failed: {str(e)}")
        
    finally:
        db.close()