import sys

def save_to_file(names):
    file = open("male.txt", "w") #file을 열고 file 변수에 저장
    for name in names :
        file.write(name+'\n')
        # writer.writerow(job.values())
    return