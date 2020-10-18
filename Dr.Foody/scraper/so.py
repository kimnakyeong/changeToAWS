import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://stackoverflow.com/jobs?q=python&sort=i"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html): #html = soup
    title = html.find("div", {"class":"grid--cell fl1"}).find("h2").find("a")["title"]
    company, location = html.find("h3", {
        "class": "fc-black-700"
        }).find_all("span", recursive=False)
    company=company.get_text(strip=True)
    location=location.get_text(strip=True)
    job_id = html["data-jobid"]
    return {
        "title": title, 
        "company": company, 
        "location": location, 
        "link": f"https://stackoverflow.com/jobs/{job_id}"
    }
    # company, location = html.find("h3", { # 2개의 item이 있다는 것을 아니까 2개의 변수에 담음. unpacking 방법
    #     "class": "fc-black-700"
    # }).find_all(
    #     "span", recursive=False) #recursive = False : 좀 더 깊은 레벨로 가지말고, 첫번째 depth만 가져오기
    # company = company.get_text(strip=True).strip("-") #strip=True
    # location = location.get_text(strip=True)
    # return {"title": title}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: page {page}")        
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page() # 1. 마지막 페이지 추출
    # page 갯수만큼 request를 보내야 한다. 
    jobs = extract_jobs(last_page) # 2. 1페이지부터 마지막 페이지 까지 request 날림. 
    return jobs