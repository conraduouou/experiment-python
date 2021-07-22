#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from decouple import config
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

HERE_CODE = "PH"
HERE_IATA = "MNL"

# flight search endpoint
locations_endpoint = "https://tequila-api.kiwi.com/locations/query"
search_endpoint = "https://tequila-api.kiwi.com/v2/search"
prices_endpoint = "https://api.sheety.co/80df8836e657518ca270cc78ca65b49d/flightDeals/prices"
users_endpoint = "https://api.sheety.co/80df8836e657518ca270cc78ca65b49d/flightDeals/users"

# headers
sheety_headers = {
    "Authorization": f"Bearer {config('SHEETY_TOKEN')}"
}

search_headers = {
    "apikey": config('FLIGHT_KEY')
}

# initialize classes
data_manager = DataManager(prices_endpoint, users_endpoint, sheety_headers)
flight_search = FlightSearch(s_endpoint=search_endpoint, l_endpoint=locations_endpoint, headers=search_headers, iata_code=HERE_IATA)
flight_data = []

# supply test values
for row in range(data_manager.sheet_rows):
    if data_manager.sheet_data[row]["iataCode"] == "":
        to_pass = {
            "price": {
                "iataCode": flight_search.search_location(data_manager.sheet_data[row]["city"])
            }
        }

        data_manager.update_code(to_pass, row)


for row in data_manager.sheet_data:
    flight_data.append(flight_search.search_flight(row["iataCode"], row["lowestPrice"]))


messenger = NotificationManager(flight_data, config('ACCOUNT_SID'), config('AUTH_TOKEN'))

messenger.send_message()