from nextcaptcha import NextCaptchaAPI
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

# Set up Selenium WebDriver
driver = uc.Chrome()

# Navigate to the website
driver.get("https://skipthegames.com/reply/phone/190490348178")

# Find and click the button
button = driver.find_element(By.ID, "submit_post_request_email")
button.click()

# Wait for the CAPTCHA to appear
time.sleep(10)

# Solve the CAPTCHA
api = NextCaptchaAPI(client_key="next_49f953531e5072ab68967dab3dc5197999")
result = api.hcaptcha(website_url=driver.current_url, website_key="697b3626-2d5a-4a82-bd49-a70ecbe27091Y")

# Process the result
if result.get("status") == "ready":
    print(f"Captcha solved: {result.get('solution')}")
else:
    print(f"Failed to solve Captcha: {result.get('error')}")

# Close the WebDriver
driver.quit()