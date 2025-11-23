from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # S3 path
    file_size = Column(BigInteger, nullable=False)
    content_type = Column(String, nullable=False)
    upload_status = Column(String, default="pending")  # pending, processing, completed, failed
    extracted_content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="files")

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    curriculum_id = Column(Integer, ForeignKey("curricula.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    sequence_order = Column(Integer, nullable=False)
    bloom_level = Column(String, nullable=False)
    estimated_duration = Column(Integer)  # minutes
    content_data = Column(Text)  # JSON string
    activities = Column(Text)  # JSON string
    resources = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    curriculum = relationship("Curriculum", back_populates="modules")

class StudentResponse(Base):
    __tablename__ = "student_responses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    assessment_attempt_id = Column(Integer, ForeignKey("assessment_attempts.id"), nullable=False)
    response_text = Column(Text)
    is_correct = Column(String)  # correct, incorrect, partial
    points_earned = Column(Integer, default=0)
    ai_feedback = Column(Text)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student")
    question = relationship("Question")
    assessment_attempt = relationship("AssessmentAttempt")