from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import subprocess

chrome_driver_path = "C:\\Users\\nyter\\Desktop\\Scraper\\chromedriver-win64\\chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=C:/Users/nyter/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument('profile-directory=Profile 1')
service = Service(chrome_driver_path)
base_url = "https://www.privatedelights.ch/USA"

# Define the list of state and city paths to visit
locations = [
    "Illinois/Chicago/",
    "New-York/New-York/",
    "California/Los-Angeles/",
    # Add more state/city paths as needed
]
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    for location in locations:
        full_url = f"{base_url}/{location}"
        driver.get(full_url)
        time.sleep(3)  # Adjust this sleep time based on page load speed

        try:
            show_more_button = driver.find_element(By.XPATH, "//button[.//span[text()='Show more filters']]")
            show_more_button.click()
            time.sleep(0.5)
        except Exception as e:
            print("Failed to click 'Show more filters' button:", e)
        
        try:
            dropdown = driver.find_element(By.XPATH, "//label[text()='Age from']/following::div[contains(@class, 'v-select__slot')]")
            dropdown.click()
            time.sleep(0.2)
        except Exception as e:
            print("Failed to click 'Age from' dropdown:", e)

        try:
            agemax = driver.find_element(By.XPATH, "//div[contains(text(), '21')]")
            agemax.click()
            time.sleep(0.2)
        except Exception as e:
            print("Failed to click 21:", e)

        try:
            search_button = driver.find_element(By.XPATH, "//div[@class='v-btn__content' and text()='Search']/..")
            search_button.click()
            time.sleep(4)  # Allow time for search results to load
        except Exception as e:
            print("Failed to click 'Search' button:", e)

        # Collect ad links for the current page based on the specific location
        ad_links = driver.find_elements(By.CSS_SELECTOR, f"a[href*='/USA/{location}']")
        ad_urls = set()

        for ad in ad_links:
            ad_url = ad.get_attribute("href")
            if ad_url not in ad_urls:
                ad_urls.add(ad_url)
            if len(ad_urls) >= 30:  # Limit to 30 listings
                break
        
        # Visit each unique ad page
        for ad_url in ad_urls:
            try:
                driver.get(ad_url)
                time.sleep(2)
                subprocess.Popen([r"C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe", r"C:\Users\nyter\Desktop\P89\89.ahk"])
                time.sleep(1)
            except Exception as e:
                print(f"Failed to load ad URL {ad_url}: {e}")

except Exception as e:
    print(f"Failed to load {full_url}: {e}")
finally:
    driver.quit()
