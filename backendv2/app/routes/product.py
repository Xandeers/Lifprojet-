from fastapi import APIRouter
from typing import List

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product
from app.schemas.product import ProductBase

router = APIRouter()


@router.get("/search")
async def search_by_text(query: str, db: Session = Depends(get_db)) -> List[ProductBase]:
    return db.query(Product).all() #type: ignore