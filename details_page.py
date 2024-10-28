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





# function to scrape information from a details page (title, price, etc.)
def scrape_details_page(url):
    try:
        driver.get(url)
        # Wait for the page to load (you can adjust this)
        time.sleep(2)
        html_content = driver.page_source
        scroll_to_bottom()
        time.sleep(2) 
        # Regex pattern for scraping the title
        title_pattern = r'<h1[^>]+>([^<]+)<\/h1>'
    
        # Scrape the title (adjust the selector according to the page structure)
        title = re.search(title_pattern,html_content)
        if title:
           title = title.group(1)
        else:
            title = None
        
        price_pattern = r'(\$\d+[^<]+)<\/span><\/span>[^>]+><\/div><\/div>'
        price = re.search(price_pattern,html_content)
    
        if price:
            price = price.group(1)
        else:
            price = None

        address_pattern = r'dir-ltr"><div[^>]+><section><div[^>]+ltr"><h2[^>]+>([^<]+)<\/h2>'
        address =  re.search(address_pattern,html_content)
        if address:
           address =  address.group(1)
        else:
            address = None
        
        guest_pattern = r'<li class="l7n4lsf[^>]+>([^<]+)<span'
        guest =   re.search(guest_pattern,html_content)
        if guest:
           guest = guest.group(1)
        else:
            guest = None
        # You can add more information to scrape (example: price, description, etc.)
        
        bed_bath_pattern = r'<\/span>(\d+[^<]+)'
        bed_bath = re.findall(bed_bath_pattern,html_content)
        bed_bath_details = [] 
        if bed_bath:
            for bed_bath_info in bed_bath:
                bed_bath_details.append(bed_bath_info.strip())
        
        reviews_pattern = r'l1nqfsv9[^>]+>([^<]+)<\/div>[^>]+>(\d+[^<]+)<\/div>'
        reviews_details =  re.findall(reviews_pattern,html_content)
        review_list = []
        if reviews_details:
               for review in reviews_details:
                    attribute, rating = review  # Unpack the attribute and rating
                    review_list.append(f'{attribute} {rating}')  # Combine into a readable format


        host_name_pattern = r't1gpcl1t atm_w4_16rzvi6 atm_9s_1o8liyq atm_gi_idpfg4 dir dir-ltr[^>]+>([^<]+)'
        host_name =  re.search(host_name_pattern,html_content)
        if host_name:
           host_name = host_name.group(1)    
        else:
            host_name = None

        total_review_pattern = r'pdp-reviews-[^>]+>[^>]+>(\d+[^<]+)<\/span>'
        total_review =  re.search(total_review_pattern,html_content)
        if total_review:
           total_review =  total_review.group(1)    
        else:
            total_review = None


        host_info_pattern = r'd1u64sg5[^"]+atm_67_1vlbu9m dir dir-ltr[^>]+><div><span[^>]+>([^<]+)'
        host_info = re.findall(host_info_pattern,html_content)
        host_info_list = []
        if host_info:
            for host_info_details in host_info:
                 host_info_list.append(host_info_details)
        
        # Print the scraped information (for debugging purposes)
        print(f"Title: {title}\n Price:{price}\n Address: {address}\n Guest: {guest}\n bed_bath_details:{bed_bath_details}\n Reviews: {review_list}\n Host_name: {host_name}\n total_review: {total_review}\n Host Info: {host_info_list}\n ")
        
        # Return the information as a dictionary (or adjust based on your needs)
          # Store the scraped information in a dictionary
        return {
            "url": url,
            "Title": title,
            "Price": price,
            "Address": address,
            "Guest": guest,
            "Bed_Bath_Details": bed_bath_details,
            "Reviews": review_list,
            "Host_Name": host_name,
            "Total_Reviews": total_review,
            "Host_Info": host_info
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


# Function to save data to CSV using pandas
def save_to_csv(data, filename='airbnb_data.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")



scraped_data = []


# Scrape the details page for each URL stored in the url_list  
for url in url_list[:5]:
    print(f"Scraping details from: {url}")
    data = scrape_details_page(url)
    if data:
        scraped_data.append(data)
     

# After scraping, save data to CSV
if scraped_data:
    save_to_csv(scraped_data)
else:
    print("No data to save.")

# Close the browser
driver.quit()
    





 