# Student Result Management System

Role-based Student Result Management with three access points:
- Admin: full control (manage students, teachers, subjects, assignments, and summary stats).
- Teacher: view all students for assigned subjects, inline marks entry/edit.
- Student: view own marks, CGPA, pass/fail.

FastAPI backend (MySQL + SQLAlchemy), Streamlit frontend, JWT auth, bcrypt_sha256 password hashing.

## Technologies Used

- FastAPI for API and OpenAPI/Swagger docs.[1]
- Uvicorn ASGI server for development and deployment runs.[2][1]
- SQLAlchemy (2.x) ORM with MySQL (PyMySQL driver).
- Streamlit for the Python-only UI (no HTML/CSS/React).
- Passlib with bcrypt_sha256 hashing (fixes bcrypt 72-byte limit by pre-hashing with HMAC-SHA256).[3]
- Python-JOSE for JWT.
- Pandas/Plotly for frontend data + visualization.

## Project Structure

```
python_dbms_project/
├── backend/
│   ├── __init__.py
│   ├── main.py               # FastAPI app
│   ├── database.py           # SQLAlchemy engine/session
│   ├── models.py             # ORM models
│   ├── schemas.py            # Pydantic models
│   ├── crud.py               # DB operations
│   ├── auth.py               # JWT + password hashing (bcrypt_sha256)
│   ├── auth_bearer.py        # JWT Bearer dependency
│   └── scripts/
│       └── reset_passwords.py  # optional helper to reset seeded passwords
├── frontend/
│   ├── app.py                # Streamlit entry
│   ├── admin_dashboard.py
│   ├── teacher_dashboard.py
│   └── student_dashboard.py
├── database/
│   ├── tables.sql            # schema + base seed
│   ├── student_seed.sql      # extra students
│   └── marks_seed.sql        # marks inserts
├── config.py
├── requirements.txt
├── .env                      # environment variables (create this)
└── README.md
```

## ER Diagram

Mermaid (for GitHub/Docs renderers):
```mermaid
erDiagram
    admins {
        int admin_id PK
        varchar username UK
        varchar password_hash
        varchar full_name
        varchar email UK
        timestamp created_at
    }

    teachers {
        int teacher_id PK
        varchar username UK
        varchar password_hash
        varchar full_name
        varchar email UK
        varchar phone
        varchar department
        timestamp created_at
    }

    students {
        int student_id PK
        varchar username UK
        varchar password_hash
        varchar full_name
        varchar email UK
        varchar phone
        varchar roll_number UK
        int semester
        varchar department
        timestamp created_at
    }

    subjects {
        int subject_id PK
        varchar subject_code UK
        varchar subject_name
        int semester
        int credits
        int max_marks
        int passing_marks
    }

    teacher_subjects {
        int assignment_id PK
        int teacher_id FK
        int subject_id FK
        varchar academic_year
        UNIQUE (teacher_id, subject_id, academic_year)
    }

    marks {
        int mark_id PK
        int student_id FK
        int subject_id FK
        decimal marks_obtained
        varchar academic_year
        enum exam_type
        int updated_by
        timestamp updated_at
        UNIQUE (student_id, subject_id, academic_year, exam_type)
    }

    teachers ||--o{ teacher_subjects : assigned_to
    subjects ||--o{ teacher_subjects : has
    students ||--o{ marks : receives
    subjects ||--o{ marks : evaluates
```

Key relationships:
- teacher_subjects is a many-to-many bridge between teachers and subjects (scoped by academic_year).
- marks is a many-to-many bridge between students and subjects, with attributes (score, year, exam type).

## Prerequisites

- Python 3.11+ (3.13 supported; ensure compatible dependency pins).
- MySQL 8.x running locally with a user/password that has DDL/DML permissions.
- PowerShell or Bash.

## Environment Variables

Create a .env file in the project root:
```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/student_management
SECRET_KEY=change-me-in-production
```

config.py reads these at runtime.

## Install Dependencies

- Create and activate a virtual environment.
- Install requirements with versions compatible with modern Python and Windows.

PowerShell:
```
python -m venv .venv
. .\.venv\Scripts\Activate.ps1

pip install -U pip setuptools wheel
pip install -r requirements.txt
```

Notes:
- To avoid Python 3.13 “TypingOnly” import errors in older SQLAlchemy, use a 2.0.x that supports 3.13 (your requirements file is already set appropriately).
- Streamlit runs the frontend; FastAPI runs the backend via Uvicorn.[2][1]

## Database Setup

1) Create schema and base seed
```
mysql -u root -p < database/tables.sql
```

2) Seed additional students (optional)
```
mysql -u root -p < database/student_seed.sql
```

