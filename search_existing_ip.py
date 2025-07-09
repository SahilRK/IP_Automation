from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
import easygui as egui
from logger_conf import create_log_file

logger = create_log_file()

def open_exist_ip_page(driver):
    status = True
    wait = WebDriverWait(driver,20)
    try:
        existing_ip_link = wait.until(EC.presence_of_element_located((By.ID,'lnkviewip')))
        status = True
    except:
        status = False
        print("Existing IP Link not found in homepage")
    
    if status:
        time.sleep(2)
        #registration_link = driver.find_element(By.ID, "lnkRegisterNewIP")
        driver.execute_script("arguments[0].click()",existing_ip_link)
        return status

def check_for_exist_ip_find_page(driver,listOfOpenWindows):
    retry_count = 0
    status = True
    while retry_count < 3:
        for window in listOfOpenWindows:
            driver.switch_to.window(window)
            wait = WebDriverWait(driver,5)
            try:
                registration_link = wait.until(EC.presence_of_element_located((By.ID, "ctl00_HomePageContent_txtAccMobileNo")))
                print("Opened Existing IP Search Page")
                #egui.msgbox("Opened Existing IP Search Page","Element Found","OK")
                status = True
                break
            except Exception as e:
                status = False
        if status:
            break
        else:
            retry_count += 1
    if status:
        return status
    else:
        print(f"Existing IP Search Link not found")
        return status

def select_details_type(driver,selection_type,selection_value):
    #value_to_select = "925010006609655"
    status,status_msg = select_value_from_dropdown(driver,"ID","ctl00_HomePageContent_ddlType",selection_type)
    #egui.msgbox(status_msg)
    status,status_msg = fill_input_textbox(driver,"ID","ctl00_HomePageContent_txtAccMobileNo",selection_value,selection_type)
    status,status_msg = click_action_button(driver,"ID","ctl00_HomePageContent_btnSubmit","Submit")
    return (status,status_msg)

def select_value_from_dropdown(driver,locator,locator_value,element_value):
    wait = WebDriverWait(driver,10)
    retry_count = 0
    status = False
    exception_msg = ""
    locator = str(locator).upper()
    while retry_count < 3:
        try:
            match locator:
                case "ID":
                    details_select_type = wait.until(EC.visibility_of_element_located((By.ID,locator_value)))
                    #details_select_type = driver.find_element(By.ID,locator_value)
                case "NAME":
                    details_select_type = wait.until(EC.visibility_of_element_located((By.NAME,locator_value)))
                case "CLASS":
                    details_select_type = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,locator_value)))
                case "XPATH":
                    details_select_type = wait.until(EC.visibility_of_element_located((By.XPATH,locator_value)))    
            select_element = Select(details_select_type)
            try:
                select_element.select_by_visible_text(element_value)
                return_value = select_element.first_selected_option.text
                #egui.msgbox(return_value,"Selected Value","OK")
                if return_value == element_value:
                    exception_msg = f"Selected: {element_value}"
                    status = True
                    break
                else:
                    exception_msg = f"Selected element with value {return_value} does not match {element_value}"
                    status = False
                    retry_count += 1
            except Exception as e:
                print(f"No details found with {element_value}")
                exception_msg = f"No details found with {element_value}"
                status = False
                retry_count += 1
        except Exception as e:
            print(f"Unable to find the select drop down for {element_value}")
            exception_msg = f"Unable to find the select drop down for {element_value}"
            status = False
            retry_count += 1
    return (status,exception_msg)

