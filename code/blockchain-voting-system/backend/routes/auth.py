from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_routes = Blueprint('auth', __name__)

ADMIN_KEY = "default_admin_key"

@auth_routes.route('/register', methods=['POST'])
def register():
    """
    Allows users to register. Role is restricted to 'voter' unless explicitly set as 'admin' 
    by someone who knows the default key.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'voter')
    key = data.get('key', '')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    if role == "admin" and key != ADMIN_KEY:
        return jsonify({'error': 'Error the admin key is incorrect'}), 400

    hashed_password = generate_password_hash(password)
    
    new_user = User(username=username, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password,password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({'access_token': access_token}), 200

