from flask import Blueprint, jsonify, request

auth_routes = Blueprint('auth', __name__)

# Mock user data
users = {
    'admin': {'password': 'admin123', 'role': 'admin'},
    'voter': {'password': 'voter123', 'role': 'voter'}
}

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)
    if user and user['password'] == password:
        return jsonify({'username': username, 'role': user['role']}), 200
    return jsonify({'error': 'Invalid credentials'}), 401
