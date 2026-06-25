import os
import requests

class AviationStackAPI:
    @classmethod
    def search_flights(cls, origin, destination, date):
        url = 'https://api.aviationstack.com/v1/flights'
        params = {
            'access_key': os.getenv('AVIATIONSTACK_API_KEY'),
            'dep_iata': origin,
            'arr_iata': destination,
            'flight_date': date,
            'limit': 10
        }
        resp = requests.get(url, params=params)
        data = resp.json()

        # ✅ Log the full response for debugging
        print("AviationStack response status:", resp.status_code)
        print("AviationStack response data:", data)

        # Check for errors
        if not data.get('data'):
            print("No 'data' key or empty list. Check API response.")
            return []

        flights = []
        for flight in data['data']:
            flights.append({
                'id': flight.get('flight', {}).get('iata', 'N/A'),
                'airline': flight.get('airline', {}).get('name', 'Unknown'),
                'flight_number': flight.get('flight', {}).get('number', 'N/A'),
                'departure': flight.get('departure', {}).get('scheduled', ''),
                'arrival': flight.get('arrival', {}).get('scheduled', ''),
                'duration': 'N/A',
                'stops': 0,
                'price': 0,
                'currency': 'JMD'
            })

        for f in flights:
            f['price'] = 35000 + (hash(f['id']) % 20000)
        return flights