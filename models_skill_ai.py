import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base

class Course(Base):
    __tablename__ = "academic_courses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_code = Column(String(50), unique=True, nullable=False)
    title = Column(String(150), nullable=False)
    department = Column(String(100), nullable=False)
    syllabus_text = Column(Text, nullable=True) # Full text syllabus for AI parsing
    extracted_skills = Column(JSON, default=list) # Stored AI-extracted skills

class UserLearningProfile(Base):
    """Stores a student's or faculty's unstructured career background, goals, and interests."""
    __tablename__ = "user_learning_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    target_role_or_domain = Column(String(150), nullable=True) # e.g., "Full-Stack AI Engineer" / "Quantum Computing Research"
    interests = Column(JSON, default=list)                     # e.g., ["Robotics", "Edge AI", "Computer Vision"]
    raw_bio_or_resume = Column(Text, nullable=True)
    known_skills = Column(JSON, default=list)                  # e.g., [{"skill": "Python", "level": "Advanced"}]
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AIAnalysisLog(Base):
    """Audit log of generated AI gap analyses and recommendations."""
    __tablename__ = "ai_analysis_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    analysis_type = Column(String(50), nullable=False) # "GAP_ANALYSIS", "RECOMMENDATIONS", "SYLLABUS_EXTRACTION"
    input_payload = Column(JSON, nullable=False)
    ai_response = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)