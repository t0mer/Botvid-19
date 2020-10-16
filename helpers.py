# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
from datetime import time
from datetime import datetime
import time
import os
from os import path
from selenium.common.exceptions import InvalidSessionIdException
from loguru import logger

#### Setting ChromeOptions ####
def GetBrowser():
    options = webdriver.ChromeOptions()
    options.add_argument("-incognito")
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--start-maximized')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=360,640")
    options.add_argument('--ignore-certificate-errors')
    browser = webdriver.Chrome(executable_path='/opt/chromedriver-86.0.4240.22/chromedriver', options=options)
    return browser

##### Screenshot for mobile view - like webtop #####
def mobile_screenshot(browser,Image):
    if path.exists(Image):
        os.remove(Image)
    logger.info(browser)
    browser.set_window_size(380, 660) #the trick
    time.sleep(2)
    browser.save_screenshot(Image)
    browser.close()

#### Screenshot for regular view ####
def fullpage_screenshot(browser,Image):
    if path.exists(Image):
        os.remove(Image)
    logger.info(browser)
    browser.set_window_size(800, 600) #the trick
    time.sleep(2)
    browser.save_screenshot(Image)
    

#### Browser state logging ####
def log_browser(browser):
    logger.debug(f"Opened page. Url: {browser.current_url}, size: {len(browser.page_source)}")



def ping(browser, page):
    try:
        browser.get('https://bots.techblog.co.il/' + page + '.html')
    except:
        logger.info("Unable to ping")