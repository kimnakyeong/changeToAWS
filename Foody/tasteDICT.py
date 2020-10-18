import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def food_dictionary(name):
    
    if name == "ブルダック 炒め麺":
        file_name = '/home/LG/Foody/wordsBULNIHONGOASD.txt'
    elif name == "마시는 홍초":
        file_name = '/home/LG/Foody/reviewHBLOGHASD.txt'
    elif name == "辛ラーメン":
        file_name = '/home/LG/Foody/wordsSHINNIHONGOASD.txt'

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

    shin = ["새콤달콤", "상큼", "신맛", "새콤달콤"]
    shin2 = []
    zz = ["담백", "밍밍", "간장", "나트륨", "짜"]
    zz2 = []
    ss = ["쓴맛"]
    ss2 = []
    dan = ["甘い", "甘み", "甘辛い", "설탕물", "새콤달콤", "단맛"]
    dan2 = []
    mae = ["辛い", "辛さ", "激辛", "リピート", "痛い", "甘辛い", "辛", "辛党", "病みつき", "からい", "辛味","出汁", "まろやか", "唐辛子"]
    mae2 = []
    
    taste_num = {"새콤달콤":4, "상큼":2, "신맛":4, "담백":1, "밍밍":1, "쓴맛":2, "甘い":2, "甘み":2, "甘辛い":1, "설탕물": 4, "辛い":3, "辛さ":3, "激辛":4, "リピート":2, "痛い":4, "辛":4, "辛党":5, "病みつき":5, "からい":3, "辛味":4, "出汁":5, "病みつき":5, "からい":3, "辛味":3, "出汁":5, "まろやか":-3, "唐辛子":4}
    taste_sum = [0, 0, 0, 0, 0] 
    taste_count = [0,0,0,0,0]
   
    sentence_dict = {}

    list_dict = []

    for sentence in review_key:
        content_dict = {}
        if sentence in taste_num.keys():
            print(sentence)
            print(review_val[review_key.index(sentence)])
            content_dict["keyword"] =  sentence
            content_dict["number"] = review_val[review_key.index(sentence)]
        if content_dict:
            list_dict.append(content_dict)

    sentence_dict["keyword_dict"] = list_dict
    
    return sentence_dict