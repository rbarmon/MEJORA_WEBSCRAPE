import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os

def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"error fetching {url}: {e}")
        return None



if __name__ == "__main__":
    load_url = "https://furien.jp/projects/617941?utm_source=kyujinbox&utm_medium=cpc&utm_campaign=furien&argument=hGPKreyn&dmai=furien_kyujinbox"
    soup = get_soup(load_url)
    
    topic = soup.find("div", class_="job-card section-bottom")
    #print(topic)
    h3tag = topic.find("h3",class_="job-card__title text-br")
    title = h3tag.find("span").text.strip()
    print(title)
    
    
    # for j, element in enumerate(topic.find_all("a"), start=1):
    #     url = urljoin(load_url, element.get("href"))
    #     if url!="javascript:void(0);":
    #         extract_job_data(url)
            