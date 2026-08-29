import instructor
from openai import AsyncOpenAI
from core.config import settings
from schemas_skill_ai import (
    SkillExtractionResponse,
    AIGapAnalysisRequest,
    AIGapAnalysisResponse,
    AIRecommendationRequest,
    AIRecommendationResponse,
    TargetPersona
)

# Connect Instructor to Groq's High-Speed Free Endpoint
client = instructor.from_openai(
    AsyncOpenAI(
        base_url=settings.GROQ_BASE_URL,
        api_key=settings.GROQ_API_KEY
    ),
    mode=instructor.Mode.JSON
)

AI_MODEL = settings.GROQ_MODEL


async def ai_extract_skills(text: str) -> SkillExtractionResponse:
    """
    Groq AI parses unstructured text (syllabi, resumes) and extracts
    standardized skills and proficiencies.
    """
    system_prompt = (
        "You are an expert Talent Acquisition Architect and Academic Curriculum Specialist. "
        "Analyze the provided text and extract concrete technical, domain, and analytical skills. "
        "Deduplicate skills and estimate proficiency level (Beginner, Intermediate, or Advanced)."
    )

    return await client.chat.completions.create(
        model=AI_MODEL,
        response_model=SkillExtractionResponse,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Text to analyze:\n\n{text}"}
        ],
        temperature=0.1
    )


async def ai_compute_gap_analysis(payload: AIGapAnalysisRequest) -> AIGapAnalysisResponse:
    """
    Groq AI performs semantic gap analysis between a candidate profile and a target job.
    """
    system_prompt = (
        "You are an elite Technical Hiring Director and Skill Evaluator. "
        "Perform a comprehensive semantic gap analysis between the candidate profile and target job description. "
        "Calculate a fair readiness score between 0 and 100% and identify critical missing skills."
    )

    user_prompt = f"""
    Target Role: {payload.target_role}
    
    Target Job Description:
    {payload.target_job_description}
    
    Candidate Background / Resume:
    {payload.user_bio_or_resume}
    """

    return await client.chat.completions.create(
        model=AI_MODEL,
        response_model=AIGapAnalysisResponse,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )


async def ai_generate_recommendations(payload: AIRecommendationRequest) -> AIRecommendationResponse:
    """
    Groq AI generates personalized certifications, projects, and opportunities for Students/Faculty.
    """
    if payload.persona == TargetPersona.STUDENT:
        system_prompt = (
            "You are an Academia-Industry Placement Director. "
            "Recommend industry-standard certifications, hands-on capstone projects, "
            "and internship avenues tailored to the student's career aspirations and stated interests."
        )
    else:
        system_prompt = (
            "You are a Senior Academic R&D and Industry Partnership Consultant. "
            "Recommend Faculty Development certifications, joint industry-academia "
            "research projects, patent opportunities, and corporate consultancy grants."
        )

    user_prompt = f"""
    Persona: {payload.persona.value}
    Academic Department: {payload.academic_department}
    Career Goals / Aspirations: {payload.career_goals}
    Specific Interests: {', '.join(payload.interests)}
    Current Verified Skills: {', '.join(payload.current_skills)}
    """

    return await client.chat.completions.create(
        model=AI_MODEL,
        response_model=AIRecommendationResponse,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
