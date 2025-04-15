from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from extensions import db, jwt, login_manager

app = Flask(__name__)
app.config.from_pyfile('config.py')


# Initialize extensions
db.init_app(app)
jwt.init_app(app)
login_manager.init_app(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# Intialize Migrate
migrate = Migrate(app, db)


# Import models
from models import User, Listing, Booking
print("Using database:", app.config['SQLALCHEMY_DATABASE_URI'])

# Import routes
from routes import *


if __name__ == '__main__':
    app.run(debug=True, port=5000)


