from os import set_inheritable
from decouple import config
import requests

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self, endpoint, headers) -> None:
        """Initialize class with specified endpoint and headers. Also gets sheet data from that endpoint."""
        self.endpoint = endpoint
        self.headers = headers
    
        response = requests.get(url=self.endpoint, headers=headers)
        response.raise_for_status()

        self.sheet_data = response.json()['prices']
        self.rows = len(self.sheet_data)

    
    def update_code(self, json_params, row) -> None:
        """Updates row with their corresponding IATA codes."""
        response = requests.put(url=self.endpoint + f"/{row + 2}", headers=self.headers, json=json_params)
        response.raise_for_status()