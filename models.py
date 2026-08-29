import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.database import Base

class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    ASSESSMENT_SCHEDULED = "ASSESSMENT_SCHEDULED"
    ASSESSMENT_COMPLETED = "ASSESSMENT_COMPLETED"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    OFFER_EXTENDED = "OFFER_EXTENDED"
    OFFER_ACCEPTED = "OFFER_ACCEPTED"
    OFFER_REJECTED = "OFFER_REJECTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opportunity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    resume_text = Column(Text, nullable=False)

    # 🤖 AI-Generated Fields
    match_score = Column(Float, default=0.0)             # AI Match Score (0.0 - 100.0%)
    ai_verdict = Column(String(50), nullable=True)       # "STRONG_MATCH", "POTENTIAL_MATCH", "LOW_FIT"
    ai_screening_summary = Column(Text, nullable=True)   # AI Recruiter Summary
    ai_strengths = Column(JSON, default=list)            # Top matching skills
    ai_flags = Column(JSON, default=list)                # Missing skills / flags

    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.APPLIED, nullable=False)
    notes = Column(Text, nullable=True)                  # Recruiter internal notes
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    interviews = relationship("InterviewSlot", back_populates="application", cascade="all, delete-orphan")
    assessments = relationship("AssessmentRecord", back_populates="application", cascade="all, delete-orphan")
    offer = relationship("JobOffer", back_populates="application", uselist=False, cascade="all, delete-orphan")

class InterviewSlot(Base):
    __tablename__ = "interview_slots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), nullable=False)
    round_name = Column(String(100), nullable=False)     # e.g., "Technical Round 1"
    scheduled_time = Column(DateTime, nullable=False)
    interviewer_name = Column(String(100), nullable=False)
    meeting_link = Column(String(255), nullable=True)
    feedback = Column(Text, nullable=True)
    status = Column(String(50), default="SCHEDULED")     # "SCHEDULED", "COMPLETED", "CANCELLED"

    application = relationship("Application", back_populates="interviews")

class AssessmentRecord(Base):
    __tablename__ = "assessment_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), nullable=False)
    assessment_name = Column(String(150), nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, default=100.0)
    passed = Column(Boolean, default=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="assessments")

class JobOffer(Base):
    __tablename__ = "job_offers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), unique=True, nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    offered_salary_or_stipend = Column(String(100), nullable=False)
    joining_date = Column(DateTime, nullable=False)
    offer_letter_text = Column(Text, nullable=False)
    status = Column(String(50), default="EXTENDED")      # "EXTENDED", "ACCEPTED", "REJECTED"
    extended_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, nullable=True)

    application = relationship("Application", back_populates="offer")