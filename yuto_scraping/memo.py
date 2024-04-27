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
    
    topics = soup.find_all(class_="p-result_title_link s-biggerlink_link")
    print(topics)
    for j, topic in enumerate(topics, start=1):
        # ここで find('a') を使用して、各 topic 内の最初の 'a' タグを取得します。
        element = topic.find('a')
        if element:
            url = urljoin(load_url, element.get("href"))
            print(f"Link {j}: {url}")
