from flask import Blueprint, request, jsonify
from api.routes.auth import login_required
from api.schemas.recipe import recipe_create_schema
from api.extensions import db
from marshmallow import ValidationError
from api.models.recipe import Recipe

recipe_bp = Blueprint("recipe", __name__)


# Feed - Algo based on follows and preferences
@recipe_bp.route("/feed", methods=["GET"])
def recipe_feed():
    return "TODO"


# Search - Based on keywords in title and description
@recipe_bp.route("/search", methods=["GET"])
def recipe_search():
    query = request.args.get("q", "").strip().replace(" ", " & ")
    if not query:
        return jsonify({"error": "q parameter is required"}), 400
    return "TODO"


# Create Recipe
@recipe_bp.route("/", methods=["POST"])
@login_required()
def recipe_create():
    recipe_data = request.get_json()

    try:
        recipe: Recipe = recipe_create_schema.load(recipe_data)
    except ValidationError as error:
        return jsonify({"error": error.messages}), 400

    db.session.add(recipe)
    db.session.commit()

    return recipe_create_schema.jsonify(recipe)


# Modify Recipe
@recipe_bp.route("/<id>", methods=["PUT"])
@login_required()
def recipe_modify(id):
    return "TODO"


# Delete Recipe
@recipe_bp.route("/<id>", methods=["DELETE"])
@login_required(id)
def recipe_delete():
    return "TODO"


# Like Recipe
@recipe_bp.route("/<id>/like", methods=["POST"])
@login_required()
def recipe_like(id):
    return "TODO"


# Comment Recipe
@recipe_bp.route("/<id>/comment", methods=["POST"])
@login_required()
def recipe_comment(id):
    return "TODO"
