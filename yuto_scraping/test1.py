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
        print(f"error fetching {url}: {e}")
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
            return
        
        title = category = salary = job_desc = None
        
        h1tag = soup.find(class_="c-heading c-heading--lv1")
        if h1tag:
            category = h1tag.find("span").text.strip() if h1tag.find("span") else None
            if h1tag.span:
                h1tag.span.decompose()
            title = h1tag.text.strip()
        
        dltag = soup.find_all("dl", class_='c-definition-list')
        for dl in dltag:
            dttag = dl.find("dt").text.strip()
            if dttag == "提示した予算":
                salary = dl.find("dd").text.strip()
            if dttag == "依頼概要":
                job_desc = dl.find("dd").text.strip()
                
        if title is not None and category is not None and job_desc is not None:
            job_list.append([title, category, job_desc, salary, url])
        return job_list
    
    except AttributeError as e:
        print("エラーが発生しました:", e)
    except Exception as e:
        print("エラーが発生しました:", e)
        
if __name__ == "__main__":
    load_url = "https://next.rikunabi.com/rnc/docs/cp_s00700.jsp?leadtc=n_ichiran_panel_submit_btn"
    soup = get_soup(load_url)
    columns = ['求人タイトル', '求人募集のジャンル', '仕事内容', '給与', 'URL']
    csv_file = './yuto_scraping/job_listings.csv'
    count =0
    topic = soup.find(class_="rnn-group rnn-group--xm")
    # for element in topic.find_all('a'):            
    #     url = urljoin(load_url, element.get("href"))
    #     urls = list(url.split('/'))
    #     count += 1
    #     if urls[3]=="viewjob" and count % 3 ==0:
    #         print(url)
    
    next_page_element = soup.find(class_="rnn-pagination__next").find("a")
    if next_page_element:
        url = urljoin(load_url, next_page_element.get("href"))
        print(url)
