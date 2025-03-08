from api.extensions import db, ma
from marshmallow import fields, validate
from .models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        ordered = True
    
    email = fields.Str(required=True, validate=validate.Email(error="Invalid email format"))
    password = fields.Str(load_only=True, required=True)
    is_admin = fields.Bool(dump_only=True)

user_schema = UserSchema(exclude=['password_hash'])
users_schemas = UserSchema(exclude=['password_hash'], many=True)

class LoginSchema(ma.Schema):
    email = fields.Str(required=True, validate=validate.Email(error="Invalid email format"))
    password = fields.Str(required=True)

login_schema = LoginSchema()