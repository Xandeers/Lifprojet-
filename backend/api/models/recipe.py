from api.extensions import db
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Integer, Boolean, ForeignKey, String
from typing import List

class Recipe(db.Model):

    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    tag: Mapped[str] = mapped_column(String(100), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    likes: Mapped[int] = mapped_column(Integer, default=0)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    nutriscore: Mapped[str] = mapped_column(String(1), nullable=False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    # Relations
    author = relationship("User", back_populates="recipes")
    comments = relationship("Comment", back_populates="recipe", cascade="all, delete-orphan")

    def add_like(self):
        self.likes += 1
        db.session.commit()

    @classmethod
    def is_recipe_taken(cls, title: str) -> bool:
        return db.session.query(db.exists().where(cls.title == title)).scalar()

class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    recipe = relationship("Recipe", back_populates="comments")
    user = relationship("User")