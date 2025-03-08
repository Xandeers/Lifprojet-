from flask import Flask
from api.config import Config
from api.extensions import db, migrate, ma, cors
from api.blueprints import register_blueprints
from api.errors import register_error_handlers

def create_app():
    # Creation of Flask Instance + add configuration
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialization of Flask Extensions
    cors.init_app(app, 
                  supports_credentials=True, 
                  origins=["http://127.0.0.1:5173", "http://localhost:5173"])
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # Register Blueprint
    register_blueprints(app)

    # Return Flask app instance
    return app