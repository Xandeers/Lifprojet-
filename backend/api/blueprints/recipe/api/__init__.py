from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config  # Importer la configuration

# 🔹 Initialisation des extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app():
    """Créer et configurer l'application Flask."""
    app = Flask(__name__)

    # 🔹 Charger la configuration depuis config.py
    app.config.from_object(Config)

    # 🔹 Initialiser les extensions avec Flask
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Activer CORS pour gérer les requêtes entre le back et le front

    # 🔹 Importer et enregistrer les routes (Blueprints)
    from api.routes import recipe_routes
    from auth.routes import auth_routes  # Routes d'authentification (si tu en as)

    app.register_blueprint(recipe_routes, url_prefix="/api/recipes")
    app.register_blueprint(auth_routes, url_prefix="/api/auth")

    # 🔹 Créer la base de données si elle n'existe pas encore
    with app.app_context():
        db.create_all()

    return app
