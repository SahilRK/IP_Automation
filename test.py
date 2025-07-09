import os
import requests
import pandas as pd
from PIL import Image
import json

current_username = os.getlogin()

def resize_image(img_path,img,img_format):
    #Create new image path with image format
    img_path_without_ext = str.split(img_path,".")[0]
    if img_format.lower() == "png":
        img = img.convert("RGB")
        new_img_path = img_path_without_ext+".jpg"
        img.save(new_img_path,"JPEG")
    else:
        new_img_path = img_path_without_ext+"."+img_format
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
    

""" def fetch_profile_images(json_resp):
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
            print("Image not downloaded") """

def check_and_resize_image():
    profImgs = os.listdir('/home/sahilkulkarni/Automation/ESIC_IP_Generation_PY/data/Profile_Pictures')
    listOfImgExt = ('jpg','jpeg','png')
    for imgKey in profImgs:
        img_path = f"/home/sahilkulkarni/Automation/ESIC_IP_Generation_PY/data/Profile_Pictures/{imgKey}"
        #if img.split('.')[1] in listOfImgExt:
        
        try:
            img = Image.open(img_path)
            img_format = img.format
        except:
            img_format = "no_img"

        if img_format.lower() in listOfImgExt:
            print(os.path.getsize(img_path)/1000)
            new_img_path = resize_image(img_path,img,img_format)
            #omsId_imgPath_Dict[imgKey] = f'{new_img_path}'
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
    
    #print(omsId_imgPath_Dict)
    #return omsId_imgPath_Dict

def remove_old_image(img_path):
    os.remove(img_path)


check_and_resize_image()

""" listOfImgs = ""
profImgs = os.listdir('/home/sahilkulkarni/Automation/ESIC_IP_Generation_PY/data/Profile_Pictures')
listOfImgExt = ('jpg','jpeg','png')
for imgKey in profImgs:
    listOfImgs = listOfImgs+f'"{imgKey}" : "C:\\RPA\\Solutions\\ESIC_NewRegistration_Qzone_Windows\\Data\\az.stdbot_admin01\\Profile_Pictures\\{imgKey}",'+"\n"

print("---------------------------------------------------------------")
print(listOfImgs)
print("---------------------------------------------------------------") """