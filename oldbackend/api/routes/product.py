from flask import Blueprint, request, jsonify
from sqlalchemy import text
from api.extensions import db
from api.schemas.product import products_schema

product_bp = Blueprint("product", __name__)


@product_bp.route("/search", methods=["GET"])
def search_products():
    query = request.args.get("q", "").strip().replace(" ", " & ")
    if not query:
        return jsonify({"error": "q parameter is required"}), 400

    sql = text(
        """
        SELECT p.*
        FROM products p
        WHERE to_tsvector('french', p.name) @@ to_tsquery('french', :query)
        LIMIT 20
    """
    )

    results = db.session.execute(sql, {"query": query}).fetchall()
    products = [row[0] if isinstance(row, tuple) else row for row in results]

    return jsonify({"query": query, "products": products_schema.dump(products)})
