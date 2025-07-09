from selenium import webdriver
#from selenium.webdriver.remote import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from login import *
#from open_registration_page import *
from search_existing_ip import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import pandas as pd
import os
import sys
from logger_conf import create_log_file
from datetime import datetime

sys.tracebacklimit = 0
#Initialze the chrome driver path

""" ser = Service("./chromedriver/linux-116.0.5793.0/chromedriver-linux64/chromedriver")

#Initialize driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
#options.add_experimental_option("detach",True)
options.binary_location = "./chrome/linux-116.0.5793.0/chrome-linux64/chrome"
driver = webdriver.Chrome(options=options,service=ser) """

# Initialize Chrome WebDriver with WebDriver Manager
opts = webdriver.ChromeOptions()
opts.add_argument("--start-maximized")
serv = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(options=opts,service=serv)

#Set credentials
username = "45500254880011099"
password = "India#06250325"
URL = "https://portal.esic.gov.in/EmployerPortal/ESICInsurancePortal/Portal_Loginnew.aspx"
#URL = "https://portal.esic.in/EmployerPortal/ESICInsurancePortal/Portal_Loginnew.aspx"

############ For Testing Only ##########
existing_session_id = ""
command_executor = ""
########################################
retry_count = 0
employee_details = []
input_data_folder = "/home/sahilkulkarni/Automation/ESIC_IP_Generation_PY/data/Input"
processed_data_folder = "/home/sahilkulkarni/Automation/ESIC_IP_Generation_PY/data/Processed/"
processed_file_name = f"ESIC_Existing_IP_No_Details_{datetime.today().strftime("%d%M%Y%H%M%S")}.xlsx"
input_file_list = os.listdir(input_data_folder)
#inp_files = os.walk(input_data_folder)

logger = create_log_file()

def read_employee_data(inp_file):
    emp_data_DT = pd.read_excel(inp_file)
    return emp_data_DT

#Open ESIC Portal 
def open_portal():
    #login_button = driver.find_element(By.ID, "btnLogin")
    status = False
    status_msg = ""
    try:
        driver.get(URL)
        driver.maximize_window()
        check_login_btn = ""
        wait = WebDriverWait(driver,30)

        login_button = wait.until(EC.visibility_of_element_located((By.ID, "btnLogin")))
        check_login_btn = login_button.get_attribute("value")
        if str.lower(check_login_btn) == "login":
            status = True
            status_msg = "Logged In"
        else:
            status = False
            status_msg = "Unable to find login button on homepage"
    except Exception as e:
        logger.error(f"Error at Stage1: Open Portal. Error Msg: Unable to open the homepage or find login button. {e}")
        #print(f"Error at Stage1: Open Portal. Error Msg: Unable to open the homepage or find login button. {e}")
        #print(f"hello {e.args}")
        status = False
        status_msg = f"Error at Stage1: Open Portal. Error Msg: Unable to open the homepage or find login button. {e}"

    return (status,status_msg)

def check_if_portal_is_loggedin():
    try:
        driver.get(URL)
        driver.maximize_window()
        check_login_btn = ""
        wait = WebDriverWait(driver,30)

        login_button = wait.until(EC.presence_of_element_located((By.ID, "btnLogin")))
        return True
    except:
        return False

def call_login_func():
    retry_count = 0
    status = False
    status_msg = ""
    while retry_count < 3:
        status,status_msg = open_portal()
        if status:
            status,status_msg = login_to_portal(driver,username,password)
            if status:
                status = True
                status_msg = "Login Successful"
                break
            else:
                driver.close()
                status = False
                status_msg = "Login Unsuccessful"
                retry_count +=1
        else:
            try:
                driver.close()
                retry_count +=1
            except Exception as e:
                logger.error("Error at Stage1: Open Portal. Error Msg: Unable to close driver after trying to open portal")
                status_msg = "Error at Stage1: Open Portal. Error Msg: Unable to close driver after trying to open portal"
                status = False
                driver.quit()
    return (status,status_msg)

""" def call_open_reg_func():
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
            retry_count += 1 """

