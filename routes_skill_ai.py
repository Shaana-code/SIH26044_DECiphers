from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db
from models import User, UserRole
from dependencies import get_current_user, RequireRoles
from models_skill_ai import Course, UserLearningProfile, AIAnalysisLog
from schemas_skill_ai import (
    TextExtractionRequest,
    SkillExtractionResponse,
    AIGapAnalysisRequest,
    AIGapAnalysisResponse,
    AIRecommendationRequest,
    AIRecommendationResponse
)
from ai_skill_engine import (
    ai_extract_skills,
    ai_compute_gap_analysis,
    ai_generate_recommendations
)

ai_skill_router = APIRouter(prefix="/api/v1/ai-skills", tags=["Module 4: AI Skill Mapping & Recommendation Engine"])

# --- 1. AI Text / Syllabus Skill Extraction ---

@ai_skill_router.post("/extract", response_model=SkillExtractionResponse)
async def extract_skills_from_text(
    payload: TextExtractionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    AI Endpoint: Extracts standardized skills, categories, and proficiency from any
    raw text (e.g., Course Syllabus, Student Resume, Project Report).
    """
    try:
        result = await ai_extract_skills(payload.raw_text)
        
        # Log AI action
        log_entry = AIAnalysisLog(
            user_id=current_user.id,
            analysis_type="SKILL_EXTRACTION",
            input_payload={"text_length": len(payload.raw_text)},
            ai_response=result.model_dump()
        )
        db.add(log_entry)
        await db.commit()

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Skill Extraction failed: {str(e)}"
        )

# --- 2. AI Skill Gap Analysis ---

@ai_skill_router.post("/gap-analysis", response_model=AIGapAnalysisResponse)
async def analyze_skill_gap(
    payload: AIGapAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    AI Endpoint: Evaluates a candidate against a target job description and returns:
    - Semantic readiness score (0-100%)
    - Critical missing skills & remedies
    - Immediate action roadmap
    """
    try:
        analysis = await ai_compute_gap_analysis(payload)
        
        log_entry = AIAnalysisLog(
            user_id=current_user.id,
            analysis_type="GAP_ANALYSIS",
            input_payload=payload.model_dump(),
            ai_response=analysis.model_dump()
        )
        db.add(log_entry)
        await db.commit()

        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Gap Analysis failed: {str(e)}"
        )

# --- 3. AI Personalized Recommendations for Students & Faculty ---

@ai_skill_router.post("/recommendations", response_model=AIRecommendationResponse)
async def get_personalized_recommendations(
    payload: AIRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    AI Endpoint: Recommends certifications, hands-on projects, and internships/grants
    tailored to a Student or Faculty persona based on their interests and career goals.
    """
    try:
        recommendations = await ai_generate_recommendations(payload)

        log_entry = AIAnalysisLog(
            user_id=current_user.id,
            analysis_type="RECOMMENDATIONS",
            input_payload=payload.model_dump(),
            ai_response=recommendations.model_dump()
        )
        db.add(log_entry)
        await db.commit()

        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Recommendation generation failed: {str(e)}"
        )