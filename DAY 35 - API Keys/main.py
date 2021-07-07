import requests
from twilio.rest import Client

# constants
LATITUDE = 14.69
LONGITUDE = 121.00
API_KEY = "bb4d1f3635a6578a93e1ae51fcbf0e54"

account_sid = "AC2a10ad9b2fc92cf340629a6318328d0a"
auth_token = "ecfa98dd6d019dca4d55ecdf6e69a329"


# API params
parameters = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "exclude": "current,minutely,daily",
    "appid": API_KEY
}

# get data from API
response = requests.get(
    url="https://api.openweathermap.org/data/2.5/onecall",
    params= parameters
    )
response.raise_for_status()

# convert into json and get 12 hours worth of data from now
data = response.json()["hourly"]
forecast_today = [item["weather"][0]["id"] for item in data if data.index(item) < 12]

will_rain = False

for item in forecast_today:
    if item < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body="It's going to raaaaaaain, bring an umbrella!! ☔",
            from_="+17013532120",
            to="+639262652721"
        )
    print(message.status)