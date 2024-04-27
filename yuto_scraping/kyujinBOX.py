'''
求人ボックススクレイピング
https://xn--pckua2a7gp15o89zb.com/

1ページ25件

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
    load_url = "https://xn--pckua2a7gp15o89zb.com/%E7%94%9F%E6%88%90AI%E3%81%AE%E4%BB%95%E4%BA%8B"
    soup = get_soup(load_url)
    

    
    topic = soup.find(class_="p-resultArea u-pdt20")
    print(topic)
    for j, element in enumerate(topic.find_all("a"), start=1):
        url = urljoin(load_url, element.get("href"))
        print(f"Link {j}: {url}")
