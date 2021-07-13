import requests
from datetime import datetime, timedelta
from flight_data import FlightData

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self, **kw) -> None:
        """Initialize class with specified **s_endpoint, **l_endpoint, **iata_code and **headers."""
        self.search_endpoint = kw.pop('s_endpoint', None)
        self.location_endpoint = kw.pop('l_endpoint', None)
        self.headers = kw.pop('headers', None)
        self.code = kw.pop('iata_code', None)

    def search_location(self, location) -> str:
        """Uses the Kiwi API to search via the location endpoint with specified location as str for IATA code."""

        search_params = {
            "term": location,
            "location_types": "city"
        }

        response = requests.get(url=self.location_endpoint, params=search_params, headers=self.headers)
        response.raise_for_status()

        data = response.json()["locations"]

        for item in data:
            if item["name"].lower() == location.lower():
                return item['code']
    
    def request_search(self, stopovers, params) -> FlightData:
        params['max_stopovers'] = stopovers

        response = requests.get(url=self.search_endpoint, params=params, headers=self.headers)
        response.raise_for_status()

        try:
            f_data = response.json()['data']
            data = f_data[0]
            
        except IndexError:
            if stopovers == 0:
                return self.request_search(1, params)
            else:
                return None
        else:
            return FlightData(
                price=data["price"],
                d_city=data["cityFrom"],
                d_code=data["flyFrom"],
                a_city=data["cityTo"],
                a_code=data["flyTo"],
                outbound=data['route'][0]["local_departure"].split("T")[0],
                inbound=data['route'][2 if stopovers != 0 else 1]["local_departure"].split("T")[0],
                stopovers=1 if stopovers != 0 else 0,
                via_city=data['route'][0]['cityTo'] if stopovers != 0 else ""
            )

    def search_flight(self, iata_code, lowest_price) -> FlightData:
        today = datetime.now()
        later = today + timedelta(days=6*30)

        search_params = {
            "date_from": f"{today.strftime('%d/%m/%Y')}",
            "date_to": f"{later.strftime('%d/%m/%Y')}",
            "fly_from": self.code,
            "fly_to": iata_code,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "price_to": lowest_price,
            "flight_type": "round",
            "max_stopovers": 0
        }

        return self.request_search(0, search_params)