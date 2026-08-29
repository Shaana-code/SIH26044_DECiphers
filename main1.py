import streamlit as st
import pandas as pd
from datetime import datetime, date

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="DECiphers: Campus-Corporate Bridge", layout="wide")

# --- 2. INITIALIZE SESSION STATE (Using your specific Entity Names) ---
if 'db' not in st.session_state:
    st.session_state.db = {
        "users": [
            {"UserID": "USR001", "Name": "Admin", "Role": "Super Admin", "Email": "admin@university.edu"},
            {"UserID": "USR002", "Name": "Rohan", "Role": "Student", "Email": "rohan@student.edu", "CGPA": 8.2, "Skills": ["Python", "SQL"]}
        ],
        "Institution": [{"ID": "INST01", "Name": "University of Tech", "Dept": "CSE", "Batch": "2024"}],
        "Company": [{"ID": "COMP01", "Name": "Google", "Domain": "Cloud", "Tier": "Tier 1", "MoUStatus": "Active"}],
        "SkillTaxonomy": ["Python", "Java", "PostgreSQL", "Docker", "AWS", "Soft Skills"],
        "OpportunityPosting": [
            {"ID": "JOB01", "Title": "Backend Intern", "Company": "Google", "EligibilityRule": 7.5, "SkillsReq": ["Python", "PostgreSQL"]}
        ],
        "Application": [],
        "InternshipEnrollment": [
            {"ID": "INT101", "Student": "Rohan", "Company": "Google", "Status": "Active", "Credits": 4}
        ],
        "MilestoneLog": []
    }

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("SIH26044 | DECiphers")
menu = st.sidebar.selectbox("Navigate Modules", [
    "Module 1: IAM",
    "Module 2: Academia Management",
    "Module 3: Industry & Corporate",
    "Module 4: Skill Mapping Engine",
    "Module 5: Opportunity Management",
    "Module 6: Recruitment ATS",
    "Module 7: Internship Monitoring"
])

# --- 4. MODULE LOGIC ---

# MODULE 1: IAM
if menu == "Module 1: IAM":
    st.header("🔐 Identity & Access Management")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Profile Onboarding")
        with st.form("register_form"):
            name = st.text_input("Full Name")
            role = st.selectbox("Role", ["Student", "Faculty/TPO", "Industry Recruiter", "College Admin"])
            email = st.text_input("Institutional Email")
            if st.form_submit_button("Register User"):
                new_user = {"UserID": f"USR{len(st.session_state.db['users'])+1}", "Name": name, "Role": role, "Email": email}
                st.session_state.db['users'].append(new_user)
                st.success("User Onboarded via JWT/OAuth Flow simulation.")
    with col2:
        st.subheader("Active User Directory")
        st.dataframe(pd.DataFrame(st.session_state.db['users']))

# MODULE 2: ACADEMIA MANAGEMENT
elif menu == "Module 2: Academia Management":
    st.header("🏫 Academia Management Service")
    st.subheader("Institutional Hierarchy")
    st.write("Hierarchy: Institution → Department → Program → Batch")
    st.table(st.session_state.db['Institution'])
    
    with st.expander("Academic Verification (Bulk Import)"):
        st.file_uploader("Upload Student AcademicRecords (CSV/Excel)")
        if st.button("Run Prerequisite Checks"):
            st.info("Verification Engine: CGPA and Backlog status verified for 2024 Batch.")

# MODULE 3: INDUSTRY & CORPORATE
elif menu == "Module 3: Industry & Corporate":
    st.header("🏢 Industry & Corporate Profile Service")
    with st.form("company_onboarding"):
        c_name = st.text_input("Company Name")
        domain = st.text_input("Industry Domain")
        tier = st.selectbox("Tier", ["Tier 1", "Tier 2", "Tier 3"])
        mou = st.selectbox("MoU Status", ["Active", "Pending"])
        if st.form_submit_button("Onboard Enterprise"):
            st.session_state.db['Company'].append({"ID": f"COMP{len(st.session_state.db['Company'])+1}", "Name": c_name, "Domain": domain, "Tier": tier, "MoUStatus": mou})
            st.rerun()
    st.subheader("Recruiter Team & Agreements")
    st.table(st.session_state.db['Company'])

