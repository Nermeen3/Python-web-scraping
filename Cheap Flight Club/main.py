# TODO: This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes
#  to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
flight_data = FlightData()
notification_manager = NotificationManager()

flights_kiwi = flight_search.search_for_flights()
flights_formatted = flight_data.format_flight_data(flights_kiwi)
data_manager.add_flight(flights_formatted)
notification_manager.send_sms()



