'''
求人ボックススクレイピング
https://xn--pckua2a7gp15o89zb.com/

1ページ25件

'''
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
    
def save_to_csv(csv_file):
    if os.path.exists(csv_file):
        existing_df = pd.read_csv(csv_file)
        if set(existing_df.columns) == set(df.columns):
            df.to_csv(csv_file, mode='a', header=False, index=False, encoding='utf-8-sig')
            print(f"Data appended to {csv_file}")
        else:
            print("Error: CSV column mismatch. No data was added.")
    else:
        df.to_csv(csv_file, mode='w', header=True, index=False, encoding='utf-8-sig')
        print(f"Data written to {csv_file}")


def extract_job_data(soup, base_url):
    job_list = []
    job_elements = soup.find_all("div", class_="job-card section-bottom")
    for job in job_elements:
        title = job.find("h2").text.strip()
        category = job.find("span", class_="category").text.strip()  # 仮のクラス名
        employer = job.find("span", class_="employer").text.strip()  # 仮のクラス名
        description = job.find("div", class_="description").text.strip()  # 仮のクラス名
        salary = job.find("span", class_="salary").text.strip()  # 仮のクラス名
        job_url = urljoin(base_url, job.find("a").get("href"))

        job_list.append([title, category, employer, description, salary, job_url])
    return job_list

if __name__ == "__main__":
    load_url = "https://xn--pckua2a7gp15o89zb.com/%E7%94%9F%E6%88%90AI%E3%81%AE%E4%BB%95%E4%BA%8B"
    soup = get_soup(load_url)
    columns = ['求人タイトル', '求人募集のジャンル', '求人者', '仕事内容', '給与', 'URL']
    csv_file = 'job_listings.csv'
    
    topic = soup.find('main')
    print(topic)
    for j, element in enumerate(topic.find_all("a"), start=1):
        url = urljoin(load_url, element.get("href"))
        if url!="javascript:void(0);":
            job_data = extract_job_data(soup, load_url)
            df = pd.DataFrame(job_data, columns=columns)
            

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"error fetching {url}: {e}")
        return None

if __name__ == "__main__":
    load_url = "https://xn--pckua2a7gp15o89zb.com/%E7%94%9F%E6%88%90AI%E3%81%AE%E4%BB%95%E4%BA%8B"
    soup = get_soup(load_url)
    #topic = soup.find(class_="p-resultArea u-pdt20")
    topic = soup.find('main')
    print(topic)
    for j, element in enumerate(topic.find_all("a"), start=1):
        url = urljoin(load_url, element.get("href"))
        if url!="javascript:void(0);":
            print(f"Link {j}: {url}")
