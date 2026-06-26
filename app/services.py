import copy
import uuid
from datetime import datetime, timedelta

# AviationStack confirmed 403 - function_access_restricted on free tier.
# Mock flights only.

MOCK_FLIGHTS = [
    {
        'airline': 'Caribbean Airlines',
        'airline_code': 'BW',
        'flight_number': 'BW201',
        'departure': '06:00',
        'arrival': '10:30',
        'duration': '4h 30m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Boeing 737-800',
        'price': 42000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 14,
    },
    {
        'airline': 'Caribbean Airlines',
        'airline_code': 'BW',
        'flight_number': 'BW205',
        'departure': '14:30',
        'arrival': '19:00',
        'duration': '4h 30m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Boeing 737-800',
        'price': 38500,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 22,
    },
    {
        'airline': 'Caribbean Airlines',
        'airline_code': 'BW',
        'flight_number': 'BW210',
        'departure': '20:45',
        'arrival': '01:15',
        'duration': '4h 30m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Boeing 737 MAX 8',
        'price': 35000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 33,
    },
    {
        'airline': 'American Airlines',
        'airline_code': 'AA',
        'flight_number': 'AA1234',
        'departure': '08:15',
        'arrival': '12:45',
        'duration': '4h 30m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Airbus A321',
        'price': 54000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 8,
    },
    {
        'airline': 'American Airlines',
        'airline_code': 'AA',
        'flight_number': 'AA1892',
        'departure': '16:45',
        'arrival': '22:10',
        'duration': '5h 25m',
        'stops': 1,
        'stop_info': '1 stop (MIA)',
        'aircraft': 'Boeing 737 MAX',
        'price': 41000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 31,
    },
    {
        'airline': 'JetBlue Airways',
        'airline_code': 'B6',
        'flight_number': 'B61089',
        'departure': '10:00',
        'arrival': '14:30',
        'duration': '4h 30m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Airbus A320',
        'price': 49500,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 5,
    },
    {
        'airline': 'JetBlue Airways',
        'airline_code': 'B6',
        'flight_number': 'B62341',
        'departure': '19:20',
        'arrival': '23:55',
        'duration': '4h 35m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Airbus A321neo',
        'price': 44000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 18,
    },
    {
        'airline': 'Delta Air Lines',
        'airline_code': 'DL',
        'flight_number': 'DL456',
        'departure': '12:30',
        'arrival': '18:45',
        'duration': '6h 15m',
        'stops': 1,
        'stop_info': '1 stop (ATL)',
        'aircraft': 'Boeing 757-200',
        'price': 36000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 27,
    },
    {
        'airline': 'Delta Air Lines',
        'airline_code': 'DL',
        'flight_number': 'DL789',
        'departure': '07:00',
        'arrival': '11:30',
        'duration': '4h 30m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Airbus A220-300',
        'price': 52000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 11,
    },
    {
        'airline': 'United Airlines',
        'airline_code': 'UA',
        'flight_number': 'UA3391',
        'departure': '09:45',
        'arrival': '15:20',
        'duration': '5h 35m',
        'stops': 1,
        'stop_info': '1 stop (EWR)',
        'aircraft': 'Boeing 737-900',
        'price': 34500,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 41,
    },
    {
        'airline': 'Air Canada',
        'airline_code': 'AC',
        'flight_number': 'AC1847',
        'departure': '11:15',
        'arrival': '19:30',
        'duration': '8h 15m',
        'stops': 1,
        'stop_info': '1 stop (YYZ)',
        'aircraft': 'Boeing 767-300ER',
        'price': 58000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 9,
    },
    {
        'airline': 'Spirit Airlines',
        'airline_code': 'NK',
        'flight_number': 'NK621',
        'departure': '05:30',
        'arrival': '09:55',
        'duration': '4h 25m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Airbus A320neo',
        'price': 28000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 52,
    },
    {
        'airline': 'Spirit Airlines',
        'airline_code': 'NK',
        'flight_number': 'NK847',
        'departure': '22:10',
        'arrival': '02:35',
        'duration': '4h 25m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Airbus A321',
        'price': 25500,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 67,
    },
    {
        'airline': 'Copa Airlines',
        'airline_code': 'CM',
        'flight_number': 'CM441',
        'departure': '13:00',
        'arrival': '20:45',
        'duration': '7h 45m',
        'stops': 1,
        'stop_info': '1 stop (PTY)',
        'aircraft': 'Boeing 737-800',
        'price': 47000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 19,
    },
    {
        'airline': 'WestJet',
        'airline_code': 'WS',
        'flight_number': 'WS2291',
        'departure': '15:00',
        'arrival': '23:10',
        'duration': '8h 10m',
        'stops': 1,
        'stop_info': '1 stop (YYC)',
        'aircraft': 'Boeing 737 MAX 8',
        'price': 55000,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 24,
    },
    {
        'airline': 'Frontier Airlines',
        'airline_code': 'F9',
        'flight_number': 'F9318',
        'departure': '17:30',
        'arrival': '22:00',
        'duration': '4h 30m',
        'stops': 0,
        'stop_info': 'Direct',
        'aircraft': 'Airbus A320neo',
        'price': 29500,
        'currency': 'JMD',
        'class': 'Economy',
        'seats_available': 38,
    },
]


def _build_iso(date_str, time_str, next_day=False):
    """Build a proper ISO datetime string from a date and HH:MM time."""
    try:
        base = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
        if next_day:
            base += timedelta(days=1)
        return base.isoformat()
    except Exception:
        return f'{date_str}T{time_str}:00'


class AviationStackAPI:
    @classmethod
    def search_flights(cls, origin, destination, date):
        print(f'Serving mock flights for {origin} → {destination} on {date}')
        return cls._mock_flights(origin, destination, date)

    @classmethod
    def _mock_flights(cls, origin, destination, date):
        flights = copy.deepcopy(MOCK_FLIGHTS)
        for f in flights:
            dep_time = f['departure']
            arr_time = f['arrival']

            # Detect overnight flights — arrival hour less than departure hour
            dep_hour = int(dep_time.split(':')[0])
            arr_hour = int(arr_time.split(':')[0])
            overnight = arr_hour < dep_hour

            f['departure'] = _build_iso(date, dep_time)
            f['arrival'] = _build_iso(date, arr_time, next_day=overnight)
            f['origin'] = origin
            f['destination'] = destination
            f['date'] = date
            f['id'] = str(uuid.uuid4())
        return flights