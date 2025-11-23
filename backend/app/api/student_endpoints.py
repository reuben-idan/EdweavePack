from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json

from ..database import get_db
from ..models.student import Student, StudentGoal, LearningPath, WeeklyPlan, DailyTask, StudentQuiz, StudentQuizResult, ProgressSnapshot
from ..schemas.student import StudentCreate, StudentGoalCreate, QuizSubmission, StudentResponse
from ..core.security import get_current_student, create_access_token
from ..tasks.student_tasks import generate_learning_path, generate_weekly_plan, generate_daily_tasks, generate_student_quiz, analyze_student_progress

router = APIRouter(prefix="/student", tags=["student"])

@router.post("/auth/register", response_model=StudentResponse)
async def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if student exists
    db_student = db.query(Student).filter(Student.email == student.email).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create student
    hashed_password = hash_password(student.password)
    db_student = Student(
        email=student.email,
        name=student.name,
        hashed_password=hashed_password,
        age=student.age,
        learning_style=student.learning_style,
        target_exams=student.target_exams,
        exam_date=student.exam_date
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    # Generate access token
    access_token = create_access_token(data={"sub": db_student.email, "type": "student"})
    
    return {"student": db_student, "access_token": access_token, "token_type": "bearer"}

@router.post("/goals")
async def create_student_goals(
    goals: StudentGoalCreate,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    # Create student goals
    db_goals = StudentGoal(
        student_id=current_student.id,
        goals=goals.goals,
        subject_focus=goals.subject_focus,
        strengths=goals.strengths,
        weaknesses=goals.weaknesses,
        timeline=goals.timeline,
        study_material_url=goals.study_material_url
    )
    db.add(db_goals)
    db.commit()
    
    # Trigger AI learning path generation
    generate_learning_path.delay(current_student.id, db_goals.id)
    
    return {"message": "Goals saved successfully. AI is generating your personalized learning path."}

@router.get("/learning-path")
async def get_learning_path(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    learning_path = db.query(LearningPath).filter(
        LearningPath.student_id == current_student.id,
        LearningPath.is_active == True
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="No active learning path found")
    
    # Get weekly plans
    weekly_plans = db.query(WeeklyPlan).filter(
        WeeklyPlan.learning_path_id == learning_path.id
    ).order_by(WeeklyPlan.week_number).all()
    
    return {
        "learning_path": learning_path,
        "weekly_plans": weekly_plans,
        "total_weeks": learning_path.total_weeks
    }

@router.get("/daily-plan")
async def get_daily_plan(
    date: Optional[str] = None,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    target_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    day_of_week = target_date.weekday() + 1  # 1-7
    
    # Get current week's plan
    learning_path = db.query(LearningPath).filter(
        LearningPath.student_id == current_student.id,
        LearningPath.is_active == True
    ).first()
    
    if not learning_path:
        return {"tasks": [], "message": "No active learning path"}
    
    # Calculate current week number
    weeks_since_start = (target_date - learning_path.created_at).days // 7 + 1
    
    weekly_plan = db.query(WeeklyPlan).filter(
        WeeklyPlan.learning_path_id == learning_path.id,
        WeeklyPlan.week_number == weeks_since_start
    ).first()
    
    if not weekly_plan:
        return {"tasks": [], "message": "No plan for this week"}
    
    # Get daily tasks
    daily_tasks = db.query(DailyTask).filter(
        DailyTask.weekly_plan_id == weekly_plan.id,
        DailyTask.day_of_week == day_of_week
    ).all()
    
    return {"tasks": daily_tasks, "weekly_plan": weekly_plan}

@router.get("/weekly-plan/{week_number}")
async def get_weekly_plan(
    week_number: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    learning_path = db.query(LearningPath).filter(
        LearningPath.student_id == current_student.id,
        LearningPath.is_active == True
    ).first()
    
    if not learning_path:
        raise HTTPException(status_code=404, detail="No active learning path")
    
    weekly_plan = db.query(WeeklyPlan).filter(
        WeeklyPlan.learning_path_id == learning_path.id,
        WeeklyPlan.week_number == week_number
    ).first()
    
    if not weekly_plan:
        raise HTTPException(status_code=404, detail="Week not found")
    
    # Get daily tasks for the week
    daily_tasks = db.query(DailyTask).filter(
        DailyTask.weekly_plan_id == weekly_plan.id
    ).order_by(DailyTask.day_of_week).all()
    
    return {"weekly_plan": weekly_plan, "daily_tasks": daily_tasks}

@router.get("/quiz")
async def get_available_quizzes(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    quizzes = db.query(StudentQuiz).filter(
        StudentQuiz.student_id == current_student.id,
        StudentQuiz.is_active == True
    ).all()
    
    # Add result status for each quiz
    quiz_data = []
    for quiz in quizzes:
        result = db.query(StudentQuizResult).filter(
            StudentQuizResult.student_id == current_student.id,
            StudentQuizResult.quiz_id == quiz.id
        ).first()
        
        quiz_data.append({
            "quiz": quiz,
            "status": "completed" if result else "available",
            "score": result.score_percentage if result else None,
            "attempts": 1 if result else 0
        })
    
    return {"quizzes": quiz_data}

@router.get("/quiz/{quiz_id}")
async def get_quiz(
    quiz_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    quiz = db.query(StudentQuiz).filter(
        StudentQuiz.id == quiz_id,
        StudentQuiz.student_id == current_student.id
    ).first()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return quiz

@router.post("/quiz/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: int,
    submission: QuizSubmission,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    quiz = db.query(StudentQuiz).filter(StudentQuiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Auto-grade quiz
    questions = quiz.questions
    correct_answers = 0
    total_questions = len(questions)
    
    for i, question in enumerate(questions):
        user_answer = submission.answers.get(str(i))
        if question.get("type") == "mcq":
            if user_answer == question.get("correct"):
                correct_answers += 1
        elif question.get("type") == "short":
            if user_answer and user_answer.lower().strip() == question.get("correct", "").lower():
                correct_answers += 1
    
    score_percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Save result
    result = StudentQuizResult(
        student_id=current_student.id,
        quiz_id=quiz_id,
        answers=submission.answers,
        score_percentage=score_percentage,
        correct_answers=correct_answers,
        total_questions=total_questions,
        time_taken_minutes=submission.time_taken_minutes
    )
    db.add(result)
    db.commit()
    
    # Trigger progress analysis
    analyze_student_progress.delay(current_student.id)
    
    return {
        "score": score_percentage,
        "correct": correct_answers,
        "total": total_questions,
        "result_id": result.id
    }

@router.get("/progress")
async def get_student_progress(
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    # Get latest progress snapshot
    latest_progress = db.query(ProgressSnapshot).filter(
        ProgressSnapshot.student_id == current_student.id
    ).order_by(ProgressSnapshot.date.desc()).first()
    
    # Get quiz history
    quiz_results = db.query(StudentQuizResult).filter(
        StudentQuizResult.student_id == current_student.id
    ).order_by(StudentQuizResult.submitted_at.desc()).limit(10).all()
    
    # Get task completion stats
    completed_tasks = db.query(DailyTask).join(WeeklyPlan).join(LearningPath).filter(
        LearningPath.student_id == current_student.id,
        DailyTask.is_completed == True
    ).count()
    
    total_tasks = db.query(DailyTask).join(WeeklyPlan).join(LearningPath).filter(
        LearningPath.student_id == current_student.id
    ).count()
    
    return {
        "progress_snapshot": latest_progress,
        "quiz_history": quiz_results,
        "task_completion": {
            "completed": completed_tasks,
            "total": total_tasks,
            "percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }
    }

@router.post("/tasks/{task_id}/complete")
async def complete_task(
    task_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    # Find task through student's learning path
    task = db.query(DailyTask).join(WeeklyPlan).join(LearningPath).filter(
        LearningPath.student_id == current_student.id,
        DailyTask.id == task_id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.is_completed = not task.is_completed
    task.completed_at = datetime.utcnow() if task.is_completed else None
    db.commit()
    
    return {"message": "Task updated successfully", "completed": task.is_completed}

def hash_password(password: str) -> str:
    # Implement password hashing
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)