from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
#from tkinter import *
#from tkinter import messagebox
import time
import easygui as egui

#driver = ""
""" #Browser URL
URL = "https://www.esic.in/EmployerPortal/ESICInsurancePortal/Portal_Loginnew.aspx"
#Initialize driver


def open_portal():
    
    driver.get(URL)
    driver.maximize_window()

    login_button = driver.find_element(By.ID, "btnLogin")
    login_text = login_button.get_attribute("value") """

    #assert login_button.get_attribute("value").lower() == "login"

def login_to_portal(driver,username,password):
    username_ele = driver.find_element(By.ID, "txtUserName")
    password_ele = driver.find_element(By.ID, "txtPassword")
    captcha_ele = driver.find_element(By.ID, "txtChallanCaptcha")
    login_button_ele = driver.find_element(By.ID, "btnLogin")

    creds_inserted = insert_username_password(username,username_ele,password,password_ele)
    if creds_inserted == True:
        captcha_entered = enter_captcha(captcha_ele)
        if captcha_entered == True:
            click_login_btn(login_button_ele)
    
    logged_in_check = check_homepage(driver)
    if logged_in_check == True:
        egui.msgbox("Logged In","Login Status")
        return True
    else:
        egui.msgbox("Login Failed","Login Status")
        return False


def insert_username_password(username,username_ele,password,password_ele):
    
    retry_count = 0
    while(retry_count < 3):
        username_ele.send_keys(username)
        time.sleep(2)
        password_ele.send_keys(password)

        if username_ele.get_attribute("value") != username:
            username_ele.clear()
            password_ele.clear()
            retry_count +=1
        else:
            #messagebox.showinfo("Login Message", f"Entered credentials successfully after {retry_count} retry" )
            #egui.msgbox(f"Entered credentials successfully after {retry_count} retry","Login Message")
            
            break
        
    if retry_count < 3:
        return True
    else:
        return False

def enter_captcha(captcha_ele):
    #input_dialog_box()
    
    retry_count = 0
    while(retry_count < 3):
        captcha_val = egui.enterbox("Enter Captcha Here", "Captcha Box")
        captcha_ele.send_keys(captcha_val)

        if str.strip(captcha_ele.get_attribute("value")) == "":
            captcha_ele.clear()
            retry_count +=1
        else:
            #messagebox.showinfo("Login Message", f"Entered credentials successfully after {retry_count} retry" )
            #egui.msgbox(f"Entered captcha successfully after {retry_count} retry","Login Message")
            
            break
        
    if retry_count < 3:
        return True
    else:
        return False

    #egui.msgbox(f"hello {captcha_ele.get_attribute("value")}")

def click_login_btn(login_button_ele):
    login_button_ele.click()


def check_homepage(driver):
    register_emp_link = driver.find_element(By.ID, "lnkRegisterNewIP").is_displayed()
    if register_emp_link == True:
        return True
    else:
        return False

