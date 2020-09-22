# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime
import time, os
from selenium.common.exceptions import InvalidSessionIdException
from loguru import logger
import helpers



def sign(parentName, parentId, kidName, kidId, formUrl, Image):
    
    try:
        logger.info("Starting process")
        browser = helpers.GetBrowser()
        try:
            helpers.ping(browser, 'infogan')
        except:
            logger.debug('Unable to ping')

        browser.get(formUrl)
        helpers.log_browser(browser)
        #get needed elements
        kid_id = '//*[@id="form-field-email"]' 
        kid_name = '//*[@id="form-field-name"]' 
        parent_id = '//*[@id="form-field-field_4"]' 
        parent_name = '//*[@id="form-field-field_3"]' 
        form_date = '//*[@id="form-field-field_2"]' 

        #Fill Date
        browser.find_element_by_xpath(form_date).send_keys(str(datetime.now().date()))
        # #UnFocus Date Fiels
        # browser.find_element_by_xpath(kid_id).click()
        #Fill Kid id
        browser.find_element_by_xpath(kid_id).send_keys(str(kidId)) 
        #Fill Kid Name
        browser.find_element_by_xpath(kid_name).send_keys(str(kidName)) 
        #Fill Parent ID
        browser.find_element_by_xpath(parent_id).send_keys(str(parentId)) 
        #Fill Parent NAme 
        browser.find_element_by_xpath(parent_name).send_keys(str(parentName)) 

        #Set Checkbox
        browser.find_element_by_xpath('//*[@id="form-field-field_1-0"]').click()
        browser.find_element_by_xpath('//*[@id="form-field-field_1-1"]').click()
        browser.find_element_by_xpath('//*[@id="form-field-field_1-2"]').click()
        browser.find_element_by_xpath('//*[@id="form-field-field_5"]').click()

        #Send The Form
        browser.find_element_by_xpath('//*[@type="submit"]').submit()

        time.sleep(2)
        helpers.log_browser(browser)
        helpers.fullpage_screenshot(browser,Image)
        return 1
    except Exception as ex:
        logger.error(str(ex))
        return 0