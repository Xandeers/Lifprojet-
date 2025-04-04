from flask import Blueprint, request, jsonify
from api import db
from api.models.recipe import Recipe, Comment
from api.schemas.recipe import recipe_schema, recipes_schema, comment_schema, comments_schema

# Création du blueprint pour les routes liées aux recettes
recipe_bp = Blueprint("recipe", __name__)

# Récupérer toutes les recettes
@recipe_bp.route("/", methods=["GET"])
def get_all_recipes():
    recipes = Recipe.query.all()
    return recipes_schema.jsonify(recipes)

# Rechercher des recettes par mot-clé (dans le titre ou le tag)
@recipe_bp.route("/search", methods=["GET"])
def search_recipes():
    query = request.args.get("q", "").lower()
    results = Recipe.query.filter(
        (Recipe.title.ilike(f"%{query}%")) |
        (Recipe.tag.ilike(f"%{query}%"))
    ).all()
    return recipes_schema.jsonify(results)

# Récupérer une recette par son ID
@recipe_bp.route("/<int:id>", methods=["GET"])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return recipe_schema.jsonify(recipe)

# Créer une nouvelle recette
@recipe_bp.route("/", methods=["POST"])
def create_recipe():
    data = request.get_json()
    
    required_fields = ["title", "content", "nutriscore", "user_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    new_recipe = Recipe(
        title=data["title"],
        tag=data.get("tag", ""),
        content=data["content"],
        nutriscore=data["nutriscore"],
        user_id=data["user_id"],
        is_public=data.get("is_public", True)
    )

    db.session.add(new_recipe)
    db.session.commit()

    return recipe_schema.jsonify(new_recipe), 201

# Modifier une recette existante
@recipe_bp.route("/<int:id>", methods=["PUT"])
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    data = request.get_json()

    recipe.title = data.get("title", recipe.title)
    recipe.tag = data.get("tag", recipe.tag)
    recipe.content = data.get("content", recipe.content)
    recipe.nutriscore = data.get("nutriscore", recipe.nutriscore)
    recipe.is_public = data.get("is_public", recipe.is_public)

    db.session.commit()
    return recipe_schema.jsonify(recipe)

# Supprimer une recette
@recipe_bp.route("/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully"})

# Ajouter un like à une recette
@recipe_bp.route("/<int:id>/like", methods=["POST"])
def like_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    recipe.add_like()
    return jsonify({"message": "Like added", "likes": recipe.likes})

# Ajouter un commentaire à une recette
@recipe_bp.route("/<int:id>/comments", methods=["POST"])
def add_comment(id):
    recipe = Recipe.query.get_or_404(id)
    data = request.get_json()

    if "content" not in data or "user_id" not in data:
        return jsonify({"error": "Missing content or user_id"}), 400

    comment = Comment(
        content=data["content"],
        recipe_id=id,
        user_id=data["user_id"]
    )

    db.session.add(comment)
    db.session.commit()

    return comment_schema.jsonify(comment), 201

# Récupérer tous les commentaires d'une recette
@recipe_bp.route("/<int:id>/comments", methods=["GET"])
def get_comments(id):
    recipe = Recipe.query.get_or_404(id)
    return comments_schema.jsonify(recipe.comments)
