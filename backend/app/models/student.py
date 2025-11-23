from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    age = Column(Integer)
    grade_level = Column(String)
    learning_style = Column(String)  # visual, auditory, reading, kinesthetic
    interests = Column(JSON)  # Student interests
    target_exams = Column(JSON)  # ["WASSCE", "SAT"]
    exam_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    goals = relationship("StudentGoal", back_populates="student")
    learning_paths = relationship("StudentLearningPath", back_populates="student")
    quiz_results = relationship("StudentQuizResult", back_populates="student")
    progress_snapshots = relationship("ProgressSnapshot", back_populates="student")

class StudentGoal(Base):
    __tablename__ = "student_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    goals = Column(Text, nullable=False)
    subject_focus = Column(JSON)  # ["Mathematics", "Physics"]
    strengths = Column(Text)
    weaknesses = Column(Text)
    timeline = Column(DateTime)
    study_material_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="goals")

class StudentLearningPath(Base):
    __tablename__ = "student_learning_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    curriculum_id = Column(Integer, ForeignKey("curricula.id"))
    title = Column(String)
    description = Column(Text)
    total_weeks = Column(Integer)
    difficulty_level = Column(String)  # beginner, intermediate, advanced
    path_data = Column(JSON)  # AI-generated path structure
    progress_data = Column(JSON)  # Progress tracking data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    student = relationship("Student", back_populates="learning_paths")
    weekly_plans = relationship("WeeklyPlan", back_populates="learning_path")

class WeeklyPlan(Base):
    __tablename__ = "weekly_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    learning_path_id = Column(Integer, ForeignKey("student_learning_paths.id"))
    week_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    topics = Column(JSON)  # ["Linear Equations", "Quadratic Functions"]
    estimated_hours = Column(Float)
    difficulty = Column(String)
    progress_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    learning_path = relationship("StudentLearningPath", back_populates="weekly_plans")
    daily_tasks = relationship("DailyTask", back_populates="weekly_plan")

class DailyTask(Base):
    __tablename__ = "daily_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    weekly_plan_id = Column(Integer, ForeignKey("weekly_plans.id"))
    day_of_week = Column(Integer)  # 1-7
    task_type = Column(String)  # lesson, practice, quiz, reading
    title = Column(String, nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer)
    priority = Column(String)  # high, medium, low
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    weekly_plan = relationship("WeeklyPlan", back_populates="daily_tasks")

class StudentQuiz(Base):
    __tablename__ = "student_quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    questions = Column(JSON)  # AI-generated questions
    time_limit_minutes = Column(Integer)
    total_points = Column(Integer)
    quiz_type = Column(String)  # daily, weekly, assessment
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    results = relationship("StudentQuizResult", back_populates="quiz")

class StudentQuizResult(Base):
    __tablename__ = "student_quiz_results"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    quiz_id = Column(Integer, ForeignKey("student_quizzes.id"))
    answers = Column(JSON)  # Student's answers
    score_percentage = Column(Float)
    correct_answers = Column(Integer)
    total_questions = Column(Integer)
    time_taken_minutes = Column(Float)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    student = relationship("Student", back_populates="quiz_results")
    quiz = relationship("StudentQuiz", back_populates="results")

class ProgressSnapshot(Base):
    __tablename__ = "progress_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DateTime, default=datetime.utcnow)
    overall_progress = Column(Float)  # 0-100
    subject_mastery = Column(JSON)  # {"Math": 85, "Physics": 72}
    tasks_completed = Column(Integer)
    quizzes_taken = Column(Integer)
    average_score = Column(Float)
    study_streak = Column(Integer)
    recommendations = Column(JSON)  # AI-generated recommendations
    
    student = relationship("Student", back_populates="progress_snapshots")

class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    answers = Column(JSON)  # Student's answers
    scores = Column(JSON)  # Individual question scores
    total_score = Column(Float)
    max_score = Column(Float)
    feedback = Column(JSON)  # AI-generated feedback
    completed_at = Column(DateTime, default=datetime.utcnow)
    time_taken_minutes = Column(Float)
    
    student = relationship("Student")
    assessment = relationship("Assessment")

class LearningAnalytics(Base):
    __tablename__ = "learning_analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    curriculum_id = Column(Integer, ForeignKey("curricula.id"))
    subject = Column(String)
    concept = Column(String)
    mastery_level = Column(Float)  # 0-100
    mastery_data = Column(JSON)  # Detailed mastery analysis
    misconceptions = Column(JSON)  # Common misconceptions
    learning_gaps = Column(JSON)  # Identified learning gaps
    recommendations = Column(JSON)  # AI recommendations
    attempts_count = Column(Integer)
    success_rate = Column(Float)
    last_practiced = Column(DateTime)
    difficulty_preference = Column(String)
    learning_velocity = Column(Float)  # concepts per week
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    student = relationship("Student")