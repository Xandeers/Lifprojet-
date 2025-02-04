from flask import jsonify, session
from webargs import fields
from webargs.flaskparser import use_args
from . import auth_bp
from .models import User, user_schema
from api import db
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'msg': 'Unauthorized access, need connection'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

# Auth Routes
@auth_bp.route('/register', methods=['POST'])
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

# Login Route
@auth_bp.route('/login', methods=['POST'])
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
        # Login logic
        session['user_id'] = user.id 
        return user_schema.jsonify(user), 200
    else:
        return jsonify({
            'error': 'Invalid credentials'
        }), 401
    
@auth_bp.route('/logout', methods=["DELETE"])
def logout():
    response = jsonify({"msg": "Logout successful"})
    session.pop('user_id', None)
    return response, 200
    
@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'msg': 'User not found'
        }), 404
    return user_schema.jsonify(user), 200