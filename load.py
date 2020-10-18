from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics
from tensorflow.keras.models import load_model
from konlpy.tag import Okt

import json
import os
from pprint import pprint

import nltk
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np

import re

okt = Okt()

model = models.Sequential()
#model = load_model('model.h5') -1
model = load_model('modelTaste.h5')

if os.path.isfile('train_docs.json'):
    with open('train_docs.json', 'r', encoding='UTF-8') as f:
        train_docs = json.load(f)
    with open('test_docs.json', 'r', encoding='UTF-8') as f:
        test_docs = json.load(f)
else:
    train_docs = [(row[0], tokenize(row[1])) for row in train_data]
    test_docs = [(row[0], tokenize(row[1])) for row in test_data]
    # JSON 파일로 저장
    with open('train_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(train_docs, make_file, ensure_ascii=False, indent="\t")
    with open('test_docs.json', 'w', encoding="utf-8") as make_file:
        json.dump(test_docs, make_file, ensure_ascii=False, indent="\t")

tokens = [t for d in train_docs for t in d[1]]
print(len(tokens))


text = nltk.Text(tokens, name='NMSC')

# 전체 토큰의 개수
print(len(text.tokens))

# 중복을 제외한 토큰의 개수
print(len(set(text.tokens)))            

# 출현 빈도가 높은 상위 토큰 10개
pprint(text.vocab().most_common(10))


font_fname = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
font_name = font_manager.FontProperties(fname=font_fname).get_name()
rc('font', family=font_name)


selected_words = [f[0] for f in text.vocab().most_common(10000)]


def term_frequency(doc):
    return [doc.count(word) for word in selected_words]

def tokenize(doc):
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)]

def remove(x) :
    m = re.sub(r'(?:\b[0-9a-zA-Zㄱ-ㅎㅏ-ㅣ]\b|[?!\W]+)\s*', ' ', x).strip() 
    m = " ".join(m.split())
    return m

def predict_pos_neg(review):
    review = remove(review)
    token = tokenize(review)
    print(token)
    if(review==""):
        return 0
    tf = term_frequency(token)
    print(tf)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))
    if(score > 0.5):
        print("[{}]는 {:.2f}% 확률로 맛 리뷰이지 않을까 추측해봅니다.^^\n".format(review, score * 100))
        return 1
    else:
        print("[{}]는 {:.2f}% 확률로 가격 리뷰이지 않을까 추측해봅니다.^^;\n".format(review, (1 - score) * 100))
        return 0

string = [
"불닭은 아 오늘 뭐 먹지 할때 먹으면 짱질리지 않는 맛",

"가끔 미친듯 매운거 먹고싶을때 땃이에요면삶을때콩나물 같이 넣고치즈도 넣고환타 옆에 챙기고 먹어요먹고나면 개운한기분먹고나서 매운얼얼함은 오래가지 않아요그래서 또사는듯먹을땐 이걸 왜샀지 싶은데. 먹고나면 개운함 ㅋ요즘처럼 칩콕에 스트레스 받을때한번씩 먹어볼만치즈가들어간 까르보나라불닭면도 있던데난 오리지날 ㅋ",

"무료배송에 가격도 마트보다 천원정도나 싸니 여기말고 다른데서 살 이유가 없네요 정말 조아용",

"이 라면이야 뭐제 최애라면이고요하나밖에 안남으면 수전증옵니다늘 재고가 떨어질 날이 없는 라면부디 이 맛이 바뀌지만 않았으면 하는 바램뿐입니다가끔 짜장라면과 1대1 비율로 같이 끓여불닭게티로 먹는데 ㄹㅇ ㅎㅈㅁ...매운 맛은 줄고 풍미는 늘고꼭 도전해보시길 바래요!",

"다 좋은데 택배에 받는사람뿐만아니라 보내는사람도 적혀있음 좀 더 좋을꺼같아여 ㅜㅜㅜㅜ 전당연히 보내는사람이 적혀있는줄알고 말을 안했는데 받는이름만 있어 당황했답니다",

"아이들이 좋아해서 자주 주문해어 먹고 있어요가격 착하고 배송 빠르고 집앞까지 가져다주시니 너무 좋아요",

"여러개 같이 구매 하면 조은데 딸랑 하개 밖에 주문이 안 되네요..ㅠㅠ급할때 시켜 먹기 좋은 듯해요",

"맛",

"마시땅",

"맛있어요",
"맛있어요~~~~",
"맛있다!!!!!",
"맛좋다.",
"많이 맵네요..",
""
]

# predict_pos_neg("올해 최고의 영화! 세 번 넘게 봐도 질리지가 않네요.")
# predict_pos_neg("배경 음악이 영화의 분위기랑 너무 안 맞았습니다. 몰입에 방해가 됩니다.")
# predict_pos_neg("주연 배우가 신인인데 연기를 진짜 잘 하네요. 몰입감 ㅎㄷㄷ")
# predict_pos_neg("믿고 보는 감독이지만 이번에는 아니네요")
# predict_pos_neg("바삭바삭한 치킨을 3가지 버전으로 맛 볼 수 있다는 게 이 집의 장점이네요 맛있게 잘 먹었습니다")
# predict_pos_neg("주연배우 때문에 봤어요")

# predict_pos_neg("깔끔하고 맛있었어요")
# predict_pos_neg("지점별로 편차가 심하다고 하는데 이곳은 만족스러웠습니다")
# predict_pos_neg("치킨튀김이살아잇네요 양이많이 완전 굿굿")
# predict_pos_neg("맛있어요 ㅠㅠ 사진은 한장만 찍었어요 배가 넘 고파가지구")

for i in string:
    predict_pos_neg(i)