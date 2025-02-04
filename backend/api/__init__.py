from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv

# Load environment variables from .env file
load_dotenv()

# Flask Extensions
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    # Flask App Instance
    app = Flask(__name__)

    # Flask App Settings
    app.secret_key = 'my-new-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # METTRE EN STRICT/LAX + SECURE EN PROD HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False
    # app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Initialization of Flask Extensions
    db.init_app(app)
    ma.init_app(app)
   
    # CORS
    CORS(app,
        supports_credentials=True,
        origins=["http://127.0.0.1:5173", "http://localhost:5173"]
    )

    # Register Blueprint
    from .blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Return Flask app instance
    return app