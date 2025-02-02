from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args, parser
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from . import db
from .models import User, user_schema

main = Blueprint('main', __name__)

# Error parsing for bad request
@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    response = {
        'error': 'Validation Error',
        'message': err.messages
    }
    return jsonify(response), 400

# Auth Routes
@main.route('/register', methods=['POST'])
@use_args({
    'username': fields.Str(required=True),
    'email': fields.Str(required=True),
    'password': fields.Str(required=True),
}, location='json')
def register(args):
    # Check if user already exists
    username = args['username']
    email = args['email']

    if User.is_username_taken(username):
        return jsonify({"error": "Username already exists"}), 400
    if User.is_email_taken(email):
        return jsonify({"error": "Email already exists"}), 400
        
    # Create a new user
    new_user = User(username, email, args['password'])

    # Add to database
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

@main.route('/login', methods=['POST'])
@use_args({
    'email': fields.Str(required=True),
    'password': fields.Str(required=True)
}, location='json')
def login(args):
    email = args['email']
    password = args['password']

    # Search user
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id), fresh=True)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token
        }), 200
    else:
        return jsonify({
            'error': 'Invalid credentials'
        }), 401
    
@main.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({
            'message': 'User not found'
        }), 404
    
    return user_schema.jsonify(user)