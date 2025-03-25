from api.extensions import db, ma
from api.models.product_naturel import ProductNatural

class ProductNaturalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductNatural
        load_instance = True
        sqla_session = db.session
        ordered = True
    
product_industrial_schema = ProductNaturalSchema()
products_industrial_schema = ProductNaturalSchema(many=True)