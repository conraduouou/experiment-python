from os import set_inheritable
from decouple import config
import requests

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self, p_endpoint, u_endpoint, headers) -> None:
        """Initialize class with specified endpoint and headers. Also gets sheet data from that endpoint."""
        self.p_endpoint = p_endpoint
        self.u_endpoint = u_endpoint
        self.headers = headers
    
        response = requests.get(url=self.p_endpoint, headers=headers)
        response.raise_for_status()

        self.sheet_data = response.json()['prices']
        self.sheet_rows = len(self.sheet_data)

        response = requests.get(url=self.u_endpoint, headers=self.headers)
        response.raise_for_status()

        self.users_data = response.json()['users']
    
    def update_code(self, json_params, row) -> None:
        """Updates row with their corresponding IATA codes."""
        response = requests.put(url=self.p_endpoint + f"/{row + 2}", headers=self.headers, json=json_params)
        response.raise_for_status()