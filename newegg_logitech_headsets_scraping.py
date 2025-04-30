import requests
import random
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

'''
We will scrape the newegg website for logitech gaming headsets 
Steps: 
1. Scrape search page for product links
2. Visit each product link and scrape the
'''

base_url = "https://www.newegg.com/p/pl?d=logitech+gaming+headset&PageSize=96&page="

# Define multiple headers to rotate between to avoid getting blocked
ua = UserAgent()
links_list = []

# Scrape search page for product links of all products that are not 'refurbished'
for page_num in range(1, 4):
    search_url = base_url + str(page_num)

    headers = {
        "User-Agent": ua.random,
        "Referrer": "https://www.newegg.com/" 
    }

    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser') # Parse html 
        
        # Loop through each product listed on the page and extract the links
        products = soup.find_all("div", class_="item-cell")

        for product in products: 
            
            refurbished_tag = product.find("div", class_="section-subtitle-text", string="Refurbished")
            
            if refurbished_tag:
                continue # skip refurbished products

            link_tag = product.find("a", class_="item-title")

            if link_tag:
                links_list.append(link_tag["href"])


for link in links_list:
    
    response = requests.get(link, headers=headers)

    # Scrape each product page for image_url, title, price, brand, model, rating, 
    # color, compatibility, connectivity (wired/wireless)
    # Note: Use find/find_all for items stored in tags with classes;
    # brand/model are stored inside tables so we need to find the table and read row by row
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Image URL
        img_tag = soup.find("img", class_="product-view-img-original")
        img_url = img_tag["src"] if img_tag else None
        print(f"Image URL: {img_url}")
        
        # Product Title
        title = soup.find("h1", class_="product-title").text.strip()
        print(f"Title: {title}")

        # Price
        price_tag = soup.find("div", class_="price-current")
        price = "" # create empty string to store price value -- if none = "none"
        if price_tag:
            price = price_tag.strong.text.strip() + price_tag.sup.text.strip() if price_tag.strong else price_tag.text.strip()
        print(f"Price: {price}")

        # Brand and Model are stored in a table for each product page
        model_table = soup.find('caption', string="Model")
        if model_table: 

            model_table = model_table.find_parent('table')
            model_rows = model_table.find_all('tr')

            for row in model_rows:
                header = row.find('th').text.strip() if row.find('th') else "No header"
                value = row.find('td').text.strip() if row.find('td') else "No value"

                print(f"{header}: {value}")
                
        else:
            print("Model caption not found")

        rating_tag = soup.find("i", class_="rating")
        rating = rating_tag["title"].split(" out")[0] if rating_tag else "No ratings"
        print(f"Rating: {rating}")

        reviews_tag = soup.find("span", class_="item-rating-num")
        reviews = reviews_tag.text.strip("()") if reviews_tag else "No reviews"
        print(f"Number of Reviews: {reviews}")

        # Compatibiity, Color, LED, Operating time are sotored in Details table
        details_table = soup.find('caption', string="Details")
        if details_table: 

            details_table = details_table.find_parent('table')
            details_rows = details_table.find_all('tr')

            for row in details_rows:
                header = row.find('th').text.strip() if row.find('th') else "No header"
                value = row.find('td').text.strip() if row.find('td') else "No value"

                print(f"{header}: {value}")

        else:
            print("Details caption not found")

        # Connection type, connector, wireless type, wireless range found in Connectivity Table

        connectivity_table = soup.find('caption', string="Connectivity")
        if connectivity_table: 

            connectivity_table = connectivity_table.find_parent('table')
            connectivity_rows = connectivity_table.find_all('tr')

            for row in connectivity_rows:
                header = row.find('th').text.strip() if row.find('th') else "No header"
                value = row.find('td').text.strip() if row.find('td') else "No value"

                print(f"{header}: {value}")

        else:
            print("Connectivity caption not found")



        # Headphone table

        headphone_table = soup.find('caption', string="Headphone")
        if headphone_table: 

            headphone_table = headphone_table.find_parent('table')
            headphone_rows = headphone_table.find_all('tr')

            for row in headphone_rows:
                header = row.find('th').text.strip() if row.find('th') else "No header"
                value = row.find('td').text.strip() if row.find('td') else "No value"

                print(f"{header}: {value}")

        else:
            print("Headphone caption not found")

        # Microphone Table

        microphone_table = soup.find('caption', string="Microphone")
        if microphone_table: 

            microphone_table = microphone_table.find_parent('table')
            microphone_rows = microphone_table.find_all('tr')

            for row in microphone_rows:
                header = row.find('th').text.strip() if row.find('th') else "No header"
                value = row.find('td').text.strip() if row.find('td') else "No value"

                print(f"{header}: {value}")

        else:
            print("Microphone caption not found")