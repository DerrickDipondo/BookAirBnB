from app import app, db
from models import User, Listing

with app.app_context():
    print("Tables:", db.Model.metadata.tables.keys())