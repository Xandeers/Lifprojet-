from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, String, Integer, event
from datetime import datetime, timezone
from app.database import Base

def score_to_grade(score):
    if score <= -1:
        return "A"
    elif score <= 2:
        return "B"
    elif score <= 10:
        return "C"
    elif score <= 18:
        return "D"
    else:
        return "E"


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    slug: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(Text)
    thumbnail_url: Mapped[str] = mapped_column(nullable=True)
    instructions: Mapped[str] = mapped_column(Text)  # Markdown format
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    nutriscore: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )

    author = relationship("User", back_populates="recipes")
    ingredients = relationship("RecipeIngredient", back_populates="recipe")

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
        return score_to_grade(total_score)

    def update_nutriscore(self):
        self.nutriscore = self.calculate_nutriscore()


@event.listens_for(Recipe, "before_insert")
@event.listens_for(Recipe, "before_update")
def update_recipe_nutriscore(mapper, connection, target):
    target.update_nutriscore()


class RecipeIngredient(Base):
    __tablename__ = "recipes_ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[float]
    unit: Mapped[str]

    recipe = relationship("Recipe", back_populates="ingredients")
    product = relationship("Product")


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
