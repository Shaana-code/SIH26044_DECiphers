import sqlite3
import uuid
from datetime import datetime
import bcrypt

def hash_password(password: str) -> str:
    """Hashes a password using native bcrypt (safe for bcrypt 4.x+)."""
    # bcrypt requires bytes and has a 72-byte limit
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def seed_database():
    print("⏳ Creating tables and seeding 'portal.db'...")

    # Connect to SQLite (creates portal.db automatically in root folder)
    conn = sqlite3.connect("portal.db")
    cursor = conn.cursor()

    # 1. Create Users Table (Module 1: IAM)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        is_verified INTEGER DEFAULT 1,
        institution_id TEXT,
        company_id TEXT,
        created_at TEXT,
        updated_at TEXT
    );
    """)

    # 2. Pre-hashed Sample Accounts for All Personas
    sample_users = [
        (
            str(uuid.uuid4()),
            "student@test.com",
            hash_password("Student@123"),
            "Aarav Sharma",
            "STUDENT",
            1, 1, None, None,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat()
        ),
        (
            str(uuid.uuid4()),
            "recruiter@company.com",
            hash_password("Recruiter@123"),
            "Priya Mehta",
            "RECRUITER",
            1, 1, None, None,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat()
        ),
        (
            str(uuid.uuid4()),
            "faculty@college.edu",
            hash_password("Faculty@123"),
            "Dr. Rajesh Rao",
            "FACULTY_TPO",
            1, 1, None, None,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat()
        ),
        (
            str(uuid.uuid4()),
            "admin@college.edu",
            hash_password("Admin@123"),
            "College Dean / Admin",
            "COLLEGE_ADMIN",
            1, 1, None, None,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat()
        ),
        (
            str(uuid.uuid4()),
            "superadmin@portal.gov",
            hash_password("Super@123"),
            "Super Administrator",
            "SUPER_ADMIN",
            1, 1, None, None,
            datetime.utcnow().isoformat(),
            datetime.utcnow().isoformat()
        )
    ]

    # 3. Insert into Database
    cursor.executemany("""
    INSERT OR IGNORE INTO users (
        id, email, hashed_password, full_name, role,
        is_active, is_verified, institution_id, company_id,
        created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, sample_users)

    conn.commit()
    conn.close()
    print("✅ 'portal.db' successfully created and seeded with sample accounts!")

if __name__ == "__main__":
    seed_database()