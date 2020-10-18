import os
import sys
import io
import flask
from flask import redirect, url_for, request, render_template, Response, jsonify, redirect
from flask import Flask, render_template
from flask_restful import Api
from werkzeug.utils import secure_filename


# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image


# app = flask.Flask(__name__)
app = Flask(__name__)
api = Api(app)

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

@app.route("/exam", methods=['POST'])
def predict():
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format(이미지 읽기)
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
            data["prediction"]=[]
            
            # print(preds)
            for i in results:
                # print (type(pre_ans))
                # pre_ans_str = ''
                print(i)
                if i  == 0: 
                    pre_ans_str = "fire"

                elif i == 1:
                    pre_ans_str = "potato"

                elif i == 2: 
                    pre_ans_str = "shin"

                else: pre_ans_str = "인식 불가"
            r={"label": pre_ans_str}
            data["prediction"].append(r)
               
        
        # return {'label':pre_ans_str}
        # return {'label': preds}
            

            # indicate that the request was a success
        # data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data) 



if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))

    app.run(debug=True)
