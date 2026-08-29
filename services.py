import csv
import io
from typing import Dict, Any
from sqlalchemy.orm import Session
from models import Course, AcademicRecord, GradeEnum

class AcademicVerificationService:
    @staticmethod
    def calculate_cgpa(session: Session, student_id: int) -> float:
        """Calculates cumulative CGPA for a student based on valid course records."""
        records = session.query(AcademicRecord).filter(AcademicRecord.student_id == student_id).all()
        if not records:
            return 0.0
        total_cgpa = sum(record.cgpa for record in records)
        return round(total_cgpa / len(records), 2)

    @staticmethod
    def count_backlogs(session: Session, student_id: int) -> int:
        """Counts active system backlogs (Grade F)."""
        return session.query(AcademicRecord).filter(
            AcademicRecord.student_id == student_id,
            AcademicRecord.grade == GradeEnum.F
        ).count()

    @staticmethod
    def verify_prerequisites(session: Session, student_id: int, course_id: int) -> bool:
        """Confirms whether a student has historically cleared prerequisites for a specific course."""
        course = session.query(Course).filter(Course.id == course_id).first()
        if not course or not course.req_prerequisites:
            return True
            
        # Extract all courses cleared by student (Grade higher than F)
        cleared_courses = session.query(AcademicRecord.course_id).filter(
            AcademicRecord.student_id == student_id,
            AcademicRecord.grade != GradeEnum.F
        ).all()
        cleared_course_ids = {c_id[0] for c_id in cleared_courses}
        
        for prereq in course.req_prerequisites:
            if prereq.id not in cleared_course_ids:
                return False
        return True

    @staticmethod
    def verify_attendance(session: Session, student_id: int, min_required: float = 75.0) -> bool:
        """Flags out if student falls below minimum compliance limits inside any active course."""
        low_attendance_records = session.query(AcademicRecord).filter(
            AcademicRecord.student_id == student_id,
            AcademicRecord.attendance_percentage < min_required
        ).count()
        return low_attendance_records == 0

class IngestionWorkerQueue:
    """Mock background worker framework evaluating parsed bulk multi-row data payloads."""
    def __init__(self, db_session: Session):
        self.db = db_session

    def process_csv_import(self, csv_data: str) -> Dict[str, Any]:
        """Parses and safely appends batch structured record entities to DB."""
        reader = csv.DictReader(io.StringIO(csv_data))
        success_count = 0
        error_count = 0
        errors = []

        for row in reader:
            try:
                record = AcademicRecord(
                    student_id=int(row['student_id']),
                    batch_id=int(row['batch_id']),
                    course_id=int(row['course_id']),
                    grade=GradeEnum[row['grade'].upper()],
                    cgpa=float(row['cgpa']),
                    attendance_percentage=float(row['attendance_percentage'])
                )
                self.db.add(record)
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Row {success_count + error_count}: {str(e)}")
        
        self.db.commit()
        return {
            "status": "Completed",
            "processed": success_count + error_count,
            "success": success_count,
            "failed": error_count,
            "errors": errors
        }
