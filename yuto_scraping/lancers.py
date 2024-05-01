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
                
        if title and category and job_desc:
            job_list.append([title, category, job_desc, salary, url])
        return job_list
    
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None
        
def next_page(load_url, soup):
    try:
        next_page_element = soup.find(class_="c-pager__item c-pager__item--next").find("a")
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
    csv_file = os.path.join(csv_dir, 'listings_joblist.csv')
    
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
        
    load_url = "https://www.lancers.jp/work/search/salesmarketing?open=1&ref=header_menu&show_description=1&sort=client&work_rank%5B%5D=0&work_rank%5B%5D=2&work_rank%5B%5D=3"
    soup = get_soup(load_url)
    columns = ['求人タイトル', '求人募集のジャンル', '仕事内容', '給与', 'URL']
    total_data_collected = 0
    
    while total_data_collected < 50:
        if soup:
            topic = soup.find(class_="p-search-job__right")
            if topic:
                for element in topic.find_all('a'):            
                    url = urljoin(load_url, element.get("href"))
                    urls = list(url.split('/'))
                    if urls[-2] == "detail":
                        print(f"Scraping: {url}")
                        job_data = extract_job_data(url)
                        if job_data:
                            df = pd.DataFrame(job_data, columns=columns)
                            save_to_csv(df, csv_file)
                            total_data_collected += len(df)
                            if total_data_collected >= 50:
                                print("Reached 50 data entries.")
                                break
        if total_data_collected < 50:
            soup, load_url = next_page(load_url, soup)
            if soup is None:
                print("No more pages to scrape or failed to fetch next page.")
                break
