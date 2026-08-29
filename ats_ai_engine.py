import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from typing import List
from core.config import settings

# Connect Instructor to Groq's High-Speed Free Endpoint
client = instructor.from_openai(
    AsyncOpenAI(
        base_url=settings.GROQ_BASE_URL,
        api_key=settings.GROQ_API_KEY
    ),
    mode=instructor.Mode.JSON
)

AI_MODEL = settings.GROQ_MODEL

# --- Schemas for AI ATS Outputs ---

class AIScreeningResult(BaseModel):
    match_score: float = Field(..., ge=0.0, le=100.0, description="Readiness score (0-100%)")
    screening_verdict: str = Field(description="STRONG_MATCH, POTENTIAL_MATCH, or LOW_FIT")
    key_strengths: List[str] = Field(description="Top matched skills and background strengths")
    flags_or_missing: List[str] = Field(description="Missing requirements or technical skill gaps")
    recruiter_summary: str = Field(description="2-sentence executive summary for the recruiter")

class InterviewQuestion(BaseModel):
    question: str
    target_skill: str
    why_ask: str
    expected_answer_guide: str

class AIInterviewQuestionsResponse(BaseModel):
    round_name: str
    suggested_questions: List[InterviewQuestion]


# --- AI ATS Functions ---

async def ai_screen_resume_against_job(
    resume_text: str,
    job_title: str,
    job_requirements: str
) -> AIScreeningResult:
    """
    Groq AI evaluates student resume against job description and assigns
    match score, strengths, and missing flags.
    """
    system_prompt = (
        "You are an expert Technical Recruiter and ATS Evaluator. "
        "Evaluate the candidate resume against the job requirements. "
        "Calculate a fair readiness score between 0 and 100% and identify critical missing skills."
    )
    user_prompt = f"""
    Target Job Title: {job_title}
    
    Job Requirements:
    {job_requirements}

    Candidate Resume / Profile:
    {resume_text}
    """

    return await client.chat.completions.create(
        model=AI_MODEL,
        response_model=AIScreeningResult,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )


async def ai_generate_interview_questions_for_candidate(
    resume_text: str,
    job_title: str,
    round_name: str
) -> AIInterviewQuestionsResponse:
    """
    Groq AI generates custom interview questions specifically targeting candidate resume gaps.
    """
    system_prompt = (
        "You are a Senior Technical Interviewer. "
        "Generate 3-5 probing interview questions specifically targeting the candidate's declared projects and potential skill gaps."
    )
    user_prompt = f"""
    Target Job: {job_title}
    Interview Round: {round_name}
    Candidate Resume:
    {resume_text}
    """

    return await client.chat.completions.create(
        model=AI_MODEL,
        response_model=AIInterviewQuestionsResponse,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )