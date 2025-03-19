from flask import Blueprint, jsonify, session, request
from api.models.user import User
from api.schemas.user import user_schema, user_login_schema
from api.extensions import db
from functools import wraps
from marshmallow import ValidationError

auth_bp = Blueprint("auth", __name__)


# Authentication route decorator
def login_required(is_admin_required=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is connected
            if "user_id" not in session:
                return jsonify({"error": "Unauthorized access, need connection"}), 401
            # Check if user is admin (only if required)
            if is_admin_required:
                user = User.query.get(session["user_id"])
                if not user.is_admin:
                    return jsonify({"error": "Administrator rights required"}), 403
            return f(*args, **kwargs)

        return decorated_function

    return decorator


# Auth Routes
@auth_bp.route("/register", methods=["POST"])
def register():
    user_data = request.get_json()

    # Serialize data to validate them
    try:
        user: User = user_schema.load(user_data)
    except ValidationError as error:
        return jsonify({"error": error.messages}), 400

    # Check if username and email are already taken
    if User.is_username_taken(user_data["username"]):
        return jsonify({"error": "Username already taken"}), 400
    if User.is_email_taken(user_data["email"]):
        return jsonify({"error": "Email already taken"}), 400

    # Add password via hash setter
    user.password = user_data["password"]

    # Add to database
    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user), 201


# Login Route
@auth_bp.route("/login", methods=["POST"])
def login():
    # Serialize data to validate them
    try:
        validated_data = user_login_schema.load(request.get_json())
    except ValidationError as error:
        return jsonify({"error": error.messages}), 400

    # Search user
    user = User.query.filter_by(email=validated_data.get("email")).first()
    if user and user.check_password(validated_data.get("password")):
        # Login logic
        session["user_id"] = user.id
        return user_schema.jsonify(user), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/logout", methods=["DELETE"])
def logout():
    response = jsonify({"msg": "Logout successfully"})
    session.pop("user_id", None)
    return response, 200


@auth_bp.route("/me", methods=["GET"])
@login_required()
def me():
    user_id = session["user_id"]
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return user_schema.jsonify(user), 200
