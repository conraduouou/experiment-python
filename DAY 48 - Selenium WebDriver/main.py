from selenium import webdriver
import time

msedge_driver_path = "C:\Development\msedgedriver.exe"
driver = webdriver.Edge(executable_path=msedge_driver_path)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element_by_id("cookie")

store = driver.find_elements_by_css_selector("#store div")
store_ids = [item.get_attribute("id") for item in store]

interval = time.time()
timeout = time.time() + 300

while time.time() < timeout:
    cookie.click()

    if time.time() - interval >= 5:

        money = driver.find_element_by_id("money").text
        if "," in money:
            money.replace(",", "")
        cookie_count = int(money)

        all_prices = driver.find_elements_by_css_selector("#store b")

        item_prices = (int(element.text.split("-")[1].strip().replace(",", "")) for element in all_prices if element.text != "")
        
        cookie_upgrades = ((key, value) for key, value in zip(item_prices, store_ids))

        affordable_upgrades = ((cost, tag_id) for cost, tag_id in cookie_upgrades if cookie_count > cost)

        try:
            to_purchase = max(affordable_upgrades)
        except ValueError:
            to_purchase = 0
        else:
            driver.find_element_by_id(to_purchase[1]).click()
            print(to_purchase[0])

        interval += 5

print(driver.find_element_by_id("cps").text)

driver.quit()