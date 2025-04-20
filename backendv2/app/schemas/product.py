from typing import Optional
from pydantic import BaseModel
from app.models import ProductCategory


class ProductInfo(BaseModel):
    id: int
    name: str
    category: ProductCategory

    energy: float
    proteins: float
    sugars: float
    saturated_fat: float
    salt: float
    fruits_veg: float
    fibers: float

    source: str
    barcode: Optional[str] = None

    class Config:
        from_attributes = True