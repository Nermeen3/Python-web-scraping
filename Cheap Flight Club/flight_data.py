import datetime as dt

class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.flights_formatted = {}

    def format_flight_data(self, flights_data):
        # data_dict = []
        # print(flights_data)
        data = flights_data['data'][0]
        data_dict = {
            'cityFrom': data['cityFrom'],
            'cityTo': data['cityTo'],
            'price': data['price'],
            'currency': flights_data['currency'],
            'distance': data['distance'],
            'utc_departure': data['utc_departure'],
            'utc_arrival': data['utc_arrival'],
            'airlines': data['airlines'],
            'baglimit': data['baglimit'],
            'deep_link': data['deep_link'],
        }
        self.flights_formatted = data_dict
        return self.flights_formatted


