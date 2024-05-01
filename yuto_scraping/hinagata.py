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
        
        # 求人タイトル title ＆依頼者 requester ＆ 仕事内容(事業内容) category
        title = soup.find("h1",class_="rn3-companyOfferHeader__heading").text.strip()
        h3 = soup.find_all(class_="rn3-companyOfferCompany__info")
        for i in h3:
            element = i.find(class_="rn3-companyOfferCompany__heading").text.strip()
            if element == "社名":
                requester = i.find(class_="rn3-companyOfferCompany__text").text.strip()
            if element == "事業内容":
                category = i.find(class_="rn3-companyOfferCompany__text").text.strip()
        
        # #仕事内容 job_desc ＆給与 salary
        div = soup.find_all("div",class_='rn3-companyOfferRecruitment__info')
        for j in div:
            h3tag = j.find(class_="rn3-companyOfferRecruitment__heading").text.strip()
            if h3tag == "仕事内容":
                job_desc = j.find(class_="rn3-companyOfferRecruitment__text").text.strip()
            if h3tag == "給与":
                salary = j.find(class_="rn3-companyOfferRecruitment__text").text.strip()
                
        if title and category and job_desc:
            job_list.append([title, category, requester, job_desc, salary, url])
        if job_list:
            return job_list
        else:
            return None
    
    except Exception as e:
        print(f"エラーが発生しました: {url}, {e}")
        return None
        
def next_page(load_url, soup):
    try:
        next_page_element = soup.find(class_="rnn-pagination__next").find("a")
        if next_page_element:
            url = urljoin(load_url, next_page_element.get("href"))
            return get_soup(url), url
        else:
            return None, None
    except Exception as e:
        print(f"Error in finding next page: {e}")
        return None, None

if __name__ == "__main__":
    csv_dir = './yuto_scraping'
    csv_file = os.path.join(csv_dir, 'test.csv')
    
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
        
    load_url = "https://next.rikunabi.com/rnc/docs/cp_s00700.jsp?leadtc=n_ichiran_panel_submit_btn"
    soup = get_soup(load_url)
    columns = ['求人タイトル', '求人募集のジャンル', '依頼者', '仕事内容', '給与', 'URL']
    count =0
    if soup:
        for _ in range(5): 
            topic = soup.find(class_="rnn-group rnn-group--xm")
            if topic:
                for element in topic.find_all('a'):            
                    url = urljoin(load_url, element.get("href"))
                    urls = list(url.split('/'))
                    count += 1
                    if urls[3]=="viewjob" and count % 3 ==0:
                        print(f"Scraping: {url}")
                        job_data = extract_job_data(url)
                        if job_data:
                            df = pd.DataFrame(job_data, columns=columns)
                            save_to_csv(df, csv_file)
            soup, load_url = next_page(load_url, soup)
            if soup is None:
                break
