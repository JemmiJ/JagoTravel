import os
import requests

class AviationStackAPI:
    @classmethod
    def search_flights(cls, origin, destination, date):
        url = 'https://api.aviationstack.com/v1'
        params = {
            'access_key': os.getenv('AVIATIONSTACK_API_KEY'),
            'dep_iata': origin,
            'arr_iata': destination,
            'flight_date': date,
            'limit': 10
        }
        resp = requests.get(url, params=params)
        data = resp.join()

        flights=[]
        for flight in data.get('data', []):
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
            f['price'] = 35000 + (hash(f['id']) %20000)
        return flights