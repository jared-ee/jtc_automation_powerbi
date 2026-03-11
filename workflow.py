import csv
import json
import sys
import time

from actions.sign_in import sign_in
from actions.cookies_utils import obtain_cookies, set_cookies
from actions.create.add_user import add_users_row_level_security, add_users_security

from data.data import DASHBOARDS, WEBSITES

def sign_in_flow(driver):
    sign_in(driver)
    obtain_cookies(driver)

def cookie_flow(driver):
    with open(WEBSITES, "r") as file:
        data = json.load(file)
    website = data["url"]
    driver.get(website)
    set_cookies(driver)
    driver.refresh()

def configure_dashboard():
    with open(DASHBOARDS, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for r in reader:
            dashboard = r[0]
            add_users_row_level_security(dashboard)
            add_users_security(dashboard)
