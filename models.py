import enum
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Enum, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Many-to-Many relationship table for Course Prerequisites
prerequisites = Table(
    'course_prerequisites',
    Base.metadata,
    Column('course_id', Integer, ForeignKey('courses.id'), primary_key=True),
    Column('prerequisite_id', Integer, ForeignKey('courses.id'), primary_key=True)
)

class Institution(Base):
    __tablename__ = 'institutions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    code = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    departments = relationship("Department", back_populates="institution", cascade="all, delete-orphan")

class Department(Base):
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    institution_id = Column(Integer, ForeignKey('institutions.id'), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    
    institution = relationship("Institution", back_populates="departments")
    programs = relationship("Program", back_populates="department", cascade="all, delete-orphan")
    courses = relationship("Course", back_populates="department", cascade="all, delete-orphan")

class Program(Base):
    __tablename__ = 'programs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    name = Column(String(255), nullable=False)  # e.g., Bachelor of Technology
    degree = Column(String(100), nullable=False) # e.g., B.Tech
    duration_years = Column(Integer, nullable=False)
    
    department = relationship("Department", back_populates="programs")
    curriculums = relationship("Curriculum", back_populates="program", cascade="all, delete-orphan")
    batches = relationship("Batch", back_populates="program", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    credits = Column(Integer, nullable=False)
    syllabus_metadata = Column(String, nullable=True) # JSON/Text format for syllabus details
    
    department = relationship("Department", back_populates="courses")
    
    # Self-referential relationship for course prerequisites
    req_prerequisites = relationship(
        'Course',
        secondary=prerequisites,
        primaryjoin=(prerequisites.c.course_id == id),
        secondaryjoin=(prerequisites.c.prerequisite_id == id),
        backref='required_for'
    )

class Curriculum(Base):
    __tablename__ = 'curriculums'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    academic_year = Column(String(20), nullable=False) # e.g., 2026-2027
    version = Column(String(20), nullable=False)
    
    program = relationship("Program", back_populates="curriculums")

class Batch(Base):
    __tablename__ = 'batches'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    name = Column(String(100), nullable=False) # e.g., Batch of 2026
    section = Column(String(10), nullable=False) # e.g., Section A
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    
    program = relationship("Program", back_populates="batches")
    academic_records = relationship("AcademicRecord", back_populates="batch", cascade="all, delete-orphan")

class GradeEnum(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F" # System backlog indicator

class AcademicRecord(Base):
    __tablename__ = 'academic_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False, index=True) # Maps to external User/Profile registry 
    batch_id = Column(Integer, ForeignKey('batches.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    grade = Column(Enum(GradeEnum), nullable=False)
    cgpa = Column(Float, nullable=False)
    attendance_percentage = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    batch = relationship("Batch", back_populates="academic_records")
    course = relationship("Course")
