import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# import os
# import pandas as pd
# import time

def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"error fetching {url}: {e}")
        return None

if __name__ == "__main__":
    #データの件数を入力:
    # repeat_count = 50
    #読み込みURL
    load_url = "https://crowdworks.jp/public/jobs?ref=public_header"
    soup = get_soup(load_url)
    topic = soup.find(id_="NKcON")
    print(topic)
    for j, element in enumerate(topic.find_all("a"), start=1):
        url = urljoin(load_url, element.get("href"))
