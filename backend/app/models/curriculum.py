from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Curriculum(Base):
    __tablename__ = "curricula"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    subject = Column(String, nullable=False)
    grade_level = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_content = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="curricula")
    learning_paths = relationship("LearningPath", back_populates="curriculum")
    assessments = relationship("Assessment", back_populates="curriculum")
    modules = relationship("Module", back_populates="curriculum")

class LearningPath(Base):
    __tablename__ = "learning_paths"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    curriculum_id = Column(Integer, ForeignKey("curricula.id"), nullable=False)
    sequence_order = Column(Integer, nullable=False)
    content = Column(JSON)
    estimated_duration = Column(Integer)  # minutes
    
    curriculum = relationship("Curriculum", back_populates="learning_paths")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    curriculum_id = Column(Integer, ForeignKey("curricula.id"), nullable=False)
    assessment_type = Column(String, nullable=False)  # quiz, test, assignment
    total_points = Column(Integer, default=0)
    time_limit = Column(Integer)  # minutes
    
    curriculum = relationship("Curriculum", back_populates="assessments")
    questions = relationship("Question", back_populates="assessment")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # multiple_choice, short_answer, essay
    options = Column(JSON)  # for multiple choice
    correct_answer = Column(Text)
    points = Column(Integer, default=1)
    explanation = Column(Text)
    
    assessment = relationship("Assessment", back_populates="questions")