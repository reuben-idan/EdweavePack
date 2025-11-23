from celery import Celery
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from ..database import get_db
from ..models.student import Student, StudentGoal, LearningPath, WeeklyPlan, DailyTask, StudentQuiz, ProgressSnapshot
from ..agents.learning_path_agent import LearningPathAgent
from ..agents.quiz_generator_agent import QuizGeneratorAgent

celery_app = Celery('student_tasks')

@celery_app.task
def generate_learning_path(student_id: int, goal_id: int):
    """Generate personalized learning path using AI"""
    db = next(get_db())
    
    student = db.query(Student).filter(Student.id == student_id).first()
    goal = db.query(StudentGoal).filter(StudentGoal.id == goal_id).first()
    
    if not student or not goal:
        return {"error": "Student or goal not found"}
    
    # Use AI agent to generate learning path
    agent = LearningPathAgent()
    path_data = agent.generate_path({
        "student_profile": {
            "age": student.age,
            "learning_style": student.learning_style,
            "target_exams": student.target_exams,
            "exam_date": student.exam_date
        },
        "goals": {
            "objectives": goal.goals,
            "subjects": goal.subject_focus,
            "strengths": goal.strengths,
            "weaknesses": goal.weaknesses,
            "timeline": goal.timeline
        }
    })
    
    # Create learning path
    learning_path = LearningPath(
        student_id=student_id,
        title=path_data["title"],
        description=path_data["description"],
        total_weeks=path_data["total_weeks"],
        difficulty_level=path_data["difficulty_level"],
        metadata=path_data["metadata"]
    )
    db.add(learning_path)
    db.commit()
    db.refresh(learning_path)
    
    # Generate weekly plans
    generate_weekly_plan.delay(learning_path.id, path_data["weekly_structure"])
    
    return {"learning_path_id": learning_path.id, "status": "generated"}

@celery_app.task
def generate_weekly_plan(learning_path_id: int, weekly_structure: dict):
    """Generate weekly plans for learning path"""
    db = next(get_db())
    
    for week_data in weekly_structure["weeks"]:
        weekly_plan = WeeklyPlan(
            learning_path_id=learning_path_id,
            week_number=week_data["week_number"],
            title=week_data["title"],
            topics=week_data["topics"],
            estimated_hours=week_data["estimated_hours"],
            difficulty=week_data["difficulty"]
        )
        db.add(weekly_plan)
        db.commit()
        db.refresh(weekly_plan)
        
        # Generate daily tasks for this week
        generate_daily_tasks.delay(weekly_plan.id, week_data["daily_structure"])
    
    return {"status": "weekly_plans_generated"}

@celery_app.task
def generate_daily_tasks(weekly_plan_id: int, daily_structure: dict):
    """Generate daily tasks for a weekly plan"""
    db = next(get_db())
    
    for day_data in daily_structure["days"]:
        for task_data in day_data["tasks"]:
            daily_task = DailyTask(
                weekly_plan_id=weekly_plan_id,
                day_of_week=day_data["day_of_week"],
                task_type=task_data["type"],
                title=task_data["title"],
                description=task_data["description"],
                duration_minutes=task_data["duration"],
                priority=task_data["priority"]
            )
            db.add(daily_task)
    
    db.commit()
    return {"status": "daily_tasks_generated"}

@celery_app.task
def generate_student_quiz(student_id: int, topic: str, difficulty: str = "medium"):
    """Generate AI-powered quiz for student"""
    db = next(get_db())
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return {"error": "Student not found"}
    
    # Use AI agent to generate quiz
    agent = QuizGeneratorAgent()
    quiz_data = agent.generate_quiz({
        "topic": topic,
        "difficulty": difficulty,
        "learning_style": student.learning_style,
        "target_exams": student.target_exams,
        "question_count": 10,
        "question_types": ["mcq", "short_answer"]
    })
    
    # Create quiz
    quiz = StudentQuiz(
        student_id=student_id,
        title=quiz_data["title"],
        description=quiz_data["description"],
        questions=quiz_data["questions"],
        time_limit_minutes=quiz_data["time_limit"],
        total_points=quiz_data["total_points"],
        quiz_type="topic_quiz"
    )
    db.add(quiz)
    db.commit()
    
    return {"quiz_id": quiz.id, "status": "generated"}

