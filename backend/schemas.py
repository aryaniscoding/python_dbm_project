from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_type: str
    user_id: int
    full_name: str

class StudentBase(BaseModel):
    full_name: str
    email: str
    roll_number: str
    semester: int
    department: str
    phone: Optional[str] = None

class StudentCreate(StudentBase):
    username: str
    password: str

class Student(StudentBase):
    student_id: int
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TeacherBase(BaseModel):
    full_name: str
    email: str
    department: str
    phone: Optional[str] = None

class TeacherCreate(TeacherBase):
    username: str
    password: str

class Teacher(TeacherBase):
    teacher_id: int
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    subject_code: str
    subject_name: str
    semester: int
    credits: int = 3
    max_marks: int = 100
    passing_marks: int = 40

class Subject(SubjectBase):
    subject_id: int
    
    class Config:
        from_attributes = True

class MarkUpdate(BaseModel):
    mark_id: Optional[int] = None
    student_id: int
    subject_id: int
    marks_obtained: Decimal
    academic_year: str = "2024-25"

class MarkResponse(BaseModel):
    mark_id: int
    student_id: int
    subject_id: int
    marks_obtained: Decimal
    academic_year: str
    exam_type: str
    student_name: str
    subject_name: str
    subject_code: str
    max_marks: int
    passing_marks: int
    
    class Config:
        from_attributes = True

class StudentResult(BaseModel):
    student_id: int
    student_name: str
    roll_number: str
    semester: int
    department: str
    subjects: List[MarkResponse]
    cgpa: float
    total_credits: int
    passed: bool
    
    class Config:
        from_attributes = True
