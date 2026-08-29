# seed_db.py
import sqlite3
import uuid
import json
from datetime import datetime
import bcrypt

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def seed_all():
    print("⏳ Seeding 'portal.db' with editable profile fields...")
    conn = sqlite3.connect("portal.db")
    cur = conn.cursor()

    # 1. Users Table with Profile Columns
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        department TEXT,
        institution_or_company TEXT,
        cgpa REAL,
        attendance REAL,
        is_active INTEGER DEFAULT 1,
        is_verified INTEGER DEFAULT 1,
        created_at TEXT
    );
    """)

    sample_users = [
        ("usr-001", "student@test.com", hash_password("Student@123"), "Aarav Sharma", "STUDENT", "Computer Science Engineering", "Global Tech University", 8.5, 85.0, 1, 1, datetime.utcnow().isoformat()),
        ("usr-002", "recruiter@company.com", hash_password("Recruiter@123"), "Priya Mehta", "RECRUITER", "Engineering Hiring", "Nexus AI Systems", None, None, 1, 1, datetime.utcnow().isoformat()),
        ("usr-003", "faculty@college.edu", hash_password("Faculty@123"), "Dr. Rajesh Rao", "FACULTY_TPO", "Computer Science Engineering", "Global Tech University", None, None, 1, 1, datetime.utcnow().isoformat()),
        ("usr-004", "admin@college.edu", hash_password("Admin@123"), "University Dean", "COLLEGE_ADMIN", "Dean Academic Affairs", "Global Tech University", None, None, 1, 1, datetime.utcnow().isoformat())
    ]
    cur.executemany("INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", sample_users)

    # 2. Opportunities Table
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
    sample_jobs = [
        ("opp-101", "AI Systems Engineering Intern", "Nexus AI Systems", "INTERNSHIP", "$1,500 / month", "Python, FastAPI, PyTorch, Docker, Vector DBs", "CGPA >= 7.5 | No Active Backlogs", "OPEN", datetime.utcnow().isoformat()),
        ("opp-102", "Graduate Cloud & DevOps Engineer", "CloudScale Infrastructure", "FULL_TIME", "$85,000 / year", "AWS, Docker, Kubernetes, Linux, Terraform", "CGPA >= 7.0 | Attendance >= 75%", "OPEN", datetime.utcnow().isoformat())
    ]
    cur.executemany("INSERT OR REPLACE INTO opportunities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", sample_jobs)

    # 3. Applications Table
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

    # 4. Logbooks Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS internship_logbooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT NOT NULL,
        student_name TEXT NOT NULL,
        company_name TEXT NOT NULL,
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

    conn.commit()
    conn.close()
    print("✅ Database successfully seeded with editable profile support.")

if __name__ == "__main__":
    seed_all()
