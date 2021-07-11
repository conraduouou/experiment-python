##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

from decouple import config
import pandas
import smtplib
import random
import datetime as dt

# function that returns bool if month and day matches today
def is_match(Datetime, p_details):
    if Datetime.month == p_details["month"]:
        return Datetime.day == p_details["day"]
    
    return False

# birthdays csv acquired through pandas
birthdays = pandas.read_csv("DAY 32 - SMTP/birthdays.csv")
birthdays_list = birthdays.to_dict(orient="records")

# datetime
now = dt.datetime.now()

# email and password
my_email = config('N_EMAIL')
password = config('N_PASSWORD')

# loop through each person in birthday list
for person in birthdays_list:
    if is_match(now, person):
        path = f"DAY 32 - SMTP/letter_templates/letter_{random.randint(1,3)}.txt"

        with open(path) as letter:
            contents = letter.read()
            contents = contents.replace("[NAME]", person["name"])
            contents = contents.replace("Angela", "Nakko <3")

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="test.2712@yahoo.com",
                msg=f"Subject: Happy Birthday, flover!\n\n{contents}"
            )