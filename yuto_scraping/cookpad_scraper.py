import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import pandas as pd
import time

# function to get BeautifulSoup object from a given URL
def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"error fetching {url}: {e}")
        return None

# function to save data to a CSV file
def save_to_csv(csv_path, csv_data, header):
    try:
        # read existing data from CSV file if it exists, otherwise create an empty DataFrame
        existing_data = pd.read_csv(csv_path, encoding='utf-8_sig') if os.path.exists(csv_path) else pd.DataFrame(columns=header)
        # concatenate existing data with new data and write to the CSV file
        csv_data = pd.concat([existing_data, csv_data], ignore_index=True)
        csv_data.to_csv(csv_path, index=False, encoding='utf-8_sig')
    except UnicodeEncodeError as e:
        print(f"error encoding CSV: {e.reason}")

# function to process a single recipe page
def process_page(url):
    soup = get_soup(url)
    if not soup:
        return
    
    # extract recipe ID from the URL
    recipe_id = url.split("/")[-1]
    material_csv_path = 'materials.csv'
    # define headers for the CSV file
    material_header = ["recipe_id"] + [f"veg_{i}" for i in range(1, 6)] + ["category"] + [f"material_{i}" for i in range(1, 31)]
    material_new_data = pd.DataFrame([[recipe_id]], columns=["recipe_id"])

    # extract material names from the page and save to CSV
    name_elements = soup.find_all('span', class_='name')
    for i, name_element in enumerate(name_elements, start=1):
        names = name_element.text.strip()
        material_new_data[f"material_{i}"] = names

    save_to_csv(material_csv_path, material_new_data, material_header)

# function to navigate to the next page and get its BeautifulSoup object
def next_page(load_url, soup):
    next_page_element = soup.find(class_="center paginate").find_all("a")[-1]
    url = urljoin(load_url, next_page_element.get("href"))
    return get_soup(url), url

# main execution block
if __name__ == "__main__":
    # input for the number of pages to retrieve
    repeat_count = int(input("please enter how many pages you would like to retrieve: "))
    load_url = "https://cookpad.com/search/%E5%92%8C%E9%A3%9F"
    soup = get_soup(load_url)

    # loop through the specified number of pages
    for _ in range(repeat_count):
        topic = soup.find(class_="recipe-list")
        # process each recipe link on the current page
        for j, element in enumerate(topic.find_all("a"), start=1):
            url = urljoin(load_url, element.get("href"))

            # process the page if it is a recipe page (URL structure check) and the element index is even
            if url.split("/")[3] == 'recipe' and j % 2 == 0:
                process_page(url)

        # move to the next page and introduce a delay to avoid overloading the server
        soup, load_url = next_page(load_url, soup)
        time.sleep(1)
    print("end of scraping")
