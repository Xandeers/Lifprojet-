from api.extensions import db
from sqlalchemy import exists, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class ProductNatural(db.Model):

    __tablename__ = 'products_natural'

    # Fields
    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    image: Mapped[str]
    information: Mapped[str] = mapped_column(Text) # description qui peu contenir par exemple les alergene exemple arrachide etc ..
    #--------macro liste--------
    energy: Mapped[float]
    fat: Mapped[float] # matiere grasse
    saturated_fat: Mapped[float]
    carbohydrates: Mapped[float] # glucide
    sugars: Mapped[float]
    fiber: Mapped[float]
    proteins: Mapped[float]
    salt: Mapped[float]
    sodium: Mapped[float]
    fruits_vegetables_nuts_estimate: Mapped[float]
    #-------------------------
    nutriscore: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


    @classmethod
    def is_product_taken(cls, name):
        return db.session.query(exists().where(cls.name == name)).scalar()