from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from backend import models, schemas, crud
from backend.database import get_db, engine
from backend.auth import create_access_token
from backend.auth_bearer import JWTBearer

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jwt_bearer = JWTBearer()

@app.post("/login", response_model=schemas.Token)
async def login(user_credentials: schemas.UserLogin, user_type: str, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_credentials.username, user_credentials.password, user_type)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    user_id_field = f"{user_type}_id"
    user_id = getattr(user, user_id_field)
    
    access_token = create_access_token(
        data={"sub": str(user_id), "user_type": user_type}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": user_type,
        "user_id": user_id,
        "full_name": user.full_name
    }

@app.get("/admin/students", response_model=List[schemas.Student])
async def get_students(current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.get_all_students(db)

@app.get("/admin/teachers", response_model=List[schemas.Teacher])
async def get_teachers(current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.get_all_teachers(db)

@app.get("/admin/subjects", response_model=List[schemas.Subject])
async def get_subjects(current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.get_all_subjects(db)

@app.post("/admin/students", response_model=schemas.Student)
async def create_student(student: schemas.StudentCreate, current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.create_student(db, student)

@app.post("/admin/teachers", response_model=schemas.Teacher)
async def create_teacher(teacher: schemas.TeacherCreate, current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.create_teacher(db, teacher)

@app.post("/admin/subjects", response_model=schemas.Subject)
async def create_subject(subject: schemas.SubjectBase, current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.create_subject(db, subject)

@app.post("/admin/assign-teacher")
async def assign_teacher_to_subject(teacher_id: int, subject_id: int, current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.assign_teacher_to_subject(db, teacher_id, subject_id)

@app.get("/admin/summary")
async def get_admin_summary(current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.get_admin_summary(db)

@app.get("/teacher/marks")
async def get_teacher_marks(current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "teacher":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.get_marks_for_teacher_subjects(db, int(current_user["sub"]))

@app.post("/teacher/marks")
async def update_teacher_marks(marks: List[schemas.MarkUpdate], current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "teacher":
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.update_marks(db, marks, int(current_user["sub"]))

@app.get("/student/results")
async def get_student_results(current_user: dict = Depends(jwt_bearer), db: Session = Depends(get_db)):
    if current_user["user_type"] != "student":
        raise HTTPException(status_code=403, detail="Access denied")
    result = crud.get_student_results(db, int(current_user["sub"]))
    if not result:
        raise HTTPException(status_code=404, detail="No results found")
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
