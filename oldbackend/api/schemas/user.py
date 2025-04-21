from api.extensions import db, ma
from marshmallow import fields, validate
from api.models.user import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        ordered = True
    
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(1, 20))
    email = fields.Str(required=True, validate=validate.Email(error="Invalid email format"))
    password = fields.Str(load_only=True, required=True)
    is_admin = fields.Bool(dump_only=True)

user_schema = UserSchema(exclude=['password_hash'])
users_schema = UserSchema(exclude=['password_hash'], many=True)

class UserLoginSchema(ma.Schema):
    email = fields.Str(required=True, validate=validate.Email(error="Invalid email format"))
    password = fields.Str(required=True)

user_login_schema = UserLoginSchema()