from bs4 import BeautifulSoup
from decouple import config
import lxml
import requests
import smtplib

AMAZON_LINK = "https://www.amazon.com/Controller-Gamepad-Joystick-Windows-Dual-Vibration/dp/B07WYWT4H8/"

headers = {
    "Request Line": "GET / HTTP/1.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55"
}

response = requests.get(AMAZON_LINK, headers=headers)

# make soup from request
soup = BeautifulSoup(response.text, "lxml")

price = float(soup.find("span", id="priceblock_saleprice").string.split('$')[1])

if price < 20:
    message = f"""Subject: Amazon Price Alert!
    \n\n{soup.find('span', id='productTitle').string.strip().split(',')[0]} is now at ${price:.2f}.\n
    """

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(config("N_EMAIL"), config("N_PASSWORD"))
        connection.sendmail(
            from_addr=config("N_EMAIL"),
            to_addrs="louiserafaellalu@gmail.com",
            msg=message
        )
    
    print("OK")