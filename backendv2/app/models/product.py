from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum
from sqlalchemy import Enum
from app.database import Base

class ProductCategory(PyEnum):
    drink = "drink"
    cheese = "cheese"
    fat = "fat"
    other = "other"

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    category: Mapped[ProductCategory] = mapped_column(
        Enum(ProductCategory, name="product_category")
    )  # 4 algos pour le Nutriscore selon catégorie: "drink", "cheese", "fat", "other"

    energy: Mapped[float]
    proteins: Mapped[float]
    sugars: Mapped[float]
    saturated_fat: Mapped[float]
    salt: Mapped[float]
    fruits_veg: Mapped[float]
    fibers: Mapped[float]

    source: Mapped[str]  # "ciqual", "off"...
    barcode: Mapped[str] = mapped_column(nullable=True)  # pour OFF seulement
