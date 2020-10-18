import requests 
from bs4 import BeautifulSoup




URL = 'https://www.coupang.com/vp/products/14344?itemId=13412321&vendorItemId=3000014958&q=%EB%B6%88%EB%8B%AD%EB%B3%B6%EC%9D%8C%EB%A9%B4&itemsCount=36&searchId=155de4aa76ce40a2918d7398a8a211ef&rank=0&isAddedCart='
R_URL = 'https://www.coupang.com/vp/product/reviews?productId=14344&page=1&size=100'

review = []
#for page in range(last_page):
page = 1
print(f"Scrapping review: page {page}")
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
result = requests.get(R_URL, headers=headers)
print(result.status_code)
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
# soup = BeautifulSoup(result.text, "html.parser")
# results = soup.find_all("article", {"class": "sdp-review__article__list js_reviewArticleReviewList"})
