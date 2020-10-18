import urllib.request
import json

URL = "https://koreanname.me/api/rank/2008/2020/"

file = open("C:/Users/LG/Desktop/캡스톤 자료/크롤링/nomad_scraping/nomad_scaper/nameScrapper/test.txt", "w", -1, "utf-8")

for i in range(10):
    print(f"{i} scrapping")
    req = urllib.request.urlopen(f"{URL}{i+1}")
    res = req.readline()
    j = json.loads(res)
    f_array = j["male"]
    for name in f_array:
        file.write(f"{name['name']}\n")