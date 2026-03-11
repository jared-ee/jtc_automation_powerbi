import time
import pickle
import selenium.webdriver
from data.data import COOKIES

def obtain_cookies(driver):
    pickle.dump(driver.get_cookies(), open("data/cookies.pkl", "wb"))

def set_cookies(driver):
    cookies = pickle.load(open("data/cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()

def get_api_cookies():
    cookies = pickle.load(open(COOKIES, "rb"))
    cookie_header = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

    return cookie_header
