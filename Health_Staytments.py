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

parser = ArgumentParser()
parser.add_argument("-u", "--user", dest="userCode")
parser.add_argument("-p", "--pass", dest="SitePassword")
parser.add_argument("-k", "--kid", dest="KidCovid")
parser.add_argument("-n", "--numberOfKids", dest="NumberKids")


args = parser.parse_args()
userCode = args.userCode
SitePassword = args.SitePassword
KidCovid = 'sign' #args.KidCovid
NumberKids = int (args.NumberKids)
option = webdriver.ChromeOptions()
option.add_argument("-incognito")
option.add_argument("--headless")
option.add_argument("disable-gpu")
option.add_argument("--no-sandbox")
option.add_argument('--start-maximized')
option.add_argument("--disable-dev-shm-usage")
option.add_argument("--window-size=800,600")


def fullpage_screenshot():
    print(browser)
    now = datetime.now()
    browser.set_window_size(800, 600) #the trick
    time.sleep(2)
    image = "/opt/Approval_form.png"
    browser.save_screenshot(image)
    browser.close()


print("Strating process")

browser = webdriver.Chrome(executable_path="/opt/chromedriver-85.0.4183.87/chromedriver", options=option)
browser.get("https://parents.education.gov.il/prhnet/parents/rights-obligations-regulations/health-statement-kindergarden")
start = '//*[@id="main-content"]/section[1]/div/health-declaration/div/div[1]/div[4]/div/div/div/input'
time.sleep( 2 )
browser.find_element_by_xpath(start).click()
time.sleep( 2 )
user = '//*[@id="HIN_USERID"]'
siteAccess = '//*[@id="Ecom_Password"]'
NextPhase = '//*[@id="loginButton2"]'
#5425110
#nRc3pJM7LPtT4iV7Fucv
browser.find_element_by_xpath(user).send_keys(userCode)
browser.find_element_by_xpath(siteAccess).send_keys(SitePassword)
browser.find_element_by_xpath(NextPhase).click()
time.sleep( 2 )
print("Logged IN...")
element = "//input[@value='מילוי הצהרת בריאות']"
checkForButton = browser.find_elements_by_xpath(element)
LenCheckForButton = len(checkForButton)
if KidCovid == 'yuval':
    try:
        browser.find_element_by_xpath('//*[@id="main-content"]/section[1]/div/health-declaration/div/div[1]/div/div[5]/div/div/input').click()
        time.sleep( 2 )
        browser.find_element_by_xpath("//input[@value='אישור']").click()
        time.sleep( 2 )
        fullpage_screenshot()
    except:
        fullpage_screenshot()
    else:
        fullpage_screenshot()
elif KidCovid == 'omer':
    try:
        browser.find_element_by_xpath('//*[@id="main-content"]/section[1]/div/health-declaration/div/div[2]/div/div[5]/div/div/input').click()
        time.sleep( 2 )
        browser.find_element_by_xpath("//input[@value='אישור']").click()
        time.sleep( 2 )
        fullpage_screenshot()
    except:
        fullpage_screenshot()
    else:
        fullpage_screenshot()
elif KidCovid == 'sign':
    print("starting Sign..")
    print(len(checkForButton))
    if int(LenCheckForButton) == 0:
        fullpage_screenshot()
    elif (LenCheckForButton == NumberKids or LenCheckForButton > 0 ):
        for x in range(LenCheckForButton):
            print(x + 1) 
            checkForButton = browser.find_elements_by_xpath(element)
            for button in checkForButton:
                print(button)
                browser.execute_script("arguments[0].click()", button)
                time.sleep( 2 )
                browser.find_elements_by_xpath("//input[@value='מילוי הצהרת בריאות']").click()
                time.sleep( 2 )
        fullpage_screenshot()
    else:
        print("Used else...")
        fullpage_screenshot()
