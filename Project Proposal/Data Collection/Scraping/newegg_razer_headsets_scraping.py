import requests
import random
import time
import json

from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# Get the page content
base_url = "https://www.newegg.com/p/pl?d=razer+gaming+headset&PageSize=96&N=50002202%2050116902"

# Define multiple headers to rotate between to avoid getting blocked
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/121.0.0.0 Chrome/121.0.6167.140 Safari/537.36"
]
cookies = {
    "MUID":"1BD6C235741868883176D19475F6695A"

    
}

links_list = []
product_data = []

# Define a function to scrape tables from each product page/link
# include soup 
def scrape_table(table_caption, soup):
    table = soup.find('caption', string=table_caption)
                
    table_data = {}  
    
    if table:
        table = table.find_parent('table')
        rows = table.find_all('tr')

        for row in rows:
            header = row.find('th').text.strip() if row.find('th') else "No header"
            value = row.find('td').text.strip() if row.find('td') else "No value"

            table_data[header] = value

        return table_data
                
    else:
        print(f"{table_caption} caption not found")
        
# Scrape search page for product links of all products that are not 'refurbished'
# for page_num in range(1,4): 

search_url = base_url
page_num = 1

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept": "application/x-clarity-gzip",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.newegg.com/p/pl?d=razer+gaming+headset&PageSize=96&N=50002202%2050116902",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}

try:

    response = requests.get(search_url, headers=headers, cookies=cookies)
    response.raise_for_status()
    response.encoding = 'utf-8' 
    print(response.headers)
    print(response.text[:500]) 

    content_encoding = response.headers.get('Content-Encoding', '')


    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser') # Parse html 
        
        # Loop through each product listed on the page and extract the links
        products = soup.find_all("div", class_="item-cell")

        for product in products:  

            link_tag = product.find("a", class_="item-title")
            if link_tag:
                title = link_tag.text.strip()

                if "refurbished" in title.lower() or "replacement" in title.lower() or "used" in title.lower() or "mouse" in title.lower() or "keyboard" in title.lower() or "seiren" in title.lower() or "leviathan" in title.lower():
                    print(f"Skipping: {title} (Refurbished/Replacement/Used/Mouse/Keyboard/Seiren)")
                    continue

                # Only include titles that have "headset" 
                if "headset" in title.lower():
                    product_info = {
                        "title": title,
                        "url": link_tag["href"],
                        "page_num": page_num # store page number to use in referral link again in second loop
                    }
                    product_data.append(product_info)

        print(f"Page {page_num} scraped successfully")
    
    else:
        print(f"Failed to retrieve page {page_num}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching {search_url}: {e}")

time.sleep(random.uniform(3, 10)) # add a random delay to avoid website detection

with open('razer_product_links.json', 'w') as f:
    json.dump(product_data, f, indent=4)

print(f"Total products found: {len(product_data)}") # check to see how many products were found

total_products = len(product_data)

# Scrape each product page for product info
for index, product in enumerate(product_data, start=1): 
    link = product['url']
    page_num = product.get('page_num', 1)

    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept": "application/x-clarity-gzip",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.newegg.com/p/pl?d=razer+gaming+headset&PageSize=96&N=50002202%2050116902",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1"
    }

    try: 
        
        print(f"Scraping product {index}/{total_products}") # prints progress
        
        response = requests.get(link, headers=headers, cookies=cookies)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        # Scrape each product page for image_url, title, price, brand, model, rating, 
        # color, compatibility, connectivity (wired/wireless)
        # Note: Use find/find_all for items stored in tags with classes;
        # brand/model are stored inside tables so we need to find the table and read row by row
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # DEBUGGING
            print(soup.prettify())  

            # Image URL
            img_tag = soup.find("img", class_="product-view-img-original")
            img_url = img_tag["src"] if img_tag else None
            
            # Product Title
            title_tag = soup.find("h1", class_="product-title")
            if title_tag:
                title = title_tag.text.strip()
                print(f"Scraping: {title}") # DEBUGGING 
            else:
                print("Product title not found")
            
            # Price
            price_tag = soup.find("div", class_="price-current")
            price = "" # create empty string to store price value -- if none = "none"
            if price_tag:
                price = price_tag.strong.text.strip() + price_tag.sup.text.strip() if price_tag.strong else price_tag.text.strip()

            # Rating
            rating_tag = soup.find("i", class_="rating")
            if rating_tag and rating_tag.get("title"):
                rating = rating_tag["title"].split(" out")[0] 
            else:
                rating = "No ratings"

            # Reviews
            reviews_tag = soup.find("span", class_="item-rating-num")
            reviews = reviews_tag.text.strip("()") if reviews_tag else "No reviews"
            
            # Scrape tables 
            model_table = scrape_table("Model", soup)
            details_table = scrape_table("Details", soup)
            connectivity_table = scrape_table("Connectivity", soup)
            headphone_table = scrape_table("Headphone", soup)
            microphone_table = scrape_table("Microphone", soup)

            # Define dictionary to store all scraped product info/details

            product_info = {
                "title": title,
                "url": link,
                "img_url": img_url,
                "price": price,
                "rating": rating,
                "reviews": reviews,
                "model_table": model_table,
                "details_table": details_table,
                "connectivity_table": connectivity_table,
                "headphone_table": headphone_table,
                "microphone_table": microphone_table
            }

            # add product info to the links list 
            for prod in product_data:
                if prod["url"] == link:
                    prod.update(product_info)
            
            if index % 10 == 0:
                with open('razer_product_data.json', 'w', encoding="utf-8") as f:
                    json.dump(product_data, f, ensure_ascii=False, indent=4)
            
            print(f"Product {index}/{total_products} scraped and data saved.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {link}: {e}")
        
    time.sleep(random.uniform(5, 20)) # add random time delay between 1s to 5s

with open('razer_product_data.json', 'w', encoding="utf-8") as f:
    json.dump(product_data, f, ensure_ascii=False, indent=4)

print("All products scraped and data saved to 'razer_product_data.json'.")