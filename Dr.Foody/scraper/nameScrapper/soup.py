import requests 
from bs4 import BeautifulSoup
from selenium import webdriver

URL = "https://koreanname.me/api/rank/2008/2020/"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def extract_name(html):
    name = ""
    return {
        "name": name
    }

def extract_names(last_page, url): # 횟수 받아서 실질적으로 요청해야 하는 곳.
    reviews = []
    for page in range(last_page):
        print(f"Scrapping review: page {page}")
        result = requests.get(f"{url}{page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("article", {"class": "sdp-review__article__list js_reviewArticleReviewList"})
        for result in results:
            review = extract_name(result)
            if(review):
                reviews.append(review)
    return reviews


def get_names():
    last_page = 350
    name = extract_names(last_page, URL)
    return name
