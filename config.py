import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    database_url: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:aryanforreal,,@localhost:3306/student_management")
    secret_key: str = os.getenv("SECRET_KEY", "123")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()
