import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import re
import json
import requests

def remove_emoji(text):
    """Remove emojis and special characters from text"""
    # Remove emojis and special characters
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def clean_text(text):
    """Clean text for JSON compatibility"""
    # Replace special characters
    text = text.replace('"', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('-', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('+', ' ')
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32)
    
    # Remove multiple spaces
    text = ' '.join(text.split())
    
    return text.strip()

def process_page(driver):
    """Process the current page and send data to Google Apps Script"""
    # Get URL using Selenium
    current_url = driver.current_url
    
    # Get page text using Selenium
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
    sleep(0.05)
    actions.key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform()
    sleep(0.05)
    
    # Get text from clipboard using Selenium's execute_script
    page_text = driver.execute_script("""
        const textarea = document.createElement('textarea');
        document.body.appendChild(textarea);
        textarea.focus();
        document.execCommand('paste');
        const text = textarea.value;
        document.body.removeChild(textarea);
        return text;
    """)
    
    # Clean the text
    page_text = remove_emoji(page_text)
    page_text = clean_text(page_text)
    
    # Prepare and send the data to Google Apps Script
    webapp_url = "https://script.google.com/macros/s/AKfycbz6J-pC0yip_5l7U_rdpanmr2fi19NvRvMbRGFiROxW0OzinP3RFgNYGzwjA8393wjY4g/exec"
    
    payload = {
        "url": current_url,
        "pageText": page_text
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(webapp_url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Error sending data: Status code {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")

# List of posting URLs for different cities
posting_urls = [
    "https://skipthegames.com/posts/boston/female-escorts?ageMin=19&ageMax=21&area[]=BOS&heightType=f&psizeType=in&weightType=l",
    "https://skipthegames.com/posts/new-york-city/female-escorts?ageMin=19&ageMax=211&area[]=NY&heightType=f&psizeType=in&weightType=l",
    "https://skipthegames.com/posts/philadelphia/female-escorts?ageMin=19&ageMax=21&area[]=BOS&heightType=f&psizeType=in&weightType=l",
    "https://skipthegames.com/posts/houston/female-escorts?ageMin=19&ageMax=21&area[]=BOS&heightType=f&psizeType=in&weightType=l",
    "https://skipthegames.com/posts/dallas/female-escorts?ageMin=19&ageMax=21&area[]=BOS&heightType=f&psizeType=in&weightType=l",
]

# Initialize Chrome Driver
driver = uc.Chrome(headless=True)

try:
    for posting_url in posting_urls:
        # Extract the city from the URL
        city_match = re.search(r"/posts/([^/]+)/female-escorts", posting_url)
        city = city_match.group(1)
        
        # Navigate to the provided URL
        driver.get(posting_url)
        sleep(1)  # Allow time for the page to load
        
        # Click the "Single Photo" button
        single_photo_button = driver.find_element(By.ID, "radio_clsfd_display_mode_single")
        single_photo_button.click()
        sleep(1)
        
        # Collect all ad links
        ad_links = driver.find_elements(By.CSS_SELECTOR, f"a[href^='/posts/{city}/female-escorts']")
        ad_urls = set()
        
        for ad in ad_links:
            ad_url = ad.get_attribute("href")
            if ad_url not in ad_urls:
                ad_urls.add(ad_url)
            if len(ad_urls) >= 30:  # Limit to 30 listings
                break
                
        # Visit each unique ad page
        for ad_url in ad_urls:
            driver.get(ad_url)
            sleep(2)  # Wait for page to load
            process_page(driver)
            sleep(1.5)  # Wait between processing pages

except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()