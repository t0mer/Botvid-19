# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import date, time, datetime
from selenium.common.exceptions import InvalidSessionIdException
import os, time, helpers
from loguru import logger


def sign(user, password, schoolid, kidnum, Image):
    try:
        browser = helpers.GetBrowser()
        logger.info("Starting process")

        try:
            helpers.ping(browser, 'infogan')
        except:
            logger.debug('Unable to ping')
        logger.debug('----------------------------------------------------------------------')
        logger.info("Starting Mashov Sign process for kid number: " + kidnum)
        
        browser.get("https://web.mashov.info/students/login")
        time.sleep(3)
              
        #choose school:
        form_element_mashov_select_school = browser.find_element_by_xpath("//*[@id='mat-input-3']")
        form_element_mashov_user = browser.find_element_by_xpath("//*[@id='mat-input-0']")
        form_element_mashov_password = browser.find_element_by_xpath("//*[@id='mat-input-4']")
        form_element_mashov_login = browser.find_element_by_xpath("//*[@id='mat-tab-content-0-0']/div/div/button[1]")


        form_element_mashov_select_school.click()
        #form_element_mashov_select_school.send_keys(_convert(var_mashov_school_id)) # Moving to identify by school number instead of school name
        form_element_mashov_select_school.send_keys(schoolid)
        form_element_mashov_select_school.send_keys(Keys.ARROW_DOWN)
        form_element_mashov_select_school.send_keys(Keys.RETURN)

        form_element_mashov_user.click()
        form_element_mashov_user.send_keys(user)
        form_element_mashov_password.click()
        form_element_mashov_password.send_keys(password)
        form_element_mashov_login.click()
        time.sleep(3)

        logger.info(f"Logged in") 

        form_element_mashov_select_daily_corona_report = browser.find_element_by_xpath("//*[@id='mainView']/mat-sidenav-content/mshv-student-covidsplash/mat-card/mat-card-content/div[3]/mat-card")
        form_element_mashov_select_daily_corona_report.click()
        time.sleep(10)

        form_element_mashov_select_option1 = browser.find_element_by_xpath("//*[@id='mat-checkbox-1']/label/div")
        form_element_mashov_select_option2 = browser.find_element_by_xpath("//*[@id='mat-checkbox-2']/label/div")
        form_element_mashov_check_if_selected_option1 = browser.find_element_by_xpath("//*[@id='mat-checkbox-1-input']").get_attribute("aria-checked")
        form_element_mashov_check_if_selected_option2 = browser.find_element_by_xpath("//*[@id='mat-checkbox-2-input']").get_attribute("aria-checked")
        form_element_mashov_submit_report = browser.find_element_by_xpath("//*[@id='mainView']/mat-sidenav-content/mshv-students-covid-clearance/mat-card/mat-card-actions/button");

        if form_element_mashov_check_if_selected_option1 != ("true"):
            form_element_mashov_select_option1.click()
            time.sleep(2)


        if form_element_mashov_check_if_selected_option2 != ("true"):
            form_element_mashov_select_option2.click()
            time.sleep(2)

        form_element_mashov_submit_report.click()

        logger.info(f"Submitted Report")
        time.sleep(3) 

        helpers.log_browser(browser)
        helpers.mobile_screenshot(browser,Image)        
        
        logger.info(f"Screenshot Saved")
        logger.info("Finished Mashov Sign process for kid number: " + kidnum)
        logger.debug('----------------------------------------------------------------------')        
        
        return 1
    except Exception as ex:
        logger.error(str(ex))
        return 0



