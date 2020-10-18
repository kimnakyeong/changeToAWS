from flask import Flask, render_template, url_for, request
from flask_restful import reqparse, Api, Resource
import pandas as pd 
from load import predict_pos_neg

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


app = Flask(__name__)
api = Api(app)

def gender_features(word):
    return {'last_letter': word[-1]}
gender_features("나경")

def get_model():
    global model
    model = load_model('food_final.h5')
    print("*model loaded!")

def prepare_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image

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


##photo

@app.route("/predictPhoto", methods=['POST'])
def predict():
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format(이미지 읽기)
            print(flask.request.files)
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            # image = Image.open(image)
        
            # preprocess the image and prepare it for classification
            #이미지 전처리
            prepared_image = prepare_image(image, target_size=(64, 64))
            # print(prepared_image)
            
            # classify the input image and then initialize the list
            # of predictions to return to the client

            #예측
            preds = model.predict(prepared_image).tolist()         
            results = np.argmax(preds, axis=1)
            
            # print(preds)
            for i in results:
                # print (type(pre_ans))
                # pre_ans_str = ''
                if i  == 0: 
                    pre_ans_str = 2
                    print("신라면")
                elif i == 1:
                    pre_ans_str = 3
                    print("불닭")

                elif i == 2: 
                    pre_ans_str = 1
                    print("자가비")

                else: pre_ans_str = "인식 불가"
            r={"label": pre_ans_str}
            # data["prediction"].append(r)
               
        
        # return {'label':pre_ans_str}
        # return {'label': preds}
            

            # indicate that the request was a success
        # data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(r)

##photo



# @app.route('/', methods=['GET'])
# def home():
#     return render_template('home.html')
# #    return render_template('home.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     request.on_json_loading_failed = on_json_loading_failed_return
#     print(request.get_json())
#     if request.method == 'POST':
#         message = request.form['message']
#         #왜 이렇게 쓴 걸까?
#         data = message
#         #vect = cv.transform(data).toarray()
#         my_prediction = obj.classify(gender_features(data))
#         print(my_prediction)
#     return 
# #    return render_template('result.html', prediction = my_prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5000 ,debug=True)