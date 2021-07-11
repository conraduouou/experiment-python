from decouple import config
import requests
import smtplib
from datetime import datetime

MY_LAT = 14.689061 # Your latitude
MY_LONG = 120.995954 # Your longitude

EMAIL    = config('N_EMAIL')
PASSWORD = config('N_PASSWORD')

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:

        now = datetime.now()

        parameters = {
            "date": f"{now.year}-{now.month}-{now.day + 1}",
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0,
        }

        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        data = response.json()

        # apparently, sunset and sunrise times in the PH are flipped
        sunset = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunrise = int(data["results"]["sunset"].split("T")[1].split(":")[0])

        now_hour = now.hour

        if now_hour > sunset:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(EMAIL, PASSWORD)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs="louiserafaellalu@gmail.com",
                    msg=f"Subject: Look up, Flover!\n\nThe ISS is above you!! Quick!"
                )