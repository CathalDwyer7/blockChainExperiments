from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Import and register blueprints
from routes.auth import auth_routes
from routes.elections import election_routes

app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(election_routes, url_prefix='/api/elections')

# Root route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Blockchain Voting System API!"})

if __name__ == '__main__':
    app.run(debug=True)

