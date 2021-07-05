import requests

parameters = {
    "amount": 10,
    "type": "boolean"
}

request = requests.get(url="https://opentdb.com/api.php", params=parameters)
request.raise_for_status()

question_data = request.json()["results"]