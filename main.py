from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base

# 1. Import models from Module 1 and Module 4 so SQLAlchemy discovers all tables
import modules.module1_iam.models
import modules.module4_ai_skills.models_skill_ai

# 2. Import routers for Module 1 (IAM) and Module 4 (AI Skill Engine)
from modules.module1_iam.routes import auth_router
from modules.module4_ai_skills.routes_skill_ai import ai_skill_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager that initializes database tables on server startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(" Database tables for Module 1 (IAM) & Module 4 (AI Skills) initialized.")
    yield


# Initialize FastAPI Application
app = FastAPI(
    title="Academia–Industry AI Collaboration Portal",
    description="Backend API for IAM (Module 1) and AI-Driven Skill Mapping & Recommendations (Module 4)",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for Streamlit / Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Module Routers
app.include_router(auth_router)
app.include_router(ai_skill_router)


# Root Health-Check Endpoint
@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "online",
        "service": "Academia-Industry AI Platform API",
        "active_modules": [
            "modules.module1_iam (Identity & Access Management)",
            "modules.module4_ai_skills (AI Skill Mapping & Recommendations)"
        ],
        "docs_url": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)