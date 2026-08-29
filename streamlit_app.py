import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# --- 1. PAGE CONFIGURATION (WIDE LAYOUT) ---
st.set_page_config(
    page_title="SkillBridge AI | Academia-Industry Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SESSION STATE INITIALIZATION ---
if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# Helper function to check backend health
def check_backend():
    try:
        res = requests.get(f"{API_URL}/", timeout=2)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False

# --- 3. SIDEBAR: AUTHENTICATION & 1-CLICK PERSONA SWITCHER ---
with st.sidebar:
    st.title("🎓 SkillBridge AI")
    st.caption("Bridging Academic Curricula & Industry Demand")
    
    # Backend status indicator
    if check_backend():
        st.success("🟢 Backend Connected (`:8000`)")
    else:
        st.error("🔴 Backend Offline. Run `uvicorn main:app`")

    st.divider()

    if not st.session_state.token:
        st.subheader("⚡ 1-Click Persona Login")
        st.caption("Quick test accounts from `seed_db.py`:")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎓 Student", use_container_width=True):
                res = requests.post(f"{API_URL}/api/v1/auth/login", json={"email": "student@test.com", "password": "Student@123"})
                if res.status_code == 200:
                    st.session_state.token = res.json()["access_token"]
                    st.session_state.user_info = {"name": "Aarav Sharma", "role": "STUDENT", "email": "student@test.com"}
                    st.rerun()
        with col2:
            if st.button("💼 Recruiter", use_container_width=True):
                res = requests.post(f"{API_URL}/api/v1/auth/login", json={"email": "recruiter@company.com", "password": "Recruiter@123"})
                if res.status_code == 200:
                    st.session_state.token = res.json()["access_token"]
                    st.session_state.user_info = {"name": "Priya Mehta", "role": "RECRUITER", "email": "recruiter@company.com"}
                    st.rerun()

        if st.button("🏛️ Faculty / TPO", use_container_width=True):
            res = requests.post(f"{API_URL}/api/v1/auth/login", json={"email": "faculty@college.edu", "password": "Faculty@123"})
            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.session_state.user_info = {"name": "Dr. Rajesh Rao", "role": "FACULTY_TPO", "email": "faculty@college.edu"}
                st.rerun()

        st.divider()
        with st.expander("🔑 Manual Login / Register"):
            auth_mode = st.radio("Mode", ["Login", "Register"])
            m_email = st.text_input("Email")
            m_pass = st.text_input("Password", type="password")
            
            if auth_mode == "Register":
                m_name = st.text_input("Full Name")
                m_role = st.selectbox("Role", ["STUDENT", "FACULTY_TPO", "RECRUITER"])
                if st.button("Create Account", use_container_width=True):
                    r = requests.post(f"{API_URL}/api/v1/auth/register", json={
                        "email": m_email, "password": m_pass, "full_name": m_name, "role": m_role
                    })
                    if r.status_code == 201:
                        st.success("Registered! Switch to Login.")
                    else:
                        st.error(r.json().get("detail", "Registration failed"))
            else:
                if st.button("Log In", use_container_width=True):
                    r = requests.post(f"{API_URL}/api/v1/auth/login", json={"email": m_email, "password": m_pass})
                    if r.status_code == 200:
                        st.session_state.token = r.json()["access_token"]
                        st.session_state.user_info = {"name": m_email.split('@')[0], "role": "USER", "email": m_email}
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
    else:
        user = st.session_state.user_info
        with st.container(border=True):
            st.markdown(f"### 👤 **{user['name']}**")
            st.markdown(f"**Role:** `{user['role']}`")
            st.markdown(f"**Email:** `{user['email']}`")
        
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.token = None
            st.session_state.user_info = None
            st.rerun()

# --- 4. MAIN DASHBOARD CONTENT ---

st.title("🎓 Academia–Industry AI Collaboration Portal")
st.caption("AI-Powered Curriculum Mapping, Semantic Skill Gap Analysis, and Personalized Upskilling Roadmaps")

# KPI Summary Cards (Using native st.metric)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric(label="Placement Readiness Index", value="84%", delta="+12% this term")
kpi2.metric(label="Verified Industry Skills", value="142", delta="+28 new")
kpi3.metric(label="Active Industry MoUs", value="18", delta="3 Pending")
kpi4.metric(label="Avg. Gap Closure Time", value="2.8 wks", delta="-15% faster")

st.divider()

if not st.session_state.token:
    st.info("💡 **Welcome to the Demo:** Click any **1-Click Persona Login button** in the left sidebar to start testing.")
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # Modular Tabs for AI Tools
    tab1, tab2, tab3 = st.tabs([
        "📄 1. AI Skill Extractor", 
        "📊 2. AI Skill Gap Analysis", 
        "🎯 3. AI Personalized Recommendations"
    ])

    # --- TAB 1: AI SKILL EXTRACTOR ---
    with tab1:
        st.subheader("📄 Extract Competencies from Syllabus or Resume")
        st.write("Extract standardized technical skills, proficiencies, and contextual evidence from unstructured text.")

        sample_text = (
            "Course Syllabus: CS402 - Distributed Cloud Architecture.\n"
            "Topics: Hands-on microservices with FastAPI and Python. Implementing asynchronous worker queues with Redis. "
            "Container orchestration using Docker and Kubernetes. Relational data modeling using PostgreSQL and SQLAlchemy. "
            "CI/CD pipeline automation with GitHub Actions and AWS EC2 deployments."
        )

        raw_input = st.text_area("Paste Course Syllabus, Resume, or Project Report:", value=sample_text, height=140)

        if st.button("🚀 Extract Skills with AI", use_container_width=True):
            with st.spinner("AI analyzing text and identifying proficiencies..."):
                try:
                    res = requests.post(f"{API_URL}/api/v1/ai-skills/extract", json={"raw_text": raw_input}, headers=headers)
                    if res.status_code == 200:
                        data = res.json()
                        st.success(f"**Extraction Summary:** {data.get('summary')}")
                        st.markdown("### 🏷️ Identified Competencies")
                        
                        cols = st.columns(2)
                        for idx, item in enumerate(data.get("extracted_skills", [])):
                            with cols[idx % 2]:
                                with st.container(border=True):
                                    st.markdown(f"#### **{item['skill_name']}** `[{item['proficiency_level']}]`")
                                    st.markdown(f"**Category:** {item['category']}")
                                    st.caption(f"_{item['context_found']}_")
                    else:
                        st.error(f"Error ({res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")

    # --- TAB 2: AI GAP ANALYSIS ---
    with tab2:
        st.subheader("📊 Semantic Skill Gap & Readiness Scoring")
        st.write("Compare candidate competencies against real-world Job Descriptions to compute readiness percentage and identify critical deficiencies.")

        c1, c2 = st.columns(2)
        with c1:
            target_role = st.text_input("Target Job Title", value="Full Stack AI / ML Engineer")
            target_jd = st.text_area(
                "Target Job Description (JD)", 
                height=160, 
                value="Looking for a Full Stack AI Engineer. Requirements: Expert in Python and PyTorch. Experience with LLM frameworks like LangChain/Instructor, Vector Databases (Pinecone/Milvus), Docker containerization, Kubernetes, and building async APIs with FastAPI."
            )
        with c2:
            st.text_input("Candidate Name", value=st.session_state.user_info.get("name", "Student Candidate"), disabled=True)
            candidate_profile = st.text_area(
                "Candidate Resume / Stated Skills", 
                height=160, 
                value="Computer Science final year student. Proficient in Python, SQL, and FastAPI. Built simple REST APIs and small web scrapers. Basic understanding of Machine Learning linear regression. Have not worked with Docker, Kubernetes, or Vector DBs yet."
            )

        if st.button("⚡ Run AI Gap Analysis", use_container_width=True):
            with st.spinner("Computing semantic gap & evaluating readiness..."):
                try:
                    payload = {
                        "target_role": target_role,
                        "target_job_description": target_jd,
                        "user_bio_or_resume": candidate_profile
                    }
                    res = requests.post(f"{API_URL}/api/v1/ai-skills/gap-analysis", json=payload, headers=headers)
                    if res.status_code == 200:
                        analysis = res.json()
                        score = analysis["readiness_score"]

                        st.divider()
                        
                        # Score Card using native st.metric and st.progress
                        score_col1, score_col2 = st.columns([1, 2])
                        with score_col1:
                            st.metric(label="AI Readiness Score", value=f"{score}%")
                        with score_col2:
                            assessment = "🟢 Strong Candidate" if score >= 75 else "🟡 Upskilling Needed" if score >= 50 else "🔴 Significant Skill Gaps"
                            st.write(f"**Readiness Assessment:** {assessment}")
                            st.progress(score / 100.0)

                        st.info(f"**Industry Alignment Summary:** {analysis.get('industry_alignment_summary')}")

                        g_col1, g_col2 = st.columns(2)
                        with g_col1:
                            st.markdown("### ✅ Verified Strengths")
                            for strength in analysis.get("strengths", []):
                                st.success(f"✔️ {strength}")
                        
                        with g_col2:
                            st.markdown("### 🚨 Critical Missing Skills & Remedies")
                            for gap in analysis.get("critical_missing_skills", []):
                                with st.container(border=True):
                                    st.markdown(f"**{gap['skill_name']}** `({gap['importance']})`")
                                    st.write(gap['gap_description'])
                                    st.caption(f"💡 **Remedy:** {gap['recommended_remedy']}")
                    else:
                        st.error(f"Error ({res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")

    # --- TAB 3: AI PERSONALIZED RECOMMENDATIONS ---
    with tab3:
        st.subheader("🎯 Personalized Certifications, Projects & Internships")
        st.write("Generates customized upskilling roadmaps tailored dynamically for Students or Faculty.")

        col_a, col_b = st.columns(2)
        with col_a:
            persona_type = st.selectbox("Target Persona", ["STUDENT", "FACULTY"])
            career_goals = st.text_input(
                "Career / Research Aspirations", 
                value="Become an AI Engineer specializing in Autonomous Robotics & Edge Vision" if persona_type == "STUDENT" else "Establish a funded Industry CoE in IoT & Edge Computing"
            )
            dept = st.text_input("Department", value="Computer Science & Engineering")
        with col_b:
            interests_input = st.text_input("Specific Interests (comma-separated)", value="Robotics, Edge Devices, Computer Vision, Embedded AI")
            skills_input = st.text_input("Existing Skills (comma-separated)", value="Python, PyTorch, OpenCV, Linux")

        if st.button("✨ Generate AI Career Roadmap", use_container_width=True):
            with st.spinner("Synthesizing custom learning pathway with LLM reasoning..."):
                try:
                    rec_payload = {
                        "persona": persona_type,
                        "career_goals": career_goals,
                        "interests": [i.strip() for i in interests_input.split(",") if i.strip()],
                        "current_skills": [s.strip() for s in skills_input.split(",") if s.strip()],
                        "academic_department": dept
                    }
                    res = requests.post(f"{API_URL}/api/v1/ai-skills/recommendations", json=rec_payload, headers=headers)
                    if res.status_code == 200:
                        recs = res.json()
                        st.success(f"**Strategic Pathway Summary:** {recs.get('strategic_pathway_summary')}")
                        st.divider()

                        r_col1, r_col2, r_col3 = st.columns(3)

                        with r_col1:
                            st.markdown("### 📜 Certifications")
                            for cert in recs.get("certifications", []):
                                with st.container(border=True):
                                    st.markdown(f"#### **{cert['title']}**")
                                    st.markdown(f"**Provider:** `{cert['platform_provider']}`")
                                    st.caption(f"**Duration:** {cert['duration']}")
                                    st.write(cert['why_recommended'])

                        with r_col2:
                            st.markdown("### 💻 Hands-on Projects")
                            for proj in recs.get("hands_on_projects", []):
                                with st.container(border=True):
                                    st.markdown(f"#### **{proj['title']}** `[{proj['difficulty']}]`")
                                    st.markdown(f"**Tech Stack:** `{'`, `'.join(proj.get('suggested_tech_stack', []))}`")
                                    st.write(proj['project_summary'])
                                    st.caption(f"🎯 **Impact:** {proj.get('portfolio_impact', '')}")

                        with r_col3:
                            st.markdown("### 💼 Opportunities & Grants")
                            for opp in recs.get("opportunities", []):
                                with st.container(border=True):
                                    st.markdown(f"#### **{opp['title']}**")
                                    st.markdown(f"**Type:** `{opp['type']}`")
                                    st.markdown(f"**Domain:** {opp['suggested_domain']}")
                                    st.caption(f"_{opp['relevance_to_goals']}_")
                    else:
                        st.error(f"Error ({res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Connection Error: {str(e)}")