def call_open_exist_num_find_func():
    retry_count = 0
    while retry_count < 3:
        check_page_status = open_exist_ip_page(driver)
        if check_page_status:
            listOfOpenWindows = driver.window_handles
            if len(listOfOpenWindows) == 2:
                check_page_status = check_for_exist_ip_find_page(driver,listOfOpenWindows)
                if check_page_status:
                    status = True
                    status_msg = "Existing IP Page found"
                    break
                else:
                    #driver.close()
                    retry_count += 1
            else:
                retry_count += 1
        else:
            driver.close()
            status = False
            status_msg = "Error in opening Existing IP Page"
            retry_count += 1
    
    return (status,status_msg)
        
def close_all_windows():
    allOpenWindows = driver.window_handles
    for win_handle in allOpenWindows:
        driver.switch_to.window(win_handle)

def switch_to_homepage():
    win_handles = driver.window_handles
    if len(win_handles) > 1:
        driver.quit()
    else:
        driver.switch_to.window(win_handles[0])
        if driver.title != "ESIC_Homepage":
            driver.quit()

        

########################### Start Execution of Program ####################
def init_process():
    status,status_msg = check_homepage(driver,10)
    if status == False:
        status,status_msg = call_login_func()
    if status:
        #Step 2
        #status = call_open_reg_func()
        status,status_msg = call_open_exist_num_find_func()
        return (status,status_msg)
    else:
        logger.error("Unable to login to ESIC portal")
        return (status,status_msg)

def write_extracted_data_to_excel(employee_details: dict):
    final_res_df = pd.DataFrame()
    #for keys in employee_details.keys():
    final_res_df = final_res_df.from_dict(employee_details,orient='columns')
    final_res_df.to_excel(f"{processed_data_folder}/{processed_file_name}","ESIC_Details")
    #final_res_df.loc[len(final_res_df)] = 


########################### Read each input file and process
                          
mob_status = False
acc_status = False
if len(input_file_list) != 0:
    for inp_file in input_file_list:
        emp_det_DT = read_employee_data(f"{input_data_folder}/{inp_file}")
        for ind,dtRow in emp_det_DT.iterrows():
            mob_num = dtRow["MOBILE NUMBER"]
            acc_num = dtRow["ACCOUNT NUMBER"]
            qms_id = dtRow["QMS ID"]
            curr_emp_dict= {"ACC_NO":f"{acc_num}","MOB_NO": f"{mob_num}","QMS_ID" : f"{qms_id}"}

            try:
                status,status_msg = init_process()
                if status:
                #status,status_msg = select_value_from_dropdown(driver,"ID","ctl00_HomePageContent_ddlType","Mobile Number")
                    status,status_msg = select_details_type(driver,"Account Number",str(acc_num))
                    if status:
                        acc_status,status_msg,curr_emp_dict = check_for_ip_details(driver,"ID","ctl00_HomePageContent_gdvIpDetails","Account Number",curr_emp_dict,qms_id)
                        if acc_status == False:
                            status,status_msg = select_details_type(driver,"Mobile Number",str(mob_num))
                            if status:
                                mob_status,status_msg,curr_emp_dict = check_for_ip_details(driver,"ID","ctl00_HomePageContent_gdvIpDetails","Mobile Number",curr_emp_dict,qms_id)
                    if (mob_status or acc_status):
                        print(f"Data available for {qms_id}. "+status_msg)
                        driver.close()
                        switch_to_homepage()
                        employee_details.append(curr_emp_dict)
                    else:
                        print(status_msg)
                        curr_emp_dict["Remarks"] = status_msg
                        employee_details.append(curr_emp_dict)
                else:
                    logger.error(status_msg)
                    driver.quit()
            except Exception as e:
                logger.error(f"Error occured for {qms_id}: Err Message: {e}")
                driver.quit()
    write_extracted_data_to_excel(employee_details)
else:
    logger.info("There are no files for processing currently")
#driver.quit()



""" print(f"Session ID is : {existing_session_id}")
print(f"Session URL is : {command_executor}") """

""" ############ For Testing Only ##########
existing_session_id = driver.session_id
command_executor = driver.command_executor._client_config.remote_server_addr
######################################## """
