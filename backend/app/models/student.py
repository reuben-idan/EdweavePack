from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    grade_level = Column(String)
    learning_style = Column(String)  # visual, auditory, kinesthetic, mixed
    interests = Column(JSON)  # Array of interests
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    learning_paths = relationship("PersonalizedPath", back_populates="student")
    assessment_attempts = relationship("AssessmentAttempt", back_populates="student")

class PersonalizedPath(Base):
    __tablename__ = "personalized_paths"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    curriculum_id = Column(Integer, ForeignKey("curricula.id"), nullable=False)
    path_data = Column(JSON)  # Customized learning sequence
    progress = Column(JSON)  # Progress tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="learning_paths")

class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    answers = Column(JSON)  # Student responses
    scores = Column(JSON)  # Individual question scores
    total_score = Column(Float)
    max_score = Column(Float)
    feedback = Column(JSON)  # AI-generated feedback
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="assessment_attempts")

class LearningAnalytics(Base):
    __tablename__ = "learning_analytics"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    curriculum_id = Column(Integer, ForeignKey("curricula.id"), nullable=False)
    mastery_data = Column(JSON)  # Concept mastery levels
    misconceptions = Column(JSON)  # Identified misconceptions
    learning_gaps = Column(JSON)  # Areas needing work
    recommendations = Column(JSON)  # AI recommendations
    generated_at = Column(DateTime(timezone=True), server_default=func.now())