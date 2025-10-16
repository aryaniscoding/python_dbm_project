from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Admin(Base):
    __tablename__ = "admins"
    
    admin_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Teacher(Base):
    __tablename__ = "teachers"
    
    teacher_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    department = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    subjects = relationship("TeacherSubject", back_populates="teacher")

class Student(Base):
    __tablename__ = "students"
    
    student_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    roll_number = Column(String(50), unique=True)
    semester = Column(Integer)
    department = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    marks = relationship("Mark", back_populates="student")

class Subject(Base):
    __tablename__ = "subjects"
    
    subject_id = Column(Integer, primary_key=True, index=True)
    subject_code = Column(String(20), unique=True)
    subject_name = Column(String(100))
    semester = Column(Integer)
    credits = Column(Integer, default=3)
    max_marks = Column(Integer, default=100)
    passing_marks = Column(Integer, default=40)
    
    teacher_assignments = relationship("TeacherSubject", back_populates="subject")
    marks = relationship("Mark", back_populates="subject")

class TeacherSubject(Base):
    __tablename__ = "teacher_subjects"
    
    assignment_id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"))
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"))
    academic_year = Column(String(20))
    
    teacher = relationship("Teacher", back_populates="subjects")
    subject = relationship("Subject", back_populates="teacher_assignments")

class Mark(Base):
    __tablename__ = "marks"
    
    mark_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.student_id"))
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"))
    marks_obtained = Column(DECIMAL(5,2), default=0)
    academic_year = Column(String(20))
    exam_type = Column(Enum('internal', 'external', 'practical'), default='external')
    updated_by = Column(Integer)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    student = relationship("Student", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")