@celery_app.task
def analyze_student_progress(student_id: int):
    """Analyze student progress and generate recommendations"""
    db = next(get_db())
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return {"error": "Student not found"}
    
    # Calculate progress metrics
    learning_path = db.query(LearningPath).filter(
        LearningPath.student_id == student_id,
        LearningPath.is_active == True
    ).first()
    
    if not learning_path:
        return {"error": "No active learning path"}
    
    # Get completed tasks
    completed_tasks = db.query(DailyTask).join(WeeklyPlan).filter(
        WeeklyPlan.learning_path_id == learning_path.id,
        DailyTask.is_completed == True
    ).count()
    
    total_tasks = db.query(DailyTask).join(WeeklyPlan).filter(
        WeeklyPlan.learning_path_id == learning_path.id
    ).count()
    
    # Get quiz performance
    from sqlalchemy import func
    quiz_stats = db.query(
        func.avg(StudentQuizResult.score_percentage).label('avg_score'),
        func.count(StudentQuizResult.id).label('quiz_count')
    ).filter(StudentQuizResult.student_id == student_id).first()
    
    # Calculate subject mastery
    subject_mastery = {}
    for subject in student.goals[0].subject_focus if student.goals else []:
        # Mock calculation - in real implementation, analyze quiz results by subject
        subject_mastery[subject] = min(85, (completed_tasks / max(total_tasks, 1)) * 100 + 10)
    
    # Generate AI recommendations
    recommendations = generate_recommendations(student, completed_tasks, total_tasks, quiz_stats)
    
    # Create progress snapshot
    progress = ProgressSnapshot(
        student_id=student_id,
        overall_progress=(completed_tasks / max(total_tasks, 1)) * 100,
        subject_mastery=subject_mastery,
        tasks_completed=completed_tasks,
        quizzes_taken=quiz_stats.quiz_count or 0,
        average_score=quiz_stats.avg_score or 0,
        study_streak=calculate_study_streak(student_id, db),
        recommendations=recommendations
    )
    db.add(progress)
    db.commit()
    
    return {"progress_id": progress.id, "status": "analyzed"}

def generate_recommendations(student, completed_tasks, total_tasks, quiz_stats):
    """Generate AI-powered recommendations"""
    recommendations = []
    
    completion_rate = (completed_tasks / max(total_tasks, 1)) * 100
    avg_score = quiz_stats.avg_score or 0
    
    if completion_rate < 50:
        recommendations.append({
            "type": "focus",
            "title": "Increase Study Consistency",
            "description": "You've completed less than 50% of tasks. Try setting daily study reminders.",
            "priority": "high"
        })
    
    if avg_score < 70:
        recommendations.append({
            "type": "review",
            "title": "Review Fundamental Concepts",
            "description": "Your quiz scores suggest reviewing basic concepts before advancing.",
            "priority": "high"
        })
    
    if avg_score > 85:
        recommendations.append({
            "type": "advance",
            "title": "Ready for Advanced Topics",
            "description": "Excellent performance! Consider moving to more challenging material.",
            "priority": "medium"
        })
    
    return recommendations

def calculate_study_streak(student_id: int, db: Session) -> int:
    """Calculate consecutive days of study activity"""
    # Get recent task completions
    recent_completions = db.query(DailyTask.completed_at).join(WeeklyPlan).join(LearningPath).filter(
        LearningPath.student_id == student_id,
        DailyTask.is_completed == True,
        DailyTask.completed_at >= datetime.now() - timedelta(days=30)
    ).order_by(DailyTask.completed_at.desc()).all()
    
    if not recent_completions:
        return 0
    
    # Calculate streak
    streak = 1
    current_date = recent_completions[0].completed_at.date()
    
    for completion in recent_completions[1:]:
        completion_date = completion.completed_at.date()
        if (current_date - completion_date).days == 1:
            streak += 1
            current_date = completion_date
        else:
            break
    
    return streak