def fill_input_textbox(driver,locator,locator_value,element_value,selection_type):
    retry_count = 0
    wait = WebDriverWait(driver,10)
    locator = str(locator).upper()
    while retry_count < 3:
        try:
            match locator:
                case "ID":
                    textbox_input_type = wait.until(EC.visibility_of_element_located((By.ID,locator_value)))
                case "NAME":
                    textbox_input_type = driver.find_element(By.NAME,'ctl00_HomePageContent_ddlType')
                case "CLASS":
                    textbox_input_type = driver.find_element(By.CLASS_NAME,'ctl00_HomePageContent_ddlType')
                case "XPATH":
                    textbox_input_type = driver.find_element(By.XPATH,'ctl00_HomePageContent_ddlType')

            try:
                textbox_input_type.clear()
                textbox_input_type.send_keys(element_value)
                entered_value = textbox_input_type.get_attribute("value")
                #egui.msgbox(entered_value)
                if entered_value == element_value:
                    exception_msg = f"Entered value for : {element_value}"
                    status = True
                    break
                else:
                    status = False
                    exception_msg = f"Value entered in textbox is different from input for {selection_type}"
                    retry_count +=1
            except Exception as e:
                exception_msg = f"Unable to enter the value for {selection_type}"
                status = False
                retry_count += 1
        except Exception as e:
            exception_msg = f"Unable to find textbox for {element_value}"
            status = False
            retry_count += 1
    return (status,exception_msg)

def click_action_button(driver,locator,locator_value,element_value):
    retry_count = 0
    wait = WebDriverWait(driver,10)
    locator = str(locator).upper()
    while retry_count < 3:
        try:
            match locator:
                case "ID":
                    textbox_input_type = wait.until(EC.visibility_of_element_located((By.ID,locator_value)))
                case "NAME":
                    textbox_input_type = driver.find_element(By.NAME,'ctl00_HomePageContent_ddlType')
                case "CLASS":
                    textbox_input_type = driver.find_element(By.CLASS_NAME,'ctl00_HomePageContent_ddlType')
                case "XPATH":
                    textbox_input_type = driver.find_element(By.XPATH,'ctl00_HomePageContent_ddlType')

            try:
                textbox_input_type.click()
                #entered_value = textbox_input_type.get_attribute("value")
                #egui.msgbox(entered_value)
                exception_msg = f"Clicked {element_value} button"
                status = True
                break
            except Exception as e:
                print(f"Unable to click {element_value}")
                exception_msg = f"Unable to click {element_value} button"
                status = False
                retry_count += 1
        except Exception as e:
            print(f"Unable to find button for {element_value}")
            exception_msg = f"Unable to find button for {element_value}"
            status = False
            retry_count += 1
    return (status,exception_msg)

def check_for_ip_details(driver,locator,locator_value,search_type,curr_emp_dict: dict,qms_id):
    result_header_arr = []
    result_val_arr = []
    retry_count = 0
    wait = WebDriverWait(driver,10)
    locator = str(locator).upper()
    status = False
    status_msg = ""
    try:
        match locator:
            case "ID":
                ip_details_tbl = wait.until(EC.visibility_of_element_located((By.ID,locator_value)))
        tbl_details = ip_details_tbl.find_elements(By.TAG_NAME,"tr")
        for tr_node in tbl_details:
            if len(result_header_arr) == 0: 
                th_nodes = tr_node.find_elements(By.TAG_NAME,"th")
                for th_node in th_nodes:
                    result_header_arr.append(th_node.get_attribute("innerHTML"))
            td_nodes = tr_node.find_elements(By.TAG_NAME,"td")
            for td_node in td_nodes:
                print(td_node.get_attribute("innerHTML"))
                result_val_arr.append(td_node.get_attribute("innerHTML"))
            
        for indx,val in enumerate(result_val_arr):
            curr_emp_dict[f"{result_header_arr[indx]}"] = val
        #employee_details[f"{qms_id}"] = temp_dict
        status = True
        status_msg = f"Data found for employee using {search_type}"            
        curr_emp_dict["Remarks"] = status_msg
    except UnexpectedAlertPresentException as unAlEx:
        #alertWin = driver.switch_to.alert
        #print(f"Alert text is: {alertWin.text}")
        #alertWin.accept()
        status = False
        status_msg = f"IP Details with {search_type} are not available. Error msg from portal - f{unAlEx.alert_text}"
    except Exception as e:
        print(f"Error in fetching IP Details: {str(e)}")
        status = False
        status_msg = f"Unable to find IP Details with {search_type}. Error in fetching IP Details: {e}"
        #employee_details = {}
    return (status,status_msg,curr_emp_dict)