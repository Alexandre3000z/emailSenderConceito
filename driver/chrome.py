from driver.driverConfig import ensure_chromedriver
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

import undetected_chromedriver as uc

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--lang=pt-BR")
    
    driver = uc.Chrome(options=options, version_main=149)
    return driver