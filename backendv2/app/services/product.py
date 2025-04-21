from sqlalchemy import text
from sqlalchemy.orm import Session


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def search_products_fts(self, query: str):
        sql = text("""
                   SELECT *,
                          ts_rank(search_field, websearch_to_tsquery('french', :query)) AS rank
                   FROM products
                   WHERE search_field @@ websearch_to_tsquery('french', :query)
                   ORDER BY rank DESC
                       LIMIT 15
                   """)
        return self.db.execute(sql, {"query": query}).mappings().all()