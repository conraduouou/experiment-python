import requests
import datetime as dt

# exercise details
APP_ID = "844aaf96"
API_KEY = "f2522ec51bbc374b262c0c7942826d82"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = "https://api.sheety.co/80df8836e657518ca270cc78ca65b49d/workoutTracing/workouts"

# exercise headers
exercise_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0"
}

# exercise params
post_params = {
    "query": input("Tell me which exercises you did: ")
}

# request to nutritionix
response = requests.post(url= exercise_endpoint, json=post_params, headers=exercise_headers)
workout_data = response.json()["exercises"]

# date to store exercise tracking
today = dt.datetime.now()

# security headers
sheety_headers = {
    "Authorization": "Bearer nagyungiloveusomuchhuhuhuhu"
}

for item in workout_data:
    post_sheety = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%X"),
            "exercise": item["name"].title(),
            "duration": item["duration_min"],
            "calories": item["nf_calories"]
        }
    }

    response = requests.post(url=sheety_endpoint, json=post_sheety, headers=sheety_headers)
    print(response.text)
