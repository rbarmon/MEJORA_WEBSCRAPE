import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os
import time

def get_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
def save_to_csv(df, csv_file):
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

def extract_job_data(url):
    try:
        job_list = []
        soup = get_soup(url)
        if not soup:
            return None

        title = soup.find("h1", class_="rn3-companyOfferHeader__heading").text.strip()
        requester, category = None, None
        for element in soup.find_all(class_="rn3-companyOfferCompany__info"):
            header = element.find(class_="rn3-companyOfferCompany__heading").text.strip()
            text = element.find(class_="rn3-companyOfferCompany__text").text.strip()
            if header == "社名":
                requester = text
            elif header == "事業内容":
                category = text

        job_desc, salary = None, None
        for element in soup.find_all("div", class_="rn3-companyOfferRecruitment__info"):
            header = element.find(class_="rn3-companyOfferRecruitment__heading").text.strip()
            text = element.find(class_="rn3-companyOfferRecruitment__text").text.strip()
            if header == "仕事内容":
                job_desc = text
            elif header == "給与":
                salary = text

        if title and category and job_desc:
            job_list.append([title, category, requester, job_desc, salary, url])
        return job_list
    
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None
        
def next_page(load_url, soup):
    next_page_element = soup.find(class_="rnn-pagination__next")
    if next_page_element and next_page_element.find("a"):
        next_url = urljoin(load_url, next_page_element.find("a").get("href"))
        return get_soup(next_url), next_url
    return None, None

if __name__ == "__main__":
    csv_dir = './yuto_scraping'
    csv_file = os.path.join(csv_dir, 'test.csv')
    
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
        
    load_url = "https://next.rikunabi.com/rnc/docs/cp_s00700.jsp?leadtc=n_ichiran_panel_submit_btn"
    soup = get_soup(load_url)
    columns = ['求人タイトル', '求人募集のジャンル', '依頼者', '仕事内容', '給与', 'URL']
    count = 0 
    num = 0
    data_collected = []
    while count < 50 and soup:
        job_elements = soup.find_all("a", href=True)
        for element in job_elements:
            url = urljoin(load_url, element.get("href"))
            urls = list(url.split('/'))
            num += 1
            if urls[3]=="viewjob" and num % 3 ==0:
                print(f"Scraping: {url}")
                job_data = extract_job_data(url)
                if job_data:
                    df = pd.DataFrame(job_data, columns=columns)
                    save_to_csv(df, csv_file)
                    count += 1
                    if count > 50:
                        break
        if count < 50:
            soup, load_url = next_page(load_url, soup)
            if not soup:
                print("No more pages to scrape.")
                break
