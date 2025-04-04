from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# Enable CORS for React frontend
CORS(app)

from routes import *

if __name__ == '__main__':
    app.run(debug=True, port=5000)