3) Seed marks (optional)  
You can insert marks via:
- Admin UI (teacher assignment + data entry),
- Teacher inline editing (Streamlit),
- SQL files (e.g., database/marks_seed.sql).

## Password Hashing

- The app uses Passlib’s bcrypt_sha256 scheme, which first HMAC-SHA256 pre-hashes the password and then applies bcrypt to avoid bcrypt’s 72-byte input limit.[3]
- If you re-seed users, generate bcrypt_sha256 hashes and store them in password_hash.

Generate a hash for a plaintext (example: “secret”):
```
python -c "from passlib.context import CryptContext; print(CryptContext(schemes=['bcrypt_sha256']).hash('secret'))"
```
This yields a string prefixed with $bcrypt-sha256$; use it to update corresponding rows in admins/teachers/students.[3]

## Run the Backend

From the project root:
```
uvicorn backend.main:app --reload
```
- You can also run FastAPI apps as modules (module:object resolution).[4][1]
- FastAPI auto-generates interactive docs at the /docs route for the running server.[1]

Common alternatives:
- python -m backend.main (if main.py has an entrypoint).
- Programmatic Uvicorn run is also supported if you prefer code-based server startup.[2]

## Run the Frontend (Streamlit)

From the project root:
```
streamlit run frontend/app.py
```

- If you previously imported using “from frontend.something import …” and run into ModuleNotFoundError, either:
  - run from the project root so the parent is on sys.path, or[4]
  - change imports in frontend/app.py to sibling form:
    - from admin_dashboard import admin_dashboard
    - from teacher_dashboard import teacher_dashboard
    - from student_dashboard import student_dashboard

## Default Accounts (example)

Update these in your DB to known plaintexts if needed (using bcrypt_sha256 hashes):
- Admin: admin / secret
- Teacher: teacher1 / secret
- Student: student1 / secret

You can create users via Admin UI or via SQL inserts.

## API Endpoints (summary)

- POST /login?user_type=admin|teacher|student
- Admin
  - GET /admin/students, GET /admin/teachers, GET /admin/subjects
  - POST /admin/students, POST /admin/teachers, POST /admin/subjects
  - POST /admin/assign-teacher?teacher_id=..&subject_id=..
  - GET /admin/summary
- Teacher
  - GET /teacher/marks
  - POST /teacher/marks
- Student
  - GET /student/results

All protected routes require Authorization: Bearer <token>.

## Seeding Marks by Pattern

You can clone marks from “template” students (e.g., student_id 1/2/3) to all others using INSERT … SELECT with NOT EXISTS checks to avoid duplicates. MySQL supports INSERT … SELECT for copying data efficiently.[5][6]

## Troubleshooting

- Run Uvicorn properly:
  - uvicorn backend.main:app --reload starts the server using module:app semantics.[1]
  - Running as a package/module (python -m) can fix import path issues for absolute package imports (backend.*, frontend.*).[4][2]
- bcrypt vs passlib:
  - Use bcrypt_sha256 to avoid bcrypt input length limits.[3]
  - If you change schemes, re-hash and update all stored password_hash values; a new scheme won’t validate old hashes.
- SQLAlchemy on Python 3.13:
  - Ensure a 2.0.x version with Python 3.13 compatibility in requirements.
- Streamlit imports:
  - If “from frontend.*” fails, run streamlit from project root or use sibling imports (no package prefix).

## Development Tips

- Use /docs (OpenAPI UI) for quick testing of endpoints, including Authorization header testing.[1]
- For VS Code, set the workspace folder to the project root so launch/debug tasks run modules with the correct working directory.[7]
- Keep seed SQL files idempotent where possible (use INSERT IGNORE or ON DUPLICATE KEY UPDATE if desired).

## Security Notes

- JWTs are signed with SECRET_KEY; rotate in production.
- Use HTTPS and secure cookie/session handling if you expose through a web server.
- Enforce password policies; bcrypt_sha256 is robust and removes the 72-byte truncation risk inherent to bcrypt.[3]

## Running From Scratch (Checklist)

- Install MySQL, create a user and schema.
- Create venv, install requirements.
- Create .env with DATABASE_URL and SECRET_KEY.
- Apply database/tables.sql (and optional seeds).
- Start backend (Uvicorn).[1]
- Start frontend (Streamlit).
- Login with seeded users; Admin can create/assign; Teacher can enter marks inline; Student can view results and CGPA.

References (operations and concepts):
- Run Uvicorn/FastAPI server and patterns for module:app execution.[2][1]
- Running as a module from other files and import path behavior.[4]
- FastAPI interactive docs are available at /docs on the running app.[1]
- Passlib bcrypt_sha256 pre-hashes with HMAC-SHA256 to remove bcrypt’s 72-byte limit and is identified by $bcrypt-sha256$.[3]

