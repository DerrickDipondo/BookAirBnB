from flask import request, jsonify
from app import app, db
from models import User, Listing, Booking, Review
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

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
    max_price = request.args.get('max_price', type=float)
    query = Listing.query
    if location:
        query = query.filter(Listing.location.like(f'%{location}%'))
    if max_price:
        query = query.filter(Listing.price <= max_price)
    listings = [{
        'id': l.id, 
        'title': l.title, 
        'price': l.price, 
        'location': l.location,
        'host_id': l.host_id
    } for l in query.all()]
    return jsonify(listings)

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
        return jsonify({'message': 'Invalid price format'}), 400@app.route('/api/listings/<int:listing_id>', methods=['GET'])


@app.route('/api/listings/<int:listing_id>', methods=['PUT'])
@login_required
def update_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.host_id != current_user.id:
        return jsonify({'message': 'You can only update your own listings'}), 403
    data = request.get_json()
    try:
        listing.title = data.get('title', listing.title)
        listing.price = float(data.get('price', listing.price))
        listing.location =data.get('location', listing.location)
        db.session.commit()
        return jsonify({'message': 'Listing updated'})
    except KeyError:
        return jsonify({'message': 'Invalid fields provided'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid price format'}), 400
    
@app.route('/api/listings/<int:listing_id>', methods=['DELETE'])
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    if listing.host_id != current_user.id:
        return jsonify({'message': 'You can only delete your own listings'}), 403
    # Check if there are active bookings
    if Booking.query.filter_by(listing_id=listing_id).first():
        return jsonify({'message': 'Cannot delete listing with active bookings'}), 409
    db.session.delete(listing)
    db.session.commit()
    return jsonify({'message': 'Listing deleted'})


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
    
@app.route('/api/book', methods=['POST'])
@login_required
def create_booking():
    data = request.get_json()
    try:
        listing = Listing.query.get_or_404(data['listing_id'])
        booking_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
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
        return jsonify({'message': 'Missing required fields(listing_id, date)'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid date format(use YYYY-MM-DD)'}), 400
    
@app.route('/api/bookings', methods=['GET'])
@login_required
def get_bookings():
    bookings = Booking.query.get_or_404(user_id=current_user.id).all()
    return jsonify([{
        'id': b.id,
        'listing_id': b.listing_id,
        'date': b.date.isoformat(),
        'title': Listing.query.get(b.listing_id).title
    } for b in bookings])

@app.route('/api/bookings/<int:booking_id>', methods=['[PUT]'])
@login_required
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        return jsonify({'message': 'You can only update your own bookings'}), 403
    data = request.get_json()
    try:
        new_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        existing_booking = Booking.query.filter(listing_id=booking.listing_id, date=new_date).first()
        if existing_booking and existing_booking.id != booking_id:
            return jsonify({'message': 'Date already booked'}), 409
        booking.date = new_date
        db.session.commit()
        return jsonify({'message': 'Booking updated'})
    except KeyError:
        return jsonify({'message': 'Missing date field'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid date format (use YYYY-MM-DD)'}), 400

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        return jsonify({'message': 'You can only delete your bookings'}), 403
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted'})

@app.route('/api/reviews', methods=['POST'])
@login_required
def create_review():
    data = request.get_json()
    try:
        booking = Booking.query.get_or_404(data['booking_id'])
        if booking.user_id != current_user.id:
            return jsonify({'message': 'You can only review your own bookings'}), 403
        if Review.query.filter_by(booking_id=booking.id).first():
            return jsonify({'message': 'Review already exists for this booking'}), 409
        review = Review(
            booking_id=booking.id,
            user_id=current_user.id,
            rating=int(data['rating']),
            comment=data.get('comment', '')
        )
        if not 1 <= review.rating <= 5:
            return jsonify({'message': 'Rating must be between 1 and 5'}), 400
        db.session.add(review)
        db.session.commit()
        return jsonify({'message': 'Review created', 'id': Review.id}), 201
    except KeyError:
        return jsonify({'message': 'Missing required fields(booking_id, rating)'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid rating format'}), 400
    
@app.route('/api/reviews/<int:listing_id>', methods=['GET'])
@login_required
def get_reviews(listing_id):
   Listing.query.get_or_404(listing_id) # Ensure listing exists
   reviews = Review.query.join(Booking).filter(Booking.listing_id == listing_id).all()
   return jsonify([{
       'id': r.id,
       'booking_id': r.booking_id,
       'user_id': r.user_id,
       'rating': r.rating,
       'comment': r.comment,
       'created_at': r.created_at.isoformat()
   } for r in reviews])

@app.route('/api/reviews/<int:review_id>', methods=['POST'])
@login_required
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        return jsonify({'message': 'You can only update your own reviews'}), 403
    data = request.get_json()
    try:
        review.rating = int(data.get('rating', review.rating))
        review.comment = data.get('comment', review.comment)
        if not 1 <= review.rating <= 5:
            return jsonify({'message': 'Rating must be between 1 and 5'}), 400
        db.session.commit()
        return jsonify({'message': 'Review updated'})
    except ValueError:
        return jsonify({'message': 'Invalid rating format'}), 400

@app.route('/api/review/<int:review_id>', methods=['DELETE'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        return jsonify({'message': 'You can only delete your reviews'}), 403
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'})


    




