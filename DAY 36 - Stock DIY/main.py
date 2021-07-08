import requests
import datetime as dt
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# twilio
SID = "AC2a10ad9b2fc92cf340629a6318328d0a"
TOKEN = "ecfa98dd6d019dca4d55ecdf6e69a329"

# api keys
STOCK_API_KEY = "4UT0V9I4XBXI5UDK"
NEWS_API_KEY = "5bc84800eed443baa5f34f1d7a73452e"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey":STOCK_API_KEY
}

response = requests.get(url="https://www.alphavantage.co/query", params=stock_parameters)
response.raise_for_status()

# get data and assign yesterday and day before yesterday
data = response.json()["Time Series (Daily)"]
stock_data = [data[item] for item in data]

last1_day = stock_data[0]
last2_day = stock_data[1]
 
stock_price_difference = (float(last1_day["4. close"]) - float(last2_day["4. close"]))
difference_percentage = abs(stock_price_difference / float(last1_day["1. open"]))

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

news_parameters = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
    "language": "en"
}

response = requests.get(url="https://newsapi.org/v2/everything", params=news_parameters)
news_data = response.json()["articles"]
latest_news = [item for item in news_data if news_data.index(item) < 3]

to_send = ""

if difference_percentage > 0.05:
    if stock_price_difference > 0:
        to_send += "\n" + STOCK + f": 🔺 {difference_percentage * 100:.0f}%\n"
    else:
        to_send += "\n" + STOCK + f": 🔻 {difference_percentage * 100:.0f}%\n"
    
    for item in latest_news:
        to_send += f"Headline: {item['title']}\n"
        to_send += f"Brief: {item['description']}\n\n"


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

if difference_percentage > 0.05:
    client = Client(SID, TOKEN)
    message = client.messages \
        .create(
            body=to_send,
            from_="+17013532120",
            to="+639262652721"
        )
    
    print(message.status)


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""