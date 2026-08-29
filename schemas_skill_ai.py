import uuid
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from enum import Enum

class TargetPersona(str, Enum):
    STUDENT = "STUDENT"
    FACULTY = "FACULTY"

# --- 1. Syllabus & Resume Skill Extraction ---
class ExtractedSkillItem(BaseModel):
    skill_name: str
    category: str = Field(description="e.g. Programming, Cloud, Data Science, Soft Skills")
    proficiency_level: str = Field(description="Beginner, Intermediate, or Advanced")
    context_found: str = Field(description="Short quote or reason why this skill was identified")

class SkillExtractionResponse(BaseModel):
    summary: str
    extracted_skills: List[ExtractedSkillItem]

class TextExtractionRequest(BaseModel):
    raw_text: str = Field(..., min_length=20, description="Raw syllabus, resume, or project description text")

# --- 2. AI Skill Gap Analysis ---
class SkillGapItem(BaseModel):
    skill_name: str
    importance: str = Field(description="Critical, Recommended, or Nice-to-have")
    gap_description: str
    recommended_remedy: str

class AIGapAnalysisRequest(BaseModel):
    target_job_description: str
    user_bio_or_resume: str
    target_role: str

class AIGapAnalysisResponse(BaseModel):
    readiness_score: float = Field(..., ge=0.0, le=100.0, description="Readiness percentage (0-100%)")
    strengths: List[str]
    critical_missing_skills: List[SkillGapItem]
    industry_alignment_summary: str
    immediate_action_items: List[str]

# --- 3. AI Personalized Recommendations ---
class CertificationRecommendation(BaseModel):
    title: str
    platform_provider: str # e.g., AWS, Coursera, Google Cloud, IEEE
    duration: str
    why_recommended: str

class ProjectRecommendation(BaseModel):
    title: str
    domain: str
    difficulty: str # "Beginner", "Intermediate", "Advanced"
    suggested_tech_stack: List[str]
    project_summary: str
    portfolio_impact: str

class OpportunityRecommendation(BaseModel):
    title: str
    type: str # "Industry Internship", "Research Grant", "Corporate Consultancy", "Open Source"
    suggested_domain: str
    relevance_to_goals: str

class AIRecommendationRequest(BaseModel):
    persona: TargetPersona
    career_goals: str
    interests: List[str]
    current_skills: List[str]
    academic_department: Optional[str] = "Computer Science"

class AIRecommendationResponse(BaseModel):
    strategic_pathway_summary: str
    certifications: List[CertificationRecommendation]
    hands_on_projects: List[ProjectRecommendation]
    opportunities: List[OpportunityRecommendation]






    