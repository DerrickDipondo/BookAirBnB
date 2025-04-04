from flask import request, jsonify
from app import app, db
from models import User, Listing
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(email=data['email'], is_host=data.get('is_host', False))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201

@app.route('api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in'})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

@app.route('/api/listings', methods=['GET'])
def get_listings():
    listings = Listing.query.all()
    return jsonify([{'id': l.id,
                    'title': l.title, 
                    'price': l.price, 
                    'location': l.location
                    } for l in listings])