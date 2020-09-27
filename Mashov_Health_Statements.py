#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os.path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from argparse import ArgumentParser
from selenium.common.exceptions import InvalidSessionIdException
from loguru import logger


driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)
parser = ArgumentParser()
parser.add_argument("-u", "--user", dest="Mashov_Username")
parser.add_argument("-p", "--pass", dest="Mashov_Password")
parser.add_argument("-s", "--schoolid", dest="Mashov_School_ID")
parser.add_argument("-kn", "--kidnum", dest="Mashov_Kid_Number")

args = parser.parse_args()
var_screenshot_path = "/opt"
var_mashov_username = args.Mashov_Username
var_mashov_password = args.Mashov_Password
var_mashov_school_id = args.Mashov_School_ID
var_mashov_kid_number = args.Mashov_Kid_Number

option = webdriver.ChromeOptions()
option.add_argument("--window-size=800,600")
option.add_argument("disable-gpu")
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-shm-usage")
option.add_argument('--start-maximized')
option.add_argument("-incognito")
option.add_argument("--headless")
option.add_experimental_option("excludeSwitches", ['enable-automation'])

logger.debug('----------------------------------------------------------------------')
logger.info("Starting Mashov Sign process for kid number: " + var_mashov_kid_number)


# **************************** Mashov website ****************************
logger.info(f"Browsing to Mashov website")

driver.get("https://web.mashov.info/students/login")
#choose school:
form_element_mashov_select_school = driver.find_element_by_xpath("//*[@id='mat-input-3']");
#form_element_mashov_select_year = driver.find_element_by_xpath("//*[@id='mat-tab-content-0-0']/div/div/mat-form-field[2]");
form_element_mashov_user = driver.find_element_by_xpath("//*[@id='mat-input-0']");
form_element_mashov_password = driver.find_element_by_xpath("//*[@id='mat-input-4']");
form_element_mashov_login = driver.find_element_by_xpath("//*[@id='mat-tab-content-0-0']/div/div/button[1]");


form_element_mashov_select_school.click()
#form_element_mashov_select_school.send_keys(_convert(var_mashov_school_id)) # Moving to identify by school number instead of school name
form_element_mashov_select_school.send_keys(var_mashov_school_id)
form_element_mashov_select_school.send_keys(Keys.ARROW_DOWN)
form_element_mashov_select_school.send_keys(Keys.RETURN)


form_element_mashov_user.click()
form_element_mashov_user.send_keys(var_mashov_username)
form_element_mashov_password.click()
form_element_mashov_password.send_keys(var_mashov_password)
form_element_mashov_login.click()
time.sleep(10)

logger.info(f"Logged in")

form_element_mashov_select_daily_corona_report = driver.find_element_by_xpath("//*[@id='mainView']/mat-sidenav-content/mshv-student-covidsplash/mat-card/mat-card-content/div[3]/mat-card");
form_element_mashov_select_daily_corona_report.click()
time.sleep(10)

form_element_mashov_select_option1 = driver.find_element_by_xpath("//*[@id='mat-checkbox-1']/label/div");
form_element_mashov_select_option2 = driver.find_element_by_xpath("//*[@id='mat-checkbox-2']/label/div");
form_element_mashov_check_if_selected_option1 = driver.find_element_by_xpath("//*[@id='mat-checkbox-1-input']").get_attribute("aria-checked");
form_element_mashov_check_if_selected_option2 = driver.find_element_by_xpath("//*[@id='mat-checkbox-2-input']").get_attribute("aria-checked");
form_element_mashov_submit_report = driver.find_element_by_xpath("//*[@id='mainView']/mat-sidenav-content/mshv-students-covid-clearance/mat-card/mat-card-actions/button");

if form_element_mashov_check_if_selected_option1 != ("true"):
    form_element_mashov_select_option1.click()
    time.sleep(2)


if form_element_mashov_check_if_selected_option2 != ("true"):
    form_element_mashov_select_option2.click()
    time.sleep(2)

form_element_mashov_submit_report.click()

logger.info(f"Submitted Report")
time.sleep(10)

driver.save_screenshot(var_screenshot_path + "/mashovkid" + var_mashov_kid_number + ".png" )
logger.info(f"Saved Screenshot")
logger.info("Finished Mashov Sign process for kid number: " + var_mashov_kid_number)
logger.debug('----------------------------------------------------------------------')

driver.close()
