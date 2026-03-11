import time
import pickle
import json

#from actions.utilities import *
from data.data import WEBSITES

# Paths
sign_in_path = '''//*[@id="m_login"]/div[1]/div/div/div[1]/ng-component/div/div[2]/div[1]/div/a''' 
email_field = '''//*[@id="i0116"]'''
next_button = '''//*[@id="idSIButton9"]'''
ver_code_field = '''//*[@id="verificationCodeInput"]'''

def sign_in(driver):
    with open(WEBSITES, "r") as file:
        data = json.load(file)

    website = data["url"]
    while True:
        token = input("Please enter a valid token: ")
        if token:
            break
    website = website + token
    driver.get(website)
    