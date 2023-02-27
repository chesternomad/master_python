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


#d1 = date.today().strftime('%d/%m/%Y')
email_sent = 0
keyword = 'SUCCESS'
url = 'url'

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("window-size=1980,960")
options.add_argument('--disable-gpu')
options.add_argument("screenshot")
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)
driver.get(url)
driver.maximize_window()
time.sleep(10)


def send_email():
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'to_addr'
    mail.Subject = '[Action Required!] F2 process Failed'
    #mail.Body = 'One of the daily F2 tasks has failed. Please look into it asap'
    # this field is optional
    mail.HTMLBody = 'One of the daily F2 tasks has failed. Please look into it asap <br><img src="C:\\temp\\screenshot.png">'

    # To attach a file to the email (optional):
    # attachment  = "Path to the attachment"
    # mail.Attachments.Add(attachment)

    mail.Send()
    time.sleep(20)
    os.remove('C:\\temp\\screenshot.png')

    return 1


while datetime.datetime.now().hour < 18:
    driver.refresh()
    if not email_sent:
        try:
            element = driver.find_element(
                By.XPATH, f"//*[contains(text(),'{keyword}')]")
            if bool(element):
                driver.save_screenshot('C:\\temp\\screenshot.png')
                email_sent = send_email()
        except NoSuchElementException as err:
            pass
    else:
        break
    time.sleep(180)
driver.quit()
