import json
from pathlib import Path
from difflib import SequenceMatcher
import os

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
        similarity = calculate_similarity(new_text, entry['pageText'])
        print(f"Similarity with {entry['url']}: {similarity:.2%}")
        if similarity >= similarity_threshold:
            print(f"Similar content found. Would not send to webapp. Similar to URL: {entry['url']}")
            return True
    return False

def test_similarity_checking():
    # Clear any existing saved_texts.json
    if os.path.exists('saved_texts.json'):
        os.remove('saved_texts.json')
    
    saved_texts = []
    
    # Test Case 1: Completely different texts
    print("\nTest Case 1: Different Texts")
    text1 = {
        "url": "http://example.com/1",
        "pageText": "Owen wang is a very smart invidual who is extremely smart. This guy is smart."
    }
    text2 = {
        "url": "http://example.com/2",
        "pageText": "Owen wang is a very smart invidual who is extremely dumb. This guy is smart."
    }
    
    print("Processing first text...")
    if not is_similar_to_existing(text1['pageText'], saved_texts):
        saved_texts.append(text1)
        save_texts(saved_texts)
        print("Text 1 saved successfully")
    
    print("\nProcessing second text...")
    if not is_similar_to_existing(text2['pageText'], saved_texts):
        saved_texts.append(text2)
        save_texts(saved_texts)
        print("Text 2 saved successfully")
    
    # Test Case 2: Very similar texts (95% similar)
    print("\nTest Case 2: Similar Texts")
    text3 = {
        "url": "http://example.com/3",
        "pageText": "Hello this is a test message about dogs and cats in the park"
    }
    
    print("Processing similar text...")
    if not is_similar_to_existing(text3['pageText'], saved_texts):
        saved_texts.append(text3)
        save_texts(saved_texts)
        print("Text 3 saved successfully")
    else:
        print("Text 3 was not saved due to similarity")
    
    # Test Case 3: Identical text
    print("\nTest Case 3: Identical Text")
    text4 = {
        "url": "http://example.com/4",
        "pageText": "Hello this is a test message about dogs and cats"
    }
    
    print("Processing identical text...")
    if not is_similar_to_existing(text4['pageText'], saved_texts):
        saved_texts.append(text4)
        save_texts(saved_texts)
        print("Text 4 saved successfully")
    else:
        print("Text 4 was not saved due to similarity")
    
    # Test Case 4: Text with slight differences
    print("\nTest Case 4: Slightly Different Text")
    text5 = {
        "url": "http://example.com/5",
        "pageText": "Hello this is a test message about dogs and cats and birds"
    }
    
    print("Processing slightly different text...")
    if not is_similar_to_existing(text5['pageText'], saved_texts):
        saved_texts.append(text5)
        save_texts(saved_texts)
        print("Text 5 saved successfully")
    else:
        print("Text 5 was not saved due to similarity")
    
    # Print final saved texts
    print("\nFinal saved texts:")
    with open('saved_texts.json', 'r') as f:
        final_texts = json.load(f)
        for i, text in enumerate(final_texts, 1):
            print(f"\nText {i}:")
            print(f"URL: {text['url']}")
            print(f"Content: {text['pageText']}")

if __name__ == "__main__":
    test_similarity_checking()