import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# Initialize Chrome Driver
driver = uc.Chrome()

try:
    # Navigate to the main page with ads
    driver.get("https://skipthegames.com/posts/boston/female-escorts?ageMin=19&ageMax=20&area[]=BOS&heightType=f&psizeType=in&weightType=l")
    sleep(3)  # Allow time for the page to load

    # Click the "Single Photo" button to ensure the right view mode
    single_photo_button = driver.find_element(By.ID, "radio_clsfd_display_mode_single")
    single_photo_button.click()
    sleep(2)

    # Collect all ad links on the main page
    ad_links = driver.find_elements(By.CSS_SELECTOR, "a[href^='/posts/boston/female-escorts']")
    ad_urls = [ad.get_attribute("href") for ad in ad_links]

    # Visit each ad page
    for ad_url in ad_urls:
        driver.get(ad_url)  # Navigate to the ad URL
        sleep(1)  # Wait for ad page to load

        # Press F1 to trigger the AutoHotkey script
        ActionChains(driver).send_keys("F1").perform()
        sleep(1)  # Allow time for the AutoHotkey script to process

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()  # Ensure the driver quits at the end
