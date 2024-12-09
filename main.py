from selenium import webdriver
#from selenium.webdriver.remote import webdriver
from login import *
from open_registration_page import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

#Initialze the chrome driver path

ser = Service("./chromedriver/linux-115.0.5790.170/chromedriver-linux64/chromedriver")

#Initialize driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach",True)
options.binary_location = "./chrome/linux-115.0.5790.170/chrome-linux64/chrome"
driver = webdriver.Chrome(options=options,service=ser)

#Set credentials
username = "45500254880011099"
password = "Quess#00100424"
URL = "https://www.esic.in/EmployerPortal/ESICInsurancePortal/Portal_Loginnew.aspx"

############ For Testing Only ##########
existing_session_id = ""
command_executor = ""
########################################

#Open ESIC Portal and 
def open_portal():
    
    driver.get(URL)
    driver.maximize_window()
    check_login_btn = ""

    login_button = driver.find_element(By.ID, "btnLogin")
    check_login_btn = login_button.get_attribute("value")

    if str.lower(check_login_btn) == "login":
        return True
    else:
        return False

def call_login_func():
    retry_count = 0
    while retry_count < 3:
        check_login_btn = open_portal()
        if check_login_btn == True:
            check_login_status = login_to_portal(driver,username,password)
            if check_login_status == True:
                ############ For Testing Only ##########
                existing_session_id = driver.session_id
                command_executor = driver.command_executor._client_config.remote_server_addr
                ########################################
                break
            else:
                driver.close()
                retry_count += 1
        else:
            try:
                driver.close()
            except Exception as e:
                print(e)
            retry_count += 1

def call_open_reg_func():
    retry_count = 0
    while retry_count < 3:
        check_reg_page_status = open_registration_page(driver)
        print(driver.window_handles)
        """ if check_reg_page_status == True:
            check_login_status = open_registration_page(driver)
            if check_login_status == True:
                ############ For Testing Only ##########
                existing_session_id = driver.session_id
                command_executor = driver.command_executor._client_config.remote_server_addr
                ########################################
                break
            else:
                driver.close()
                retry_count += 1
        else:
            try:
                driver.close()
            except Exception as e:
                print(e)
            retry_count += 1 """

call_login_func()
call_open_reg_func()

#driver.quit()



print(f"Session ID is : {existing_session_id}")
print(f"Session URL is : {command_executor}")
