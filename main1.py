"""
SIH Problem Statement 26044 | Team DECiphers
Portal for Academia-Industry Collaboration for Skill Mapping, Internships & Placement
-------------------------------------------------------------------------------------
Master FastAPI Application Entrypoint (Aggregating Modules 1 to 7)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from core.config import settings

# =============================================================================
# 1. IMPORT ALL DATABASE MODELS (Registers tables with SQLAlchemy Base metadata)
# =============================================================================
try:
    import modules.module1_iam.models
    import modules.module2_academia.models
    import modules.module3_corporate.models
    import modules.module4_ai_skills.models_skill_ai
    import modules.module5_opportunities.models
    import modules.module6_applications.models
    import modules.module7_evaluations.models
except ImportError as e:
    print(f"[Warning] Some module models could not be imported: {e}")

# =============================================================================
# 2. IMPORT ROUTERS FOR MODULES 1 THROUGH 7
# =============================================================================
from modules.module1_iam.routes import auth_router
from modules.module2_academia.routes import academia_router
from modules.module3_corporate.routes import corporate_router
from modules.module4_ai_skills.routes_skill_ai import ai_skill_router
from modules.module5_opportunities.routes import opportunity_router
from modules.module6_applications.routes import application_router
from modules.module7_evaluations.routes import evaluation_router


# =============================================================================
# 3. APPLICATION LIFECYCLE MANAGEMENT (STARTUP / SHUTDOWN)
# =============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager: Automatically verifies database connectivity and
    creates all database tables across Modules 1 to 7 on application startup.
    """
    print("=" * 70)
    print(f"🚀 Starting {settings.PROJECT_NAME}...")
    print(f"📦 Database Target: {settings.DATABASE_URL}")
    print(f"🧠 AI Engine Target: Groq LLM ({settings.GROQ_MODEL})")
    
    # Initialize all database tables asynchronously
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All database tables for Modules 1–7 initialized successfully.")
    print("=" * 70)
    
    yield
    
    # Clean shutdown
    await engine.dispose()
    print("🛑 Database connections closed. Application shut down.")


# =============================================================================
# 4. INITIALIZE FASTAPI APPLICATION WITH OPENAPI TAGS
# =============================================================================
tags_metadata = [
    {"name": "Module 1: IAM & Auth", "description": "Multi-role RBAC, JWT tokens, user verification, and tenant profiles."},
    {"name": "Module 2: Academia Management", "description": "Institutional hierarchy, course prerequisite graphs, and student eligibility verifier."},
    {"name": "Module 3: Corporate Profiles", "description": "Company registration, recruiter team management, and MoU agreements."},
    {"name": "Module 4: AI Skill Mapping Engine", "description": "LLM-driven syllabus extraction, semantic gap scoring, and personalized career roadmaps."},
    {"name": "Module 5: Opportunity Management", "description": "Campus recruitment drives, internships, and dynamic eligibility rules."},
    {"name": "Module 6: AI-ATS & Applications", "description": "Real-time AI resume screening, stage pipelines, interview scheduling, and TPO 1-offer policy."},
    {"name": "Module 7: Internship & Credits", "description": "Milestone logbooks, 60/40 dual-mentor evaluation, and academic credit transfer sync."},
    {"name": "System & Health", "description": "Platform status and diagnostic endpoints."}
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Unified Backend API for Academia-Industry Skill Mapping, Internships & Placement Engine (SIH 26044 - DECiphers)",
    version="3.0.0",
    lifespan=lifespan,
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)


# =============================================================================
# 5. CONFIGURE CORS (Cross-Origin Resource Sharing)
# =============================================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Streamlit, React, or mobile clients
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# 6. MOUNT ROUTERS FOR ALL 7 MODULES
# =============================================================================
app.include_router(auth_router)
app.include_router(academia_router)
app.include_router(corporate_router)
app.include_router(ai_skill_router)
app.include_router(opportunity_router)
app.include_router(application_router)
app.include_router(evaluation_router)


# =============================================================================
# 7. ROOT HEALTH-CHECK & SYSTEM DIAGNOSTIC ENDPOINTS
# =============================================================================
@app.get("/", tags=["System & Health"], status_code=status.HTTP_200_OK)
async def root_health_check():
    """
    Root status endpoint returning active services, modules, and documentation paths.
    """
    return {
        "status": "online",
        "platform": settings.PROJECT_NAME,
        "team": "DECiphers (SIH 26044)",
        "version": "3.0.0",
        "active_modules": [
            "Module 1: Identity & Access Management (IAM & RBAC)",
            "Module 2: Academia Management & Course Prerequisite Graphs",
            "Module 3: Industry & Corporate Profile Management (MoUs)",
            "Module 4: AI Skill Taxonomy, Extraction & Gap Engine (Groq)",
            "Module 5: Opportunity Management (Internships & Jobs)",
            "Module 6: AI-Powered Applicant Tracking System (ATS)",
            "Module 7: Internship Evaluation & Academic Credit Transfer"
        ],
        "api_documentation": "/docs",
        "redoc_documentation": "/redoc"
    }


@app.get("/health", tags=["System & Health"])
async def ping():
    return {"ping": "pong", "service": "DECiphers Core Backend", "ai_provider": "Groq Cloud"}


# =============================================================================
# 8. DIRECT SCRIPT EXECUTION
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
