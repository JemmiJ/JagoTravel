"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db, bcrypt
from flask import render_template, send_from_directory, request, jsonify, send_file, session, Flask
import os
from .models import User, Booking
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .config import Config
from .services import AviationStackAPI
import uuid
import stripe

###
# Routing for your application.
###

# Ensure your app is configured with the upload folder

flight_cache = {}

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# for this I used form-data and not raw->json in postman
@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/assets/<path:filename>')
def assests(filename):
     return send_from_directory(os.path.join(app.static_folder, "assets"), filename)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    upload_dir = app.config['UPLOAD_FOLDER']
    print("🔍 CONFIGURED UPLOAD_FOLDER =", upload_dir)

    # Print out the parent directories to see where things actually are:
    def list_dir(path):
        try:
            return os.listdir(path)
        except Exception as e:
            return f"<error: {e}>"

    project_src = os.getcwd()
    app_dir     =  os.path.join(project_src, 'app')
    static_dir  = os.path.join(app_dir, 'static')

    print("📂 project/src contents:", list_dir(project_src))
    print("📂 app/ contents:",      list_dir(app_dir))
    print("📂 app/static contents:", list_dir(static_dir))
    print("📂 app/static/uploads contents:", list_dir(upload_dir))

    return send_from_directory(os.path.join(app.static_folder, "uploads"), filename)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/api/signup', methods=['POST'])
def register_user():
    # Get user form fields
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    phoneNumber = request.form.get('phoneNumber')

    # Check all required fields
    if not all([username, password, name, email, address, phoneNumber]):
        return jsonify({'error': 'All fields are required.'}), 400

    # Check for existing user
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists.'}), 409

    # Save photo
    """photo = request.files.get('photo')
    if photo.filename == '' or not allowed_file(photo.filename):
        return jsonify({'error': 'Invalid or missing photo file.'}), 400

    filename = secure_filename(photo.filename)
    photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    photo.save(photo_path)"""


    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create user
    new_user = User(
        name=name,
        username=username,
        email=email,
        password=hashed_password,
        address=address,
        phoneNumber=phoneNumber
    )

    # Commit to database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.', 'id': new_user.id}), 201

# For this i used raw->json in postman
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email','').strip()
        password = data.get('password','').strip()

        # Verify if both fields were filled
        if not email or not password:
            return jsonify({'error': 'Email and password are required.'}), 400
        
        # Look up user in the database
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            # Successful login
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
                    'phone number': user.phoneNumber
                }
            }), 200
        else:
            # Failed login
            return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

@app.route('/api/user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'id': current_user.id,
        'name': current_user.name,
        'username': current_user.username,
        'email': current_user.email,
        'address': current_user.address,
        'phoneNumber': current_user.phoneNumber,
        'address': current_user.address 
    })

@app.route('/api/user', methods=['PUT'])
@login_required
def update_user():
    data = request.get_json()
    user = current_user
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'phoneNumber' in data:
        user.phoneNumber = data['phoneNumber']
    if 'address' in data:
        user.address = data['address']
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/flights', methods=['GET'])
def search_flights():
    origin = request.args.get('origin', '').strip().upper()
    destination = request.args.get('destination', '').strip().upper()
    date = request.args.get('date', '').strip()

    if not origin or not destination or not date:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        flights = AviationStackAPI.search_flights(origin, destination, date)
        print(f"AviationStack returned {len(flights)} flights")  # debug
        for flight in flights:
            unique_key = f"{flight['airline']}_{flight['flight_number']}_{flight['departure']}"
            flight_id = str(hash(unique_key))
            flight['id'] = flight_id
            flight_cache[flight_id] = flight
        return jsonify(flights)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/flights/<flight_id>', methods=['GET'])
def flight_details(flight_id):
    flight = flight_cache.get(flight_id)
    if not flight:
        return jsonify({'error': 'Flight not found'}), 404
    flight['base_fare'] = flight['price']
    flight['taxes'] = int(flight['price'] * 0.15)
    flight['total'] = flight['price'] + flight['taxes']
    return jsonify(flight)

@app.route('/api/bookings', methods=['POST'])
@login_required
def create_booking():
    data = request.get_json()
    required = ['flight_id', 'total_price']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400
    passenger_name = current_user.name
    email = current_user.email
    phonenumber = current_user.phoneNumber
    booking_ref = f"JAGO-{str(uuid.uuid4())[:8].upper()}"

    booking = Booking(
        user_id=current_user.id,
        flight_data={'flight_id': data['flight_id']},
        passenger_name=passenger_name,
        email=email,
        phonenumber=phonenumber,
        seat_preference=data.get('seat_preference'),
        special_requests=data.get('special_requests'),
        total_price=data['total_price'],
        booking_reference=booking_ref,
        status='pending'
    )
    db.session.add(booking)
    db.session.commit()

    return jsonify({
        'booking_id': booking.id,
        'booking_reference': booking_ref
    }), 201

@app.route('/api/bookings', methods=['GET'])
@login_required
def get_user_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return jsonify([b.to_dict() for b in bookings])

@app.route('/api/bookings/<booking_id>', methods=['GET'])
@login_required
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    if booking.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(booking.to_dict())

@app.route('/api/create-payment-intent', methods=['POST'])
@login_required
def create_payment_intent():
    data = request.get_json()
    booking_id = data.get('booking_id')
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(booking.total_price * 100), # Amount in cents (JMD)
            currency='jmd',
            metadata={'booking_id': booking.id}, # Pass the booking ID for webhook
        )
        # Send the client_secret back to the client
        return jsonify({
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payment-webhook', methods=['POST'])
def payment_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET') # Get from Stripe Dashboard

    try:
        # Verify the webhook signature to ensure it's from Stripe
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': 'Invalid signature'}), 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        booking_id = payment_intent['metadata']['booking_id']
        booking = Booking.query.get(booking_id)
        if booking:
            booking.status = 'paid'
            db.session.commit()
            print(f"Booking {booking_id} marked as paid.")
    
    # Return a 200 response to acknowledge receipt
    return jsonify({'status': 'success'}), 200
    
# For this nothing really needed to inserted in postman, just send a post request to the endpoint
@app.route('/api/auth/logout', methods=['POST'])
@login_required
def handle_logout():
    logout_user()  # ← This now correctly refers to flask_login.logout_user
    return jsonify({'message': 'Logged out successfully'}), 200


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response