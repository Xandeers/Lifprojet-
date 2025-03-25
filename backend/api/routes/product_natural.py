from flask import Blueprint, jsonify, request
from api.extensions import db
from api.models.product_natural import ProductNatural

product_natural_bp = Blueprint("product_natural", __name__)

#2Récupérer tous les produits naturels
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

#3Récupérer un produit par ID
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

#4Ajouter un nouveau produit naturel
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

#5Supprimer un produit par ID
@product_natural_bp.route("/products_natural/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = ProductNatural.query.get(product_id)

    if not product:
        return jsonify({"error": "Produit non trouvé"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Produit supprimé avec succès"}), 200

#6. Rechercher des produits par mot-clé dans le nom
@product_natural_bp.route("/products_natural/search", methods=["GET"])
def search_products():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({"error": "Veuillez fournir un mot-clé pour la recherche."}), 400

    # Recherche insensible à la casse
    products = ProductNatural.query.filter(ProductNatural.name.ilike(f"%{query}%")).all()

    if not products:
        return jsonify({"message": "Aucun produit trouvé pour ce mot-clé."}), 404

    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "image": product.image,
            "information": product.information,
            "energy": product.energy,
            "proteins": product.proteins,
            "carbohydrates": product.carbohydrates,
            "fat": product.fat,
            "nutriscore": product.nutriscore
        }
        for product in products
    ])

# Classer les aliments selon un nutriment sera utile pour les recette et la creation de programme 

@product_natural_bp.route("/products_natural/sort", methods=["GET"])
def sort_products():
    nutrient = request.args.get("nutrient", "").strip()
    order = request.args.get("order", "desc").lower()  # "asc" ou "desc" (par défaut desc)

    # Liste des nutriments valides
    valid_nutrients = {
        "energy": ProductNatural.energy,
        "fat": ProductNatural.fat,
        "saturated_fat": ProductNatural.saturated_fat,
        "carbohydrates": ProductNatural.carbohydrates,
        "sugars": ProductNatural.sugars,
        "fiber": ProductNatural.fiber,
        "proteins": ProductNatural.proteins,
        "salt": ProductNatural.salt,
        "sodium": ProductNatural.sodium,
        "fruits_vegetables_nuts_estimate": ProductNatural.fruits_vegetables_nuts_estimate,
    }

    if nutrient not in valid_nutrients:
        return jsonify({"error": "Nutriment invalide. Choisissez parmi: " + ", ".join(valid_nutrients.keys())}), 400

    # Trier en fonction de l'ordre
    if order == "asc":
        products = ProductNatural.query.order_by(valid_nutrients[nutrient].asc()).all()
    else:
        products = ProductNatural.query.order_by(valid_nutrients[nutrient].desc()).all()

    if not products:
        return jsonify({"message": "Aucun produit trouvé."}), 404

    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "image": product.image,
            "information": product.information,
            nutrient: getattr(product, nutrient),  # Ajoute seulement la valeur du nutriment choisi
            "nutriscore": product.nutriscore
        }
        for product in products
    ])
