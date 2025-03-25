from api.extensions import db
from sqlalchemy import exists, Text, Float, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

class ProductNatural(db.Model):
    __tablename__ = 'products_natural'

    # Clé primaire auto-incrémentée
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Infos générales
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    image: Mapped[str] = mapped_column(String(500), nullable=True)
    information: Mapped[str] = mapped_column(Text, nullable=True)  # Description et allergènes
    
    # Macros nutritionnelles
    energy: Mapped[float] = mapped_column(Float, nullable=False)
    fat: Mapped[float] = mapped_column(Float, nullable=False)  # Matières grasses
    saturated_fat: Mapped[float] = mapped_column(Float, nullable=False)
    carbohydrates: Mapped[float] = mapped_column(Float, nullable=False)  # Glucides
    sugars: Mapped[float] = mapped_column(Float, nullable=False)
    fiber: Mapped[float] = mapped_column(Float, nullable=True)
    proteins: Mapped[float] = mapped_column(Float, nullable=False)
    salt: Mapped[float] = mapped_column(Float, nullable=True)  # g / 100g
    sodium: Mapped[float] = mapped_column(Float, nullable=True)  # mg / 100g
    fruits_vegetables_nuts_estimate: Mapped[float] = mapped_column(Float, nullable=True)  # Estimation

    # Nutriscore et dates
    nutriscore: Mapped[str] = mapped_column(String(5), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Vérifier si un produit existe déjà
    @classmethod
    def is_product_taken(cls, name: str) -> bool:
        return db.session.query(exists().where(cls.name == name)).scalar()
    
    def __repr__(self):
        return f"<ProductNatural {self.name} ({self.energy} kcal)>"
