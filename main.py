from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Institution, Department, Program, Course, Batch
from services import AcademicVerificationService, IngestionWorkerQueue

def setup_demo_data(session):
    inst = Institution(name="Global Tech University", code="GTU")
    session.add(inst)
    session.flush()

    dept = Department(institution_id=inst.id, name="Computer Science Engineering", code="CSE")
    session.add(dept)
    session.flush()

    prog = Program(department_id=dept.id, name="Bachelor of Technology", degree="B.Tech", duration_years=4)
    session.add(prog)
    session.flush()

    # Create sequence paths (Math -> Data Structures -> Algorithms)
    math1 = Course(department_id=dept.id, code="CS101", title="Discrete Mathematics", credits=4)
    ds = Course(department_id=dept.id, code="CS201", title="Data Structures", credits=4)
    algo = Course(department_id=dept.id, code="CS301", title="Algorithms", credits=4)
    
    ds.req_prerequisites.append(math1)
    algo.req_prerequisites.append(ds)
    session.add_all([math1, ds, algo])
    session.flush()

    batch = Batch(program_id=prog.id, name="Batch of 2028", section="A", start_year=2024, end_year=2028)
    session.add(batch)
    session.flush()
    return batch, math1, ds, algo

def run_pipeline():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("--- Initializing Mock University Framework ---")
    batch, math1, ds, algo = setup_demo_data(session)
    
    print("\n--- Processing Worker Queue Data Ingestion ---")
    csv_mock_payload = (
        "student_id,batch_id,course_id,grade,cgpa,attendance_percentage\n"
        f"1001,{batch.id},{math1.id},A,9.0,85.0\n"
        f"1001,{batch.id},{ds.id},B,8.0,78.5\n"
        f"1002,{batch.id},{math1.id},F,4.0,60.0\n" 
    )
    
    worker = IngestionWorkerQueue(session)
    ingestion_result = worker.process_csv_import(csv_mock_payload)
    print(f"Ingestion Finished: {ingestion_result}")

    print("\n--- Running Academic Verification Engines ---")
    verifier = AcademicVerificationService()
    
    for s_id in [1001, 1002]:
        print(f"\nStudent Evaluation [ID: {s_id}]:")
        print(f" - Cumulative CGPA: {verifier.calculate_cgpa(session, s_id)}")
        print(f" - Active Backlogs: {verifier.count_backlogs(session, s_id)}")
        print(f" - Safe Attendance (>75%): {verifier.verify_attendance(session, s_id)}")
        print(f" - Prerequisite Passed (Algo Course): {verifier.verify_prerequisites(session, s_id, algo.id)}")

if __name__ == "__main__":
    run_pipeline()

