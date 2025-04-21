from http.client import HTTPException
from typing import Optional, Any, Type

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.password import check_password


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def is_username_taken(self, username: str) -> bool:
        return self.db.execute(select(User).where(User.username == username)).first() is not None

    def is_email_taken(self, email: str) -> bool:
        return self.db.execute(select(User).where(User.email == email)).first() is not None

    def is_user_admin(self, user_id: int) -> bool:
        user = self.db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        return user.is_admin if user else False

    def create_user(self, user_data: UserCreate) -> User:
        # check if username or email are already taken
        if self.is_username_taken(user_data.username):
            raise ValueError("Username taken")
        if self.is_email_taken(str(user_data.email)):
            raise ValueError("Email taken")

        user = User(
            username=user_data.username,
            email=str(user_data.email),
        )
        user.password = user_data.password

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate_user(self, user_data: UserLogin) -> Optional[User]:
        user = self.db.query(User).filter(User.email == user_data.email).first()
        if not user or not check_password(user_data.password, str(user.password_hash)):
            raise ValueError("Invalid credentials")

        return user

    def get_user_by_id(self, user_id: int) -> Type[User]:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise ValueError("Invalid User ID")
        return user
