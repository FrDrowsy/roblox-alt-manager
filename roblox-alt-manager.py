import json
from os.path import abspath, dirname
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime

def log(log_message, warning=False):
    if warning:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " - WARNING - " + log_message)
    else:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " - " + log_message)

def main():
    script = dirname(abspath(__file__))

    with open(f"{script}\\alt_list.json") as f:
        data = json.load(f)

    account_choice = random.choice(list(data.keys()))

    passw = str(data.get(account_choice).get("password"))

    options = Options()
    options.add_argument("--log-level=3")

    s = Service(f"{script}\\chromedriver.exe")

    browser = webdriver.Chrome(service=s, options=options)
    current_url = browser.current_url

    log("Getting Roblox")
    browser.get("https://roblox.com/login")

    log("Logging in")
    username = browser.find_element(by=By.XPATH, value="//*[@id=\"login-username\"]")
    username.send_keys(account_choice)

    password = browser.find_element(by=By.XPATH, value="//*[@id=\"login-password\"]")
    password.send_keys(passw)

    log_in = browser.find_element(by=By.XPATH, value="//*[@id=\"login-button\"]")

    time.sleep(.5)

    log_in.click()

    flag = True
    while(flag):
        if browser.current_url != current_url:
            flag = False
            log("Successfully logged in as: " + account_choice)
            input("Press enter to close Chrome window.")
        else:
            time.sleep(1)

if __name__ == "__main__":
    main()
