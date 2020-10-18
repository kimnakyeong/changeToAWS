import csv

def save_to_file(jobs):
    file = open("jobs.csv", "w", -1, "utf-8") #file을 열고 file 변수에 저장
    writer = csv.writer(file)         #writer 작성
    writer.writerow(["title", "company", "location", "link"])
    for job in jobs :
        writer.writerow(list(job.values()))
        # writer.writerow(job.values())
    return