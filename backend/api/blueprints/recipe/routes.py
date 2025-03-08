from flask import Blueprint, request, jsonify
from api import db
from .models import Recipe, recipe_schema, recipes_schema

recipe_bp = Blueprint("recipe", __name__)

# 🔹 Récupérer toutes les recettes
@recipe_bp.route("/", methods=["GET"])
def get_all_recipes():
    recipes = Recipe.query.all()
    return recipes_schema.jsonify(recipes)

# 🔹 Récupérer une recette par ID
@recipe_bp.route("/<int:id>", methods=["GET"])
def get_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404
    return recipe_schema.jsonify(recipe)

# 🔹 Ajouter une recette
@recipe_bp.route('/recipe', methods=['POST'])
def create_recipe():
    data = request.get_json()

    new_recipe = Recipe(
        title=data.get("title", ""),  # Par défaut, une chaîne vide
        tag=data.get("tag", ""),  # Tag par défaut vide
        content=data.get("content", ""),  # Contenu obligatoire
        likes=data.get("likes", 0),  # Nombre de likes, 0 par défaut
        is_public=data.get("is_public", True),  # Par défaut, la recette est publique
        nutriscore=data.get("nutriscore", "C")  # Nutriscore par défaut à "C"
    )

    # Ajouter et sauvegarder la recette en base de données
    db.session.add(new_recipe)
    db.session.commit()

    return recipe_schema.jsonify(new_recipe), 201

# 🔹 Modifier une recette
@recipe_bp.route("/<int:id>", methods=["PUT"])
def update_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404

    data = request.get_json()
    recipe.title = data["title"]
    recipe.tag = data.get("tag", recipe.tag)
    recipe.content = data["content"]
    recipe.nutriscore = data["nutriscore"]
    
    db.session.commit()
    return recipe_schema.jsonify(recipe)

# 🔹 Supprimer une recette
@recipe_bp.route("/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"message": "Recipe not found"}), 404

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully"})
