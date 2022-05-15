from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from os.path import abspath, dirname
import random
import time
import string
import json
from datetime import datetime
import sys

def log(log_message, warning=False):
    if warning:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " - WARNING - " + log_message)
    else:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " - " + log_message)

def main():
    script = dirname(abspath(__file__))

    log("Starting in 5 seconds...")
    time.sleep(5)

    while True:
        with open(f"{script}\\alt_list.json") as f:
            data = json.load(f)
            f.close()

        options = Options()
        options.add_argument("--log-level=3")

        s = Service(f"{script}\\chromedriver.exe")

        browser = webdriver.Chrome(service=s, options=options)

        log("Getting Roblox")

        browser.get("https://roblox.com/")

        months = ["Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month = random.choice(months)
        month_select = Select(browser.find_element(by=By.ID, value="MonthDropdown"))
        month_select.select_by_value(month)

        day_select = Select(browser.find_element(by=By.ID, value="DayDropdown"))
        day = random.randint(1, 28)
        if day < 10:
            # days are stored as 01, 02 etc on the roblox website up to 09
            day = "0" + str(day) 
        else:
            day = str(day)
        day_select.select_by_value(day)

        year = str(random.randint(1970, 2000))
        year_select = Select(browser.find_element(by=By.ID, value="YearDropdown"))
        year_select.select_by_value(year)

        log("Birth values set")

        username = browser.find_element(by=By.XPATH, value="//*[@id=\"signup-username\"]")

        # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        username.send_keys(name)

        password = browser.find_element(by=By.XPATH, value="//*[@id=\"signup-password\"]")

        passw = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(21))
        password.send_keys(passw)

        log("Credentials set")

        singup = browser.find_element(by=By.XPATH, value="//*[@id=\"signup-button\"]")

        # wait for js on roblox to load stuff
        time.sleep(.5)

        username_validation = browser.find_element(by=By.XPATH, value="//*[@id=\"signup-usernameInputValidation\"]").text
        
        log("Validating username")

        while username_validation == "Username not appropriate for Roblox." or username_validation == "This username is already in use":
            log(f"Username invalid, changing username - USERNAME = {name} - ERROR = {username_validation}", True)
            username.clear()
            name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
            username.send_keys(name)

            time.sleep(0.5)

            username_validation = browser.find_element(by=By.XPATH, value="//*[@id=\"signup-usernameInputValidation\"]").text

        log("Username valid")

        singup.click()

        log("Checking for ratelimit")

        ratelimit_warning = browser.find_element(by=By.XPATH, value ="//*[@id=\"GeneralErrorText\"]")

        # wait for js on roblox to load stuff
        time.sleep(.5)
        if ratelimit_warning.text != "Sorry! An unknown error occurred. Please try again later.":
            log("Ratelimit not present")
            log("Signing up, waiting for succesful signin")

            flag = True
            while flag:
                if "home" in browser.current_url:
                    flag = False
                    log("Signin successful")
                else:
                    # wait for signup page to change to home page
                    time.sleep(1)

            user_dict= {name : {"password" : passw, "month" : month, "day" : day, "year" : year, "created_at" : datetime.now().strftime("%d/%m/%Y %H:%M:%S")}}
            data.update(user_dict)

            with open(f"{script}\\alt_list.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            log("Written to file, closing")

            browser.close()
        else:
            log("Getting ratelimited. Please wait some time.", True)
            browser.close()
            sys.exit(0)
        
    log("Beggining next iteration")
    
if __name__ == "__main__":
    main()
