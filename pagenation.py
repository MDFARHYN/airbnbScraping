from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

# Stealth setup to avoid detection
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

# Function to scrape the current page and return all property URLs
def scrape_current_page():
    html_content = driver.page_source
    url_pattern = 'labelledby="[^"]+" href="(\/rooms\/\d+[^"]+)"'
    urls = re.findall(url_pattern, html_content)
    return urls

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Give time for the page to load additional content

# Function to wait for the "Next" button and click it
def go_to_next_page():
    try:
        # Wait until the "Next" button is clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next']"))
        )
        scroll_to_bottom()  # Scroll to the bottom of the page before clicking
        next_button.click()
        return True
    except Exception as e:
        print(f"Couldn't navigate to next page: {e}")
        return False

# base url
url = "https://www.airbnb.com/s/United-States/homes?flexible_trip_lengths%5B%5D=one_week&date_picker_type=flexible_dates&place_id=ChIJCzYy5IS16lQRQrfeQ5K5Oxw&refinement_paths%5B%5D=%2Fhomes&search_type=AUTOSUGGEST"
driver.get(url)

# Ask the user how many pages to scrape
num_pages = int(input("How many pages do you want to scrape? "))

url_list = []  # Storing all URLs in a Python list

# Scrape the specified number of pages
for page in range(num_pages):
    print(f"Scraping page {page + 1}...")
    
    # Scrape URLs from the current page
    urls = scrape_current_page()
    for url in urls:
        details_page_url = "https://www.airbnb.com" + url
        print(details_page_url)  # Print extracted URLs
        url_list.append(details_page_url)
    
    # Try to go to the next page
    if not go_to_next_page():
        break  # If there's no "Next" button or an error occurs, stop the loop
    
    # Wait for the next page to load
    time.sleep(3)

# After scraping is complete, print the total number of URLs
print(f"Total URLs scraped: {len(url_list)}")


# Close the browser
driver.quit()
    





 