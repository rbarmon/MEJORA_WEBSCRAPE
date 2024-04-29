'''
求人タイトル
求人募集のジャンル
取得コードサンプル
'''

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
    load_url = "https://www.lancers.jp/work/detail/4960062"
    soup = get_soup(load_url)
    # 求人タイトル title ＆カテゴリー category
    h1tag = soup.find(class_="c-heading c-heading--lv1")
    category = h1tag.find("span").text.strip()
    if h1tag.span:
        h1tag.span.decompose()
    title = h1tag.text.strip()
    
    #仕事内容 job_desc ＆給与 salary
    dltag = soup.find_all("dl",class_='c-definition-list')
    for dl in dltag:
        dttag = dl.find("dt").text.strip()
        if dttag=="提示した予算":
            salary = dl.find("dd").text.strip()
        if dttag=="依頼概要":
            job_desc = dl.find("dd").text.strip()
            
    print(title, category, salary, job_desc)