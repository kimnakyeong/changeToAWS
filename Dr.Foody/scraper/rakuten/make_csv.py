import csv

def save_to_file(jobs):
    file = open("coupang_reviews.csv", "w", -1, newline='', "utf-8") #file을 열고 file 변수에 저장
    writer = csv.writer(file)         #writer 작성
    writer.writerow(["product", "review", "nation", "user_name", "coupang_survey"])
    for job in jobs :
        writer.writerow(list(job.values()))
        # writer.writerow(job.values())
    return