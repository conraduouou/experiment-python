from decouple import config
from twitterBot import InternetSpeedTwitterBot

PROMISED_DOWN = 150.0
PROMISED_UP = 100.0

bot = InternetSpeedTwitterBot(PROMISED_DOWN, PROMISED_UP)

bot.get_internet_speed()

if bot.down < PROMISED_DOWN or bot.up < PROMISED_DOWN:
    bot.tweet_at_provider()