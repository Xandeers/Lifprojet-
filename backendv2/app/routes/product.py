from fastapi import APIRouter
from typing import List

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductBase
from app.services.product import ProductService

router = APIRouter()


@router.get("/search")
async def search_by_text(query: str, db: Session = Depends(get_db)) -> List[ProductBase]:
    product_service = ProductService(db)
    results = product_service.search_products_fts(query)
    products = [ProductBase(**row) for row in results]
    return products