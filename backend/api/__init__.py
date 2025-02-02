from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv
from os import getenv
from werkzeug.exceptions import HTTPException

# Load environment variables from .env file
load_dotenv()

# Flask Extensions
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
cors = CORS()

def create_app():
    # Flask App Instance
    app = Flask(__name__)

    # Flask App Settings
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')

    # Initialization of Flask Extensions
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    cors.init_app(app)

    # Register Blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Return Flask app instance
    return app