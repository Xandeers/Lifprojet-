from slugify import slugify
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, String, Integer, event, UniqueConstraint
from datetime import datetime, timezone
from app.database import Base
import secrets
import string


class Recipe(Base):
    __tablename__ = "recipes"

    # Fields
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(Text)
    thumbnail_url: Mapped[str] = mapped_column(nullable=True)
    instructions: Mapped[str] = mapped_column(Text)  # Markdown format
    nutriscore: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Relationships
    author = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")
    likes = relationship("RecipeLike", backref="recipe", cascade="all, delete-orphan")

    def calculate_nutriscore(self):
        total_negative = 0
        total_positive = 0

        for ingredient in self.ingredients:
            product = ingredient.product
            quantity = ingredient.quantity

            if not product:
                continue

            # Conversion
            energy_kj_per_100g = product.energy * 4.184  # conversion kCal vers kJ
            energy = (energy_kj_per_100g / 100) * quantity
            sugars = (product.sugars / 100) * quantity
            saturated_fat = (product.saturated_fat / 100) * quantity
            salt = (product.salt / 100) * quantity
            fibers = (product.fibers / 100) * quantity
            proteins = (product.proteins / 100) * quantity
            fruits_veg = (product.fruits_veg / 100) * quantity

            # Nutriscore points
            negative_points = (
                energy / 335.0 + sugars / 4.5 + saturated_fat / 1.0 + salt / 0.09
            )
            positive_points = fibers / 0.9 + proteins / 1.6 + fruits_veg / 40.0

            total_negative += negative_points
            total_positive += positive_points

        total_score = total_negative - total_positive
        return total_score

    def update_nutriscore(self):
        self.nutriscore = self.calculate_nutriscore()


class RecipeIngredient(Base):
    __tablename__ = "recipes_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[float]
    unit: Mapped[str]

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    recipe = relationship("Recipe", back_populates="ingredients")
    product = relationship("Product")

    @classmethod
    def model_validate(cls, ingredient):
        pass

class RecipeLike(Base):
    __tablename__ = "recipe_likes"

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    __table_args__ = (
        UniqueConstraint("user_id", "recipe_id", name="unique_like"),
    )

class Comment(Base):
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


@event.listens_for(Recipe, "before_insert")
@event.listens_for(Recipe, "before_update")
def update_recipe_nutriscore(mapper, connection, target):
    target.update_nutriscore()

def generate_slug_suffix(length: int = 6) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@event.listens_for(Recipe, "before_insert")
def generate_slug(mapper, connection, target: Recipe):
    if not target.slug:
        slug = f"{slugify(target.title)}-{generate_slug_suffix()}"
        target.slug = slug