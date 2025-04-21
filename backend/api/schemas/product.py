from api.extensions import db, ma
from marshmallow import fields
from api.models import Product


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        sqla_session = db.session
        ordered = True

    id = fields.Int(dump_only=True)
    name = fields.Str()
    category = fields.Str()
    energy = fields.Float()
    proteins = fields.Float()
    sugars = fields.Float()
    saturated_fat = fields.Float()
    salt = fields.Float()
    fruits_veg = fields.Float()
    fibers = fields.Float()
    source = fields.Str()


products_schema = ProductSchema(many=True)
