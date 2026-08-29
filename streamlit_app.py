import streamlit as st
import requests
import json
from datetime import datetime

# --- LOAD SECRETS (Works both on Streamlit Cloud and Locally) ---
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
GROQ_MODEL = st.secrets.get("GROQ_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))
API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://127.0.0.1:8000"))

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="SkillBridge AI | SIH DECiphers Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SESSION STATE ---
if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None

def check_backend():
    try:
        res = requests.get(f"{API_URL}/", timeout=2)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False

# --- 3. SIDEBAR: 1-CLICK PERSONA SWITCHER ---
with st.sidebar:
    st.title("🎓 SIH 26044")
    st.caption("Academia–Industry Collaboration | Team DECiphers")
    
    if check_backend():
        st.success("🟢 Backend Connected (`:8000`)")
    else:
        st.info("🟡 Standalone Live Demo Mode")

    st.divider()

    if not st.session_state.token:
        st.subheader("⚡ 1-Click Persona Login")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎓 Student", use_container_width=True):
                st.session_state.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHVkZW50QHRlc3QuY29tIiwicm9sZSI6IlNUVURFTlQiLCJleHAiOjE3NzEwMDAwMDB9.mockSignature"
                st.session_state.user_info = {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "name": "Aarav Sharma", 
                    "role": "STUDENT", 
                    "email": "student@test.com",
                    "student_id": 1001,
                    "dept": "Computer Science Engineering",
                    "cgpa": 8.5,
                    "attendance": 85.0,
                    "internship": "Nexus AI Systems"
                }
                st.rerun()
        with col2:
            if st.button("💼 Recruiter", use_container_width=True):
                st.session_state.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyZWNydWl0ZXJAY29tcGFueS5jb20iLCJyb2xlIjoiUkVDUlVJVEVSIiwiZXhwIjoxNzcxMDAwMDAwfQ.mockSignature"
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
                st.session_state.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmYWN1bHR5QGNvbGxlZ2UuZWR1Iiwicm9sZSI6IkZBQ1VMVFlfVFBPIiwiZXhwIjoxNzcxMDAwMDAwfQ.mockSignature"
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
                st.session_state.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBjb2xsZWdlLmVkdSIsInJvbGUiOiJDT0xMRUdFX0FETUlOIiwiZXhwIjoxNzcxMDAwMDAwfQ.mockSignature"
                st.session_state.user_info = {
                    "id": "44444444-4444-4444-4444-444444444444",
                    "name": "University Dean", 
                    "role": "COLLEGE_ADMIN", 
                    "email": "admin@college.edu"
                }
                st.rerun()
    else:
        user = st.session_state.user_info
        with st.container(border=True):
            st.markdown(f"### 👤 **{user['name']}**")
            st.markdown(f"**Role:** `{user['role']}`")
            st.markdown(f"**Email:** `{user['email']}`")
            if "cgpa" in user:
                st.caption(f"🎓 CGPA: **{user['cgpa']}** | Attendance: **{user['attendance']}%**")
        
        if st.button("🚪 Switch Persona / Log Out", use_container_width=True):
            st.session_state.token = None
            st.session_state.user_info = None
            st.rerun()

# --- 4. TOP KPI METRICS ---
st.title("🎓 Academia–Industry Collaboration & AI Placement Portal")
st.caption("Unified Dashboard Covering Modules 1 through 7 | Team DECiphers")

k1, k2, k3, k4 = st.columns(4)
k1.metric(label="Placement Readiness", value="86.4%", delta="+14.2% vs. cohort")
k2.metric(label="Skills Mapped", value="248", delta="+36 syllabus tags")
k3.metric(label="Active MoUs", value="19", delta="4 New Industry Tie-ups")
k4.metric(label="Credit Transfer Sync", value="94.2%", delta="+8% on-time grading")

st.divider()

if not st.session_state.token:
    st.info("💡 **Welcome to the Demo:** Select any **Persona from the sidebar** to unlock all 6 module tabs.")
else:
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # All 6 Functional Tabs (Covering Modules 1 to 7)
    tab_m1, tab_m4, tab_m6, tab_m2, tab_m3_5, tab_m7 = st.tabs([
        "🔑 1. IAM & Access Control (Mod 1)",
        "🧠 2. AI Skill & Gap Engine (Mod 4)",
        "💼 3. AI-ATS & Recruitment (Mod 6)",
        "🏫 4. Academia & Verifier (Mod 2)",
        "🏢 5. MoUs & Opportunities (Mod 3 & 5)",
        "📋 6. Internship & Credits (Mod 7)"
    ])

    # =========================================================================
    # TAB 1: MODULE 1 (IAM, RBAC & SECURITY AUDIT)
    # =========================================================================
    with tab_m1:
        st.subheader("🔑 Module 1: Identity & Access Management (IAM) & Multi-Role RBAC")
        st.write("Stateless JWT authentication, password hashing, multi-tenancy IDs, and role authorization matrices.")

        iam_sub1, iam_sub2, iam_sub3 = st.tabs([
            "📋 User Directory (portal.db)", 
            "🛡️ RBAC Permissions Matrix", 
            "🔍 Active JWT Token Inspector"
        ])

        with iam_sub1:
            st.markdown("#### 👥 Registered Multi-Tenant Users in `portal.db`")
            users_table = [
                {"Full Name": "Aarav Sharma", "Email": "student@test.com", "Role": "STUDENT", "Tenant / Link ID": "GTU-CSE-2028-1001", "Status": "Active & Verified"},
                {"Full Name": "Priya Mehta", "Email": "recruiter@company.com", "Role": "RECRUITER", "Tenant / Link ID": "NEXUS-AI-CORP-99", "Status": "Active & Verified"},
                {"Full Name": "Dr. Rajesh Rao", "Email": "faculty@college.edu", "Role": "FACULTY_TPO", "Tenant / Link ID": "GTU-FACULTY-402", "Status": "Active & Verified"},
                {"Full Name": "College Dean", "Email": "admin@college.edu", "Role": "COLLEGE_ADMIN", "Tenant / Link ID": "GTU-ADMIN-01", "Status": "Active & Verified"},
                {"Full Name": "System Admin", "Email": "superadmin@portal.gov", "Role": "SUPER_ADMIN", "Tenant / Link ID": "SYSTEM-ROOT", "Status": "Active & Verified"}
            ]
            st.table(users_table)

        with iam_sub2:
            st.markdown("#### 🛡️ Role-Based Access Control (RBAC) Policy Matrix")
            rbac_rules = [
                {"Role": "STUDENT", "Module 1 (Auth)": "Self Profile", "Module 2 (Academia)": "View Own Grades", "Module 4 (AI Skills)": "Run Gap Analysis", "Module 5/6 (ATS)": "Apply / View Offers", "Module 7 (Logbook)": "Submit Logs"},
                {"Role": "RECRUITER", "Module 1 (Auth)": "Company Team", "Module 2 (Academia)": "No Access", "Module 4 (AI Skills)": "Extract Job Skills", "Module 5/6 (ATS)": "Post Jobs / Screen", "Module 7 (Logbook)": "Industry Grade (60%)"},
                {"Role": "FACULTY_TPO", "Module 1 (Auth)": "Dept Directory", "Module 2 (Academia)": "Verify Eligibility", "Module 4 (AI Skills)": "Course Mapping", "Module 5/6 (ATS)": "Audit Drives / Enforce 1-Offer", "Module 7 (Logbook)": "Faculty Grade (40%)"},
                {"Role": "COLLEGE_ADMIN", "Module 1 (Auth)": "Full Tenant", "Module 2 (Academia)": "Curriculum CRUD", "Module 4 (AI Skills)": "Taxonomy Edit", "Module 5/6 (ATS)": "Approve MoUs / Drives", "Module 7 (Logbook)": "Credit Sync Board"}
            ]
            st.table(rbac_rules)

        with iam_sub3:
            st.markdown("#### 🔍 Active JWT Session Token Decoder")
            with st.container(border=True):
                st.markdown(f"**Current Logged-in Subject (`sub`):** `{st.session_state.user_info['email']}`")
                st.markdown(f"**Active Security Role (`role`):** `{st.session_state.user_info['role']}`")
                st.markdown("**Algorithm:** `HS256` | **Token Type:** `Bearer (Access Token)`")
                
                st.text_area("Encoded JWT Bearer String:", value=st.session_state.token, height=70, disabled=True)
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

    # =========================================================================
    # TAB 2: MODULE 4 (AI SKILL MAPPING & GAP ENGINE)
    # =========================================================================
    with tab_m4:
        st.subheader("🧠 Module 4: Intelligent Skill Extraction, Gap Scoring & Pathways")
        st.write("Maps academic curricula to industry demand using Groq LLM reasoning.")

        subtab1, subtab2, subtab3 = st.tabs(["📄 Syllabus/Resume Extractor", "📊 Job Gap Analysis", "🎯 Personalized Pathways"])

        with subtab1:
            st.markdown("#### 📄 Extract Skills from Course Syllabus or Resume")
            sample_syllabus = (
                "Course Code: CS402 - Distributed AI & Cloud Systems\n"
                "Topics: Asynchronous API design with Python and FastAPI. Relational database indexing with PostgreSQL. "
                "Background task queues with Redis and Celery. Container orchestration with Docker and Kubernetes. "
                "Vector search with Milvus and Pinecone for RAG architectures. CI/CD pipelines with GitHub Actions."
            )
            raw_text = st.text_area("Paste Syllabus or Resume Text:", value=sample_syllabus, height=120)

            if st.button("🚀 Run AI Skill Extractor", use_container_width=True):
                with st.spinner("AI parsing technical competencies and proficiencies..."):
                    st.success("**Extraction Summary:** Identified 6 cloud-native backend and AI competencies.")
                    c1, c2 = st.columns(2)
                    with c1:
                        with st.container(border=True):
                            st.markdown("##### **FastAPI / Python** `[Advanced]`")
                            st.caption("Category: Web Architecture | _'Asynchronous API design with Python and FastAPI'_")
                        with st.container(border=True):
                            st.markdown("##### **PostgreSQL** `[Intermediate]`")
                            st.caption("Category: Database Systems | _'Relational database indexing with PostgreSQL'_")
                    with c2:
                        with st.container(border=True):
                            st.markdown("##### **Vector Databases (Milvus/Pinecone)** `[Advanced]`")
                            st.caption("Category: Generative AI / RAG | _'Vector search for RAG architectures'_")
                        with st.container(border=True):
                            st.markdown("##### **Docker & Kubernetes** `[Intermediate]`")
                            st.caption("Category: Cloud & DevOps | _'Container orchestration with Docker and Kubernetes'_")

        with subtab2:
            st.markdown("#### 📊 Semantic Job Readiness & Skill Gap Evaluator")
            col_l, col_r = st.columns(2)
            with col_l:
                target_role = st.text_input("Target Job Title", value="Full-Stack AI Systems Engineer")
                target_jd = st.text_area("Job Requirements:", height=130, value="Requirements: Proficient in Python, FastAPI, PyTorch, Vector Databases (Pinecone/Milvus), Docker containerization, Kubernetes, and AWS EC2 deployments.")
            with col_r:
                cand_name = st.session_state.user_info.get("name", "Student")
                st.text_input("Candidate Name", value=cand_name, disabled=True)
                cand_resume = st.text_area("Candidate Resume / Profile:", height=130, value="Final-year student. Strong in Python, FastAPI REST APIs, SQL, and database design. Built small web scrapers and machine learning regression models. Have not worked with Docker, Kubernetes, or Vector DBs yet.")

            if st.button("⚡ Run AI Gap Analysis", use_container_width=True):
                score = 78.5
                score_col1, score_col2 = st.columns([1, 2])
                score_col1.metric("AI Job Readiness Score", f"{score}%")
                with score_col2:
                    st.write("**Assessment:** 🟡 Upskilling Needed")
                    st.progress(score / 100.0)
                st.info("**Industry Summary:** Candidate demonstrates strong backend fundamentals in Python and FastAPI, but lacks containerization and vector embedding infrastructure experience required for enterprise RAG roles.")
                
                g1, g2 = st.columns(2)
                with g1:
                    st.markdown("##### ✅ Matched Strengths")
                    st.success("✔️ Python Asynchronous Development")
                    st.success("✔️ REST API Architecture (FastAPI)")
                with g2:
                    st.markdown("##### 🚨 Critical Missing Skills & Remedies")
                    with st.container(border=True):
                        st.markdown("**Docker & Kubernetes** `(Critical)`")
                        st.caption("💡 **Remedy:** Complete Course CS402 Module 4 or Docker Certified Associate track.")

        with subtab3:
            st.markdown("#### 🎯 Personalized Upskilling Roadmaps for Students & Faculty")
            c_a, c_b = st.columns(2)
            with c_a:
                persona_type = st.selectbox("Target Persona", ["STUDENT", "FACULTY"])
                career_goals = st.text_input("Career / R&D Aspirations", value="Specialize in AI Systems & Production Agentic RAG Pipelines" if persona_type == "STUDENT" else "Establish a funded Industry Center of Excellence (CoE) in IoT & Edge AI")
            with c_b:
                interests_in = st.text_input("Stated Interests", value="Generative AI, Vector Databases, Docker, Distributed Systems")
                skills_in = st.text_input("Current Skills", value="Python, FastAPI, SQL, Linux")

            if st.button("✨ Generate AI Career Roadmap", use_container_width=True):
                r1, r2, r3 = st.columns(3)
                with r1:
                    st.markdown("### 📜 Certifications")
                    with st.container(border=True):
                        st.markdown("#### **AWS Certified Machine Learning**")
                        st.caption("Provider: `AWS` | Duration: **6 Weeks**")
                        st.write("Validates cloud model hosting and data pipeline integration.")
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
                        st.caption("Type: `Industry Internship` | Domain: **Enterprise AI**")
                        st.write("_Aligned with Nexus AI Systems hiring tracks._")

    # =========================================================================
    # TAB 3: MODULE 6 (AI-ATS & RECRUITMENT PIPELINE)
    # =========================================================================
    with tab_m6:
        st.subheader("💼 Module 6: Recruitment & Application Workflow Engine (ATS)")
        st.write("Real-time AI resume screening, stage management, custom AI interview questions, and TPO policy enforcement.")

        ats_tab1, ats_tab2 = st.tabs(["📋 Recruiter Live ATS Pipeline", "📝 Student Application & Offer Portal"])

        with ats_tab1:
            st.markdown("#### 💼 Live Applicant Pipeline (Ranked by AI Match Score)")
            candidates = [
                {
                    "id": "app-001",
                    "student_name": "Aarav Sharma",
                    "email": "student@test.com",
                    "role": "AI Systems Engineering Intern",
                    "match_score": 86.5,
                    "verdict": "STRONG_MATCH",
                    "summary": "Excellent Python/FastAPI backend fundamentals. Strong relational DB design. Ready for technical round.",
                    "status": "INTERVIEW_SCHEDULED",
                    "strengths": ["Python", "FastAPI", "PostgreSQL", "REST APIs"]
                },
                {
                    "id": "app-002",
                    "student_name": "Rohan Gupta",
                    "email": "rohan@test.com",
                    "role": "AI Systems Engineering Intern",
                    "match_score": 64.0,
                    "verdict": "POTENTIAL_MATCH",
                    "summary": "Has good general programming knowledge in C++, but lacks async microservice experience.",
                    "status": "APPLIED",
                    "strengths": ["C++", "Python Basics"]
                }
            ]

            for cand in candidates:
                with st.container(border=True):
                    col_x, col_y, col_z = st.columns([2, 1, 1])
                    with col_x:
                        st.markdown(f"### 👤 {cand['student_name']} `({cand['email']})`")
                        st.caption(f"🤖 Verdict: `{cand['verdict']}` | Summary: _{cand['summary']}_")
                        st.write(f"**Strengths:** `{'`, `'.join(cand['strengths'])}`")
                    with col_y:
                        st.metric("AI Match Score", f"{cand['match_score']}%")
                        st.markdown(f"**Status:** `{cand['status']}`")
                    with col_z:
                        new_st = st.selectbox("Stage", ["APPLIED", "SHORTLISTED", "INTERVIEW_SCHEDULED", "OFFER_EXTENDED", "REJECTED"], index=["APPLIED", "SHORTLISTED", "INTERVIEW_SCHEDULED", "OFFER_EXTENDED", "REJECTED"].index(cand["status"]), key=f"st_{cand['id']}")
                        if st.button("💾 Save Stage", key=f"btn_{cand['id']}"):
                            st.success(f"Status for {cand['student_name']} updated to `{new_st}`!")

                    with st.expander(f"🎯 Generate Custom AI Interview Questions for {cand['student_name']}"):
                        if st.button("Generate Questions with Groq AI", key=f"q_{cand['id']}"):
                            st.markdown(f"##### 📋 Generated Questions for `{cand['student_name']}`:")
                            st.markdown("1. **How do you handle connection pooling and transaction rollbacks in async FastAPI applications using SQLAlchemy 2.0?**")
                            st.caption("🎯 *Target Skill:* `FastAPI & PostgreSQL` | 💡 *Why Ask:* Validates production backend claims.")
                            st.markdown("2. **Since your resume does not mention Docker, explain how you would isolate and containerize your microservice for deployment on Kubernetes?**")
                            st.caption("🎯 *Target Skill:* `Docker / Containerization` | 💡 *Why Ask:* Directly probes identified resume gap.")

        with ats_tab2:
            st.markdown("#### 📝 Student Opportunity Submission & Offer Tracker")
            with st.container(border=True):
                st.markdown("### 💼 Job Opening: **AI Systems Engineering Intern**")
                st.caption("Company: **Nexus AI Systems** | Location: **Hybrid** | Stipend: **$1,500 / Month**")
                user_res = st.text_area("Your Resume Submission Text:", value="Aarav Sharma | Email: student@test.com\nProficient in Python, building async APIs with FastAPI, and relational modeling with PostgreSQL. Built an intelligent search engine prototype and automated data pipelines.", height=80)
                if st.button("🚀 Submit Application & Run Real-time AI Screening"):
                    st.success("🎉 Application Submitted! AI Match Score: **86.5% (STRONG_MATCH)**. Profile ranked #1 in recruiter pipeline.")

            st.markdown("---")
            st.markdown("#### 📬 Active Job Offers & TPO Policy Enforcement")
            with st.container(border=True):
                st.markdown("### 🎉 Offer Extended: **Nexus AI Systems**")
                st.markdown("**Role:** AI Systems Engineering Intern | **Stipend:** `$1,500 / month` | **Joining Date:** `2026-07-01`")
                o_c1, o_c2 = st.columns(2)
                with o_c1:
                    if st.button("✅ Accept Offer (Enforce TPO 'One Offer' Policy)", use_container_width=True):
                        st.success("🎉 Offer Accepted! TPO Policy Enforced: All other pending applications are automatically WITHDRAWN.")
                with o_c2:
                    if st.button("❌ Decline Offer", use_container_width=True):
                        st.warning("Offer Declined.")

    # =========================================================================
    # TAB 4: MODULE 2 (ACADEMIA & ACADEMIC VERIFIER)
    # =========================================================================
    with tab_m2:
        st.subheader("🏫 Module 2: Institutional Hierarchy & Academic Verification")
        st.write("Prerequisite knowledge graphs, student eligibility calculations (CGPA, backlogs, attendance).")

        acad1, acad2 = st.tabs(["🌳 Prerequisite Knowledge Graph", "🔍 Student Eligibility & Record Verifier"])

        with acad1:
            st.markdown("#### 🌳 University Course Prerequisite Sequence")
            c_g1, c_g2, c_g3 = st.columns(3)
            with c_g1:
                with st.container(border=True):
                    st.markdown("### **CS101**\n**Discrete Mathematics**")
                    st.info("Level 1 Foundation")
            with c_g2:
                with st.container(border=True):
                    st.markdown("### **CS201**\n**Data Structures**")
                    st.warning("Requires: **CS101**")
            with c_g3:
                with st.container(border=True):
                    st.markdown("### **CS301**\n**Algorithms**")
                    st.error("Requires: **CS201**")

        with acad2:
            st.markdown("#### 🔍 Student Academic Verification Engine (`AcademicVerificationService`)")
            eval_student = st.selectbox("Select Student:", ["Student 1001 (Aarav Sharma - High Performer)", "Student 1002 (Karan Verma - Backlog & Low Attendance)"])

            if "1001" in eval_student:
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                col_m1.metric("Cumulative CGPA", "8.50", "Eligible (>= 7.0)")
                col_m2.metric("Active Backlogs", "0", "Clean Record")
                col_m3.metric("Attendance", "85.0%", "Above 75% Cutoff")
                col_m4.metric("Prerequisite (CS301)", "Passed", "CS101 & CS201 Cleared")
                st.success("✅ **Placement Status: VERIFIED & ELIGIBLE** for Tier-1 Corporate Hiring Drives.")
            else:
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                col_m1.metric("Cumulative CGPA", "4.00", "Below Cutoff", delta_color="inverse")
                col_m2.metric("Active Backlogs", "1 Active (Grade F)", "Failed CS101", delta_color="inverse")
                col_m3.metric("Attendance", "60.0%", "Below 75% Cutoff", delta_color="inverse")
                col_m4.metric("Prerequisite (CS301)", "BLOCKED", "CS101 Not Cleared", delta_color="inverse")
                st.error("❌ **Placement Status: BLOCKED.** Student has active backlogs and attendance below 75%.")

    # =========================================================================
    # TAB 5: MODULES 3 & 5 (CORPORATE MoUs & OPPORTUNITIES)
    # =========================================================================
    with tab_m3_5:
        st.subheader("🏢 Modules 3 & 5: Corporate Profiles, MoUs & Opportunities")
        corp1, corp2 = st.tabs(["💼 Live Campus Recruitment Drives (Mod 5)", "📜 Corporate MoUs & Tie-ups (Mod 3)"])

        with corp1:
            jobs = [
                {"title": "AI Systems Engineering Intern", "company": "Nexus AI Systems", "type": "INTERNSHIP", "stipend": "$1,500 / month", "eligibility": "CGPA >= 7.5 | No Backlogs", "skills": "Python, FastAPI, Docker, Vector DBs"},
                {"title": "Graduate Cloud & DevOps Engineer", "company": "CloudScale Infrastructure", "type": "FULL_TIME", "stipend": "$85,000 / year", "eligibility": "CGPA >= 7.0 | Attendance >= 75%", "skills": "AWS, Docker, Kubernetes, Linux"}
            ]
            for job in jobs:
                with st.container(border=True):
                    j1, j2 = st.columns([3, 1])
                    j1.markdown(f"### **{job['title']}**\n🏢 **{job['company']}** | 💰 **{job['stipend']}**\n- 🎯 Required Skills: `{job['skills']}`\n- 📋 Rules: `{job['eligibility']}`")
                    with j2:
                        st.markdown("**Status:** `OPEN`")
                        if st.button("Apply via ATS (Mod 6)", key=f"j_{job['title']}"):
                            st.success(f"Application ready in Tab 3!")

        with corp2:
            mous = [
                {"Company": "Google Cloud Partner Network", "Domain": "Cloud Computing & AI", "Signed Date": "2025-08-15", "Valid Until": "2028-08-15", "Benefits": "Sponsored Cloud Credits, 50 Annual Internships, Joint FDPs"},
                {"Company": "NVIDIA Deep Learning Institute", "Domain": "Edge AI & Computing", "Signed Date": "2025-11-01", "Valid Until": "2027-11-01", "Benefits": "Hardware Lab Sponsorship, Jetson Kits, Certification Grants"}
            ]
            st.table(mous)

    # =========================================================================
    # TAB 6: MODULE 7 (INTERNSHIP MONITORING & CREDIT SYNC)
    # =========================================================================
    with tab_m7:
        st.subheader("📋 Module 7: Internship Monitoring, Dual Evaluation & Credit Sync")
        mod7_1, mod7_2, mod7_3 = st.tabs(["📝 Weekly Milestone Logbook", "⚖️ Dual-Mentor Evaluation", "🎓 Credit Transfer & Certificate"])

        with mod7_1:
            with st.container(border=True):
                col_l1, col_l2 = st.columns(2)
                col_l1.text_input("Enrolled Student", value="Aarav Sharma (ID: 1001)", disabled=True)
                col_l2.text_input("Host Enterprise", value="Nexus AI Systems", disabled=True)
                tasks = st.text_area("Tasks Completed This Week:", value="Implemented asynchronous vector search endpoints in FastAPI using Milvus. Reduced semantic query latency by 35% with Redis caching.")
                if st.button("📤 Submit Weekly Logbook", use_container_width=True):
                    st.success("✅ Logbook for Week 4 submitted for dual-mentor signoff!")

        with mod7_2:
            eval_col1, eval_col2 = st.columns(2)
            with eval_col1:
                with st.container(border=True):
                    st.markdown("### 💼 Industry Mentor Rating (60%)")
                    r1 = st.slider("Technical Competency", 1, 5, 5, key="i1")
                    r2 = st.slider("Sprint Deliverables", 1, 5, 5, key="i2")
                    ind_score = round(((r1 + r2) / 10.0) * 100, 1)
                    st.metric("Industry Score (60% Weight)", f"{ind_score}%")
            with eval_col2:
                with st.container(border=True):
                    st.markdown("### 🏛️ Faculty Supervisor Rating (40%)")
                    f1 = st.slider("Logbook Quality", 1, 5, 5, key="f1")
                    f2 = st.slider("Curriculum Alignment", 1, 5, 4, key="f2")
                    fac_score = round(((f1 + f2) / 10.0) * 100, 1)
                    st.metric("Faculty Score (40% Weight)", f"{fac_score}%")

            composite = round((ind_score * 0.6) + (fac_score * 0.4), 2)
            st.metric("🎯 Final Composite Internship Score", f"{composite}%", "Awarded Grade: O (Outstanding)")
            if st.button("🔒 Finalize Evaluation & Sync Credits", use_container_width=True):
                st.success(f"Evaluation Finalized! Composite score of **{composite}%** synced to university board records.")

        with mod7_3:
            c_card1, c_card2 = st.columns(2)
            with c_card1:
                with st.container(border=True):
                    st.markdown("### 📊 Academic Credit Transfer")
                    st.write("**Course Equivalent:** `CS490 - Industry Capstone Internship`")
                    st.write("**Transferred Credits:** `+12 Credits` (Approved by Board of Studies)")
                    st.progress(12 / 14)
            with c_card2:
                with st.container(border=True):
                    st.markdown("### 📜 Digital Completion Certificate")
                    st.write("Awarded to **Aarav Sharma** for completing 8-Week AI Systems Internship with Grade **O (Outstanding)**.")
                    st.download_button("📥 Download Verified Certificate (PDF)", data=b"Certificate PDF Payload", file_name="Certificate_Aarav_Sharma.pdf", use_container_width=True)
