from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from tkinter import *
#from tkinter import messagebox
import time
import easygui as egui

def open_registration_page(driver):
    wait = WebDriverWait(driver,30)
    registration_link = wait.until(EC.presence_of_element_located((By.ID, "lnkRegisterNewIP1")))
    time.sleep(2)
    #registration_link = driver.find_element(By.ID, "lnkRegisterNewIP")
    registration_link.is_displayed()

