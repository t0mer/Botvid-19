# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
from datetime import time
from datetime import datetime
import time
from argparse import ArgumentParser
import os
from selenium.common.exceptions import InvalidSessionIdException
from loguru import logger


parser = ArgumentParser()
parser.add_argument("-u", "--user", dest="user_id")
parser.add_argument("-p", "--pass", dest="user_password")
parser.add_argument("-k", "--kid", dest="KidCovid")
parser.add_argument("-m", "--messageid", dest="message_id")


args = parser.parse_args()
user_id = args.user_id
user_password = args.user_password
KidCovid = args.KidCovid
message_id = args.message_id

option = webdriver.ChromeOptions()
option.add_argument("-incognito")
option.add_argument("--headless")
option.add_argument("disable-gpu")
option.add_argument("--no-sandbox")
option.add_argument('--start-maximized')
option.add_argument("--disable-dev-shm-usage")
option.add_argument("--window-size=800,600")
option.add_argument('--ignore-certificate-errors')


def fullpage_screenshot():
    logger.info(f"[{message_id}] Saving screenshot from browser: {browser}")
    browser.set_window_size(800, 600) #the trick
    time.sleep(2)
    image = f"/opt/Approval_form_{message_id}.png"
    browser.save_screenshot(image)
    browser.close()
    return image

def log_browser(browser):
    logger.debug(f"[{message_id}] Opened page. Url: {browser.current_url}, size: {len(browser.page_source)}")


logger.info("Starting process")

browser = webdriver.Chrome(executable_path="/opt/chromedriver-85.0.4183.87/chromedriver", options=option)
browser.get("https://parents.education.gov.il/prhnet/parents/rights-obligations-regulations/health-statement-kindergarden")
start = '//*[@id="main-content"]/section[1]/div/health-declaration/div/div[1]/div[4]/div/div/div/input'
time.sleep(2)
log_browser(browser)

browser.find_element_by_xpath(start).click()
time.sleep(2)
log_browser(browser)

user = '//*[@id="HIN_USERID"]'
site_access = '//*[@id="Ecom_Password"]'
next_phase = '//*[@id="loginButton2"]'

browser.find_element_by_xpath(user).send_keys(user_id)
browser.find_element_by_xpath(site_access).send_keys(user_password)
browser.find_element_by_xpath(next_phase).click()
time.sleep(2)
log_browser(browser)

logger.info(f"[{message_id}] Logged in")

element = "//input[@value='מילוי הצהרת בריאות']"

checkForButton = browser.find_elements_by_xpath(element)

LenCheckForButton = len(checkForButton)

if KidCovid == 'sign':
    logger.info(f"[{message_id}] Starting sign... check buttons: {LenCheckForButton}")

    if LenCheckForButton == 0:
        logger.error(f"[{message_id}] Not able to find the check buttons. Exit")
        fullpage_screenshot()

    elif LenCheckForButton > 0:
        for x in range(LenCheckForButton):
            logger.info(x + 1) 
            browser.find_element_by_xpath(element).click()
            time.sleep(2)
            ToApprove = browser.find_elements_by_xpath("//input[@value='אישור']")
            
            for a in ToApprove:
                browser.execute_script("arguments[0].click()", a)
            time.sleep(2)

        fullpage_screenshot()
    else:
        logger.error(r"[{message_id}] Used else...")
