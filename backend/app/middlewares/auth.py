
from fastapi import Request, HTTPException
from app.utils.session import verify_session_token


async def auth_middleware(request: Request, call_next):
    session_token = request.cookies.get("session_id")
    request.state.user_id = None

    if session_token:
        try:
            user_id = verify_session_token(session_token)
            request.state.user_id = user_id
        except HTTPException:
            request.state.user = None


    response = await call_next(request)
    return response
