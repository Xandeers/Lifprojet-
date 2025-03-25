from flask import Blueprint, jsonify, request
from api.extensions import db
from api.models.product_natural import ProductNatural

product_natural_bp = Blueprint("product_natural", __name__)

#Récupérer tous les produits naturels
@product_natural_bp.route("/products_natural", methods=["GET"])
def get_all_products():
    products = ProductNatural.query.all()
    
    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "image": product.image,
            "information": product.information,
            "energy": product.energy,
            "fat": product.fat,
            "saturated_fat": product.saturated_fat,
            "carbohydrates": product.carbohydrates,
            "sugars": product.sugars,
            "fiber": product.fiber,
            "proteins": product.proteins,
            "salt": product.salt,
            "sodium": product.sodium,
            "fruits_vegetables_nuts_estimate": product.fruits_vegetables_nuts_estimate,
            "nutriscore": product.nutriscore,
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat(),
        }
        for product in products
    ])

#Récupérer un produit par ID
@product_natural_bp.route("/products_natural/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    product = ProductNatural.query.get(product_id)
    
    if not product:
        return jsonify({"error": "Produit non trouvé"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "image": product.image,
        "information": product.information,
        "energy": product.energy,
        "fat": product.fat,
        "saturated_fat": product.saturated_fat,
        "carbohydrates": product.carbohydrates,
        "sugars": product.sugars,
        "fiber": product.fiber,
        "proteins": product.proteins,
        "salt": product.salt,
        "sodium": product.sodium,
        "fruits_vegetables_nuts_estimate": product.fruits_vegetables_nuts_estimate,
        "nutriscore": product.nutriscore,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
    })

#Ajouter un nouveau produit naturel
@product_natural_bp.route("/products_natural", methods=["POST"])
def add_product():
    data = request.json

    if ProductNatural.is_product_taken(data["name"]):
        return jsonify({"error": "Ce produit existe déjà"}), 400

    new_product = ProductNatural(
        name=data["name"],
        image=data.get("image", ""),
        information=data.get("information", ""),
        energy=data["energy"],
        fat=data["fat"],
        saturated_fat=data["saturated_fat"],
        carbohydrates=data["carbohydrates"],
        sugars=data["sugars"],
        fiber=data.get("fiber", 0),
        proteins=data["proteins"],
        salt=data.get("salt", 0),
        sodium=data.get("sodium", 0),
        fruits_vegetables_nuts_estimate=data.get("fruits_vegetables_nuts_estimate", 0),
        nutriscore=data.get("nutriscore", ""),
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Produit ajouté avec succès", "id": new_product.id}), 201

#Supprimer un produit par ID
@product_natural_bp.route("/products_natural/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = ProductNatural.query.get(product_id)

    if not product:
        return jsonify({"error": "Produit non trouvé"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Produit supprimé avec succès"}), 200

from flask import Blueprint, jsonify, request
from api.extensions import db
from api.models.product_natural import ProductNatural

product_natural_bp = Blueprint("product_natural", __name__)

# ✅ 1. Récupérer tous les produits naturels
@product_natural_bp.route("/products_natural", methods=["GET"])
def get_all_products():
    products = ProductNatural.query.all()
    
    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "image": product.image,
            "information": product.information,
            "energy": product.energy,
            "fat": product.fat,
            "saturated_fat": product.saturated_fat,
            "carbohydrates": product.carbohydrates,
            "sugars": product.sugars,
            "fiber": product.fiber,
            "proteins": product.proteins,
            "salt": product.salt,
            "sodium": product.sodium,
            "fruits_vegetables_nuts_estimate": product.fruits_vegetables_nuts_estimate,
            "nutriscore": product.nutriscore,
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat(),
        }
        for product in products
    ])

# ✅ 2. Récupérer un produit par ID
@product_natural_bp.route("/products_natural/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    product = ProductNatural.query.get(product_id)
    
    if not product:
        return jsonify({"error": "Produit non trouvé"}), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "image": product.image,
        "information": product.information,
        "energy": product.energy,
        "fat": product.fat,
        "saturated_fat": product.saturated_fat,
        "carbohydrates": product.carbohydrates,
        "sugars": product.sugars,
        "fiber": product.fiber,
        "proteins": product.proteins,
        "salt": product.salt,
        "sodium": product.sodium,
        "fruits_vegetables_nuts_estimate": product.fruits_vegetables_nuts_estimate,
        "nutriscore": product.nutriscore,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
    })

# ✅ 3. Ajouter un nouveau produit naturel
@product_natural_bp.route("/products_natural", methods=["POST"])
def add_product():
    data = request.json

    if ProductNatural.is_product_taken(data["name"]):
        return jsonify({"error": "Ce produit existe déjà"}), 400

    new_product = ProductNatural(
        name=data["name"],
        image=data.get("image", ""),
        information=data.get("information", ""),
        energy=data["energy"],
        fat=data["fat"],
        saturated_fat=data["saturated_fat"],
        carbohydrates=data["carbohydrates"],
        sugars=data["sugars"],
        fiber=data.get("fiber", 0),
        proteins=data["proteins"],
        salt=data.get("salt", 0),
        sodium=data.get("sodium", 0),
        fruits_vegetables_nuts_estimate=data.get("fruits_vegetables_nuts_estimate", 0),
        nutriscore=data.get("nutriscore", ""),
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Produit ajouté avec succès", "id": new_product.id}), 201

#Supprimer un produit par ID
@product_natural_bp.route("/products_natural/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = ProductNatural.query.get(product_id)

    if not product:
        return jsonify({"error": "Produit non trouvé"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Produit supprimé avec succès"}), 200
