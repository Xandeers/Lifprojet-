from api.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum


class ProductCategory(str, Enum):
    drink = "drink"
    cheese = "cheese"
    fat = "fat"
    other = "other"


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    category: Mapped[ProductCategory] = mapped_column(
        Enum(ProductCategory)
    )  # 4 algos pour le Nutriscore selon catégorie: "drink", "cheese", "fat", "other"

    energy: Mapped[float]
    proteins: Mapped[float]
    sugars: Mapped[float]
    saturated_fat: Mapped[float]
    salt: Mapped[float]
    fruits_veg: Mapped[float]
    fibers: Mapped[float]

    source: Mapped[str] # "ciqual", "off"...
    barcode: Mapped[str] = mapped_column(nullable=True) # pour OFF seulement
