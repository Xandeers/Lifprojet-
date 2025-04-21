from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    bio: Optional[str] = None
    avatar: Optional[str] = None
    preferences: Optional[dict] = None

    class Config:
        from_attributes = True


class UserPublicBase(BaseModel):
    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True