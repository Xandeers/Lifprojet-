from api.extensions import db, ma
from api.models.product import ProductIndustrial


class ProductIndustrialSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductIndustrial
        load_instance = True
        sqla_session = db.session
        ordered = True


product_industrial_schema = ProductIndustrialSchema()
products_industrial_schema = ProductIndustrialSchema(many=True)
