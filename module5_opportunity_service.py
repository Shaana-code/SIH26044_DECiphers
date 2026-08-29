from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Module 5 - Opportunity Management Service")


# ============================================================
# DATA MODELS
# ============================================================

class EligibilityRule(BaseModel):
    min_cgpa: Optional[float] = None
    max_cgpa: Optional[float] = None
    no_active_backlogs: Optional[bool] = None
    graduation_year: Optional[int] = None
    required_skills: List[str] = []


class CompensationDetail(BaseModel):
    stipend: Optional[float] = None
    ctc: Optional[float] = None
    currency: str = "INR"
    ppo_eligible: bool = False
    bond_required: bool = False


class OpportunityPosting(BaseModel):
    title: str
    description: str

    # Job / Internship / Apprenticeship / Project
    opportunity_type: str

    company_name: str
    location: str

    # Open to all / Partner colleges / Department specific
    audience_type: str = "Open to all"

    eligible_departments: List[str] = []

    eligibility: EligibilityRule

    compensation: CompensationDetail

    deadline: datetime


class StudentProfile(BaseModel):
    name: str
    cgpa: float
    active_backlogs: int
    graduation_year: int
    department: str
    skills: List[str]


# ============================================================
# TEMPORARY DATABASE
# ============================================================

opportunities = []
opportunity_id_counter = 1


# ============================================================
# CREATE OPPORTUNITY
# ============================================================

@app.post("/api/v1/opportunities")
def create_opportunity(opportunity: OpportunityPosting):

    global opportunity_id_counter

    if opportunity.deadline < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Deadline must be in the future"
        )

    new_opportunity = {
        "id": opportunity_id_counter,
        **opportunity.dict(),
        "created_at": datetime.now()
    }

    opportunities.append(new_opportunity)

    opportunity_id_counter += 1

    return {
        "message": "Opportunity created successfully",
        "opportunity": new_opportunity
    }


# ============================================================
# GET ALL OPPORTUNITIES
# ============================================================

@app.get("/api/v1/opportunities")
def get_opportunities():

    return {
        "count": len(opportunities),
        "opportunities": opportunities
    }


# ============================================================
# GET OPPORTUNITY BY ID
# ============================================================

@app.get("/api/v1/opportunities/{opportunity_id}")
def get_opportunity(opportunity_id: int):

    for opportunity in opportunities:

        if opportunity["id"] == opportunity_id:
            return opportunity

    raise HTTPException(
        status_code=404,
        detail="Opportunity not found"
    )


# ============================================================
# DELETE OPPORTUNITY
# ============================================================

@app.delete("/api/v1/opportunities/{opportunity_id}")
def delete_opportunity(opportunity_id: int):

    for opportunity in opportunities:

        if opportunity["id"] == opportunity_id:

            opportunities.remove(opportunity)

            return {
                "message": "Opportunity deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Opportunity not found"
    )


# ============================================================
# ELIGIBILITY CHECK
# ============================================================

def check_eligibility(
    student: StudentProfile,
    opportunity: dict
):

    rule = opportunity["eligibility"]

    # ----------------------------
    # CGPA CHECK
    # ----------------------------

    if rule.get("min_cgpa") is not None:

        if student.cgpa < rule["min_cgpa"]:

            return False, (
                f"Minimum CGPA required is "
                f"{rule['min_cgpa']}"
            )

    if rule.get("max_cgpa") is not None:

        if student.cgpa > rule["max_cgpa"]:

            return False, (
                f"Maximum CGPA allowed is "
                f"{rule['max_cgpa']}"
            )

    # ----------------------------
    # BACKLOG CHECK
    # ----------------------------

    if rule.get("no_active_backlogs") is True:

        if student.active_backlogs > 0:

            return False, "Active backlogs are not allowed"

    # ----------------------------
    # GRADUATION YEAR
    # ----------------------------

    if rule.get("graduation_year") is not None:

        if student.graduation_year != rule["graduation_year"]:

            return False, (
                f"Graduation year must be "
                f"{rule['graduation_year']}"
            )

    # ----------------------------
    # DEPARTMENT CHECK
    # ----------------------------

    if opportunity["audience_type"] == "Department specific":

        allowed_departments = opportunity[
            "eligible_departments"
        ]

        if student.department not in allowed_departments:

            return False, "Department is not eligible"

    # ----------------------------
    # SKILL CHECK
    # ----------------------------

    required_skills = [
        skill.lower()
        for skill in rule.get("required_skills", [])
    ]

    student_skills = [
        skill.lower()
        for skill in student.skills
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in student_skills
    ]

    if missing_skills:

        return False, (
            "Missing required skills: "
            + ", ".join(missing_skills)
        )

    return True, "Student is eligible"


# ============================================================
# CHECK STUDENT ELIGIBILITY FOR AN OPPORTUNITY
# ============================================================

@app.post(
    "/api/v1/opportunities/{opportunity_id}/check-eligibility"
)
def check_student_eligibility(
    opportunity_id: int,
    student: StudentProfile
):

    opportunity = None

    for item in opportunities:

        if item["id"] == opportunity_id:

            opportunity = item
            break

    if opportunity is None:

        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    # Check deadline

    if datetime.now() > opportunity["deadline"]:

        return {
            "eligible": False,
            "reason": "Application deadline has passed"
        }

    eligible, reason = check_eligibility(
        student,
        opportunity
    )

    return {
        "student": student.name,
        "opportunity": opportunity["title"],
        "eligible": eligible,
        "reason": reason
    }


# ============================================================
# SEARCH OPPORTUNITIES
# ============================================================

@app.get("/api/v1/opportunities/search/{keyword}")
def search_opportunities(keyword: str):

    keyword = keyword.lower()

    results = []

    for opportunity in opportunities:

        if (
            keyword in opportunity["title"].lower()
            or keyword in opportunity["company_name"].lower()
            or keyword in opportunity["description"].lower()
        ):

            results.append(opportunity)

    return {
        "keyword": keyword,
        "count": len(results),
        "results": results
    }