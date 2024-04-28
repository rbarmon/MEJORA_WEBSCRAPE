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
    h1tag = soup.find(class_="c-heading c-heading--lv1")
    type = h1tag.find("span").text.strip()
    if h1tag.span:
        h1tag.span.decompose()
    title = h1tag.text.strip()
