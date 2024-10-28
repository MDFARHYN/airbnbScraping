import pandas as pd
import re
import time
import random
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Function to create proxy authentication extension
def create_proxy_auth_extension(proxy_host, proxy_user, proxy_pass):
    import zipfile
    import os

    # Separate the host and port
    host = proxy_host.split(':')[0]
    port = proxy_host.split(':')[1]

    # Define proxy extension files
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    
    background_js = f"""
    var config = {{
            mode: "fixed_servers",
            rules: {{
              singleProxy: {{
                scheme: "http",
                host: "{host}",
                port: parseInt({port})
              }},
              bypassList: ["localhost"]
            }}
          }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy_user}",
                    password: "{proxy_pass}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """

    # Create the extension
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return pluginfile


# Function to configure and return the WebDriver with proxy
def init_driver_with_proxy(proxy_server, proxy_username, proxy_password):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # Add proxy authentication if necessary
    if proxy_username and proxy_password:
        options.add_extension(create_proxy_auth_extension(proxy_server, proxy_username, proxy_password))

    # Stealth mode to avoid detection
    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    return driver


# Proxy pool for rotation (list of proxy servers)
proxy_pool = [
    {"proxy": "proxy1.com:8000", "username": "user1", "password": "pass1"},
    {"proxy": "proxy2.com:8000", "username": "user2", "password": "pass2"},
    {"proxy": "proxy3.com:8000", "username": "user3", "password": "pass3"}
   
]

# Function to scrape details page (rotate proxy on each request)
def scrape_details_page(url):
    try:
        # Rotate proxy by choosing a random one from the pool
        proxy = random.choice(proxy_pool)
        driver = init_driver_with_proxy(proxy['proxy'], proxy['username'], proxy['password'])

        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        html_content = driver.page_source

        # Regex pattern for scraping the title
        title_pattern = r'<h1[^>]+>([^<]+)<\/h1>'
    
        # Scrape the title  
        title = re.search(title_pattern,html_content)
        if title:
           title = title.group(1)
        else:
            title = None

        # Scrape the price  
        price_pattern = r'(\$\d+[^<]+)<\/span><\/span>[^>]+><\/div><\/div>'
        price = re.search(price_pattern,html_content)
    
        if price:
            price = price.group(1)
        else:
            price = None
        
        # Scrape the address  
        address_pattern = r'dir-ltr"><div[^>]+><section><div[^>]+ltr"><h2[^>]+>([^<]+)<\/h2>'
        address =  re.search(address_pattern,html_content)
        if address:
           address =  address.group(1)
        else:
            address = None

        # Scrape the guest  
        guest_pattern = r'<li class="l7n4lsf[^>]+>([^<]+)<span'
        guest =   re.search(guest_pattern,html_content)
        if guest:
           guest = guest.group(1)
        else:
            guest = None
        # You can add more information to scrape (example: price, description, etc.)
        
        # Scrape the bedrooms, bed, bath  details  
        bed_bath_pattern = r'<\/span>(\d+[^<]+)'
        bed_bath = re.findall(bed_bath_pattern,html_content)
        bed_bath_details = [] 
        if bed_bath:
            for bed_bath_info in bed_bath:
                bed_bath_details.append(bed_bath_info.strip())
       
        #scrape reviews such as Cleanliness, Accuracy, Communication etc.
        reviews_pattern = r'l1nqfsv9[^>]+>([^<]+)<\/div>[^>]+>(\d+[^<]+)<\/div>'
        reviews_details =  re.findall(reviews_pattern,html_content)
        review_list = []
        if reviews_details:
               for review in reviews_details:
                    attribute, rating = review  # Unpack the attribute and rating
                    review_list.append(f'{attribute} {rating}')  # Combine into a readable format

        #scrape host name
        host_name_pattern = r't1gpcl1t atm_w4_16rzvi6 atm_9s_1o8liyq atm_gi_idpfg4 dir dir-ltr[^>]+>([^<]+)'
        host_name =  re.search(host_name_pattern,html_content)
        if host_name:
           host_name = host_name.group(1)    
        else:
            host_name = None

        #scrape total number of review
        total_review_pattern = r'pdp-reviews-[^>]+>[^>]+>(\d+[^<]+)<\/span>'
        total_review =  re.search(total_review_pattern,html_content)
        if total_review:
           total_review =  total_review.group(1)    
        else:
            total_review = None

        #scrape host info
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


# List of URLs to scrape
url_list = ["https://www.airbnb.com/rooms/968367851365040114?adults=1&category_tag=Tag%3A8148&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1750644422&search_mode=regular_search&check_in=2025-01-18&check_out=2025-01-23&source_impression_id=p3_1729605408_P3X7GT0Ec98R7_ET&previous_page_section_name=1000&federated_search_id=62850efb-a8ab-4062-92ec-e9010fc6a24f"]  # Replace with actual URLs
scraped_data = []

# Scrape the details page for each URL with proxy rotation
for url in url_list:
    print(f"Scraping details from: {url}")
    data = scrape_details_page(url)
    if data:
        scraped_data.append(data)

# After scraping, save data to CSV
if scraped_data:
    save_to_csv(scraped_data)
else:
    print("No data to save.")
