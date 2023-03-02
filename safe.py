import requests
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import win32com.client as win32
from selenium.common.exceptions import NoSuchElementException

key_list = ['accountsTradeable[]', 'commoditiesTradeable[]']

url_list = ['url1',
            'url2']


def search_value(team, key):
    element = driver.find_element(By.NAME, key)

    with open(f'C:\\temp\\{team}_{key[:-2]}.txt', 'w') as f:
        f.write(element.text.encode("gbk", "ignore").decode("gbk", "ignore"))
        f.close()
    time.sleep(30)
    return


if __name__ == '__main__':
    for i in url_list:
        head, team = i.split('=')
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        driver.get(i)
        # driver.maximize_window()
        time.sleep(10)
        for j in key_list:
            search_value(team, j)
        driver.quit()
