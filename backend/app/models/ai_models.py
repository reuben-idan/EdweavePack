from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class AIInteraction(Base):
    """Track AI interactions and responses"""
    __tablename__ = "ai_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    interaction_type = Column(String, nullable=False)  # chat, curriculum_gen, assessment_gen, etc.
    input_data = Column(JSON)
    output_data = Column(JSON)
    ai_service = Column(String)  # bedrock, comprehend, textract, etc.
    model_used = Column(String)  # claude-3, titan, etc.
    tokens_used = Column(Integer, default=0)
    processing_time = Column(Float)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LearningAnalytics(Base):
    """Store AI-generated learning analytics"""
    __tablename__ = "learning_analytics"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    curriculum_id = Column(Integer, ForeignKey("curricula.id"), nullable=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)
    analytics_type = Column(String)  # performance, prediction, recommendation
    insights = Column(JSON)
    confidence_score = Column(Float)
    generated_by = Column(String)  # ai_service used
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PersonalizedContent(Base):
    """Store AI-personalized content for students"""
    __tablename__ = "personalized_content"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    original_content_id = Column(Integer)  # Reference to original curriculum/lesson
    content_type = Column(String)  # explanation, practice, assessment
    personalized_data = Column(JSON)
    learning_style = Column(String)  # visual, auditory, kinesthetic
    difficulty_level = Column(String)
    ai_generated = Column(Boolean, default=True)
    effectiveness_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AIRecommendation(Base):
    """Store AI-generated recommendations"""
    __tablename__ = "ai_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recommendation_type = Column(String)  # teaching_strategy, study_plan, content_improvement
    target_entity_type = Column(String)  # curriculum, assessment, student
    target_entity_id = Column(Integer)
    recommendation_data = Column(JSON)
    priority = Column(String, default="medium")  # low, medium, high
    status = Column(String, default="pending")  # pending, accepted, rejected, implemented
    ai_confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ContentAnalysis(Base):
    """Store AI analysis of uploaded content"""
    __tablename__ = "content_analysis"

    id = Column(Integer, primary_key=True, index=True)
    content_source = Column(String)  # s3_key, url, text
    content_type = Column(String)  # pdf, docx, video, text
    extracted_text = Column(Text)
    entities = Column(JSON)  # Comprehend entities
    key_phrases = Column(JSON)  # Comprehend key phrases
    sentiment = Column(JSON)  # Comprehend sentiment
    topics = Column(JSON)  # Identified topics
    difficulty_level = Column(String)
    reading_level = Column(String)
    language = Column(String, default="en")
    ai_services_used = Column(JSON)  # List of AWS services used
    processing_status = Column(String, default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StudyPlan(Base):
    """AI-generated personalized study plans"""
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    curriculum_id = Column(Integer, ForeignKey("curricula.id"), nullable=True)
    plan_name = Column(String)
    goals = Column(JSON)  # Learning goals
    schedule = Column(JSON)  # Weekly/daily schedule
    milestones = Column(JSON)  # Progress milestones
    adaptive_adjustments = Column(JSON)  # AI adjustments based on progress
    estimated_completion = Column(DateTime)
    actual_completion = Column(DateTime, nullable=True)
    effectiveness_rating = Column(Float, nullable=True)
    ai_generated = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIFeedback(Base):
    """Store AI-generated feedback on student work"""
    __tablename__ = "ai_feedback"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    question_id = Column(Integer)
    student_response = Column(Text)
    ai_score = Column(Float)
    max_score = Column(Float)
    feedback_text = Column(Text)
    strengths = Column(JSON)
    improvements = Column(JSON)
    ai_model_used = Column(String)
    confidence_score = Column(Float)
    human_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())