# MODULE 4: SKILL MAPPING ENGINE
elif menu == "Module 4: Skill Mapping Engine":
    st.header("🧠 Skill Taxonomy & Mapping Engine")
    student_sel = st.selectbox("Select Student Profile", [u['Name'] for u in st.session_state.db['users'] if u['Role'] == 'Student'])
    
    # Skill Gap Analysis Logic
    st.subheader("Skill Gap Report")
    st.write(f"Analyzing {student_sel}'s verified skills against Industry Demand...")
    
    col1, col2 = st.columns(2)
    col1.metric("Syllabus Skill Extraction", "Verified")
    col2.metric("Compatibility Score", "72%")
    
    st.warning("Gap Identified: Student missing 'PostgreSQL' and 'Docker' as per Tier 1 benchmarks.")
    st.info("Recommendation: Suggested Micro-credential - 'Advanced RDBMS Implementation'")

# MODULE 5: OPPORTUNITY MANAGEMENT
elif menu == "Module 5: Opportunity Management":
    st.header("💼 Opportunity Management (Placements)")
    with st.form("post_job"):
        title = st.text_input("Opening Title")
        company_name = st.selectbox("Company", [c['Name'] for c in st.session_state.db['Company']])
        min_cgpa = st.number_input("Eligibility: Min CGPA", 0.0, 10.0, 7.0)
        req_skills = st.multiselect("Required Skills", st.session_state.db['SkillTaxonomy'])
        if st.form_submit_button("Post Opportunity"):
            st.session_state.db['OpportunityPosting'].append({
                "ID": f"JOB{len(st.session_state.db['OpportunityPosting'])+1}",
                "Title": title, "Company": company_name, "EligibilityRule": min_cgpa, "SkillsReq": req_skills
            })
    st.subheader("Live Opportunities")
    st.table(st.session_state.db['OpportunityPosting'])

# MODULE 6: RECRUITMENT ATS
elif menu == "Module 6: Recruitment ATS":
    st.header("📑 Recruitment & Application Workflow (ATS)")
    for job in st.session_state.db['OpportunityPosting']:
        st.write(f"### Pipeline for {job['Title']} ({job['Company']})")
        col1, col2 = st.columns([3,1])
        col1.write(f"Eligibility: CGPA >= {job['EligibilityRule']}")
        if col2.button(f"Apply for {job['ID']}"):
            st.session_state.db['Application'].append({
                "AppID": f"APP{len(st.session_state.db['Application'])+1}",
                "Job": job['Title'], "Student": "Rohan", "Stage": "Applied"
            })
            st.success("Application Submitted successfully!")

    st.subheader("Hiring Pipeline Status")
    if st.session_state.db['Application']:
        st.table(st.session_state.db['Application'])
    else:
        st.write("No active applications.")

# MODULE 7: INTERNSHIP MONITORING
elif menu == "Module 7: Internship Monitoring":
    st.header("📅 Internship Monitoring & Credit Evaluation")
    st.subheader("Active Enrollment Tracking")
    st.table(st.session_state.db['InternshipEnrollment'])
    
    with st.form("milestone_submission"):
        st.subheader("Weekly Milestone Logbook")
        st_name = st.selectbox("Student", [u['Name'] for u in st.session_state.db['users'] if u['Role'] == 'Student'])
        log_desc = st.text_area("Milestone Description")
        rating = st.slider("Industry Mentor Rating (1-5)", 1, 5, 3)
        if st.form_submit_button("Submit to Faculty Supervisor"):
            log_entry = {"Date": str(date.today()), "Student": st_name, "Log": log_desc, "MentorRating": rating}
            st.session_state.db['MilestoneLog'].append(log_entry)
            st.success("Log submitted. Pending Faculty approval for Credit Transfer.")
    
    if st.session_state.db['MilestoneLog']:
        st.write("Recent Submissions")
        st.table(st.session_state.db['MilestoneLog'])

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("System Entities: Institution, RecruiterTeam, SkillGapReport, OpportunityPosting, MilestoneLog")
