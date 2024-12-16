from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import easygui as egui

def open_registration_page(driver):
    status = ""
    wait = WebDriverWait(driver,10)
    try:
        registration_link = wait.until(EC.presence_of_element_located((By.ID, "lnkRegisterNewIP")))
        status = True
    except Exception as e:
        status = False
        print(f"Registration Link Element not found with exception {e}")
        return status
    
    if status == True:
        time.sleep(2)
        #registration_link = driver.find_element(By.ID, "lnkRegisterNewIP")
        driver.execute_script("arguments[0].click()",registration_link)
        #registration_link.click()
        return True
    else:
        return False

def check_for_registration_page(driver,listOfOpenWindows):
    for window in listOfOpenWindows:
        driver.switch_to.window(window)
        wait = WebDriverWait(driver,10)
        try:
            registration_link = wait.until(EC.presence_of_element_located((By.ID, "ctl00_HomePageContent_txtEmployerCode")))
            status = True
        except Exception as e:
            status = False
            print(f"Registration Link Element not found with exception {e}")
        return status
        