import os
import sys
import io
import flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
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


app = flask.Flask(__name__)

def get_model():
    global model
    model = load_model('food_final.h5')
    model.summary()
    print("*model loaded!")
# model_path = './food_final.h5'
# model = load_model(model_path)

# image_path = './shin.jpg'
# print('model loaded. start Serving')


def prepare_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
  
    return image

print('loading keras')
get_model()


@app.route('/', methods=['GET'])
def index():
    return 'hello'


@app.route("/predict", methods=['POST'])
def predict():
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            # preprocess the image and prepare it for classification
            prepared_image = prepare_image(image, target_size=(64, 64))
            
            # classify the input image and then initialize the list
            # of predictions to return to the client
            preds = model.predict(prepared_image).tolist()         
            preds = np.argmax(preds, axis=1)
            print(preds)
            for i in preds:
                pre_ans = i.argmax()
                print(pre_ans)
                pre_ans_str = ''
                if pre_ans == 0: 
                    pre_ans_str = "fire"

                elif pre_ans == 1:
                    pre_ans_str = "potato"

                elif pre_ans == 2: 
                    pre_ans_str = "shin"

                else: pre_ans_str = "모름"

               
        
        return pre_ans_str
        # return {'label': preds}
            

            # indicate that the request was a success
        data["success"] = True

    # return the data dictionary as a JSON response
    # return jsonify(preds).data 

if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))

    app.run()