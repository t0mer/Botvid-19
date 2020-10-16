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
import helpers


def sign(userCode, sitePassword, Image):
    try:
        #### Starting Sign Proc ####
        logger.info("Starting process")
        logger.debug('-----------------------0000000000-----------------------------------------------')
        logger.debug(str(Image))
        #### Initialize Browser ####
        browser = helpers.GetBrowser()

        try:
            helpers.ping(browser, 'edu')
        except:
            logger.debug('Unable to ping')
        
        browser.get("https://parents.education.gov.il/prhnet/parents/rights-obligations-regulations/health-statement-kindergarden")
        start = '//*[@id="main-content"]/section[1]/div/health-declaration/div/div[1]/div[4]/div/div/div/input'
        time.sleep(2)
        helpers.fullpage_screenshot(browser,Image)
        helpers.log_browser(browser)
        browser.find_element_by_xpath(start).click()
        time.sleep(2)
        
        #### Logging In ####
        user = '//*[@id="HIN_USERID"]'
        siteAccess = '//*[@id="Ecom_Password"]'
        NextPhase = '//*[@id="loginButton2"]'
        browser.find_element_by_xpath(user).send_keys(userCode)
        browser.find_element_by_xpath(siteAccess).send_keys(sitePassword)
        browser.find_element_by_xpath(NextPhase).click()
        time.sleep(2)
        helpers.log_browser(browser)
        logger.info(f"Logged in")
        time.sleep(2)

        try:
            element = "//input[@value='מילוי הצהרת בריאות']"
            checkForButton = browser.find_elements_by_xpath(element)
            LenCheckForButton = len(checkForButton)
            logger.info(f"Starting sign... check buttons: {LenCheckForButton}")
            if LenCheckForButton == 0:
                logger.error("Not able to find the check buttons. Exit")
                helpers.fullpage_screenshot(browser, Image)

            elif LenCheckForButton > 0:
                for x in range(LenCheckForButton):
                    logger.info(x + 1) 
                    browser.find_element_by_xpath(element).click()
                    time.sleep(2)
                    ToApprove = browser.find_elements_by_xpath("//input[@value='אישור']")
                    
                    for a in ToApprove:
                        browser.execute_script("arguments[0].click()", a)
                    time.sleep(2)
        except Exception as ex:
            logger.error(str(ex))
        
        helpers.fullpage_screenshot(browser, Image)
        browser.close()
        return 1
    except Exception as ex:
        logger.info('#################################################################################################')
        logger.error(str(ex))
        browser.close()
        return 0