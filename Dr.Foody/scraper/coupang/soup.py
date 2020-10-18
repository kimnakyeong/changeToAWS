import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
import re


URL = 'https://www.coupang.com/vp/products/14344?itemId=13412321&vendorItemId=3000014958&q=%EB%B6%88%EB%8B%AD%EB%B3%B6%EC%9D%8C%EB%A9%B4&itemsCount=36&searchId=155de4aa76ce40a2918d7398a8a211ef&rank=0&isAddedCart='
R_URL1 = 'https://www.coupang.com/vp/product/reviews?productId=14344'
R_URL2 = 'https://www.coupang.com/vp/product/reviews?productId=117523085'
R_URL3 = 'https://www.coupang.com/vp/product/reviews?productId=3630576'
R_URL4 = 'https://www.coupang.com/vp/product/reviews?productId=80669031'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

p=re.compile()


# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
# result = requests.get(URL, headers=headers)

def get_last_page(): # 쿠팡은 10까지 돼서 last_page 구할 필요 없음
    driver = webdriver.Chrome("C:/PythonSelenium/chromedriver.exe")
    driver.get(URL)
    
    driver.implicitly_wait(1)
    req = driver.page_source
    soup = BeautifulSoup(req, "html.parser")
    pages = soup.find("span", {"class": "count"}).get_text()
    if(pages[1] != ",") :
        pages = int(pages[0:2])+ int(pages[3])
    else : 
        pages = int(pages[0]+pages[2])
    if(pages%100==0):
        last_page = pages
    else:
        last_page = pages+1
    return last_page

def extract_review(html):
    product = html.find("div", {"class": "sdp-review__article__list__info__product-info__name"}).get_text(strip=True)
    review = html.find("div", {"class": "sdp-review__article__list__review__content js_reviewArticleContent"})
    nation = "korea"
    user_name = html.find("span", {"class": "sdp-review__article__list__info__user__name js_reviewUserProfileImage"}).get_text(strip=True)
    coupang_survey = html.find("span", {"class": "sdp-review__article__list__survey__row__answer"})
    if(coupang_survey == None):
        coupang_survey = ""
    else:
        coupang_survey = coupang_survey.get_text(strip=True)
    
    file_not_include = ['배달', '배송', '배승', '빠른', '빠르', '빨라', '빨리', '느리', '느린', '느려', '늦게']
    
    if(review == None):
        return False
    elif any(format in review.get_text(strip=True) for format in file_not_include):
        return False
    else:
        if(user_name)

    return {
        "product": product,
        "user_name" : user_name,
        "nation" : nation, # 추가
        "age" : "20",
        "review": review.get_text(strip=True),
    }



def extract_reviews(last_page, url): # 횟수 받아서 실질적으로 요청해야 하는 곳.
    reviews = []
    for page in range(last_page):
        print(f"Scrapping review: page {page}")
        result = requests.get(f"{url}&page={page+1}&size=100", headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("article", {"class": "sdp-review__article__list js_reviewArticleReviewList"})
        for result in results:
            review = extract_review(result)
            if(review):
                reviews.append(review)
    return reviews



def get_reviews():
    last_page = 10
    review1 = extract_reviews(last_page, R_URL1) #
    review2 = extract_reviews(last_page, R_URL2)
    review3 = extract_reviews(last_page, R_URL3)
    review4 = extract_reviews(last_page, R_URL4)
    review = review1 + review2 + review3 + review4
    return review

# last_job = get_jobs()
# print(last_job)