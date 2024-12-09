from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import easygui as egui

def open_registration_page(driver):
    status = ""
    wait = WebDriverWait(driver,30)
    try:
        registration_link = wait.until(EC.presence_of_element_located((By.ID, "lnkRegisterNewIP1")))
        status = True
    except Exception as e:
        status = False
        print(e)
    
    if status == True:
        time.sleep(2)
        #registration_link = driver.find_element(By.ID, "lnkRegisterNewIP")
        registration_link.click()
        return True
    else:
        return False