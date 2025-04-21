from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.database import Base
from app.utils.password import hash_password


class User(Base):
    __tablename__ = "users"

    # Fields
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False)
    bio: Mapped[str] = mapped_column(String(150), nullable=True)
    preferences: Mapped[dict] = mapped_column(
        MutableDict.as_mutable(JSONB), default=dict, nullable=True
    )
    avatar: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    # Relationship
    recipes = relationship("Recipe", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    # Password methods
    @property
    def password(self) -> str:
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, raw_password: str) -> None:
        self.password_hash = hash_password(raw_password)