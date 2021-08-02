from selenium import webdriver
from decouple import config
import time

class InternetSpeedTwitterBot():

    def __init__(self, promised_down, promised_up):
        
        # retrieve msedge driver executable
        msedge_driver_path = "C:\Development\msedgedriver.exe"
        self.driver = webdriver.Edge(executable_path=msedge_driver_path)

        # download and upload speed
        self.down = 0
        self.up = 0

        # promised download and upload speed
        self.p_down = promised_down
        self.p_up = promised_up
    
    
    def get_internet_speed(self):
        """Tells bot to open up speedtest.net and get both download and upload speed."""

        # open up speedtest.net
        self.driver.get("https://www.speedtest.net/")
        time.sleep(4)

        # retrieve download and upload speed
        self.driver.find_element_by_css_selector(".start-button .start-text").click()
        time.sleep(75)
        
        self.down = float(self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text)
        self.up = float(self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text)

        
    def tweet_at_provider(self):
        """Tells bot to go to twitter.com and tweet current download/upload speed to provider."""

        # open up twitter.com
        self.driver.get("https://twitter.com/")
        time.sleep(4)

        # login process
        self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[3]/div[3]/span/span').click()
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div/main/div/div/div/div[1]/div/div[3]/a/div/span/span').click()
        time.sleep(2)
        self.driver.find_element_by_name('session[username_or_email]').send_keys(config("MY_EMAIL"))
        self.driver.find_element_by_name('session[password]').send_keys(config("MY_PASS"))
        self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div').click()
        time.sleep(5)

        # tweeting process
        tweet = \
            f"""TEST MESSAGE by BOT\n\nHey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {self.p_down}down/{self.p_up}up?"""

        self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div').send_keys(tweet)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span').click()