import uuid
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
from modules.module6_applications.models import ApplicationStatus
from modules.module6_applications.ats_ai_engine import AIInterviewQuestionsResponse

# --- Application Schemas ---
class ApplicationSubmitRequest(BaseModel):
    opportunity_id: uuid.UUID
    resume_text: str
    target_job_title: Optional[str] = "Software Engineer"
    target_job_requirements: Optional[str] = "Python, FastAPI, SQL, Git, Problem Solving"

class ApplicationStatusUpdateRequest(BaseModel):
    status: ApplicationStatus
    notes: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: uuid.UUID
    opportunity_id: uuid.UUID
    student_id: uuid.UUID
    status: ApplicationStatus
    match_score: float
    ai_verdict: Optional[str] = None
    ai_screening_summary: Optional[str] = None
    ai_strengths: List[Any] = []
    ai_flags: List[Any] = []
    notes: Optional[str] = None
    applied_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Interview Schemas ---
class ScheduleInterviewRequest(BaseModel):
    round_name: str
    scheduled_time: datetime
    interviewer_name: str
    meeting_link: Optional[str] = None

class InterviewResponse(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    round_name: str
    scheduled_time: datetime
    interviewer_name: str
    meeting_link: Optional[str]
    status: str
    model_config = ConfigDict(from_attributes=True)

# --- Assessment Schemas ---
class RecordAssessmentRequest(BaseModel):
    assessment_name: str
    score: float
    max_score: float = 100.0
    passed: bool = True

class AssessmentResponse(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    assessment_name: str
    score: float
    max_score: float
    passed: bool
    model_config = ConfigDict(from_attributes=True)

# --- Offer Letter Schemas ---
class ExtendOfferRequest(BaseModel):
    offered_salary_or_stipend: str
    joining_date: datetime
    offer_letter_text: str

class RespondOfferRequest(BaseModel):
    accept: bool  # True = Accept, False = Reject

class JobOfferResponse(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    student_id: uuid.UUID
    offered_salary_or_stipend: str
    joining_date: datetime
    offer_letter_text: str
    status: str
    extended_at: datetime
    responded_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)