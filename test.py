import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import re
import requests
from difflib import SequenceMatcher
import json
from pathlib import Path

def remove_emoji(text):
    """Remove emojis and special characters from text"""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags 
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

def calculate_similarity(text1, text2):
    """Calculate similarity ratio between two texts"""
    return SequenceMatcher(None, text1, text2).ratio()

def load_saved_texts():
    """Load previously saved texts from file"""
    try:
        with open('saved_texts.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_texts(texts):
    """Save texts to file"""
    with open('saved_texts.json', 'w') as f:
        json.dump(texts, f)

def is_similar_to_existing(new_text, saved_texts, similarity_threshold=0.9):
    """Check if new text is similar to any existing texts"""
    for entry in saved_texts:
        if calculate_similarity(new_text, entry['pageText']) >= similarity_threshold:
            print(f"Similar content found. Not sending to webapp. Similar to URL: {entry['url']}")
            return True
    return False

def process_page(driver, saved_texts):
    """Process the current page and send data to Google Apps Script if content is unique enough"""
    # Get URL using Selenium
    current_url = driver.current_url
    
    page_text = driver.execute_script("return document.body.innerText")
    
    # Clean the text
    page_text = remove_emoji(page_text)
    page_text = clean_text(page_text)

    print(f"Processing URL: {current_url}")
    
    # Check for similarity with existing texts
    if not is_similar_to_existing(page_text, saved_texts):
        # Prepare and send the data to Google Apps Script
        webapp_url = "https://script.google.com/macros/s/AKfycbxWgMjGw9fQ7cJ43SJNVXeDEf1tZzCnExQLvNuo0fyaZh2XRkwuaVknZLI-hnuO0-nRnw/exec"
        
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
            else:
                # Save new text only if successfully sent to webapp
                saved_texts.append(payload)
                save_texts(saved_texts)
                print(f"Successfully processed and saved: {current_url}")
        except Exception as e:
            print(f"Error sending data: {e}")
    
    return saved_texts

max_age = 25

# List of posting URLs for different cities
posting_urls = [
    f"https://skipthegames.com/posts/boston/female-escorts?ageMin=19&ageMax={max_age}&area[]=BOS&heightType=f&psizeType=in&weightType=l",
    f"https://skipthegames.com/posts/new-york-city/female-escorts?ageMin=19&ageMax={max_age}1&area[]=NY&heightType=f&psizeType=in&weightType=l",
    f"https://skipthegames.com/posts/philadelphia/female-escorts?ageMin=19&ageMax={max_age}&area[]=BOS&heightType=f&psizeType=in&weightType=l",
    f"https://skipthegames.com/posts/houston/female-escorts?ageMin=19&ageMax={max_age}&area[]=BOS&heightType=f&psizeType=in&weightType=l",
    f"https://skipthegames.com/posts/dallas/female-escorts?ageMin=19&ageMax={max_age}&area[]=BOS&heightType=f&psizeType=in&weightType=l",
]

driver = uc.Chrome()
saved_texts = load_saved_texts()

try:
    for posting_url in posting_urls:
        # Extract the city from the URL
        city_match = re.search(r"/posts/([^/]+)/female-escorts", posting_url)
        city = city_match.group(1)
        
        # Navigate to the provided URL
        driver.get(posting_url)
        sleep(2) # Change depending on internet speed

        # Collect all ad links
        ad_links = driver.find_elements(By.CSS_SELECTOR, f"a[href^='/posts/{city}/female-escorts']")
        ad_urls = set()
        
        for ad in ad_links:
            ad_url = ad.get_attribute("href")
            if ad_url not in ad_urls:
                ad_urls.add(ad_url)
            if len(ad_urls) >= 30:  # Scrapes 30 at a time
                break
                
        # Visit each unique ad page
        for ad_url in ad_urls:
            driver.get(ad_url)
            sleep(2)  # Change depending on internet speed
            saved_texts = process_page(driver, saved_texts)
            sleep(1)  # Change depending on internet speed

except Exception as e:
    print("An error occurred:", e)
finally:
    driver.quit()