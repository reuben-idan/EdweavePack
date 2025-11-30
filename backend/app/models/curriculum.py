from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Curriculum(Base):
    __tablename__ = "curricula"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    grade_level = Column(String, nullable=False)
    description = Column(Text)
    content_data = Column(JSON)
    ai_generated = Column(Boolean, default=True)
    amazon_q_powered = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    curriculum_id = Column(Integer, ForeignKey("curricula.id"))
    assessment_data = Column(JSON)
    total_points = Column(Integer, default=100)
    time_limit = Column(Integer)
    ai_generated = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())