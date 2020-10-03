# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, time, datetime
from selenium.common.exceptions import InvalidSessionIdException
import os, time, helpers
from loguru import logger

def sign(userCode, sitePassword, Image):
    try:
        browser = helpers.GetBrowser()
        logger.info("Starting process")

        try:
            helpers.ping(browser, 'infogan')
        except:
            logger.debug('Unable to ping')

        browser.get("https://www.webtop.co.il/mobilev2/?")
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="misradHachinuch"]').click()
        time.sleep(1)

        browser.find_element_by_xpath('//*[@id="HIN_USERID"]').send_keys(str(userCode)) 
        browser.find_element_by_xpath('//*[@id="Ecom_Password"]').send_keys(str(sitePassword)) 
        time.sleep(1)
        logger.info('logged in!')
        browser.find_element_by_xpath('//*[@id="loginButton2"]').click()
        time.sleep(2)
        browser.get("https://www.webtop.co.il/mobilev2/corona.aspx")
        time.sleep(1)
        sign_btn=browser.find_element_by_xpath('//*[@id="viewData"]')
        if 'disabled' not in sign_btn.get_attribute('class').split():
            logger.info("class: " + sign_btn.get_attribute('class'))
            sign_btn.click()
            time.sleep(1)
            browser.find_element_by_xpath('//*[@id="signForm"]').click()
            time.sleep(2)
        helpers.log_browser(browser)
        helpers.mobile_screenshot(browser,Image)
        return 1
    except Exception as ex:
        logger.error(str(ex))
        return 0