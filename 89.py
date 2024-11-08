import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import re
import subprocess

# List of posting URLs for different cities
posting_urls = [
    "https://skipthegames.com/posts/boston/female-escorts?ageMin=19&ageMax=21&area[]=BOS&heightType=f&psizeType=in&weightType=l",
    "https://skipthegames.com/posts/new-york-city/female-escorts?ageMin=19&ageMax=211&area[]=NY&heightType=f&psizeType=in&weightType=l",
    "https://skipthegames.com/posts/philadelphia/female-escorts?ageMin=19&ageMax=21&area[]=BOS&heightType=f&psizeType=in&weightType=l",
    "https://skipthegames.com/posts/houston/female-escorts?ageMin=19&ageMax=21&area[]=BOS&heightType=f&psizeType=in&weightType=l",
    "https://skipthegames.com/posts/dallas/female-escorts?ageMin=19&ageMax=21&area[]=BOS&heightType=f&psizeType=in&weightType=l",
]

# Initialize Chrome Driver
driver = uc.Chrome()

try:
    for posting_url in posting_urls:
        
        # Extract the city from the URL (e.g., "boston" or "new-york")
        city_match = re.search(r"/posts/([^/]+)/female-escorts", posting_url)
        city = city_match.group(1)
        
        # Navigate to the provided URL
        driver.get(posting_url)
        sleep(1)  # Allow time for the page to load

        # Click the "Single Photo" button to ensure the right view mode
        single_photo_button = driver.find_element(By.ID, "radio_clsfd_display_mode_single")
        single_photo_button.click()
        sleep(1)

        # Collect all ad links on the main page, with a limit of 30 unique URLs
        ad_links = driver.find_elements(By.CSS_SELECTOR, f"a[href^='/posts/{city}/female-escorts']")
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
