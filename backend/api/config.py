from dotenv import load_dotenv
from os import getenv

# Load environment variables from .env file
load_dotenv()


class Config:
    SECRET_KEY = getenv("SECRET_KEY")

    # SQLAlchemy ORM
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session Cookies (METTRE EN STRICT/LAX + SECURE EN PROD HTTPS)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    # SESSION_COOKIE_SAMESITE = 'Lax'
