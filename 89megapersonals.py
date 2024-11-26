from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import re
import subprocess

# List of posting URLs for different cities
posting_urls = [
    "https://megapersonals.eu/public/post_list/7/2/1"
]

# Initialize Chrome Driver
chrome_driver_path = "C:\\Users\\nyter\\Desktop\\Scraper\\chromedriver-win64\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:/Users/nyter/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument('profile-directory=Profile 1')
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    for posting_url in posting_urls:
        
        # Navigate to the provided URL
        driver.get(posting_url)
        sleep(1)  # Allow time for the page to load

        # Collect all ad links on the main page, with a limit of 30 unique URLs
        ad_links = driver.find_elements(By.CSS_SELECTOR, "a.listtitle")
        ad_urls = set()  # Use a set to remove duplicates
        for ad in ad_links:
            ad_url = ad.get_attribute("href")
            if ad_url not in ad_urls:
                ad_urls.add(ad_url)
            if len(ad_urls) >= 30:  # Limit to 30 listings
                break

        # Visit each unique ad page
        for ad_url in ad_urls:
            driver.get(ad_url)  # Navigate to the ad URL
            sleep(2)  # Wait for ad page to load

            # Press F1 to trigger the AutoHotkey script
            subprocess.Popen([r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe", r"C:\Users\nyter\Desktop\P89\89.ahk"])
            sleep(1.5)  # Allow time for the AutoHotkey script to process

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()  # Ensure the driver quits at the end
