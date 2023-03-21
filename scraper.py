# from bs4 import BeautifulSoup
# import mechanize
# from requests_ntlm import HttpNtlmAuth
# from selenium.webdriver.chrome.service import Service
# build .bat file by script below
# @echo off
# python C:\python\scrape.py
# pause
import requests
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import win32com.client as win32
from selenium.common.exceptions import NoSuchElementException
import datetime
import os

email_sent = 0
# keyword = 'FAILED'
url = 'http://f2sql-uks-p1w01/ReportServer/Pages/ReportViewer.aspx?%2FFuturesII-2%2FHong%20Kong%20Checks%2FScheduler%20Status&rc:showbackbutton=true'
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("window-size=1980,960")
options.add_argument('--disable-gpu')
# options.add_argument("screenshot")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.get(url)
driver.maximize_window()
time.sleep(10)


def send_email(screenshot):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'hkit@sucfin.com'
    mail.Subject = '[Action Required!] F2 process Failed'
    attachment = mail.Attachments.Add(screenshot)
<<<<<<< Updated upstream
    attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "f2_screenshot")
    mail.HTMLBody = 'The latest running task has failed. Please look into it asap <br><img src="cid:f2_screenshot">'
=======
    attachment.PropertyAccessor.SetProperty(
        "http://schemas.microsoft.com/mapi/proptag/0x3712001F", "f2_screenshot")
    mail.HTMLBody = 'One of the daily F2 tasks has failed. Please look into it asap <br><img src="cid:f2_screenshot">'
>>>>>>> Stashed changes
    mail.Send()
    time.sleep(20)
    return 1


while datetime.datetime.now().hour < 13:
    driver.refresh()
    if not email_sent:
        try:
            element = driver.find_element(
                By.XPATH, f"//*[contains(@id,'97iT0R0x0')]")
            if element.text == 'FAILED':
                screenshot = 'C:\\temp\\screenshot.png'
                driver.save_screenshot(screenshot)
                email_sent = send_email(screenshot)
                os.remove(screenshot)
        except NoSuchElementException as err:
            pass
    else:
        break
<<<<<<< Updated upstream
    time.sleep(180)
driver.quit()
=======
time.sleep(180)
driver.quit()
>>>>>>> Stashed changes
