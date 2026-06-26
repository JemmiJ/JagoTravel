from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(500), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    loyalty_points = db.Column(db.Integer, default=0, nullable=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_data = db.Column(db.JSON, nullable=False)
    passenger_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=False)
    seat_preference = db.Column(db.String(50), nullable=True)
    special_requests = db.Column(db.JSON, nullable=True)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    booking_reference = db.Column(db.String(20), unique=True, nullable=False)
    checked_in = db.Column(db.Boolean, default=False, nullable=True)
    boarding_pass_code = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'booking_reference': self.booking_reference,
            'passenger_name': self.passenger_name,
            'email': self.email,
            'phonenumber': self.phonenumber,
            'seat_preference': self.seat_preference,
            'special_requests': self.special_requests,
            'total_price': self.total_price,
            'flight_data': self.flight_data,
            'status': self.status,
            'checked_in': self.checked_in,
            'boarding_pass_code': self.boarding_pass_code,
            'created_at': self.created_at.isoformat(),
        }


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    fromcountry = db.Column(db.String(80), nullable=False)
    tocountry = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    residentcountry = db.Column(db.String(80), unique=True, nullable=False)
    fromrequirements = db.Column(db.Text, nullable=False)
    torequirements = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'fromcountry': self.fromcountry,
            'tocountry': self.tocountry,
            'duration': self.duration,
            'residentcountry': self.residentcountry,
            'fromrequirements': self.fromrequirements,
            'torequirements': self.torequirements,
        }