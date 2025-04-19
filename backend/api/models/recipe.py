from api.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, String, Integer
from datetime import datetime, timezone


class Recipe(db.Model):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(Text)
    thumbnail_url: Mapped[str] = mapped_column(nullable=True)
    instructions: Mapped[str] = mapped_column(Text)  # Markdown format
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    author = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe")


class RecipeIngredient(db.Model):
    __tablename__ = "recipes_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[float]
    unit: Mapped[str]

    recipe = relationship("Recipe", back_populates="ingredients")
    product = relationship("Product")


class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500))
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("comments.id"), nullable=True
    )

    author = relationship("User", back_populates="comments")
    parent = relationship(
        "Comment", remote_side=lambda: [Comment.id], backref="children", lazy="joined"
    )
