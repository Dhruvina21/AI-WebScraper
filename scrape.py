import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import service

def scrape_website(website):
    print("Launching chrome browser...")

    chrome_driver_path = ""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    
