from . import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

# User Model
class User(db.Model):
    __tablename__ = 'users'

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, password, is_admin=False):
        self.username = username
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin

    # Methods to verify if user already exists
    @classmethod
    def is_username_taken(cls, username):
        """Vérifie si un username est déjà pris"""
        return db.session.query(cls.id).filter_by(username=username).first() is not None

    @classmethod
    def is_email_taken(cls, email):
        """Vérifie si un email est déjà utilisé"""
        return db.session.query(cls.id).filter_by(email=email).first() is not None

    # Password methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# User Schema for serialization
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    is_admin = ma.auto_field()

user_schema = UserSchema()
users_schema = UserSchema(many=True)