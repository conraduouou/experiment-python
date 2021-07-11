from decouple import config
import datetime as dt
import requests

USERNAME = "louise"
TOKEN = config('PIXELA_PASSWORD')

pixela_endpoint = "https://pixe.la/v1/users"

# user_params = {
#     "token": TOKEN,
#     "username": USERNAME,
#     "agreeTermsOfService": "yes",
#     "notMinor": "yes"
# }

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response)

# graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

# graph_config = {
#     "id": "graph1",
#     "name": "Meditation Graph",
#     "unit": "min",
#     "type": "int",
#     "color": "momiji"
# }

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response)

# today = dt.datetime(year=2021, month=7, day=7)

# graph_update = {
#     "date": today.strftime("%Y%m%d"),
#     "quantity": "10"
# }

# update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/graph1"

# response = requests.post(url=update_endpoint, json=graph_update, headers=headers)
# print(response)

# headers = {
#     "X-USER-TOKEN": TOKEN
# }

# delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/graph1/{today.strftime('%Y%m%d')}"

# response = requests.delete(url=delete_endpoint, headers=headers)
# print(response)