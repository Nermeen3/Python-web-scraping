import requests

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.flight_deals_url = "https://api.sheety.co/c56f8a5b2a5e01a72c6fecbf6ce455a7/flightDeals/prices"
        # self.headers = {
        #     'Authorization': 'Basic bnVsbDpudWxs'
        # }
        # self.flight_deals_response = requests.get(url=self.flight_deals_url, headers=self.headers).json()
        # print(self.flight_deals_response)

    def add_flight(self, flights):
        self.flights_params = {
            'price': {
                'cityFrom': flights['cityFrom'],
                'cityTo': flights['cityTo'],
                'price': flights['price'],
                'currency': flights['currency'],
                'distance': flights['distance'],
                'departureTime': flights['utc_departure'],
                'arrivalTime': flights['utc_arrival'],
                'airline': flights['airlines'][0],
                'bagInfo': str(flights['baglimit']),
                'deepLink': flights['deep_link'],
            }
        }
        print(flights_params)
        add_flights_response = requests.post(url=self.flight_deals_url, json=flights_params)
        print(add_flights_response.text)





