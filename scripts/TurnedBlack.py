import requests
from bs4 import BeautifulSoup
import json

# URL to scrape
url = "https://www.turnblack.in/product/nylah-co-ord-set/"

# Send a GET request to the URL
response = requests.get(url)
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Initialize a dictionary to hold the scraped data
    data = {
        "title": "",
        "images": [],
        "product_description": "",
        "price": "",
        "sku": "",
        "categories": []
    }
    
    # Find the element with class name "product_title entry-title"
    product_title = soup.find(class_="product_title entry-title")
    if product_title:
        data["title"] = product_title.get_text(strip=True)
    else:
        data["title"] = "Product title not found."
    
    # Find all elements with class name "wp-post-image"
    images = soup.find_all(class_="wp-post-image")
    for img in images:
        img_url = img['src']  # Assuming the image URL is in the 'src' attribute
        data["images"].append(img_url)
    
    # Find the element with class name "woocommerce-product-details__short-description"
    product_description = soup.find(class_="woocommerce-product-details__short-description")
    if product_description:
        description_text = product_description.get_text(strip=True)
        data["product_description"] = description_text
    else:
        data["product_description"] = "Product description not found."
    
    # Find the element with class name "woocommerce-Price-amount amount"
    product_price = soup.find(class_="woocommerce-Price-amount amount")
    if product_price:
        data["price"] = product_price.get_text(strip=True)
    else:
        data["price"] = "Price not found."
    
    # Find the SKU and categories in the product meta
    product_meta = soup.find(class_="product_meta")
    
    # Find the SKU
    sku = product_meta.find(class_="sku")
    if sku:
        data["sku"] = sku.get_text(strip=True)
    else:
        data["sku"] = "SKU not found."
    
    # Find the categories
    categories = product_meta.find(class_="posted_in")
    if categories:
        category_links = categories.find_all("a")
        data["categories"] = [category.get_text(strip=True) for category in category_links]
    else:
        data["categories"] = ["Categories not found."]
    
    # Write the data to a JSON file
    with open('scraped_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    
    print("Data successfully scraped and stored in scraped_data.json")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")