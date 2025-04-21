import os
from dotenv import load_dotenv
from itsdangerous import URLSafeSerializer, SignatureExpired, BadSignature
from fastapi import Request, Response, HTTPException
from datetime import timedelta

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
COOKIE_NAME = "session_id"
SESSION_COOKIE_LIFETIME = timedelta(days=1)

serializer = URLSafeSerializer(SECRET_KEY)

def create_session_token(user_id) -> str:
    return serializer.dumps(user_id)

def verify_session_token(cookie: str) -> int | None:
    try:
        user_id = serializer.loads(cookie, max_age=SESSION_COOKIE_LIFETIME.total_seconds())
        return user_id
    except SignatureExpired:
        raise HTTPException(status_code=401, detail="Session expired")
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid session")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid token")

def set_session_cookie(response: Response, session_token: str):
    response.set_cookie(
        key=COOKIE_NAME,
        value=session_token,
        httponly=True,
        max_age=int(SESSION_COOKIE_LIFETIME.total_seconds()),
        secure=False,
        samesite="lax",
        path="/"
    )

def delete_session_cookie(response: Response):
    response.delete_cookie(key="session_id")

def get_current_user_id(request: Request):
    user_id = request.state.user_id
    if user_id is None:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    return user_id