import uuid
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    COLLEGE_ADMIN = "COLLEGE_ADMIN"
    FACULTY_TPO = "FACULTY_TPO"
    STUDENT = "STUDENT"
    RECRUITER = "RECRUITER"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Multi-tenant associations
    institution_id = Column(UUID(as_uuid=True), nullable=True)  # For College Staff/Students
    company_id = Column(UUID(as_uuid=True), nullable=True)      # For Recruiters

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)