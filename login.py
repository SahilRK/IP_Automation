from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import easygui as egui
from captcha_breaker import take_screenshot_captcha
from logger_conf import create_log_file

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
logger = create_log_file()

def login_to_portal(driver,username,password):
    retry_count = 0
    status = False
    status_msg = ""
    while retry_count < 6:
        username_ele = driver.find_element(By.ID, "txtUserName")
        print(f"Username found")
        password_ele = driver.find_element(By.ID, "txtPassword")
        print(f"Password found")
        captcha_ele = driver.find_element(By.ID, "txtChallanCaptcha")
        print(f"Captcha found")
        login_button_ele = driver.find_element(By.ID, "btnLogin")

        creds_inserted = insert_username_password(username,username_ele,password,password_ele)
        if creds_inserted == True:
            take_screenshot_captcha(driver)
            captcha_entered = enter_captcha(captcha_ele)
            if captcha_entered == True:
                click_login_btn(login_button_ele)
    
        status,status_msg = check_homepage(driver,3)
        if status:
            #egui.msgbox("Logged In","Login Status")
            driver.execute_script("document.title = 'ESIC_Homepage'")
            status = True
            status_msg = "Logged In"
            break
        else:
            status,status_msg = check_for_captcha_error(driver,3)
            if status:
                retry_count+=1
            else:
                status,status_msg = check_for_credential_error(driver,3)
                if status:
                    break
                else:
                    retry_count+=1
    
    return(status,status_msg)
    


def insert_username_password(username,username_ele,password,password_ele):
    
    retry_count = 0
    while(retry_count < 3):
        username_ele.clear()
        username_ele.send_keys(username)
        time.sleep(2)
        password_ele.clear()
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
    status = False
    retry_count = 0
    while(retry_count < 3):
        captcha_val = egui.enterbox("Enter Captcha Here", "Captcha Box")
        captcha_ele.send_keys(captcha_val)
        time.sleep(2)
        if str.strip(captcha_ele.get_attribute("value")) != "":
            status = True
            break
        else:
            #messagebox.showinfo("Login Message", f"Entered credentials successfully after {retry_count} retry" )
            #egui.msgbox(f"Entered captcha successfully after {retry_count} retry","Login Message")
            captcha_ele.clear()
            retry_count +=1
            status = False
            
    if status:
        return True
    else:
        return False

    #egui.msgbox(f"hello {captcha_ele.get_attribute("value")}")

def click_login_btn(login_button_ele):
    login_button_ele.click()


def check_homepage(driver,wait_time):
    status = False
    status_msg = ""
    wait = WebDriverWait(driver,wait_time)
    try:
        register_emp_link = wait.until(EC.visibility_of_element_located((By.ID,"lnkRegisterNewIP")))
        #register_emp_link = driver.find_element(By.ID, "lnkRegisterNewIP").is_displayed()
        status = True
        status_msg = "Logged in"
    except:
        status = False
        status_msg = "Not logged in"
    return (status,status_msg)

def check_for_captcha_error(driver,wait_time):
    wait = WebDriverWait(driver,wait_time)
    status = False
    status_msg = ""
    try:
        captcha_err_ele = wait.until(EC.visibility_of_element_located((By.ID, 'lblChallanMessage')))
        if captcha_err_ele.text != "":
            status = True
            status_msg = "Invalid captcha"
            ##### Clear both captcha and authentication error
            driver.execute_script("document.getElementById('lblChallanMessage').innerHTML = ''")
            driver.execute_script("document.getElementById('lblMessage').innerHTML = ''")
        else:
            status = False
            status_msg = "Valid captcha"
    except Exception as e:
        status = True
        status_msg = f"Error in fetching captcha error message :- {e}"
    
    return (status,status_msg)

def check_for_credential_error(driver,wait_time):
    wait = WebDriverWait(driver,wait_time)
    status = False
    status_msg = ""
    try:
        creds_err_ele = wait.until(EC.visibility_of_element_located((By.ID, 'lblMessage')))
        if str(creds_err_ele.get_attribute('innerHTML')).strip() != "":
            status = True
            status_msg = "Invalid credentials. Authentication failed."
            ##### Clear both captcha and authentication error
            driver.execute_script("document.getElementById('lblMessage').innerHTML = ''")
            driver.execute_script("document.getElementById('lblChallanMessage').innerHTML = ''")
        else:
            status = False
            status_msg = "Valid credentials"
    except Exception as e:
        status = True
        status_msg = f"Error in fetching authentication error message :- {e}"
    
    return (status,status_msg)