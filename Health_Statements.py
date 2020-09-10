# -*- coding: utf-8 -*-
from datetime import date
from datetime import time
from datetime import datetime
import time
from argparse import ArgumentParser
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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


def full_page_screenshot(browser):
    image_file = f"/opt/Approval_form_{message_id}.png"

    logger.info(f"[{message_id}] Saving screenshot from browser, session_id: {browser.session_id}, "
                f"image_file: {image_file}")

    browser.set_window_size(800, 600)  # the trick
    time.sleep(2)

    browser.save_screenshot(image_file)
    browser.close()


def log_browser(browser):
    logger.debug(f"[{message_id}] Opened page. Url: {browser.current_url}, size: {len(browser.page_source)}")


def login(browser, user_id, user_password):
    user = '//*[@id="HIN_USERID"]'
    site_access = '//*[@id="Ecom_Password"]'
    next_phase = '//*[@id="loginButton2"]'

    browser.find_element_by_xpath(user).send_keys(user_id)
    browser.find_element_by_xpath(site_access).send_keys(user_password)
    browser.find_element_by_xpath(next_phase).click()
    time.sleep(2)
    log_browser(browser)


def sign_parents_portal(browser):
    # 1
    browser.get(
        "https://parents.education.gov.il/prhnet/parents/rights-obligations-regulations/health-statement-kindergarden")
    start = '//*[@id="main-content"]/section[1]/div/health-declaration/div/div[1]/div[4]/div/div/div/input'
    time.sleep(2)
    log_browser(browser)

    # 2
    browser.find_element_by_xpath(start).click()
    time.sleep(2)
    log_browser(browser)

    # 3
    login(browser, user_id, user_password)
    logger.info(f"[{message_id}] Logged in")

    # 4
    element = "//input[@value='מילוי הצהרת בריאות']"
    kids_checks_buttons = browser.find_elements_by_xpath(element)

    # 5
    len_kids_checks_buttons = len(kids_checks_buttons)
    logger.info(f"[{message_id}] Starting sign... check buttons: {len_kids_checks_buttons}")

    if len_kids_checks_buttons <= 0:
        logger.error(f"[{message_id}] Not able to find the check buttons. Exit")
        full_page_screenshot(browser)
        return

    # 6
    for x in range(len_kids_checks_buttons):
        logger.info(x + 1)
        browser.find_element_by_xpath(element).click()
        time.sleep(2)

        ToApprove = browser.find_elements_by_xpath("//input[@value='אישור']")

        for a in ToApprove:
            browser.execute_script("arguments[0].click()", a)
        time.sleep(2)

    full_page_screenshot(browser)


def sign_pedagogy_portal(browser):
    # 1
    browser.get("https://pedagogy.co.il/student.html#!/login")
    log_browser(browser)

    # 2
    login_element = browser.find_element_by_xpath('//*[@id="main-app"]/div/div/div/div[2]/div/div[1]/div[2]/a/div')
    login_element.click()
    log_browser(browser)

    # 3
    login(browser, user_id, user_password)

    full_page_screenshot(browser)


def main():
    logger.info(f"[{message_id}] Starting process")

    if KidCovid != 'sign':
        return

    browser = webdriver.Chrome(executable_path="/opt/chromedriver-85.0.4183.87/chromedriver", options=option)

    # sign_parents_portal(browser)

    sign_pedagogy_portal(browser)


if __name__ == '__main__':
    main()
