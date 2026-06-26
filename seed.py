"""
Demo seed script — run once to add a cancelled and checked-in booking
to the demo account.

Usage:
    flask shell < seed.py
OR:
    python seed.py  (if FLASK_APP is set)
"""

import os
os.environ.setdefault('FLASK_APP', 'app')

from app import app, db
from app.models import Booking, User
import uuid
from datetime import datetime, timedelta

with app.app_context():
    # Find demo user
    user = User.query.filter_by(email='ajaferguson278@gmail.com').first()
    if not user:
        print("User not found. Check the email address.")
    else:
        # ── Checked-in booking with boarding pass ──────────────────────
        checked_in = Booking(
            user_id=user.id,
            flight_data={
                'airline': 'Caribbean Airlines',
                'flight_number': 'BW201',
                'origin': 'KIN',
                'destination': 'JFK',
                'departure': '2026-07-15T06:00:00',
                'arrival': '2026-07-15T10:30:00',
                'duration': '4h 30m',
                'stops': 0,
                'route': 'KIN → JFK',
            },
            passenger_name=user.name,
            email=user.email,
            phonenumber=user.phoneNumber,
            seat_preference='window',
            special_requests=[],
            total_price=48300,
            booking_reference=f'JAGO-{str(uuid.uuid4())[:8].upper()}',
            status='checked_in',
            checked_in=True,
            boarding_pass_code=f'BP{str(uuid.uuid4())[:6].upper()}',
        )

        # ── Cancelled booking ──────────────────────────────────────────
        cancelled = Booking(
            user_id=user.id,
            flight_data={
                'airline': 'American Airlines',
                'flight_number': 'AA1234',
                'origin': 'KIN',
                'destination': 'MIA',
                'departure': '2026-07-10T08:15:00',
                'arrival': '2026-07-10T12:45:00',
                'duration': '4h 30m',
                'stops': 0,
                'route': 'KIN → MIA',
            },
            passenger_name=user.name,
            email=user.email,
            phonenumber=user.phoneNumber,
            seat_preference='aisle',
            special_requests=[],
            total_price=62100,
            booking_reference=f'JAGO-{str(uuid.uuid4())[:8].upper()}',
            status='cancelled',
            checked_in=False,
            boarding_pass_code=None,
        )

        db.session.add(checked_in)
        db.session.add(cancelled)
        db.session.commit()

        print(f"✓ Checked-in booking added: {checked_in.booking_reference}")
        print(f"✓ Cancelled booking added:  {cancelled.booking_reference}")
        print(f"✓ Done. User: {user.name} ({user.email})")
