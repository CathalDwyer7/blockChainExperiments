from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Import extensions
from extensions import db, jwt

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure the database and JWT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_secret_key')

# Initialize extensions
db.init_app(app)
jwt.init_app(app)

# Import and register blueprints
from routes.auth import auth_routes
from routes.elections import election_routes

app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(election_routes, url_prefix='/api/elections')

if __name__ == '__main__':
    app.run(debug=True)

