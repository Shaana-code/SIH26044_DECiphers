import uuid
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from modules.module1_iam.models import User, UserRole
from modules.module1_iam.dependencies import get_current_user, RequireRoles
from modules.module6_applications.models import (
    Application, ApplicationStatus, InterviewSlot, AssessmentRecord, JobOffer
)
from modules.module6_applications.schemas import (
    ApplicationSubmitRequest, ApplicationStatusUpdateRequest, ApplicationResponse,
    ScheduleInterviewRequest, InterviewResponse,
    RecordAssessmentRequest, AssessmentResponse,
    ExtendOfferRequest, RespondOfferRequest, JobOfferResponse
)
from modules.module6_applications.ats_ai_engine import (
    ai_screen_resume_against_job,
    ai_generate_interview_questions_for_candidate,
    AIInterviewQuestionsResponse
)

application_router = APIRouter(prefix="/api/v1/applications", tags=["Module 6: AI-Powered ATS & Applications"])

# --- 1. STUDENT: Apply to Job (Real-Time AI Screening + TPO One-Offer Policy) ---

@application_router.post("/apply", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_to_opportunity(
    payload: ApplicationSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can apply.")

    # TPO Policy Check: If student already accepted an offer, block new applications
    accepted_offer_stmt = select(JobOffer).where(
        JobOffer.student_id == current_user.id,
        JobOffer.status == "ACCEPTED"
    )
    if (await db.execute(accepted_offer_stmt)).scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="TPO Policy: You have already accepted an offer and cannot submit new applications."
        )

    # Check for duplicate submission
    dup_stmt = select(Application).where(
        Application.opportunity_id == payload.opportunity_id,
        Application.student_id == current_user.id
    )
    if (await db.execute(dup_stmt)).scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already applied for this opening.")

    # 🤖 RUN REAL-TIME AI RESUME SCREENING
    try:
        ai_eval = await ai_screen_resume_against_job(
            resume_text=payload.resume_text,
            job_title=payload.target_job_title or "Target Role",
            job_requirements=payload.target_job_requirements or "Standard Requirements"
        )
        match_score = ai_eval.match_score
        ai_verdict = ai_eval.screening_verdict
        ai_summary = ai_eval.recruiter_summary
        ai_strengths = ai_eval.key_strengths
        ai_flags = ai_eval.flags_or_missing
    except Exception:
        # Fallback if AI service is temporarily unavailable
        match_score = 70.0
        ai_verdict = "POTENTIAL_MATCH"
        ai_summary = "Application submitted (Screening queued)."
        ai_strengths = []
        ai_flags = []

    new_app = Application(
        opportunity_id=payload.opportunity_id,
        student_id=current_user.id,
        resume_text=payload.resume_text,
        match_score=match_score,
        ai_verdict=ai_verdict,
        ai_screening_summary=ai_summary,
        ai_strengths=ai_strengths,
        ai_flags=ai_flags,
        status=ApplicationStatus.APPLIED
    )
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return new_app


# --- 2. STUDENT: View My Applications ---

@application_router.get("/my-applications", response_model=List[ApplicationResponse])
async def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application).where(Application.student_id == current_user.id).order_by(Application.applied_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()


# --- 3. RECRUITER / TPO: View Applicants (Ranked by AI Match Score) ---

@application_router.get("/opportunity/{opportunity_id}/applicants", response_model=List[ApplicationResponse], dependencies=[Depends(RequireRoles([UserRole.RECRUITER, UserRole.FACULTY_TPO, UserRole.COLLEGE_ADMIN]))])
async def get_applicants_for_opportunity(
    opportunity_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    stmt = (
        select(Application)
        .where(Application.opportunity_id == opportunity_id)
        .order_by(Application.match_score.desc()) # Ranked by AI Score
    )
    res = await db.execute(stmt)
    return res.scalars().all()


# --- 4. RECRUITER: Generate Custom AI Interview Questions ---

@application_router.get("/{application_id}/ai-interview-questions", response_model=AIInterviewQuestionsResponse, dependencies=[Depends(RequireRoles([UserRole.RECRUITER, UserRole.FACULTY_TPO]))])
async def get_ai_interview_questions(
    application_id: uuid.UUID,
    round_name: str = "Technical Round 1",
    db: AsyncSession = Depends(get_db)
):
    app_obj = await db.get(Application, application_id)
    if not app_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    return await ai_generate_interview_questions_for_candidate(
        resume_text=app_obj.resume_text,
        job_title="Target Opening",
        round_name=round_name
    )


# --- 5. RECRUITER / TPO: Update Application Status ---

@application_router.patch("/{application_id}/status", response_model=ApplicationResponse, dependencies=[Depends(RequireRoles([UserRole.RECRUITER, UserRole.FACULTY_TPO]))])
async def update_application_status(
    application_id: uuid.UUID,
    payload: ApplicationStatusUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    app_obj = await db.get(Application, application_id)
    if not app_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    app_obj.status = payload.status
    if payload.notes:
        app_obj.notes = payload.notes

    await db.commit()
    await db.refresh(app_obj)
    return app_obj


# --- 6. RECRUITER: Schedule Interview Round ---

@application_router.post("/{application_id}/interviews", response_model=InterviewResponse, dependencies=[Depends(RequireRoles([UserRole.RECRUITER]))])
async def schedule_interview(
    application_id: uuid.UUID,
    payload: ScheduleInterviewRequest,
    db: AsyncSession = Depends(get_db)
):
    app_obj = await db.get(Application, application_id)
    if not app_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    interview = InterviewSlot(
        application_id=application_id,
        round_name=payload.round_name,
        scheduled_time=payload.scheduled_time,
        interviewer_name=payload.interviewer_name,
        meeting_link=payload.meeting_link,
        status="SCHEDULED"
    )
    app_obj.status = ApplicationStatus.INTERVIEW_SCHEDULED
    db.add(interview)
    await db.commit()
    await db.refresh(interview)
    return interview


# --- 7. RECRUITER / TPO: Record Online Assessment Score ---

@application_router.post("/{application_id}/assessments", response_model=AssessmentResponse, dependencies=[Depends(RequireRoles([UserRole.RECRUITER, UserRole.FACULTY_TPO]))])
async def record_assessment(
    application_id: uuid.UUID,
    payload: RecordAssessmentRequest,
    db: AsyncSession = Depends(get_db)
):
    app_obj = await db.get(Application, application_id)
    if not app_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    record = AssessmentRecord(
        application_id=application_id,
        assessment_name=payload.assessment_name,
        score=payload.score,
        max_score=payload.max_score,
        passed=payload.passed
    )
    app_obj.status = ApplicationStatus.ASSESSMENT_COMPLETED
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


# --- 8. RECRUITER: Extend Offer ---

@application_router.post("/{application_id}/offer", response_model=JobOfferResponse, dependencies=[Depends(RequireRoles([UserRole.RECRUITER]))])
async def extend_offer(
    application_id: uuid.UUID,
    payload: ExtendOfferRequest,
    db: AsyncSession = Depends(get_db)
):
    app_obj = await db.get(Application, application_id)
    if not app_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    existing = (await db.execute(select(JobOffer).where(JobOffer.application_id == application_id))).scalars().first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Offer already extended for this application.")

    offer = JobOffer(
        application_id=application_id,
        student_id=app_obj.student_id,
        offered_salary_or_stipend=payload.offered_salary_or_stipend,
        joining_date=payload.joining_date,
        offer_letter_text=payload.offer_letter_text,
        status="EXTENDED"
    )
    app_obj.status = ApplicationStatus.OFFER_EXTENDED
    db.add(offer)
    await db.commit()
    await db.refresh(offer)
    return offer


# --- 9. STUDENT: Accept or Reject Offer (With Auto-Withdrawal of Other Applications) ---

@application_router.post("/offers/{offer_id}/respond", response_model=JobOfferResponse)
async def respond_to_offer(
    offer_id: uuid.UUID,
    payload: RespondOfferRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    offer = await db.get(JobOffer, offer_id)
    if not offer or offer.student_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found or unauthorized.")

    if offer.status != "EXTENDED":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Offer is already {offer.status.lower()}.")

    offer.responded_at = datetime.utcnow()
    app_obj = await db.get(Application, offer.application_id)

    if payload.accept:
        offer.status = "ACCEPTED"
        if app_obj:
            app_obj.status = ApplicationStatus.OFFER_ACCEPTED

        # TPO Policy: Auto-withdraw all other pending applications for this student
        other_apps_stmt = select(Application).where(
            Application.student_id == current_user.id,
            Application.id != offer.application_id,
            Application.status.notin_([ApplicationStatus.OFFER_ACCEPTED, ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN])
        )
        other_apps = (await db.execute(other_apps_stmt)).scalars().all()
        for other_app in other_apps:
            other_app.status = ApplicationStatus.WITHDRAWN

    else:
        offer.status = "REJECTED"
        if app_obj:
            app_obj.status = ApplicationStatus.OFFER_REJECTED

    await db.commit()
    await db.refresh(offer)
    return offer