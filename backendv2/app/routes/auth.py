from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserBase, UserLogin
from app.services.user import UserService
from app.utils.session import create_session_token, set_session_cookie, delete_session_cookie, get_current_user_id

router = APIRouter()


@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserBase:
    user_service = UserService(db)
    try:
        new_user = user_service.create_user(user_data)
        return new_user # type: ignore
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user_data: UserLogin, response: Response, db: Session = Depends(get_db)) -> UserBase:
    user_service = UserService(db)
    try:
        user = user_service.authenticate_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = create_session_token(user.id)
    set_session_cookie(response, token)

    return user # type: ignore

@router.delete("/logout")
async def logout(response: Response):
    delete_session_cookie(response)
    return HTTPException(status_code=204, detail="Logout successful")

@router.get("/me")
async def get_profile(current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)) -> UserBase:
    user_service = UserService(db)
    user = user_service.get_user_by_id(current_user_id)

    return user # type: ignore