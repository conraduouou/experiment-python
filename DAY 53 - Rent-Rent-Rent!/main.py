from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# constants
FORMS_URL = "https://forms.gle/7GUHKVhPQtSkhFQP7"
RENTS_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
SCROLL_HEIGHT = "document.body.scrollHeight"

# retrieve msedge driver executable
msedge_driver_path = "C:\Development\msedgedriver.exe"
driver = webdriver.Edge(executable_path=msedge_driver_path)

# open site
driver.get(RENTS_URL)


def bypass(captcha):
    ActionChains(driver).click_and_hold(captcha).perform()
    time.sleep(5)
    ActionChains(driver).release().perform()


def get_info() -> dict:
    body = driver.find_element_by_tag_name('body')

    # press buttons to render the whole page before making a soup out of it
    for i in range(20):
        body.send_keys(Keys.TAB)

    for i in range(100):
        body.send_keys(Keys.ARROW_DOWN)

    # make soup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # get links, addresses, and prices from soup
    links = [link['href'] for link in soup.find_all(name='a', class_='list-card-img')]
    addrs = [address.text for address in soup.find_all(name='address', class_='list-card-addr')]
    prices = [price.text for price in soup.find_all(name='div', class_='list-card-price')]

    return {"addresses": addrs, "prices": prices, "links": links}


time.sleep(5)

# if ever captcha gets in the way, hope this isn't illegal
try:
    captcha = driver.find_element_by_id('px-captcha')
except NoSuchElementException:
    pass
else:
    bypass(captcha)
finally:
    time.sleep(10)
    info = get_info()


# form answering process
for i in range(len(info['addresses'])):

    # open forms
    driver.get(FORMS_URL)

    time.sleep(3)

    add = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    pri = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    lnk = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    found = False


    if "|" in info['addresses'][i]:
        address = info['addresses'][i].split('|')[1].strip()
    
    if "+" in info['prices'][i]:
        price = info['prices'][i].split('+')[0]
    elif "/" in info['prices'][i]:
        price = info['prices'][i].split('/')[0]
    
    if not info['links'][i].startswith('https'):
        lnk.send_keys("https://www.zillow.com" + info['links'][i])
        found = True
    
    add.send_keys(address)
    pri.send_keys(price)
    if not found:
        lnk.send_keys(info['links'][i])

    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span').click()

    time.sleep(5)