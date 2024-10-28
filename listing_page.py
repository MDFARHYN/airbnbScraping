from selenium import webdriver
from selenium_stealth import stealth
import time
import re 

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


# base url or page1 url
url = "https://www.airbnb.com/s/United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-11-01&monthly_length=3&monthly_end_date=2025-02-01&price_filter_input_type=0&channel=EXPLORE&query=United%20States&place_id=ChIJCzYy5IS16lQRQrfeQ5K5Oxw&date_picker_type=calendar&source=structured_search_input_header&search_type=user_map_move&search_mode=regular_search&price_filter_num_nights=5&ne_lat=78.7534545389953&ne_lng=17.82560738379206&sw_lat=-36.13028852123955&sw_lng=-124.379810004604&zoom=2.613816079556603&zoom_level=2.613816079556603&search_by_map=true"
driver.get(url)


# Fetch and print the page source
html_content = driver.page_source
#print(html_content)


# Define a regex pattern to capture all property URLs from listing pages
url_pattern = 'labelledby="[^"]+" href="(\/rooms\/\d+[^"]+)"'

# Find all matching URLs in the HTML content
urls = re.findall(url_pattern, html_content)
print(len(urls))

 
url_list = [] #Storing all URLs in a Python list

for url in urls:
    details_page_url =  "https://www.airbnb.com"+url
    print(details_page_url) # Print extracted URLs
    url_list.append(details_page_url)




 
driver.quit()