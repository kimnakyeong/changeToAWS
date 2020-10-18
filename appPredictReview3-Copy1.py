from flask import Flask, render_template, url_for, request

from flask_restful import reqparse, Api, Resource

import pandas as pd 

from load import predict_pos_neg
import joblib


import tensorflow as tf

from tensorflow import keras

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions

from tensorflow.keras.models import load_model

from tensorflow.keras.preprocessing import image

from keras.preprocessing.image import img_to_array

import numpy as np

from PIL import Image



import os

import sys

import io

import flask

from flask import redirect, url_for, request, render_template, Response, jsonify, redirect

from flask import Flask, render_template

from flask_restful import Api

from werkzeug.utils import secure_filename
import cv2

from Foody.tasteNUMBER import product_name
from Foody.TasteFigure import product_figure
from Foody.tasteDICT import food_dictionary
from gensim.models import Word2Vec
from Word2VecModel.FoodWord2vec import foodKeyWord
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
  try:
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Virtual devices must be set before GPUs have been initialized
    print(e)
# config = tf.compat.v1.ConfigProto ()


def gender_features(word):

    return {'last_letter': word[-1]}

gender_features("나경")



def get_model():

    global model

    model = load_model('june_model.h5')

    print("*model loaded!")



def prepare_image(image, target_size):

    cvt_image =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  
    im_pil = Image.fromarray(cvt_image)
    
    # resize the array (image) then PIL image
    im_resized = im_pil.resize((64, 64))

    img_array = img_to_array(im_resized)
    
    image_array_expanded = np.expand_dims(img_array, axis = 0)
    return image_array_expanded
    


print('loading keras')

get_model()



class FlaskApiReview(Resource):        

    def post(self):

        try:

            parser = reqparse.RequestParser()

            parser.add_argument('review', type=str)

            args = parser.parse_args()



            data = args['review']

            print(data)

            #vect = cv.transform(data).toarray()

            my_prediction = predict_pos_neg(data)

            print(my_prediction)



            return {'taste': my_prediction}

        except Exception as e:

            return {'error': str(e)}



        

api.add_resource(FlaskApiReview, '/predictReview')



def on_json_loading_failed_return(e):

    return {}

#taste number

class TasteFigure(Resource):        

    def post(self):

        try:
            parser = reqparse.RequestParser()

            parser.add_argument('productName', type=str)

            args = parser.parse_args()
            
            data = args['productName']

            print(data)

            #vect = cv.transform(data).toarray()

            product_num = product_figure(data)

            print(product_num)
            
            return {'taste_item': product_num }

        except Exception as e:

            return {'error': str(e)}



        

api.add_resource(TasteFigure, '/tasteFigure')




## food keyword 수치 내보내기 수요일 작업

class FoodDICT(Resource):        

    def post(self):

        try:

            parser = reqparse.RequestParser()

            parser.add_argument('productName', type=str)

            args = parser.parse_args()

            data = args['productName']
            #vect = cv.transform(data).toarray()
            print(args)
            food_dict = food_dictionary(data)

            return food_dict

        except Exception as e:

            return {'error': str(e)}

api.add_resource(FoodDICT, '/foodDict')


## food keyword

##food word

class FoodKeyWord(Resource):        

    def post(self):

        try:

            parser = reqparse.RequestParser()

            parser.add_argument('productNameKeyWord', type=str)
            parser.add_argument('productNameList', type=str, action="append")
#             data = request.form.get('productNameKeyWord')
#             dataList = request.form.getlist('productNameList')
            args = parser.parse_args()

            data = args['productNameKeyWord']
            dataList = args['productNameList']
            print(dataList)
#             vect = cv.transform(data).toarray()
            food_dict = foodKeyWord(data, dataList)


            return food_dict

        except Exception as e:

            return {'error': str(e)}



        

api.add_resource(FoodKeyWord, '/foodKeyWord')


##food word


#taste number

class TasteNumber(Resource):        

    def post(self):

        try:
            parser = reqparse.RequestParser()

            parser.add_argument('productName', type=str)

            args = parser.parse_args()
            
            data = args['productName']

            print(data)

            #vect = cv.transform(data).toarray()

            product_num = product_name(data)

            print(product_num)

            taste_list = {}
            taste_name = ['sour','salty','bitter','sweet','hot']
            
            for i in range(len(product_num)):
                taste_list[taste_name[i]] = product_num[i]
            
            taste_test = sorted(taste_list.items(), key=lambda taste_list: taste_list[1], reverse=True)
            print(taste_test)
            
            items_taste = {}
            for test_item in taste_test:
                items_taste[test_item[0]] = test_item[1] 
            
            return {'taste': items_taste }

        except Exception as e:

            return {'error': str(e)}



        

api.add_resource(TasteNumber, '/tasteNumber')



##photo


@app.route("/predictPhoto", methods=['POST'])
def predict():
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            image = np.fromstring(flask.request.files["image"].read(),dtype=np.uint8)         
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            image = cv2.resize(image, (292, 512), interpolation=cv2.INTER_AREA)
            # 내부가 파란색으로 채워진 사각형을 그립니다. 
            
            cv2.rectangle(image,(10,90), (290, 410), (0, 0, 255), 3)
            image = image[90:410, 10:290]
           
            #이미지 전처리
          
            prepared_image = prepare_image(image, target_size=(64, 64))
          
            

            #예측
            preds = model.predict(prepared_image).tolist()         
            results = np.argmax(preds, axis=1)
            
            for i in results:
                pre_ans_str = ''
                print(i)
                if i  == 0: 
                    pre_ans_str = 2
                    print("불닭볶음면2")

                elif i == 1:
                    pre_ans_str = 17
                    print("허니")
                    
                elif i == 2: 
                    pre_ans_str = 3
                    print("자가")
                    
                elif i == 3:
                    pre_ans_str = 4
                    print("청정원 홍초 석류")

                elif i == 4: 
                    pre_ans_str = 5
                    print("브라우니")

                elif i == 5:
                    pre_ans_str = 1
                    print("신라면")
                    
                elif i == 6: 
                    pre_ans_str = 51

                elif i == 7: 
                    pre_ans_str = 0
                    food_id = 8  
                      
                elif i == 8: 
                    pre_ans_str = 0
                    print("인식불가")
                      
                
                print(str(pre_ans_str))
            r={"label": pre_ans_str}

    return flask.jsonify(r)



##photo




if __name__ == '__main__':

    app.run(host='0.0.0.0' ,port=5000 ,debug=True)
