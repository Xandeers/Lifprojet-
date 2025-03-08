from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

# Flask Extensions
cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()