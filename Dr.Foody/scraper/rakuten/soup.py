import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import re


URL = 'https://search.rakuten.co.jp/search/mall/%E3%83%9B%E3%83%B3%E3%83%81%E3%83%A7/?s=5'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
URLS = []
review_all = []


# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
# result = requests.get(URL, headers=headers)

# def get_last_page(): # 쿠팡은 10까지 돼서 last_page 구할 필요 없음
#     driver = webdriver.Chrome("C:/PythonSelenium/chromedriver.exe")
#     driver.get(URL)
#     driver.implicitly_wait(1)
#     req = driver.page_source
#     soup = BeautifulSoup(req, "html.parser")
#     pages = soup.find("span", {"class": "count"}).get_text()

def get_urls():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find_all("div", {"class":"content title"})
    # last_page = pages[-2].get_text(strip=True)
    for page in pages:
        food = page.find('a')['title']
        not_include = ['オジンオ','カリーブルダック','チーズブルダック','カルボブルダック','農心','お菓子セット','チーズラーメン','カルボナーラ']
        if not any(word in food for word in not_include): 
            URLS.append(page.find('a')['href'])




def extract_review(html):
    #nickname, age, gender, review, rate
    nickname = html.find("dt", {"class": "revUserFaceName"}).get_text(strip=True)
    age = html.find("span", {"class": "revUserFaceDtlTxt"})
    age_gender = age.find("span")
    rate = html.find("span", {"class": "revUserRvwerNum"}).get_text()
    review = html.find("dt", {"class": "revRvwUserEntryTtl"})
    review2 = html.find("dd", {"class": "revRvwUserEntryCmt"})

    if (age_gender == None):
        age = ""
        gender = ""
    else: 
        age_gender = age_gender.get_text()
        age = age_gender[:3]
        gender = age_gender[4:]
    if (review == None):
        review = ""
    else: 
        review = review.get_text()
    if(review2 == None):
        return False
    else: 
        review2 = review2.get_text()
    return {
        "nickname": nickname,
        "age": age,
        "gender": gender,
        "rate" : rate, # 추가 
        "review" : review+review2,
    }



def extract_reviews(last_page, url_review): # 횟수 받아서 실질적으로 요청해야 하는 곳.
    url = url_review[:-4] ##
    for page in range(last_page):
        print(f"Scrapping review: page {page}")
        result = requests.get(f"{url}{page+1.1}/", headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "hreview"})
        for result in results:
            review = extract_review(result)
            if(review):
                review_all.append(review)

def go_to_url(url):
    driver = webdriver.Chrome("C:/PythonSelenium/chromedriver.exe")
    driver.get(url)
    driver.implicitly_wait(1)
    pages = driver.find_element_by_class_name("all-shops-recommend-settings-api")
    url_review = pages.get_attribute('data-item-id')
    return url_review

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("span", {"class":"Count"})
    if (pages == None):
        return False
    else:
        #pages = int(pages.get_text())
        number = re.sub('[^0-9]', '', pages.get_text())
        pages = int(number)


    if(pages%15 == 0):
        last_page = pages//15
    else:
        last_page = pages//15 + 1
    return last_page


def get_reviews():
    get_urls() # 각 사이트 url을 가져옴.
    print(URLS)
    for url in URLS:
        print(url)
        url_number = go_to_url(url) # URL당, 리뷰가 있는 url 존재
        url_review = "https://review.rakuten.co.jp/item/1/"+url_number+"/1.1/"
        last_page = get_last_page(url_review)
        extract_reviews(last_page, url_review)

def save_to_file(jobs):
    file = open("rakuten_reviews.csv", "w", -1, "utf-8") #file을 열고 file 변수에 저장
    writer = csv.writer(file)         #writer 작성
    writer.writerow(["nickname", "age", "gender", "rate", "review"])
    for job in jobs :
        writer.writerow(list(job.values()))
        # writer.writerow(job.values())
    return

get_reviews()
save_to_file(review_all)
# last_job = get_jobs()
# print(last_job)