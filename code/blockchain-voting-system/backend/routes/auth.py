from functools import wraps
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from models import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_routes = Blueprint("auth", __name__)

ADMIN_KEY = "default_admin_key"


@auth_routes.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    key = data.get("key", "")
    is_admin = False

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    if len(key) > 0:
        if key != ADMIN_KEY:
            return jsonify({"error": "Error the admin key is incorrect"}), 400
        else:
            is_admin = True

    hashed_password = generate_password_hash(password)

    new_user = User(username=username,password=hashed_password,is_admin=is_admin)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(
        identity={"id": user.id, "is_admin": user.is_admin}
    )
    return jsonify({"access_token": access_token}), 200


@auth_routes.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return (
        jsonify(logged_in_as=current_user),
        200,
    )  # {'logged_in_as': {'id': 1, 'is_admin': False}}


# usfull decorator
def admin_required(fn):
    """
    Custom decorator to check if the user is admin
    """

    @wraps(fn)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()

        if not current_user["is_admin"]:
            return jsonify({"error": "Unauthorized"}), 403

        return fn(*args, **kwargs)

    return decorated_function
