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
    
# def extract_job_data(url):
    # soup = get_soup(load_url)
    # h1tag = soup.find(class_="c-heading c-heading--lv1")
    # type = h1tag.find("span").text.strip()
    # if h1tag.span:
    #     h1tag.span.decompose()
    # title = h1tag.text.strip()

if __name__ == "__main__":
    load_url = "https://www.lancers.jp/work/search?open=1&ref=header_menu"
    soup = get_soup(load_url)
    

    
    topics = soup.find_all(class_="p-search-job-media__title c-media__title")
    for topic in topics:
        for element in topic.find("a"):
            print(element)
            
            url = urljoin(load_url, topic.get("href"))
            urls = list(url.split('/'))
            if urls[-2]=="detail":
                print(url)
        
        # if topic.find(class_="p-search-job-media__title c-media__title"):
            
        #     tags_to_remove = soup.find_all('ul', class_='p-search-job-media__tags')
        #     for tag in tags_to_remove:
        #         tag.decompose()
        #     title = topic.get_text(strip=True)
        #     print(title)

