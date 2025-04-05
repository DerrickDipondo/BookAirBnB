from flask import request, jsonify
from app import app, db
from models import User, Listing, Booking
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
def home():
    return "Welcome to BookAirBnB!"

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(email=data['email'], is_host=data.get('is_host', False))
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201

@app.route('/api/login', methods=['POST'])
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
    location = request.args.get('location', '')
    max_price = request.arg.get('max_price', type=float)
    query = Listing.query
    if location:
        query = query.filter(Listing.location.like(f'%{location}'))
    if max_price:
        query = query.filter(Listing.price <= max_price)
    listings = [{'id': l.id, 'title': l.title, 'price': l.price, 'location': l.location} for l in query.all()]
    return jsonify(listings)

@app.route('/api/listings', methods=['POST'])
@login_required
def create_listing():
    if not current_user.is_host:
        return jsonify({'message': 'Only hosts can create listings'}), 403
    data = request.get_json()
    try:
        listing = Listing(
            host_id=current_user.id,
            title=data['title'],
            price=float(data['price']),
            location=data['location']
        )
        db.session.add(listing)
        db.session.commit()
        return jsonify({'message': 'Listing created', 'id': listing.id}), 201
    except KeyError:
        return jsonify({'message': 'Missing required fields'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid price format'}), 400

@app.route('/api/listings/<int:listing_id>', methods=['GET'])
def get_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return jsonify({
        'id': listing.id,
        'title': listing.title,
        'price': listing.price,
        'location': listing.location,
        'host_id': listing.host_id
    })

@app.route('/api/book', methods=['POST'])
@login_required
def book_listing():
    data = request.get_json()
    try:
        listing = Listing.query.get_or_404(data['listing_id'])

        booking_date = data['date']

        # Basic check: ensure no overlapping booking
        existing_booking = Booking.query.filter_by(listing_id=listing.id, date=booking_date).first()
        if existing_booking:
            return jsonify({'message': 'Date already booked'}), 409
        booking = Booking(
            user_id=current_user.id,
            listing_id=listing.id,
            date=booking_date
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify({'message': 'Booking created', 'id': booking.id}), 201
    except KeyError:
        return jsonify({'message': 'Missing required fields'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid date format (use YYYY-MM-DD)'}), 400

@app.route('/api/bookings', methods=['GET'])
@login_required
def get_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': b.id,
        'listing_id': b.listing_id,
        'date': b.date.isoformat(),
        'title': Listing.query.get(b.listing_id).title
    } for b in bookings])


