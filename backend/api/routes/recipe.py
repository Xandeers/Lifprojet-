from flask import Blueprint

recipe_bp = Blueprint("recipe", __name__)


# Recipe Feed - Algo based on follows and preferences
@recipe_bp.route("/feed", methods=["GET"])
def recipe_feed():
    return "TODO"
