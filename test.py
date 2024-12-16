""" from selenium import webdriver
#from selenium.webdriver.remote import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver1 = webdriver.Chrome()
options = webdriver.ChromeOptions()

url = "http://localhost:36331"
session_id = "1125b3ad4002568949363e4302914d44"

driver = webdriver.Remote(command_executor=url,options=options)
driver1.close()   # this prevents the dummy browser
driver.session_id = session_id

def open_registration_page(driver):
    wait = WebDriverWait(driver,30)
    registration_link = wait.until(EC.presence_of_element_located((By.ID, "lnkRegisterNewIP1")))
    time.sleep(2)
    #registration_link = driver.find_element(By.ID, "lnkRegisterNewIP")
    registration_link.click()

open_registration_page(driver) """

def loop():
    i = 1
    while i < 10:
        i +=1
        print(i)
        return True
    
loop()