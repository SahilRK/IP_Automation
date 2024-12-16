from selenium import webdriver
#from selenium.webdriver.remote import webdriver
from login import *
from open_registration_page import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

#Create a logger and configure the log location

logging.basicConfig()
logger =  logging.getLogger(__name__)


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
retry_count = 0

#Open ESIC Portal and 
def open_portal():
    
    driver.get(URL)
    driver.maximize_window()
    check_login_btn = ""
    wait = WebDriverWait(driver,30)

    #login_button = driver.find_element(By.ID, "btnLogin")
    try:
        login_button = wait.until(EC.presence_of_element_located((By.ID, "btnLogin")))
        check_login_btn = login_button.get_attribute("value")
        if str.lower(check_login_btn) == "login":
            return True
        else:
            return False
    except Exception as e:
        print("Unable to open the homepage or find login button")

def call_login_func():
    retry_count = 0
    check_login_btn = open_portal()
    if check_login_btn == True:
        while retry_count < 3:
            check_login_status = login_to_portal(driver,username,password)
            if check_login_status == True:
                return True
            else:
                driver.close()
                retry_count += 1
    else:
        try:
            driver.close()
        except Exception as e:
            print(e)
        return False

def call_open_reg_func():
    retry_count = 0
    status = True
    while retry_count < 3:
        check_reg_page_status = open_registration_page(driver)
        if check_reg_page_status == True:
            listOfOpenWindows = driver.window_handles
            if len(listOfOpenWindows) == 2:
                check_reg_page_status = check_for_registration_page(driver,listOfOpenWindows)
                if check_reg_page_status == True:
                    break
                else:
                    driver.close()
                    retry_count += 1
            else:
                return False
        else:
            try:
                driver.close()
            except Exception as e:
                print(e)
            retry_count += 1
    print()

status = call_login_func()
if status:
    #Step 2
    status = call_open_reg_func()
else:
    retry_count += 1

#driver.quit()



""" print(f"Session ID is : {existing_session_id}")
print(f"Session URL is : {command_executor}") """

""" ############ For Testing Only ##########
existing_session_id = driver.session_id
command_executor = driver.command_executor._client_config.remote_server_addr
######################################## """