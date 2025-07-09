import requests
import pandas as pd
import os
from PIL import Image
import json

""" curl --location --request POST 'https://api.getharbour.com/v1/onboard/fetchprofileimage' \
--header 'Authorization: Basic cnBhdXNlcjpGRklFREFDRUlFRQ==' \
--header 'Content-Type: application/json' \
--data-raw '["AS675786", "GS10345447"]' """

current_username = os.getlogin()

def get_input_data():
    """ user_input_file_path = f"C:\RPA\Solutions\ESIC_NewRegistration_Qzone_Windows\Data\{current_username}\Profile_Pictures\profimages.xlsx"
    inputDf = pd.read_excel(user_input_file_path)
    list_of_oms_id = []
    for indx,row in inputDf.iterrows():
        oms_id = row["QMS_ID"]
        list_of_oms_id.append(oms_id) """
    inputFiles = os.listdir(f"C:\RPA\Solutions\ESIC_NewRegistration_Qzone_Windows\Data\{current_username}\Input")
    
    omsId_imgPath_Dict = {}
    if (len(inputFiles)) > 0:
        for file in inputFiles:
            print(file)
            list_of_oms_id = []
            inputDf = pd.read_excel(f"C:\RPA\Solutions\ESIC_NewRegistration_Qzone_Windows\Data\{current_username}\Input\{file}",sheet_name="Sheet1")

            for indx,row in inputDf.iterrows():
                oms_id = row["QMS ID"]
                omsId_imgPath_Dict[f'{oms_id}'] = "No File"
                list_of_oms_id.append(oms_id)
            oms_id_list = json.dumps(list_of_oms_id)

            print(len(list_of_oms_id))
            if(len(list_of_oms_id) > 0):

                ########### Step2: Trigger API to fetch profile images ########### 
                json_resp = trigger_pop_photo_api(oms_id_list)

                ########### Step3: Trigger API to fetch profile images for all the non available cases in POP ########### 
                #json_resp_worq = trigger_worq_photo_api()

                ########### Step4: Fetch profile images and save them in Profile Pictures folder ###########
                fetch_profile_images(json_resp)

                ########### Step5: Check image for size and resize it if the image is not within 50kb to 100kb #############
                omsId_imgPath_Dict = check_and_resize_image(omsId_imgPath_Dict)

        json_file = f'C:\RPA\Solutions\ESIC_NewRegistration_Qzone_Windows\Data\{current_username}\Profile_Pictures\profImgPath.json'
        omsId_Json_obj = json.dumps(omsId_imgPath_Dict)
        with open(json_file,'w') as f:
            f.write(omsId_Json_obj)

    

def trigger_pop_photo_api(oms_id_list):
    url = "https://api.getharbour.com/v1/onboard/fetchprofileimage"
    header = {'Authorization' : 'Basic cnBhdXNlcjpGRklFREFDRUlFRQ==', 'Content-Type':'application/json'}
    #raw_data = '["AS675786", "GS10345447"]'
    raw_data = f'{oms_id_list}'
    #raw_data = '["GS10337069"]'

    response = requests.post(url=url, headers=header,data=raw_data)

    json_resp = response.json()
    return json_resp

