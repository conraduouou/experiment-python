from selenium import webdriver
from decouple import config
import time

msedge_driver_path = "C:\Development\msedgedriver.exe"
driver = webdriver.Edge(executable_path=msedge_driver_path)

driver.get("https://www.linkedin.com/jobs/search/?geoId=101165590&keywords=python%20developer&location=United%20Kingdom")
driver.maximize_window()

time.sleep(10)

driver.find_element_by_class_name("cta-modal__primary-btn").click()

time.sleep(10)

driver.find_element_by_id("username").send_keys(config("LINKEDIN_EMAIL"))
driver.find_element_by_id("password").send_keys(config("LINKEDIN_PASSWORD"))
driver.find_element_by_css_selector("form button").click()

time.sleep(5)

job_listings = driver.find_elements_by_class_name("job-card-container--clickable")


for job in job_listings:

    job.click()
    time.sleep(2)

    driver.find_element_by_class_name("jobs-save-button").click()