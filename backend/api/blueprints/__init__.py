from flask import Flask
from .auth import auth_bp
from .product import product_bp
# from .recipe import recipe_bp

def register_blueprints(app: Flask):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(product_bp, url_prefix='/product')
    # app.register_blueprint(recipe_bp, url_prefix='/recipe')