import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def product_figure(name):
    
    if name == "ブルダック炒め麵":
        file_name = '/home/LG/Foody/wordsBULDAK2014ASD.txt'
    elif name == "마시는 홍초":
        file_name = '/home/LG/Foody/reviewHBLOGHASD.txt'
    elif name == "辛ラーメン":
        file_name = '/home/LG/Foody/wordsSHINASD.txt'

    pandsa = pd.read_csv(file_name, names=["taste"])
    panda_ary = pandsa.taste.tolist()
    review_key =[]
    review_val =[]

    for panda in panda_ary:
        list = panda.split(" ")
        review_key.append(list[1])
        review_val.append(int(list[len(list)-1]))

    sentences = {}
    for i in range(len(review_key)):
        sentences[review_key[i]] = review_val[i]

    taste_name = ['sour','salty','bitter','sweet','hot']


    shin = ["새콤달콤", "상큼", "신맛", "새콤달콤"]
    zz = ["담백", "밍밍", "간장", "나트륨", "짜"]
    ss = ["쓴맛"]
    dan = ["달콤", "감미", "달큼", "설탕물", "새콤달콤", "단맛"]
    mae = ["알싸", "매운맛", "매콤", "눈물", "화끈하", "지옥", "빨개지", "피똥", "눈물나", "도전", "고추", "맵", "칼칼"]

    taste_num = {"새콤달콤":4, "상큼":2, "신맛":4, "담백":1, "밍밍":1, "쓴맛":2, "달콤":3, "감미":3, "달큼":2, "설탕물": 4, "알싸":2, "매운맛":4, "매콤":4, "도전":4, "고추":4, "눈물":4, "화끈하":4, "지옥":5, "빨개지":5, "간장":3, "나트륨":3, "피똥":5, "눈물나":5, "단맛":4, "맵":3, "짜":3, "칼칼":3}
    taste_sum = [0, 0, 0, 0, 0] 
    taste_count = [0,0,0,0,0]


    dict_array = []
    taste_dict = {}
        

    for sentence in review_key:
        if sentence in shin :
            taste_sum[0]+=taste_num[sentence]*sentences[sentence]
            taste_count [0]+=1*sentences[sentence]
        if sentence in zz:
            taste_sum[1]+=taste_num[sentence]*sentences[sentence]
            taste_count [1]+=1*sentences[sentence]
        if sentence in ss:
            taste_sum[2]+=taste_num[sentence]*sentences[sentence]
            taste_count [2]+=1*sentences[sentence]
        if sentence in dan:
            taste_sum[3]+=taste_num[sentence]*sentences[sentence]
            taste_count [3]+=1*sentences[sentence]
        if sentence in mae:
            taste_sum[4]+=taste_num[sentence]*sentences[sentence]
            taste_count [4]+=1*sentences[sentence]

    returnDict = {}
    returnval = []

    for i in range(len(taste_sum)):
        if taste_count[i] == 0 :
            returnval.append(0)
        else:
            returnval.append(taste_sum[i]/taste_count[i])
            
    returnDict["taste_rate"] = returnval
    returnDict["taste_count"] = taste_count
    returnDict["taste_sum"] = taste_sum
    
    lists = []
    
    for i in range(len(taste_count)):
        lists_dict = {}
        lists_dict["taste_name"] = taste_name[i]
        lists_dict["taste_count"] = taste_count[i]
        lists_dict["taste_sum"] = taste_sum[i]
        lists_dict["taste_rate"] = returnval[i]
        if lists_dict :
            lists.append(lists_dict)
        
    
    return lists