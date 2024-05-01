'''
求人タイトル ◯
依頼者　◯
求人募集のジャンル　◯
仕事内容
給与
案件URL
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
    load_url = "https://next.rikunabi.com/viewjob/jkf0982208cacd7a2d/?list_disp_no=49&referrer_id=cp_s00700&jrtk=5-nrt1-0-1hspvblsdk3oh800-f0982208cacd7a2d--SoBt6_M3BZ2hbexg3J0KbzkdCdPP&leadtc=n_ichiran_adnet_ttl&betskey=SoAI6_I3BZ3pgW2Xh50JbzkdCdPP"
    soup = get_soup(load_url)
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
            
    print(title, requester, category, salary, job_desc)