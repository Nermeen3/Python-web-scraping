import requests
import datetime as dt

class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.api_key = "123"
        self.search_url = "https://api.tequila.kiwi.com/v2/search"
        self.headers = {
            'apikey': self.api_key,
            'Content-Type': 'application/json'
        }
        self.params = {
            'apiKey': self.api_key,
            'fly_from': 'GE',
            'fly_to': 'JO',
            'date_from': dt.datetime.now().strftime("%d/%m/%Y"),
            'date_to': dt.datetime.now().strftime("%d/10/%Y"),
            'limit': 1,
            'max_stopovers': 1,
            # 'curr': 'USD, GEL, JOD'
        }

    def search_for_flights(self):
        search_response = requests.get(url=self.search_url, params=self.params, headers=self.headers).json()
        return search_response





