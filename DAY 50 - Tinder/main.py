from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from decouple import config
import time

# retrieve msedge driver executable
msedge_driver_path = "C:\Development\msedgedriver.exe"
driver = webdriver.Edge(executable_path=msedge_driver_path)

# open tinder using driver and maximize
driver.get("https://www.tinder.com/")
driver.maximize_window()

# login process
time.sleep(3)
driver.find_element_by_xpath('//*[@id="o-738591094"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="o1827995126"]/div/div/div[1]/div/div[3]/span/div[2]/button').click()

# switch to new popup tab
time.sleep(3)
driver.switch_to.window(driver.window_handles[1])
print(driver.title)

# login to facebook popup
time.sleep(3)
driver.find_element_by_name("email").send_keys(config("MY_EMAIL"))
driver.find_element_by_name("pass").send_keys(config("MY_PASS"))
driver.find_element_by_name("login").click()

# switch back to tinder
time.sleep(3)
driver.switch_to.window(driver.window_handles[0])
print(driver.title)

# dismiss all requests
driver.find_element_by_xpath('//*[@id="o-738591094"]/div/div[2]/div/div/div[1]/button').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="o1827995126"]/div/div/div/div/div[3]/button[1]/span').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="o1827995126"]/div/div/div/div/div[3]/button[2]/span').click()

# hit dislike because we don't like hurting people's feelings
swipes = 0

while swipes < 20:
    time.sleep(5)

    # in case there's a popup for a like
    try:
        driver.find_element_by_xpath('//*[@id="o1827995126"]/div/div/div/div[3]/button[2]/span').click()
    except NoSuchElementException:
        pass

    # in case there's a popup for tinder extension
    try:
        driver.find_element_by_xpath('//*[@id="o1827995126"]/div/div/div[2]/button[2]/span').click()
    except NoSuchElementException:
        pass

    # in case buttons can't be detected
    try:
        driver.find_element_by_xpath('//*[@id="o-738591094"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[4]/div/div[2]/button').click()
    except ElementNotInteractableException:
        try:
            driver.find_element_by_xpath('//*[@id="o-738591094"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[5]/div/div[2]/button').click()
        except NoSuchElementException:
            continue
    except NoSuchElementException:
        continue

    swipes += 1

driver.quit()