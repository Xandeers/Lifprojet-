from api.extensions import db, ma
from api.models.recipe import Recipe, RecipeIngredient
from marshmallow import fields


class RecipeCreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Recipe
        load_instance = True
        sqla_session = db.session
        ordered = True
        exclude = ("id", "slug", "nutriscore", "created_at", "updated_at")

    ingredients = fields.List(
        fields.Nested(
            "RecipeIngredientSchema", only=["id", "product_id", "quantity", "unit"]
        )
    )


class RecipeIngredientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecipeIngredient
        load_instance = True
        sqla_session = db.session


recipe_create_schema = RecipeCreateSchema()
