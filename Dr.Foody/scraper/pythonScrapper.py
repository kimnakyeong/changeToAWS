import requests
from bs4 import BeautifulSoup



indeed = "https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit=50"
r = requests.get(indeed)
# print(r.text)

soup_indeed = BeautifulSoup(r.text, "html.parser")

pagination = soup_indeed.find("div", {"class":"pagination"})

pages = pagination.find_all("a")
spans = []
for page in pages:
    spans.append(page.find("span"))

print(spans[:-1]) 