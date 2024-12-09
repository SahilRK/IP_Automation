from selenium import webdriver
from login import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#Initialize driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=options)

#Set credentials
username = "45500254880011099"
password = "Quess#00100424"
URL = "https://www.esic.in/EmployerPortal/ESICInsurancePortal/Portal_Loginnew.aspx"

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

retry_count = 0
while retry_count < 3:
    check_login_btn = open_portal()
    if check_login_btn == True:
        check_login_status = login_to_portal(driver,username,password)
        break
    else:
        try:
            driver.close()
        except Exception as e:
            print(e)
        retry_count += 1

#driver.quit()
