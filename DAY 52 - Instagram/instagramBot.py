from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
import time

class InstaFollower():

    def __init__(self, account):
        """Initializes instagram follower bot with account and account to follow from as arguments."""

        # retrieve msedge driver executable
        msedge_driver_path = "C:\Development\msedgedriver.exe"
        self.driver = webdriver.Edge(executable_path=msedge_driver_path)

        # set members
        self.account = account

    
    def login(self, password):
        """Logs into account with specified password."""

        # login process
        self.driver.get("https://www.instagram.com/")

        time.sleep(5)

        self.driver.find_element_by_name('username').send_keys(self.account)
        self.driver.find_element_by_name('password').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()


    def find_followers(self, account):
        """Searches account specified as argument."""

        # searching process
        time.sleep(5)
        self.driver.get(f'https://www.instagram.com/{account}')

        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        
        time.sleep(2)
        self.to_scroll = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]')

        
    def follow(self):
        """Follows all followers seen in object found in find_followers."""

        for i in range(5):
            time.sleep(4)

            buttons = [button for button in self.driver.find_elements_by_css_selector('.isgrP li button') if button.text.lower() != "following" and button.text.lower() != "requested"]

            for button in buttons:
                time.sleep(1)
                button.click()

            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", self.to_scroll)

        
    def unfollow(self):

        time.sleep(5)
        self.driver.maximize_window()

        self.driver.get(f"https://www.instagram.com/{self.account}")
        time.sleep(5)

        no_following = int(self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text)

        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(5)

        self.to_scroll = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[3]')

        buttons_pressed = 0

        while buttons_pressed < no_following:
            buttons = [button for button in self.driver.find_elements_by_css_selector('li button')]

            for button in buttons:
                time.sleep(2)
                button.click()

                time.sleep(2)
                self.driver.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]').click()

                buttons_pressed += 1
            
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", self.to_scroll)