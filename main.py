from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="Industry & Corporate Profile Service")

# --- DATA MODELS (The Schemas) ---

class Company(BaseModel):
    id: int
    name: str
    website: str
    industry: str
    tier: str  # Tier 1, Tier 2, etc.
    is_verified: bool = False

class Recruiter(BaseModel):
    id: int
    company_id: int
    user_id: int  # Linked to Module 1
    name: str
    role: str  # Lead Recruiter, Hiring Manager, Interviewer

class MoU(BaseModel):
    id: int
    company_id: int
    start_date: date
    expiry_date: date
    document_url: str  # Linked to Module 9
    status: str # Active, Expired, Pending

class Engagement(BaseModel):
    id: int
    company_id: int
    college_id: int
    event_type: str  # Workshop, Guest Lecture, Seminar
    proposed_date: date
    status: str  # Proposed, Approved, Completed

# --- MOCK DATABASES (Lists) ---

db_companies = []
db_recruiters = []
db_mous = []
db_engagements = []

# --- ROUTES ---

# 1. COMPANY MANAGEMENT
@app.post("/api/v1/industry/companies", tags=["Companies"])
def register_company(company: Company):
    db_companies.append(company.dict())
    return {"message": "Company registered", "data": company}

@app.get("/api/v1/industry/companies", tags=["Companies"])
def list_companies():
    return db_companies

@app.put("/api/v1/industry/companies/{company_id}/verify", tags=["Companies"])
def verify_company(company_id: int):
    for co in db_companies:
        if co["id"] == company_id:
            co["is_verified"] = True
            return {"message": "Company KYC Verified"}
    raise HTTPException(status_code=404, detail="Company not found")

# 2. RECRUITER TEAM HIERARCHY
@app.post("/api/v1/industry/recruiters", tags=["Recruiters"])
def add_recruiter(recruiter: Recruiter):
    # Check if company exists first
    company_exists = any(c["id"] == recruiter.company_id for c in db_companies)
    if not company_exists:
        raise HTTPException(status_code=400, detail="Company does not exist")
    
    db_recruiters.append(recruiter.dict())
    return {"message": "Recruiter added to team", "data": recruiter}

@app.get("/api/v1/industry/companies/{company_id}/team", tags=["Recruiters"])
def get_company_team(company_id: int):
    team = [r for r in db_recruiters if r["company_id"] == company_id]
    return team

# 3. MoU AGREEMENTS
@app.post("/api/v1/industry/mou", tags=["MoU"])
def create_mou(mou: MoU):
    db_mous.append(mou.dict())
    return {"message": "MoU Agreement recorded", "data": mou}

@app.get("/api/v1/industry/mou/check/{company_id}", tags=["MoU"])
def check_mou_status(company_id: int):
    for m in db_mous:
        if m["company_id"] == company_id:
            return m
    return {"status": "No MoU found"}

# 4. CAMPUS ENGAGEMENTS (Workshops/Lectures)
@app.post("/api/v1/industry/engagements/propose", tags=["Engagements"])
def propose_engagement(eng: Engagement):
    db_engagements.append(eng.dict())
    return {"message": "Engagement proposal sent to college", "data": eng}

@app.get("/api/v1/industry/engagements/college/{college_id}", tags=["Engagements"])
def get_college_engagements(college_id: int):
    events = [e for e in db_engagements if e["college_id"] == college_id]
    return events