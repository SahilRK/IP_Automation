from wand.image import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from logger_conf import create_log_file

logger = create_log_file()

def take_screenshot_captcha(driver):
    print(driver)
    captcha = driver.find_element(By.ID, "img1")
    captcha.screenshot("./data/Captchas/testCaptcha.png")
    
    read_image()

def read_image():
    with Image(filename="./data/Captchas/testCaptcha.png") as img:
        print(img.size)

        