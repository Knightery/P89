from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time

chrome_driver_path = "C:\\Users\\nyter\\Desktop\\Scraper\\chromedriver-win64\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:/Users/nyter/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument('profile-directory=Profile 1')
service = Service(chrome_driver_path)
try:
    # Initialize the WebDriver only once
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the target website
    driver.get("https://privatedelights.ch/USA/New-York/New-York/")

    # Wait for the page to load
    time.sleep(3)
    
    try:
        show_more_button = driver.find_element(By.XPATH, "//button[.//span[text()='Show more filters']]")
        show_more_button.click()
        time.sleep(0.5)
    except Exception as e:
        print("Failed to click 'Show more filters' button:", e)
    
    time.sleep(2)

    try:
        dropdown = driver.find_element(By.XPATH, "//label[text()='Age from']/following::div[contains(@class, 'v-select__slot')]")
        dropdown.click()
    except Exception as e:
        print("Failed to click 'Age from' dropdown:", e)

    time.sleep(2)

    try:
        option_18 = driver.find_element(By.XPATH, "//div[contains(text(), '21')]")
        option_18.click()
    except Exception as e:
        print("Failed to click 18:", e)

    time.sleep(5)
    
except Exception as e:
    print(f"Error occurred: {e}")