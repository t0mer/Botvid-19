# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime
import time, os
from selenium.common.exceptions import InvalidSessionIdException
from loguru import logger
import helpers

def sign(email, user_id, password, Image):

    try:
        logger.info("Starting process")
        browser = helpers.GetBrowser()
        try:
            helpers.ping(browser, 'infogan')
        except:
            logger.debug('Unable to ping')

        browser.delete_all_cookies()
        browser.get("https://amdocsprodmain.service-now.com/one_portal?id=aop_sc_cat_item&sys_id=781f12f1db5cd8903780e1aa4b961903")
        helpers.log_browser(browser)

        time.sleep(4)

        # Email page
        xpath_email = browser.find_element_by_xpath('//*[@id="i0116"]')
        xpath_email_submit = browser.find_element_by_xpath('//*[@id="idSIButton9"]')

        xpath_email.send_keys(email)
        xpath_email_submit.click()

        time.sleep(4)

        # User and Password page
        xpath_user = browser.find_element_by_xpath('//*[@id="userNameInput"]')
        xpath_password = browser.find_element_by_xpath('//*[@id="passwordInput"]')
        xpath_sign_in = browser.find_element_by_xpath('//*[@id="submitButton"]')

        xpath_user.clear()
        xpath_user.send_keys("ntnet\\" + user_id)
        xpath_password.send_keys(password)
        xpath_sign_in.click()

        time.sleep(4)

        # Declaration
        xpath_approved = browser.find_element_by_xpath("//input[@name='u_approved']")
        xpath_submit = browser.find_element_by_xpath("//button[@name='submit']")

        xpath_approved.click()
        xpath_submit.click()

        helpers.log_browser(browser)
        helpers.fullpage_screenshot(browser,Image)

        return 1
    except Exception as ex:
        logger.error(str(ex))
        return 0
