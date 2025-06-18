import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import service
import time

def scrape_website(website):
    print("Launching chrome browser...")

    chrome_driver_path = ""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        #use our webdriver to get to this specific website
        driver.get(website)
        print("Page loaded...")
        html = driver.page_source
        time.sleep(10)

        return html
    finally:
        driver.quit()


    