def trigger_worq_photo_api():
    url = "https://employee-mss.hamarahr.com/api/v1/employee_profile_details"
    header = {'Content-Type':'application/json'}
    params = {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjE2MjE2LCJpc3MiOiJodHRwOi8vaW5lZGdlLmxvY2FsaG9zdC5jb20vYXBpL2xvZ2luIiwiaWF0IjoxNTg4MjI5Mzg4LCJleHAiOjI1OTIwMDAxNTg4MjI5Mzg4LCJuYmYiOjE1ODgyMjkzODgsImp0aSI6IjJNQVhNWmNVV3JNRkg5UWgifQ.AOQsf78rtjutNZylLJwREJmdQKJhIR4ooFUDcboxu_E','emp_id': f'AS675786',}
    #raw_data = '["AS675786", "GS10345447"]'

    response = requests.post(url=url, headers=header,params=params)

    json_resp = response.json()
    return json_resp

""" print(response.status_code)
print(json_resp["list"])
print("######################") """

""" def resize_image(imgSize,img_path,img,img_format):
    new_width = 800
    img_format = f".{img_format.lower()}"
    if img_path.endswith(img_format):
        new_img_path = img_path
    else:
        new_img_path = img_path+"."+img_format
    while (imgSize > 90 or imgSize < 50): 
        img_height,img_width = img.size
        new_height = int(img_height * (new_width/img_width))
        r_img_size = (new_height,new_width)
        r_img = img.resize(r_img_size,Image.LANCZOS)
        r_img.save(new_img_path)

        imgSize = os.path.getsize(new_img_path)/1000
        print(f"New Image size is "+str(imgSize))
        if imgSize < 90 and imgSize > 50:
            new_width -= 100
        elif imgSize < 50:
            new_width += 50
    remove_old_image(img_path) """

def resize_image(img_path,img,img_format):
    #Create new image path with image format
    if img_format.lower() == "png":
        img = img.convert("RGB")
        new_img_path = img_path+".jpg"
        img.save(new_img_path,"JPEG")
    else:
        new_img_path = img_path+"."+img_format
        img.save(new_img_path)
    #Delete old file with no path:
    remove_old_image(img_path)
    #Get the current size of the new file
    imgSize = os.path.getsize(new_img_path)/1000
    new_width = 800
    while (imgSize > 90 or imgSize < 60): 
        img_height,img_width = img.size
        new_height = int(img_height * (new_width/img_width))
        r_img_size = (new_height,new_width)
        r_img = img.resize(r_img_size,Image.LANCZOS)
        r_img.save(new_img_path)

        imgSize = os.path.getsize(new_img_path)/1000
        print(f"New Image size is "+str(imgSize))
        if imgSize > 90:
            new_width -= 100
        elif imgSize < 60:
            new_width += 50
    return new_img_path
    

def fetch_profile_images(json_resp):
    for emp_details in json_resp["list"]:
        offer_id = emp_details['offerId']
        awsS3FileUrl = emp_details['profileImageUrl']
        profImagePath = f"C:\RPA\Solutions\ESIC_NewRegistration_Qzone_Windows\Data\{current_username}\Profile_Pictures\{offer_id}"
        profileImgResp = requests.get(awsS3FileUrl)
        if profileImgResp.status_code == 200:
            with open(profImagePath,'wb') as file:
                file.write(profileImgResp.content)
                print("Image downloaded successfully")
        else:
            print("Image not downloaded")

def check_and_resize_image(omsId_imgPath_Dict):
    #profImgs = os.listdir(f'C:\RPA\Solutions\ESIC_NewRegistration_Qzone_Windows\Data\{current_username}\Profile_Pictures')
    listOfImgExt = ('jpg','jpeg','png')
    for imgKey,_ in omsId_imgPath_Dict.items():
        img_path = f"C:\RPA\Solutions\ESIC_NewRegistration_Qzone_Windows\Data\{current_username}\Profile_Pictures\{imgKey}"
        #if img.split('.')[1] in listOfImgExt:
        
        try:
            img = Image.open(img_path)
            img_format = img.format
        except:
            img_format = "no_img"

        if img_format.lower() in listOfImgExt and omsId_imgPath_Dict[imgKey] == "No File":
            print(os.path.getsize(img_path)/1000)
            new_img_path = resize_image(img_path,img,img_format)
            omsId_imgPath_Dict[imgKey] = f'{new_img_path}'
    """ for imgFileName in profImgs:
        img_path = f"C:\RPA\Solutions\ESIC_NewRegistration_Qzone_Windows\Data\{current_username}\Profile_Pictures\{imgFileName}"
        #if img.split('.')[1] in listOfImgExt:
        
        try:
            img = Image.open(img_path)
            img_format = img.format
        except:
            img_format = "no_img"

        if img_format.lower() in listOfImgExt and omsId_imgPath_Dict[imgFileName] == "No File":
            print(os.path.getsize(img_path)/1000)
            new_img_path = resize_image(img_path,img,img_format)
            omsId_imgPath_Dict[imgFileName] = f'{new_img_path}' """
    
    print(omsId_imgPath_Dict)
    return omsId_imgPath_Dict

def remove_old_image(img_path):
    os.remove(img_path)

########### Step1: Get list of OMS ID's ###################
get_input_data()
    

