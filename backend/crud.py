from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from backend import models, schemas
from backend.auth import verify_password, get_password_hash
from typing import List, Optional
from decimal import Decimal

def authenticate_user(db: Session, username: str, password: str, user_type: str):
    if user_type == "admin":
        user = db.query(models.Admin).filter(models.Admin.username == username).first()
    elif user_type == "teacher":
        user = db.query(models.Teacher).filter(models.Teacher.username == username).first()
    elif user_type == "student":
        user = db.query(models.Student).filter(models.Student.username == username).first()
    else:
        return None
    
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_all_students(db: Session) -> List[models.Student]:
    return db.query(models.Student).all()

def get_all_teachers(db: Session) -> List[models.Teacher]:
    return db.query(models.Teacher).all()

def get_all_subjects(db: Session) -> List[models.Subject]:
    return db.query(models.Subject).all()

def create_student(db: Session, student: schemas.StudentCreate):
    hashed_password = get_password_hash(student.password)
    db_student = models.Student(
        username=student.username,
        password_hash=hashed_password,
        full_name=student.full_name,
        email=student.email,
        phone=student.phone,
        roll_number=student.roll_number,
        semester=student.semester,
        department=student.department
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def create_teacher(db: Session, teacher: schemas.TeacherCreate):
    hashed_password = get_password_hash(teacher.password)
    db_teacher = models.Teacher(
        username=teacher.username,
        password_hash=hashed_password,
        full_name=teacher.full_name,
        email=teacher.email,
        phone=teacher.phone,
        department=teacher.department
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

def create_subject(db: Session, subject: schemas.SubjectBase):
    db_subject = models.Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def assign_teacher_to_subject(db: Session, teacher_id: int, subject_id: int, academic_year: str = "2024-25"):
    assignment = models.TeacherSubject(
        teacher_id=teacher_id,
        subject_id=subject_id,
        academic_year=academic_year
    )
    db.add(assignment)
    db.commit()
    return assignment

def get_teacher_subjects(db: Session, teacher_id: int):
    return db.query(models.Subject).join(models.TeacherSubject).filter(
        models.TeacherSubject.teacher_id == teacher_id
    ).all()

def get_marks_for_teacher_subjects(db: Session, teacher_id: int):
    rows = db.query(
        models.Mark.mark_id,
        models.Mark.student_id,
        models.Mark.subject_id,
        models.Mark.marks_obtained,
        models.Mark.academic_year,
        models.Mark.exam_type,
        models.Student.full_name.label('student_name'),
        models.Subject.subject_name,
        models.Subject.subject_code,
        models.Subject.max_marks,
        models.Subject.passing_marks
    ).join(models.Student).join(models.Subject).join(models.TeacherSubject).filter(
        models.TeacherSubject.teacher_id == teacher_id
    ).all()
    
    # Convert Row objects to dictionaries
    return [dict(row._mapping) for row in rows]


def update_marks(db: Session, marks_updates: List[schemas.MarkUpdate], updated_by: int):
    for mark_update in marks_updates:
        existing_mark = db.query(models.Mark).filter(
            and_(
                models.Mark.student_id == mark_update.student_id,
                models.Mark.subject_id == mark_update.subject_id,
                models.Mark.academic_year == mark_update.academic_year
            )
        ).first()
        
        if existing_mark:
            existing_mark.marks_obtained = mark_update.marks_obtained
            existing_mark.updated_by = updated_by
        else:
            new_mark = models.Mark(
                student_id=mark_update.student_id,
                subject_id=mark_update.subject_id,
                marks_obtained=mark_update.marks_obtained,
                academic_year=mark_update.academic_year,
                updated_by=updated_by
            )
            db.add(new_mark)
    
    db.commit()
    return True

def get_student_results(db: Session, student_id: int):
    marks = db.query(
        models.Mark.marks_obtained,
        models.Subject.subject_name,
        models.Subject.subject_code,
        models.Subject.credits,
        models.Subject.max_marks,
        models.Subject.passing_marks
    ).join(models.Subject).filter(models.Mark.student_id == student_id).all()
    
    if not marks:
        return None
        
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    
    # Convert marks to dictionaries
    marks_dict = [dict(mark._mapping) for mark in marks]
    
    total_credits = sum(mark['credits'] for mark in marks_dict)
    total_grade_points = sum(
        (mark['marks_obtained'] / mark['max_marks'] * 10) * mark['credits'] 
        for mark in marks_dict
    )
    cgpa = total_grade_points / total_credits if total_credits > 0 else 0
    passed = all(mark['marks_obtained'] >= mark['passing_marks'] for mark in marks_dict)
    
    return {
        'student': student,  # This is an ORM instance, which FastAPI can serialize
        'marks': marks_dict,  # Now these are dictionaries
        'cgpa': round(cgpa, 2),
        'total_credits': total_credits,
        'passed': passed
    }
def get_admin_summary(db: Session):
    total_students = db.query(models.Student).count()
    total_teachers = db.query(models.Teacher).count()
    total_subjects = db.query(models.Subject).count()
    
    # Get pass/fail statistics
    passed_students = 0
    failed_students = 0
    
    students = db.query(models.Student).all()
    for student in students:
        result = get_student_results(db, student.student_id)
        if result:
            if result['passed']:
                passed_students += 1
            else:
                failed_students += 1
    
    return {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_subjects': total_subjects,
        'passed_students': passed_students,
        'failed_students': failed_students
    }
