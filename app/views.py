import os
import uuid
import random
import string
from app import app, db, bcrypt
from flask import send_from_directory, request, jsonify
from flask_login import login_user, logout_user, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, Booking, Country
from .services import AviationStackAPI

# ─── Static file serving ────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.static_folder, 'uploads'), filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

# Catch-all for Vue Router
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory(app.static_folder, 'index.html')


# ─── Auth ────────────────────────────────────────────────────────────────────

@app.route('/api/signup', methods=['POST'])
def register_user():
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    phoneNumber = request.form.get('phoneNumber')

    if not all([name, username, email, password, address, phoneNumber]):
        return jsonify({'error': 'All fields are required.'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists.'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(
        name=name,
        username=username,
        email=email,
        password=hashed_password,
        address=address,
        phoneNumber=phoneNumber,
        loyalty_points=0,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.', 'id': new_user.id}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            login_user(user)
            return jsonify({
                'message': 'Login successful',
                'token': access_token,
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'username': user.username,
                    'email': user.email,
                    'address': user.address,
                    'phoneNumber': user.phoneNumber,
                    'loyalty_points': user.loyalty_points or 0,
                }
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials.'}), 401

    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500


@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def handle_logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully.'}), 200


# ─── User / Profile ──────────────────────────────────────────────────────────

@app.route('/api/user', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    return jsonify({
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'address': user.address,
        'phoneNumber': user.phoneNumber,
        'loyalty_points': user.loyalty_points or 0,
    })


@app.route('/api/user', methods=['PUT'])
@jwt_required()
def update_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'phoneNumber' in data:
        user.phoneNumber = data['phoneNumber']
    if 'address' in data:
        user.address = data['address']

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully.'})


# ─── Flights ─────────────────────────────────────────────────────────────────

flight_cache = {}

@app.route('/api/flights', methods=['GET'])
def search_flights():
    origin = request.args.get('origin', '').strip().upper()
    destination = request.args.get('destination', '').strip().upper()
    date = request.args.get('date', '').strip()

    if not origin or not destination or not date:
        return jsonify({'error': 'origin, destination and date are required.'}), 400

    try:
        flights = AviationStackAPI.search_flights(origin, destination, date)
        for flight in flights:
            flight_id = str(uuid.uuid4())
            flight['id'] = flight_id
            flight_cache[flight_id] = flight
        return jsonify(flights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/flights/<flight_id>', methods=['GET'])
def flight_details(flight_id):
    flight = flight_cache.get(flight_id)
    if not flight:
        return jsonify({'error': 'Flight not found. Please search again.'}), 404
    flight['base_fare'] = flight['price']
    flight['taxes'] = int(flight['price'] * 0.15)
    flight['total'] = flight['price'] + flight['taxes']
    return jsonify(flight)


# ─── Bookings ────────────────────────────────────────────────────────────────

@app.route('/api/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404

    data = request.get_json()
    if not data.get('flight_id') or not data.get('total_price'):
        return jsonify({'error': 'flight_id and total_price are required.'}), 400

    booking_ref = f'JAGO-{str(uuid.uuid4())[:8].upper()}'

    booking = Booking(
        user_id=user_id,
        flight_data={'flight_id': data['flight_id']},
        passenger_name=user.name,
        email=user.email,
        phonenumber=user.phoneNumber,
        seat_preference=data.get('seat_preference'),
        special_requests=data.get('special_requests'),
        total_price=data['total_price'],
        booking_reference=booking_ref,
        status='pending',
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify({
        'booking_id': booking_ref,
        'booking_reference': booking_ref,
        'message': 'Booking created successfully.',
    }), 201


@app.route('/api/bookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    user_id = int(get_jwt_identity())
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
    return jsonify([b.to_dict() for b in bookings])


@app.route('/api/bookings/<booking_ref>', methods=['GET'])
@jwt_required()
def get_booking(booking_ref):
    user_id = int(get_jwt_identity())
    booking = Booking.query.filter_by(booking_reference=booking_ref).first()
    if not booking:
        return jsonify({'error': 'Booking not found.'}), 404
    if booking.user_id != user_id:
        return jsonify({'error': 'Unauthorized.'}), 403
    return jsonify(booking.to_dict())


@app.route('/api/bookings/<booking_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_booking(booking_id):
    user_id = int(get_jwt_identity())
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found.'}), 404
    if booking.user_id != user_id:
        return jsonify({'error': 'Unauthorized.'}), 403
    if booking.status == 'confirmed':
        return jsonify({'error': 'Cannot cancel a confirmed booking.'}), 400

    booking.status = 'cancelled'
    db.session.commit()
    return jsonify({'message': 'Booking cancelled successfully.'})


# ─── Mock Payment ─────────────────────────────────────────────────────────────

@app.route('/api/mock-payment', methods=['POST'])
@jwt_required()
def mock_payment():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    booking_id = data.get('booking_id')

    if not booking_id:
        return jsonify({'error': 'booking_id is required.'}), 400

    booking = Booking.query.filter_by(booking_reference=booking_id).first()
    if not booking:
        return jsonify({'error': 'Booking not found.'}), 404
    if booking.user_id != user_id:
        return jsonify({'error': 'Unauthorized.'}), 403

    booking.status = 'confirmed'

    # Award loyalty points — 1 point per JMD 100 spent
    user = User.query.get(user_id)
    points_earned = int(booking.total_price / 100)
    user.loyalty_points = (user.loyalty_points or 0) + points_earned

    db.session.commit()

    return jsonify({
        'message': 'Payment successful.',
        'booking_reference': booking.booking_reference,
        'points_earned': points_earned,
    })


# ─── Check-In ────────────────────────────────────────────────────────────────

@app.route('/api/checkin', methods=['POST'])
@jwt_required()
def check_in():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    booking_ref = data.get('booking_reference')

    if not booking_ref:
        return jsonify({'error': 'booking_reference is required.'}), 400

    booking = Booking.query.filter_by(booking_reference=booking_ref).first()
    if not booking:
        return jsonify({'error': 'Booking not found.'}), 404
    if booking.user_id != user_id:
        return jsonify({'error': 'Unauthorized.'}), 403
    if booking.status != 'confirmed':
        return jsonify({'error': 'Only confirmed bookings can be checked in.'}), 400
    if booking.checked_in:
        return jsonify({'error': 'Already checked in.', 'boarding_pass_code': booking.boarding_pass_code}), 400

    boarding_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    booking.checked_in = True
    booking.boarding_pass_code = boarding_code
    db.session.commit()

    return jsonify({
        'message': 'Check-in successful.',
        'boarding_pass_code': boarding_code,
        'booking_reference': booking_ref,
    })


# ─── Loyalty Points ───────────────────────────────────────────────────────────

@app.route('/api/loyalty-points', methods=['GET'])
@jwt_required()
def get_loyalty_points():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    return jsonify({
        'points': user.loyalty_points or 0,
        'equivalent_jmd': (user.loyalty_points or 0) * 100,
    })


# ─── Country Info ─────────────────────────────────────────────────────────────

@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    return jsonify([c.to_dict() for c in countries])


# ─── Error handlers ───────────────────────────────────────────────────────────

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response