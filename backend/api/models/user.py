from api.extensions import db
from sqlalchemy import exists, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.mutable import MutableDict
from bcrypt import checkpw, hashpw, gensalt
from datetime import datetime, timezone


# User Model
class User(db.Model):
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
    recipes = relationship("Recipe", back_populates="author")
    comments = relationship("Comment", back_populates="author")

    @property
    def password(self):
        raise AttributeError("password cannot be read directly")

    @password.setter
    def password(self, raw_password):
        self.password_hash = hashpw(raw_password.encode("utf-8"), gensalt()).decode(
            "utf-8"
        )

    def check_password(self, raw_password):
        return checkpw(raw_password.encode("utf-8"), self.password_hash.encode("utf-8"))

    @classmethod
    def is_username_taken(cls, username):
        return db.session.query(exists().where(cls.username == username)).scalar()

    @classmethod
    def is_email_taken(cls, email):
        return db.session.query(exists().where(cls.email == email)).scalar()

    @classmethod
    def is_user_admin(cls, user_id):
        user = cls.query.get(user_id)
        return user.is_admin if user else False
