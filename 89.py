import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# Prompt the user for the starting URL
start_url = input("Enter the URL of the page to start scraping: ")

# Initialize Chrome Driver
driver = uc.Chrome()

try:
    # Navigate to the provided URL
    driver.get(start_url)
    sleep(3)  # Allow time for the page to load

    # Click the "Single Photo" button to ensure the right view mode
    single_photo_button = driver.find_element(By.ID, "radio_clsfd_display_mode_single")
    single_photo_button.click()
    sleep(2)

    # Collect all ad links on the main page, with a limit of 30 unique URLs
    ad_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/posts/boston/female-escorts']")
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
        sleep(5)  # Wait for ad page to load

        # Press F1 to trigger the AutoHotkey script
        ActionChains(driver).send_keys("F1").perform()
        sleep(5)  # Allow time for the AutoHotkey script to process

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()  # Ensure the driver quits at the end
