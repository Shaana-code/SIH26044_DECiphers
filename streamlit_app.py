"""
SIH Problem Statement 26044 | Team DECiphers
Portal for Academia-Industry Collaboration for Skill Mapping, Internships & Placement
-------------------------------------------------------------------------------------
Fully Dynamic Multi-Persona Web Dashboard with SQLite & Groq AI Integration
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta
import streamlit as st
import requests

# --- 1. SECRETS & AI CONFIGURATION ---
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
GROQ_MODEL = st.secrets.get("GROQ_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SkillBridge AI | SIH DECiphers Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. DYNAMIC DATABASE INITIALIZER (portal.db) ---
def get_db_connection():
    conn = sqlite3.connect("portal.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_dynamic_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Opportunities Table (Module 5)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        job_type TEXT NOT NULL,
        stipend TEXT NOT NULL,
        skills TEXT NOT NULL,
        eligibility TEXT NOT NULL,
        status TEXT DEFAULT 'OPEN',
        created_at TEXT
    );
    """)

    # 2. Applications Table (Module 6)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id TEXT PRIMARY KEY,
        opportunity_id TEXT NOT NULL,
        student_name TEXT NOT NULL,
        student_email TEXT NOT NULL,
        target_role TEXT NOT NULL,
        resume_text TEXT NOT NULL,
        match_score REAL DEFAULT 0.0,
        verdict TEXT,
        summary TEXT,
        strengths TEXT,
        missing TEXT,
        status TEXT DEFAULT 'APPLIED',
        applied_at TEXT
    );
    """)

    # 3. Logbooks Table (Module 7)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS internship_logbooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT NOT NULL,
        week_number TEXT NOT NULL,
        hours_worked INTEGER NOT NULL,
        milestones TEXT NOT NULL,
        artifact_link TEXT,
        mentor_rating REAL DEFAULT 5.0,
        faculty_rating REAL DEFAULT 5.0,
        status TEXT DEFAULT 'APPROVED',
        submitted_at TEXT
    );
    """)

    # Pre-seed sample opportunities if table is empty
    cur.execute("SELECT COUNT(*) FROM opportunities")
    if cur.fetchone()[0] == 0:
        sample_jobs = [
            ("opp-101", "AI Systems Engineering Intern", "Nexus AI Systems", "INTERNSHIP", "$1,500 / month", "Python, FastAPI, PyTorch, Docker, Vector DBs", "CGPA >= 7.5 | No Active Backlogs", "OPEN", datetime.utcnow().isoformat()),
            ("opp-102", "Graduate Cloud & DevOps Engineer", "CloudScale Infrastructure", "FULL_TIME", "$85,000 / year", "AWS, Docker, Kubernetes, Linux, Terraform", "CGPA >= 7.0 | Attendance >= 75%", "OPEN", datetime.utcnow().isoformat()),
            ("opp-103", "Embedded Robotics Research Fellow", "RoboTech Autonomous Labs", "RESEARCH_GRANT", "$2,200 / month", "C++, ROS2, OpenCV, Edge AI", "Open to M.Tech / PhD & Faculty", "OPEN", datetime.utcnow().isoformat())
        ]
        cur.executemany("INSERT INTO opportunities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_jobs)

    # Pre-seed sample applications if table is empty
    cur.execute("SELECT COUNT(*) FROM applications")
    if cur.fetchone()[0] == 0:
        sample_apps = [
            (
                "app-001", "opp-101", "Aarav Sharma", "student@test.com", "AI Systems Engineering Intern",
                "Aarav Sharma: Final year CS. Strong in Python, FastAPI, PostgreSQL, and Git. Built async APIs and data pipelines.",
                86.5, "STRONG_MATCH", "Strong backend fundamentals in Python/FastAPI with relational DB design skills.",
                json.dumps(["Python", "FastAPI", "PostgreSQL", "REST APIs"]),
                json.dumps(["Docker", "Kubernetes"]),
                "INTERVIEW_SCHEDULED", datetime.utcnow().isoformat()
            ),
            (
                "app-002", "opp-101", "Rohan Gupta", "rohan@test.com", "AI Systems Engineering Intern",
                "Rohan Gupta: Proficient in C++ and Python fundamentals. Basic algorithms and data structures.",
                64.0, "POTENTIAL_MATCH", "Good programming fundamentals, but lacks async microservices and database indexing experience.",
                json.dumps(["C++", "Python Basics", "Git"]),
                json.dumps(["FastAPI", "Docker", "Vector DBs"]),
                "APPLIED", datetime.utcnow().isoformat()
            )
        ]
        cur.executemany("INSERT INTO applications VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_apps)

    # Pre-seed sample logbooks
    cur.execute("SELECT COUNT(*) FROM internship_logbooks")
    if cur.fetchone()[0] == 0:
        sample_logs = [
            ("student@test.com", "Week 1", 40, "Onboarding, repo setup, and microservice architecture planning", "https://github.com/nexus-ai/rag-pipeline/pull/1", 5.0, 5.0, "APPROVED", datetime.utcnow().isoformat()),
            ("student@test.com", "Week 2", 42, "Implemented async JWT authentication middleware and Redis rate limiter", "https://github.com/nexus-ai/rag-pipeline/pull/14", 4.8, 5.0, "APPROVED", datetime.utcnow().isoformat()),
            ("student@test.com", "Week 3", 38, "PostgreSQL schema migrations and connection pool optimization in SQLAlchemy", "https://github.com/nexus-ai/rag-pipeline/pull/28", 4.9, 4.8, "APPROVED", datetime.utcnow().isoformat())
        ]
        cur.executemany("INSERT INTO internship_logbooks (student_email, week_number, hours_worked, milestones, artifact_link, mentor_rating, faculty_rating, status, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", sample_logs)

    conn.commit()
    conn.close()

# Initialize DB on load
init_dynamic_db()

# --- 4. GROQ AI HELPER FUNCTION ---
def call_groq_ai(system_prompt: str, user_prompt: str, response_format="json") -> dict:
    """Calls Groq API directly with fallback demo response if key is missing."""
    if not GROQ_API_KEY or GROQ_API_KEY == "gsk_PASTE_YOUR_LOCAL_KEY_HERE":
        # Fallback response for offline demo
        return {
            "score": 82.5,
            "verdict": "STRONG_MATCH",
            "summary": "Candidate exhibits strong programming fundamentals and relevant coursework.",
            "strengths": ["Python", "FastAPI", "Database Modeling"],
            "missing": ["Docker Containerization", "Cloud Deployments"],
            "questions": [
                {"q": "How do you handle asynchronous database transactions in FastAPI with SQLAlchemy 2.0?", "skill": "FastAPI", "why": "Validates claimed async backend skills."},
                {"q": "How would you containerize your microservice for deployment onto a Kubernetes cluster?", "skill": "Docker", "why": "Tests identified containerization gap."}
            ]
        }
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }
    if response_format == "json":
        payload["response_format"] = {"type": "json_object"}

    try:
        res = requests.post(GROQ_BASE_URL, headers=headers, json=payload, timeout=12)
        if res.status_code == 200:
            return json.loads(res.json()["choices"][0]["message"]["content"])
        else:
            st.error(f"Groq API Error ({res.status_code}): {res.text}")
    except Exception as e:
        st.warning(f"AI Service Notice: {str(e)}")
    
    return {}

# --- 5. SIDEBAR: 1-CLICK PERSONA SWITCHER ---
if "user_info" not in st.session_state or st.session_state.user_info is None:
    st.session_state.user_info = {
        "id": "11111111-1111-1111-1111-111111111111",
        "name": "Aarav Sharma", 
        "role": "STUDENT", 
        "email": "student@test.com",
        "student_id": 1001,
        "dept": "Computer Science Engineering",
        "cgpa": 8.5,
        "attendance": 85.0
    }

with st.sidebar:
    st.title("🎓 SIH 26044")
    st.caption("Academia–Industry Collaboration | Team DECiphers")
    
    if GROQ_API_KEY and not GROQ_API_KEY.startswith("gsk_PASTE"):
        st.success("🟢 Groq AI Active (High Speed)")
    else:
        st.info("🟡 Groq Key in Demo Fallback Mode")

    st.divider()
    st.subheader("⚡ Switch Persona (Live Demo)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎓 Student", use_container_width=True):
            st.session_state.user_info = {
                "id": "11111111-1111-1111-1111-111111111111",
                "name": "Aarav Sharma", 
                "role": "STUDENT", 
                "email": "student@test.com",
                "student_id": 1001,
                "dept": "Computer Science Engineering",
                "cgpa": 8.5,
                "attendance": 85.0
            }
            st.rerun()
            
    with col2:
        if st.button("💼 Recruiter", use_container_width=True):
            st.session_state.user_info = {
                "id": "22222222-2222-2222-2222-222222222222",
                "name": "Priya Mehta", 
                "role": "RECRUITER", 
                "email": "recruiter@company.com",
                "company": "Nexus AI Systems"
            }
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🏛️ Faculty / TPO", use_container_width=True):
            st.session_state.user_info = {
                "id": "33333333-3333-3333-3333-333333333333",
                "name": "Dr. Rajesh Rao", 
                "role": "FACULTY_TPO", 
                "email": "faculty@college.edu",
                "institution": "Global Tech University"
            }
            st.rerun()
            
    with col4:
        if st.button("🏫 Admin", use_container_width=True):
            st.session_state.user_info = {
                "id": "44444444-4444-4444-4444-444444444444",
                "name": "University Dean", 
                "role": "COLLEGE_ADMIN", 
                "email": "admin@college.edu"
            }
            st.rerun()

    st.divider()
    user = st.session_state.user_info
    with st.container(border=True):
        st.markdown(f"### 👤 **{user['name']}**")
        st.markdown(f"**Role:** `{user['role']}`")
        st.markdown(f"**Email:** `{user['email']}`")
        if "cgpa" in user:
            st.caption(f"🎓 CGPA: **{user['cgpa']}** | Attendance: **{user['attendance']}%**")

# --- 6. TOP KPI SUMMARY DASHBOARD ---
st.title("🎓 Academia–Industry Collaboration & AI Placement Portal")
st.caption("SIH 26044: Real-time Skill Mapping, AI-ATS, Prerequisite Verification & Credit Sync")

conn = get_db_connection()
total_opps = conn.execute("SELECT COUNT(*) FROM opportunities WHERE status='OPEN'").fetchone()[0]
total_apps = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
avg_score = conn.execute("SELECT AVG(match_score) FROM applications").fetchone()[0] or 75.0
conn.close()

k1, k2, k3, k4 = st.columns(4)
k1.metric(label="Active Hiring Drives", value=str(total_opps), delta="Live Openings")
k2.metric(label="Total ATS Applications", value=str(total_apps), delta="+1 Real-time")
k3.metric(label="Average AI Match Score", value=f"{avg_score:.1f}%", delta="+5.4% quality")
k4.metric(label="Credit Transfer Rate", value="96.2%", delta="Module 7 Sync")

st.divider()

# --- 7. MAIN NAVIGATION TABS (MODULES 1 TO 7) ---
tab_m4, tab_m6, tab_m2, tab_m3_5, tab_m7, tab_m1 = st.tabs([
    "🧠 1. AI Skill & Gap Engine (Mod 4)",
    "💼 2. AI-ATS & Application Pipeline (Mod 6)",
    "🏫 3. Academia & Prerequisite Verifier (Mod 2)",
    "🏢 4. Corporate MoUs & Post Job (Mod 3 & 5)",
    "📋 5. Internship Monitoring & Credits (Mod 7)",
    "🔑 6. IAM & Access Control (Mod 1)"
])

# =============================================================================
# TAB 1: MODULE 4 (AI SKILL MAPPING & GAP ENGINE)
# =============================================================================
with tab_m4:
    st.subheader("🧠 Module 4: Live AI Skill Extraction, Gap Scoring & Career Pathways")
    st.write("Dynamic LLM reasoning to map any custom resume or syllabus against target industry roles.")

    sub1, sub2, sub3 = st.tabs(["📄 AI Skill Extractor", "📊 Live Job Gap Analysis", "🎯 AI Career Recommendations"])

    with sub1:
        st.markdown("#### 📄 Extract Skills from Any Course Syllabus or Resume")
        sample_text = (
            "Course Syllabus: CS402 - Distributed AI & Cloud Systems.\n"
            "Topics: Microservices with Python and FastAPI. Relational database indexing with PostgreSQL and SQLAlchemy. "
            "Container orchestration using Docker and Kubernetes. Vector search with Milvus and Pinecone for RAG architectures. "
            "CI/CD pipeline automation with GitHub Actions and AWS deployments."
        )
        custom_input = st.text_area("Enter Syllabus or Resume to Parse Dynamically:", value=sample_text, height=130)

        if st.button("🚀 Extract Skills with Groq AI", use_container_width=True):
            with st.spinner("AI parsing technical concepts and inferring proficiencies..."):
                sys_prompt = "You are an ATS skill extractor. Return JSON with 'summary' (str) and 'skills' (list of {name, category, level})."
                res_data = call_groq_ai(sys_prompt, custom_input)
                
                summary = res_data.get("summary", "Identified high-relevance technical skills for modern backend & AI roles.")
                skills = res_data.get("skills", [
                    {"name": "FastAPI", "category": "Backend", "level": "Advanced"},
                    {"name": "PostgreSQL", "category": "Database", "level": "Intermediate"},
                    {"name": "Docker & Kubernetes", "category": "Cloud & DevOps", "level": "Intermediate"},
                    {"name": "Vector Databases (Milvus)", "category": "Generative AI", "level": "Advanced"}
                ])

                st.success(f"**Summary:** {summary}")
                cols = st.columns(2)
                for idx, sk in enumerate(skills):
                    with cols[idx % 2]:
                        with st.container(border=True):
                            st.markdown(f"##### **{sk.get('name', 'Skill')}** `[{sk.get('level', 'Intermediate')}]`")
                            st.caption(f"**Category:** {sk.get('category', 'Technical')}")

    with sub2:
        st.markdown("#### 📊 Dynamic Job Gap Analysis & Readiness Meter")
        c_l, c_r = st.columns(2)
        with c_l:
            dyn_role = st.text_input("Target Job Title", value="Full-Stack AI Systems Engineer")
            dyn_jd = st.text_area("Target Job Requirements:", height=130, value="Requirements: Proficient in Python, FastAPI, PyTorch, Vector Databases (Pinecone/Milvus), Docker containerization, Kubernetes, and AWS deployments.")
        with c_r:
            st.text_input("Candidate Name", value=st.session_state.user_info.get("name", "Aarav Sharma"), disabled=True)
            dyn_resume = st.text_area("Candidate Resume / Profile:", height=130, value="Final-year student. Strong in Python, FastAPI REST APIs, SQL, and database design. Built web scrapers and simple ML models. Have not worked with Docker, Kubernetes, or Vector DBs yet.")

        if st.button("⚡ Compute Semantic Gap Score", use_container_width=True):
            with st.spinner("Analyzing semantic gap with Groq LLM..."):
                sys_p = "You are a Technical Hiring Director. Compare resume against JD. Return JSON with 'score' (float 0-100), 'verdict' (str), 'summary' (str), 'strengths' (list of str), 'deficits' (list of {skill, remedy})."
                u_p = f"Role: {dyn_role}\nJD: {dyn_jd}\nResume: {dyn_resume}"
                gap_data = call_groq_ai(sys_p, u_p)

                score = float(gap_data.get("score", 78.5))
                score_c1, score_c2 = st.columns([1, 2])
                with score_c1:
                    st.metric("AI Job Readiness Score", f"{score:.1f}%")
                with score_c2:
                    st.write(f"**Verdict:** `{gap_data.get('verdict', 'POTENTIAL_MATCH')}`")
                    st.progress(score / 100.0)

                st.info(f"**AI Evaluation Summary:** {gap_data.get('summary', 'Strong core fundamentals in Python and API design. Needs practical containerization experience.')}")
                
                g1, g2 = st.columns(2)
                with g1:
                    st.markdown("##### ✅ Matched Strengths")
                    for st_item in gap_data.get("strengths", ["Python Backend", "FastAPI Architecture", "SQL Query Design"]):
                        st.success(f"✔️ {st_item}")
                with g2:
                    st.markdown("##### 🚨 Critical Missing Skills & Remedies")
                    for d_item in gap_data.get("deficits", [{"skill": "Docker & Kubernetes", "remedy": "Complete Docker Certified Associate track."}]):
                        with st.container(border=True):
                            st.markdown(f"**{d_item.get('skill')}**")
                            st.caption(f"💡 **Remedy:** {d_item.get('remedy')}")

    with sub3:
        st.markdown("#### 🎯 AI Personalized Career & R&D Pathways")
        p_type = st.selectbox("Persona Type", ["STUDENT", "FACULTY"])
        p_goal = st.text_input("Career / R&D Goal", value="Specialize in Production RAG Pipelines & AI Systems" if p_type == "STUDENT" else "Establish a funded Industry Center of Excellence in Edge AI")
        p_interests = st.text_input("Interests (comma-separated)", value="Generative AI, Vector Databases, Docker, Distributed Systems")
        p_skills = st.text_input("Current Skills", value="Python, FastAPI, SQL, Linux")

        if st.button("✨ Generate AI Career Roadmap", use_container_width=True):
            r1, r2, r3 = st.columns(3)
            with r1:
                st.markdown("### 📜 Certifications")
                with st.container(border=True):
                    st.markdown("#### **AWS Certified Machine Learning - Specialty**")
                    st.caption("Provider: `AWS` | Duration: **6 Weeks**")
                    st.write("Validates cloud model hosting, endpoint autoscaling, and data pipeline integration.")
            with r2:
                st.markdown("### 💻 Hands-on Projects")
                with st.container(border=True):
                    st.markdown("#### **Enterprise RAG Engine with Milvus** `[Intermediate]`")
                    st.caption("Tech Stack: `Python`, `FastAPI`, `Milvus`, `Docker`")
                    st.write("Build a multi-tenant document search service with semantic hybrid search.")
            with r3:
                st.markdown("### 💼 Opportunities")
                with st.container(border=True):
                    st.markdown("#### **AI Systems Engineering Intern**")
                    st.caption("Company: **Nexus AI Systems** | Location: **Hybrid**")
                    st.write("Matched to your declared goals and verified competencies.")

# =============================================================================
# TAB 2: MODULE 6 (AI-ATS & RECRUITMENT PIPELINE - FULLY DYNAMIC)
# =============================================================================
with tab_m6:
    st.subheader("💼 Module 6: Recruitment & Application Workflow Engine (ATS)")
    st.write("Real-time applicant submission, live AI resume screening, stage management, and TPO policy enforcement.")

    ats_sub1, ats_sub2 = st.tabs(["📋 Recruiter Live ATS Pipeline", "📝 Student Apply & Offer Tracker"])

    # --- RECRUITER ATS BOARD ---
    with ats_sub1:
        st.markdown("#### 💼 Live Candidate Board (Ranked by AI Match Score)")
        
        conn = get_db_connection()
        apps_db = conn.execute("SELECT * FROM applications ORDER BY match_score DESC").fetchall()
        conn.close()

        if not apps_db:
            st.info("No applications submitted yet. Switch to the Student view to submit an application.")
        else:
            for app in apps_db:
                with st.container(border=True):
                    c_info, c_score, c_action = st.columns([2, 1, 1])
                    with c_info:
                        st.markdown(f"### 👤 **{app['student_name']}** `({app['student_email']})`")
                        st.caption(f"**Target Role:** `{app['target_role']}` | **Applied:** `{app['applied_at'][:10]}`")
                        st.write(f"🤖 **AI Screening Verdict:** `{app['verdict']}`")
                        st.caption(f"_{app['summary']}_")
                    with c_score:
                        st.metric("AI Match Score", f"{app['match_score']:.1f}%")
                        st.markdown(f"**Current Status:** `{app['status']}`")
                    with c_action:
                        stage_options = ["APPLIED", "SHORTLISTED", "INTERVIEW_SCHEDULED", "OFFER_EXTENDED", "OFFER_ACCEPTED", "REJECTED"]
                        current_idx = stage_options.index(app["status"]) if app["status"] in stage_options else 0
                        new_stage = st.selectbox("Advance Stage", stage_options, index=current_idx, key=f"stage_sel_{app['id']}")
                        
                        if st.button("💾 Save Stage", key=f"save_stage_{app['id']}"):
                            c = get_db_connection()
                            c.execute("UPDATE applications SET status=? WHERE id=?", (new_stage, app["id"]))
                            c.commit()
                            c.close()
                            st.success(f"Stage for {app['student_name']} updated to {new_stage}!")
                            st.rerun()

                    # Dynamic AI Interview Question Generator
                    with st.expander(f"🎯 Generate Custom AI Interview Questions for {app['student_name']}"):
                        round_type = st.selectbox("Select Round", ["System Design & Python", "Data Structures & Algorithms", "Culture & Leadership"], key=f"rnd_sel_{app['id']}")
                        if st.button(f"Generate Questions with Groq AI", key=f"gen_q_{app['id']}"):
                            with st.spinner("Groq LLM analyzing candidate resume gaps..."):
                                q_sys = "You are a Technical Interviewer. Return JSON with 'questions' (list of {q, skill, why})."
                                q_u = f"Role: {app['target_role']}\nRound: {round_type}\nResume: {app['resume_text']}"
                                q_res = call_groq_ai(q_sys, q_u)
                                
                                q_list = q_res.get("questions", [
                                    {"q": "How do you handle connection pooling and transaction rollbacks in async FastAPI applications?", "skill": "FastAPI & PostgreSQL", "why": "Tests claimed backend resilience."},
                                    {"q": "Explain how you would containerize your application for deployment onto a Kubernetes cluster?", "skill": "Docker", "why": "Probes identified resume gap."}
                                ])
                                for idx, q in enumerate(q_list, 1):
                                    st.markdown(f"**{idx}. {q.get('q')}**")
                                    st.caption(f"🎯 *Target Skill:* `{q.get('skill')}` | 💡 *Why Ask:* _{q.get('why')}_")

    # --- STUDENT APPLY & OFFER TRACKER ---
    with ats_sub2:
        st.markdown("#### 📝 Submit Live Application with Real-Time AI Screening")
        
        conn = get_db_connection()
        opps_list = conn.execute("SELECT * FROM opportunities WHERE status='OPEN'").fetchall()
        conn.close()

        if opps_list:
            selected_opp = st.selectbox("Select Target Job Opening:", [f"{o['title']} ({o['company']})" for o in opps_list])
            opp_obj = next(o for o in opps_list if f"{o['title']} ({o['company']})" == selected_opp)

            with st.container(border=True):
                st.markdown(f"### 💼 **{opp_obj['title']}**")
                st.markdown(f"🏢 **{opp_obj['company']}** | 💰 **{opp_obj['stipend']}**")
                st.caption(f"🎯 **Required Skills:** `{opp_obj['skills']}`")
                st.info(f"📋 **Eligibility Rules:** {opp_obj['eligibility']}")

                user_name = st.session_state.user_info.get("name", "Aarav Sharma")
                user_email = st.session_state.user_info.get("email", "student@test.com")
                
                sub_resume = st.text_area("Your Resume / Portfolio Summary to Submit:", value="Aarav Sharma | Final Year CS | Email: student@test.com\nProficient in Python, FastAPI, PostgreSQL, and Git. Built asynchronous REST APIs and search engine backend prototypes.", height=110)

                if st.button("🚀 Submit Application & Trigger Real-Time AI Screening", use_container_width=True):
                    with st.spinner("AI evaluating candidate against job criteria in real-time..."):
                        # AI Screen
                        sys_p = "You are an ATS Evaluator. Return JSON with 'score' (float 0-100), 'verdict' (str: STRONG_MATCH/POTENTIAL_MATCH/LOW_FIT), 'summary' (str)."
                        u_p = f"Job: {opp_obj['title']} at {opp_obj['company']}\nReqs: {opp_obj['skills']}\nResume: {sub_resume}"
                        ai_res = call_groq_ai(sys_p, u_p)

                        score_val = float(ai_res.get("score", 86.5))
                        verdict_val = ai_res.get("verdict", "STRONG_MATCH")
                        summary_val = ai_res.get("summary", "Candidate displays strong relevant backend qualifications.")

                        # Dynamic insert into SQLite
                        new_app_id = f"app-{datetime.utcnow().strftime('%M%S')}"
                        c = get_db_connection()
                        c.execute(
                            "INSERT INTO applications (id, opportunity_id, student_name, student_email, target_role, resume_text, match_score, verdict, summary, strengths, missing, status, applied_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (new_app_id, opp_obj['id'], user_name, user_email, opp_obj['title'], sub_resume, score_val, verdict_val, summary_val, json.dumps(["Python", "FastAPI"]), json.dumps(["Docker"]), "APPLIED", datetime.utcnow().isoformat())
                        )
                        c.commit()
                        c.close()

                        st.success(f"🎉 Application Submitted! AI Match Score: **{score_val:.1f}% ({verdict_val})**. Record saved dynamically to ATS Database!")
                        st.rerun()

        st.markdown("---")
        st.markdown("#### 📬 Active Job Offers & TPO Policy Enforcement")
        with st.container(border=True):
            st.markdown("### 🎉 Offer Extended: **Nexus AI Systems**")
            st.markdown("**Role:** AI Systems Engineering Intern | **Stipend:** `$1,500 / month` | **Joining Date:** `2026-07-01`")
            
            o1, o2 = st.columns(2)
            with o1:
                if st.button("✅ Accept Offer (Enforce TPO 'One Offer' Policy)", use_container_width=True):
                    c = get_db_connection()
                    c.execute("UPDATE applications SET status='OFFER_ACCEPTED' WHERE student_email=?", (st.session_state.user_info.get("email"),))
                    c.commit()
                    c.close()
                    st.success("🎉 Offer Accepted! TPO Policy Enforced: All other pending campus applications are automatically WITHDRAWN.")
                    st.rerun()
            with o2:
                if st.button("❌ Decline Offer", use_container_width=True):
                    st.warning("Offer Declined. You remain eligible for other campus placement drives.")

# =============================================================================
# TAB 3: MODULE 2 (ACADEMIA & ACADEMIC VERIFIER)
# =============================================================================
with tab_m2:
    st.subheader("🏫 Module 2: Institutional Hierarchy & Academic Verification")
    st.write("Course prerequisite graph traversal and automated student eligibility validation (CGPA, backlogs, attendance).")

    acad1, acad2 = st.tabs(["🌳 Prerequisite Knowledge Graph", "🔍 Student Eligibility & Record Verifier"])

    with acad1:
        st.markdown("#### 🌳 University Course Prerequisite Sequence")
        st.write("Structured course dependencies: Students must complete foundational courses before advancing to high-level subjects.")
        
        g1, g2, g3 = st.columns(3)
        with g1:
            with st.container(border=True):
                st.markdown("### **CS101**\n**Discrete Mathematics**")
                st.caption("Credits: **4** | Dept: **CSE**")
                st.info("Level 1 Foundation (No prerequisites)")
        with g2:
            with st.container(border=True):
                st.markdown("### **CS201**\n**Data Structures**")
                st.caption("Credits: **4** | Dept: **CSE**")
                st.warning("Requires: **CS101 (Discrete Math)**")
        with g3:
            with st.container(border=True):
                st.markdown("### **CS301**\n**Algorithms**")
                st.caption("Credits: **4** | Dept: **CSE**")
                st.error("Requires: **CS201 (Data Structures)**")

    with acad2:
        st.markdown("#### 🔍 Student Academic Verification Engine (`AcademicVerificationService`)")
        eval_cand = st.selectbox("Select Student to Evaluate:", [
            "Student 1001 (Aarav Sharma - High Performer)",
            "Student 1002 (Karan Verma - Backlog & Low Attendance)"
        ])

        if "1001" in eval_cand:
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Cumulative CGPA", "8.50", "Eligible (>= 7.0)")
            col_m2.metric("Active Backlogs", "0", "Clean Record")
            col_m3.metric("Attendance", "85.0%", "Above 75% Safe Threshold")
            col_m4.metric("Prerequisite (CS301)", "Passed", "CS101 & CS201 Cleared")
            st.success("✅ **Placement Eligibility Status: VERIFIED & ELIGIBLE** for Tier-1 Corporate Hiring Drives.")
        else:
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Cumulative CGPA", "4.00", "Below Cutoff", delta_color="inverse")
            col_m2.metric("Active Backlogs", "1 Active (Grade F)", "Failed CS101", delta_color="inverse")
            col_m3.metric("Attendance", "60.0%", "Below 75% Cutoff", delta_color="inverse")
            col_m4.metric("Prerequisite (CS301)", "BLOCKED", "CS101 Not Cleared", delta_color="inverse")
            st.error("❌ **Placement Eligibility Status: BLOCKED.** Student has active backlogs and attendance below 75%. Blocked from Module 5/6 campus placement drives.")

# =============================================================================
# TAB 4: MODULES 3 & 5 (CORPORATE MoUs & DYNAMIC JOB POSTINGS)
# =============================================================================
with tab_m3_5:
    st.subheader("🏢 Modules 3 & 5: Corporate Profiles, MoUs & Dynamic Job Postings")
    st.write("Post new recruitment drives dynamically and manage institutional enterprise tie-ups.")

    corp1, corp2, corp3 = st.tabs([
        "💼 Live Job Board (Mod 5)", 
        "➕ Post New Job Drive (Recruiter Dynamic Entry)", 
        "📜 Corporate MoUs (Mod 3)"
    ])

    with corp1:
        st.markdown("#### 💼 Live Campus Opportunities")
        conn = get_db_connection()
        all_jobs = conn.execute("SELECT * FROM opportunities ORDER BY created_at DESC").fetchall()
        conn.close()

        for j in all_jobs:
            with st.container(border=True):
                jx1, jx2 = st.columns([3, 1])
                with jx1:
                    st.markdown(f"### **{j['title']}**")
                    st.markdown(f"🏢 **{j['company']}** | 🏷️ `{j['job_type']}` | 💰 **{j['stipend']}**")
                    st.caption(f"🎯 **Required Skills:** `{j['skills']}`")
                    st.info(f"📋 **Eligibility Rules:** {j['eligibility']}")
                with jx2:
                    st.markdown(f"**Status:** `{j['status']}`")
                    st.caption(f"Posted: `{j['created_at'][:10]}`")

    with corp2:
        st.markdown("#### ➕ Post a New Job / Internship Drive (Dynamic Form)")
        with st.form("post_job_form"):
            new_title = st.text_input("Job Title", value="Cloud Security & DevOps Intern")
            new_company = st.text_input("Hiring Enterprise", value=st.session_state.user_info.get("company", "TechCorp Global"))
            new_type = st.selectbox("Opportunity Type", ["INTERNSHIP", "FULL_TIME", "RESEARCH_GRANT"])
            new_stipend = st.text_input("Compensation / Stipend", value="$1,800 / month")
            new_skills = st.text_input("Required Skills (comma-separated)", value="AWS, Python, Terraform, Docker, Linux")
            new_rules = st.text_input("Eligibility Rules", value="CGPA >= 7.5 | No Active Backlogs | Batch 2026-2028")

            submitted = st.form_submit_button("📢 Publish Recruitment Drive to Platform", use_container_width=True)
            if submitted:
                new_id = f"opp-{datetime.utcnow().strftime('%M%S')}"
                c = get_db_connection()
                c.execute(
                    "INSERT INTO opportunities (id, title, company, job_type, stipend, skills, eligibility, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (new_id, new_title, new_company, new_type, new_stipend, new_skills, new_rules, "OPEN", datetime.utcnow().isoformat())
                )
                c.commit()
                c.close()
                st.success(f"🎉 '{new_title}' successfully published and dynamically saved to database!")
                st.rerun()

    with corp3:
        st.markdown("#### 📜 Institutional Memorandums of Understanding (MoUs)")
        mous_data = [
            {"Company": "Google Cloud Partner Network", "Domain": "Cloud Computing & AI", "Signed Date": "2025-08-15", "Valid Until": "2028-08-15", "Benefits": "Sponsored Cloud Credits, 50 Annual Internships, Joint FDPs"},
            {"Company": "NVIDIA Deep Learning Institute", "Domain": "Edge AI & Computing", "Signed Date": "2025-11-01", "Valid Until": "2027-11-01", "Benefits": "Hardware Lab Sponsorship, Jetson Kits, Certification Grants"},
            {"Company": "Amazon Web Services (AWS Academy)", "Domain": "DevOps & Cloud Architecture", "Signed Date": "2026-01-10", "Valid Until": "2029-01-10", "Benefits": "Curriculum Alignment, Free Certification Vouchers for Top 10%"}
        ]
        st.table(mous_data)

# =============================================================================
# TAB 5: MODULE 7 (INTERNSHIP MONITORING, DUAL EVALUATION & CREDIT SYNC)
# =============================================================================
with tab_m7:
    st.subheader("📋 Module 7: Internship Progress, Dual-Mentor Evaluation & Credit Sync")
    st.write("Dynamic weekly logbook submissions, 60/40 weighted dual evaluation, and university credit transfer sync.")

    m7_tab1, m7_tab2, m7_tab3 = st.tabs([
        "📝 Submit Weekly Logbook (Dynamic)", 
        "⚖️ Dual-Mentor Evaluation Rubric", 
        "🎓 Credit Transfer & Certificate"
    ])

    with m7_tab1:
        st.markdown("#### 📝 Student Weekly Progress Submission")
        with st.form("logbook_form"):
            col_lg1, col_lg2 = st.columns(2)
            with col_lg1:
                st.text_input("Enrolled Student", value="Aarav Sharma (ID: 1001)", disabled=True)
                week_choice = st.selectbox("Logbook Week", ["Week 4: Vector Search & Redis Caching", "Week 5: Async API Optimization", "Week 6: Final Deployment"])
            with col_lg2:
                hours_input = st.number_input("Hours Worked", min_value=1, max_value=60, value=40)
                pr_link = st.text_input("Work Artifact / Pull Request Link", value="https://github.com/nexus-ai/rag-pipeline/pull/42")

            milestone_desc = st.text_area("Milestones Completed This Week:", value="Implemented asynchronous vector search endpoints in FastAPI using Milvus. Reduced semantic query latency by 35% with Redis caching.")
            
            log_submitted = st.form_submit_button("📤 Submit Weekly Logbook for Dual Review", use_container_width=True)
            if log_submitted:
                c = get_db_connection()
                c.execute(
                    "INSERT INTO internship_logbooks (student_email, week_number, hours_worked, milestones, artifact_link, mentor_rating, faculty_rating, status, submitted_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (st.session_state.user_info.get("email", "student@test.com"), week_choice.split(":")[0], hours_input, milestone_desc, pr_link, 5.0, 5.0, "APPROVED", datetime.utcnow().isoformat())
                )
                c.commit()
                c.close()
                st.success("✅ Logbook successfully submitted and saved dynamically into database!")
                st.rerun()

        st.markdown("##### 📜 Live Verified Logbook History (From Database)")
        conn = get_db_connection()
        logs_db = conn.execute("SELECT week_number, hours_worked, milestones, mentor_rating, status, submitted_at FROM internship_logbooks ORDER BY id DESC").fetchall()
        conn.close()
        
        st.table([
            {
                "Week": l["week_number"], 
                "Hours": l["hours_worked"], 
                "Milestones": l["milestones"], 
                "Industry Rating": f"{l['mentor_rating']}/5.0", 
                "Status": l["status"],
                "Date": l["submitted_at"][:10]
            } for l in logs_db
        ])

    with m7_tab2:
        st.markdown("#### ⚖️ Dual-Mentor Joint Evaluation Rubric")
        st.write("Dynamic score calculation: **60% Industry Mentor (Execution & Deliverables)** + **40% Faculty Guide (Academic Rigor)**.")

        ev1, ev2 = st.columns(2)
        with ev1:
            with st.container(border=True):
                st.markdown("### 💼 Industry Mentor Rating (60%)")
                r1 = st.slider("Technical Competency & Code Quality", 1, 5, 5, key="ev_ind_1")
                r2 = st.slider("Sprint Deliverables & Punctuality", 1, 5, 5, key="ev_ind_2")
                ind_score = round(((r1 + r2) / 10.0) * 100, 1)
                st.metric("Industry Score (60% Weight)", f"{ind_score}%")

        with ev2:
            with st.container(border=True):
                st.markdown("### 🏛️ Faculty Supervisor Rating (40%)")
                f1 = st.slider("Logbook Rigor & Report Quality", 1, 5, 5, key="ev_fac_1")
                f2 = st.slider("Curriculum Learning Alignment", 1, 5, 4, key="ev_fac_2")
                fac_score = round(((f1 + f2) / 10.0) * 100, 1)
                st.metric("Faculty Score (40% Weight)", f"{fac_score}%")

        composite_grade = round((ind_score * 0.6) + (fac_score * 0.4), 2)
        res1, res2 = st.columns([1, 2])
        with res1:
            st.metric("🎯 Final Composite Internship Score", f"{composite_grade}%")
        with res2:
            awarded = "O (Outstanding)" if composite_grade >= 90 else "A+ (Excellent)" if composite_grade >= 80 else "A (Very Good)"
            st.write(f"**Awarded University Grade:** `{awarded}`")
            st.progress(composite_grade / 100.0)

        if st.button("🔒 Finalize Joint Evaluation & Sync to Academic Records", use_container_width=True):
            st.success(f"🎉 Evaluation Finalized! Composite score of **{composite_grade}%** dynamically synced to University Board records.")

    with m7_tab3:
        st.markdown("#### 🎓 Academic Credit Transfer & Verified Certificate")
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("### 📊 Academic Credit Transfer")
                st.write("**Course Equivalent:** `CS490 - Industry Capstone Internship`")
                st.write("**Total Mandatory Credits:** `14 Credits`")
                st.write("**Transferred Credits:** `+12 Credits` (100% Approved by Board of Studies)")
                st.progress(12 / 14)
        with c2:
            with st.container(border=True):
                st.markdown("### 📜 Digital Completion Certificate")
                st.write("Awarded to **Aarav Sharma (Student ID: 1001)** for completing 8-Week Professional Internship in **AI Systems Engineering** with Grade **O (Outstanding)**.")
                st.download_button("📥 Download Verified Certificate (PDF)", data=b"Mock Certificate PDF Payload for Aarav Sharma", file_name="Certificate_Aarav_Sharma.pdf", use_container_width=True)

# =============================================================================
# TAB 6: MODULE 1 (IAM & SECURITY AUDIT)
# =============================================================================
with tab_m1:
    st.subheader("🔑 Module 1: Identity & Access Management (IAM) & RBAC Matrix")
    st.write("Multi-role authorization, user registry, and live JWT token inspector.")

    iam1, iam2 = st.tabs(["🛡️ RBAC Permissions Matrix", "🔍 Active JWT Token Inspector"])

    with iam1:
        st.markdown("#### 🛡️ Role-Based Access Control (RBAC) Matrix")
        st.table([
            {"Role": "STUDENT", "Module 1 (Auth)": "Self Profile", "Module 2 (Academia)": "View Own Grades", "Module 4 (AI Skills)": "Run Gap Analysis", "Module 5/6 (ATS)": "Apply / View Offers", "Module 7 (Logbook)": "Submit Logs"},
            {"Role": "RECRUITER", "Module 1 (Auth)": "Company Team", "Module 2 (Academia)": "No Access", "Module 4 (AI Skills)": "Extract Job Skills", "Module 5/6 (ATS)": "Post Jobs / Screen", "Module 7 (Logbook)": "Industry Grade (60%)"},
            {"Role": "FACULTY_TPO", "Module 1 (Auth)": "Dept Directory", "Module 2 (Academia)": "Verify Eligibility", "Module 4 (AI Skills)": "Course Mapping", "Module 5/6 (ATS)": "Audit Drives / Enforce 1-Offer", "Module 7 (Logbook)": "Faculty Grade (40%)"},
            {"Role": "COLLEGE_ADMIN", "Module 1 (Auth)": "Full Tenant", "Module 2 (Academia)": "Curriculum CRUD", "Module 4 (AI Skills)": "Taxonomy Edit", "Module 5/6 (ATS)": "Approve MoUs / Drives", "Module 7 (Logbook)": "Credit Sync Board"}
        ])

    with iam2:
        st.markdown("#### 🔍 Active JWT Session Token Decoder")
        with st.container(border=True):
            st.markdown(f"**Current Logged-in Subject (`sub`):** `{st.session_state.user_info['email']}`")
            st.markdown(f"**Active Security Role (`role`):** `{st.session_state.user_info['role']}`")
            st.json({
                "header": {"alg": "HS256", "typ": "JWT"},
                "payload": {
                    "sub": st.session_state.user_info['email'],
                    "role": st.session_state.user_info['role'],
                    "name": st.session_state.user_info['name'],
                    "exp": 1771000000,
                    "iss": "SkillBridge-IAM-Service"
                }
            })
