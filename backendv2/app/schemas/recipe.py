from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.product import ProductBase
from app.schemas.user import UserPublicBase


class RecipeIngredientBase(BaseModel):
    quantity: float
    unit: str
    product: ProductBase

    class Config:
        from_attributes = True

class RecipeIngredientAtCreate(BaseModel):
    id: int
    quantity: float
    unit: str = "g"

    class Config:
        from_attributes = True

class RecipeCreate(BaseModel):
    title: str
    description: str
    thumbnail_url: str
    instructions: str
    ingredients: List[RecipeIngredientAtCreate]

    class Config:
        from_attributes = True

class RecipeBase(RecipeCreate):
    id: int
    slug: str
    nutriscore: int
    ingredients: List[RecipeIngredientBase]
    author: UserPublicBase
    likes_count: int = 0
    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True

