from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')


# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Intialize Migrate with app & db
migrate = Migrate(app, db)

# Enable CORS for React frontend
CORS(app)

# Import models
from models import User, Listing, Booking
print("Using database:", app.config['SQLALCHEMY_DATABASE_URI'])

# Import routes
from routes import *


if __name__ == '__main__':
    app.run(debug=True, port=5000)
