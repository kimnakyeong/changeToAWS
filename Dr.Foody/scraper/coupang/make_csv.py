import csv

def save_to_file(jobs):
    file = open("coupang.csv", "w", newline='', encoding="utf-8") #file을 열고 file 변수에 저장
    writer = csv.writer(file)         #writer 작성
    writer.writerow(["product", "username", "nation", "age", "review"])
    for job in jobs :
        writer.writerow(list(job.values()))
        # writer.writerow(job.values())
    return